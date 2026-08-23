# QA Prompt Skill Suite

This directory contains 54 installable QA skills plus the original standalone test-case
prompt. The suite combines the 36-skill STLC and automation collection from
[skillmasterclass](https://github.com/PramodDutta/skillmasterclass/tree/d8c5108d5ae524b10a5a1c695cdee8cfc018be7b/skillmasterclass/skills)
with 18 focused additions for API testing, AI safety and guardrails, and test deliverables.

## Suite inventory

| Area | Count | Skills |
| --- | ---: | --- |
| STLC · Requirement Analysis | 1 | `jira-requirement-analyzer` |
| STLC · Test Planning | 1 | `test-plan-generator` |
| STLC · Test Design | 2 | `test-scenario-designer`, `api-test-designer` |
| STLC · Test Case Development | 2 | `test-case-writer`, `test-data-generator` |
| STLC · Test Execution | 3 | `automation-script-generator`, `test-execution-tracker`, `regression-suite-selector` |
| STLC · Defect Management | 3 | `bug-reporter`, `bug-triage-assistant`, `rca-analyzer` |
| STLC · Test Closure | 2 | `test-coverage-analyzer`, `test-closure-reporter` |
| Playwright | 11 | `pw-accessibility-auditor`, `pw-api-tester`, `pw-ci-configurator`, `pw-fixture-designer`, `pw-flaky-debugger`, `pw-locator-fixer`, `pw-network-mocker`, `pw-page-object-builder`, `pw-test-generator`, `pw-trace-analyzer`, `pw-visual-regression` |
| Selenium | 11 | `se-cross-browser-runner`, `se-data-driven-designer`, `se-driver-manager`, `se-flaky-debugger`, `se-framework-scaffolder`, `se-grid-configurator`, `se-locator-strategist`, `se-page-object-builder`, `se-report-integrator`, `se-test-generator`, `se-wait-fixer` |
| API Testing | 6 | `api-contract-validator`, `api-collection-builder`, `api-workflow-tester`, `api-authorization-boundary-tester`, `api-resilience-tester`, `api-performance-test-planner` |
| AI Safety and Guardrails | 6 | `ai-threat-modeler`, `prompt-injection-resilience-tester`, `sensitive-data-leakage-tester`, `ai-agent-tool-safety-tester`, `content-safety-guardrail-evaluator`, `ai-fairness-bias-evaluator` |
| Test Deliverables | 6 | `review-test-deliverables`, `maintain-test-traceability`, `draft-test-status-brief`, `assemble-release-decision-record`, `curate-test-evidence-bundle`, `prepare-qa-audit-handoff` |
| **Total** | **54** | **36 upstream + 18 extensions** |

The legacy `stlc/testcase_creator.md` remains available as a standalone fill-in prompt and is
not included in the skill count.

## Directory map

```text
prompt_templates/
├── stlc/                 # 14 STLC skills, grouped by seven numbered phases
├── playwright/           # 11 Playwright skills
├── selenium/             # 11 Selenium skills
├── api_testing/          # 6 API testing extensions
├── safety_guardrails/    # 6 AI safety and guardrail extensions
└── test_deliverables/    # 6 evidence and handoff extensions
```

Each skill is a folder containing a required `SKILL.md`. The 18 extensions also include
`agents/openai.yaml` for Codex skill-list metadata.

## Use a skill

Copy the folder for the skill you need only when the destination name is unused. This
example refuses to merge into or overwrite an existing installation:

```bash
skill_source=chapter_02_Prompt_Eng/prompt_templates/api_testing/api-contract-validator
skill_destination="$HOME/.codex/skills/api-contract-validator"

if [ -e "$skill_destination" ]; then
  echo "Skill already exists; compare and back it up before an explicitly approved update."
  exit 1
fi

mkdir -p "$(dirname "$skill_destination")"
cp -R "$skill_source" "$skill_destination"
```

Then invoke it by name, such as `$api-contract-validator`. Review the skill's required inputs
and guardrails before using it. Generated plans, cases, reports, or decisions remain drafts
until the named human reviewer approves them.

## Provenance

The original 36 skills were synchronized from upstream commit
`d8c5108d5ae524b10a5a1c695cdee8cfc018be7b` dated 2026-07-14 and placed under the matching
STLC, Playwright, and Selenium categories. This repository then hardens that baseline for
credential handling, execution authorization, network isolation, evidence redaction, and
semantic correctness. The 18 extensions follow the same evidence-first approach: never
fabricate missing inputs or results, protect sensitive data, and stop at a human-review gate.
