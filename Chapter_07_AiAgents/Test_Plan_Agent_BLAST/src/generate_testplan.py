import json
import re

from llm_client import generate, SchemaValidationError

SYSTEM_PROMPT = """You are a senior QA engineer and AI Test Plan Agent.

Generate a test plan STRICTLY from the normalized Jira issue JSON provided by the user. Output ONLY a JSON object matching this schema:

{
  "title": "string",
  "scope": {"in_scope": ["..."], "out_of_scope": ["..."], "assumptions": ["..."]},
  "test_strategy": "string describing levels: smoke, functional, regression, exploratory",
  "test_data": ["..."],
  "environment": ["..."],
  "scenarios": [
    {
      "title": "string",
      "description": "string",
      "traceability": ["source string from the issue"],
      "test_cases": [
        {
          "preconditions": ["..."],
          "steps": ["..."],
          "expected_result": "string",
          "test_data": "string or null",
          "priority": "high | medium | low",
          "automation_candidate": true,
          "traceability": ["source string from the issue"]
        }
      ]
    }
  ],
  "traceability_matrix": [{"requirement": "string", "case_ids": ["SC-XX.TC-XX"]}],
  "low_confidence_notes": ["..."]
}

HARD RULES:
1. NO FABRICATION. Every scenario, test case, and expected result must trace to a field, comment, or acceptance criterion in the provided JSON. Each test case MUST have a non-empty "traceability" list quoting the source text.
2. MISSING DATA: if description/acceptance criteria are empty, generate smoke tests from the summary, mark priority conservatively, and list exactly what was missing in "low_confidence_notes".
3. Use professional imperative tone for steps ("Click Save", not "The user should click Save").
4. Derive priority from the issue type and priority field; bugs get regression-heavy plans.
5. Keep IDs deterministic: scenarios named by topic. Do NOT invent feature requirements or credentials.
6. Respond with ONLY the JSON object — no markdown fences, no preamble.
"""


def _clean_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise SchemaValidationError("Groq output contains no JSON object.")
    return text[start : end + 1]


def _backfill_ids(plan: dict) -> None:
    known_case_ids = set()
    for s_idx, scenario in enumerate(plan.get("scenarios", []), start=1):
        scenario.setdefault("scenario_id", f"SC-{s_idx:02d}")
        scenario.setdefault("traceability", [])
        for c_idx, case in enumerate(scenario.get("test_cases", []), start=1):
            case.setdefault(
                "case_id", f"TC-{s_idx:02d}.{c_idx:02d}"
            )
            case.setdefault("priority", "medium")
            case.setdefault("automation_candidate", False)
            case.setdefault("test_data", None)
            case.setdefault("preconditions", [])
            case.setdefault("traceability", [])
            known_case_ids.add(case["case_id"])

    for row in plan.get("traceability_matrix", []):
        normalized_ids = []
        for ref in row.get("case_ids", []):
            match = re.match(r"^SC-(\d+)\.?TC-(\d+)(?:\.(\d+))?$", str(ref))
            if match:
                s_idx = int(match.group(1))
                if match.group(3):
                    c_idx = int(match.group(3))
                    candidate = f"TC-{s_idx:02d}.{c_idx:02d}"
                else:
                    candidate = f"TC-{s_idx:02d}.{int(match.group(2)):02d}"
                if candidate in known_case_ids:
                    normalized_ids.append(candidate)
                    continue
            normalized_ids.append(str(ref))
        row["case_ids"] = normalized_ids


def _validate(plan: dict) -> list[str]:
    errors = []
    if not isinstance(plan, dict):
        return ["Output is not a JSON object."]

    scenarios = plan.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("'scenarios' must be a non-empty list.")
        return errors

    for i, scenario in enumerate(scenarios):
        cases = scenario.get("test_cases")
        if not isinstance(cases, list) or not cases:
            errors.append(f"scenarios[{i}].test_cases must be a non-empty list.")
            continue
        for j, case in enumerate(cases):
            label = f"scenarios[{i}].test_cases[{j}]"
            if not case.get("steps"):
                errors.append(f"{label}.steps must be a non-empty list.")
            if not case.get("expected_result"):
                errors.append(f"{label}.expected_result must be a non-empty string.")
            if not case.get("traceability"):
                errors.append(f"{label}.traceability must be non-empty (R1).")
    return errors


def generate_testplan(normalized: dict, model_label: str) -> dict:
    """Call Groq, parse, validate, and backfill the TestPlan JSON (llm.md §1.3)."""
    user_prompt = json.dumps(normalized, indent=2, ensure_ascii=False)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Normalized Jira issue:\n{user_prompt}"},
    ]

    raw = generate(messages, temperature=0.2, max_tokens=8192, json_mode=True)

    try:
        plan = json.loads(_clean_json(raw))
    except (json.JSONDecodeError, SchemaValidationError) as e:
        plan = None
        first_error = str(e)

    errors = _validate(plan) if plan is not None else [first_error]

    if errors:
        retry_prompt = (
            "Your previous output failed validation with these errors:\n"
            + "\n".join(f"- {e}" for e in errors)
            + "\n\nReturn a corrected JSON object ONLY, satisfying every HARD RULE."
        )
        raw2 = generate(
            messages + [{"role": "assistant", "content": raw}, {"role": "user", "content": retry_prompt}],
            temperature=0.2,
            max_tokens=8192,
            json_mode=True,
        )
        try:
            plan = json.loads(_clean_json(raw2))
        except (json.JSONDecodeError, SchemaValidationError) as e:
            raise SchemaValidationError(
                "Groq output failed schema validation twice. Last error: "
                + "; ".join(errors + [str(e)])
            )
        errors = _validate(plan)
        if errors:
            raise SchemaValidationError(
                "Groq output still invalid after retry: " + "; ".join(errors)
            )

    _backfill_ids(plan)
    plan["source_jira_id"] = normalized.get("source_jira_id", "")
    plan["plan_id"] = f"TP-{normalized.get('source_jira_id', 'UNKNOWN')}"
    plan["generated_at"] = __import__("datetime").datetime.now().isoformat(timespec="seconds")
    plan["author"] = "AI Test Plan Agent"
    plan["version"] = "1.0"
    plan["model"] = model_label
    plan["constitution_version"] = "0.3"
    return plan
