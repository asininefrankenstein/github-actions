# Example Workflows

This directory contains example workflows demonstrating how to use the reusable workflows in this repository. Copy and adapt these examples for your own projects.

## Available Examples

| Example | Description |
|---------|-------------|
| [example-caller.yml](examples/example-caller.yml) | Basic usage of lint and test workflows |
| [example-release-on-tag.yml](examples/example-release-on-tag.yml) | Trigger release pipeline on tag creation |
| [example-uplift-release.yml](examples/example-uplift-release.yml) | Chain uplift and release in one workflow |
| [example-go-sdk-release.yml](examples/example-go-sdk-release.yml) | **Complete Go SDK/library release pipeline** |
| [example-docker-helm-release.yml](examples/example-docker-helm-release.yml) | **Docker + Helm chart release pipeline** |

---

## Example: Basic Lint and Test

**File:** [`examples/example-caller.yml`](examples/example-caller.yml)

Demonstrates calling the lint and test workflows with manual trigger support.

```yaml
name: CI
on:
  push:
    branches: [main]
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
      framework: auto
      coverage: true
```

---

## Example: Release on Tag Creation

**File:** [`examples/example-release-on-tag.yml`](examples/example-release-on-tag.yml)

Triggers the release pipeline when a semantic version tag is pushed (e.g., `v1.0.0`).

```yaml
name: Release
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'
      - 'v[0-9]+.[0-9]+.[0-9]+-*'  # Prereleases

jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      run-tests: true
      create-release: true
      release-notes-auto: true
      build-type: docker  # or: none, goreleaser, custom
```

### Important Note

Tags created by the default `GITHUB_TOKEN` do **not** trigger other workflows. If you use the uplift workflow with `GITHUB_TOKEN`, this workflow will **not** run automatically.

To trigger this workflow from uplift-created tags, you must either:
1. Use a GitHub App token with uplift (see uplift workflow documentation)
2. Chain uplift and release in a single workflow (recommended - see below)

---

## Example: Uplift with Release Pipeline (Recommended)

**File:** [`examples/example-uplift-release.yml`](examples/example-uplift-release.yml)

The **recommended approach** for automated releases. Chains uplift (auto-tagging) with the release pipeline in a single workflow.

```yaml
name: Release
on:
  push:
    branches: [main]

jobs:
  # Step 1: Analyze commits and create version tag
  uplift:
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  # Step 2: Create release if new version was tagged
  release:
    needs: uplift
    if: ${{ needs.uplift.outputs.released == 'true' }}
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      release-tag: ${{ needs.uplift.outputs.version }}
      run-tests: true
      create-release: true
```

### Why This Approach?

1. **Avoids GITHUB_TOKEN limitation** - Tags created by `GITHUB_TOKEN` don't trigger other workflows, but chaining jobs in one workflow bypasses this
2. **Complete CI/CD pipeline** - commit -> tag -> release in one flow
3. **Simpler configuration** - No need to set up GitHub App tokens

### Using GitHub App for Separate Workflows

If you prefer separate workflows (one for tagging, one for releasing), configure uplift to use a GitHub App:

```yaml
jobs:
  uplift:
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main
    with:
      use-github-app: true
    secrets:
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

This allows created tags to trigger other workflows like `example-release-on-tag.yml`.

---

## Conventional Commits Reference

The uplift workflow uses [Conventional Commits](https://www.conventionalcommits.org/) to determine version bumps:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (0.X.0) | `feat: add user authentication` |
| `fix:` | Patch (0.0.X) | `fix: resolve login timeout` |
| `feat!:` or `BREAKING CHANGE:` | Major (X.0.0) | `feat!: redesign API endpoints` |
| `chore:`, `docs:`, `style:`, etc. | No bump | `docs: update README` |

---

## Full CI/CD Pipeline Example

Combine all workflows for a complete pipeline:

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:

jobs:
  # Run on all pushes and PRs
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

  # Only on main branch pushes
  version:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  release:
    needs: [lint, test, version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      release-tag: ${{ needs.version.outputs.version }}
      run-tests: false  # Already ran above
      build-type: docker
      create-release: true
```

---

## Go SDK/Library Release Pipeline

**File:** [`examples/example-go-sdk-release.yml`](examples/example-go-sdk-release.yml)

A complete CI/CD pipeline for Go SDK or library releases with linting, testing, auto-tagging, and multi-platform binary builds via GoReleaser.

### Pipeline Stages

```
┌─────────┐    ┌─────────┐    ┌─────────────┐    ┌─────────────┐
│  Lint   │───▶│  Test   │───▶│   Version   │───▶│   Release   │
│         │    │         │    │ (auto-tag)  │    │ (GoReleaser)│
└─────────┘    └─────────┘    └─────────────┘    └─────────────┘
     │              │               │                   │
     ▼              ▼               ▼                   ▼
 golangci-lint  go test +      Conventional        Multi-platform
                coverage       Commits → tag       binaries + GH Release
```

### Quick Start

```yaml
name: Go SDK Release
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      go: true

  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      framework: go
      coverage: true
      coverage-threshold: 70

  version:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  release:
    needs: [lint, test, version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/goreleaser.yml@main
    with:
      release-tag: ${{ needs.version.outputs.version }}
      go-version: 'stable'
```

### Requirements

1. **Go module** - `go.mod` in repository root
2. **GoReleaser config** - `.goreleaser.yml` in repository root
3. **Conventional Commits** - Use commit prefixes for auto-versioning

### Example `.goreleaser.yml`

```yaml
version: 2

before:
  hooks:
    - go mod tidy

builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - darwin
      - windows
    goarch:
      - amd64
      - arm64
    ldflags:
      - -s -w
      - -X main.version={{.Version}}
      - -X main.commit={{.Commit}}
      - -X main.date={{.Date}}

archives:
  - format: tar.gz
    name_template: >-
      {{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: 'checksums.txt'

changelog:
  sort: asc
  filters:
    exclude:
      - '^docs:'
      - '^chore:'
      - '^ci:'
```

### Workflow Behavior

| Event | Lint | Test | Version | Release |
|-------|------|------|---------|---------|
| Pull Request | :white_check_mark: | :white_check_mark: | :x: Skipped | :x: Skipped |
| Push to main (no version bump) | :white_check_mark: | :white_check_mark: | :white_check_mark: No tag | :x: Skipped |
| Push to main (feat/fix commit) | :white_check_mark: | :white_check_mark: | :white_check_mark: New tag | :white_check_mark: GoReleaser |

### Configuration Options

#### Lint Job

| Input | Default | Description |
|-------|---------|-------------|
| `go` | `false` | Enable Go linting |
| `go-version` | `stable` | Go version to use |
| `go-lint-version` | `latest` | golangci-lint version |
| `go-lint-args` | `''` | Additional golangci-lint arguments |

#### Test Job

| Input | Default | Description |
|-------|---------|-------------|
| `framework` | `auto` | Test framework (`go` for Go projects) |
| `go-version` | `stable` | Go version to use |
| `coverage` | `false` | Enable coverage reporting |
| `coverage-threshold` | `0` | Minimum coverage percentage |
| `test-command` | `''` | Custom test command |

#### Release Job (goreleaser.yml)

| Input | Default | Description |
|-------|---------|-------------|
| `release-tag` | `github.ref_name` | Tag name for the release |
| `go-version` | `stable` | Go version for builds |
| `goreleaser-version` | `latest` | GoReleaser version |
| `goreleaser-config` | `.goreleaser.yml` | Config file path |
| `goreleaser-args` | `''` | Additional GoReleaser args |
| `dry-run` | `false` | Skip publishing (test mode) |
| `snapshot` | `false` | Create snapshot build |

### Release Artifacts

GoReleaser automatically creates:
- Multi-platform binaries (linux/darwin/windows, amd64/arm64)
- Compressed archives (`.tar.gz`, `.zip` for Windows)
- Checksums file
- GitHub Release with changelog

---

## Docker + Helm Chart Release Pipeline

**File:** [`examples/example-docker-helm-release.yml`](examples/example-docker-helm-release.yml)

A complete CI/CD pipeline for containerized applications with Helm charts. Builds multi-arch Docker images and publishes Helm charts to OCI registries.

### Pipeline Stages

```
┌─────────┐    ┌─────────┐    ┌─────────────┐    ┌─────────┐    ┌─────────┐
│  Lint   │───▶│  Test   │───▶│   Version   │───▶│ Docker  │───▶│  Helm   │
│         │    │         │    │ (auto-tag)  │    │  Build  │    │ Publish │
└─────────┘    └─────────┘    └─────────────┘    └─────────┘    └─────────┘
     │              │               │                 │              │
     ▼              ▼               ▼                 ▼              ▼
 YAML + Helm    App tests      Conventional     Multi-arch      OCI registry
   linting                    Commits → tag    image push      chart push
```

### Quick Start

```yaml
name: Release
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      yaml: true
      helm: true
      helm-chart-path: 'charts/'

  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      framework: auto

  version:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  docker:
    needs: [lint, test, version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: ${{ github.repository }}
      platforms: 'linux/amd64,linux/arm64'

  helm:
    needs: [lint, test, version, docker]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/helm-publish.yml@main
    with:
      chart-name: myapp
      chart-path: 'charts/myapp'
```

### Requirements

1. **Dockerfile** - In repository root (or specify path)
2. **Helm chart** - In `charts/<chart-name>/` directory
3. **Conventional Commits** - Use commit prefixes for auto-versioning

### Workflow Behavior

| Event | Lint | Test | Version | Docker | Helm |
|-------|------|------|---------|--------|------|
| Pull Request | :white_check_mark: | :white_check_mark: | :x: Skipped | :x: Skipped | :x: Skipped |
| Push to main (no bump) | :white_check_mark: | :white_check_mark: | :white_check_mark: No tag | :x: Skipped | :x: Skipped |
| Push to main (feat/fix) | :white_check_mark: | :white_check_mark: | :white_check_mark: New tag | :white_check_mark: Push | :white_check_mark: Push |

### Configuration Options

#### Docker Job (docker-build.yml)

| Input | Default | Description |
|-------|---------|-------------|
| `image-name` | `github.repository` | Docker image name |
| `platforms` | `linux/amd64,linux/arm64` | Target platforms |
| `registry` | `ghcr.io` | Container registry |
| `push` | `true` | Push image to registry |
| `file` | `./Dockerfile` | Dockerfile path |
| `context` | `.` | Build context |

#### Helm Job (helm-publish.yml)

| Input | Default | Description |
|-------|---------|-------------|
| `chart-name` | *required* | Helm chart name |
| `chart-path` | `charts/<chart-name>` | Path to chart directory |
| `registry` | `ghcr.io` | OCI registry |
| `lint` | `true` | Run helm lint |
| `update-dependencies` | `true` | Run helm dependency update |

### Variant: Docker Only

For projects that only need container images (no Helm chart):

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      yaml: true

  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main

  version:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  docker:
    needs: [version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: ${{ github.repository }}
```

### Variant: Helm Only

For projects that only need Helm chart publishing (image built elsewhere):

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      helm: true
      helm-chart-path: 'charts/'

  version:
    needs: [lint]
    if: github.ref == 'refs/heads/main'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  helm:
    needs: [version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/helm-publish.yml@main
    with:
      chart-name: myapp
      chart-path: 'charts/myapp'
```

### Release Artifacts

| Artifact | Location |
|----------|----------|
| Docker Image | `ghcr.io/<owner>/<repo>:<version>` |
| Helm Chart | `oci://ghcr.io/<owner>/<chart-name>:<version>` |

### Installing the Helm Chart

```bash
# Pull the chart
helm pull oci://ghcr.io/myorg/myapp --version 1.0.0

# Install the chart
helm install my-release oci://ghcr.io/myorg/myapp --version 1.0.0

# Install with custom values
helm install my-release oci://ghcr.io/myorg/myapp --version 1.0.0 \
  --set image.tag=1.0.0 \
  --set replicaCount=3
```
