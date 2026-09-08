import json
from pathlib import Path

from deliver import render_markdown
from generate_testplan import generate_testplan
from jira_client import fetch_issue, validate_key, normalize_key
from llm_client import _model
from normalize_issue import normalize_issue

ROOT_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = ROOT_DIR / ".tmp"
OUTPUT_DIR = ROOT_DIR / "output"


def run_pipeline(jira_id: str) -> dict:
    """Full BLAST pipeline: fetch → normalize → generate → deliver."""
    key = normalize_key(jira_id)
    validate_key(key)

    TMP_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw = fetch_issue(key)
    (TMP_DIR / f"raw_{key}.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    normalized = normalize_issue(raw)
    (TMP_DIR / f"normalized_{key}.json").write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    plan = generate_testplan(normalized, _model())
    (TMP_DIR / f"testplan_{key}.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    markdown = render_markdown(plan)
    md_path = OUTPUT_DIR / f"test_plan_{key}.md"
    json_path = OUTPUT_DIR / f"test_plan_{key}.json"
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "key": key,
        "summary": normalized.get("summary", ""),
        "confidence": normalized.get("confidence", "medium"),
        "markdown": markdown,
        "plan": plan,
        "md_path": str(md_path),
        "json_path": str(json_path),
    }
