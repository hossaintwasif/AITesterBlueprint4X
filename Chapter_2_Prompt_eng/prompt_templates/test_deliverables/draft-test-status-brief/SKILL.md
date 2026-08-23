---
name: draft-test-status-brief
description: >-
  Draft an as-of QA status brief from approved execution, defect, plan, and risk
  snapshots. Use for daily or weekly testing updates, standups, sprint reports,
  stakeholder summaries, and comparisons with a prior status snapshot. Reports
  sourced progress, changes, blockers, risks, and next actions without logging test
  outcomes, filling missing metrics, closing a cycle, or making a release decision.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Draft Test Status Brief

Turn existing QA records into a time-bounded communication. Keep source freshness and
metric denominators visible so readers can distinguish current facts from unknowns.

## Workflow

1. Record the brief ID, reporting period, audience, scope, release or build,
   environment, and as-of time with timezone.
2. Inventory the approved source snapshots with URI or path, version, snapshot time,
   and access state. Flag stale, partial, conflicting, or inaccessible sources.
3. Copy or calculate metrics only from sourced counts. Show numerator, denominator,
   formula, and scope; keep unreported cases unknown or not run according to the source.
4. Compare with a prior snapshot only when scope, denominator, build, and status
   definitions are compatible. Otherwise state that no valid trend is available.
5. Summarize verified progress, new and resolved blockers, changed risks, and next
   actions. Attribute owners and dates only when the source states them.
6. HUMAN REVIEW GATE: present the draft to the QA lead or status owner. Require
   confirmation of facts, audience, redactions, and distribution before publication.

## Output Contract

Return these fields:

- Brief ID; reporting period; as-of timestamp and timezone; audience; scope; release or
  build; environment.
- Source snapshots table: Source | URI or path | Version | Snapshot time | Access state.
- Executive summary labeled draft.
- Metrics table: Metric | Current numerator and denominator | Current value | Prior
  numerator and denominator | Prior value | Delta | Source and as-of | Verification state.
- Execution distribution exactly as reported by the source.
- New, continuing, and resolved blockers with evidence references.
- Risks and changes since the prior valid snapshot.
- Next actions: action | stated owner | stated due date | source.
- Missing, stale, partial, and conflicting inputs.
- Redaction register: item | reason | display treatment | original preserved.
- HUMAN REVIEW GATE: status owner | required confirmations | sign-off status |
  publication status and approved audience.

## Scope Boundary

- Summarize an existing execution ledger; do not create, update, or infer case results.
- Provide an in-cycle status brief; do not create a closure report, assess coverage,
  recommend go or no-go, or record a release decision.

## Guardrails

- Never invent results, counts, denominators, defects, blockers, owners, dates, trends,
  source links, or explanations for a change.
- Never convert missing or stale information into a green status.
- Redact secrets and personal data from displayed output, label each redaction, and
  preserve originals. Do not expose restricted evidence to an unauthorized audience.
- Keep publication status withheld until the named human approves. Do not publish,
  update a dashboard, declare closure, or sign off a release autonomously.
