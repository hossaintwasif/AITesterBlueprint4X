---
name: pw-visual-regression
description: >-
  Sets up Playwright visual/screenshot regression testing. Use when an SDET says
  "add visual regression", "snapshot this component", "set up toHaveScreenshot",
  "mask the dynamic parts of this page", or "manage baselines". Produces snapshot
  tests with masking, thresholds, and a baseline strategy — a draft the engineer
  runs to generate and review the first baselines.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW Visual Regression

You set up **snapshot tests whose first baselines the engineer must generate and
eyeball** — never trust an auto-approved baseline. You make snapshots deterministic.

## When to use
- A page or component needs pixel/visual regression coverage.
- Flaky snapshot diffs need masking or threshold tuning.
- Someone says "add visual regression", "manage/update baselines".

## Workflow
1. **Authorize the capture** — confirm an approved non-production target, synthetic
   data/identity, allowed navigation and side effects, and a stable reset state.
2. **Pick the smallest stable target** — prefer a component locator over a full
   page; less surface means fewer false diffs.
3. **Neutralize non-determinism before snapping:** `mask` dynamic regions (dates,
   avatars, ads), disable animations (`animations: 'disabled'`), freeze data, and
   pin viewport + a consistent font/rendering environment (ideally Docker in CI).
4. **Configure tolerances** deliberately — `maxDiffPixelRatio` / `threshold` in
   config, not sprinkled ad hoc. Tight enough to catch real regressions.
5. **Protect visual evidence** — classify screenshots as potentially sensitive. Use a
   supplied policy to mask/redact secrets, tokens, PII, confidential data, and volatile
   regions; approve repository audience, access, retention, and deletion before storage.
6. **Establish baselines** via `--update-snapshots`, then **review each PNG by eye**
   before committing — a wrong baseline locks in the bug.
7. **Document the update flow** so baselines are refreshed intentionally, per platform.
8. **HUMAN REVIEW GATE (mandatory).** Before capture, update, or commit, require approval
   of the target/data, scope, mask/redaction policy, tolerances, baseline image, audience,
   access, retention, and deletion.

## Output shape
```typescript
import { test, expect } from '@playwright/test';
import { approvedVisualPolicy } from './approved-visual-policy';

test('dashboard card matches baseline', async ({ page }) => {
  await page.goto(approvedVisualPolicy.path);
  const card = approvedVisualPolicy.target(page);
  await expect(card).toBeVisible();                       // web-first: wait for render
  await expect(card).toHaveScreenshot(approvedVisualPolicy.baselineName, {
    animations: 'disabled',
    mask: approvedVisualPolicy.maskedRegions(page),
    maxDiffPixelRatio: approvedVisualPolicy.maxDiffPixelRatio,
  });
});
```
```
# fail closed unless the exact reviewed spec and Playwright project are supplied
: "${VISUAL_REVIEW_SPEC:?set exact approved visual spec}"
: "${VISUAL_REVIEW_PROJECT:?set approved Playwright project}"
npx playwright test "$VISUAL_REVIEW_SPEC" --project="$VISUAL_REVIEW_PROJECT" --update-snapshots
```

## Guardrails
- Baselines are **generated then human-reviewed** — never auto-approve; a bad
  baseline turns a bug green forever. Never assume a locator/testid exists.
- The policy module is project-supplied and human-approved; withhold screenshots if
  sensitive regions cannot be reliably masked/redacted or access controls are unknown.
- Mask every sensitive and dynamic region and disable animations, or evidence may leak
  data and diffs will be flaky.
- Pin viewport, OS, and fonts; snapshots taken on different platforms won't match —
  generate per-project baselines in the CI environment, not just locally.
- No `waitForTimeout` before snapping; wait on a web-first assertion instead.
- Never capture against production, a real user account, or unowned data without explicit
  authorization. Do not update or commit baselines before the mandatory human gate.
- Never run an unscoped `--update-snapshots`; require the exact approved spec and project
  so unrelated baselines cannot be rewritten.
