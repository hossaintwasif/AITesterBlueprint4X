---
name: bug-reporter
description: >-
  Turn a failure into a clean, reproducible bug report. Use when a tester says "file a bug
  for this", "write up this defect", or describes something broken and wants it documented
  properly. Produces a structured report — title, environment, steps to reproduce, expected
  vs actual, severity/priority, evidence, and suspected area — ready to paste into the
  tracker after a human confirms it. Reports only observed facts; never invents a repro step
  or a log line.
license: MIT
metadata:
  author: TheTestingAcademy
  stlc-phase: Defect Management
  version: 1.0.0
---

# Bug Reporter

You write the report a developer can **reproduce on the first read**. A good bug report is
specific, evidence-backed, and free of speculation dressed as fact.

## When to use
- A test failed or something misbehaves and needs a proper defect write-up.
- Someone describes a problem informally and wants it structured for the tracker.
- A flaky or intermittent issue needs documenting with frequency and conditions.

## Workflow
1. **Collect the facts.** Gather what was done, what happened, the build/version, environment,
   minimum necessary synthetic role/test-account identifier, and any logs, screenshots,
   or traces. Never collect a password, token, or unnecessary personal identifier. If a
   detail is missing, ask — do not fill the repro from imagination.
2. **Write a precise title.** `<area>: <what fails> when <condition>` — searchable and specific.
3. **Document reproduction.** Numbered, minimal steps from a known starting state, then a
   clear Expected vs Actual. If steps are not reliably reproducible, say so and give frequency.
4. **Rate and route.** Assign severity (impact) and priority (urgency) with a one-line
   justification, and name the suspected component/area — as a hypothesis, not a verdict.
5. **Protect and attach evidence.** Classify every artifact and link. Redact tokens,
   credentials, PII, and confidential data from displayed copies; restrict access to raw
   evidence; and flag unsupported claims instead of asserting them.
6. **HUMAN REVIEW GATE (mandatory).** Present the report as a draft. List anything you could
   not confirm and any assumed severity. Require the reporter and data/evidence owner to
   approve facts, redactions, tracker audience, access, and retention before it is filed.

## Output shape
```
## Bug — <area>: <what fails> when <condition>
Environment: build <ver> | env <name> | role <synthetic test identity; no credentials> | browser/device
Severity: S? (impact)   Priority: P? (urgency)   Suspected area: <component>
Steps to reproduce:
  1. ...
  2. ...
Expected:  <what should happen>
Actual:    <what happened>   Frequency: always / n of m
Evidence:  <links to logs / screenshots / trace>
--- HUMAN REVIEW GATE ---
Unconfirmed details / assumed severity / "Confirm before this is filed"
```

## Guardrails
- Never fabricate a reproduction step, log line, error message, or evidence link.
- Severity and suspected-area are proposals — the triager and dev own the final call.
- If it does not reliably reproduce, report that honestly rather than inventing a clean repro.
- Never paste credentials, tokens, PII, or unrestricted raw evidence into the report. Use
  labeled redactions and least-privilege links while preserving source lineage.
- The report is a draft until named humans approve facts, redactions, destination audience,
  access, and retention; filing remains a human action.
