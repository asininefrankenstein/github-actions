# Example Workflows

This directory contains example workflows demonstrating how to use the reusable workflows in this repository. Copy and adapt these examples for your own projects.

## Available Examples

| Example | Description |
|---------|-------------|
| [example-caller.yml](examples/example-caller.yml) | Basic usage of lint and test workflows |
| [example-release-on-tag.yml](examples/example-release-on-tag.yml) | Trigger release pipeline on tag creation |
| [example-uplift-release.yml](examples/example-uplift-release.yml) | Chain uplift and release in one workflow |

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
