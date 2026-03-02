# Central Reusable GitHub Actions

A centralized collection of reusable GitHub Actions workflows for CI/CD standardization across projects.

See [Architecture Guide](docs/architecture.md) for the building block design.

## Quick Start

Reference any workflow from your repository:

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      python: true
```

## Example Pipelines

| Example | Description |
|---------|-------------|
| [Basic CI](docs/example-caller.yml) | Lint and test on push/PR. |
| [Semantic Release](docs/example-semantic-release.yml) | Auto-version, tag, and release from Conventional Commits. |
| [Go SDK](docs/example-go-sdk-release.yml) | Full pipeline: lint, test, auto-version with GoReleaser hooks. |
| [Docker + Helm](docs/example-docker-helm-release.yml) | Build container, scan, publish Helm chart, create release. |
| [Self-Release](docs/example-self-release.yml) | CI/CD for workflow-only repos like this one. |

See [docs/examples.md](docs/examples.md) for detailed pipeline documentation.

## Available Workflows

| Workflow | Description |
|----------|-------------|
| [lint.yml](docs/workflows.md#lint-workflow) | Multi-language linting (Python, Go, Shell, YAML, Helm) |
| [test.yml](docs/workflows.md#test-workflow) | Test runner with coverage (pytest, go, npm, bun) |
| [semantic-release.yml](docs/workflows.md#semantic-release-workflow) | Automatic semantic versioning with native feat! support |
| [docker-build.yml](docs/workflows.md#docker-build-workflow) | Multi-arch container builds with caching |
| [helm-publish.yml](docs/workflows.md#helm-publish-workflow) | Publish Helm charts to OCI registries |
| [webhook.yml](docs/workflows.md#webhook-workflow) | Post-release webhooks and workflow triggers |
| [image-scan.yml](docs/workflows.md#image-scan-workflow) | Container security scanning with Trivy |
| [ci-cd-unified.yml](docs/workflows.md#ci-cd-unified-workflow) | Complete CI/CD pipeline (lint, test, release) |
| [code-scan.yml](docs/workflows.md#code-scan-workflow) | Trivy filesystem scan (Stage 1 — Code Analysis) |
| [release-gate.yml](docs/workflows.md#release-gate-workflow) | Manual approval gate via GitHub Environment |
| [pipeline-summary.yml](docs/workflows.md#pipeline-summary-workflow) | Collector: merges all block metadata into pipeline-metadata artifact |

See [docs/workflows.md](docs/workflows.md) for detailed workflow documentation.

## Required Secrets

| Secret | Used By | Description |
|--------|---------|-------------|
| `GITHUB_TOKEN` | All workflows | Auto-provided, used for most operations |
| `APP_ID` | semantic-release | GitHub App ID for triggering downstream workflows |
| `APP_PRIVATE_KEY` | semantic-release | GitHub App private key |

## Versioning

This repository uses [Semantic Versioning](https://semver.org/) with go-semantic-release based on [Conventional Commits](https://www.conventionalcommits.org/).

### Initial Development (0.x.x)

During initial development (versions < 1.0.0), the project follows semver spec #4:
> "Major version zero (0.y.z) is for initial development. Anything MAY change at any time."

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (0.x.0) | 0.1.5 → 0.2.0 |
| `fix:` | Patch (0.0.x) | 0.1.5 → 0.1.6 |
| `feat!:` or `fix!:` | **Minor (0.x.0)** | 0.1.5 → 0.2.0 |

**Note:** Breaking changes (`feat!`, `fix!`) bump minor, not major, during 0.x.x versions.

### Stable Releases (≥1.0.0)

After reaching 1.0.0, breaking changes bump the major version:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (x.Y.0) | 1.2.3 → 1.3.0 |
| `fix:` | Patch (x.y.Z) | 1.2.3 → 1.2.4 |
| `feat!:` or `fix!:` | **Major (X.0.0)** | 1.2.3 → 2.0.0 |

### Graduating to v1.0.0

To signal your project is ready for stable release:

**Option 1:** Disable initial development mode in your workflow:
```yaml
release:
  uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
  with:
    allow-initial-development-versions: false
```

**Option 2:** Manually create the v1.0.0 tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

See [docs/examples.md](docs/examples.md) for more details on Conventional Commits.

## License

MIT
