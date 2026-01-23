# Workflow Templates

Copy and adapt these templates for your own projects.

## Available Templates

| Template | Description |
|----------|-------------|
| [example-caller.yml](example-caller.yml) | Basic lint and test |
| [example-release-on-tag.yml](example-release-on-tag.yml) | Release when tag is pushed |
| [example-semantic-release.yml](example-semantic-release.yml) | Auto-version + release (recommended) |
| [example-go-sdk-release.yml](example-go-sdk-release.yml) | Go SDK: lint, test, GoReleaser |
| [example-docker-helm-release.yml](example-docker-helm-release.yml) | Docker + Helm + security scan |
| [example-self-release.yml](example-self-release.yml) | For workflow-only repos |

## Key Concepts

### Conventional Commits

go-semantic-release uses [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

| Prefix | Version Bump (≥1.0.0) | Example |
|--------|----------------------|---------|
| `feat:` | Minor (X.Y.0) | `feat: add user auth` |
| `fix:` | Patch (X.Y.Z) | `fix: resolve timeout` |
| `feat!:` | **Major (X.0.0)** | `feat!: redesign API` |
| `fix!:` | **Major (X.0.0)** | `fix!: breaking bugfix` |

**Note:** During initial development (0.x.x versions), `feat!` bumps minor not major (per semver spec).

### GitHub App Token

Releases created by `GITHUB_TOKEN` don't trigger other workflows. Use a GitHub App:

```yaml
release:
  uses: jacaudi/github-actions/.github/workflows/semantic-release.yml@main
  with:
    use-github-app: true
  secrets:
    app-id: ${{ secrets.APP_ID }}
    app-private-key: ${{ secrets.APP_PRIVATE_KEY }}
```

### Required Secrets

| Secret | Description |
|--------|-------------|
| `APP_ID` | GitHub App ID |
| `APP_PRIVATE_KEY` | GitHub App private key |
| `RENOVATE_TRIGGER_TOKEN` | Token with `workflow` scope (for webhook notifications) |
