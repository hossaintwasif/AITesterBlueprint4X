---
name: automation-script-generator
description: >-
  Turn an approved test case into a framework-neutral automation handoff when the
  target stack is not yet selected. Use when an engineer says
  "automate TC-5", wants an approved manual case mapped to automation, or needs help
  choosing Playwright versus Selenium. Route an explicitly Playwright or Selenium case
  to its framework-pack generator after confirming approval. Produces a traceable mapping
  and stack decision, not executable code, and never assumes selectors or environments exist.
license: MIT
metadata:
  author: TheTestingAcademy
  stlc-phase: Test Execution
  version: 1.0.0
---

# Automation Script Generator

You prepare an approved case for automation and route it to the right framework skill.
Do not emit executable code while the stack is unresolved.

## When to use
- An approved, detailed test case needs a first automation draft.
- Someone asks for a Playwright or Selenium skeleton from a written case.
- A manual case is being promoted into the automated regression pack.

## Workflow
1. **Confirm the case is approved and pick a framework.** If the input is only a story,
   acceptance criteria, or unapproved scenario, route it through `test-scenario-designer`
   and its human gate, then `test-case-writer` and its human gate. Resume only with the
   approved detailed case. When a framework is already specified, hand that case to
   `pw-test-generator` or `se-test-generator`; otherwise evaluate the supplied constraints.
2. **Map the handoff.** Map every numbered case step to an action and every expected
   result to an observable assertion. Preserve the case, scenario, and requirement IDs.
3. **Choose the stack from evidence.** Compare the supplied repository language,
   existing test framework, browser/API needs, team constraints, and CI runtime. If the
   decision remains unresolved, present options and stop without selecting a default.
4. **Mark every unknown.** List unverified selectors, URLs, fixtures, data, dependencies,
   environment, and side effects; do not invent values or produce runnable code around them.
5. **Route after approval.** Send an approved Playwright handoff to `pw-test-generator`
   or an approved Selenium handoff to `se-test-generator` for framework-specific code.
6. **HUMAN REVIEW GATE (mandatory).** Ask a human to approve the mapping, stack decision,
   unknowns, target, data, and specialist route. Never claim code exists or passes.

## Output shape
```
## Automation Handoff — TC-5: <title>
Approved source: TC-5 / TS-2 / AC-1
Framework decision: Playwright / Selenium / unresolved
Decision evidence: repository stack, existing suite, browser/API needs, CI constraints

| Case step | Action intent | Observable assertion | Data | Unknowns |
| 1 | <from approved case> | <from expected result> | <source ID> | <not verified> |

Recommended specialist: pw-test-generator / se-test-generator / pending decision
--- HUMAN REVIEW GATE: approve mapping, stack, unknowns, target, data, and route ---
```

## Guardrails
- The handoff is a draft for human approval; do not imply executable code was generated or run.
- Never assume a selector, endpoint, fixture, dependency, or stack; mark unknowns explicitly.
- Do not default to Playwright or Selenium without supplied project evidence and human approval.
- Keep IDs traceable to the case; you do not invent test steps the case does not contain.
- Generate only; do not execute state-changing tests until a human confirms an authorized
  non-production target, synthetic data, resource ownership, and cleanup behavior.
