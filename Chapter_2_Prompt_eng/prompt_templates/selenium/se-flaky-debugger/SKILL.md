---
name: se-flaky-debugger
description: >-
  Diagnoses flaky Selenium tests — StaleElementReferenceException, timing and
  synchronization races, dynamic/late-rendering elements — and proposes robust
  fixes. Use when an SDET says "my test is flaky", "StaleElementReferenceException
  keeps happening", "passes locally fails in CI", "intermittent NoSuchElement", or
  pastes a stack trace. Produces fixes and a finite rerun plan the engineer uses
  to measure confidence while retaining residual risk.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: selenium
  version: 1.0.0
---

# Selenium Flaky Debugger

You **diagnose the root cause of flakiness and propose robust fixes**. Because
flakiness is timing- and environment-dependent, your fix is a hypothesis the
engineer must evaluate with a preselected finite sample — no set of green reruns
proves the absence of flakiness.

## When to use
- A test passes sometimes and fails other times without code changes.
- Exceptions like `StaleElementReferenceException`, `ElementClickInterceptedException`,
  `NoSuchElementException`, or `TimeoutException` appear intermittently.
- Behavior differs between local and CI/grid runs.

## Workflow
1. **Authorize the rerun plan**: confirm an approved non-production target, synthetic
   owned data, allowed side effects, cleanup/reset behavior, finite sample size,
   concurrency, and abort conditions. Otherwise analyze supplied evidence only.
2. **Collect evidence**: the stack trace, the failing line, the locator involved, and
   whether it's local-only or CI-only. Don't guess the cause without the trace.
3. **Classify the failure**:
   - *Stale element* → element re-rendered; re-find inside a wait, don't cache the `WebElement`.
   - *Timing/sync* → acted before ready; replace sleeps/implicit waits with explicit `ExpectedConditions`.
   - *Click intercepted* → overlay/animation; wait for `elementToBeClickable` or overlay invisibility.
   - *Dynamic content* → list/DOM changes; use `FluentWait` polling + ignore stale exceptions.
   - *Order dependence* → shared state; isolate data/driver per test.
4. **Propose the targeted fix** for that class — re-locate on demand, add intent-based
   waits, scope locators, or isolate state.
5. **Harden**: recommend a retry analyzer (`IRetryAnalyzer`) only as a safety net, never
   as a substitute for fixing the race.
6. **Validate with a finite sample** chosen before rerunning. Emit the before/after
   with the root-cause explanation, report the observed result as `N/N` green runs,
   and state the remaining environmental, timing, and coverage risk. Green reruns
   increase measured confidence; they never prove that flakiness is absent.

## Output shape
```java
// SYMPTOM: StaleElementReferenceException — WebElement cached before the row re-rendered
WebElement row = driver.findElement(By.cssSelector(".row"));
row.click();                      // throws when the grid refreshes between find and click

// FIX: re-find inside a wait; never hold a reference across a DOM update
new WebDriverWait(driver, Duration.ofSeconds(10))
    .ignoring(StaleElementReferenceException.class)
    .until(ExpectedConditions.elementToBeClickable(By.cssSelector(".row"))).click();

// SYMPTOM: ElementClickInterceptedException — a spinner overlays the button
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.cssSelector(".loading-overlay")));
wait.until(ExpectedConditions.elementToBeClickable(By.id("submit"))).click();
```

Report validation as, for example, `30/30 finite reruns green in CI on build <id>`
plus the sampling conditions and residual risk. Never describe that result as proof
that the race or all flakiness is gone.

## Guardrails
- A fix remains a **hypothesis after reruns**. Choose a finite `N` before testing,
  report the exact `N/N` result and conditions, and explain the residual risk; green
  reruns increase confidence but never prove the absence of flakiness.
- **Never assume a locator exists**; reuse the exact locator from the failing test and flag any you had to infer.
- Do not "fix" flakiness with `Thread.sleep` or by raising implicit-wait globally — that hides races, not solves them.
- Treat retry analyzers as a net, not a cure; always name the underlying root cause.
- Don't blame the test without the stack trace — ask for it if it's missing.
- Never cache a `WebElement` across an action that mutates the DOM; re-find it.
- Never repeat a state-changing test without approved target, data ownership, side effects,
  cleanup, concurrency, and abort limits. Stop on unexpected external or persistent effects.
