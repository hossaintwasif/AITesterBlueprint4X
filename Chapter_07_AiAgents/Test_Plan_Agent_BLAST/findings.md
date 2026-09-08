# 🔍 Findings — Jira Test Plan Creator

> **Purpose:** Research, discoveries, constraints, and the exact mechanics of fetching data from Jira.
> **Status:** 🟡 Living document (WIP) — updated as new discoveries land
> **Last updated:** 2026-09-04

---

## 🆕 Session 3 update — Live handshakes + reasoning-model discovery

On 2026-09-04 the whole pipeline was built and executed live. New discoveries:

| Finding | Detail | Consequence |
|---------|--------|-------------|
| **Jira handshake passes** | `GET /rest/api/3/myself` → 200, displayName `Twasif Hossain` | Basic Auth (`email:token`) works with the `.env` token; `read:jira-work` scope confirmed sufficient |
| **Groq handshake passes** | `chat/completions` with `openai/gpt-oss-120b` → 200 | API key valid; model available on the account |
| **`gpt-oss-120b` is a reasoning model** | The response has a hidden `reasoning` field; `content` stays empty until reasoning finishes. With small `max_tokens` (10) the whole budget was consumed by `reasoning_tokens` (48) and content came back `""` with `finish_reason: length` | All Groq calls must use generous `max_tokens` (test connection = 256, generation = 8192). Client now raises a clear error when the model emits no content |
| **LLM ID drift** | The model wrote `SC-1.TC-1` in the traceability matrix while deterministic IDs are `SC-01` / `TC-01.01` | `_backfill_ids()` normalizes matrix references against real case IDs |
| **Sparse ticket behavior** | KAN-1 has summary "Task 1", no description content, no AC, no priority | R2 path confirmed: medium/low confidence, smoke test from summary, missing data listed in `low_confidence_notes` — zero fabrication |

**Handshake commands that now work (Phase 2 complete):**

```bash
# Jira — who am I
curl -s -X GET "https://hossaintwasif98-jira.atlassian.net/rest/api/3/myself" \
  --user "$JIRA_Email:$JIRA_API_TOKEN" -H "Accept: application/json"

# Groq — reasoning model, so give it a real token budget
curl -s -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer $GROQ_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": "Reply with exactly: pong"}], "temperature": 0, "max_tokens": 256}'
```

---



## 🧠 Thinking / What I Investigated

To build "Jira ID → Test Plan," I needed to answer three research questions before writing any code:

1. **How do we authenticate against Jira reliably?** (API token vs PAT vs OAuth)
2. **Which endpoints return everything a test plan needs?** (issue fields, comments, attachments, links, changelog)
3. **What has been built before?** (reference implementations to learn from, not copy blindly)

---

## 🆕 Session 2 update — Environment now inspected, Discovery Questions partially answered

On 2026-09-03 I re-read the whole folder including `.env`. This changed the plan materially:

| Question | Answer from `.env` / project | Effect |
|----------|------------------------------|--------|
| Jira flavor | **Cloud** (`hossaintwasif98-jira.atlassian.net`) | REST **v3** is the API; ADF parsing is mandatory, not optional |
| Which project? | **KAN** (`/jira/software/projects/KAN/...`) | Discovery scope = the KAN project/board |
| LLM for reasoning | **Groq**, model `openai/gpt-oss-120b`, key present | Layer 2/3 generation via Groq OpenAI-compatible API |
| Where data lives | Jira issues (source of truth) | `fetch_issue.py` is the spine of the pipeline |

**Unresolved still (needs user):** scope of the plan (single ticket vs KAN board backlog), attachments in the truth set, delivery target (local Markdown? Confluence?), tone/ID conventions, and the LLM's allowed tasks (interpretation only vs full generation).

**New risk found:** the repo is a git repository but has **no `.gitignore`** and `.env` holds live secrets. Fixed immediately — `.gitignore` created (`*.env`, `.tmp/`, Python artifacts).

---

## ✅ Finding 1 — Jira flavors decide the API version

| Flavor | Base URL pattern | REST version | Notes |
|--------|------------------|--------------|-------|
| **Jira Cloud** | `https://YOUR-SITE.atlassian.net` | `/rest/api/3/...` (also `/rest/api/2` works) | v3 = latest, ADF support in descriptions/comments |
| **Jira Data Center / Server** | `https://jira.company.com` | `/rest/api/2/...` | Self-hosted; v3 not available |

**Decision point (Discovery Q2):** If the user's Jira is Cloud → use v3. If self-hosted → v2. The fetch tool should accept the base URL from `.env`, so both work with the same code.

---

## ✅ Finding 2 — Authentication: email + API token (Basic Auth)

Official Atlassian docs confirm: scripts authenticate with **HTTP Basic Auth** where username = account email, password = API token.

Key facts:
- API tokens are created at `https://id.atlassian.com/manage-profile/security/api-tokens`
- Tokens created after 15 Dec 2024 **expire after 1 year by default** (configurable 1–365 days)
- Scoped tokens exist; for read-only fetching the scope needed is `read:jira-work`
- Tokens are **variable length** — code must not assume fixed length
- Alternative: **Personal Access Tokens (PATs)** on Jira Data Center, and OAuth 2.0 (3LO) for apps — overkill for this tool

**→ Resolved for this project (2026-09-03):** the target is **Jira Cloud** (from `.env`), so Basic Auth (`JIRA_Email` + `JIRA_API_TOKEN`) against REST v3. Token creation date and expiry are **not recorded** in the `.env` — the progress log now tracks this as an open risk.

**Constraint:** credentials go in `.env` only. Never in code, never committed.

---

## ✅ Finding 3 — The exact requests we will use

### 3.1 Core: Get one issue by key

```bash
# LIVE request for this project — Jira Cloud REST v3, KAN project
# Replace KAN-1 with the real issue key.
curl -s -X GET \
  "https://hossaintwasif98-jira.atlassian.net/rest/api/3/issue/KAN-1?fields=summary,description,issuetype,status,priority,components,labels,assignee,reporter,created,updated,comment,attachment,subtasks,issuelinks&expand=renderedFields,names" \
  --user "$JIRA_Email:$JIRA_API_TOKEN" \
  -H "Accept: application/json"
```

```bash
# Live connectivity check (handshake for Phase 2): "who am I" + JQL for the KAN board
curl -s -X GET \
  "https://hossaintwasif98-jira.atlassian.net/rest/api/3/myself" \
  --user "$JIRA_Email:$JIRA_API_TOKEN" \
  -H "Accept: application/json"

curl -s -X POST \
  "https://hossaintwasif98-jira.atlassian.net/rest/api/3/search" \
  --user "$JIRA_Email:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jql": "project = KAN ORDER BY updated DESC", "fields": ["key", "summary"], "maxResults": 10}'
```

> Note: variables are sourced from the local `.env` (`JIRA_Email`, `JIRA_API_TOKEN`). The literal values are never pasted into scripts or logs.

```bash
# Jira Data Center / Server (REST v2) — same shape, v2 path
curl -s -X GET \
  "https://jira.company.com/rest/api/2/issue/PROJ-123?fields=summary,description,issuetype,status,priority,comment,attachment,subtasks&expand=renderedFields,names" \
  --user "your-email@example.com:your-api-token" \
  -H "Accept: application/json"
```

What comes back (fields relevant to a test plan):

| Field | Why a test plan needs it |
|-------|--------------------------|
| `fields.summary` | Scope definition |
| `fields.description` | **ADF document** (Cloud v3) or wiki text (v2) — core source for scenarios |
| `fields.comment.comments[]` | Clarifications, edge cases, AC discussions |
| `fields.attachment[]` | Mockups, AC docs, requirement specs |
| `fields.subtasks[]` / `parent` | Decompose scope into testable units |
| `fields.issuelink` (needs `issuelinks` field) | Related requirements / blocked-by |
| `fields.customfield_*` | Acceptance criteria often live in custom fields (e.g., story points, AC field) |
| `fields.labels`, `components` | Test-suite grouping |

### 3.2 JQL search — linked issues, epics, subtasks in one call

```bash
curl -s -X POST \
  "https://YOUR-SITE.atlassian.net/rest/api/3/search" \
  --user "your-email@example.com:your-api-token" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "jql": "issue = PROJ-123 OR parent = PROJ-123 OR issueLinkType in (\"is blocked by\") AND issue = PROJ-123",
    "fields": ["summary", "description", "issuetype", "status", "priority"],
    "maxResults": 50
  }'
```

### 3.3 Changelog — status history for regression hints

```bash
curl -s -X GET \
  "https://YOUR-SITE.atlassian.net/rest/api/3/issue/PROJ-123/changelog?maxResults=100" \
  --user "your-email@example.com:your-api-token"
```

### 3.4 Attachment download (to `.tmp/`)

```bash
curl -s -X GET \
  "https://YOUR-SITE.atlassian.net/rest/api/3/attachment/content/ATTACHMENT_ID" \
  --user "your-email@example.com:your-api-token" \
  -o .tmp/attachment_ATTACHMENT_ID
```

### 3.5 Python equivalent (Layer 3 tools will use this)

```python
import os, requests
from requests.auth import HTTPBasicAuth

BASE = os.environ["JIRA_BASE_URL"]       # https://hossaintwasif98-jira.atlassian.net
EMAIL = os.environ["JIRA_Email"]
TOKEN = os.environ["JIRA_API_TOKEN"]

def fetch_issue(key: str) -> dict:
    url = f"{BASE}/rest/api/3/issue/{key}"
    params = {
        "fields": "summary,description,issuetype,status,priority,components,labels,comment,attachment,subtasks,issuelinks",
        "expand": "renderedFields,names",
    }
    resp = requests.get(url, params=params,
                        auth=HTTPBasicAuth(EMAIL, TOKEN),
                        headers={"Accept": "application/json"},
                        timeout=30)
    resp.raise_for_status()   # 401 -> bad token, 404 -> bad key
    return resp.json()
```

---

## ✅ Finding 5 — The Groq LLM contract (OpenAI-compatible)

From `.env`: `GROQ_API_KEY` + `GROQ_MODEL=openai/gpt-oss-120b`. Groq exposes an OpenAI-compatible chat-completions endpoint, so `generate_testplan.py` needs no Groq-specific SDK — plain `requests` is enough.

```bash
# Groq LLM connectivity check (handshake for Phase 2)
curl -s -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": "Reply with exactly: pong"}], "temperature": 0}'
```

```python
import os, requests

def generate(prompt: str) -> str:
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={
            "model": os.environ["GROQ_MODEL"],   # openai/gpt-oss-120b
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,                   # low => reproducible-ish plans
            "response_format": {"type": "json_object"},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

**Design consequences for the generator:**
1. Use `response_format: json_object` + `temperature <= 0.2` — the model emits the `TestPlan` JSON from the schema in `llm.md`, and the tool validates it with jsonschema before writing anything.
2. `gpt-oss-120b` is a strong open-weight model, but it is still probabilistic: the schema + traceability rules (R1–R3) are enforced by **code validation after generation**, not by prompt promises.
3. The prompt contract for generation is the "Delivery Payload" for the LLM — it is designed in Phase 3 (SOP-03) once the remaining Discovery Questions are answered.

---

## ✅ Finding 6 — Descriptions are ADF on Cloud; must be normalized

On Jira Cloud v3, `fields.description` is an **Atlassian Document Format** (ADF) JSON tree, not plain text. The normalize tool must walk ADF nodes (`doc → content[] → paragraph/heading/list/codeBlock`) and emit Markdown. On v2/Data Center it's wiki markup (also needs conversion, or fetch `renderedFields.description` which returns ready HTML in the `expand` result).

**Design consequence:** `normalize_issue.py` needs an `adf_to_markdown()` deterministic converter. This is the highest-risk tool — it gets the most unit tests.

---

## ✅ Finding 7 — Reference implementations (GitHub)

| Repo | Stack | What to borrow | What to avoid |
|------|-------|----------------|---------------|
| [sachinpratap001/intelligent-test-plan-agent](https://github.com/sachinpratap001/intelligent-test-plan-agent) | React+Express+SQLite, Groq/Ollama, Jira v3 | Settings→test-connection flow, `findings/progress/task_plan` discipline, PDF template idea, SSE streaming | Full web app = overkill for our single-command objective; we keep a CLI-first pipeline |
| [bhaumikgohel/Intelligent-Test-Plan-Generator-Using-JIRA](https://github.com/bhaumikgohel/Intelligent-Test-Plan-Generator-Using-JIRA) | Similar full-stack | Template-driven plan structure | Same — heavy frontend |
| [nagarjunabhr8/Test-Plan-Generator-from-JIRA-board](https://github.com/nagarjunabhr8/Test-Plan-Generator-from-JIRA-board) | Similar | Confirms the market pattern: fetch → parse → LLM → template | — |

**My architecture decision:** stay true to BLAST's 3-layer model instead of a web app. `tools/` as atomic Python scripts, `architecture/` as SOPs, navigation layer = LLM. Deliverable = files in `.tmp/` + final Markdown. Simpler, deterministic, testable — exactly what BLAST prioritizes.

---

## ⚠️ Known constraints / risks

1. **Token expiry:** tokens die yearly (or sooner). Progress log must note token creation date; `.env` doc must say where to rotate it. **Open item:** we do not know when this project's token was created.
2. **No published hard rate limit** on Jira Cloud REST, but bulk calls (JQL search) should still be polite and cached in `.tmp/` to avoid refetching.
3. **Custom fields:** "Acceptance Criteria" may live in `customfield_XXXXX`. Fetch tool must pull `names` expand so we can map field IDs → human names dynamically instead of hardcoding.
4. **Empty descriptions:** many tickets have everything in comments/attachments. Generator must handle "description empty" gracefully — fall back to comments + title-derived smoke tests, and flag low-confidence output.
5. ~~**Data Center vs Cloud** unknown~~ → **Resolved:** Jira Cloud confirmed from `.env` (2026-09-03). REST v3 + ADF parsing are now hard requirements.
6. **New (2026-09-03): no `.gitignore` existed** while `.env` holds live credentials → created `.gitignore` (`.env`, `.tmp/`, Python artifacts). If this repo was ever pushed, the token is exposed and must be rotated.

---

## 📚 Sources

- [The Jira Cloud platform REST API (Atlassian)](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Jira Cloud REST API — Issues group (Atlassian)](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/)
- [Manage API tokens for your Atlassian account](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- [Jira API Get Issue — A Complete Guide (Airbyte)](https://airbyte.com/data-engineering-resources/jira-api-get-issue)
- [Groq Cloud docs — OpenAI-compatible chat completions](https://console.groq.com/docs/openai)
- [sachinpratap001/intelligent-test-plan-agent (GitHub)](https://github.com/sachinpratap001/intelligent-test-plan-agent)
- [bhaumikgohel/Intelligent-Test-Plan-Generator-Using-JIRA (GitHub)](https://github.com/bhaumikgohel/Intelligent-Test-Plan-Generator-Using-JIRA)
- [nagarjunabhr8/Test-Plan-Generator-from-JIRA-board (GitHub)](https://github.com/nagarjunabhr8/Test-Plan-Generator-from-JIRA-board)
