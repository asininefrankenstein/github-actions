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
| [Release on Tag](docs/example-release-on-tag.yml) | Create GitHub Release when a version tag is pushed. |
| [Uplift + Release](docs/example-uplift-release.yml) | Auto-tag from commits and release in one workflow. |
| [Go SDK](docs/example-go-sdk-release.yml) | Full pipeline: lint, test, auto-tag, GoReleaser multi-platform builds. |
| [Docker + Helm](docs/example-docker-helm-release.yml) | Build container, scan, publish Helm chart, create release. |
| [Self-Release](docs/example-self-release.yml) | CI/CD for workflow-only repos like this one. |

See [docs/examples.md](docs/examples.md) for detailed pipeline documentation.

## Available Workflows

| Workflow | Description |
|----------|-------------|
| [lint.yml](docs/workflows.md#lint-workflow) | Multi-language linting (Python, Go, Shell, YAML, Helm) |
| [test.yml](docs/workflows.md#test-workflow) | Test runner with coverage (pytest, go, npm, bun) |
| [docker-build.yml](docs/workflows.md#docker-build-workflow) | Multi-arch container builds with caching |
| [helm-publish.yml](docs/workflows.md#helm-publish-workflow) | Publish Helm charts to OCI registries |
| [uplift.yml](docs/workflows.md#uplift-workflow) | Semantic versioning from Conventional Commits |
| [release.yml](docs/workflows.md#release-workflow) | Full release pipeline with tests and builds |
| [goreleaser.yml](docs/workflows.md#goreleaser-workflow) | Go multi-platform binary releases |
| [webhook.yml](docs/workflows.md#webhook-workflow) | Post-release webhooks and workflow triggers |
| [image-scan.yml](docs/workflows.md#image-scan-workflow) | Container security scanning with Trivy |

See [docs/workflows.md](docs/workflows.md) for detailed workflow documentation.

## Required Secrets

| Secret | Used By | Description |
|--------|---------|-------------|
| `GITHUB_TOKEN` | All workflows | Auto-provided, used for most operations |
| `APP_ID` | Uplift | GitHub App ID for triggering downstream workflows |
| `APP_PRIVATE_KEY` | Uplift | GitHub App private key |

## License

MIT
