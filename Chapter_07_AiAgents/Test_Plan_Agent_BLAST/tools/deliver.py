import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from deliver import render_markdown  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python deliver.py <JIRA-KEY>")
        sys.exit(2)
    key = sys.argv[1].strip().upper()
    root = Path(__file__).resolve().parent.parent
    plan_path = root / ".tmp" / f"testplan_{key}.json"
    if not plan_path.exists():
        print(f"Missing {plan_path}. Run generate_testplan.py first.")
        sys.exit(1)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    output_dir = root / "output"
    output_dir.mkdir(exist_ok=True)
    md_path = output_dir / f"test_plan_{key}.md"
    json_path = output_dir / f"test_plan_{key}.json"
    md_path.write_text(render_markdown(plan), encoding="utf-8")
    json_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Delivered → {md_path}")
    print(f"Delivered → {json_path}")


if __name__ == "__main__":
    main()
