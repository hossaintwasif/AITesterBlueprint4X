---
name: api-workflow-tester
description: >-
  Design stateful tests spanning multiple API calls, lifecycle transitions,
  asynchronous jobs, events, or callbacks. Use when asked to test an end-to-end API
  workflow, chain endpoints, verify a resource lifecycle, or validate eventual outcomes.
  Produce a cross-operation sequence with state evidence and cleanup, not a single-endpoint matrix.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Workflow Tester

Verify state and data integrity across documented API transitions.

## Inputs and evidence

Require the workflow requirement or contract, documented states and transitions, actors,
operations or events, and available persistence or event evidence. Mark undocumented timing,
terminal states, and side effects `Not specified`.

## Workflow

1. Map starting state, allowed transitions, actors, calls, events, and terminal outcomes.
2. Trace IDs, correlation values, and data dependencies passed between steps.
3. Define response and persisted-state assertions after each transition.
4. Define polling, callback, or event checks using only documented timing and terminal states.
5. Add negative transition cases and safe compensating cleanup for owned test resources.
6. **HUMAN REVIEW GATE (mandatory).** Confirm the sequence, side effects, test identities,
   environment, and cleanup before writing automation or invoking any operation.

## Output shape

| Step | State before | Call or event | Expected state | Evidence | Cleanup |
|---|---|---|---|---|---|

Include prerequisites, correlation map, unresolved requirements, and review decision.

## Guardrails

- Never invent a state, transition, callback, timeout, event, or consistency window.
- Never assume a successful response proves a downstream state change; require evidence.
- Use synthetic, uniquely identified records and redact credentials and sensitive data.
- Do not execute against a live system without explicit authorization, environment scope,
  request limits, and ownership of every resource that may be changed or removed.
