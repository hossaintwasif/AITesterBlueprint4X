---
name: assemble-release-decision-record
description: >-
  Assemble a formal release decision record from supplied exit criteria, approved
  closure and coverage artifacts, risk evidence, waivers, and human approvals. Use
  when preparing a release gate packet, documenting a go or no-go meeting, recording
  a conditional release, or preserving a decision and its conditions. Maps evidence
  to criteria but does not recreate closure metrics, recommend an outcome, approve a
  waiver, execute a release, or make the decision for the authorized owner.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Assemble Release Decision Record

Create an auditable record of the evidence presented and the decision a named human
authority made. Keep the decision unrecorded until authoritative approval is supplied.

## Workflow

1. Record the decision record ID and version, release candidate and immutable build,
   environment, meeting or decision time, and as-of time with timezone.
2. Inventory the authoritative exit policy, criteria, closure report, coverage
   analysis, risk register, evidence manifest, and approval sources by version.
3. Map each supplied criterion to its threshold and sourced actual. Mark it met, not
   met, or unknown only through a direct comparison; mark ambiguous criteria unknown.
4. Record residual risks, conditions, exceptions, and waivers only from supplied
   records. Include owner, approval evidence, scope, and expiry when stated.
5. Leave decision status unrecorded until an authorized human explicitly supplies the
   outcome. Then capture the exact outcome, authority, timestamp, rationale source,
   conditions, dissent, and required follow-up without embellishment.
6. HUMAN REVIEW GATE: require the release owner and required approvers to confirm the
   criteria mapping, decision text, redactions, and distribution. Perform no release.

## Output Contract

Return these fields:

- Decision record ID and version; as-of timestamp and timezone; release candidate;
  immutable build; environment; decision meeting timestamp.
- Source inventory table: Source ID | Type | URI or path | Version or revision |
  Approved by if stated | Source as-of | Access state.
- Criteria table: Criterion ID | Threshold | Sourced actual | Evaluation |
  Evidence source and exact location | Exception or waiver ID.
- Residual risks and conditions: Risk ID | Evidence | Accepted by if stated | Condition |
  Owner if stated | Due or expiry if stated.
- Waiver register: Waiver ID | Scope | Approval source | Approver | Approved at | Expiry.
- Human decision: unrecorded, go, no-go, or conditional-go | decision authority |
  supplied timestamp | rationale source | dissent.
- Follow-up commitments and decision-record version history.
- Missing, stale, conflicting, and unverified inputs.
- Redaction register: item | reason | display treatment | original preserved.
- HUMAN REVIEW GATE: release owner | required approvers | confirmation state |
  sign-off status | publication status.

## Scope Boundary

- Consume approved test closure, coverage, execution, and evidence artifacts; do not
  regenerate their metrics, reassess their findings, or create a closure report.
- Record a human release decision; do not recommend, choose, approve, deploy, roll back,
  or otherwise execute one.

## Guardrails

- Never invent criteria, thresholds, actuals, evidence, risks, waivers, approvers,
  timestamps, rationale, dissent, or decisions.
- Never infer approval from silence, attendance, job title, a green metric, or missing data.
- Redact secrets and personal data from displayed copies, log each redaction, and
  preserve the authoritative original.
- Do not approve waivers, sign for another person, publish the record, or trigger release
  actions without explicit human authorization after the review gate.
