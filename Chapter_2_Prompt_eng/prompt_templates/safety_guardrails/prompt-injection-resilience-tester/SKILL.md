---
name: prompt-injection-resilience-tester
description: >-
  Design and assess authorized prompt-injection resilience tests for AI, LLM,
  RAG, and agent systems. Use when a tester needs coverage for direct or indirect
  instruction attacks, retrieved untrusted content, instruction hierarchy,
  obfuscation, multi-turn persistence, canary exfiltration, or injection-triggered
  tool behavior without using real secrets or production side effects.
license: MIT
metadata:
  author: TheTestingAcademy
  category: AI Safety and Guardrails
  version: 1.0.0
---

# Prompt Injection Resilience Tester

Build a reproducible injection matrix and report only behavior demonstrated by captured runs.
Use benign objectives and canaries so a successful test cannot expose real data or cause harm.

## Workflow

1. Confirm written authorization, staging isolation, allowed channels, prohibited actions,
   rate limits, stop conditions, and the human owner. Without these, produce a plan only.
2. Record the build, model/provider and version, system/developer prompt revision, guardrail
   configuration, retrieval corpus revision, tools, temperature/seed when available, and run ID.
3. Design synthetic cases across direct input, retrieved documents, web or file content,
   multi-turn context, encoding or obfuscation, conflicting instructions, and tool handoffs.
   Use a unique benign canary as the protected target; never use a real secret.
4. Define the expected control from the supplied policy or specification. If it is absent,
   write `Not specified`; do not invent the expected refusal or priority rule.
5. Execute only approved cases. Capture the input identifier, output, retrieval context,
   guardrail decision, tool trace, latency, and repetitions. Redact sensitive incidental data.
6. Report successful attacks, blocked attempts, inconsistent outcomes, and untested paths.
   A blocked sample is evidence for that run only, not proof of resilience.

## Evidence register

Classify every statement as `Observed`, `Inferred`, `Hypothesis`, or `Not tested`.

| Classification | Source / run ID | Expected control | Observed result | Evidence artifact | Unresolved gap |
|---|---|---|---|---|---|
| Observed / Inferred / Hypothesis / Not tested | case and repetition ID | cited policy behavior | captured behavior or no run | redacted output and trace | variance or missing path |

Record exact build, model, prompt, policy, guardrail, corpus, tool, and environment versions.
Keep raw observations separate from inferred cause and remediation hypotheses.

--- HUMAN REVIEW GATE ---
Unverified items:
Remaining risks:
Required approver:
Decision: approve / revise / reject

## Guardrails

- Run only in an explicitly authorized staging or sandbox environment using synthetic inputs,
  identities, secrets, canaries, and mock tools. Stop before any external side effect.
- Never fabricate a policy, payload result, model response, tool trace, metric, source, or
  evidence link. Mark missing facts `Not specified` and absent runs `Not tested`.
- Never claim safe, secure, compliant, injection-proof, or fully tested from sampled results.
- Require the security owner to approve the corpus and the human release owner to decide how
  findings affect deployment.
