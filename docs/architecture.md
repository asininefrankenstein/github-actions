# Architecture Guide

A concise reference for the building block CI/CD design used in this repository.

---

## Philosophy

Each workflow in this repository is a **building block**: one responsibility, one artifact. Blocks compose into E2E pipelines by declaring `needs:` dependencies between jobs. Because every block is a standalone reusable workflow, individual blocks can be tested, versioned, and reused across pipelines without modification.

The two rules that make composition work:

1. **One block = one `pipeline-meta-{block}` artifact.** Every block uploads its result metadata as a named artifact so downstream jobs and the summary collector can consume it.
2. **Blocks do not know about each other.** A block reads its own inputs, does its work, and writes its metadata. Orchestration is the caller's responsibility.

---

## Block Catalogue

| Block | Workflow | Artifact | Stage |
|-------|----------|----------|-------|
| build-artifact | docker-build.yml | pipeline-meta-build-artifact | 1: Build |
| test-artifact | image-validate.yml | pipeline-meta-test-artifact | 2: Test |
| release-gate | release-gate.yml | pipeline-meta-release-gate | 3: Manual Gate |
| semantic-release | semantic-release.yml | pipeline-meta-semantic-release | 6: Release |
| helm-publish | helm-publish.yml | pipeline-meta-helm-publish | Optional |
| webhook | webhook.yml | pipeline-meta-webhook | Optional |
| pipeline-summary | pipeline-summary.yml | pipeline-metadata | Collector |

Stages 1–6 represent the canonical ordering for a full production pipeline. Optional blocks slot in wherever the calling pipeline needs them. The `pipeline-summary` block always runs last.

---

## Artifact Convention

**Per-block artifacts** follow the naming pattern `pipeline-meta-{block}` and contain a single file, `meta.json`, with the block's result data. Retention is 30 days.

**The merged artifact** produced by `pipeline-summary` is named `pipeline-metadata` and contains `pipeline-metadata.json` — a single document that aggregates all block results for the run. Retention is 90 days.

JSON Schema Draft-07 files in `docs/schemas/` document the exact shape of each block's `meta.json` as well as the merged `pipeline-metadata.json`:

| Schema file | Describes |
|-------------|-----------|
| `docs/schemas/meta-build.json` | `pipeline-meta-build-artifact` artifact |
| `docs/schemas/meta-test-artifact.json` | `pipeline-meta-test-artifact` artifact |
| `docs/schemas/meta-release-gate.json` | `pipeline-meta-release-gate` artifact |
| `docs/schemas/meta-release.json` | `pipeline-meta-semantic-release` artifact |
| `docs/schemas/meta-helm.json` | `pipeline-meta-helm-publish` artifact |
| `docs/schemas/meta-webhook.json` | `pipeline-meta-webhook` artifact |
| `docs/schemas/meta-pipeline.json` | merged `pipeline-metadata` artifact |

---

## `did-not-run` Sentinel

`pipeline-summary` iterates over the fixed list of known blocks. For any block whose `pipeline-meta-{block}` artifact is absent — because that block was not included in this pipeline run — the merged metadata records:

```json
{ "status": "did-not-run" }
```

This ensures the merged document always has an entry for every block, making downstream consumers (dashboards, compliance checks) straightforward to write without special-casing missing keys.

---

## Three Prescribed E2E Pipelines

Three reference pipelines covering the common development workflow are provided in `docs/`:

### `docs/example-dev-pipeline.yml` — Feature branch / dev push

Runs on every push to a feature branch. Executes the fast feedback loop: lint only. No build, no release.

### `docs/example-pr-pipeline.yml` — Pull request

Runs on `pull_request` events. Executes build and test. No release gate or semantic release — produces a validated build artifact for review.

### `docs/example-main-pipeline.yml` — Main branch / production

Runs on push to `main`. Executes the full pipeline: build → test → release gate (manual approval) → semantic release → helm publish → webhook → pipeline summary.

All three pipelines end with `pipeline-summary` using `if: always()` to capture metadata regardless of intermediate failures.

---

## Schemas

JSON Schema Draft-07 files in `docs/schemas/` provide machine-readable contracts for every block's artifact output. Use them to:

- Validate `meta.json` files in tests or local tooling
- Generate typed clients for consuming pipeline metadata
- Document the fields that each block guarantees to emit

The top-level merged schema is `docs/schemas/meta-pipeline.json`. It includes the `blocks` object whose property keys are the block names from the catalogue above and whose values conform to the individual block schemas.
