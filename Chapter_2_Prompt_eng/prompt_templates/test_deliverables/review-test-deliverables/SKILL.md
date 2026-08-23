---
name: review-test-deliverables
description: >-
  Review existing test plans, scenarios, cases, execution summaries, defect reports,
  coverage reports, and closure artifacts for quality before peer review, release,
  audit, or client handoff. Use when asked to quality-check a QA deliverable, find
  inconsistencies, verify its evidence and version, or decide whether it is ready for
  human review. Produces source-located findings without generating replacement tests,
  approving an artifact, or changing a source system.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Review Test Deliverables

Review existing artifacts against their stated requirements and review basis. Treat
the result as a draft quality assessment, never as approval or release sign-off.

## Workflow

1. Establish the review ID, scope, release or build, environment, as-of time with
   timezone, intended audience, and supplied checklist, template, or policy revision.
   Label an absent review basis as missing rather than inventing one.
2. Inventory every artifact by ID, type, source URI or path, version or revision,
   owner if stated, and access state. Do not review inaccessible content.
3. Check completeness, internal consistency, executable and observable wording,
   explicit cross-artifact links, metric formulas and denominators, evidence
   references, dates, and version alignment.
4. Record each finding against an exact section, page, row, case ID, or line. Separate
   observed evidence from interpretation and use blocker, major, or minor severity
   only with a stated rationale.
5. List conflicts, missing inputs, stale versions, unverifiable claims, and proposed
   dispositions. Do not silently rewrite or repair the source artifact.
6. HUMAN REVIEW GATE: present the draft to the named artifact owner. Require the owner
   to accept, reject, or revise each blocker and authorize any publication or update.

## Output Contract

Return these fields:

- Review ID; as-of timestamp and timezone; scope; release or build; environment; audience.
- Review basis: source, version, and applicability.
- Source inventory table: Artifact ID | Type | Source URI or path | Version or revision |
  Stated owner | Access state.
- Findings table: Finding ID | Artifact ID | Exact location | Category | Severity |
  Observed evidence | Recommended disposition.
- Cross-artifact inconsistencies.
- Missing, stale, inaccessible, and unverified inputs.
- Redaction register: item | reason | display treatment | original preserved.
- Draft assessment: ready for human review, needs revision, or indeterminate.
- HUMAN REVIEW GATE: review owner | required confirmations | accepted dispositions |
  sign-off status | publication status.

## Scope Boundary

- Review the quality of supplied deliverables; do not generate test plans, test cases,
  execution results, coverage conclusions, closure reports, or release decisions.
- Check whether traceability and evidence references exist and agree; leave coverage
  sufficiency analysis to the coverage analyzer.

## Guardrails

- Never invent artifact contents, IDs, versions, owners, evidence, metrics, approvals,
  or review criteria. Mark absent facts missing or unverified.
- Never label an artifact approved, final, compliant, released, or signed off.
- Redact secrets and personal data from displayed output when necessary, label each
  redaction, and preserve the original. Never claim redaction was performed if it was not.
- Do not publish, share externally, overwrite artifacts, or mutate trackers without
  explicit authorization after the human review gate.
