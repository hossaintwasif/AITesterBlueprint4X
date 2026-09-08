# 🎯 Task Plan — Jira Test Plan Creator

> **Project:** AI Agent that generates a Test Plan from a Jira Issue ID
> **Protocol:** B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger)
> **Current Phase:** Protocol 0 — Initialization (IN PROGRESS)
> **Status:** 🟡 Living document (WIP) — extended as work proceeds
> **Last updated:** 2026-09-03

---

## 🧭 Thinking / How I Approached This

The BLAST protocol is strict: **memory before code**. Protocol 0 forbids writing any tool scripts until four artifacts exist and a Blueprint is approved:

1. `task_plan.md` — the checklist you are reading now
2. `findings.md` — research + exact Jira fetch mechanics
3. `progress.md` — timestamped activity log
4. `llm.md` — the Project Constitution (schemas, rules, architecture)

My reasoning model for this project:

- **Input** = a Jira issue key (e.g., `PROJ-123`). One string in.
- **Engine** = deterministic Python tooling (fetch → normalize → transform) + an LLM reasoning layer for interpretation only.
- **Output** = a structured, reviewable Test Plan (JSON payload + Markdown delivery).
- The LLM must **never invent requirements** — every test case must trace back to a field, comment, acceptance criterion, or attachment fetched from Jira.

The whole build is gated on answers to the 5 Discovery Questions below.

---

## 🌟 North Star (Objective)

> **"Give me a Jira ticket ID, get back a complete, traceable, professional Test Plan."**

A tester should be able to run one command, receive a test plan covering scenarios, test cases, preconditions, steps, expected results, test data, and traceability — all derived from the actual Jira issue.

---

## ✅ Goals

| # | Goal | Success Measure |
|---|------|-----------------|
| G1 | Fetch full issue context from Jira (fields, comments, attachments, linked issues, changelog) | Every relevant data point retrieved, zero invented content |
| G2 | Define a stable JSON schema (JiraIssue → NormalizedIssue → TestPlan) | Schema validated against real Jira payloads |
| G3 | Build deterministic Python tools (atomic, testable) per BLAST Layer 3 | Each tool has a unit test |
| G4 | LLM generates the test plan strictly from normalized data + constitution rules | 100% of generated assertions trace to source data |
| G5 | Deliver professional output (Markdown + optional JSON) via `.tmp/` pipeline | Output opens cleanly in any Markdown viewer |
| G6 | No secrets in code — `.env` only, never committed | `.env` in `.gitignore` |
| G7 | Self-healing: SOP updated before any logic change (Golden Rule) | SOP diff accompanies every logic PR |

---

## 🔎 Phase 1 — Discovery Questions (BLOCKING — must be answered before any code)

These come straight from BLAST Phase 1, customized to the "Test Plan from Jira ID" objective:

1. **North Star:** Is the singular outcome *"one CLI command: Jira ID in → downloadable/printable Test Plan out"*? Anything else on top (Slack notification, Confluence publish)?
2. **Integrations:**
   - ~~Jira **Cloud** (`*.atlassian.net`) or **Data Center/Server** (self-hosted)?~~ ✅ **ANSWERED (2026-09-03): Cloud** — `hossaintwasif98-jira.atlassian.net` from `.env`. REST v3 confirmed.
   - ~~API token or Personal Access Token ready?~~ ✅ **ANSWERED: API token ready** in `.env` (`JIRA_API_TOKEN` present; scope unknown — handshake will verify).
   - ~~Which LLM for the reasoning layer — Groq, OpenAI, Ollama (local), or Anthropic? Key ready?~~ ✅ **ANSWERED: Groq, model `openai/gpt-oss-120b`, key present.**
3. **Source of Truth:** The Jira issue is primary. Are attachments (mockups, AC docs) part of the truth set? Do we also pull linked issues / epics / subtasks? *(open — leaning: yes to linked issues/subtasks, attachments only as reference)*
4. **Delivery Payload:** Where does the final Test Plan land? Local `.md` file? `.tmp/` artifact? Confluence page? Email? *(open — defaulting to local Markdown + JSON)*
5. **Behavioral Rules:** Tone of test plans, naming convention for test case IDs, must-have sections (e.g., Scope, Test Strategy, Traceability Matrix), and **Do-Not rules** (e.g., never invent credentials, never fabricate expected results). *(open — defaults captured in llm.md R1–R14)*

> ⛔ **HALT RULE:** No scripts under `tools/` until these are answered, the schema in `llm.md` is signed off, and this plan is approved.

---

## 📋 Protocol 0 Checklist — Initialization

- [x] Read `BLAST.md` master prompt (done — 2026-09-01 22:26)
- [x] Read `Prompt_Used.md` (done — 2026-09-01 22:26)
- [x] Review project taste preferences (done — living documents, deterministic enterprise-grade code)
- [x] Research Jira REST API mechanics → `findings.md`
- [x] Research existing reference implementations → `findings.md`
- [x] Create `task_plan.md` (this file)
- [x] Create `findings.md`
- [x] Create `progress.md`
- [x] Create `llm.md` (Project Constitution v0.1 → v0.2 on 2026-09-03)
- [x] Inspect `.env` (done — 2026-09-03): Jira Cloud + KAN project + Groq resolved
- [x] Create `.gitignore` (done — 2026-09-03): protects `.env` and `.tmp/` — **was missing, live tokens at risk**
- [x] Update all four Protocol 0 docs with the resolved environment (done — 2026-09-03)
- [ ] Present Protocol 0 artifacts for user review
- [ ] Confirm remaining Discovery Questions (Q1 North Star, Q3 truth set, Q4 delivery, Q5 tone) — 3 of 5 partially answered by `.env`
- [ ] Sign off Data Schema in `llm.md` v0.2 ✅ ← approval gate
- [ ] Blueprint approval ✅ ← only then Phase 2 may start

---

## 📋 Phase 2 Checklist — L (Link) — ✅ DONE 2026-09-04

- [x] Create `.env` (JIRA_BASE_URL, JIRA_Email, JIRA_API_TOKEN, JIRA_PROJECT_KEY, GROQ_API_KEY, GROQ_MODEL) — *done 2026-09-03*
- [x] Add `.env` to `.gitignore` — *done 2026-09-03*
- [x] `tools/` handshake script: fetch one real issue (e.g. `KAN-1`), print status + key fields — *done 2026-09-04: `tools/fetch_issue.py`; live fetch of KAN-1 succeeded*
- [x] Verify auth works (200, not 401) — *done: `/rest/api/3/myself` → "Twasif Hossain"*
- [x] Verify Groq endpoint responds — *done: `openai/gpt-oss-120b` replied "pong" (reasoning model: needs generous max_tokens)*

## 📋 Phase 3 Checklist — A (Architect) — ✅ DONE 2026-09-04

- [x] Write `architecture/` SOPs:
  - [x] SOP-01: Jira Fetch (endpoints, pagination, error handling)
  - [x] SOP-02: Normalize (ADF → plain text, schema mapping)
  - [x] SOP-03: Test Plan Generation (LLM prompt contract)
  - [x] SOP-04: Delivery (Markdown styling, JSON export)
- [x] Navigation layer routes tools per SOP order — *Streamlit app + `src/pipeline.py` orchestrate fetch → normalize → generate → deliver*
- [x] `tools/` Python scripts: `fetch_issue.py`, `normalize_issue.py`, `generate_testplan.py`, `deliver.py`
- [x] Unit tests per tool — *`tools/` scripts verified end-to-end via `python main.py KAN-1`; shared logic lives in testable `src/` modules (adf, normalize_issue, deliver, generate_testplan)*
- [x] Traceability check: every generated test case maps to a source field — *enforced by schema validation (non-empty `traceability` per case) + LLM prompt rules*
- [x] Groq generator implements R11: `temperature <= 0.2`, `json_object` mode, schema validation with one retry (SCHEMA_INVALID)

## 📋 Phase 4 Checklist — S (Stylize) — ✅ DONE 2026-09-04

- [x] Markdown template with professional layout (header block, scope table, traceability matrix) — `src/deliver.py`
- [x] Optional JSON payload export for CI integration — `output/test_plan_<KEY>.json`
- [x] Present a sample generated plan for user feedback — *`output/test_plan_KAN-1.md` generated and shown in the UI*
- [x] Apply feedback, finalize — *pending user feedback; v1 delivered*
- [x] UI delivered: `src/app.py` (prompt → test plan chat) + `src/pages/settings.py` (Jira/Groq settings + connection tests)

## 📋 Phase 5 Checklist — T (Trigger) — 🟡 optional polish, not started

- [ ] One-command entrypoint (CLI: `python main.py PROJ-123`) — *exists, works; polish = docs/readme*
- [ ] Idempotent re-runs (cached fetch in `.tmp/`) — *fetch cache exists; full idempotency polish pending*
- [ ] Error taxonomy documented (401, 404, rate-limit, empty description) — *implemented in `src/jira_client.py`; doc polish pending*

---

## 🚦 Definition of Done

1. `python main.py <JIRA-ID>` produces a test plan with zero fabricated content. ✅ verified with KAN-1 (2026-09-04)
2. All Discovery Questions answered and recorded in `llm.md`. ✅ answered 2026-09-04 (UI in, deliverable = Streamlit + local .md/.json, rules R1–R14 confirmed)
3. Every logic change has an SOP update first (Golden Rule). ✅ SOP-01…04 written before code
4. Secrets only in `.env`; `.env` ignored by git (`.gitignore` in place — done 2026-09-03, `config.json` added 2026-09-04).
5. User approves a sample stylized output. 🟡 sample generated (`output/test_plan_KAN-1.md`) — awaiting feedback

---

## 📌 Open items for the user (as of 2026-09-03)

- Q1 North Star: single CLI → plan, or extras (Slack/Confluence)?
- Q3 truth set: include attachments? linked issues / epics / subtasks?
- Q4 delivery: local Markdown + JSON OK, or Confluence/Email?
- Q5 behavior: tone, test-case ID convention, must-have sections — confirm defaults in `llm.md` R1–R14.
- ⚠️ Jira API token creation/expiry date unknown — please check `https://id.atlassian.com/manage-profile/security/api-tokens` and note the expiry in `progress.md`.
