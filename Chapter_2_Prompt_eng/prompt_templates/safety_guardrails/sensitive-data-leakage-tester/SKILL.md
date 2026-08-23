---
name: sensitive-data-leakage-tester
description: >-
  Design and assess authorized sensitive-data leakage tests for AI, LLM, RAG,
  memory, and agent systems. Use when a privacy or security tester needs to check
  synthetic PII and secret canaries, tenant isolation, prompts, context, retrieval,
  caches, logs, telemetry, errors, model providers, or retention paths for exposure.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# Sensitive Data Leakage Tester

Trace synthetic canaries through every approved data surface and distinguish an observed leak
from an untested or merely suspected path. Never introduce real credentials or customer data.

## Workflow

1. Confirm written authorization, privacy owner, staging boundaries, permitted surfaces,
   retention and deletion rules, redaction requirements, and stop conditions.
2. Record the build, model/provider and version, prompt/configuration revision, retrieval and
   memory settings, tenant setup, logging/telemetry configuration, and run ID.
3. Create unique synthetic canaries for each data class and tenant. Document where each canary
   is seeded, where it may legitimately appear, and where disclosure is prohibited.
4. Test approved flows across user input, generated output, retrieval, memory, session changes,
   cross-tenant access, errors, caches, traces, logs, telemetry, exports, and provider calls.
5. Capture exact canary matches, destination, identity/tenant, timestamps, trace IDs, redacted
   artifacts, repetitions, and cleanup evidence. Absence in sampled artifacts is not proof of
   absence elsewhere.
6. Report confirmed exposures, inferred propagation paths, hypotheses, not-tested surfaces,
   data-retention gaps, and required containment as a draft for privacy/security review.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Observed / Inferred / Hypothesis / Not tested | canary and trace ID | cited isolation or redaction rule | exact match, no match, or no run | redacted log/output | uninspected channel or retention question |

Record exact build, model, prompt, policy, guardrail, corpus, tenant, logging, provider, and
environment versions. Preserve canary provenance and cleanup status.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic inputs,
  identities, PII, secrets, and canaries. Do not copy production data into a test corpus.
- Never fabricate a policy, leak, clean result, metric, trace, source, deletion event, or
  evidence link. Mark missing facts `Not specified` and uninspected surfaces `Not tested`.
- Never claim safe, private, compliant, leak-free, or fully tested from sampled observations.
- Do not probe another tenant, provider, log store, or production system without explicit scope;
  require privacy and security owners to review severity and remediation.
