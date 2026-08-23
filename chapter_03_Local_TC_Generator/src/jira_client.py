import re
import requests
from requests.auth import HTTPBasicAuth
from config_store import get_setting


class JiraError(Exception):
    pass


class ConnectionError(JiraError):
    pass


class AuthenticationError(JiraError):
    pass


class NotFoundError(JiraError):
    pass


def _build_url(path: str) -> str:
    base = get_setting("jira_url").rstrip("/")
    return f"{base}{path}"


def fetch_ticket(ticket_key: str) -> dict:
    """Fetch a Jira ticket and return {key, summary, description, acceptance_criteria}."""
    email = get_setting("jira_email")
    token = get_setting("jira_api_token")

    if not email or not token:
        raise AuthenticationError(
            "Jira credentials not configured. Go to Settings page to set them up."
        )

    url = _build_url(f"/rest/api/2/issue/{ticket_key}")

    try:
        resp = requests.get(
            url,
            auth=HTTPBasicAuth(email, token),
            headers={"Accept": "application/json"},
            timeout=15,
        )
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            f"Cannot reach Jira at {get_setting('jira_url')}. Check the URL in Settings."
        )
    except requests.exceptions.Timeout:
        raise ConnectionError("Jira request timed out. Check your network or Jira URL.")

    if resp.status_code == 401:
        raise AuthenticationError(
            "Jira authentication failed. Check your email and API token in Settings."
        )
    if resp.status_code == 404:
        raise NotFoundError(f"Ticket **{ticket_key}** not found.")
    if not resp.ok:
        raise JiraError(f"Jira error {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    fields = data.get("fields", {})

    summary = fields.get("summary", "")
    description_raw = fields.get("description", {})

    if isinstance(description_raw, dict):
        description = _extract_text_from_adf(description_raw)
    else:
        description = str(description_raw) if description_raw else ""

    acceptance_criteria = _extract_acceptance_criteria(description, fields)

    return {
        "key": data.get("key", ticket_key),
        "summary": summary,
        "description": description,
        "acceptance_criteria": acceptance_criteria,
    }


def _extract_text_from_adf(doc: dict) -> str:
    """Extract plain text from Atlassian Document Format (ADF)."""
    texts = []

    def walk(node):
        if node.get("type") == "text":
            texts.append(node.get("text", ""))
        for child in node.get("content", []):
            walk(child)

    walk(doc)
    return "\n".join(texts)


def _extract_acceptance_criteria(description: str, fields: dict) -> str:
    """Try to pull acceptance criteria from description headers or custom fields."""
    patterns = [
        r"(?i)acceptance\s*criteria\s*:?\s*\n(.*?)(?=\n\s*\n\w|\Z)",
        r"(?i)##\s*acceptance\s*criteria\s*\n(.*?)(?=\n#|\Z)",
        r"(?i)ac\s*:?\s*\n(.*?)(?=\n\s*\n\w|\Z)",
    ]
    for pat in patterns:
        match = re.search(pat, description, re.DOTALL)
        if match:
            return match.group(1).strip()

    for key, value in fields.items():
        if "acceptance" in key.lower() and value:
            return str(value)

    return ""


def test_connection() -> str:
    """Verify Jira credentials. Returns username on success, raises on failure."""
    url = _build_url("/rest/api/2/myself")
    email = get_setting("jira_email")
    token = get_setting("jira_api_token")

    resp = requests.get(
        url,
        auth=HTTPBasicAuth(email, token),
        headers={"Accept": "application/json"},
        timeout=10,
    )
    if resp.ok:
        return resp.json().get("displayName", "Connected")
    if resp.status_code == 401:
        raise AuthenticationError("Invalid credentials")
    raise JiraError(f"Error {resp.status_code}: {resp.text[:200]}")
