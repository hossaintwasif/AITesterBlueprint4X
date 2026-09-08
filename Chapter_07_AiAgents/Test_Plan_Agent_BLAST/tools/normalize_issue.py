import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from normalize_issue import normalize_issue  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python normalize_issue.py <JIRA-KEY>")
        sys.exit(2)
    key = sys.argv[1].strip().upper()
    root = Path(__file__).resolve().parent.parent
    raw_path = root / ".tmp" / f"raw_{key}.json"
    if not raw_path.exists():
        print(f"Missing {raw_path}. Run fetch_issue.py first.")
        sys.exit(1)
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    normalized = normalize_issue(raw)
    (root / ".tmp" / f"normalized_{key}.json").write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Normalized {key} → .tmp/normalized_{key}.json (confidence: {normalized['confidence']})")


if __name__ == "__main__":
    main()
