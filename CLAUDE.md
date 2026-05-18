# GitHub Actions Repository

This repository provides reusable composite actions and workflows for CI/CD pipelines. All components are designed to be called from other repositories using GitHub's `uses:` syntax.

---

## Composite Actions

### Docker Build (Deprecated)

**Path:** `.github/actions/docker/action.yml`
**Status:** DEPRECATED - Use the `docker-build.yml` reusable workflow instead.

Builds multi-architecture Docker images using QEMU emulation, Docker Buildx, and GitHub Container Registry.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `registry` | No | `ghcr.io` | Container registry (e.g., ghcr.io, docker.io) |
| `image-name` | **Yes** | - | Image name (e.g., owner/repo or just repo name) |
| `platforms` | No | `linux/amd64,linux/arm64` | Target platforms for multi-arch builds (comma-separated) |
| `push` | No | `true` | Push image to registry after build |
| `context` | No | `.` | Build context path |
| `file` | No | `./Dockerfile` | Path to Dockerfile |
| `build-args` | No | `''` | Build arguments (newline-separated KEY=VALUE pairs) |
| `tags` | No | `''` | Custom tags (newline-separated, overrides auto-generated tags) |
| `labels` | No | `''` | Custom labels (newline-separated KEY=VALUE pairs) |
| `cache-from` | No | `type=gha` | Cache sources (e.g., type=gha, type=registry,ref=...) |
| `cache-to` | No | `type=gha,mode=max` | Cache destinations |
| `provenance` | No | `true` | Generate provenance attestation |

#### Outputs

| Output | Description |
|--------|-------------|
| `imageid` | Image ID |
| `digest` | Image digest |
| `metadata` | Build result metadata |
| `tags` | Generated tags |
| `labels` | Generated labels |
| `version` | Generated version |

---

### Test Summary

**Path:** `.github/actions/test-summary/action.yml`

Generates rich test summaries for GitHub Actions with support for multiple test frameworks. Can parse JUnit XML, pytest JSON, Go, npm, and generic formats, or accept manual test counts.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `title` | No | `Test Results` | Title for the test summary section |
| `results-file` | No | `''` | Path to test results file (JUnit XML, pytest JSON, or plain text) |
| `format` | No | `auto` | Test output format: `auto`, `junit`, `pytest-json`, `go`, `npm`, `generic` |
| `passed` | No | `''` | Number of passed tests (manual input) |
| `failed` | No | `''` | Number of failed tests (manual input) |
| `skipped` | No | `''` | Number of skipped tests (manual input) |
| `total` | No | `''` | Total number of tests (manual input) |
| `duration` | No | `''` | Test duration (manual input, e.g., "1m 23s") |
| `details` | No | `''` | Additional details to include (plain text or markdown) |
| `details-file` | No | `''` | Path to file containing additional details |
| `show-passed` | No | `false` | Show passed tests in details (may produce large output) |
| `max-details-lines` | No | `100` | Maximum lines to show in details section (0 for unlimited) |
| `badge` | No | `true` | Show status badge (pass/fail indicator) |

#### Outputs

| Output | Description |
|--------|-------------|
| `status` | Overall test status: `passed`, `failed`, or `unknown` |
| `passed-count` | Number of passed tests |
| `failed-count` | Number of failed tests |
| `total-count` | Total number of tests |

---

## Reusable Workflows

### Docker Build

**Path:** `.github/workflows/docker-build.yml`

Reusable workflow for multi-architecture Docker image builds. Handles registry login, tag generation (SHA, branch, semver), multi-platform builds via Docker Buildx, and provenance attestation. Uses per-platform runners for native builds.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `registry` | No | `ghcr.io` | Container registry |
| `image-name` | No | `''` | Image name (defaults to repository name) |
| `platforms` | No | `linux/amd64,linux/arm64` | Target platforms (comma-separated) |
| `push` | No | `true` | Push image to registry after build |
| `context` | No | `.` | Build context path |
| `file` | No | `./Dockerfile` | Path to Dockerfile |
| `build-args` | No | `''` | Build arguments (newline-separated KEY=VALUE) |
| `tags` | No | `''` | Custom tags (overrides auto-generated) |
| `version` | No | `''` | Version string for OCI labels (e.g., v0.1.4) |
| `labels` | No | `''` | Custom labels (newline-separated KEY=VALUE) |
| `cache-from` | No | `type=gha` | Cache sources |
| `cache-to` | No | `type=gha,mode=max` | Cache destinations |
| `provenance` | No | `true` | Generate provenance attestation |
| `registry-username` | No | `''` | Registry username (defaults to github.actor for ghcr.io) |
| `amd64-runner` | No | `ubuntu-24.04` | Runner label for AMD64 builds |
| `arm64-runner` | No | `ubuntu-24.04-arm` | Runner label for ARM64 builds |
| `sha-format` | No | `short` | SHA tag format: `short`, `long`, or `none` |
| `runs-on` | No | `ubuntu-24.04` | DEPRECATED: Use `amd64-runner` instead |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-password` | No | Registry password/token (defaults to GITHUB_TOKEN for ghcr.io) |

#### Outputs

| Output | Description |
|--------|-------------|
| `imageid` | Image ID |
| `digest` | Image digest |
| `metadata` | Build result metadata |
| `tags` | Generated tags |
| `labels` | Generated labels |
| `version` | Generated version |
| `image-ref` | Fully-qualified image reference pinned by digest (registry/name@sha256:...) |

---

### Helm Publish

**Path:** `.github/workflows/helm-publish.yml`

Publishes Helm charts to OCI registries. Handles dependency updates, linting, version injection, and OCI push.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `chart-name` | **Yes** | - | Name of the Helm chart to publish |
| `chart-path` | No | `''` | Path to the chart directory (defaults to `charts/<chart-name>`) |
| `registry` | No | `ghcr.io` | OCI registry to publish to |
| `registry-username` | No | `''` | Registry username (defaults to github.actor for ghcr.io) |
| `repository` | No | `''` | Repository owner (defaults to github.repository_owner) |
| `version` | No | `''` | Chart version (defaults to tag name with `v` prefix stripped) |
| `app-version` | No | `''` | App version for the chart |
| `update-dependencies` | No | `true` | Run `helm dependency update` before publishing |
| `lint` | No | `true` | Run `helm lint` before publishing |
| `runs-on` | No | `ubuntu-latest` | Runner label |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-password` | No | Registry password/token (defaults to GITHUB_TOKEN for ghcr.io) |

#### Outputs

| Output | Description |
|--------|-------------|
| `chart-name` | Published chart name |
| `chart-version` | Published chart version |
| `chart-app-version` | Published chart app version |
| `chart-ref` | Full OCI reference to the published chart |

---

### Image Validate

**Path:** `.github/workflows/image-validate.yml`

Validates container images by pulling them and running user-specified commands inside. Useful for post-build verification of image contents and behavior.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `image-ref` | **Yes** | - | Image reference to validate (e.g., ghcr.io/owner/repo@sha256:...) |
| `command` | **Yes** | - | Shell command(s) to execute inside the container |
| `shell` | No | `/bin/sh` | Shell to use as entrypoint (empty string uses image default) |
| `docker-args` | No | `''` | Additional `docker run` arguments (e.g., `--env FOO=bar`) |
| `runs-on` | No | `ubuntu-latest` | Runner label |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-username` | No | Registry username for private images |
| `registry-password` | No | Registry password for private images |

#### Outputs

| Output | Description |
|--------|-------------|
| `result` | Validation result: `passed` or `failed` |
| `output` | Captured stdout/stderr from validation command |

---

### Lint

**Path:** `.github/workflows/lint.yml`

Multi-language linting workflow supporting Python (ruff), Go (golangci-lint), Shell (shellcheck), YAML (yamllint), Helm (helm lint), and JSON (jq). Each linter is independently toggleable.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| **Python** | | | |
| `python` | No | `false` | Enable Python linting with ruff |
| `python-version` | No | `3.12` | Python version |
| `ruff-version` | No | `''` | Ruff version (empty for latest) |
| `ruff-args` | No | `.` | Arguments to pass to `ruff check` |
| **Go** | | | |
| `go` | No | `false` | Enable Go linting with golangci-lint |
| `go-version` | No | `stable` | Go version |
| `golangci-lint-version` | No | `latest` | golangci-lint version |
| `golangci-lint-args` | No | `''` | Arguments to pass to golangci-lint |
| **Shell** | | | |
| `shell` | No | `false` | Enable shell script linting with shellcheck |
| `shellcheck-version` | No | `stable` | ShellCheck version |
| `shellcheck-paths` | No | `.` | Paths to check (space-separated) |
| `shellcheck-args` | No | `''` | Arguments to pass to shellcheck |
| **YAML** | | | |
| `yaml` | No | `false` | Enable YAML linting with yamllint |
| `yamllint-config` | No | `''` | Path to yamllint config file |
| `yamllint-args` | No | `.` | Arguments to pass to yamllint |
| **Helm** | | | |
| `helm` | No | `false` | Enable Helm chart linting |
| `helm-chart-path` | No | `charts/` | Path to Helm chart(s) |
| `helm-args` | No | `''` | Arguments to pass to `helm lint` |
| **JSON** | | | |
| `json` | No | `false` | Enable JSON linting with jq |
| `json-paths` | No | `.` | Paths/globs to check (space-separated) |
| `json-exclude` | No | `node_modules .git` | Exclude patterns (space-separated) |
| **General** | | | |
| `working-directory` | No | `.` | Working directory for all lint commands |
| `fail-fast` | No | `true` | Stop on first linter failure |
| `upload-artifact` | No | `true` | Upload lint results as artifact |
| `artifact-name` | No | `lint-results` | Artifact name |
| `artifact-retention-days` | No | `7` | Days to retain artifacts |

#### Outputs

| Output | Description |
|--------|-------------|
| `python-status` | Python lint result: `success`, `failure`, or `skipped` |
| `go-status` | Go lint result: `success`, `failure`, or `skipped` |
| `shell-status` | Shell lint result: `success`, `failure`, or `skipped` |
| `yaml-status` | YAML lint result: `success`, `failure`, or `skipped` |
| `helm-status` | Helm lint result: `success`, `failure`, or `skipped` |
| `json-status` | JSON lint result: `success`, `failure`, or `skipped` |
| `overall-status` | Overall lint result: `success` or `failure` |

---

### Pipeline Summary

**Path:** `.github/workflows/pipeline-summary.yml`

Building block collector that always runs last in an E2E pipeline. Downloads all `pipeline-meta-*` artifacts and merges them into a single `pipeline-metadata.json` artifact.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `runs-on` | No | `ubuntu-24.04` | Runner label |

#### Outputs

| Output | Description |
|--------|-------------|
| `status` | pipeline-metadata artifact upload status |

---

### Release Gate

**Path:** `.github/workflows/release-gate.yml`

Manual approval gate that pauses the pipeline and waits for a reviewer to approve the deployment in a GitHub environment configured with required reviewers.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `environment` | No | `release-approval` | GitHub environment name configured with required reviewers |
| `runs-on` | No | `ubuntu-24.04` | Runner label |

#### Outputs

| Output | Description |
|--------|-------------|
| `status` | Gate result: `approved` or `failed` |

---

### Semantic Release

**Path:** `.github/workflows/semantic-release.yml`

Automatic semantic versioning using go-semantic-release. Analyzes commit history following Conventional Commits, creates version tags and GitHub releases. Supports `feat!` syntax for breaking changes, optional GitHub App authentication for triggering downstream workflows.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `dry-run` | No | `false` | Run in dry-run mode (no tags or releases created) |
| `allow-initial-development-versions` | No | `true` | Allow versions < 1.0.0 |
| `changelog-file` | No | `''` | Path to changelog file (empty = no file) |
| `prepend` | No | `true` | Prepend new entries to existing changelog |
| `prerelease` | No | `false` | Mark release as prerelease |
| `create-release` | No | `true` | Create a GitHub Release (false for tag-only) |
| `hooks` | No | `''` | Hooks to run (e.g., goreleaser, npm-binary-releaser, exec) |
| `config-file` | No | `''` | Path to .semrelrc config file |
| `validate-config` | No | `true` | Validate .semrelrc JSON syntax before release |
| `runs-on` | No | `ubuntu-latest` | Runner label |
| `use-github-app` | No | `false` | Use GitHub App authentication |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `app-id` | No | GitHub App ID (required if `use-github-app` is true) |
| `app-private-key` | No | GitHub App private key (required if `use-github-app` is true) |

#### Outputs

| Output | Description |
|--------|-------------|
| `new-release-published` | Whether a new release was published (`true`/`false`) |
| `new-release-version` | New version (e.g., v1.2.3) |
| `new-release-major-version` | Major version number |
| `new-release-minor-version` | Minor version number |
| `new-release-patch-version` | Patch version number |
| `new-release-git-head` | Git commit SHA of the release |
| `new-release-git-tag` | Git tag created for the release |

---

### Test

**Path:** `.github/workflows/test.yml`

Configurable test runner supporting Python (pytest), Go, Node.js (npm), and Bun with auto-detection. Handles dependency installation, test execution, coverage collection, and result summary generation.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `test-command` | No | `''` | Custom test command (overrides framework detection) |
| `test-framework` | No | `auto` | Framework: `auto`, `pytest`, `go`, `npm`, `bun`, `custom` |
| `python-version` | No | `3.12` | Python version for pytest |
| `go-version` | No | `stable` | Go version for go test |
| `node-version` | No | `20` | Node.js version for npm/bun |
| `coverage` | No | `false` | Enable code coverage |
| `coverage-threshold` | No | `0` | Minimum coverage percentage (0 to disable) |
| `test-args` | No | `''` | Additional test command arguments |
| `test-packages` | No | `./...` | Go package pattern |
| `working-directory` | No | `.` | Working directory |
| `install-dependencies` | No | `true` | Install dependencies before tests |
| `setup-command` | No | `''` | Command(s) after dependency install, before tests (runs from repo root) |
| `timeout-minutes` | No | `30` | Test timeout in minutes |
| `fail-on-error` | No | `true` | Fail workflow if tests fail |
| `artifact-name` | No | `test-results` | Artifact name (empty to skip upload) |
| `artifact-retention-days` | No | `7` | Days to retain artifacts |

#### Outputs

| Output | Description |
|--------|-------------|
| `status` | Test result: `passed`, `failed`, or `unknown` |
| `passed` | Number of passed tests |
| `failed` | Number of failed tests |
| `total` | Total number of tests |
| `coverage` | Coverage percentage (if enabled) |

---

### Webhook

**Path:** `.github/workflows/webhook.yml`

Triggers webhooks or GitHub workflows after releases. Supports HTTP webhooks (POST/GET/PUT) with custom headers and payloads, GitHub `workflow_dispatch` triggers, and retry logic.

#### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| **HTTP Webhook** | | | |
| `webhook-url` | No | `''` | Webhook URL (use secrets for sensitive URLs) |
| `webhook-method` | No | `POST` | HTTP method: `POST`, `GET`, `PUT` |
| `webhook-payload` | No | `''` | Custom JSON payload (default includes release context) |
| `webhook-headers` | No | `{}` | Additional headers as JSON object |
| `webhook-content-type` | No | `application/json` | Content-Type header |
| **Workflow Dispatch** | | | |
| `trigger-workflow` | No | `false` | Trigger a GitHub workflow via workflow_dispatch |
| `trigger-repo` | No | `''` | Target repository (owner/repo, defaults to current) |
| `trigger-workflow-id` | No | `''` | Workflow filename or ID (e.g., renovate.yml) |
| `trigger-ref` | No | `main` | Git ref for dispatch |
| `trigger-inputs` | No | `{}` | Workflow inputs as JSON object |
| **General** | | | |
| `release-tag` | No | `''` | Release tag for context |
| `release-url` | No | `''` | Release URL for context |
| `fail-on-error` | No | `false` | Fail workflow on webhook failure |
| `retry-count` | No | `3` | Number of retries |
| `retry-delay` | No | `5` | Delay between retries in seconds |
| `runs-on` | No | `ubuntu-latest` | Runner label |

#### Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `webhook-url` | No | Webhook URL (overrides input if provided) |
| `webhook-token` | No | Bearer token for webhook authentication |
| `github-token` | No | GitHub token for workflow_dispatch (needs `workflow` scope) |

#### Outputs

| Output | Description |
|--------|-------------|
| `status` | Webhook call status: `success`, `failure`, `skipped` |
| `response-code` | HTTP response code from webhook |

---

## Quick Reference

| Component | Path | Type | Purpose |
|-----------|------|------|---------|
| Docker Build (action) | `.github/actions/docker/` | Composite | Docker image builds (deprecated) |
| Test Summary | `.github/actions/test-summary/` | Composite | Test result summaries |
| Docker Build | `.github/workflows/docker-build.yml` | Workflow | Multi-arch Docker builds |
| Helm Publish | `.github/workflows/helm-publish.yml` | Workflow | Helm chart OCI publishing |
| Image Validate | `.github/workflows/image-validate.yml` | Workflow | Container image validation |
| Lint | `.github/workflows/lint.yml` | Workflow | Multi-language linting |
| Pipeline Summary | `.github/workflows/pipeline-summary.yml` | Workflow | Artifact collection |
| Release Gate | `.github/workflows/release-gate.yml` | Workflow | Manual approval gate |
| Semantic Release | `.github/workflows/semantic-release.yml` | Workflow | Automatic versioning & releases |
| Test | `.github/workflows/test.yml` | Workflow | Multi-framework test runner |
| Webhook | `.github/workflows/webhook.yml` | Workflow | Post-release webhook triggers |
