import re
import time

import requests
from requests.auth import HTTPBasicAuth

from config_store import get_setting

KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")


class JiraError(Exception):
    pass


class ConnectionError(JiraError):
    pass


class AuthenticationError(JiraError):
    pass


class NotFoundError(JiraError):
    pass


class RateLimitError(JiraError):
    pass


def normalize_key(key: str) -> str:
    return key.strip().upper()


def validate_key(key: str) -> None:
    if not KEY_PATTERN.match(key):
        raise JiraError(
            f"Invalid issue key **{key}**. Expected format: `PROJ-123` (letters/digits, dash, number)."
        )


def _base_url() -> str:
    base = get_setting("jira_base_url").strip().rstrip("/")
    if not base:
        raise AuthenticationError(
            "Jira URL not configured. Set it in the Settings page."
        )
    return base


def _auth() -> HTTPBasicAuth:
    email = get_setting("jira_email").strip()
    token = get_setting("jira_api_token").strip()
    if not email or not token:
        raise AuthenticationError(
            "Jira credentials not configured. Add your email and API token in Settings."
        )
    return HTTPBasicAuth(email, token)


def _request(method: str, url: str, **kwargs) -> requests.Response:
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            resp = requests.request(method, url, timeout=30, **kwargs)
        except requests.exceptions.Timeout:
            raise ConnectionError("Jira request timed out. Check your network.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot reach Jira at {_base_url()}. Check the URL in Settings."
            )

        if resp.status_code == 429:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise RateLimitError("Jira rate limit hit. Try again shortly.")
        return resp
    raise JiraError("Unreachable state in retry loop.")


def fetch_issue(key: str) -> dict:
    """Fetch a full Jira Cloud v3 issue payload (all fields, names, rendered)."""
    key = normalize_key(key)
    validate_key(key)
    url = f"{_base_url()}/rest/api/3/issue/{key}"
    resp = _request(
        "GET",
        url,
        auth=_auth(),
        headers={"Accept": "application/json"},
        params={"expand": "names,renderedFields"},
    )

    if resp.status_code == 401:
        raise AuthenticationError(
            "Jira authentication failed (401). Check email and API token in Settings."
        )
    if resp.status_code == 404:
        raise NotFoundError(f"Issue **{key}** not found.")
    if not resp.ok:
        raise JiraError(f"Jira error {resp.status_code}: {resp.text[:300]}")

    issue = resp.json()

    try:
        changelog_resp = _request(
            "GET",
            f"{_base_url()}/rest/api/3/issue/{key}/changelog",
            auth=_auth(),
            headers={"Accept": "application/json"},
            params={"maxResults": 100},
        )
        if changelog_resp.ok:
            issue["changelog"] = changelog_resp.json()
    except JiraError:
        pass

    return issue


def test_connection() -> str:
    url = f"{_base_url()}/rest/api/3/myself"
    resp = _request(
        "GET", url, auth=_auth(), headers={"Accept": "application/json"}
    )
    if resp.ok:
        return resp.json().get("displayName", "Connected")
    if resp.status_code == 401:
        raise AuthenticationError("Invalid Jira credentials (401).")
    raise JiraError(f"Jira error {resp.status_code}: {resp.text[:200]}")
