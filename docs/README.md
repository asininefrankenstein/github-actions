# Component Reference

Detailed documentation for all reusable component workflows.

## Table of Contents

- [component-lint.yml](#component-lint)
- [component-test.yml](#component-test)
- [component-semantic-release.yml](#component-semantic-release)
- [component-container-build.yml](#component-container-build)
- [component-helm-publish.yml](#component-helm-publish)
- [component-pipeline-summary.yml](#component-pipeline-summary)

---

## component-lint

Multi-language linting with dynamic matrix execution. Builds a matrix of enabled linters, runs each in parallel on separate runners, then collects results into a summary table.

**Supported linters:** Python (ruff), Go (golangci-lint), Shell (shellcheck), YAML (yamllint), JSON (jq), Helm

**Usage:**

```yaml
jobs:
  lint:
    uses: jacaudi/github-actions/.github/workflows/component-lint.yml@main
    with:
      yaml: true
      go: true
      go-version: '1.25'
      helm: true
      helm-chart-path: 'chart'
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
| `json-paths` | string | `'.'` | Paths to check for JSON files |
| `json-exclude` | string | `'node_modules .git'` | Patterns to exclude |
| `working-directory` | string | `'.'` | Working directory for all commands |
| `fail-fast` | boolean | `true` | Stop on first linter failure |
| `upload-artifact` | boolean | `true` | Upload lint results as artifact |
| `artifact-name` | string | `'lint-results'` | Name for lint result artifacts |
| `artifact-retention-days` | number | `7` | Days to retain lint artifacts |

**Outputs:**

| Output | Description |
|--------|-------------|
| `python-status` | Python lint result: success, failure, or skipped |
| `go-status` | Go lint result |
| `shell-status` | Shell lint result |
| `yaml-status` | YAML lint result |
| `helm-status` | Helm lint result |
| `json-status` | JSON lint result |
| `overall-status` | Overall result: success or failure |

**Step Summary:** Per-linter table with Passed/Failed/Skipped status and overall result.

---

## component-test

Configurable test runner with auto-detection for Go, Python, Node.js, and Bun. Generates step summaries with pass/fail counts, coverage, pass rate, and collapsible test output.

**Usage:**

```yaml
jobs:
  test:
    uses: jacaudi/github-actions/.github/workflows/component-test.yml@main
    with:
      test-framework: 'go'
      go-version: '1.25'
      coverage: true
      coverage-threshold: 70
      test-packages: './internal/...'
```

**Custom test command:**

```yaml
jobs:
  verify:
    uses: jacaudi/github-actions/.github/workflows/component-test.yml@main
    with:
      test-framework: 'custom'
      setup-command: 'task generate'
      test-command: |
        if ! git diff --exit-code; then
          echo "::error::Generated files are out of sync"
          exit 1
        fi
      artifact-name: ''
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `test-command` | string | `''` | Custom test command (overrides framework) |
| `test-framework` | string | `'auto'` | Framework: auto, pytest, go, npm, bun, custom |
| `python-version` | string | `'3.12'` | Python version for pytest |
| `go-version` | string | `'stable'` | Go version for go test |
| `node-version` | string | `'20'` | Node.js version for npm/bun |
| `coverage` | boolean | `false` | Enable code coverage |
| `coverage-threshold` | number | `0` | Minimum coverage % (0 to disable) |
| `test-args` | string | `''` | Additional test arguments |
| `test-packages` | string | `'./...'` | Package pattern for Go |
| `working-directory` | string | `'.'` | Working directory |
| `install-dependencies` | boolean | `true` | Install dependencies before testing |
| `setup-command` | string | `''` | Commands to run before tests (from repo root) |
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

**Step Summary:** Status badge, pass/fail count table, pass rate, coverage with threshold check, configuration table, collapsible test output.

---

## component-semantic-release

Automatic semantic versioning using [semantic-release](https://github.com/semantic-release/semantic-release) (JS). Analyzes conventional commits, creates version tags and GitHub Releases, and generates a changelog file with proper header management (no duplicate headers).

Release behavior (changelog, prerelease, branches, commit message) is configured in `.releaserc.json` in the consuming repo -- not via workflow inputs. This keeps release config version-controlled alongside the code.

**Usage:**

```yaml
jobs:
  release:
    uses: jacaudi/github-actions/.github/workflows/component-semantic-release.yml@main
    permissions:
      contents: write
      issues: write
      pull-requests: write
    with:
      use-github-app: true
    secrets:
      app-id: ${{ secrets.APP_ID }}
      app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

**Example `.releaserc.json`:**

```json
{
  "branches": ["main"],
  "tagFormat": "v${version}",
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", {
      "changelogFile": "CHANGELOG.md",
      "changelogTitle": "# Changelog"
    }],
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md"],
      "message": "release: v${nextRelease.version} [skip ci]"
    }],
    "@semantic-release/github"
  ]
}
```

**Prerelease branches:**

```json
{
  "branches": [
    "main",
    { "name": "beta", "prerelease": true }
  ]
}
```

**Tag-only mode (no GitHub Release):** Remove `@semantic-release/github` from the plugins list.

**With extra plugins (e.g., exec hooks):**

```yaml
    with:
      use-github-app: true
      extra-plugins: '@semantic-release/changelog @semantic-release/git @semantic-release/exec'
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `dry-run` | boolean | `false` | Run without creating tags/releases |
| `semantic-release-version` | string | `'24'` | semantic-release npm package version |
| `extra-plugins` | string | `'@semantic-release/changelog @semantic-release/git'` | Additional plugins to install (space-separated) |
| `node-version` | string | `'lts/*'` | Node.js version |
| `use-github-app` | boolean | `false` | Use GitHub App authentication |
| `runs-on` | string | `'ubuntu-latest'` | Runner label |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `app-id` | No | GitHub App ID (required if use-github-app is true) |
| `app-private-key` | No | GitHub App private key |

**Outputs:**

| Output | Description |
|--------|-------------|
| `new-release-published` | Whether a new release was published (true/false) |
| `new-release-version` | Bare version (e.g., 1.2.3) -- use for Helm chart versions |
| `new-release-version-v` | v-prefixed version (e.g., v1.2.3) -- use for container/OCI tags |
| `new-release-major-version` | Major version number |
| `new-release-minor-version` | Minor version number |
| `new-release-patch-version` | Patch version number |
| `new-release-git-head` | Git commit SHA of the release |
| `new-release-git-tag` | Git tag created (e.g., v1.2.3) |

**Required Permissions:**

```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

**Required Files:** `.releaserc.json` in the repo root.

**Step Summary:** Version information table with major/minor/patch, release links, token type warning.

**Block Metadata:** `pipeline-meta-semantic-release` (30-day retention)

---

## component-container-build

Multi-architecture container image builds using native runners (no QEMU emulation). Builds each platform in parallel, then merges into a multi-arch manifest.

**Usage:**

```yaml
jobs:
  container:
    uses: jacaudi/github-actions/.github/workflows/component-container-build.yml@main
    permissions:
      contents: read
      packages: write
    with:
      image-name: ${{ github.repository }}
      platforms: 'linux/amd64,linux/arm64'
      version: ${{ github.ref_name }}
```

**Build without pushing (PR validation):**

```yaml
    with:
      image-name: ${{ github.repository }}
      push: false
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
| `version` | string | `''` | Version string for OCI labels |
| `labels` | string | `''` | Custom labels (KEY=VALUE per line) |
| `cache-from` | string | `'type=gha'` | Cache sources |
| `cache-to` | string | `'type=gha,mode=max'` | Cache destinations |
| `provenance` | boolean | `true` | Generate provenance attestation |
| `registry-username` | string | `''` | Registry username (defaults to github.actor) |
| `amd64-runner` | string | `'ubuntu-24.04'` | Runner for AMD64 builds |
| `arm64-runner` | string | `'ubuntu-24.04-arm'` | Runner for ARM64 builds |

**Secrets:**

| Secret | Required | Description |
|--------|----------|-------------|
| `registry-password` | No | Registry password (defaults to GITHUB_TOKEN) |

**Outputs:**

| Output | Description |
|--------|-------------|
| `digest` | Image digest |
| `image-ref` | Fully-qualified image reference (registry/name@sha256:...) |
| `tags` | Generated tags |
| `version` | Generated version |

**Required Permissions:**

```yaml
permissions:
  contents: read
  packages: write
```

**Step Summary:** Build details table (registry, image, platforms), digest, version, tag list.

**Block Metadata:** `pipeline-meta-build-artifact` (30-day retention)

---

## component-helm-publish

Publishes Helm charts to OCI registries. Lints, updates dependencies, publishes, and generates step summaries with install commands.

**Usage:**

```yaml
jobs:
  helm:
    uses: jacaudi/github-actions/.github/workflows/component-helm-publish.yml@main
    permissions:
      contents: read
      packages: write
    with:
      chart-name: 'my-app'
      chart-path: 'chart'
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `chart-name` | string | `''` | Chart name (defaults to repository name) |
| `chart-path` | string | `'chart'` | Path to chart directory |
| `registry` | string | `'ghcr.io'` | OCI registry |
| `registry-username` | string | `''` | Registry username (defaults to github.actor) |
| `repository` | string | `''` | Repository path (defaults to <owner>/charts) |
| `version` | string | `''` | Chart version (defaults to tag without v prefix) |
| `app-version` | string | `''` | App version (defaults to v-prefixed version) |
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
| `chart-app-version` | Published chart app version |
| `chart-ref` | Full OCI reference |

**Required Permissions:**

```yaml
permissions:
  contents: read
  packages: write
```

**Installing published charts:**

```bash
helm pull oci://ghcr.io/<owner>/charts/<chart-name> --version v1.0.0
helm install my-release oci://ghcr.io/<owner>/charts/<chart-name> --version v1.0.0
```

**Step Summary:** Chart details table, pull/install commands.

**Block Metadata:** `pipeline-meta-helm-publish` (30-day retention)

---

## component-pipeline-summary

Collector that downloads all `pipeline-meta-*` artifacts and merges them into a single `pipeline-metadata.json`. Always add as the last job with `if: always()`.

**Usage:**

```yaml
jobs:
  pipeline-summary:
    needs: [container, helm]
    if: always()
    uses: jacaudi/github-actions/.github/workflows/component-pipeline-summary.yml@main
```

**Inputs:**

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `runs-on` | string | `'ubuntu-24.04'` | Runner label |

**Outputs:**

| Output | Description |
|--------|-------------|
| `status` | Artifact upload status: `passed` |

Blocks that did not run are recorded as `{"status": "did-not-run"}` in the merged output. The `pipeline-metadata` artifact has 90-day retention.

**Step Summary:** Block status table with pass/fail/skipped icons.

---

## Block Metadata Convention

Every component emits a `pipeline-meta-<block>` artifact containing `meta.json`:

| Artifact | Emitted by | Key fields |
|----------|-----------|------------|
| `pipeline-meta-build-artifact` | container-build | image_ref, digest, version, platforms |
| `pipeline-meta-helm-publish` | helm-publish | chart_name, chart_version, chart_ref |
| `pipeline-meta-semantic-release` | semantic-release | version, git_tag, new_release_published |
| `pipeline-metadata` | pipeline-summary | All blocks merged, pipeline context |

Per-block artifacts: 30-day retention. Merged artifact: 90-day retention.

---

## GitHub App Token

Tags and releases created by `GITHUB_TOKEN` do not trigger downstream workflows. To trigger the release workflow from a tag created by semantic-release, use a GitHub App:

1. Create a [GitHub App](https://docs.github.com/en/apps/creating-github-apps) with `contents: write` permission
2. Install it on your repository
3. Add `APP_ID` and `APP_PRIVATE_KEY` as repository secrets
4. Set `use-github-app: true` in the semantic-release component call
