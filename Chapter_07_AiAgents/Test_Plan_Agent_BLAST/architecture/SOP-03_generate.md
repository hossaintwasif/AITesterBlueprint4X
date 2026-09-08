# SOP-03 — Generate (LLM interpretation)

## Goal
Turn `NormalizedIssue` JSON into a `TestPlan` JSON (`llm.md` §1.3) via Groq, then validate it with deterministic code (R11).

## Inputs
- `.tmp/normalized_{key}.json`
- `GROQ_API_KEY`, `GROQ_MODEL` (default `openai/gpt-oss-120b`)

## Tool logic
1. **Prompt contract.** System message = role + behavioral rules (R1 no fabrication, R2 missing data, R9 tone, R10 priority derivation) + compact `TestPlan` schema. User message = the normalized JSON, verbatim. The LLM never receives credentials.
2. **Groq call.** `POST https://api.groq.com/openai/v1/chat/completions`:
   - `temperature: 0.2`, `response_format: {"type": "json_object"}`, generous `max_tokens`.
   - 429 → exponential backoff, max 3 retries. If the API rejects `response_format`, retry once without it.
3. **Parse.** Strip markdown fences → `json.loads`. Parse failure = SCHEMA_INVALID.
4. **Validate + backfill.** Code checks the schema: non-empty `scenarios`, every case with non-empty `steps`, `expected_result`, and `traceability` (R1). Missing IDs are backfilled deterministically (`SC-01`, `TC-01.01`, …); defaults filled for metadata fields.
5. **One retry.** On SCHEMA_INVALID, re-call Groq once with the validation errors appended; if it fails again, stop and report instead of shipping malformed JSON.

## Output
`.tmp/testplan_{key}.json` — validated `TestPlan`.

## Test connection
Tiny completion ("Reply with exactly: pong") → 200 = valid key.
