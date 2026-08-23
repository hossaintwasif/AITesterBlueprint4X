---
name: api-performance-test-planner
description: >-
  Create a review-ready API performance plan and optional k6 or JMeter draft. Use
  when asked to plan load, stress, spike, soak, throughput, concurrency, or latency
  testing for APIs. Produce an evidence-based workload, thresholds, monitoring needs,
  and abort conditions without inventing an SLA or starting load automatically.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Performance Test Planner

Translate documented traffic and service objectives into a controlled workload.

## Inputs and evidence

Require the authorized target environment, endpoint mix, traffic evidence, service objectives,
dependencies, test-data strategy, and current baseline if available. Record missing rates,
latency objectives, error budgets, or capacity expectations as `TBD`.

## Workflow

1. Select only the requested test type: baseline, load, stress, spike, or soak.
2. Derive virtual users or request rate, traffic mix, ramp, and duration from supplied evidence.
3. Define checks and thresholds from documented SLOs; keep absent thresholds `TBD`.
4. Specify synthetic data, correlation, server-side monitoring, network context, and cleanup.
5. Draft the requested k6 or JMeter artifact with configurable rates, durations, and safe defaults.
6. **HUMAN REVIEW GATE (mandatory).** Confirm target ownership, rates, duration, schedule,
   data, monitoring, dependencies, and abort conditions before any load is generated.

## Output shape

| Scenario | VUs or RPS | Ramp | Duration | Dataset | Threshold source | Abort condition |
|---|---|---|---|---|---|---|

Include assumptions, monitoring plan, execution prerequisites, and review decision.

## Guardrails

- Never load-test production, a third party, or a shared environment without explicit authorization.
- Never invent traffic, pass/fail thresholds, baselines, bottlenecks, or execution results.
- Start with a reviewed smoke workload; enforce approved request and concurrency ceilings.
- Redact credentials and personal data; use synthetic or approved anonymized datasets.
- Do not infer server capacity or root cause from client latency alone.
