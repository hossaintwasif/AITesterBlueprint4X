# SOP-02 — Normalize

## Goal
Transform a raw Jira v3 payload into the `NormalizedIssue` schema (`llm.md` §1.2). Deterministic, no LLM.

## Inputs
- Raw issue JSON from SOP-01 (`.tmp/raw_{key}.json`)

## Tool logic
1. **ADF → Markdown.** Walk the ADF tree (`doc → content[]`):
   - `paragraph` → text + blank line; `heading` → `#` * level; `bulletList`/`orderedList` → list items; `codeBlock` → fenced block; `blockquote`, `panel`, `rule` → markdown equivalents.
   - Inline marks: `strong` → `**…**`, `em` → `*…*`, `code` → `` `…` ``, `link` → `[text](href)`, `hardBreak` → newline.
   - `text` nodes append their text; unknown node types recurse into `content`.
2. **Acceptance criteria.** From `names` expand, find custom fields whose name contains `acceptance` (case-insensitive); parse ADF or plain text values. If none, scan the description for `Acceptance Criteria` / `AC:` sections.
3. **Comments** (`fields.comment.comments[]`) → `author`, `created`, `body_markdown` (ADF-converted).
4. **Structure.** Attachments (id/filename/mime), subtasks, parent, linked issues, changelog → simplified records.
5. **Requirements.** Distilled, traceable lines: summary + description lines + AC + non-empty comments. Every item records its source (`summary` | `description` | `acceptance criteria` | `comment by X`).
6. **Confidence.** `high` if AC present; `medium` if description present but no AC; `low` if description empty (R2). Reasons are always recorded.

## Edge cases
- Empty description → fall back to comments + summary (R2 path).
- ADF parse failure → `renderedFields` HTML → strip tags → plain text, log warning (ADF_PARSE).

## Output
`.tmp/normalized_{key}.json` matching `NormalizedIssue` in `llm.md`.
