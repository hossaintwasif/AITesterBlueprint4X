def adf_to_markdown(doc) -> str:
    """Convert an Atlassian Document Format (ADF) tree to Markdown."""
    if not isinstance(doc, dict):
        return str(doc) if doc else ""
    return _render_node(doc).strip()


def _render_node(node: dict) -> str:
    node_type = node.get("type", "")

    if node_type == "text":
        text = node.get("text", "")
        for mark in node.get("marks", []):
            text = _apply_mark(text, mark)
        return text

    if node_type == "hardBreak":
        return "\n"

    content = node.get("content", [])
    inner = _render_children(content)

    renderers = {
        "doc": lambda: inner,
        "paragraph": lambda: inner + "\n\n",
        "heading": lambda: f"{'#' * min(node.get('attrs', {}).get('level', 1), 6)} {inner}\n\n",
        "bulletList": lambda: inner + "\n",
        "orderedList": lambda: inner + "\n",
        "listItem": lambda: f"- {inner}\n",
        "codeBlock": lambda: f"```\n{inner}\n```\n\n",
        "blockquote": lambda: "\n".join(f"> {line}" for line in inner.splitlines()) + "\n\n",
        "panel": lambda: f"> **Note:** {inner}\n\n",
        "rule": lambda: "---\n\n",
        "table": lambda: inner + "\n",
        "tableRow": lambda: "| " + inner.replace("\n", " | ") + " |\n",
        "tableHeader": lambda: _table_cell(inner),
        "tableCell": lambda: _table_cell(inner),
        "mention": lambda: f"@{node.get('attrs', {}).get('text', 'user')}",
        "emoji": lambda: node.get("attrs", {}).get("shortName", ""),
        "inlineCard": lambda: node.get("attrs", {}).get("url", ""),
    }

    renderer = renderers.get(node_type)
    if renderer:
        return renderer()
    return inner


def _table_cell(inner: str) -> str:
    return inner.replace("\n", " ") + " | "


def _render_children(content: list) -> str:
    return "".join(_render_node(child) for child in content)


def _apply_mark(text: str, mark: dict) -> str:
    mark_type = mark.get("type", "")
    if mark_type == "strong":
        return f"**{text}**"
    if mark_type == "em":
        return f"*{text}*"
    if mark_type == "code":
        return f"`{text}`"
    if mark_type == "link":
        href = mark.get("attrs", {}).get("href", "")
        return f"[{text}]({href})" if href else text
    return text


def html_to_text(html: str) -> str:
    """Fallback for malformed ADF: strip tags from renderedFields HTML."""
    import re

    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</(p|div|li|h[1-6]|tr)>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "- ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return text
