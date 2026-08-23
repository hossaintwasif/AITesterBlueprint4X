---
name: pw-fixture-designer
description: >-
  Designs custom Playwright test fixtures (auth/session, seeded data, page
  objects) with correct setup/teardown and scope. Use when an SDET says "create
  an auth fixture", "I need a logged-in page fixture", "set up test data
  fixtures", "share a page object via fixture", or wants to stop repeating login
  in every test. Produces a typed fixtures module — a draft to wire in and run.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW Fixture Designer

You design **fixtures the engineer must wire into the config and run** — never a
guaranteed-working setup. You pick the right scope, and always tear down cleanly.

## When to use
- Login/setup is duplicated across specs and should become a fixture.
- Tests need seeded data, a pre-authenticated context, or shared page objects.
- Someone says "design/create a fixture for X".

## Workflow
1. **Classify each fixture's scope.** Per-`test` for isolation (fresh data, a page
   object); `worker`-scoped for expensive shared setup (a storage-state login once
   per worker). Default to test scope unless reuse is safe and read-only.
2. **Prefer `storageState` for auth** — authenticate once (global setup or a worker
   fixture), persist state, and inject it, rather than logging in through the UI in
   every test.
3. **Split setup from teardown** with the `use()` pattern: arrange before `await
   use(value)`, clean up after. Every created resource (DB row, temp user) gets
   deleted or reset.
4. **Type the fixtures** via `test.extend<MyFixtures>()` so consumers get IntelliSense.
5. **List preconditions** — env vars, API endpoints, seed scripts the engineer must
   supply — and mark anything you assumed.
6. **HUMAN REVIEW GATE (mandatory).** Before any setup or teardown request, require
   approval of the non-production target, exact contract-backed operation, test identity,
   synthetic data, resource ownership, and cleanup scope. Stop if any is unresolved.

## Output shape
```typescript
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import {
  createOwnedTestResource,
  deleteOwnedTestResource,
} from '../support/contract-backed-test-data';

type Fixtures = { loginPage: LoginPage; ownedResourceId: string };

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));            // test-scoped, fresh per test
  },
  ownedResourceId: async ({ request }, use) => {
    const resource = await createOwnedTestResource(request);
    await use(resource.id);
    await deleteOwnedTestResource(request, resource.id);
  },
});
export { expect };
```

Treat the setup/teardown imports as placeholders the team must implement from reviewed
contract operations; do not infer endpoints, methods, payloads, or identifiers.

## Guardrails
- This is a **draft the engineer must wire into `playwright.config.ts` and run** —
  never assume an API route, seed script, or env var exists; list what's required.
- Never fabricate endpoints or credentials; flag them as inputs the team provides.
- Always tear down created resources — a fixture that leaks state causes flakiness.
- Never issue setup or teardown writes until the mandatory review gate is approved;
  use only synthetic resources owned by the approved test identity in non-production.
- Never delete a resource unless ownership and the exact cleanup operation are confirmed.
- Treat `storageState` as a credential-bearing artifact: use a synthetic account, keep it
  out of Git and general CI artifacts, restrict access, and expire or revoke it after use.
- Do not put auth in a UI-login-per-test; use protected `storageState`. No `waitForTimeout`.
