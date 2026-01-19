# Central Reusable GitHub Actions

A centralized collection of reusable GitHub Actions workflows and composite actions for CI/CD standardization across projects. This repository provides production-ready workflows for linting, testing, multi-architecture Docker builds, Helm chart publishing, semantic versioning, and automated releases.

## Quick Start

Reference any workflow from your repository:

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      python: true
```

## Documentation

- **[Example Workflows](docs/examples.md)** - Copy-and-paste examples for common use cases including:
  - Basic lint and test setup
  - Release on tag creation
  - Chaining uplift and release pipelines
  - Full CI/CD pipeline patterns

## Workflows

### Lint Workflow

Multi-language linting supporting Python (ruff), Go (golangci-lint), Shell (shellcheck), YAML (yamllint), and Helm charts.

**Usage:**

```yaml
name: CI
on: [push, pull_request]

jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      # Enable the linters you need
      python: true
      python-version: '3.12'
      ruff-args: '--select=E,W,F'

      go: true
      go-version: 'stable'

      shell: true
      shellcheck-paths: 'scripts/'

      yaml: true
      yamllint-args: '.github/'

      helm: true
      helm-chart-path: 'charts/'

      fail-fast: true  # Stop on first failure
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `python` | boolean | `false` | Enable Python linting with ruff |
| `python-version` | string | `'3.12'` | Python version to use |
| `ruff-version` | string | `''` | Ruff version (empty for latest) |
| `ruff-args` | string | `'.'` | Additional ruff arguments |
| `go` | boolean | `false` | Enable Go linting with golangci-lint |
| `go-version` | string | `'stable'` | Go version to use |
| `golangci-lint-version` | string | `'latest'` | golangci-lint version |
| `golangci-lint-args` | string | `''` | Additional golangci-lint arguments |
| `shell` | boolean | `false` | Enable shell linting with shellcheck |
| `shellcheck-version` | string | `'stable'` | ShellCheck version |
| `shellcheck-paths` | string | `'.'` | Paths to check (space-separated) |
| `yaml` | boolean | `false` | Enable YAML linting with yamllint |
| `yamllint-config` | string | `''` | Path to yamllint config file |
| `yamllint-args` | string | `'.'` | Additional yamllint arguments |
| `helm` | boolean | `false` | Enable Helm chart linting |
| `helm-chart-path` | string | `'charts/'` | Path to Helm chart(s) |
| `helm-args` | string | `''` | Additional helm lint arguments |
| `working-directory` | string | `'.'` | Working directory for all commands |
| `fail-fast` | boolean | `true` | Stop on first linter failure |

**Outputs:**

| Output | Description |
|--------|-------------|
| `python-status` | Python lint result: success, failure, or skipped |
| `go-status` | Go lint result: success, failure, or skipped |
| `shell-status` | Shell lint result: success, failure, or skipped |
| `yaml-status` | YAML lint result: success, failure, or skipped |
| `helm-status` | Helm lint result: success, failure, or skipped |
| `overall-status` | Overall lint result: success or failure |

---

### Test Workflow

Configurable test runner with auto-detection for pytest, go test, npm test, and bun test. Generates rich GitHub Actions summaries with pass/fail counts, coverage, and duration.

**Usage:**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      framework: 'auto'  # auto-detects: pytest, go, npm, bun
      coverage: true
      coverage-threshold: 80
      timeout-minutes: 30
      artifact-name: 'test-results'
```

**Custom Test Command:**

```yaml
jobs:
  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      test-command: 'make test'
      framework: 'custom'
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `test-command` | string | `''` | Custom test command (overrides framework) |
| `framework` | string | `'auto'` | Test framework: auto, pytest, go, npm, bun, custom |
| `python-version` | string | `'3.12'` | Python version for pytest |
| `go-version` | string | `'stable'` | Go version for go test |
| `node-version` | string | `'20'` | Node.js version for npm/bun |
| `coverage` | boolean | `false` | Enable code coverage collection |
| `coverage-threshold` | number | `0` | Minimum coverage percentage (0 to disable) |
| `test-args` | string | `''` | Additional test arguments |
| `working-directory` | string | `'.'` | Working directory for tests |
| `install-dependencies` | boolean | `true` | Install dependencies before testing |
| `timeout-minutes` | number | `30` | Timeout for test execution |
| `fail-on-error` | boolean | `true` | Fail workflow if tests fail |
| `artifact-name` | string | `'test-results'` | Artifact name (empty to skip upload) |
| `artifact-retention-days` | number | `7` | Days to retain test artifacts |

**Outputs:**

| Output | Description |
|--------|-------------|
| `status` | Test result: passed, failed, or unknown |
| `passed` | Number of passed tests |
| `failed` | Number of failed tests |
| `total` | Total number of tests |
| `coverage` | Coverage percentage (if enabled) |

---

### Docker Build Workflow

Multi-architecture container image building with QEMU, BuildKit, and GHA caching. Automatically generates semantic version tags.

**Usage:**

```yaml
name: Build and Push
on:
  push:
    tags: ['v*']

jobs:
  docker:
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      registry: 'ghcr.io'
      image-name: 'myorg/myapp'
      platforms: 'linux/amd64,linux/arm64'
      push: true
    secrets:
      registry-password: ${{ secrets.GITHUB_TOKEN }}
```

**With Build Arguments:**

```yaml
jobs:
  docker:
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: 'myorg/myapp'
      build-args: |
        VERSION=${{ github.ref_name }}
        BUILD_DATE=${{ github.event.head_commit.timestamp }}
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `registry` | string | `'ghcr.io'` | Container registry |
| `image-name` | string | `''` | Image name (defaults to repository name) |
| `platforms` | string | `'linux/amd64,linux/arm64'` | Target platforms |
| `push` | boolean | `true` | Push image to registry |
| `context` | string | `'.'` | Build context path |
| `file` | string | `'./Dockerfile'` | Path to Dockerfile |
| `build-args` | string | `''` | Build arguments (KEY=VALUE per line) |
| `tags` | string | `''` | Custom tags (overrides auto-generated) |
| `labels` | string | `''` | Custom labels (KEY=VALUE per line) |
| `cache-from` | string | `'type=gha'` | Cache sources |
| `cache-to` | string | `'type=gha,mode=max'` | Cache destinations |
| `provenance` | boolean | `true` | Generate provenance attestation |
| `registry-username` | string | `''` | Registry username |
| `runs-on` | string | `'ubuntu-latest'` | Runner label |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-password` | No | Registry password/token (defaults to GITHUB_TOKEN) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `imageid` | Image ID |
| `digest` | Image digest |
| `metadata` | Build metadata |
| `tags` | Generated tags |
| `labels` | Generated labels |
| `version` | Generated version |

**Required Permissions:**

```yaml
permissions:
  contents: read
  packages: write
```

---

### Helm Publish Workflow

Publish Helm charts to OCI registries with automatic linting and dependency updates.

**Usage:**

```yaml
name: Publish Helm Chart
on:
  push:
    tags: ['v*']

jobs:
  helm:
    uses: jacaudi/github-actions/.github/workflows/helm-publish.yml@main
    with:
      chart-name: 'my-chart'
      chart-path: 'charts/my-chart'
      registry: 'ghcr.io'
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `chart-name` | string | **required** | Name of the Helm chart |
| `chart-path` | string | `''` | Path to chart directory (defaults to charts/<chart-name>) |
| `registry` | string | `'ghcr.io'` | OCI registry |
| `registry-username` | string | `''` | Registry username |
| `repository` | string | `''` | Repository owner (defaults to github.repository_owner) |
| `version` | string | `''` | Chart version (defaults to tag without v prefix) |
| `update-dependencies` | boolean | `true` | Run helm dependency update |
| `lint` | boolean | `true` | Run helm lint |
| `runs-on` | string | `'ubuntu-latest'` | Runner label |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-password` | No | Registry password (defaults to GITHUB_TOKEN) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `chart-name` | Published chart name |
| `chart-version` | Published chart version |
| `chart-ref` | Full OCI reference |

**Required Permissions:**

```yaml
permissions:
  contents: read
  packages: write
```

**Installing Published Charts:**

```bash
# Pull the chart
helm pull oci://ghcr.io/myorg/my-chart --version 1.0.0

# Install the chart
helm install my-release oci://ghcr.io/myorg/my-chart --version 1.0.0
```

---

### Uplift Workflow

Automatic semantic versioning using [Uplift](https://uplift.dev) based on Conventional Commits.

**Usage:**

```yaml
name: Release
on:
  push:
    branches: [main]

jobs:
  version:
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main
    secrets:
      # Optional: Use GitHub App for triggering downstream workflows
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

**Dry Run Mode:**

```yaml
jobs:
  version:
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main
    with:
      dry-run: true
      uplift-args: 'release'
```

**Prerelease Versions:**

```yaml
jobs:
  version:
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main
    with:
      prerelease: 'beta'  # Creates v1.2.3-beta.1
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `uplift-args` | string | `'release'` | Uplift command: release, tag, bump, changelog |
| `dry-run` | boolean | `false` | Run without making changes |
| `fetch-tags` | boolean | `true` | Fetch all tags |
| `config-file` | string | `''` | Path to Uplift config file |
| `skip-changelog` | boolean | `false` | Skip changelog generation |
| `skip-bumps` | boolean | `false` | Skip file version bumps |
| `prerelease` | string | `''` | Prerelease suffix (alpha, beta, rc) |
| `runs-on` | string | `'ubuntu-latest'` | Runner label |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `app-id` | No | GitHub App ID for triggering workflows |
| `app-private-key` | No | GitHub App private key |

**Outputs:**

| Output | Description |
|--------|-------------|
| `version` | New version created |
| `previous-version` | Previous version |
| `changelog` | Generated changelog |
| `released` | Whether a release was created (true/false) |

**Required Permissions:**

```yaml
permissions:
  contents: write
```

> **Note:** Using GITHUB_TOKEN will **not** trigger downstream workflows. To trigger other workflows when a tag is created, provide `app-id` and `app-private-key` secrets for a GitHub App.

---

### Release Workflow

Full release pipeline orchestrating tests, builds, and GitHub release creation.

**Usage:**

```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      run-tests: true
      build-type: 'docker'
      docker-platforms: 'linux/amd64,linux/arm64'
      create-release: true
```

**With GoReleaser:**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      run-tests: true
      test-framework: 'go'
      build-type: 'goreleaser'
      goreleaser-config: '.goreleaser.yml'
```

**Minimal Release (No Build):**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      run-tests: true
      build-type: 'none'
      create-release: true
      release-notes-auto: true
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| **Test Options** |
| `run-tests` | boolean | `true` | Run tests before release |
| `test-command` | string | `''` | Custom test command |
| `test-framework` | string | `'auto'` | Test framework |
| `fail-on-test-failure` | boolean | `true` | Fail release if tests fail |
| **Release Options** |
| `create-release` | boolean | `true` | Create GitHub release |
| `release-tag` | string | `''` | Tag name (defaults to github.ref_name) |
| `release-name` | string | `''` | Release name |
| `release-notes` | string | `''` | Custom release notes |
| `release-notes-auto` | boolean | `true` | Auto-generate notes |
| `release-draft` | boolean | `false` | Create as draft |
| `release-prerelease` | boolean | `false` | Mark as prerelease |
| **Build Options** |
| `build-type` | string | `'none'` | Build type: none, docker, goreleaser, custom |
| `build-command` | string | `''` | Custom build command |
| **Docker Options** |
| `docker-registry` | string | `'ghcr.io'` | Container registry |
| `docker-image-name` | string | `''` | Image name |
| `docker-platforms` | string | `'linux/amd64,linux/arm64'` | Target platforms |
| `docker-context` | string | `'.'` | Build context |
| `docker-file` | string | `'./Dockerfile'` | Dockerfile path |
| `docker-build-args` | string | `''` | Build arguments |
| **GoReleaser Options** |
| `goreleaser-version` | string | `'latest'` | GoReleaser version |
| `goreleaser-args` | string | `''` | Additional arguments |
| `goreleaser-config` | string | `'.goreleaser.yml'` | Config file path |
| `go-version` | string | `'stable'` | Go version |
| **Artifact Options** |
| `artifact-pattern` | string | `''` | Glob pattern for release artifacts |
| `artifact-retention-days` | number | `90` | Artifact retention days |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `docker-registry-password` | No | Registry password for Docker builds |
| `goreleaser-token` | No | Token for GoReleaser |
| `release-token` | No | Token for creating releases |

**Outputs:**

| Output | Description |
|--------|-------------|
| `release-id` | Created release ID |
| `release-url` | Release URL |
| `release-tag` | Release tag name |
| `test-status` | Test result: passed, failed, skipped |
| `build-status` | Build result: success, failure, skipped |
| `docker-digest` | Docker image digest |
| `docker-tags` | Docker image tags |

**Required Permissions:**

```yaml
permissions:
  contents: write
  packages: write  # Only for Docker builds
```

---

## Composite Actions

### Docker Build Action

The Docker composite action is used internally by the docker-build workflow but can also be used directly for more control.

**Usage:**

```yaml
steps:
  - uses: actions/checkout@v4

  - uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}

  - uses: jacaudi/github-actions/.github/actions/docker@main
    with:
      registry: 'ghcr.io'
      image-name: '${{ github.repository }}'
      platforms: 'linux/amd64,linux/arm64'
      push: true
```

### Test Summary Action

Generate rich test summaries for any test framework.

**Usage:**

```yaml
steps:
  - name: Run Tests
    run: pytest --json-report --json-report-file=results.json

  - uses: jacaudi/github-actions/.github/actions/test-summary@main
    if: always()
    with:
      title: 'Test Results'
      results-file: 'results.json'
      format: 'auto'  # auto-detects: junit, pytest-json, go, npm
```

**Manual Input:**

```yaml
- uses: jacaudi/github-actions/.github/actions/test-summary@main
  with:
    title: 'Unit Tests'
    passed: '42'
    failed: '3'
    skipped: '5'
    duration: '1m 23s'
```

---

## Common Patterns

### Full CI/CD Pipeline

```yaml
name: CI/CD
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:

jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      python: true
      yaml: true

  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      coverage: true
      coverage-threshold: 80

  release:
    needs: [lint, test]
    if: startsWith(github.ref, 'refs/tags/v')
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      run-tests: false  # Already ran above
      build-type: 'docker'
      create-release: true
```

### Using Workflow Outputs

```yaml
jobs:
  build:
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: 'myapp'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          echo "Deploying image with digest: ${{ needs.build.outputs.digest }}"
          echo "Tags: ${{ needs.build.outputs.tags }}"
```

### Passing Secrets

Use `secrets: inherit` to pass all secrets:

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      build-type: 'docker'
    secrets: inherit
```

Or pass specific secrets:

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      build-type: 'docker'
    secrets:
      docker-registry-password: ${{ secrets.GHCR_TOKEN }}
```

---

## Required Secrets

| Secret | Used By | Description |
|--------|---------|-------------|
| `GITHUB_TOKEN` | All workflows | Auto-provided, used for most operations |
| `APP_ID` | Uplift | GitHub App ID for triggering downstream workflows |
| `APP_PRIVATE_KEY` | Uplift | GitHub App private key |

---

## External Actions Used

All external actions are pinned to specific versions:

| Action | Version |
|--------|---------|
| `actions/checkout` | v4 |
| `actions/setup-python` | v5 |
| `actions/setup-go` | v5 |
| `actions/setup-node` | v4 |
| `actions/upload-artifact` | v4 |
| `actions/create-github-app-token` | v1 |
| `docker/setup-qemu-action` | v3 |
| `docker/setup-buildx-action` | v3 |
| `docker/login-action` | v3 |
| `docker/metadata-action` | v5 |
| `docker/build-push-action` | v6 |
| `golangci/golangci-lint-action` | v6 |
| `ludeeus/action-shellcheck` | 2.0.0 |
| `azure/setup-helm` | v4 |
| `oven-sh/setup-bun` | v2 |
| `appany/helm-oci-chart-releaser` | v0.5.0 |
| `gembaadvantage/uplift-action` | v2 |
| `goreleaser/goreleaser-action` | v6 |

---

## Local Testing

Test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act (macOS)
brew install act

# List available workflows
act -l

# Run a workflow
act workflow_call -W .github/workflows/lint.yml
```

---

## Contributing

1. Follow Conventional Commits for automatic versioning
2. Pin all external actions to specific versions
3. Include descriptions for all inputs and outputs
4. Generate GitHub Actions summaries for visibility
5. Test workflows locally before pushing

---

## License

MIT
