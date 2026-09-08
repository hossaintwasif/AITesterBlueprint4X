# 📜 LLM.md — Project Constitution (v0.3)

> **Purpose:** The single source of truth for how this project is built. Schemas, behavioral rules, architectural invariants.
> **Status:** 🟡 Living document — amended only with explicit approval of a change record
> **Last updated:** 2026-09-04

---

## 🧠 Thinking / Design Philosophy

BLAST's core doctrine: **LLMs are probabilistic; business logic must be deterministic.** Therefore:

- The LLM in this project has exactly **two jobs**: (1) the navigation layer that routes data between SOPs and tools in the correct order, and (2) the *interpretation* of normalized Jira content into human-readable test scenarios.
- Everything else — fetching, parsing, schema validation, traceability checks, delivery — is **deterministic Python** with unit tests.
- The LLM **never sees raw credentials**, never decides endpoint URLs, and never fabricates requirements. If source data is missing, it must say so explicitly (low-confidence markers), not invent plausible content.

### 🔒 Resolved configuration (from `.env`, 2026-09-03)

| Item | Value | Consequence |
|------|-------|-------------|
| Jira flavor | **Cloud** (`hossaintwasif98-jira.atlassian.net`) | REST v3 only; ADF parsing is a hard requirement |
| Jira project | **KAN** | Discovery scope = KAN project/board |
| Auth | `JIRA_Email` + `JIRA_API_TOKEN` (Basic Auth) | Read-only scope `read:jira-work` is sufficient |
| LLM provider | **Groq**, model `openai/gpt-oss-120b` | OpenAI-compatible `chat/completions`; no SDK needed |
| Generation knobs | `temperature <= 0.2`, `response_format: json_object` | Low variance, schema-validatable output |

These were assumptions in v0.1; they are now facts. The remaining unknowns (plan scope, delivery target, tone/ID conventions) were answered by the user on 2026-09-04:

| Discovery Question | Answer (2026-09-04) |
|--------------------|---------------------|
| Q1 North Star | A simple UI: user types a natural-language prompt ("fetch this Jira and create a test plan") → app fetches the Jira issue and generates the test plan automatically |
| Q3 Source of truth | The single Jira issue (fields, ADF description, comments, attachments metadata, subtasks, links, changelog); attachments are metadata-only in v1 |
| Q4 Delivery payload | Streamlit chat UI with inline Markdown + download button; artifacts in `output/test_plan_<KEY>.md` and `.json` |
| Q5 Behavioral rules | R1–R14 defaults confirmed: no fabrication, mandatory traceability, professional imperative tone, deterministic IDs, priority from issue type + Jira priority |

---

## 📦 1. Data Schemas (Data-First Rule)

Schema is defined **before any code**. All shapes are JSON.

### 1.1 `JiraIssue` — INPUT (what the fetch tool returns, normalized from Jira REST v3)

```json
{
  "jira_id": "KAN-1",
  "flavor": "cloud",
  "summary": "string (required)",
  "issue_type": "Story | Bug | Task | Epic | ...",
  "status": "To Do | In Progress | Done | ...",
  "priority": "Highest | High | Medium | Low | Lowest",
  "components": ["string"],
  "labels": ["string"],
  "assignee": "string | null",
  "reporter": "string | null",
  "created": "ISO-8601",
  "updated": "ISO-8601",
  "description_markdown": "string (ADF already converted)",
  "description_empty": "boolean",
  "acceptance_criteria": ["string"],
  "comments": [
    { "author": "string", "created": "ISO-8601", "body_markdown": "string" }
  ],
  "attachments": [
    { "id": "string", "filename": "string", "mime_type": "string", "local_path": "string|null" }
  ],
  "subtasks": ["{ jira_id, summary, issue_type, status }"],
  "parent": "{ jira_id, summary } | null",
  "linked_issues": ["{ jira_id, summary, link_type }"],
  "changelog": ["{ created, field, from, to }"]
}
```

> v0.2 note: `flavor` is no longer a runtime unknown — it is `"cloud"`. The field is kept for logging only.

### 1.2 `NormalizedIssue` — INTERMEDIATE (parse output, generator input)

```json
{
  "source_jira_id": "KAN-1",
  "summary": "string",
  "feature_scope": "string (summary + description distilled)",
  "requirements": ["string (each traceable: field | comment | attachment | AC)"],
  "acceptance_criteria": ["string"],
  "constraints": ["string (explicit only)"],
  "risks": ["string (explicit only)"],
  "stakeholders": ["string (assignee, reporter, commenters)"],
  "related_items": ["string (subtasks + links)"],
  "confidence": "high | medium | low",
  "confidence_reasons": ["string"]
}
```

### 1.3 `TestPlan` — OUTPUT (what the generator produces)

```json
{
  "plan_id": "TP-KAN-1-20260903",
  "title": "string",
  "source_jira_id": "KAN-1",
  "generated_at": "ISO-8601",
  "author": "AI Test Plan Agent",
  "version": "1.0",
  "scope": {
    "in_scope": ["string"],
    "out_of_scope": ["string"],
    "assumptions": ["string"]
  },
  "test_strategy": "string (levels: smoke, functional, regression, exploratory)",
  "test_data": ["string (explicitly requested or derived from requirements)"],
  "environment": ["string (from components/labels or flagged as REQUIRED INPUT)"],
  "scenarios": [
    {
      "scenario_id": "SC-01",
      "title": "string",
      "description": "string",
      "traceability": ["Jira field: description", "Jira comment: id"],
      "test_cases": [
        {
          "case_id": "TC-01.01",
          "preconditions": ["string"],
          "steps": ["string"],
          "expected_result": "string",
          "test_data": "string | null",
          "priority": "high | medium | low",
          "automation_candidate": "boolean",
          "traceability": ["string (must be non-empty)"]
        }
      ]
    }
  ],
  "traceability_matrix": [
    { "requirement": "string", "case_ids": ["TC-01.01"] }
  ],
  "low_confidence_notes": ["string (where data was missing or ambiguous)"],
  "constitution_version": "0.2"
}
```

---

## 📏 2. Behavioral Rules (inviolable)

| # | Rule |
|---|------|
| R1 | **No fabrication.** Every scenario and expected result must trace to a `JiraIssue` field, comment, attachment, or AC. `traceability` is mandatory on every test case. |
| R2 | **Missing data ≠ guessing.** If description/AC is empty, generate title-derived smoke tests, mark `confidence: low`, and list exactly what was missing in `low_confidence_notes`. |
| R3 | **Determinism over cleverness.** Tools are pure functions of their inputs. Same Jira ID + same data ⇒ same plan (stable IDs like `TC-01.01`). |
| R4 | **Golden Rule.** If logic changes, the SOP in `architecture/` is updated BEFORE the code. No exception. |
| R5 | **Secrets.** Credentials live only in `.env` (git-ignored). Tools read `os.environ`. The LLM never receives tokens. |
| R6 | **All intermediates in `.tmp/`.** Fetch cache, normalized JSON, ADF dumps. `.tmp/` is disposable and git-ignored. |
| R7 | **Schema-first.** A new field in the plan must first be added to section 1 of this constitution and validated; then code follows. |
| R8 | **HALT rule (Protocol 0).** No `tools/` scripts until Discovery Questions are answered and the schema + Blueprint are approved. |
| R9 | **Language.** Test plans delivered in English unless the user states otherwise; tone = professional, imperative steps ("Click Save", not "The user should click Save"). |
| R10 | **Priority derivation.** Bug → regression-heavy plan, high priority. Story → functional + AC-driven. Epic → decomposed by subtasks. Priority is derived from issue type + Jira priority field, never assumed. |
| R11 | **LLM contract (Groq).** Generation goes through `https://api.groq.com/openai/v1/chat/completions` with `temperature <= 0.2` and `response_format: json_object`. The raw LLM output is parsed and **validated against the TestPlan schema by code**; invalid output triggers one retry, then the tool stops and reports rather than shipping malformed JSON. |
| R12 | **Environment contract.** `.env` holds `JIRA_BASE_URL`, `JIRA_Email`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`, `GROQ_API_KEY`, `GROQ_MODEL`. `JIRA_URL` is the human board URL and is never used as an API base. `.env` and `.tmp/` are git-ignored. |
| R13 | **Validation at boundaries only.** Tools trust their own internal contracts; they validate (a) user input (Jira key format), (b) external responses (Jira REST, Groq), and nothing else. |
| R14 | **Scope of the v1 plan.** The pipeline targets a single Jira ID. Board-wide ("whole KAN backlog") generation is a separate later feature unless the user explicitly asks for it now. |
| R15 | **Reasoning-model budget.** `openai/gpt-oss-120b` emits a hidden `reasoning` field before `content`; small `max_tokens` values yield empty content. Every Groq call must use generous budgets (test connection ≥ 256, generation 8192). If content is empty and reasoning exists, the client raises a clear error instead of shipping empty output. |
| R16 | **ID determinism.** Scenario/case IDs are `SC-XX` / `TC-XX.YY`, assigned by code (`_backfill_ids`). LLM-written matrix references (e.g. `SC-1.TC-1`) are normalized to real case IDs by code — the LLM's IDs never leak into the deliverable. |

---

## 🏛️ 3. Architectural Invariants

### 3.1 The 3-Layer A.N.T. model (fixed, never flattened)

```
Layer 1: architecture/   → SOPs in Markdown (goals, inputs, tool logic, edge cases)
Layer 2: Navigation      → LLM reasoning layer: routes data SOP-to-SOP, calls tools in order
Layer 3: tools/          → deterministic Python scripts (atomic, testable, env-driven)
```

- Layer 2 **never reimplements** what a tool does. It orchestrates only.
- Each tool does **one thing** (fetch / normalize / generate / deliver).

### 3.2 Directory contract

```
Test_Plan_Agent_BLAST/
├── BLAST.md                  # master protocol (given)
├── Prompt_Used.md            # original prompt (given)
├── task_plan.md              # protocol 0 ✓
├── findings.md               # protocol 0 ✓ (v3: live handshakes, reasoning-model discovery)
├── progress.md               # protocol 0 ✓
├── llm.md                    # this constitution ✓ (v0.3)
├── .env                      # secrets — git-ignored ✓
├── config.json               # UI-persisted settings (Jira/Groq) — git-ignored ✓
├── .gitignore                # protects .env, config.json, .tmp/ ✓
├── architecture/             # SOPs (Layer 1) ✓
│   ├── SOP-01_jira_fetch.md
│   ├── SOP-02_normalize.md
│   ├── SOP-03_generate.md
│   └── SOP-04_deliver.md
├── src/                      # shared, testable modules + Streamlit UI (Layer 2 navigation + UI)
│   ├── config_store.py       # .env + config.json loader
│   ├── jira_client.py        # REST v3 fetch + handshake
│   ├── adf.py                # ADF → Markdown deterministic converter
│   ├── normalize_issue.py    # raw → NormalizedIssue
│   ├── generate_testplan.py  # Groq call + schema validation + ID backfill
│   ├── deliver.py            # TestPlan → Markdown renderer
│   ├── pipeline.py           # fetch → normalize → generate → deliver orchestrator
│   ├── app.py                # Streamlit chat UI
│   ├── pages/settings.py     # Jira/Groq settings + connection tests
│   └── requirements.txt
├── tools/                    # atomic CLI scripts (Layer 3) ✓
│   ├── fetch_issue.py
│   ├── normalize_issue.py
│   ├── generate_testplan.py
│   └── deliver.py
├── main.py                   # one-command entrypoint ✓
├── output/                   # final deliverables: test_plan_<KEY>.md + .json ✓
└── .tmp/                     # all intermediate artifacts (disposable, git-ignored)
```

### 3.3 Execution pipeline (target)

```
Jira ID (input, e.g. KAN-1)
  → tools/fetch_issue.py        [SOP-01] → .tmp/raw_KAN-1.json
  → tools/normalize_issue.py    [SOP-02] → .tmp/normalized_KAN-1.json
  → tools/generate_testplan.py  [SOP-03] → .tmp/testplan_KAN-1.json   (Groq interpretation here)
  → tools/deliver.py            [SOP-04] → test_plan_KAN-1.md  (+ optional .json)
```

> v0.2: the LLM hop is pinned to Groq `openai/gpt-oss-120b` (OpenAI-compatible endpoint), `temperature <= 0.2`, `json_object` mode — see Finding 5 in `findings.md`.

### 3.4 Error taxonomy (tools must implement, not just document)

| Code | Meaning | Tool behavior |
|------|---------|---------------|
| 401 | Bad/expired token | Stop; instruct user to rotate token (findings.md has the link) |
| 404 | Bad issue key | Stop; suggest key format `[A-Z]+-\d+` |
| 429 | Rate limited | Exponential backoff, max 3 retries, then stop |
| EMPTY_DESC | No description | Continue with R2 rules, mark low confidence |
| ADF_PARSE | Malformed ADF | Fall back to renderedFields HTML; log warning |
| SCHEMA_INVALID | Groq output fails TestPlan schema validation | One retry with the validation errors appended to the prompt; then stop and report |

---

## 📝 4. Change Record

| Version | Date | Change | Approved by |
|---------|------|--------|-------------|
| 0.1 | 2026-09-01 | Initial constitution: schemas, rules, architecture | Pending user review |
| 0.2 | 2026-09-03 | `.env` inspected → Cloud/KAN/Groq locked in; R11–R14 added; `.gitignore` added; error taxonomy + SCHEMA_INVALID; schema examples moved to KAN; Finding 5 (Groq contract) referenced | Pending user review |
| 0.3 | 2026-09-04 | Phases 1–4 delivered: Discovery Q1/Q3/Q4/Q5 answered (UI, delivery, rules); R15 (reasoning-model token budget) + R16 (ID determinism) added; directory contract updated (src/, tools/, main.py, output/, config.json git-ignored); SOP-01…04 written; pipeline verified live with KAN-1 | User go-ahead 2026-09-04 |
