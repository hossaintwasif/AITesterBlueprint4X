---
name: ai-fairness-bias-evaluator
description: >-
  Design and assess evidence-backed fairness and bias evaluations for AI, LLM,
  recommendation, ranking, or agent behavior. Use when a responsible-AI tester
  needs approved subgroup, paired counterfactual, intersectional, allocation,
  quality-of-service, or stereotype tests using synthetic or consented data.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# AI Fairness and Bias Evaluator

Surface measurable disparities and qualitative harms without inventing demographic data,
claiming causality, or turning a sampled evaluation into legal or compliance certification.

## Workflow

1. Confirm the decision context, affected population, system owner, approved attributes,
   applicable supplied policy, privacy/legal reviewers, authorized staging environment,
   and prohibited data uses.
2. Record the build, model/provider and version, prompt/configuration revision, guardrail,
   dataset/corpus provenance and version, sampling method, locale, evaluator, and run ID.
3. Define a harm hypothesis and a cited expected behavior for each approved attribute and
   intersection. Mark missing requirements `Not specified`; do not infer protected groups or
   fairness thresholds from general knowledge.
4. Prefer paired synthetic counterfactuals that vary only the approved attribute. Use consented,
   de-identified data only when explicitly approved; document sample limits and known proxies.
5. Capture per-case outputs and compute pre-approved subgroup rates, deltas, denominators,
   uncertainty, missing groups, and reviewer disagreements. Preserve qualitative examples in
   redacted form.
6. Separate observed disparity from inferred pattern and causal hypothesis. Recommend further
   review or mitigation, then require a fresh evaluation after material changes.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Observed / Inferred / Hypothesis / Not tested | pair/subgroup and run ID | cited fairness requirement | output, rate, delta, uncertainty, or no run | redacted cases and calculation | sample, proxy, intersection, or reviewer gap |

Record exact build, model, prompt, policy, guardrail, dataset, sampling, metric, evaluator,
locale, and environment versions. Always show counts and denominators with aggregate rates.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic inputs by
  default. Never infer or generate sensitive attributes for real people.
- Never fabricate a policy, demographic, label, test result, metric, threshold, source,
  reviewer decision, or evidence link. Mark missing facts and groups explicitly.
- Never claim safe, fair, unbiased, compliant, causal, representative, or fully tested from
  sampled results. Avoid ranking groups or presenting disparity as a trait of people.
- Require domain, privacy, legal, and system owners to review attribute choices, interpretation,
  mitigation, and release impact.
