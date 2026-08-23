---
name: api-resilience-tester
description: >-
  Plan controlled API resilience tests for timeouts, retries, throttling, duplicate
  delivery, dependency failures, idempotency, and recovery. Use when asked to test
  429 handling, retry behavior, duplicate submissions, partial failure, or fault recovery.
  Produce a bounded fault matrix and safe runbook rather than an unapproved chaos run.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Resilience Tester

Verify documented invariants under controlled failure without causing a retry storm.

## Inputs and evidence

Require the resilience requirements, dependency map, target environment, injection method,
monitoring access, and owner-approved safety budget. Mark unspecified retry counts, timeouts,
rate limits, idempotency guarantees, and recovery objectives `Not specified`.

## Workflow

1. Extract documented failure modes, client behavior, service behavior, and invariants.
2. Define one controlled fault and injection point per scenario.
3. Specify observable response, state, recovery, duplication, and telemetry evidence.
4. Set request and concurrency budgets, abort conditions, monitoring, rollback, and cleanup.
5. Order proposed runs from the smallest probe to any sustained or concurrent scenario.
6. **HUMAN REVIEW GATE (mandatory).** Obtain service-owner approval of the environment,
   fault injection, budgets, timing, monitoring, and rollback before execution.

## Output shape

| Fault | Injection point | Expected behavior | Invariant | Abort condition | Evidence |
|---|---|---|---|---|---|

Include prerequisites, safety budget, rollback, unknown guarantees, and review decision.

## Guardrails

- Never inject failure or concurrency into production or shared dependencies without explicit approval.
- Never invent retry counts, timeouts, status codes, rate limits, or recovery results.
- Prevent unbounded retries and stop immediately when an approved abort condition is met.
- Redact secrets and sensitive payloads; use synthetic data.
- Never claim idempotency, exactly-once behavior, or recovery without observed evidence.
