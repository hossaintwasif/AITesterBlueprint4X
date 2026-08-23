---
name: maintain-test-traceability
description: >-
  Build or update a versioned test traceability register linking requirements and
  acceptance criteria to scenarios, cases, automation, executions, defects, and
  evidence. Use when asked to maintain an RTM, connect test artifacts, validate
  lineage after a requirement or test change, or find broken and stale trace links.
  Records only evidenced relationships and does not assess coverage sufficiency,
  infer pass status, or modify source systems without review.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Maintain Test Traceability

Maintain referential integrity and change lineage across test artifacts. Treat a link
as verified only when an authoritative source explicitly supports it.

## Workflow

1. Freeze the register ID, scope, release or build, environment, as-of time with
   timezone, and authoritative source baselines with versions or revisions.
2. Inventory source and target artifacts using their real IDs and revisions. Record
   inaccessible or missing artifacts without constructing substitute IDs.
3. Add a relationship only when a source reference, metadata field, or reviewed
   mapping proves it. Capture the relation type and evidence location.
4. Validate link targets, revision alignment, build and environment consistency, and
   freshness. Classify each link as verified, stale, broken, or unverified.
5. Produce a change-impact queue for downstream artifacts that may require human
   validation. Treat absent links as unlinked, not automatically untested or failed.
6. HUMAN REVIEW GATE: show proposed additions, changes, and removals to the traceability
   owner. Apply or publish no register change until that owner confirms it.

## Output Contract

Return these fields:

- Register ID and version; as-of timestamp and timezone; scope; release or build;
  environment.
- Source baselines table: Source system or artifact | URI or path | Version or revision |
  Snapshot time | Access state.
- Traceability table: Link ID | From type | From ID and revision | Relation | To type |
  To ID and revision | Evidence source and exact location | Last verified | Link state.
- Stale, broken, unverified, and unlinked items.
- Change-impact table: Changed artifact | Version change | Candidate downstream artifact |
  Evidence for impact | Validation owner if stated | Status.
- Coverage and pass assessment: not performed.
- Redaction register: item | reason | display treatment | original preserved.
- HUMAN REVIEW GATE: traceability owner | proposed mutations | required confirmations |
  register approval status | publication status.

## Scope Boundary

- Maintain IDs, relationships, revisions, and change impact; do not judge whether the
  linked tests provide adequate positive, negative, boundary, or risk coverage.
- Do not log executions, assign test outcomes, calculate pass rates, or create closure
  and release reports.

## Guardrails

- Never infer a relationship from similar names, proximity, or expected process flow.
  Never invent IDs, revisions, evidence links, owners, timestamps, or test outcomes.
- Never equate linked with covered, executed, or passed; preserve those states separately.
- Redact secrets and personal data from displayed output, document the redaction, and
  preserve originals and source references.
- Do not delete links, update an RTM, publish the register, approve coverage, or sign off
  a release without explicit human authorization after the review gate.
