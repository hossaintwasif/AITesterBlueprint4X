---
name: ai-agent-tool-safety-tester
description: >-
  Design and assess authorized safety tests for AI agents that call tools or act
  on external systems. Use when a tester needs to verify tool allowlists,
  authentication, authorization, least privilege, argument validation, approval
  gates, dry-run behavior, tenant isolation, idempotency, rollback, or prevention
  of unintended and injection-triggered side effects.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# AI Agent Tool Safety Tester

Verify the boundary between a model's proposal and an external action. Prefer mocks and
read-only dry-runs; never let a safety test create an unapproved real-world side effect.

## Workflow

1. Inventory tools, owners, schemas, credentials, permission scopes, data boundaries, approval
   rules, side effects, rollback paths, and prohibited actions from supplied artifacts.
2. Confirm written authorization, staging isolation, synthetic accounts/data, mock endpoints,
   rate limits, stop conditions, and the human who can approve each state-changing action.
3. Record the build, model/provider and version, prompt/configuration revision, agent runtime,
   tool schema/version, policy/guardrail revision, identity/role, and run ID.
4. Design cases for denied tools, excessive permissions, invalid or injected arguments,
   cross-tenant targets, skipped confirmation, repeated calls, partial failure, timeout,
   retry, cancellation, rollback, and untrusted content influencing tool selection.
5. Execute mocks first. Capture whether an action was proposed, requested, approved, blocked,
   executed, rolled back, or not tested; record exact sanitized arguments and tool responses.
6. Report observed authorization failures and side effects separately from inferred causes and
   remediation hypotheses. Require re-runs after any policy, prompt, model, or tool change.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Observed / Inferred / Hypothesis / Not tested | case and tool-call ID | cited permission or approval rule | proposed, blocked, executed, rolled back, or no run | sanitized trace and state proof | side effect or recovery not verified |

Record exact build, model, prompt, policy, guardrail, agent runtime, tool schema, identity,
corpus, and environment versions. Never infer execution from a natural-language response.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic inputs,
  identities, credentials, records, and mock tools. Obtain a human approval immediately before
  any permitted external or state-changing call.
- Never fabricate a policy, permission, approval, tool call, result, side effect, rollback,
  metric, source, trace, or evidence link. Mark absent facts and runs explicitly.
- Never claim safe, secure, compliant, least-privileged, or side-effect-free from sampled runs.
- Stop on unexpected writes, messages, purchases, deletions, permission changes, or scope escape;
  preserve evidence and escalate to the tool and security owners.
