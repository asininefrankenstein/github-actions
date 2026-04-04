# Architecture Guide

A concise reference for the component-based CI/CD design used in this repository.

---

## Philosophy

Each workflow is a **component**: one responsibility, one artifact. Components compose into pipelines by declaring `needs:` dependencies between jobs. Because every component is a standalone reusable workflow, individual components can be tested, versioned, and reused across pipelines without modification.

Two rules make composition work:

1. **One component = one `pipeline-meta-{block}` artifact.** Every component uploads its result metadata so downstream jobs and the summary collector can consume it.
2. **Components do not know about each other.** A component reads its own inputs, does its work, and writes its metadata. Orchestration is the caller's responsibility.

---

## Component Catalogue

| Component | Workflow | Artifact | Purpose |
|-----------|----------|----------|---------|
| lint | component-lint.yml | lint-results-* | Multi-language linting |
| test | component-test.yml | test-results | Test runner with coverage |
| semantic-release | component-semantic-release.yml | pipeline-meta-semantic-release | Version, tag, GitHub Release |
| container-build | component-container-build.yml | pipeline-meta-build-artifact | Multi-arch container images |
| helm-publish | component-helm-publish.yml | pipeline-meta-helm-publish | Helm chart OCI publishing |
| pipeline-summary | component-pipeline-summary.yml | pipeline-metadata | Metadata collector |

---

## Three-Stage Pipeline

The prescribed pipeline pattern splits CI/CD into three workflow files:

| Stage | Workflow | Trigger | Components |
|-------|----------|---------|------------|
| PR | `pr.yml` | Pull request | lint, test, container-build (no push) |
| CI | `ci.yml` | Push to main | lint, test, approval gate, semantic-release |
| Release | `release.yml` | Tag `v*` | container-build, helm-publish, pipeline-summary |

See [pipeline-three-stage-go.md](pipeline-three-stage-go.md) for the full design spec and [examples.md](examples.md) for ready-to-use templates.

---

## Artifact Convention

**Per-component artifacts** follow the naming pattern `pipeline-meta-{block}` and contain a single file, `meta.json`, with the component's result data. Retention is 30 days.

**The merged artifact** produced by `pipeline-summary` is named `pipeline-metadata` and contains `pipeline-metadata.json` -- a single document that aggregates all component results for the run. Retention is 90 days.

---

## `did-not-run` Sentinel

`pipeline-summary` iterates over a fixed list of known blocks. For any block whose `pipeline-meta-{block}` artifact is absent, the merged metadata records:

```json
{ "status": "did-not-run" }
```

This ensures the merged document always has an entry for every block, making downstream consumers straightforward to write without special-casing missing keys.
