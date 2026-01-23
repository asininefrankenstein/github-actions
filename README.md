# Central Reusable GitHub Actions

A centralized collection of reusable GitHub Actions workflows for CI/CD standardization across projects.

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

See [docs/workflows.md](docs/workflows.md) for detailed workflow documentation.

## Required Secrets

| Secret | Used By | Description |
|--------|---------|-------------|
| `GITHUB_TOKEN` | All workflows | Auto-provided, used for most operations |
| `APP_ID` | semantic-release | GitHub App ID for triggering downstream workflows |
| `APP_PRIVATE_KEY` | semantic-release | GitHub App private key |

## License

MIT
