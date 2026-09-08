# SOP-01 — Jira Fetch

## Goal
Retrieve the complete context for one Jira Cloud issue (REST v3) and cache the raw payload in `.tmp/`.

## Inputs
- `jira_id` (e.g. `KAN-1`) — validated at the boundary against `^[A-Z][A-Z0-9]*-[0-9]+$`
- `jira_base_url` (`https://<site>.atlassian.net`), `email`, `api_token` — from `.env` or `config.json` (UI)

## Tool logic
1. `GET {base}/rest/api/3/issue/{key}?expand=names,renderedFields` with HTTP Basic Auth (`email:api_token`).
   - No `fields` filter → full payload, so custom fields (e.g. Acceptance Criteria) are always available.
2. Best-effort `GET {base}/rest/api/3/issue/{key}/changelog?maxResults=100` → attached as `changelog`; a failure here is logged, never fatal.
3. Cache raw payload → `.tmp/raw_{key}.json`. Idempotent re-runs read the cache first.

## Edge cases
| Code | Meaning | Behavior |
|------|---------|----------|
| 401 | Bad/expired token | Stop; raise `AuthenticationError` — rotate token (link in `findings.md`) |
| 404 | Bad issue key | Stop; raise `NotFoundError` — suggest key format `[A-Z]+-\d+` |
| 429 | Rate limited | Exponential backoff (1s, 2s, 4s), max 3 retries, then stop |
| EMPTY_DESC | No description/ADF | Continue; normalize sets `description_empty` → generator applies low-confidence rules (R2) |
| ADF_PARSE | Malformed ADF | Fall back to `renderedFields.description` (HTML → text); log warning |
| Network/timeout | Unreachable | Raise `ConnectionError` with an actionable message |

## Test connection
`GET {base}/rest/api/3/myself` → returns `displayName` on 200; 401 → `AuthenticationError`.
