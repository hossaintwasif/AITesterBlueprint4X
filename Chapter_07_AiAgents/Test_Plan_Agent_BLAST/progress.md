# 📊 Progress Log — Jira Test Plan Creator

> **Purpose:** Chronological activity log. Every session, every step, every error, every result.
> **Status:** 🟡 Living document — updated continuously while working
> **Convention:** Entries use local time `YYYY-MM-DD HH:MM` (IST). Each entry: ✅ done / ⚠️ error / 🔬 result / 📝 note. Newest entries appended at the bottom.
> **Cadence rule:** Log at natural checkpoints (roughly every 10–30 min of work, or immediately after any error/decision).

---

## 2026-09-01 — Session 1: Protocol 0 Initialization

### 22:26 — Session started
- ✅ Read `BLAST.md` — understood the 5 phases and the Protocol 0 mandate.
- ✅ Read `Prompt_Used.md` — confirmed objective: **Test Plan Creator from a Jira ID**, Protocol 0 first.
- ✅ Reviewed project taste preferences (`.commandcode/taste/`).
  - Key preferences adopted: living/WIP documents, structured thinking, enterprise-grade deterministic code, review-before-write.
- 📝 Thinking: Protocol 0 is a documentation phase — the four memory files ARE the deliverable today. No `tools/` code until Discovery Questions are answered and schema is approved (HALT rule).

### 22:29 — Research: Jira authentication
- ✅ Verified official Atlassian API-token docs.
- 🔬 Result: Scripts authenticate via **HTTP Basic Auth** (`email:api-token`). Tokens expire yearly (post-15-Dec-2024 policy). Scoped tokens exist; `read:jira-work` is enough for fetching.
- ✅ Verified Jira Cloud REST v3 is the current API (`/rest/api/3/issue/{key}`); Data Center uses v2.

### 22:33 — Research: reference implementations
- ✅ Searched GitHub for prior art.
- 🔬 Result: 3 similar full-stack projects found (React+Express+Groq/Ollama). All follow: fetch Jira → parse → LLM → template.
- 📝 Decision: We stay CLI-first with BLAST's 3-layer architecture (SOPs / navigation / atomic Python tools) instead of a web app. Simpler and deterministic.
- ✅ Inspected `sachinpratap001/intelligent-test-plan-agent` README — captured its endpoint list and env-var patterns as reference (not copied).

### 22:38 — Drafting findings
- ✅ Compiled findings: API version matrix, auth mechanics, 5 curl requests (issue fetch, JQL search, changelog, attachment download) + Python `requests` equivalent.
- ✅ Identified top risk: **ADF description parsing** on Cloud v3 → dedicated `adf_to_markdown()` converter with its own test suite.
- ⚠️ Known gap: "Acceptance Criteria" may live in custom fields — solved dynamically via `expand=names` (no hardcoded field IDs).

### 22:42 — Drafting schema & constitution
- ✅ Designed JSON schemas in `llm.md`: `JiraIssue` (input) → `NormalizedIssue` (intermediate) → `TestPlan` (output).
- ✅ Defined behavioral rules (no fabrication, traceability, deterministic tools) and architectural invariants (`.env` secrets, `.tmp/` intermediates, Golden Rule: SOP before code).

### 22:45 — Files written
- ✅ Created `task_plan.md` — phases, goals, checklists, Discovery Questions, Definition of Done.
- ✅ Created `findings.md` — research + exact curl/requests for Jira.
- ✅ Created `progress.md` — this log.
- ✅ Created `llm.md` — Project Constitution v0.1.
- 🔬 Result: Protocol 0 artifacts complete. **HALT state maintained** — zero scripts written, as required.
- 📝 Next: present artifacts to user; collect answers to the 5 Discovery Questions; get schema + Blueprint sign-off. Only then Phase 2 (Link) begins.

---

## 2026-09-03 — Session 2: Full review + environment resolution

### Start — Re-read every file in the folder
- ✅ Read `BLAST.md`, `Prompt_Used.md`, `task_plan.md`, `findings.md`, `progress.md`, `llm.md`, and `.env` (all 7 files).
- 🔬 Result: all four Protocol 0 artifacts already exist and are in good shape from Session 1. This session's job: review them against the actual `.env` and update everything that was only assumed.
- ⚠️ Error/risk found: `.env` holds live Jira + Groq credentials but **no `.gitignore` existed**. The repo is git-tracked — the tokens are exposed if the folder was ever committed.
- 📝 Thinking: Protocol 0 is still in force. No `tools/` code until Discovery Questions are answered and the schema is signed off.

### Step 1 — `.env` review
- ✅ Inspected `.env`: Jira URL is a **board URL** (`.../jira/software/projects/KAN/boards/2`), not an API base. Derived and added `JIRA_BASE_URL=https://hossaintwasif98-jira.atlassian.net` and `JIRA_PROJECT_KEY=KAN`.
- 🔬 Result: Discovery Q2 answered by evidence — Jira **Cloud**, project **KAN**, Groq model `openai/gpt-oss-120b` with key present.
- ⚠️ Open risk: token creation/expiry date unknown — added to open items.

### Step 2 — Security fix
- ✅ Created `.gitignore`: `.env`, `.tmp/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`.
- 🔬 Result: secrets and intermediates now excluded from git. Logged as risk #6 in findings.md.

### Step 3 — findings.md update
- ✅ Added "Session 2 update" section: env questions resolved (Cloud / KAN / Groq), unresolved items listed.
- ✅ Replaced the placeholder `YOUR-SITE` curls with **live** requests against `hossaintwasif98-jira.atlassian.net` (issue fetch for `KAN-1`, `myself` + JQL search handshakes).
- ✅ Added new **Finding 5: Groq LLM contract** — OpenAI-compatible endpoint, `json_object` mode, `temperature <= 0.2`, curl + Python equivalents.
- ✅ Renumbered old findings (ADF → 6, references → 7); resolved the old "Data Center vs Cloud unknown" risk; added the `.gitignore` gap as risk #6; added Groq docs source.

### Step 4 — llm.md constitution v0.1 → v0.2
- ✅ Added "Resolved configuration" table (Cloud/KAN/Groq facts from `.env`).
- ✅ `JiraIssue.flavor` pinned to `"cloud"` (kept for logging); schema examples moved to `KAN-1`; constitution_version → 0.2.
- ✅ New rules R11–R14: Groq contract + schema validation with one retry; environment contract; boundary-only validation; single-Jira-ID scope for v1.
- ✅ Pipeline annotated with Groq hop; directory contract updated (`.gitignore` now present); error taxonomy + `SCHEMA_INVALID`; change record + v0.2 row.

### Step 5 — task_plan.md update
- ✅ Discovery Q2 sub-items marked ANSWERED (Cloud, API token, Groq) with dates; Q1/Q3/Q4/Q5 kept open with current defaults.
- ✅ Protocol 0 checklist: `.env` inspection, `.gitignore` creation, doc updates marked done.
- ✅ Phase 2: `.env` creation and `.gitignore` marked done (they existed/are done now); handshake steps still pending with pointer to the curl templates.
- ✅ Phase 3: added R11 checklist item for the Groq generator.
- ✅ Added "Open items for the user" section at the bottom (4 discovery confirmations + token expiry warning).

### End of session — results
- 🔬 Result: Protocol 0 documentation is now consistent with the real environment. All four memory files updated; `.gitignore` created; `.env` extended.
- ⚠️ Errors fixed this session: missing `.gitignore` (live secret exposure), stale assumptions (Data Center vs Cloud), numbering collision in findings.md.
- 📝 Next (blocked on user): confirm Q1/Q3/Q4/Q5, sign off `llm.md` v0.2 schema, approve Blueprint → then Phase 2 Link (handshake scripts).

---

## 2026-09-04 — Session 3: Phases 1–4 delivered in one go (UI + full pipeline)

### Start — Discovery answers locked in (from the user)
- ✅ **Q1 North Star:** a simple UI where the user types a natural-language prompt ("fetch this Jira and create a test plan"); the app fetches the Jira issue and generates the test plan automatically.
- ✅ **Q2 Integrations:** Jira Cloud (`hossaintwasif98-jira.atlassian.net`) + Groq `openai/gpt-oss-120b` — both from `.env` (already answered).
- ✅ **Q3 Source of truth:** the single Jira issue (fields, ADF description, comments, attachments metadata, subtasks, links, changelog). Attachments stay metadata-only in v1.
- ✅ **Q4 Delivery:** Streamlit UI (chat + settings) with local `output/test_plan_<KEY>.md` + `.json` artifacts and a download button.
- ✅ **Q5 Behavioral rules:** defaults from `llm.md` R1–R14 confirmed (no fabrication, traceability mandatory, professional tone, deterministic IDs).
- 📝 Blueprint approved by the user's go-ahead → HALT rule lifted. Phase 2 (Link) may start.

### Step 1 — Phase 1/2: Golden Rule — SOPs before code
- ✅ Created `architecture/` Layer 1: `SOP-01_jira_fetch.md`, `SOP-02_normalize.md`, `SOP-03_generate.md`, `SOP-04_deliver.md` (goals, inputs, tool logic, edge cases, error taxonomy).
- ✅ Wrote the `tools/` Layer 3 atomic scripts + `src/` shared clients + `main.py` CLI entrypoint.
- 🔬 Result: BLAST 3-layer architecture in place — SOPs (Layer 1), Streamlit = navigation (Layer 2), deterministic Python (Layer 3).

### Step 2 — Phase 2 (Link): handshakes — both PASS
- ✅ Jira handshake: `GET /rest/api/3/myself` → **200, displayName "Twasif Hossain"**.
- ✅ Groq handshake: `chat/completions` with `openai/gpt-oss-120b` → **200, replied "pong"**.
- ⚠️ Error found & fixed: `openai/gpt-oss-120b` is a **reasoning model** — it spends tokens on hidden `reasoning` before emitting `content`. With a tiny `max_tokens` the content was empty (`finish_reason: length`, `reasoning_tokens` burned the whole budget). Fix: raise the test-connection budget to 256 tokens, and the generator already uses 8192. The client now raises a clear error if the model never emits content.
- ⚠️ Error found & fixed: the LLM wrote `SC-1.TC-1` in the traceability matrix while deterministic IDs are `SC-01`/`TC-01.01`. Fix: `_backfill_ids()` now normalizes matrix references to real case IDs.

### Step 3 — Phase 3 (Architect): pipeline end-to-end
- ✅ `python main.py KAN-1` → fetch → normalize → Groq generate → deliver. Produced `output/test_plan_KAN-1.md` + `.json` with scenarios, test cases, and traceability.
- 🔬 Result: KAN-1 is a thin ticket ("Task 1", no AC). The plan correctly followed R2: low/medium confidence, smoke-style case, and `low_confidence_notes` listing missing data. No fabricated requirements.
- ✅ `.tmp/` intermediates: `raw_KAN-1.json`, `normalized_KAN-1.json`, `testplan_KAN-1.json` — all cached, re-runs deterministic.

### Step 4 — Phase 4 (Stylize): UI
- ✅ `src/app.py` — chat UI: natural-language prompt → Jira key regex → pipeline → markdown test plan inline + download button.
- ✅ `src/pages/settings.py` — Jira URL/email/token + Groq key/model, with **Test Jira Connection** and **Test Groq Connection** buttons, persisted to `config.json` (git-ignored).
- ✅ `config.json` added to `.gitignore` (user-entered credentials must never be committed).
- ✅ `src/requirements.txt` (streamlit, requests, python-dotenv); streamlit installed locally.

### End of session — results
- 🔬 Result: All four phases (Blueprint, Link, Architect, Stylize) delivered: UI + settings + live Jira + live Groq + validated test plan artifacts.
- ✅ Definition of Done v1 satisfied: one prompt → test plan, zero fabrication (R2 honored on sparse ticket), secrets only in `.env`/`config.json`, SOPs updated first.
- 📝 Phase 5 (Trigger) remains as a polish phase: cron/scheduled generation, idempotency polish, deeper attachment handling.
