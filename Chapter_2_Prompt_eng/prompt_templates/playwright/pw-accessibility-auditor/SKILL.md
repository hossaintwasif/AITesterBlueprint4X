---
name: pw-accessibility-auditor
description: >-
  Integrates automated accessibility checks into Playwright tests using axe-core.
  Use when an SDET says "add a11y checks", "run axe on this page", "screen for
  selected WCAG rules", or "triage these accessibility violations". Produces
  @axe-core/playwright-based tests and evidence mapped to a supplied accessibility
  policy; it never determines WCAG compliance, and automated checks cover only a fraction.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW Accessibility Auditor

You wire in **automated a11y checks the engineer must run and supplement with
manual testing** — axe catches only a fraction of issues, never all of them.

## When to use
- A page/component needs automated accessibility coverage.
- Someone wants to triage or gate on axe violations.
- Someone says "add a11y checks", "map these to WCAG".

## Workflow
1. **Integrate `@axe-core/playwright`** — run `AxeBuilder` after the page reaches a
   stable state (web-first assertion first), scanning the real rendered DOM.
2. **Confirm the policy and versions** — record the product's approved accessibility
   standard/conformance target plus installed axe and rule-set versions. Select only
   axe tags supported by that version and mapped by the supplied policy; never silently
   default to a WCAG edition or conformance level.
3. **Scope the scan** — use `.include()`/`.exclude()` for the approved component and
   documented third-party exclusions. Record every exclusion and its owner.
4. **Triage without inventing a gate** — preserve every violation and its axe impact.
   Apply blocking impacts or rule IDs only from the approved policy; impact labels do
   not by themselves establish WCAG conformance or permission to defer an issue.
5. **Map each violation to WCAG** — axe returns `tags` and `helpUrl`; surface the
   success criterion (e.g. 1.4.3 contrast, 4.1.2 name/role/value) so it's actionable.
6. **Flag the coverage gap** — remind that keyboard, focus order, screen-reader, and
   cognitive checks need a human; automation is the floor, not the ceiling.
7. **HUMAN REVIEW GATE (mandatory).** Require the accessibility owner to confirm the
   target standard, axe tags/version, exclusions, blocking policy, manual coverage,
   and publication wording before enabling a CI gate or making a conformance statement.

## Output shape
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { accessibilityPolicy, approvedPage } from './approved-accessibility-policy';

test('approved page satisfies the configured automated gate', async ({ page }) => {
  await page.goto(approvedPage.path);
  await expect(page.getByRole('heading', { name: approvedPage.heading })).toBeVisible();

  const results = await new AxeBuilder({ page })
    .withTags(accessibilityPolicy.axeTags)
    .analyze();

  const evidence = accessibilityPolicy.redactFindings(results.violations);
  await test.info().attach('axe-violations', {
    body: Buffer.from(JSON.stringify(evidence, null, 2)),
    contentType: 'application/json',
  });

  const blocking = results.violations.filter(
    (violation) => accessibilityPolicy.blockingRuleIds.includes(violation.id));
  expect(blocking, JSON.stringify(blocking, null, 2)).toEqual([]);
});
```

Treat the imported policy/page module as a required, human-approved project input. It
must record the target standard, installed axe/rule-set version, tags, exclusions,
blocking rules, owners, manual-test obligations, and a fail-closed `redactFindings`
implementation. Classify the attached evidence and approve its audience, access,
retention, and deletion before CI publication; withhold it if safe redaction fails.

## Guardrails
- Automated axe checks are the **floor** — this is a draft the engineer must run and
  back with manual keyboard/screen-reader testing; never claim WCAG compliance or
  "fully accessible" from automated results.
- Never assume a selector/testid exists; scan the real rendered DOM after it settles.
- Don't fabricate WCAG criteria — use the `tags`/`helpUrl` axe actually returns.
- Never hardcode a WCAG edition, tags, exclusions, impact threshold, or rule gate without
  the supplied policy and installed axe-version support. Record every non-blocking finding.
- Treat DOM snippets and related evidence as potentially sensitive; redact them and apply
  approved access and retention controls before attaching or publishing artifacts.
- Do not enable the CI gate or publish a conformance statement before the human review gate.
