---
name: pw-ci-configurator
description: >-
  Generates CI configuration (GitHub Actions) for a Playwright suite. Use when an
  SDET says "set up Playwright in CI", "add a GitHub Actions workflow", "shard my
  tests across jobs", "upload traces and the HTML report", or "run browsers in a
  matrix". Produces a workflow with install, sharding, blob/HTML reporting, and
  artifacts — a draft the engineer commits and runs on their pipeline.
license: MIT
metadata:
  author: TheTestingAcademy
  pack: playwright
  version: 1.0.0
---

# PW CI Configurator

You draft a **CI workflow the engineer must commit and run on their runner** —
never a guaranteed-green pipeline. You wire in sharding, reporting, and artifacts.

## When to use
- A repo needs Playwright running on GitHub Actions.
- A slow suite should be sharded across parallel jobs.
- Someone wants trace/video/report artifacts on failure.

## Workflow
1. **Confirm the runtime** — Node version, package manager, and which projects/
   browsers must run. Don't assume; ask if unstated.
2. **Install correctly** — cache deps, then `npx playwright install --with-deps`
   for the browsers actually used (don't install all if only Chromium is needed).
3. **Authorize CI execution** — confirm an approved non-production target, synthetic
   test identity/data, allowed writes and other side effects, cleanup/reset behavior,
   request and retry volume, concurrency, and abort limits. Start with a manual trigger;
   enable push/PR triggers only after the target and execution policy are approved.
4. **Shard for speed** — a matrix of `shardIndex/shardTotal`, each job running
   `--shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}` with the **blob**
   reporter, then a final `merge-reports` job to produce one HTML report.
5. **Minimize and classify evidence** — default to `trace: 'retain-on-failure'`,
   `video: 'retain-on-failure'`, and `screenshot: 'only-on-failure'`. Inventory exact
   artifact paths and classify possible secrets, tokens, PII, and confidential data.
6. **Review artifact handling** — redact or exclude sensitive evidence; approve the
   paths, uploader permissions, viewer access, retention, and deletion policy before upload.
7. **Persist only approved evidence** — upload the approved blob/report paths needed for
   merging and failure-only traces/videos; do not use broad workspace globs.
8. **Set CI ergonomics** — use retries and workers only within the approved execution
   budget, and `fail-fast: false` only when continuing other shards cannot multiply harm.
9. **HUMAN REVIEW GATE (mandatory).** Stop before committing or enabling the workflow
   until a human approves its trigger, target, identity/data, side effects, cleanup,
   retry/concurrency/abort budget, and artifact sensitivity, redaction, access, and retention.

## Output shape
```yaml
name: playwright
on: workflow_dispatch # add push/PR only after execution authorization
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true # safer default; relax only inside the approved execution budget
      matrix:
        shard: ${{ fromJSON(vars.PLAYWRIGHT_APPROVED_SHARDS) }}
    steps:
      - uses: actions/checkout@<approved-checkout-immutable-sha>
      - uses: actions/setup-node@<approved-setup-node-immutable-sha>
        with: { node-version: '${{ vars.PLAYWRIGHT_NODE_VERSION }}', cache: npm }
      - run: npm ci
      - run: npm run playwright:install-ci # project script installs the approved browser set
      - run: npx playwright test --shard=${{ matrix.shard.index }}/${{ matrix.shard.total }} --reporter=blob
      - uses: actions/upload-artifact@<approved-upload-artifact-immutable-sha>
        if: always()
        with:
          name: blob-${{ matrix.shard.index }}
          path: blob-report # exact path must pass the artifact review gate
          retention-days: ${{ fromJSON(vars.PLAYWRIGHT_ARTIFACT_RETENTION_DAYS) }}
  merge-reports:
    if: always()
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<approved-checkout-immutable-sha>
      - uses: actions/setup-node@<approved-setup-node-immutable-sha>
        with: { node-version: '${{ vars.PLAYWRIGHT_NODE_VERSION }}', cache: npm }
      - run: npm ci
      - uses: actions/download-artifact@<approved-download-artifact-immutable-sha>
        with:
          pattern: blob-*
          path: all-blob-reports
          merge-multiple: true
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
      - uses: actions/upload-artifact@<approved-upload-artifact-immutable-sha>
        with:
          name: playwright-html-report
          path: playwright-report # exact reviewed path; contains potentially sensitive data
          retention-days: ${{ fromJSON(vars.PLAYWRIGHT_ARTIFACT_RETENTION_DAYS) }}
```

## Guardrails
- This is a **draft the engineer must commit and run** — never assume the Node
  version, package manager, browser set, or secret names; confirm them.
- `PLAYWRIGHT_NODE_VERSION` must be a repository-approved, currently supported Node
  release compatible with the project; never silently select or retain an EOL runtime.
- Replace every action placeholder with a reviewed current release pinned to its immutable
  commit SHA; record the source and review date. Do not enable a mutable or stale major tag.
- Require reviewed `PLAYWRIGHT_APPROVED_SHARDS`, artifact retention, and browser-install
  script inputs; missing values must fail closed rather than selecting defaults.
- Never hardcode credentials; reference `secrets.*`, don't invent values.
- Shards emit **blob** reports merged in a follow-up job — don't upload conflicting
  HTML reports per shard.
- Treat traces, screenshots, videos, network payloads, and reports as potentially
  containing secrets, tokens, PII, or confidential business data.
- Default trace/video/screenshot capture to failure-only settings and upload only exact,
  approved paths after redaction, least-privilege access, and retention review.
- Use `if: always()` only for reviewed artifacts required for report merging; keep optional
  diagnostic uploads failure-only and never upload the entire workspace.
- Never point a retrying or sharded job at production, shared identities, or unowned data.
  Stop on unexpected writes, external effects, cleanup failure, or volume-limit breach.
- Do not enable CI execution or artifact upload before the mandatory human review gate.
