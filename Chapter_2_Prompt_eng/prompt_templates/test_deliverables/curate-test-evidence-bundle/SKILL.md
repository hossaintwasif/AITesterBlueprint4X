---
name: curate-test-evidence-bundle
description: >-
  Inventory and validate existing test evidence such as logs, screenshots, traces,
  reports, recordings, and defect links into a versioned manifest for release, audit,
  incident, or client review. Use when asked to assemble an evidence pack, verify
  artifact provenance and freshness, identify missing proof, calculate file hashes, or
  prepare safe sharing. Does not generate evidence, assign test results, configure
  reporters, or claim that an artifact proves more than its source supports.
license: MIT
metadata:
  author: TheTestingAcademy
  category: Test Deliverables
  version: 1.0.0
---

# Curate Test Evidence Bundle

Create a provenance-first manifest of evidence that already exists. Preserve originals
and separate artifact integrity from the correctness of the claim it supports.

## Workflow

1. Record the bundle ID and version, purpose, scope, release or immutable build,
   environment, collection cutoff, and as-of time with timezone.
2. Inventory each existing artifact by source URI or path, type, linked case, run,
   defect, or claim, capture time and actor when stated, and access state.
3. Validate accessibility, non-empty content, format readability, build and environment
   alignment, freshness, and duplicate identity. Compute a checksum only from bytes
   actually read; otherwise mark the checksum unavailable.
4. Classify sensitivity using the supplied policy. Identify secrets and personal data
   before display or sharing. Preserve originals; create or describe a redacted working
   copy only when authorized and maintain its lineage to the source.
5. Record missing, corrupt, stale, mismatched, inaccessible, duplicate, and unverified
   evidence without manufacturing replacements.
6. HUMAN REVIEW GATE: require the evidence owner and data owner to confirm inclusion,
   exclusions, redactions, access, retention, and recipients before upload or publication.

## Output Contract

Return these fields:

- Bundle ID and version; purpose; scope; release or immutable build; environment;
  collection cutoff; as-of timestamp and timezone.
- Evidence manifest table: Evidence ID | Artifact type | Source URI or path | Supports |
  Linked case, run, or defect | Build | Environment | Captured at | Captured by |
  Size | Hash algorithm and value | Sensitivity | Verification state.
- Integrity and freshness findings.
- Missing and inaccessible evidence register: Expected evidence | Basis | State |
  Impact | Stated owner.
- Duplicate and mismatch register.
- Redaction register: Original evidence ID | Working-copy ID | Data class | Method |
  Authorized by | Original preserved | Verification state.
- Access and retention table: Evidence ID | Access class | Approved recipients |
  Retention source and period | Expiry if stated.
- Bundle completeness assessment labeled draft.
- HUMAN REVIEW GATE: evidence owner | data owner | required confirmations |
  sign-off status | sharing and publication status.

## Scope Boundary

- Curate evidence produced by tests and tools; do not run tests, create screenshots or
  logs, integrate reporters, update execution status, or infer pass and fail outcomes.
- Record what an artifact supports; do not perform release sign-off, compliance
  assessment, or audit-request mapping.

## Guardrails

- Never invent files, links, hashes, timestamps, actors, test results, access rights,
  retention rules, or evidence contents.
- Never alter, overwrite, or redact the authoritative original. Label transformed
  working copies and retain source lineage.
- Never expose credentials, tokens, personal data, or restricted artifacts in the
  manifest; use labeled redactions and least-privilege references.
- Do not upload, transmit, publish, approve, or sign off the bundle without explicit
  human authorization after the review gate.
