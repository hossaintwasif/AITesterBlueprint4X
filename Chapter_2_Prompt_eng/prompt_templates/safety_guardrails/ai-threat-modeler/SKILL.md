---
name: ai-threat-modeler
description: >-
  Build an evidence-backed threat model and authorized test charter for an AI,
  LLM, RAG, or agent system. Use when a tester needs to map assets, actors, trust
  boundaries, model and provider dependencies, memory, retrieval, tools, abuse
  cases, controls, and residual risk before safety or security testing begins.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# AI Threat Modeler

Create a review-ready threat model that distinguishes documented architecture from
assumptions. Stop at test design unless the approved scope explicitly authorizes execution.

## Workflow

1. Record the system owner, approved scope, environment, build, model/provider and version,
   prompt/configuration revision, data stores, tools, and supplied architecture artifacts.
2. Map assets, actors, entry points, data flows, trust boundaries, external providers,
   retrieval, memory, tool calls, logs, and administrative paths. Mark absent details
   `Not specified`.
3. Derive abuse cases for instruction manipulation, unauthorized access, data disclosure,
   unsafe output, excessive agency, availability, and supply-chain dependencies. Tie every
   case to a documented component or label it `Hypothesis`.
4. Map each abuse case to an existing control, a safe staging test, evidence to capture,
   impact, likelihood rationale, and residual risk. Use synthetic identities, records,
   secrets, and canaries.
5. Prioritize a test charter without claiming complete coverage. Route prompt injection,
   leakage, tool authorization, content safety, and fairness cases to their specialist skills.
6. Present the model and charter as a draft for the security and system owners to approve.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Not tested | architecture section or test ID | documented control | no run performed | source link or none | missing fact or planned validation |

Record exact build, model, prompt, policy, guardrail, tool, corpus, and environment versions
where applicable. Use `Not tested` for all proposed cases until execution evidence exists.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic inputs.
  If authorization or isolation is absent, stop at the draft charter.
- Never fabricate an architecture fact, policy, control, test result, metric, source, trace,
  or evidence link. Record missing information as `Not specified`.
- Never claim the system is safe, secure, compliant, certified, or fully covered from a threat
  model, an incomplete test set, or missing evidence.
- Treat risk ratings and control effectiveness as proposals until the named human approvers
  confirm them.
