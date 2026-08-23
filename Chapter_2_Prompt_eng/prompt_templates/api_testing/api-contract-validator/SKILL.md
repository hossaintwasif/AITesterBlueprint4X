---
name: api-contract-validator
description: >-
  Compare observed HTTP API requests and responses with an OpenAPI or equivalent
  endpoint contract. Use when asked to validate a response against an HTTP specification,
  find API contract drift, check status codes or headers, or review captured request and
  response evidence. Produce a conformance report without designing general API coverage;
  use a message-specific validator for AsyncAPI and standalone JSON Schema artifacts.
license: MIT
metadata:
  author: TheTestingAcademy
  category: API Testing
  version: 1.0.0
---

# API Contract Validator

Validate observed API behavior against an identified contract version.

## Inputs and evidence

Require the contract, its version or revision, and a captured request/response or runner
output. Record the method, path, status, media type, and evidence source. Mark missing
material `Not provided`; never synthesize traffic.

## Workflow

1. Resolve the observed exchange to the exact contract operation and response.
2. Check documented status, headers, required fields, types, nullability, enums, formats,
   and additional-property rules.
3. Classify every check as `Conforms`, `Mismatch`, `Ambiguous`, or `Not verifiable`.
4. Cite the contract pointer and minimal redacted evidence for every finding.
5. Separate implementation drift from possible contract staleness; do not choose a source
   of truth without owner confirmation.
6. **HUMAN REVIEW GATE (mandatory).** Ask the API owner to confirm the contract version
   and findings before recommending a specification or implementation change.

## Output shape

| Check | Contract pointer | Observed evidence | Result | Follow-up |
|---|---|---|---|---|

Include the evidence source, contract revision, unresolved ambiguities, and review decision.

## Guardrails

- Treat examples as examples, not schema constraints.
- Never mark an unobserved check as passing or fabricate a response, field, or result.
- Redact tokens, cookies, keys, personal data, and confidential payload values.
- Do not call a live endpoint unless the user confirms authorization, target environment,
  and request scope; default to offline evidence review.
