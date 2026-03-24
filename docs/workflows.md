# Workflow Reference

Detailed documentation for all reusable workflows in this repository.

## Table of Contents

- [Lint Workflow](#lint-workflow)
- [Test Workflow](#test-workflow)
- [Semantic Release Workflow](#semantic-release-workflow)
- [Docker Build Workflow](#docker-build-workflow)
- [Helm Publish Workflow](#helm-publish-workflow)
- [GoReleaser Workflow](#goreleaser-workflow)
- [Webhook Workflow](#webhook-workflow)
- [CI/CD Unified Workflow](#ci-cd-unified-workflow)
- [Release Gate Workflow](#release-gate-workflow)
- [Pipeline Summary Workflow](#pipeline-summary-workflow)

---

## Lint Workflow

Multi-language linting supporting Python (ruff), Go (golangci-lint), Shell (shellcheck), YAML (yamllint), JSON (jq), and Helm charts.

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

      json: true
      json-paths: '.'
      json-exclude: 'node_modules .git'

      helm: true
      helm-chart-path: 'charts/'

      fail-fast: true  # Stop on first failure
      upload-artifact: true  # Upload lint results as artifact
      artifact-name: 'lint-results'
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
| `json` | boolean | `false` | Enable JSON linting with jq |
| `json-paths` | string | `'.'` | Paths to check for JSON files (space-separated) |
| `json-exclude` | string | `'node_modules .git'` | Patterns to exclude (space-separated) |
| `working-directory` | string | `'.'` | Working directory for all commands |
| `fail-fast` | boolean | `true` | Stop on first linter failure |
| `upload-artifact` | boolean | `true` | Upload lint results as artifact |
| `artifact-name` | string | `'lint-results'` | Name for lint result artifacts |
| `artifact-retention-days` | number | `7` | Days to retain lint artifacts |

**Outputs:**

| Output | Description |
|--------|-------------|
| `python-status` | Python lint result: success, failure, or skipped |
| `go-status` | Go lint result: success, failure, or skipped |
| `shell-status` | Shell lint result: success, failure, or skipped |
| `yaml-status` | YAML lint result: success, failure, or skipped |
| `helm-status` | Helm lint result: success, failure, or skipped |
| `json-status` | JSON lint result: success, failure, or skipped |
| `overall-status` | Overall lint result: success or failure |

---

## Test Workflow

Configurable test runner with auto-detection for pytest, go test, npm test, and bun test. Generates rich GitHub Actions summaries with pass/fail counts, coverage, and duration.

**Usage:**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    uses: jacaudi/github-actions/.github/workflows/test.yml@main
    with:
      test-framework: 'auto'  # auto-detects: pytest, go, npm, bun
      coverage: true
      coverage-threshold: 80
      timeout-minutes: 30
      artifact-name: 'test-results'  # Uploads .test-results/, coverage/, htmlcov/
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

> **Node.js built-in test runner:** When using `test-framework: custom` with `node --test`, TAP output is automatically parsed and pass/fail/skipped counts are reflected in the job step summary.

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `test-command` | string | `''` | Custom test command (overrides framework) |
| `test-framework` | string | `'auto'` | Test framework: auto, pytest, go, npm, bun, custom |
| `python-version` | string | `'3.12'` | Python version for pytest |
| `go-version` | string | `'stable'` | Go version for go test |
| `node-version` | string | `'20'` | Node.js version for npm/bun |
| `coverage` | boolean | `false` | Enable code coverage collection |
| `coverage-threshold` | number | `0` | Minimum coverage percentage (0 to disable) |
| `test-args` | string | `''` | Additional test arguments |
| `test-packages` | string | `'./...'` | Package pattern to test for Go |
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

## Docker Build Workflow

Multi-architecture container image building with native runners for fast parallel builds. Supports linux/amd64 and linux/arm64 platforms. Automatically generates semantic version tags.

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

**Single Platform (AMD64 only):**

```yaml
jobs:
  docker:
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: 'myorg/myapp'
      platforms: 'linux/amd64'
      push: true
```

**Single Platform (ARM64 only):**

```yaml
jobs:
  docker:
    uses: jacaudi/github-actions/.github/workflows/docker-build.yml@main
    with:
      image-name: 'myorg/myapp'
      platforms: 'linux/arm64'
      push: true
```

> **Performance Note:** Multi-arch builds run on native runners in parallel, providing 3-5x faster builds compared to QEMU emulation.

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
| `amd64-runner` | string | `'ubuntu-24.04'` | Runner label for AMD64 builds |
| `arm64-runner` | string | `'ubuntu-24.04-arm'` | Runner label for ARM64 builds |
| `registry-username` | string | `''` | Registry username |

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

## Helm Publish Workflow

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

## Semantic Release Workflow

Automatic semantic versioning using [go-semantic-release](https://github.com/go-semantic-release/semantic-release) based on Conventional Commits. Creates version tags and GitHub releases automatically with native `feat!` support for breaking changes.

**Basic Usage:**

```yaml
name: Release
on:
  push:
    branches: [main]

jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
    with:
      use-github-app: true
      allow-initial-development-versions: true
    secrets:
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

**Dry Run Mode:**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
    with:
      dry-run: true
```

**Tag-Only Mode (no GitHub Release):**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
    with:
      create-release: false
      changelog-file: 'CHANGELOG.md'  # optional: still generates a changelog
      use-github-app: true
    secrets:
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

**With Hooks (e.g., GoReleaser):**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
    with:
      hooks: 'goreleaser'
      use-github-app: true
    secrets:
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `dry-run` | boolean | `false` | Run without creating tags/releases |
| `allow-initial-development-versions` | boolean | `true` | Allow versions < 1.0.0 |
| `changelog-file` | string | `''` | Path to changelog file (empty = no file) |
| `prerelease` | boolean | `false` | Mark release as prerelease |
| `create-release` | boolean | `true` | Create a GitHub Release in addition to the git tag. Set to `false` for tag-only mode — the workflow still creates the tag and changelog but skips the GitHub Release. |
| `hooks` | string | `''` | Hooks to run (e.g., goreleaser, npm-binary-releaser) |
| `config-file` | string | `''` | Path to .semrelrc config file |
| `validate-config` | boolean | `true` | Validate .semrelrc JSON syntax before release |
| `runs-on` | string | `'ubuntu-latest'` | Runner label |
| `use-github-app` | boolean | `false` | Use GitHub App authentication |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `app-id` | No | GitHub App ID (required if use-github-app is true) |
| `app-private-key` | No | GitHub App private key (required if use-github-app is true) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `new-release-published` | Whether a new release was published (true/false) |
| `new-release-version` | The new version (e.g., v1.2.3) |
| `new-release-major-version` | Major version number |
| `new-release-minor-version` | Minor version number |
| `new-release-patch-version` | Patch version number |
| `new-release-git-head` | Git commit SHA of the release |
| `new-release-git-tag` | Git tag created for the release |

**Required Permissions:**

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

**Conventional Commits:**

go-semantic-release uses [Conventional Commits](https://www.conventionalcommits.org/) to determine version bumps. **Version bumping behavior differs based on whether you're in initial development (0.x.x) or stable release (≥1.0.0):**

| Commit Type | Version Bump (0.x.x) | Version Bump (≥1.0.0) | Example |
|-------------|---------------------|----------------------|---------|
| `feat:` | Minor (0.X.0) | Minor (x.Y.0) | `feat: add user auth` |
| `fix:` | Patch (0.0.X) | Patch (x.y.Z) | `fix: resolve timeout` |
| `feat!:` | **Minor (0.X.0)** | **Major (X.0.0)** | `feat!: redesign API` |
| `fix!:` | **Minor (0.X.0)** | **Major (X.0.0)** | `fix!: breaking bugfix` |
| `chore:`, `docs:`, `ci:` | Patch (0.0.X) | Patch (x.y.Z) | `chore: update deps` |

**Key Points:**
- During 0.x.x (initial development), breaking changes (`feat!`, `fix!`) bump **minor**, not major (per [semver spec #4](https://semver.org/#spec-item-4))
- After ≥1.0.0 (stable), breaking changes bump **major** as expected
- The `!` suffix or `BREAKING CHANGE:` footer marks breaking changes
- Set `allow-initial-development-versions: false` to enforce versions ≥1.0.0

**Graduating to v1.0.0:**

When ready for stable release:

1. **Disable initial development mode:**
   ```yaml
   release:
     uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
     with:
       allow-initial-development-versions: false  # Enforces ≥1.0.0
   ```

2. **Or manually create v1.0.0:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

**Configuration (.semrelrc):**

Create a `.semrelrc` file in your repository root:

```json
{
  "branches": ["main"],
  "plugins": {
    "commit-analyzer": {
      "name": "default"
    },
    "ci-condition": {
      "name": "default"
    },
    "changelog-generator": {
      "name": "default",
      "options": {
        "emojis": "false"
      }
    },
    "provider": {
      "name": "github"
    }
  }
}
```

> **Note:** Using GITHUB_TOKEN will **not** trigger downstream workflows. To trigger other workflows when a release is created, set `use-github-app: true` and provide `app-id` and `app-private-key` secrets for a GitHub App.

> **Note:** For Go SDK releases with GoReleaser, use `semantic-release.yml` with `hooks: goreleaser` to automatically build and attach binaries to releases. See [example-go-sdk-release.yml](example-go-sdk-release.yml).

---

## Webhook Workflow

Trigger webhooks or GitHub workflows after releases. Common use case: trigger [Renovate](https://docs.renovatebot.com/) to update dependencies across repositories.

**Usage - HTTP Webhook:**

```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    # ... release job ...

  notify:
    needs: release
    uses: jacaudi/github-actions/.github/workflows/webhook.yml@main
    with:
      webhook-method: 'POST'
    secrets:
      webhook-url: ${{ secrets.RENOVATE_WEBHOOK_URL }}
      webhook-token: ${{ secrets.RENOVATE_WEBHOOK_TOKEN }}
```

**Usage - Trigger GitHub Workflow (Renovate):**

```yaml
jobs:
  notify:
    needs: release
    uses: jacaudi/github-actions/.github/workflows/webhook.yml@main
    with:
      trigger-workflow: true
      trigger-repo: 'myorg/renovate-config'
      trigger-workflow-id: 'renovate.yml'
      trigger-ref: 'main'
      release-tag: ${{ needs.release.outputs.release-tag }}
    secrets:
      github-token: ${{ secrets.RENOVATE_TRIGGER_TOKEN }}
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| **HTTP Webhook** |
| `webhook-url` | string | `''` | Webhook URL (prefer using secret) |
| `webhook-method` | string | `'POST'` | HTTP method: POST, GET, PUT |
| `webhook-payload` | string | `''` | Custom JSON payload |
| `webhook-headers` | string | `'{}'` | Additional headers as JSON |
| `webhook-content-type` | string | `'application/json'` | Content-Type header |
| **GitHub Workflow Trigger** |
| `trigger-workflow` | boolean | `false` | Enable workflow_dispatch trigger |
| `trigger-repo` | string | `''` | Target repository (owner/repo) |
| `trigger-workflow-id` | string | `''` | Workflow filename or ID |
| `trigger-ref` | string | `'main'` | Git ref for the trigger |
| `trigger-inputs` | string | `'{}'` | Workflow inputs as JSON |
| **Context** |
| `release-tag` | string | `''` | Release tag for context |
| `release-url` | string | `''` | Release URL for context |
| **Behavior** |
| `fail-on-error` | boolean | `false` | Fail if webhook fails |
| `retry-count` | number | `3` | Retry attempts |
| `retry-delay` | number | `5` | Seconds between retries |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `webhook-url` | No | Webhook URL (secret, preferred over input) |
| `webhook-token` | No | Bearer token for authentication |
| `github-token` | No | Token for workflow_dispatch (needs workflow scope) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `status` | Result: success, failure, skipped |
| `response-code` | HTTP response code |

> **Renovate Integration:** To trigger Renovate after releases, you can either call a self-hosted [Renovate server webhook](https://github.com/stack11/renovate-server) or trigger a workflow_dispatch on a repository running Renovate. See [Mend Renovate docs](https://docs.mend.io/wsk/renovate-ee-job-processing-in-renovate) for more options.

---

## Release Gate Workflow

Manual approval gate that pauses the pipeline and waits for a reviewer to approve via a GitHub Environment. Stage 5 of the building block pipeline — placed between scanning and release.

**Usage:**

```yaml
jobs:
  gate:
    uses: jacaudi/github-actions/.github/workflows/release-gate.yml@main
    with:
      environment: 'release-approval'
```

**Setup (once per repository):**

1. Go to **Settings → Environments** in your repository.
2. Click **New environment** and name it `release-approval` (or whatever you pass as `environment`).
3. Under **Environment protection rules**, add **Required reviewers**.

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `environment` | string | `'release-approval'` | GitHub environment name configured with required reviewers |
| `runs-on` | string | `'ubuntu-24.04'` | Runner label |

**Outputs:**

| Output | Description |
|--------|-------------|
| `status` | Gate result: `approved` or `failed` |

> **How it works:** The job targets the named GitHub Environment. GitHub blocks the job from starting until a required reviewer approves it in the Actions UI. If the reviewer rejects the deployment, the job — and any downstream jobs — fail. Emits a `pipeline-meta-release-gate` artifact (30-day retention).

---

## Pipeline Summary Workflow

Collector block that downloads all `pipeline-meta-*` artifacts and merges them into a single `pipeline-metadata` artifact. Always add this as the last job with `if: always()` so it runs even when upstream jobs fail.

**Usage:**

```yaml
jobs:
  # ... all other blocks ...

  pipeline-summary:
    needs: [code-scan, build, test, scan, gate, release]
    if: always()
    uses: jacaudi/github-actions/.github/workflows/pipeline-summary.yml@main
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `runs-on` | string | `'ubuntu-24.04'` | Runner label |

**Outputs:**

| Output | Description |
|--------|-------------|
| `status` | Artifact upload status: `passed` |

> **Artifact merging:** The workflow downloads all artifacts matching `pipeline-meta-*`. Blocks that did not run in the current pipeline are recorded as `{"status": "did-not-run"}` in the merged output. The final `pipeline-metadata.json` (uploaded as the `pipeline-metadata` artifact) has 90-day retention. See `docs/schemas/meta-pipeline.json` for the full schema.
