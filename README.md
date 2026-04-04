# Reusable GitHub Actions Components

Component workflows for CI/CD pipelines. Each component handles one responsibility and composes into end-to-end pipelines via `needs:` dependencies.

## Quick Start

Reference any component from your repository:

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/component-lint.yml@main
    with:
      yaml: true
      go: true
```

See [docs/examples.md](docs/examples.md) for complete pipeline templates.

## Components

| Component | Description |
|-----------|-------------|
| `component-lint.yml` | Multi-language linting (Python, Go, Shell, YAML, Helm, JSON) |
| `component-test.yml` | Test runner with coverage (Go, Python, Node.js, Bun) |
| `component-semantic-release.yml` | Semantic versioning, tags, and GitHub Releases via [go-semantic-release](https://github.com/go-semantic-release/semantic-release) |
| `component-container-build.yml` | Multi-arch container builds with native runners |
| `component-helm-publish.yml` | Helm chart publishing to OCI registries |
| `component-pipeline-summary.yml` | Collects block metadata into a single pipeline artifact |

## Three-Stage Pipeline

The recommended pipeline pattern for Go projects with containers and Helm charts:

```
PR -----> lint, test, verify, container build (no push)

main ---> lint, test, approve, semantic-release (tag + GitHub Release)
                                    |
                               tag v1.2.3
                                    |
                                    v
release -> container build + push, helm publish, pipeline summary
```

| Template | Trigger | Jobs |
|----------|---------|------|
| [example-three-stage-pr.yml](docs/example-three-stage-pr.yml) | Pull request | lint, test, verify, container build |
| [example-three-stage-ci.yml](docs/example-three-stage-ci.yml) | Push to main | lint, test, approve, semantic-release |
| [example-three-stage-release.yml](docs/example-three-stage-release.yml) | Tag `v*` | container build, helm publish, summary |

See [pipeline-three-stage-go.md](docs/pipeline-three-stage-go.md) for the full design spec.

## Configurable Variables

Set in **Settings > Secrets and variables > Actions > Variables**:

| Variable | Default | Used by |
|----------|---------|---------|
| `GO_VERSION` | `stable` | lint, test |
| `TEST_PACKAGES` | `./...` | test |
| `COVERAGE_THRESHOLD` | `0` | test |
| `HELM_CHART_NAME` | repo name | helm-publish |
| `HELM_CHART_PATH` | `chart` | helm-publish |

## Required Secrets

| Secret | Used by | Description |
|--------|---------|-------------|
| `APP_ID` | semantic-release | GitHub App ID (tags must trigger downstream workflows) |
| `APP_PRIVATE_KEY` | semantic-release | GitHub App private key |

## Conventional Commits

| Commit | 0.x.x Bump | >=1.0.0 Bump |
|--------|-----------|-------------|
| `feat:` | Minor (0.X.0) | Minor (x.Y.0) |
| `fix:` | Patch (0.0.X) | Patch (x.y.Z) |
| `feat!:` | Minor (0.X.0) | **Major (X.0.0)** |
| `chore:`, `docs:` | Patch (0.0.X) | Patch (x.y.Z) |

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Detailed component reference |
| [docs/examples.md](docs/examples.md) | Pipeline templates and configuration guide |
| [docs/pipeline-three-stage-go.md](docs/pipeline-three-stage-go.md) | Three-stage pipeline design spec |
| [docs/architecture.md](docs/architecture.md) | Building block design philosophy |

## License

MIT
