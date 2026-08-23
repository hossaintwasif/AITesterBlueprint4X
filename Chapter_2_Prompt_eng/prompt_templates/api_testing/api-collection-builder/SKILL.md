---
name: api-collection-builder
description: >-
  Convert approved API test cases into a Postman/Newman or Bruno collection. Use
  when asked to build an API collection, make cases runnable in Newman or Bruno,
  parameterize environments, or package requests, assertions, chaining, and cleanup.
  Produce a reviewable execution artifact rather than redesigning API coverage.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Collection Builder

Package approved cases into a portable, environment-safe collection.

## Inputs and evidence

Require approved cases or contract-backed request details, the requested collection format,
and documented assertions. List unknown base URLs, auth sources, variables, and cleanup rules
as unresolved inputs.

## Workflow

1. Map each approved case to one request; preserve its traceability ID.
2. Parameterize base URL, authentication, resource IDs, and environment-specific values.
3. Add only contract-backed status, header, and body assertions.
4. Capture documented response values for dependent requests and add cleanup only when its
   operation and ownership are confirmed.
5. Validate artifact syntax and provide a case-to-request mapping plus run prerequisites.
6. **HUMAN REVIEW GATE (mandatory).** Stop before executing the collection; request approval
   of the environment, credentials source, write operations, request volume, and cleanup.

## Output shape

- Requested collection artifact
- Secret-free environment template
- Case-to-request traceability table
- Unresolved variables, assumptions, and run command
- `--- HUMAN REVIEW GATE ---` with approval status

## Guardrails

- Never embed credentials, tokens, real customer data, or secret example values.
- Never invent an endpoint, field, assertion, dependency, or cleanup operation.
- Never report requests as passing without supplied runner evidence.
- Do not execute writes, deletes, or live requests without confirmed authorization and target;
  default to generating the draft only.
