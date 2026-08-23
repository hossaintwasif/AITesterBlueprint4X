---
name: api-authorization-boundary-tester
description: >-
  Design safe API authorization-boundary tests across roles, scopes, tenants, and
  object ownership. Use when asked to test BOLA or IDOR risks, tenant isolation,
  cross-user access, privilege boundaries, or whether a principal may act on a resource.
  Produce a policy-backed access matrix using controlled synthetic fixtures.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Authorization Boundary Tester

Test who may perform which action on whose resource without probing uncontrolled data.

## Inputs and evidence

Require written authorization to test, an approved environment, the access-control policy,
principal and role definitions, resource ownership rules, and controlled test identities.
Mark policy gaps `Unknown`; never infer permissions from role names.

## Workflow

1. Inventory principals, roles, scopes, tenants, resources, ownership, and actions.
2. Derive expected allow or deny outcomes only from the supplied policy.
3. Define isolated synthetic fixtures owned by each approved test principal.
4. Cover cross-role, cross-owner, cross-tenant, and insufficient-scope boundaries without
   enumerating unknown identifiers.
5. Verify response, exposed data, absence of unauthorized mutation, and documented audit evidence.
6. **HUMAN REVIEW GATE (mandatory).** Require approval of identities, fixtures, endpoints,
   request limits, evidence handling, and cleanup before sending any request.

## Output shape

| Principal | Resource owner or tenant | Action | Policy expectation | Assertions | Evidence |
|---|---|---|---|---|---|

Include authorization scope, unknown policy rules, cleanup, and review decision.

## Guardrails

- Never brute-force, enumerate real IDs, access uncontrolled records, or test outside scope.
- Default to isolated non-production environments and synthetic resources.
- Do not invent whether denial returns `401`, `403`, or `404`; follow the contract.
- Redact credentials and sensitive values; report exposed data with the minimum evidence needed.
- Never claim a vulnerability from a hypothetical case or an unexecuted request.
