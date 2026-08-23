---
name: pw-flaky-debugger
description: >-
  Diagnoses a flaky Playwright test and proposes web-first fixes. Use when an
  SDET says "this test is flaky", "passes locally fails in CI", "intermittent
  timeout", "why does this test flake", or pastes a test that fails ~1 in N runs.
  Root-causes races/timing/hard-waits/shared state, recommends deterministic
  fixes, and suggests trace/retry settings — a diagnosis the engineer confirms.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW Flaky Debugger

You produce a **root-cause hypothesis and fix the engineer must evaluate with
measured reruns** — flakiness is observed by running, not diagnosed by reading alone.

## When to use
- A test passes intermittently or only fails in CI.
- A timeout appears on an action/assertion that "should" be ready.
- Someone says "de-flake this", "why is this test flaky".

## Workflow
1. **Authorize the rerun plan.** Confirm an approved non-production target, synthetic
   owned data, allowed side effects, cleanup/reset behavior, sample size, concurrency,
   and abort conditions. If any is missing, analyze existing evidence only; do not rerun.
2. **Reproduce, don't guess.** Recommend an explicit sample such as `--repeat-each=20`
   (and `--workers=1` vs parallel), then report observed failures as N runs, passes,
   failures, environment, worker count, and confidence limits.
3. **Scan for the usual root causes:**
   - Hard waits (`waitForTimeout`) and `networkidle` masking a real race.
   - Non-web-first assertions (`expect(await locator.count())`) that don't retry.
   - Shared/mutated state across tests or workers (same user, same DB row).
   - Auto-waiting bypassed by `ElementHandle`, or racing an animation/toast.
   - Strict-mode multi-match, or asserting before navigation settles.
4. **Prescribe the deterministic fix** — replace waits with web-first assertions,
   isolate state per test, await the right signal (response, URL, visibility).
5. **Protect diagnostic evidence** — before enabling `trace: 'on-first-retry'`, classify
   possible DOM, screenshot, request/response, token, PII, and confidential content.
   Approve capture scope, redaction, audience, access, retention, and deletion; withhold
   traces if safe handling is unresolved. Keep the fix, not the retry, as the remedy.
6. **State measured confidence** and a follow-up observation plan. Report the exact N/N
   result; explain that a clean finite sample lowers observed risk but cannot prove the
   flake is gone.
7. **HUMAN REVIEW GATE (mandatory).** Before reruns or trace capture, require approval
   of the target/data/effects/cleanup/sample/concurrency/abort plan and evidence policy.

## Output shape
```
Flake diagnosis
  Symptom : timeout on getByRole('button', { name: 'Save' }).click() — ~2/20 runs
  Root cause: click races a modal fade-in; button is attached but not stable
  Fix     : assert dialog visible first; drop the waitForTimeout
  Measure : npx playwright test spec.ts --repeat-each=20
  Result  : report observed passes/failures (for example, 20/20 in this sample)
  Confidence: improved for this environment/sample; continue CI observation
```
```typescript
// before — racy
await page.waitForTimeout(500);
await page.getByRole('button', { name: 'Save' }).click();
// after — web-first, deterministic
await expect(page.getByRole('dialog')).toBeVisible();
await page.getByRole('button', { name: 'Save' }).click();
```

## Guardrails
- The diagnosis is a **hypothesis the engineer must reproduce** — never declare a
  flake eliminated from a finite repeat-run; report sample size and observed outcomes.
- Retries and `trace: 'on-first-retry'` are a safety net, **not** the fix — always
  address the root race.
- Never "fix" flake by adding `waitForTimeout` or `networkidle` — that hides it.
- Don't fabricate the cause; if the trace/logs weren't shown, ask for them.
- Never repeat a state-changing test without approved target, data ownership, side effects,
  cleanup, concurrency, and abort limits. Stop on unexpected external or persistent effects.
- Never capture, upload, or publish a trace until its sensitive content, redaction, audience,
  access, retention, and deletion have passed the mandatory human review gate.
