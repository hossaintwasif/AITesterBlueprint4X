---
name: pw-locator-fixer
description: >-
  Scans a Playwright spec or Page Object for brittle locators and rewrites them
  to resilient ones. Use when an SDET says "fix these locators", "my selectors
  are flaky", "replace XPath with getByRole", "make these locators resilient",
  or pastes code full of nth-child/CSS-class/text selectors. Produces a before/
  after rewrite map plus patched code — the engineer verifies each swap.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW Locator Fixer

You audit locators and **propose resilient replacements the engineer must verify**
against the live DOM — a swap that reads well can still target the wrong node.

## When to use
- A spec/POM uses XPath, `nth-child`, CSS-class, or raw-text selectors.
- Tests fail intermittently on element lookups.
- Someone says "fix/harden/de-flake these locators".

## Workflow
1. **Scan** the provided code and flag every brittle locator:
   - XPath (`//div[...]`), `page.locator('.some-class')`, `:nth-child`, deep CSS
     descendant chains, index-based `.nth(3)`, and unanchored text matches.
2. **Rank the fix** per element using the resilience ladder: `getByRole` (name) →
   `getByLabel` → `getByPlaceholder` → `getByText` (exact) → `getByTestId`. Reach
   for `getByTestId` when semantics are weak, not as the first choice.
3. **Rewrite** each locator, preserving intent. Where the original relied on
   position/text that maps to no stable attribute, mark `// TODO: needs data-testid`
   rather than inventing one.
4. **Emit a rewrite map** (before → after → why) so the change is reviewable.
5. **Note residual risk** — any swap you couldn't confirm without the real DOM.

## Output shape
```
Rewrite map
  ✗ <provided brittle button locator> → ? getByRole('button', { name: '<verified name>' }) // TODO: verify DOM
  ✗ <provided error locator>          → ? getByTestId('<verified testid>')                  // TODO: verify DOM
  ✗ <provided row locator>            → ? getByRole('row', { name: /<verified row name>/ }) // TODO: verify DOM
```
```typescript
// before: paste the actual brittle locator
await page.locator('<provided brittle selector>').fill('<synthetic value>');
// after: replace only from inspected DOM evidence
await page.getByLabel('<verified label from DOM>').fill('<synthetic value>'); // TODO: verify
```

## Guardrails
- These are **proposed swaps the engineer must run and confirm** — never assume the
  new locator resolves to the same element without checking the real DOM.
- Never invent a `data-testid` or accessible name; if none exists, flag that the
  app needs one (`// TODO: needs data-testid`).
- Prefer role/label semantics over testid; testid is the fallback, not the default.
- Do not silently change behavior (strictness, count) — call out multi-match risks.
