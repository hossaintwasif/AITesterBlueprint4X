import re

from adf import adf_to_markdown, html_to_text


def normalize_issue(raw: dict) -> dict:
    """Convert a raw Jira v3 issue payload into the NormalizedIssue schema (llm.md §1.2)."""
    key = raw.get("key", "")
    fields = raw.get("fields", {})
    names = raw.get("names", {})

    summary = fields.get("summary") or ""
    description_md, description_empty = _extract_description(raw, fields)

    acceptance = _extract_acceptance_criteria(fields, names, description_md)
    comments = _extract_comments(fields)

    requirements = []
    if summary:
        requirements.append({"text": summary, "source": "summary"})
    for line in _lines_from(description_md):
        requirements.append({"text": line, "source": "description"})
    for ac in acceptance:
        requirements.append({"text": ac, "source": "acceptance criteria"})
    for comment in comments:
        for line in _lines_from(comment["body_markdown"]):
            requirements.append({"text": line, "source": f"comment by {comment['author']}"})

    confidence, reasons = _confidence(description_empty, acceptance, comments)

    return {
        "source_jira_id": key,
        "summary": summary,
        "feature_scope": _feature_scope(summary, description_md),
        "requirements": requirements,
        "acceptance_criteria": acceptance,
        "constraints": _explicit_lines(description_md, ("constraint", "dependency")),
        "risks": _explicit_lines(description_md, ("risk",)),
        "stakeholders": _stakeholders(fields, comments),
        "related_items": _related_items(raw, fields),
        "confidence": confidence,
        "confidence_reasons": reasons,
        "description_empty": description_empty,
        "issue_type": (fields.get("issuetype") or {}).get("name", ""),
        "status": (fields.get("status") or {}).get("name", ""),
        "priority": (fields.get("priority") or {}).get("name", ""),
        "components": [c.get("name", "") for c in fields.get("components", [])],
        "labels": list(fields.get("labels") or []),
        "attachments": [
            {
                "id": a.get("id", ""),
                "filename": a.get("filename", ""),
                "mime_type": a.get("mimeType", ""),
            }
            for a in fields.get("attachment", [])
        ],
        "changelog": [
            {
                "created": entry.get("created", ""),
                "items": [
                    {
                        "field": item.get("field", ""),
                        "from": item.get("fromString", ""),
                        "to": item.get("toString", ""),
                    }
                    for item in entry.get("items", [])
                ],
            }
            for entry in raw.get("changelog", {}).get("values", [])
        ],
    }


def _extract_description(raw: dict, fields: dict) -> tuple[str, bool]:
    description = fields.get("description")
    if not description:
        return "", True

    if isinstance(description, dict):
        try:
            return adf_to_markdown(description), False
        except Exception:
            rendered = (
                (raw.get("renderedFields") or {}).get("description")
                if isinstance(raw.get("renderedFields"), dict)
                else ""
            )
            if rendered:
                return html_to_text(rendered), False
            return "", True

    text = str(description)
    return text, not bool(text.strip())


def _extract_acceptance_criteria(fields: dict, names: dict, description_md: str) -> list[str]:
    criteria = []
    for field_id, field_name in names.items():
        if "acceptance" in field_name.lower():
            value = fields.get(field_id)
            if isinstance(value, dict):
                text = adf_to_markdown(value)
            elif value:
                text = str(value)
            else:
                continue
            criteria.extend(_lines_from(text))

    if not criteria:
        match = re.search(
            r"(?i)#{0,3}\s*acceptance\s*criteria\s*:?\s*\n(.*?)(?=\n#{1,3}\s|\Z)",
            description_md,
            re.DOTALL,
        )
        if match:
            criteria.extend(_lines_from(match.group(1)))

    return criteria


def _extract_comments(fields: dict) -> list[dict]:
    comments = []
    comment_field = fields.get("comment") or {}
    for c in comment_field.get("comments", []):
        body = c.get("body", "")
        if isinstance(body, dict):
            body_md = adf_to_markdown(body)
        else:
            body_md = str(body)
        if body_md.strip():
            comments.append(
                {
                    "author": (c.get("author") or {}).get("displayName", "unknown"),
                    "created": c.get("created", ""),
                    "body_markdown": body_md.strip(),
                }
            )
    return comments


def _lines_from(text: str) -> list[str]:
    lines = []
    for line in text.splitlines():
        line = line.strip().lstrip("-*#").strip()
        if len(line) >= 3:
            lines.append(line)
    return lines


def _explicit_lines(description_md: str, keywords: tuple[str, ...]) -> list[str]:
    found = []
    lines = description_md.splitlines()
    for i, line in enumerate(lines):
        if any(k in line.lower() for k in keywords):
            candidate = re.sub(r"^#{1,6}\s*", "", line).strip()
            if candidate and not candidate.lower().startswith(("##",)):
                found.append(candidate)
            elif i + 1 < len(lines):
                found.append(lines[i + 1].strip())
    return found


def _confidence(description_empty: bool, acceptance: list, comments: list) -> tuple[str, list[str]]:
    if description_empty and not acceptance and not comments:
        return "low", [
            "No description, acceptance criteria, or comments found in Jira.",
            "Plan built from the issue summary only (R2).",
        ]
    if not description_empty and acceptance:
        return "high", ["Description and acceptance criteria present."]
    if not description_empty:
        return "medium", ["Description present, but no acceptance criteria found."]
    return "medium", [
        "Description empty, but comments or acceptance criteria exist.",
    ]


def _feature_scope(summary: str, description_md: str) -> str:
    lines = [summary, "", description_md.strip()]
    return "\n".join(lines).strip() or summary


def _stakeholders(fields: dict, comments: list) -> list[str]:
    people = set()
    for key in ("assignee", "reporter", "creator"):
        person = fields.get(key) or {}
        name = person.get("displayName")
        if name:
            people.add(name)
    for comment in comments:
        people.add(comment["author"])
    return sorted(people)


def _related_items(raw: dict, fields: dict) -> list[str]:
    items = []
    for sub in fields.get("subtasks", []):
        items.append(f"Subtask {sub.get('key', '')}: {sub.get('fields', {}).get('summary', '')}")
    parent = fields.get("parent")
    if parent:
        items.append(f"Parent {parent.get('key', '')}: {parent.get('fields', {}).get('summary', '')}")
    for link in fields.get("issuelinks", []):
        link_type = (link.get("type") or {}).get("name", "linked")
        for side in ("outwardIssue", "inwardIssue"):
            issue = link.get(side) or {}
            if issue:
                items.append(
                    f"{link_type} {issue.get('key', '')}: {issue.get('fields', {}).get('summary', '')}"
                )
    return items
