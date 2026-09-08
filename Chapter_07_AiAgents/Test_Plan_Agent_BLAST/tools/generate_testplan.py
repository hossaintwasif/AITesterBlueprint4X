import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from generate_testplan import generate_testplan  # noqa: E402
from llm_client import _model  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python generate_testplan.py <JIRA-KEY>")
        sys.exit(2)
    key = sys.argv[1].strip().upper()
    root = Path(__file__).resolve().parent.parent
    normalized_path = root / ".tmp" / f"normalized_{key}.json"
    if not normalized_path.exists():
        print(f"Missing {normalized_path}. Run normalize_issue.py first.")
        sys.exit(1)
    normalized = json.loads(normalized_path.read_text(encoding="utf-8"))
    plan = generate_testplan(normalized, _model())
    (root / ".tmp" / f"testplan_{key}.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    scenarios = len(plan.get("scenarios", []))
    cases = sum(len(s.get("test_cases", [])) for s in plan.get("scenarios", []))
    print(f"Generated plan for {key}: {scenarios} scenarios, {cases} test cases → .tmp/testplan_{key}.json")


if __name__ == "__main__":
    main()
