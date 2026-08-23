---
name: content-safety-guardrail-evaluator
description: >-
  Evaluate an AI system's content-safety guardrails against a supplied policy and
  approved test corpus. Use when a safety tester needs to measure unsafe acceptance,
  appropriate refusal or redirection, over-refusal, policy-category coverage,
  multi-turn behavior, obfuscation, or multilingual consistency before a release.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# Content Safety Guardrail Evaluator

Measure policy behavior without inventing policy rules or treating automated evaluation as a
release decision. Balance unsafe acceptance with over-refusal of legitimate requests.

## Workflow

1. Confirm the policy owner, exact policy/taxonomy version, approved synthetic or sanitized
   corpus, authorized staging environment, reviewer access controls, and stop conditions.
2. Record the build, model/provider and version, system prompt revision, moderation/guardrail
   configuration, locale, temperature/seed when available, evaluator version, and run ID.
3. Map each case to a cited policy rule and expected allow, refuse, redirect, or escalate
   outcome. Mark uncited expectations `Not specified`; do not author policy by assumption.
4. Include approved positive controls, negative controls, benign near-boundary requests,
   multi-turn cases, transformations, obfuscation, and supported languages. Minimize exposure
   to harmful material and never expand it beyond the approved corpus.
5. Capture outputs and guardrail decisions. Report counts and denominators for unsafe
   acceptance, correct handling, over-refusal, inconsistent handling, and not-tested cases.
6. Record human reviewer disagreements and confidence limits where applicable. Present
   thresholds and release impact only as recommendations for the policy/release owners.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Observed / Inferred / Hypothesis / Not tested | corpus item and repetition ID | cited policy rule | captured allow/refuse/redirect/escalate result | redacted output and decision trace | reviewer disagreement or missing category |

Record exact build, model, prompt, policy, guardrail, corpus, evaluator, locale, and environment
versions. Keep observed behavior separate from evaluator inference and root-cause hypotheses.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic,
  sanitized, or otherwise approved inputs; restrict corpus and output access.
- Never fabricate a policy rule, expected label, model output, evaluation result, denominator,
  metric, reviewer decision, source, trace, or evidence link.
- Never claim safe, compliant, certified, unbiased, or fully covered from an automated or
  incomplete evaluation. A threshold result is evidence, not a release decision.
- Pause and escalate content outside the approved corpus or reviewer handling rules; require
  the policy and release owners to approve conclusions and deployment impact.
