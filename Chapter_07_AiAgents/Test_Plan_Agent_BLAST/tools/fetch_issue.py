import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jira_client import fetch_issue, validate_key, normalize_key  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python fetch_issue.py <JIRA-KEY>")
        sys.exit(2)
    key = normalize_key(sys.argv[1])
    validate_key(key)
    issue = fetch_issue(key)
    out = Path(__file__).resolve().parent.parent / ".tmp"
    out.mkdir(exist_ok=True)
    (out / f"raw_{key}.json").write_text(
        json.dumps(issue, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Fetched {key} → .tmp/raw_{key}.json")


if __name__ == "__main__":
    main()
