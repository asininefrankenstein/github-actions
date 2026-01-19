# Workflow Templates

Copy and adapt these templates for your own projects.

## Available Templates

| Template | Description |
|----------|-------------|
| [example-caller.yml](example-caller.yml) | Basic usage of lint and test workflows |
| [example-release-on-tag.yml](example-release-on-tag.yml) | Trigger release pipeline on tag creation |
| [example-uplift-release.yml](example-uplift-release.yml) | Chain uplift and release in one workflow |
| [example-go-sdk-release.yml](example-go-sdk-release.yml) | Complete Go SDK/library release pipeline |
| [example-docker-helm-release.yml](example-docker-helm-release.yml) | Docker + Helm chart release pipeline |
| [example-self-release.yml](example-self-release.yml) | Self-release for workflows repositories |

---

## Example: Basic Lint and Test

**File:** [`templates/example-caller.yml`](example-caller.yml)

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

**File:** [`templates/example-release-on-tag.yml`](example-release-on-tag.yml)

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

**File:** [`templates/example-uplift-release.yml`](example-uplift-release.yml)

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

**File:** [`templates/example-go-sdk-release.yml`](example-go-sdk-release.yml)

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

  # Optional: Trigger Renovate after release
  notify:
    needs: [version, release]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/webhook.yml@main
    with:
      trigger-workflow: true
      trigger-repo: myorg/renovate-config
      trigger-workflow-id: renovate.yml
    secrets:
      github-token: ${{ secrets.RENOVATE_TRIGGER_TOKEN }}
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

**File:** [`templates/example-docker-helm-release.yml`](example-docker-helm-release.yml)

A complete CI/CD pipeline for containerized applications with Helm charts. Builds multi-arch Docker images, scans for vulnerabilities, publishes Helm charts, and creates GitHub releases.

### Pipeline Stages

```
┌──────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────┐   ┌──────┐   ┌─────────┐   ┌────────┐
│ Lint │──▶│ Test │──▶│ Version │──▶│ Docker │──▶│ Scan │──▶│ Helm │──▶│ Release │──▶│ Notify │
└──────┘   └──────┘   └─────────┘   └────────┘   └──────┘   └──────┘   └─────────┘   └────────┘
    │          │           │             │           │          │           │            │
    ▼          ▼           ▼             ▼           ▼          ▼           ▼            ▼
 YAML +    App tests   auto-tag     Multi-arch   Trivy     OCI chart   GH Release   Renovate
  Helm                 (uplift)     image push   CVE scan    push      w/artifacts   webhook
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

  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main

  version:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  docker:
    needs: [version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: ${{ github.repository }}

  scan:
    needs: [version, docker]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/image-scan.yml@main
    with:
      image-ref: ghcr.io/${{ github.repository }}:${{ needs.version.outputs.version }}
      image-digest: ${{ needs.docker.outputs.digest }}
      severity: 'CRITICAL,HIGH'

  helm:
    needs: [version, scan]
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

| Event | Lint | Test | Version | Docker | Scan | Helm | Release | Notify |
|-------|------|------|---------|--------|------|------|---------|--------|
| Pull Request | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :x: | :x: | :x: |
| Push (no bump) | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | :x: | :x: | :x: |
| Push (feat/fix) | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :shield: | :white_check_mark: | :rocket: | :bell: |

### GitHub Release Content

The release job creates a GitHub Release containing:
- Container image reference with tag and digest
- Helm chart OCI reference
- Security scan summary (critical/high counts)
- Changelog from commits

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

---

## Self-Release Pipeline (Workflows Repository)

**File:** [`templates/example-self-release.yml`](example-self-release.yml)

A lightweight CI/CD pipeline for repositories that contain only reusable GitHub Actions workflows. This pattern is what this repository uses to release itself ("dogfooding").

### When to Use

This pattern is ideal for:
- Repositories containing only reusable workflows
- GitHub Actions libraries with no build artifacts
- Any repository that just needs versioning and changelog generation

### Pipeline Stages

```
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│  Lint   │───▶│   Version   │───▶│   Release   │
│  YAML   │    │ (auto-tag)  │    │ (changelog) │
└─────────┘    └─────────────┘    └─────────────┘
     │               │                   │
     ▼               ▼                   ▼
  yamllint      Conventional        GitHub Release
                Commits → tag       with changelog
```

### Quick Start

```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/lint.yml@main
    with:
      yaml: true

  version:
    needs: [lint]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: jacaudi/github-actions/.github/workflows/uplift.yml@main

  release:
    needs: [lint, version]
    if: needs.version.outputs.released == 'true'
    uses: jacaudi/github-actions/.github/workflows/release.yml@main
    with:
      build-type: none
      run-tests: false
      create-release: true
      release-tag: ${{ needs.version.outputs.version }}
```

### Workflow Behavior

| Event | Lint | Version | Release |
|-------|------|---------|---------|
| Pull Request | :white_check_mark: | :x: Skipped | :x: Skipped |
| Push to main (no version bump) | :white_check_mark: | :white_check_mark: No tag | :x: Skipped |
| Push to main (feat/fix commit) | :white_check_mark: | :white_check_mark: New tag | :rocket: GitHub Release |

### Key Configuration

| Input | Value | Description |
|-------|-------|-------------|
| `build-type` | `none` | No build artifacts needed |
| `run-tests` | `false` | No tests for workflow-only repos |
| `create-release` | `true` | Create GitHub Release |
| `release-notes-auto` | `true` | Generate changelog from commits |

### GitHub Release Content

The release includes:
- Automatically generated changelog from Conventional Commits
- Version tag reference for consumers

### Referencing Released Workflows

After a release, consumers can pin to specific versions:

```yaml
# Pin to specific version (recommended for stability)
uses: your-org/github-actions/.github/workflows/lint.yml@v1.2.0

# Pin to major version (gets minor/patch updates)
uses: your-org/github-actions/.github/workflows/lint.yml@v1

# Use latest (not recommended for production)
uses: your-org/github-actions/.github/workflows/lint.yml@main
```

### Optional: Notify Downstream

Add webhook notification to trigger Renovate or other tools after release:

```yaml
notify:
  needs: [version, release]
  if: needs.version.outputs.released == 'true'
  uses: jacaudi/github-actions/.github/workflows/webhook.yml@main
  with:
    trigger-workflow: true
    trigger-repo: ${{ github.repository_owner }}/renovate-config
    trigger-workflow-id: 'renovate.yml'
    release-tag: ${{ needs.version.outputs.version }}
  secrets:
    github-token: ${{ secrets.RENOVATE_TRIGGER_TOKEN }}
```
