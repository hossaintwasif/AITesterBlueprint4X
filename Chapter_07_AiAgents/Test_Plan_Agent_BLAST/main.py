import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from pipeline import run_pipeline  # noqa: E402
from jira_client import JiraError  # noqa: E402
from llm_client import LLMError  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <JIRA-KEY>")
        sys.exit(2)
    try:
        result = run_pipeline(sys.argv[1])
        print(f"Test plan ready: {result['md_path']}")
        print(f"Confidence: {result['confidence']}")
    except (JiraError, LLMError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
