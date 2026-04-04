# Pipeline: Three-Stage (PR / CI / Release)

Splits the pipeline into three workflow files, each with a single responsibility. The CI workflow handles validation and versioning; the Release workflow handles artifact builds and publishing, triggered independently by the tag that CI creates.

Based on [jacaudi/nextdns-operator](https://github.com/jacaudi/nextdns-operator). Uses [Uplift](https://upliftci.dev/) for semantic versioning, file bumping, and changelog generation.

## End-to-End Flow

```
                          +------------------+
                          |  Developer       |
                          |  pushes branch   |
                          +--------+---------+
                                   |
                                   v
                          +------------------+
                          |  Pull Request    |
                          |  opened          |
                          +--------+---------+
                                   |
                 +-----------------+-----------------+
                 |                 |                 |
                 v                 v                 v
           +-----------+   +------------+   +-----------------+
           |   Lint    |   |    Test    |   |  Verify Helm    |
           | yamllint  |   | go test   |   | RBAC + CRD sync |
           | helm lint |   | coverage  |   |                 |
           | golangci  |   | threshold |   |                 |
           +-----+-----+   +-----+-----+   +--------+--------+
                 |                |                   |
                 +----------------+-------------------+
                                  |
                    +-------------+-------------+
                    v                           v
           +----------------+          +----------------+
           | Build (amd64)  |          | Build (arm64)  |
           | ubuntu-latest  |          | ubuntu-arm     |
           | no push        |          | no push        |
           +----------------+          +----------------+
                    |                           |
                    +-------------+-------------+
                                  |
                                  v
                          +------------------+
                          |  PR Checks Pass  |
                          |  Ready to merge  |
                          +--------+---------+
                                   |
                                   v
                          +------------------+
                          |  Merge to main   |
                          +--------+---------+
                                   |
                     +-------------+-------------+
                     v                           v
               +-----------+              +-----------+
               |   Lint    |              |   Test    |
               +-----------+              +-----------+
                     |                           |
                     +-------------+-------------+
                                   |
                                   v
                          +--------------------+
                          |  MANUAL APPROVAL   |
                          |                    |
                          |  "release" env     |
                          |  required reviewer |
                          |  clicks Approve    |
                          +--------+-----------+
                                   |
                                   v
                          +--------------------+
                          |      Uplift        |
                          |                    |
                          | 1. Bump files      |
                          |    Chart.yaml      |
                          |    version: 0.2.0  |
                          |    appVersion:     |
                          |      "v0.2.0"     |
                          |                    |
                          | 2. Changelog       |
                          |    CHANGELOG.md    |
                          |                    |
                          | 3. Commit + Tag    |
                          |    v0.2.0          |
                          +--------+-----------+
                                   |
                              tag pushed
                          (GitHub App token)
                                   |
                                   v
                          +--------------------+
                          |   release.yml      |
                          |   triggered        |
                          +--------+-----------+
                                   |
                     +-------------+-------------+
                     |                           |
                     v                           v
          +-------------------+       +-------------------+
          |  Docker Build     |       |  Helm Publish     |
          |                   |       |                   |
          | validate          |       | lint + dep update |
          |   |               |       | package chart     |
          | build (amd64)     |       | push to GHCR OCI  |
          | build (arm64)     |       |                   |
          |   |               |       | oci://ghcr.io/    |
          | merge manifest    |       |  <owner>/charts/  |
          |   |               |       |  nextdns-operator |
          | push to GHCR     |       +-------------------+
          |                   |
          | ghcr.io/<repo>:   |
          |   v0.2.0          |
          |   0.2             |
          |   0               |
          |   <sha>           |
          +-------------------+
```

## Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `pr.yml` | Pull request opened/updated | Fast validation feedback |
| `ci.yml` | Push to `main` | Lint, test, manual approval, uplift (bump + changelog + tag) |
| `release.yml` | Tag `v*` created | Build and publish artifacts |

```
PR opened -----> pr.yml (lint, test, verify, build)

Push to main --> ci.yml (lint, test)
                                |
                          MANUAL APPROVAL
                          reviewer approves
                                |
                         ci.yml (uplift)
                          bumps files + changelog
                          commits + tags v1.2.3
                                |
                                v
                        release.yml (container, helm)
```

The key difference from a two-stage pipeline: CI and Release are **decoupled**. After lint and test pass, the CI workflow **pauses for manual approval**. Once a reviewer approves, uplift bumps version numbers in tracked files, generates a changelog, commits everything, and creates a tag. The tag event triggers the release workflow automatically. This requires a **GitHub App token** -- tags created by `GITHUB_TOKEN` don't trigger other workflows.

### Version Bumping with Uplift

Uplift calculates the next semantic version from conventional commits, then patches configured files before committing and tagging. This ensures that version references in `Chart.yaml`, `CHANGELOG.md`, and any other tracked files are always in sync with the git tag.

Configuration lives in `.uplift.yml` at the repo root:

```yaml
# .uplift.yml
bumps:
  - file: chart/Chart.yaml
    regex:
      - pattern: "version: $VERSION"
        semver: true
        count: 1
      - pattern: 'appVersion: "v$VERSION"'
        semver: true
        count: 1
```

`$VERSION` is a built-in token that matches a semantic version with an optional `v` prefix. With `semver: true`, the replacement is bare semver (no `v`). The literal `v` before `$VERSION` in the `appVersion` pattern is preserved, so `appVersion: "v0.1.0"` becomes `appVersion: "v0.2.0"`.

The `count: 1` ensures only the first match in each pattern is replaced (important when a file has multiple version-like strings).

Uplift's release process runs three stages in order:
1. **Bump** -- patch all configured files with the next version
2. **Changelog** -- generate/update `CHANGELOG.md`
3. **Tag** -- commit all changes and create a `v`-prefixed git tag

---

## PR Validation (`pr.yml`)

Runs on every pull request to catch issues before merge.

```
+-----------------------------------------------------+
|                   PR Opened/Updated                 |
+---------------------------+-------------------------+
                            |
             +--------------+-----------------+
             v              v                 v
       +----------+  +------------+  +-----------------+
       |   Lint   |  |    Test    |  |  Verify Helm    |
       |          |  |            |  |  (RBAC + CRDs)  |
       +----+-----+  +-----+-----+  +--------+--------+
            |               |                 |
            +---------------+-----------------+
                            v
               +------------------------+
               |  Container Build (x2)  |
               |  amd64  .  arm64       |
               |  (no push, verify only)|
               +------------------------+
```

### Workflow

```yaml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
```

### Jobs

#### Lint

Three-phase job: a **setup** job builds a dynamic matrix from enabled linters, the **lint** job fans out and runs each linter in parallel, and a **summary** job collects all results, writes a step summary table to the Actions UI, and fails the workflow if any linter failed.

```yaml
setup:
  name: Setup
  runs-on: ubuntu-latest
  outputs:
    matrix: ${{ steps.set-matrix.outputs.matrix }}
    has-linters: ${{ steps.set-matrix.outputs.has-linters }}
  steps:
    - name: Build linter matrix
      id: set-matrix
      run: |
        # Build JSON array of enabled linters
        LINTERS="[]"
        # Each linter is toggled by a boolean input (yaml, helm, go, etc.)
        # Only enabled linters are added to the matrix
        LINTERS=$(echo "$LINTERS" | jq -c '. + ["yaml"]')
        LINTERS=$(echo "$LINTERS" | jq -c '. + ["helm"]')
        LINTERS=$(echo "$LINTERS" | jq -c '. + ["go"]')
        echo "matrix={\"linter\":$LINTERS}" >> $GITHUB_OUTPUT
        echo "has-linters=true" >> $GITHUB_OUTPUT

lint:
  name: Lint (${{ matrix.linter }})
  needs: setup
  if: needs.setup.outputs.has-linters == 'true'
  runs-on: ubuntu-latest
  strategy:
    fail-fast: false
    matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
  steps:
    - uses: actions/checkout@v6

    # Each linter runs conditionally based on matrix value
    # --- YAML ---
    - name: Install yamllint
      if: matrix.linter == 'yaml'
      run: pip install yamllint

    - name: Run yamllint
      id: yaml-lint
      if: matrix.linter == 'yaml'
      continue-on-error: true
      run: yamllint .

    # --- Helm ---
    - name: Set up Helm
      if: matrix.linter == 'helm'
      uses: azure/setup-helm@v4

    - name: Run Helm lint
      id: helm-lint
      if: matrix.linter == 'helm'
      continue-on-error: true
      run: helm lint chart

    # --- Go ---
    - name: Set up Go
      if: matrix.linter == 'go'
      uses: actions/setup-go@v6
      with:
        go-version: ${{ vars.GO_VERSION || 'stable' }}

    - name: Run golangci-lint
      id: go-lint
      if: matrix.linter == 'go'
      uses: golangci/golangci-lint-action@v9
      continue-on-error: true

    # Record status for the summary job
    - name: Set linter status
      id: run-linter
      if: always()
      run: |
        LINTER="${{ matrix.linter }}"
        case "$LINTER" in
          yaml) STATUS="${{ steps.yaml-lint.outcome }}" ;;
          helm) STATUS="${{ steps.helm-lint.outcome }}" ;;
          go)   STATUS="${{ steps.go-lint.outcome }}" ;;
        esac
        echo "status=${STATUS:-skipped}" >> $GITHUB_OUTPUT

summary:
  name: Lint Summary
  needs: [setup, lint]
  if: always()
  runs-on: ubuntu-latest
  outputs:
    overall-status: ${{ steps.collect.outputs.overall-status }}
  steps:
    - name: Collect Results
      id: collect
      run: |
        MATRIX='${{ needs.setup.outputs.matrix }}'
        LINT_RESULT='${{ needs.lint.result }}'

        # Default all linters to skipped
        echo "python-status=skipped" >> $GITHUB_OUTPUT
        echo "go-status=skipped" >> $GITHUB_OUTPUT
        echo "shell-status=skipped" >> $GITHUB_OUTPUT
        echo "yaml-status=skipped" >> $GITHUB_OUTPUT
        echo "helm-status=skipped" >> $GITHUB_OUTPUT
        echo "json-status=skipped" >> $GITHUB_OUTPUT

        # For each linter in the matrix, set status based on overall result
        if [[ "${{ needs.setup.outputs.has-linters }}" == "true" ]]; then
          for LINTER in python go shell yaml helm json; do
            if echo "$MATRIX" | jq -e ".linter | index(\"$LINTER\")" > /dev/null; then
              if [[ "$LINT_RESULT" == "success" ]]; then
                echo "${LINTER}-status=success" >> $GITHUB_OUTPUT
              else
                echo "${LINTER}-status=failure" >> $GITHUB_OUTPUT
              fi
            fi
          done
        fi

        if [[ "$LINT_RESULT" == "success" ]] || [[ "${{ needs.setup.outputs.has-linters }}" == "false" ]]; then
          echo "overall-status=success" >> $GITHUB_OUTPUT
        else
          echo "overall-status=failure" >> $GITHUB_OUTPUT
        fi

    - name: Generate Summary
      if: always()
      run: |
        echo "## Lint Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Linter | Status |" >> $GITHUB_STEP_SUMMARY
        echo "|--------|--------|" >> $GITHUB_STEP_SUMMARY

        # Map each linter's status to an icon row
        # success -> :white_check_mark: Passed
        # failure -> :x: Failed
        # skipped -> :fast_forward: Skipped
        case "${{ steps.collect.outputs.python-status }}" in
          success) echo "| :snake: Python (ruff) | :white_check_mark: Passed |" ;;
          failure) echo "| :snake: Python (ruff) | :x: Failed |" ;;
          *)       echo "| :snake: Python (ruff) | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        case "${{ steps.collect.outputs.go-status }}" in
          success) echo "| :blue_square: Go (golangci-lint) | :white_check_mark: Passed |" ;;
          failure) echo "| :blue_square: Go (golangci-lint) | :x: Failed |" ;;
          *)       echo "| :blue_square: Go (golangci-lint) | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        case "${{ steps.collect.outputs.shell-status }}" in
          success) echo "| :shell: Shell (shellcheck) | :white_check_mark: Passed |" ;;
          failure) echo "| :shell: Shell (shellcheck) | :x: Failed |" ;;
          *)       echo "| :shell: Shell (shellcheck) | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        case "${{ steps.collect.outputs.yaml-status }}" in
          success) echo "| :page_facing_up: YAML (yamllint) | :white_check_mark: Passed |" ;;
          failure) echo "| :page_facing_up: YAML (yamllint) | :x: Failed |" ;;
          *)       echo "| :page_facing_up: YAML (yamllint) | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        case "${{ steps.collect.outputs.helm-status }}" in
          success) echo "| :wheel_of_dharma: Helm | :white_check_mark: Passed |" ;;
          failure) echo "| :wheel_of_dharma: Helm | :x: Failed |" ;;
          *)       echo "| :wheel_of_dharma: Helm | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        case "${{ steps.collect.outputs.json-status }}" in
          success) echo "| :card_file_box: JSON (jq) | :white_check_mark: Passed |" ;;
          failure) echo "| :card_file_box: JSON (jq) | :x: Failed |" ;;
          *)       echo "| :card_file_box: JSON (jq) | :fast_forward: Skipped |" ;;
        esac >> $GITHUB_STEP_SUMMARY

        echo "" >> $GITHUB_STEP_SUMMARY
        if [[ "${{ steps.collect.outputs.overall-status }}" == "success" ]]; then
          echo "**Overall Status:** :white_check_mark: All checks passed" >> $GITHUB_STEP_SUMMARY
        else
          echo "**Overall Status:** :x: Some checks failed" >> $GITHUB_STEP_SUMMARY
        fi

    - name: Fail if linters failed
      if: steps.collect.outputs.overall-status == 'failure'
      run: exit 1
```

The lint summary renders in the **Actions run summary** tab as:

> **Lint Results**
>
> | Linter | Status |
> |--------|--------|
> | Python (ruff) | Skipped |
> | Go (golangci-lint) | Passed |
> | Shell (shellcheck) | Skipped |
> | YAML (yamllint) | Passed |
> | Helm | Passed |
> | JSON (jq) | Skipped |
>
> **Overall Status:** All checks passed

#### Test

Runs Go tests with coverage reporting. All settings are configurable via [GitHub Actions variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables) so each repository can tune behavior without editing the workflow.

| Variable | Default | Description |
|----------|---------|-------------|
| `GO_VERSION` | `stable` | Go toolchain version |
| `TEST_PACKAGES` | `./...` | Space-separated package patterns to test |
| `TEST_ARGS` | _(empty)_ | Extra flags passed to `go test` (e.g., `-short`, `-run TestFoo`) |
| `COVERAGE_ENABLED` | `true` | Collect coverage profile |
| `COVERAGE_THRESHOLD` | `0` | Minimum coverage % to pass (0 = no gate) |

Set these in **Settings > Secrets and variables > Actions > Variables** (repository or environment level).

```yaml
test:
  name: Test
  runs-on: ubuntu-latest
  env:
    GO_VERSION: ${{ vars.GO_VERSION || 'stable' }}
    TEST_PACKAGES: ${{ vars.TEST_PACKAGES || './...' }}
    TEST_ARGS: ${{ vars.TEST_ARGS || '' }}
    COVERAGE_ENABLED: ${{ vars.COVERAGE_ENABLED || 'true' }}
    COVERAGE_THRESHOLD: ${{ vars.COVERAGE_THRESHOLD || '0' }}
  steps:
    - uses: actions/checkout@v6

    - name: Set up Go
      uses: actions/setup-go@v6
      with:
        go-version: ${{ env.GO_VERSION }}

    - name: Install dependencies
      run: go mod download

    - name: Run tests
      run: |
        mkdir -p .test-results
        ARGS="-v"
        if [[ "${COVERAGE_ENABLED}" == "true" ]]; then
          ARGS="${ARGS} -coverprofile=coverage.out"
        fi
        set +e
        go test ${ARGS} ${TEST_ARGS} ${TEST_PACKAGES} 2>&1 | tee .test-results/output.txt
        EXIT_CODE=${PIPESTATUS[0]}
        echo "exit_code=${EXIT_CODE}" >> $GITHUB_OUTPUT
        exit ${EXIT_CODE}

    - name: Check coverage threshold
      if: env.COVERAGE_ENABLED == 'true' && env.COVERAGE_THRESHOLD != '0'
      run: |
        if [[ ! -f coverage.out ]]; then
          echo "::error::Coverage profile not found"
          exit 1
        fi
        COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
        echo "Coverage: ${COVERAGE}%"
        if (( $(echo "${COVERAGE} < ${COVERAGE_THRESHOLD}" | bc -l) )); then
          echo "::error::Coverage ${COVERAGE}% is below threshold ${COVERAGE_THRESHOLD}%"
          exit 1
        fi

    - name: Upload coverage report
      if: env.COVERAGE_ENABLED == 'true' && always()
      uses: actions/upload-artifact@v7
      with:
        name: coverage-report
        path: coverage.out
        if-no-files-found: ignore
        retention-days: 7

    - name: Generate Summary
      if: always()
      run: |
        echo "## Test Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY

        # Parse go test output for pass/fail counts
        PASSED=$(grep -c "^--- PASS" .test-results/output.txt 2>/dev/null) || PASSED=0
        FAILED=$(grep -c "^--- FAIL" .test-results/output.txt 2>/dev/null) || FAILED=0
        SKIPPED=$(grep -c "^--- SKIP" .test-results/output.txt 2>/dev/null) || SKIPPED=0
        TOTAL=$((PASSED + FAILED + SKIPPED))

        # Status badge
        if [[ "$FAILED" -gt 0 ]]; then
          echo "**Status:** :x: Failed" >> $GITHUB_STEP_SUMMARY
        else
          echo "**Status:** :white_check_mark: Passed" >> $GITHUB_STEP_SUMMARY
        fi
        echo "" >> $GITHUB_STEP_SUMMARY

        # Results table
        if [[ "$TOTAL" -gt 0 ]]; then
          echo "| Metric | Count |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| :white_check_mark: Passed | $PASSED |" >> $GITHUB_STEP_SUMMARY
          echo "| :x: Failed | $FAILED |" >> $GITHUB_STEP_SUMMARY
          if [[ "$SKIPPED" -gt 0 ]]; then
            echo "| :fast_forward: Skipped | $SKIPPED |" >> $GITHUB_STEP_SUMMARY
          fi
          echo "| **Total** | **$TOTAL** |" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          # Pass rate
          PASS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED / $TOTAL) * 100}")
          echo "**Pass Rate:** ${PASS_RATE}%" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
        fi

        # Coverage section
        if [[ -f coverage.out ]]; then
          COVERAGE=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | tr -d '%')
          echo "### Coverage" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Coverage:** ${COVERAGE}%" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          if [[ "${COVERAGE_THRESHOLD}" != "0" ]]; then
            COVERAGE_INT=${COVERAGE%.*}
            if [[ "$COVERAGE_INT" -ge "$COVERAGE_THRESHOLD" ]]; then
              echo ":white_check_mark: Coverage meets threshold of ${COVERAGE_THRESHOLD}%" >> $GITHUB_STEP_SUMMARY
            else
              echo ":warning: Coverage ${COVERAGE}% is below threshold ${COVERAGE_THRESHOLD}%" >> $GITHUB_STEP_SUMMARY
            fi
          fi
          echo "" >> $GITHUB_STEP_SUMMARY
        fi

        # Configuration table
        echo "### Configuration" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Setting | Value |" >> $GITHUB_STEP_SUMMARY
        echo "|---------|-------|" >> $GITHUB_STEP_SUMMARY
        echo "| Framework | go |" >> $GITHUB_STEP_SUMMARY
        echo "| Working Directory | . |" >> $GITHUB_STEP_SUMMARY
        echo "| Coverage Enabled | ${COVERAGE_ENABLED} |" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY

        # Collapsible test output
        if [[ -f .test-results/output.txt ]]; then
          echo "<details>" >> $GITHUB_STEP_SUMMARY
          echo "<summary>Test Output</summary>" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
          tail -100 .test-results/output.txt >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
          echo "</details>" >> $GITHUB_STEP_SUMMARY
        fi
```

The test summary renders in the **Actions run summary** tab as:

> **Test Results**
>
> **Status:** Passed
>
> | Metric | Count |
> |--------|-------|
> | Passed | 225 |
> | Failed | 0 |
> | **Total** | **225** |
>
> **Pass Rate:** 100.0%
>
> **Coverage**
>
> **Coverage:** 71.2%
>
> Coverage meets threshold of 70%
>
> **Configuration**
>
> | Setting | Value |
> |---------|-------|
> | Framework | go |
> | Working Directory | . |
> | Coverage Enabled | true |
>
> Test Output *(collapsible)*

**Example: nextdns-operator configuration**

| Variable | Value |
|----------|-------|
| `GO_VERSION` | `1.25` |
| `TEST_PACKAGES` | `./internal/controller/... ./internal/nextdns/... ./internal/coredns/...` |
| `COVERAGE_THRESHOLD` | `70` |

#### Verify Helm RBAC Sync

Regenerates RBAC from kubebuilder output and diffs against the committed Helm template. Fails if they diverge.

```yaml
verify-helm-rbac:
  name: Verify Helm RBAC Sync
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6

    - name: Install yq
      run: |
        sudo wget -qO /usr/local/bin/yq \
          https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
        sudo chmod +x /usr/local/bin/yq

    - name: Check RBAC sync
      run: |
        ./hack/generate-helm-rbac.sh

        if ! git diff --exit-code chart/templates/_values-rbac.tpl; then
          echo "::error::Helm RBAC template is out of sync with config/rbac/role.yaml"
          echo "Run 'task generate-helm-rbac' and commit the changes"
          exit 1
        fi
```

#### Verify Helm CRD Sync

Regenerates CRDs from Go types, syncs to Helm chart, diffs. Fails if out of sync.

```yaml
verify-helm-crds:
  name: Verify Helm CRD Sync
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6

    - name: Set up Go
      uses: actions/setup-go@v6
      with:
        go-version: ${{ vars.GO_VERSION || 'stable' }}

    - name: Install Task
      uses: go-task/setup-task@v1

    - name: Regenerate CRDs and check sync
      run: |
        task manifests
        task sync-helm-crds

        if ! git diff --exit-code chart/crds/; then
          echo "::error::Helm chart CRDs are out of sync with generated CRDs"
          echo "Run 'task sync-helm-crds' and commit the changes"
          exit 1
        fi
```

#### Container Build (amd64 + arm64)

Builds the Docker image on both architectures **without pushing**. Validates the Dockerfile compiles on each platform. Uses native runners with GHA build cache.

```yaml
container-amd64:
  name: Build Container (amd64)
  needs: [lint, test, verify-helm-rbac, verify-helm-crds]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v4

    - name: Build (amd64)
      uses: docker/build-push-action@v7
      with:
        context: .
        platforms: linux/amd64
        push: false
        load: true
        tags: nextdns-operator:pr-${{ github.event.pull_request.number }}-amd64
        cache-from: type=gha,scope=amd64
        cache-to: type=gha,mode=max,scope=amd64

container-arm64:
  name: Build Container (arm64)
  needs: [lint, test, verify-helm-rbac, verify-helm-crds]
  runs-on: ubuntu-24.04-arm
  steps:
    - uses: actions/checkout@v6

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v4

    - name: Build (arm64)
      uses: docker/build-push-action@v7
      with:
        context: .
        platforms: linux/arm64
        push: false
        load: true
        tags: nextdns-operator:pr-${{ github.event.pull_request.number }}-arm64
        cache-from: type=gha,scope=arm64
        cache-to: type=gha,mode=max,scope=arm64
```

---

## CI (`ci.yml`)

Runs on push to `main`. Validates the code, waits for manual approval, then bumps version files, generates changelog, and creates a semantic version tag.

```
+-----------------------------------------------------+
|                   Push to main                      |
+---------------------------+-------------------------+
                            |
                  +---------+---------+
                  v                   v
            +----------+       +----------+
            |   Lint   |       |   Test   |
            +----+-----+       +----+-----+
                 |                  |
                 +--------+---------+
                          v
               +---------------------+
               |  MANUAL APPROVAL    |
               |  "release" env      |
               +---------------------+
                          |
                          v
               +---------------------+
               |      Uplift         |
               |  bump Chart.yaml    |
               |  update CHANGELOG   |
               |  commit + tag       |
               +---------------------+
                          |
                     creates v* tag
                          |
                     triggers release.yml
```

### Workflow

```yaml
name: CI

on:
  push:
    branches: [main]

concurrency:
  group: ci
  cancel-in-progress: false

permissions:
  contents: write
```

Only one CI pipeline runs at a time. Subsequent pushes queue rather than cancel in-flight runs.

### Jobs

#### Lint

Same linters as the PR workflow (YAML, Helm, Go). See [PR Lint](#lint) above for step details.

#### Test

Same Go test + coverage as the PR workflow. See [PR Test](#test) above for step details.

#### Approve Release

Gate job that pauses the workflow for manual approval after lint and test pass. Uses a [GitHub Environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) named `release` with required reviewers. The workflow enters a **"Waiting for review"** state in the Actions UI until a designated reviewer clicks **"Approve"**.

```yaml
approve:
  name: Approve Release
  needs: [lint, test]
  runs-on: ubuntu-latest
  environment: release
  steps:
    - name: Release approved
      run: echo "Release approved, proceeding with uplift..."
```

##### Setting Up the Environment

1. Go to **Settings > Environments** in your repository
2. Create an environment named `release`
3. Enable **Required reviewers** and add the approvers
4. Optionally set a **Wait timer** (e.g., 5 minutes) for a cooldown period before approval is possible

#### Uplift Release

Runs after approval. Analyzes conventional commits since the last tag, bumps version numbers in configured files, generates a changelog, commits everything, and creates a git tag.

```yaml
release:
  name: Uplift Release
  needs: [approve]
  runs-on: ubuntu-latest
  permissions:
    contents: write
  steps:
    - name: Generate GitHub App Token
      id: app-token
      uses: actions/create-github-app-token@v2
      with:
        app-id: ${{ secrets.APP_ID }}
        private-key: ${{ secrets.APP_PRIVATE_KEY }}

    - name: Checkout
      uses: actions/checkout@v6
      with:
        fetch-depth: 0
        fetch-tags: true
        token: ${{ steps.app-token.outputs.token }}

    - name: Configure git for app token
      run: |
        git remote set-url origin \
          "https://x-access-token:${{ steps.app-token.outputs.token }}@github.com/${{ github.repository }}.git"

    - name: Validate git history
      run: |
        COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
        TAG_COUNT=$(git tag -l 'v*' | wc -l | tr -d ' ')
        echo "Commits: ${COMMIT_COUNT}, Tags: ${TAG_COUNT}"
        echo "Recent commits:"
        git log --oneline -10 || true
        echo "Latest tags:"
        git tag -l 'v*' --sort=-v:refname | head -5 || true

    - name: Run Uplift
      uses: gembaadvantage/uplift-action@v2
      with:
        args: release
      env:
        GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
```

Uplift does everything in a single `release` command:

1. **Bump** -- patches `chart/Chart.yaml` fields per `.uplift.yml`:
   - `version: 0.1.0` becomes `version: 0.2.0` (bare semver)
   - `appVersion: "v0.1.0"` becomes `appVersion: "v0.2.0"` (v-prefixed)
2. **Changelog** -- generates/updates `CHANGELOG.md` with commits since the last tag
3. **Tag** -- stages all changes, commits, creates `v0.2.0` tag, and pushes

Key details:
- `fetch-depth: 0` + `fetch-tags: true` ensures full history for accurate version calculation
- The checkout uses the app token so uplift's push (commit + tag) triggers `release.yml`
- The remote URL is reconfigured with the app token for the push
- Uplift handles staging, committing, and pushing automatically -- no manual `git add`/`commit`/`push` steps
- No separate changelog commit step -- uplift includes the changelog in the same commit as the version bumps
- If no qualifying conventional commits exist since the last tag, uplift exits cleanly with no changes

This workflow's only job beyond validation is to produce a version tag. It does **not** build or publish artifacts.

---

## Release (`release.yml`)

Triggered automatically by a `v*` tag. Because the manual approval already happened in ci.yml before uplift created the tag, this workflow runs without any gate. Uplift already bumped `chart/Chart.yaml` before tagging, so the checked-out code has the correct version values baked in.

```
+-----------------------------------------------------+
|                Tag v* created                       |
+---------------------------+-------------------------+
                            |
               +------------+------------+
               v                         v
    +-----------------+     +------------------+
    |  Docker Build   |     |  Helm Publish    |
    |  (multi-arch,   |     |  (OCI registry)  |
    |   push to GHCR) |     |                  |
    +-----------------+     +------------------+
```

### Workflow

```yaml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: read
  packages: write
```

### Jobs

#### Docker Build (Multi-arch)

Validates the platform inputs, builds each architecture natively on platform-specific runners, then merges the per-arch images into a single multi-arch manifest.

```yaml
validate:
  name: Validate Platforms
  runs-on: ubuntu-latest
  outputs:
    strategy: ${{ steps.parse.outputs.strategy }}
    matrix: ${{ steps.parse.outputs.matrix }}
  steps:
    - name: Parse platforms
      id: parse
      run: |
        # Validate platforms are linux/amd64, linux/arm64, or both
        # Determine single vs multi strategy
        # Build matrix with platform-specific runners:
        #   linux/amd64 -> ubuntu-24.04
        #   linux/arm64 -> ubuntu-24.04-arm
        echo 'matrix={"include":[
          {"platform":"linux/amd64","runner":"ubuntu-24.04"},
          {"platform":"linux/arm64","runner":"ubuntu-24.04-arm"}
        ]}' >> "$GITHUB_OUTPUT"
        echo "strategy=multi" >> "$GITHUB_OUTPUT"

build:
  name: Build (${{ matrix.platform }})
  needs: validate
  strategy:
    fail-fast: false
    matrix: ${{ fromJson(needs.validate.outputs.matrix) }}
  runs-on: ${{ matrix.runner }}
  permissions:
    contents: read
    packages: write
  steps:
    - uses: actions/checkout@v6

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v4

    - name: Log in to GHCR
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ github.token }}

    - name: Docker Metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ghcr.io/${{ github.repository }}
        tags: |
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=semver,pattern={{major}}
          type=sha,prefix=
        labels: |
          org.opencontainers.image.version=${{ github.ref_name }}

    - name: Build and push by digest
      id: build-multi
      uses: docker/build-push-action@v6
      with:
        context: .
        platforms: ${{ matrix.platform }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        provenance: true
        outputs: >-
          type=image,
          name=ghcr.io/${{ github.repository }},
          push-by-digest=true,
          name-canonical=true,
          push=true

    - name: Export digest
      run: |
        mkdir -p /tmp/digests
        ARCH="${{ matrix.platform }}"
        ARCH="${ARCH#linux/}"
        echo "${{ steps.build-multi.outputs.digest }}" > "/tmp/digests/${ARCH}"

    - name: Upload digest
      uses: actions/upload-artifact@v7
      with:
        name: digest-${{ matrix.platform == 'linux/amd64' && 'amd64' || 'arm64' }}
        path: /tmp/digests/*
        retention-days: 1

merge:
  name: Create Multi-arch Manifest
  needs: [validate, build]
  runs-on: ubuntu-latest
  permissions:
    contents: read
    packages: write
  steps:
    - name: Download digests
      uses: actions/download-artifact@v8
      with:
        path: /tmp/digests
        pattern: digest-*
        merge-multiple: true

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v4

    - name: Log in to GHCR
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ github.token }}

    - name: Docker Metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ghcr.io/${{ github.repository }}
        tags: |
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=semver,pattern={{major}}
          type=sha,prefix=

    - name: Create manifest list and push
      working-directory: /tmp/digests
      run: |
        IMAGE="ghcr.io/${{ github.repository }}"
        AMD64_DIGEST=$(cat amd64)
        ARM64_DIGEST=$(cat arm64)

        # Build tag arguments from metadata
        TAGARGS=""
        while IFS= read -r tag; do
          [[ -n "${tag}" ]] && TAGARGS="${TAGARGS} --tag ${tag}"
        done <<< "${{ steps.meta.outputs.tags }}"

        docker buildx imagetools create ${TAGARGS} \
          "${IMAGE}@${AMD64_DIGEST}" \
          "${IMAGE}@${ARM64_DIGEST}"

    - name: Inspect manifest
      id: inspect
      run: |
        TAG=$(echo "${{ steps.meta.outputs.tags }}" | head -1)
        DIGEST=$(docker buildx imagetools inspect "${TAG}" --format '{{json .Manifest.Digest}}' | tr -d '"')
        echo "digest=${DIGEST}" >> $GITHUB_OUTPUT
        echo "image-ref=ghcr.io/${{ github.repository }}@${DIGEST}" >> $GITHUB_OUTPUT

    - name: Generate Summary
      run: |
        echo "## Docker Build Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo ":white_check_mark: **Multi-arch Build Successful**" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### Build Details" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Property | Value |" >> $GITHUB_STEP_SUMMARY
        echo "|----------|-------|" >> $GITHUB_STEP_SUMMARY
        echo "| Registry | \`ghcr.io\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Image | \`${{ github.repository }}\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Platforms | \`linux/amd64, linux/arm64\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Build Type | Native runners (parallel) |" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Digest:** \`${{ steps.inspect.outputs.digest }}\`" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "**Version:** \`${{ steps.meta.outputs.version }}\`" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### Tags" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
        echo "${{ steps.meta.outputs.tags }}" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`" >> $GITHUB_STEP_SUMMARY

    - name: Write block metadata
      if: always()
      run: |
        STATUS="passed"
        if [[ "${{ job.status }}" != "success" ]]; then STATUS="failed"; fi
        jq -n \
          --arg block     "build-artifact" \
          --arg status    "${STATUS}" \
          --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
          --arg image_ref "${{ steps.inspect.outputs.image-ref }}" \
          --arg digest    "${{ steps.inspect.outputs.digest }}" \
          --arg version   "${{ steps.meta.outputs.version }}" \
          '{ block: $block, status: $status, timestamp: $timestamp,
             image_ref: $image_ref, digest: $digest, version: $version,
             platforms: ["linux/amd64", "linux/arm64"] }' > meta.json

    - name: Upload block metadata
      if: always()
      uses: actions/upload-artifact@v7
      with:
        name: pipeline-meta-build-artifact
        path: meta.json
        retention-days: 30
```

Key details:
- Each architecture builds **natively** on its own runner (no QEMU emulation)
- Per-arch images are pushed by digest (no tags yet), then the merge job creates the multi-arch manifest and applies all tags at once
- Tags are auto-generated by `docker/metadata-action`: semver (`1.2.3`, `1.2`, `1`) + commit SHA
- The `latest` tag can be added via custom tags input if desired

#### Helm Publish

Packages the Helm chart and pushes it to an OCI registry on GHCR. Because uplift already bumped `version` and `appVersion` in `chart/Chart.yaml`, the chart is published with the correct version without any runtime patching.

```yaml
helm:
  name: Publish Helm Chart
  runs-on: ubuntu-latest
  permissions:
    contents: read
    packages: write
  env:
    CHART_NAME: ${{ vars.HELM_CHART_NAME || github.event.repository.name }}
    CHART_PATH: ${{ vars.HELM_CHART_PATH || 'chart' }}
    CHART_REPOSITORY: ${{ vars.HELM_CHART_REPOSITORY || format('{0}/charts', github.repository_owner) }}
  steps:
    - uses: actions/checkout@v6

    - name: Validate chart exists
      run: |
        if [[ ! -f "${CHART_PATH}/Chart.yaml" ]]; then
          echo "::error::Chart.yaml not found at ${CHART_PATH}/Chart.yaml"
          exit 1
        fi

    - name: Extract version
      id: version
      run: |
        # Strip 'v' prefix from tag for Helm version (Helm uses bare semver)
        VERSION="${GITHUB_REF_NAME#v}"
        echo "version=${VERSION}" >> $GITHUB_OUTPUT

        # Verify Chart.yaml matches the tag (uplift should have bumped it)
        CHART_VERSION=$(grep '^version:' "${CHART_PATH}/Chart.yaml" | awk '{print $2}')
        if [[ "${CHART_VERSION}" != "${VERSION}" ]]; then
          echo "::warning::Chart.yaml version (${CHART_VERSION}) does not match tag (${VERSION})"
        fi

    - name: Determine app version
      id: app-version
      run: |
        # App version keeps the v prefix
        VERSION="${{ steps.version.outputs.version }}"
        APP_VERSION="v${VERSION}"
        echo "app-version=${APP_VERSION}" >> $GITHUB_OUTPUT

    - name: Helm Lint
      run: helm lint "${CHART_PATH}"

    - name: Update Dependencies
      run: helm dependency update "${CHART_PATH}"

    - name: Publish Helm Chart
      uses: appany/helm-oci-chart-releaser@v0.5.0
      with:
        name: ${{ env.CHART_NAME }}
        repository: ${{ env.CHART_REPOSITORY }}
        tag: ${{ steps.version.outputs.version }}
        app_version: ${{ steps.app-version.outputs.app-version }}
        path: ${{ env.CHART_PATH }}
        registry: ghcr.io
        registry_username: ${{ github.actor }}
        registry_password: ${{ github.token }}

    - name: Generate Summary
      if: always()
      run: |
        echo "## Helm Chart Publishing Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        if [[ "${{ job.status }}" == "success" ]]; then
          echo ":white_check_mark: **Publish Successful**" >> $GITHUB_STEP_SUMMARY
        else
          echo ":x: **Publish Failed**" >> $GITHUB_STEP_SUMMARY
        fi
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### Chart Details" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Property | Value |" >> $GITHUB_STEP_SUMMARY
        echo "|----------|-------|" >> $GITHUB_STEP_SUMMARY
        echo "| Chart Name | \`${CHART_NAME}\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Version | \`${{ steps.version.outputs.version }}\` |" >> $GITHUB_STEP_SUMMARY
        echo "| App Version | \`${{ steps.app-version.outputs.app-version }}\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Chart Path | \`${CHART_PATH}\` |" >> $GITHUB_STEP_SUMMARY
        echo "| Registry | \`ghcr.io\` |" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "### Usage" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "Pull the chart:" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`bash" >> $GITHUB_STEP_SUMMARY
        echo "helm pull oci://ghcr.io/${CHART_REPOSITORY}/${CHART_NAME} --version ${{ steps.version.outputs.version }}" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "Install the chart:" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`bash" >> $GITHUB_STEP_SUMMARY
        echo "helm install my-release oci://ghcr.io/${CHART_REPOSITORY}/${CHART_NAME} --version ${{ steps.version.outputs.version }}" >> $GITHUB_STEP_SUMMARY
        echo "\`\`\`" >> $GITHUB_STEP_SUMMARY

    - name: Write block metadata
      if: always()
      run: |
        STATUS="passed"
        if [[ "${{ job.status }}" != "success" ]]; then STATUS="failed"; fi
        CHART_REF="oci://ghcr.io/${CHART_REPOSITORY}/${CHART_NAME}:${{ steps.version.outputs.version }}"
        jq -n \
          --arg block         "helm-publish" \
          --arg status        "${STATUS}" \
          --arg timestamp     "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
          --arg chart_name    "${CHART_NAME}" \
          --arg chart_version "${{ steps.version.outputs.version }}" \
          --arg chart_ref     "${CHART_REF}" \
          '{ block: $block, status: $status, timestamp: $timestamp,
             chart_name: $chart_name, chart_version: $chart_version,
             chart_ref: $chart_ref }' > meta.json

    - name: Upload block metadata
      if: always()
      uses: actions/upload-artifact@v7
      with:
        name: pipeline-meta-helm-publish
        path: meta.json
        retention-days: 30
```

Helm publish settings are configurable via repository variables, with sensible defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `HELM_CHART_NAME` | Repository name | Chart name for OCI registry |
| `HELM_CHART_PATH` | `chart` | Path to chart directory |
| `HELM_CHART_REPOSITORY` | `<owner>/charts` | OCI repository path under the registry |

Key details:
- `chart/Chart.yaml` already has the correct `version` and `appVersion` from uplift's bump stage
- The extract step verifies the Chart.yaml version matches the tag as a safety check
- Helm versions use bare semver (`1.2.3`), not the `v`-prefixed tag (`v1.2.3`)
- `app-version` keeps the `v` prefix to match the container image tag
- Defaults to `oci://ghcr.io/<owner>/charts/<repo-name>` with no configuration needed

#### Pipeline Summary

Runs last, always. Downloads all `pipeline-meta-*` artifacts emitted by previous jobs (build, helm, release-gate) and merges them into a single `pipeline-metadata.json`. Writes a summary table to the Actions UI showing each block's status.

```yaml
pipeline-summary:
  name: Collect Pipeline Metadata
  needs: [validate, build, merge, helm]
  if: always()
  runs-on: ubuntu-latest
  steps:
    - name: Download all block metadata artifacts
      uses: actions/download-artifact@v8
      with:
        pattern: pipeline-meta-*
        merge-multiple: false
        path: ./meta-artifacts

    - name: Merge metadata
      run: |
        # Collects all pipeline-meta-*/meta.json files into one
        # pipeline-metadata.json with pipeline context (run ID, commit, ref)
        # Blocks not found are marked "did-not-run"

    - name: Upload pipeline metadata
      uses: actions/upload-artifact@v7
      with:
        name: pipeline-metadata
        path: pipeline-metadata.json
        retention-days: 90

    - name: Generate Summary
      if: always()
      run: |
        echo "## Pipeline Metadata" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        echo "| Block | Status |" >> $GITHUB_STEP_SUMMARY
        echo "|-------|--------|" >> $GITHUB_STEP_SUMMARY
        # Reads pipeline-metadata.json and maps each block's status:
        #   passed       -> :white_check_mark: passed
        #   approved     -> :white_check_mark: approved
        #   failed       -> :x: failed
        #   did-not-run  -> :white_medium_square: skipped
```

The pipeline metadata artifact is retained for 90 days and can be consumed by downstream automation (dashboards, notifications, audit trails).

---

## GitHub Actions UI

Every job writes to `$GITHUB_STEP_SUMMARY` so the **Actions run summary** tab shows a consolidated view of the entire pipeline without clicking into individual job logs.

### What Renders

| Job | Summary Content |
|-----|----------------|
| **Lint Summary** | Per-linter table (Passed/Failed/Skipped per language), overall status |
| **Test** | Pass/fail count table, pass rate, coverage % with threshold check, configuration table, collapsible test output |
| **Build (per-arch)** | Build record link for Docker Desktop import, build inputs (cache, labels, platforms) |
| **Create Multi-arch Manifest** | Registry, image, platforms, digest, version, tag list |
| **Publish Helm Chart** | Chart name/version/app-version, registry, `helm pull` and `helm install` commands |
| **Pipeline Summary** | Block status table (build-artifact, helm-publish, release-gate, etc.) |

### Block Metadata Artifacts

Each job emits a `pipeline-meta-<block>` artifact containing a `meta.json` with structured data about the job's outcome. The pipeline-summary job collects these into a single `pipeline-metadata.json`.

| Artifact | Emitted by | Key fields |
|----------|-----------|------------|
| `pipeline-meta-build-artifact` | Docker merge | image_ref, digest, version, platforms |
| `pipeline-meta-helm-publish` | Helm publish | chart_name, chart_version, chart_ref |
| `pipeline-meta-release-gate` | Approval gate | status, environment, actor |
| `pipeline-metadata` | Pipeline summary | All blocks merged, pipeline context |

---

## What Uplift Changes at Release Time

When uplift runs, it modifies these files in a single commit before tagging:

| File | Field | Before | After |
|------|-------|--------|-------|
| `chart/Chart.yaml` | `version` | `0.1.0` | `0.2.0` |
| `chart/Chart.yaml` | `appVersion` | `"v0.1.0"` | `"v0.2.0"` |
| `CHANGELOG.md` | (prepended) | -- | New release entry with commit list |

The release workflow then checks out the tagged commit, which already contains these updated values. No runtime version patching is needed in the release jobs.

### Adding More Files

To bump versions in additional files, add entries to `.uplift.yml`:

```yaml
bumps:
  # Helm chart
  - file: chart/Chart.yaml
    regex:
      - pattern: "version: $VERSION"
        semver: true
        count: 1
      - pattern: 'appVersion: "v$VERSION"'
        semver: true
        count: 1

  # Version constant in Go source
  - file: internal/version/version.go
    regex:
      - pattern: 'Version = "$VERSION"'
        semver: true
        count: 1

  # Multiple similar files via glob
  - file: "deploy/*/kustomization.yaml"
    regex:
      - pattern: "newTag: v$VERSION"
        semver: true
        count: 1

  # JSON files
  - file: package.json
    json:
      - path: "version"
        semver: true
```

---

## Permissions

| Scope | PR | CI | Release | Why |
|-------|:--:|:--:|:-------:|-----|
| `contents: read` | x | | x | Checkout code |
| `contents: write` | | x | | Uplift commit + tag push |
| `packages: write` | | | x | Push container images and Helm charts |
| `pull-requests: write` | x | | | PR status comments |

---

## Secrets

| Secret | Used by | Purpose |
|--------|---------|---------|
| `APP_ID` | CI | GitHub App ID for creating tokens that trigger release workflow |
| `APP_PRIVATE_KEY` | CI | GitHub App private key |

---

## Required Files

| File | Purpose |
|------|---------|
| `.uplift.yml` | Configures which files to bump and how (regex/JSON patterns) |
| `CHANGELOG.md` | Generated/updated by uplift with each release |
| `chart/Chart.yaml` | Helm chart metadata -- `version` and `appVersion` bumped by uplift |

---

## Actions and Tools Referenced

| Action / Tool | Used by | Purpose |
|---------------|---------|---------|
| `actions/checkout@v6` | All | Clone the repository |
| `actions/setup-go@v6` | PR, CI | Install Go toolchain |
| `actions/create-github-app-token@v2` | CI | Generate app token for uplift push |
| `gembaadvantage/uplift-action@v2` | CI | Bump files, changelog, tag, and push |
| `golangci/golangci-lint-action@v9` | PR, CI | Run golangci-lint |
| `azure/setup-helm@v4` | PR, CI | Install Helm CLI |
| `go-task/setup-task@v1` | PR | Install Task runner (CRD sync) |
| `docker/setup-buildx-action@v4` | Release | Enable Buildx for multi-arch builds |
| `docker/login-action@v3` | Release | Authenticate to GHCR |
| `docker/metadata-action@v5` | Release | Generate OCI tags + labels |
| `docker/build-push-action@v6` | Release | Build images and push by digest |
| `actions/upload-artifact@v7` | Release | Pass digests between build and merge jobs |
| `actions/download-artifact@v8` | Release | Retrieve digests in merge job |
| `appany/helm-oci-chart-releaser@v0.5.0` | Release | Package and push Helm chart to OCI registry |

---

## Conventional Commits Quick Reference

Version bumps are determined by commit prefixes:

| Commit | 0.x.x Bump | >=1.0.0 Bump |
|--------|-----------|-------------|
| `fix: ...` | Patch (0.0.X) | Patch (x.y.Z) |
| `feat: ...` | Minor (0.X.0) | Minor (x.Y.0) |
| `feat!: ...` | Minor (0.X.0) | **Major (X.0.0)** |
| `chore:`, `docs:`, etc. | No release | No release |
