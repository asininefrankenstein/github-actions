# Workflow Templates

Copy and adapt these templates for your own projects. See [pipeline-three-stage-go.md](pipeline-three-stage-go.md) for the full design spec.

## Three-Stage Go Pipeline (PR / CI / Release)

| Template | Trigger | Description |
|----------|---------|-------------|
| [example-three-stage-pr.yml](example-three-stage-pr.yml) | Pull request | Lint, test, Helm verification, container build (no push) |
| [example-three-stage-ci.yml](example-three-stage-ci.yml) | Push to `main` | Lint, test, manual approval, uplift (bump + changelog + tag) |
| [example-three-stage-release.yml](example-three-stage-release.yml) | Tag `v*` | Multi-arch container build + push, Helm publish, pipeline summary |

## Key Concepts

### Conventional Commits

Uplift uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning.

| Commit Type | 0.x.x Bump | >=1.0.0 Bump | Example |
|-------------|-----------|-------------|---------|
| `feat:` | Minor (0.X.0) | Minor (x.Y.0) | `feat: add user auth` |
| `fix:` | Patch (0.0.X) | Patch (x.y.Z) | `fix: resolve timeout` |
| `feat!:` | Minor (0.X.0) | **Major (X.0.0)** | `feat!: redesign API` |
| `chore:`, `docs:`, etc. | No release | No release | `chore: update deps` |

### GitHub App Token

Tags created by `GITHUB_TOKEN` don't trigger other workflows. The CI workflow uses a GitHub App token so the tag uplift creates triggers the release workflow:

```yaml
release:
  steps:
    - uses: actions/create-github-app-token@v2
      with:
        app-id: ${{ secrets.APP_ID }}
        private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

### Required Secrets

| Secret | Description |
|--------|-------------|
| `APP_ID` | GitHub App ID |
| `APP_PRIVATE_KEY` | GitHub App private key |

### Configurable Variables

Set these in **Settings > Secrets and variables > Actions > Variables**:

| Variable | Default | Used by |
|----------|---------|---------|
| `GO_VERSION` | `stable` | PR, CI |
| `TEST_PACKAGES` | `./...` | PR, CI |
| `TEST_ARGS` | _(empty)_ | PR, CI |
| `COVERAGE_ENABLED` | `true` | PR, CI |
| `COVERAGE_THRESHOLD` | `0` | PR, CI |
| `HELM_CHART_NAME` | Repository name | Release |
| `HELM_CHART_PATH` | `chart` | Release |
| `HELM_CHART_REPOSITORY` | `<owner>/charts` | Release |

### Required Files

| File | Purpose |
|------|---------|
| `.uplift.yml` | Configures which files to bump and how |
| `CHANGELOG.md` | Generated/updated by uplift |
| `chart/Chart.yaml` | Helm chart metadata bumped by uplift |
