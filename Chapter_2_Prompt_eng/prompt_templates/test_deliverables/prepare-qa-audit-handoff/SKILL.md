---
name: prepare-qa-audit-handoff
description: >-
  Prepare an auditor-facing QA handoff by mapping a supplied audit request or control
  list to approved test deliverables and evidence IDs, custodians, access instructions,
  retention terms, and open gaps. Use for internal audit, customer assurance,
  regulatory evidence requests, due diligence, or transfer to an audit liaison. Builds
  the handoff index and chain-of-custody record without interpreting unstated controls,
  asserting compliance, transmitting artifacts, or signing on behalf of an owner.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Prepare QA Audit Handoff

Package approved QA records around the auditor's explicit request. Report what is
available and missing while leaving compliance conclusions to authorized reviewers.

## Workflow

1. Freeze the handoff ID and version, audit request reference and revision, review
   period, product and release scope, intended recipient, data boundary, and as-of time
   with timezone.
2. Inventory only approved deliverables and evidence manifests. Record source version,
   custodian, approval state, access classification, and current availability.
3. Map each supplied request or control ID to evidence and deliverable IDs with a
   concise, source-based rationale. Mark unsupported mappings unfulfilled or unverified.
4. Verify supplied access, retention, legal-hold, confidentiality, redaction, and
   recipient-authorization records. Do not invent policy terms or grant access.
5. Prepare the handoff index, chain-of-custody log, access expiry, recipient questions,
   and gaps or exceptions. Keep compliance conclusion not assessed.
6. HUMAN REVIEW GATE: require the audit liaison, evidence custodian, data owner, and any
   required compliance reviewer to approve content, redactions, recipients, and transfer.

## Output Contract

Return these fields:

- Handoff ID and version; audit request ID and revision; review period; product and
  release scope; intended recipient; data boundary; as-of timestamp and timezone.
- Source inventory table: Source ID | Type | URI or path | Version | Approval state |
  Custodian | Access classification | Availability.
- Request mapping table: Request or control ID | Supplied text and source revision |
  Deliverable and evidence IDs | Mapping rationale | Custodian | Fulfillment state.
- Gaps and exceptions table: Request or control ID | Missing item | Evidence of gap |
  Impact | Stated owner | Due date if stated.
- Chain-of-custody log: Artifact or bundle ID | From | To | Transfer method | Timestamp |
  Receipt evidence | State.
- Access and retention table: Artifact or bundle ID | Authorized recipients | Access path |
  Access expiry | Retention source and period | Legal-hold state.
- Recipient questions and pending acknowledgments.
- Redaction register: item | data class | display treatment | authorization |
  original preserved.
- Compliance conclusion: not assessed.
- HUMAN REVIEW GATE: audit liaison | custodian | data owner | compliance reviewer |
  sign-off status | transfer and publication status.

## Scope Boundary

- Map an explicit audit request to already approved deliverables and curated evidence;
  do not create test evidence, assess coverage, write a closure report, or decide release.
- Organize a handoff; do not interpret law, invent controls, certify compliance, grant
  access, or transmit artifacts.

## Guardrails

- Never invent request text, controls, mappings, evidence, custodians, approvals,
  timestamps, retention terms, access rights, receipts, or compliance conclusions.
- Treat no response, inaccessible evidence, or an absent artifact as a gap, never proof
  of compliance.
- Redact secrets and personal data from displayed working copies, record the treatment,
  preserve originals, and honor the supplied data boundary.
- Do not publish, send, upload, grant access, approve the handoff, or sign for another
  person without explicit human authorization after the review gate.
