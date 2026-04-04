# Changelog

## [v0.15.1](https://github.com/jacaudi/github-actions/releases/tag/v0.15.1) - 2026-04-04

### Bug Fixes

- [`943c121`](https://github.com/jacaudi/github-actions/commit/943c1216) fix: add changelog-file input to ci.yml semantic release job

## [v0.15.0](https://github.com/jacaudi/github-actions/releases/tag/v0.15.0) - 2026-04-04

### Breaking Changes

- [`6638b09`](https://github.com/jacaudi/github-actions/commit/6638b09b) replace uplift with go-semantic-release for versioning
- [`809f593`](https://github.com/jacaudi/github-actions/commit/809f5933) replace go-semantic-release with uplift, restructure as three-stage pipeline
  - All reusable workflow paths changed from `workflows/<name>.yml` to `workflows/component-<name>.yml`
  - Add pipeline design spec, component workflows, and example templates
  - Remove old workflows: docker-build, helm-publish, release-gate, image-validate, webhook, test scaffolds
  - Remove old example templates

### Bug Fixes

- [`b3ab80c`](https://github.com/jacaudi/github-actions/commit/b3ab80cc) fix: add missing permissions for semantic-release in ci workflows

### Documentation

- [`3a4ef75`](https://github.com/jacaudi/github-actions/commit/3a4ef752) docs: clean up changelog, remove orphaned entries from semrel migration

---

## [v0.14.2](https://github.com/jacaudi/github-actions/releases/tag/v0.14.2) - 2026-04-03

- [`0bbce65`](https://github.com/jacaudi/github-actions/commit/0bbce652b931091c9e89088f2efbdcdd45392301) fix: commit changelog file back to repo (#74)

## [v0.14.0](https://github.com/jacaudi/github-actions/releases/tag/v0.14.0) - 2026-03-12

- [`04251e3`](https://github.com/jacaudi/github-actions/commit/04251e3cad2213b800f86dca6829bd50d812b139) Merge pull request #67 from jacaudi/feat/semantic-release-tag-only
- [`1deb868`](https://github.com/jacaudi/github-actions/commit/1deb868ea6a8648a9e095cff3c6f9dd23aa3f041) docs: document create-release input in workflows.md
- [`b174df3`](https://github.com/jacaudi/github-actions/commit/b174df3ccf1bd36129fde2498885e72a64d265f5) fix: guard delete step against dry-run mode
- [`d6f8cc6`](https://github.com/jacaudi/github-actions/commit/d6f8cc6a8c493a158a5da687950cc11e04ad162d) docs: note tag-only mode in semantic-release workflow header
- [`5e5e033`](https://github.com/jacaudi/github-actions/commit/5e5e0334638b01b1d79e7d08f60d5b1f07d72321) fix: use consistent expression for tag-only mode summary row
- [`048ae75`](https://github.com/jacaudi/github-actions/commit/048ae750d0358e3480b9be02550ad0841abf64fc) feat: update summary for tag-only mode
- [`2f8e10f`](https://github.com/jacaudi/github-actions/commit/2f8e10fd010f78403ad40d834382dcd0cbd1e11c) feat: add create-release input for tag-only mode (closes #66)
- [`171e30d`](https://github.com/jacaudi/github-actions/commit/171e30d8583948fe8aceaab6a6ac9180607adee4) chore: track trivy-version input default via Renovate annotation
- [`e44a740`](https://github.com/jacaudi/github-actions/commit/e44a740535e542ed48001b3f2a6c61d38c7a09f2) chore(deps): update aquasec/trivy docker tag to v0.69.2 (#62)

## [v0.11.0](https://github.com/jacaudi/github-actions/releases/tag/v0.11.0) - 2026-02-26

- [`de87185`](https://github.com/jacaudi/github-actions/commit/de87185adde31397b499bf2be604b58f4fabf82e) feat(test): add setup-command input for pre-test setup steps (#56) (#58)

## [v0.10.0](https://github.com/jacaudi/github-actions/releases/tag/v0.10.0) - 2026-02-10

- [`b8a9276`](https://github.com/jacaudi/github-actions/commit/b8a9276abb0327f29113cf76103d88b31c75e1bc) feat(docker-build): add sha-format input for configurable SHA tags (#54)

## [v0.9.2](https://github.com/jacaudi/github-actions/releases/tag/v0.9.2) - 2026-02-10

- [`669592e`](https://github.com/jacaudi/github-actions/commit/669592e6eaf5bcadc3c19cc0166322eaec8c960e) fix(docker-build): reference build-single outputs directly in job outputs (#52)

## [v0.9.1](https://github.com/jacaudi/github-actions/releases/tag/v0.9.1) - 2026-02-10

- [`82f0ac0`](https://github.com/jacaudi/github-actions/commit/82f0ac0ce14717a910582e52b26de3b89d7d91fe) fix(docker-build): use heredoc for metadata output to prevent bash syntax error (#50)

## [v0.9.0](https://github.com/jacaudi/github-actions/releases/tag/v0.9.0) - 2026-02-10

- [`b4ed6aa`](https://github.com/jacaudi/github-actions/commit/b4ed6aa0cde7de2e056b28eb0c3f5f684b1bb43b) feat(docker-build): add image-ref output and image-validate workflow (#48)

## [v0.8.0](https://github.com/jacaudi/github-actions/releases/tag/v0.8.0) - 2026-02-01

- [`5b3aee9`](https://github.com/jacaudi/github-actions/commit/5b3aee95638a25aad49882417f18d1c771488768) feat(lint): Add summary job to aggregate parallel linter results
- [`cf5ac04`](https://github.com/jacaudi/github-actions/commit/cf5ac04bacd4357e038a63c9a6d41316914ea274) feat(lint): Replace sequential linting with parallel matrix jobs
- [`6572ca1`](https://github.com/jacaudi/github-actions/commit/6572ca17e47d3681205b5a4305fdfe16aef1d36b) feat(lint): Add setup job for dynamic linter matrix
- [`370db7c`](https://github.com/jacaudi/github-actions/commit/370db7c94a904052f9a8f9d4d7fb8d2af0aed6b3) chore(deps): migrate to shared renovate config (#41)

## [v0.7.0](https://github.com/jacaudi/github-actions/releases/tag/v0.7.0) - 2026-01-30

- [`0c3ebc3`](https://github.com/jacaudi/github-actions/commit/0c3ebc30272ead5350432e1a8fed42a65dec9761) fix(helm-publish): Prevent double v prefix in appVersion
- [`b2fbd5d`](https://github.com/jacaudi/github-actions/commit/b2fbd5d6e2872926ebe77c48781a18688a12b639) feat(docker): Add version input to override OCI version label

## [v0.6.0](https://github.com/jacaudi/github-actions/releases/tag/v0.6.0) - 2026-01-30

- [`faf40a5`](https://github.com/jacaudi/github-actions/commit/faf40a55057eb07a65eb23a8408c241696b4124d) feat(helm-publish): Add app-version input to set Chart appVersion

## [v0.5.3](https://github.com/jacaudi/github-actions/releases/tag/v0.5.3) - 2026-01-30

- [`bdd5b2f`](https://github.com/jacaudi/github-actions/commit/bdd5b2f20c3306cedc88e7160a9126c862535988) fix(deps): update actions/upload-artifact action to v6
- [`93d7630`](https://github.com/jacaudi/github-actions/commit/93d763017a66e8764be7851ee4ffed9368900134) fix(deps): update actions/download-artifact action to v7

## [v0.5.2](https://github.com/jacaudi/github-actions/releases/tag/v0.5.2) - 2026-01-29

- [`e1edddf`](https://github.com/jacaudi/github-actions/commit/e1edddf00b0f22f8a11ac8a99bcd4db5c09eabac) fix(docker): Return correct tags in job outputs
- [`cb273ff`](https://github.com/jacaudi/github-actions/commit/cb273ff70b05d022a238e8a1052673c0d333d8c7) fix(docker): Respect custom tags in multi-arch merge job

## [v0.5.1](https://github.com/jacaudi/github-actions/releases/tag/v0.5.1) - 2026-01-28

- [`86bd05a`](https://github.com/jacaudi/github-actions/commit/86bd05a8c3f19346ecac4714ff4e43f39d609408) fix(ci): Fix self-reference in deprecated pattern check
- [`cee0135`](https://github.com/jacaudi/github-actions/commit/cee013510ed2457a0505c4b319bc3552b331db99) style: Remove emojis from workflow log messages
- [`a187c66`](https://github.com/jacaudi/github-actions/commit/a187c66abeb7c863648c93b38a9c188f22750a9d) fix(ci): Handle multiple matches in GITHUB_OUTPUT validation
- [`cdf8981`](https://github.com/jacaudi/github-actions/commit/cdf89812c5d35990a35b8a00d85a958d50b1a75f) ci: Add workflow validation to catch GITHUB_OUTPUT issues
- [`c81d223`](https://github.com/jacaudi/github-actions/commit/c81d223c7c21de27284da7b8ea86a14d94bac43f) fix(docker): Compact metadata JSON to fix GITHUB_OUTPUT parsing

## [v0.5.0](https://github.com/jacaudi/github-actions/releases/tag/v0.5.0) - 2026-01-28

- [`d02f7a6`](https://github.com/jacaudi/github-actions/commit/d02f7a6f1ab164a951a46ab94145b52614f718b2) docs: Document GHCR auto-authentication for image scanning
- [`1a66b93`](https://github.com/jacaudi/github-actions/commit/1a66b936c7796c3e022898a4c00ead2600f2918a) fix(image-scan): Add packages:read permission for GHCR access
- [`1d6ac72`](https://github.com/jacaudi/github-actions/commit/1d6ac7212caf49dd72caa057f7692efb4b8d0ab4) fix(image-scan): Auto-authenticate for private GHCR images
- [`8346eaf`](https://github.com/jacaudi/github-actions/commit/8346eafc3f0380a90518ead386c1c21ae07593c6) docs: Update Docker workflow documentation for native builds
- [`8591505`](https://github.com/jacaudi/github-actions/commit/8591505a5ddc1d197f44f5c6314158771f057199) chore(docker): Mark composite action as deprecated
- [`d39f913`](https://github.com/jacaudi/github-actions/commit/d39f913895f123d9ff4ce5c426b6683c0406bef0) feat(docker): Add manifest merge job for multi-platform builds
- [`5fc3ab4`](https://github.com/jacaudi/github-actions/commit/5fc3ab4092132eb4f93bcb2a0cd81d45c18b50e9) feat(docker): Replace build job with native matrix build
- [`2150277`](https://github.com/jacaudi/github-actions/commit/21502779a43ee26100cf36473115a145a1547e97) feat(docker): Add platform validation job
- [`63c5ea9`](https://github.com/jacaudi/github-actions/commit/63c5ea91298b3f7dc87571ccf3518a3049df21c7) feat(docker): Replace runs-on with platform-specific runner inputs

## [v0.4.5](https://github.com/jacaudi/github-actions/releases/tag/v0.4.5) - 2026-01-28

- [`2bb0189`](https://github.com/jacaudi/github-actions/commit/2bb0189e77b2a9e3865dade8657894e01eff9e98) fix: Resolve issues #22, #23, #24 (#25)
- [`6bb8050`](https://github.com/jacaudi/github-actions/commit/6bb8050fa324077aafe02ed2ddc33fdf5c6eb6d4) docs: Update workflow documentation with artifact inputs

## [v0.1.5](https://github.com/jacaudi/github-actions/releases/tag/v0.1.5) - 2026-01-22

- [`93edcea`](https://github.com/jacaudi/github-actions/commit/93edcea078785babd2e6a2bf462a3c4ba4a6cc11) fix(ci): Rename Summary job to Pipeline Report

## [v0.1.4](https://github.com/jacaudi/github-actions/releases/tag/v0.1.4) - 2026-01-22

- [`32df7c3`](https://github.com/jacaudi/github-actions/commit/32df7c30a2d2bbdcb14a6a79b4f4b77767d20073) fix(release): Use correct JSON field name for release URL

## [v0.1.3](https://github.com/jacaudi/github-actions/releases/tag/v0.1.3) - 2026-01-22

- [`da69b04`](https://github.com/jacaudi/github-actions/commit/da69b0427e48b04f6e3eb42652e77e9021898d6b) fix: Configure Renovate to use fix(deps) for version bumps
- [`b1dbc6c`](https://github.com/jacaudi/github-actions/commit/b1dbc6c5c6fdfb5d4d25e8b05727b47771bf92dc) chore: Include chore commits in version bumps and changelog
- [`82c9dde`](https://github.com/jacaudi/github-actions/commit/82c9dde379083a47ba26d1334047c380fdf44539) chore(deps): update dependency python to 3.14 (#3)
- [`788eb6e`](https://github.com/jacaudi/github-actions/commit/788eb6e4cdd6c471ef0c79a06d0ba628fb005f16) chore(deps): update actions/create-github-app-token action to v2 (#5)
- [`729033f`](https://github.com/jacaudi/github-actions/commit/729033f9682b4e55b450f3ee8528ea041dbb6001) chore(deps): update actions/setup-go action to v6 (#6)
- [`0c3f8d5`](https://github.com/jacaudi/github-actions/commit/0c3f8d57ced36fe587e8b5e892b23528c76a9db3) chore(deps): update actions/setup-node action to v6 (#7)
- [`16b47e7`](https://github.com/jacaudi/github-actions/commit/16b47e79bd21d4b65b7f60f2bc7f963de4fae99b) chore(deps): update actions/setup-python action to v6 (#8)
- [`98e80eb`](https://github.com/jacaudi/github-actions/commit/98e80ebe0337657901ed41952bf9b400856b9eae) chore(deps): update actions/upload-artifact action to v6 (#9)
- [`1465afd`](https://github.com/jacaudi/github-actions/commit/1465afdd565b060b0bf6381e9700053973edf0cc) chore(deps): update aquasecurity/trivy-action action to v0.33.1 (#13)
- [`6a9b491`](https://github.com/jacaudi/github-actions/commit/6a9b4916d598c8146a39d878dc167f8fbfcc6032) chore(deps): update github/codeql-action action to v4 (#14)
- [`41ba7e5`](https://github.com/jacaudi/github-actions/commit/41ba7e55f3336b7e65881e58669e05bc93ae924b) chore(deps): update golangci/golangci-lint-action action to v9 (#11)
- [`a46facd`](https://github.com/jacaudi/github-actions/commit/a46facd3e858f569623e9ee7dc61b3bbe281dc9d) chore(deps): update dependency node to v24 (#10)

## [v0.1.2](https://github.com/jacaudi/github-actions/releases/tag/v0.1.2) - 2026-01-21

- [`c36ce3c`](https://github.com/jacaudi/github-actions/commit/c36ce3c621bcb1aa6bc7ff98d565fdad927bbd58) fix: Resolve syntax errors in image-scan.yml workflow

## [v0.1.1](https://github.com/jacaudi/github-actions/releases/tag/v0.1.1) - 2026-01-21

- [`272cdd1`](https://github.com/jacaudi/github-actions/commit/272cdd1197083b9c21d0761371f778b6ac644534) fix: Properly detect version creation in uplift workflow

## [v0.1.0](https://github.com/jacaudi/github-actions/releases/tag/v0.1.0) - 2026-01-21

- [`fab2b76`](https://github.com/jacaudi/github-actions/commit/fab2b766506787c7b7dd77f84dd7448f1dfa39a2) fix: Add yamllint config and resolve linting issues
- [`6361810`](https://github.com/jacaudi/github-actions/commit/63618102feef2e8ed8dae1f75eb447a201d36cc4) fix: Add packages write permission to CI/CD workflow
- [`ed8ddb3`](https://github.com/jacaudi/github-actions/commit/ed8ddb3d610ae2f9abeb726580d337b87c7ce234) Merge branch 'claude/review-release-workflow-idq4m'
- [`c2059a1`](https://github.com/jacaudi/github-actions/commit/c2059a135b264f058e88de2dc2d6916ca95eebd8) docs: Simplify examples - remove duplicated content and verbose summary jobs
- [`ab37f8e`](https://github.com/jacaudi/github-actions/commit/ab37f8eae61559072579de8877b01378ba0f706a) docs: Move workflow documentation to docs/workflows.md
- [`1016dd4`](https://github.com/jacaudi/github-actions/commit/1016dd40e56653eaf718097cbb4d3945f63c7a94) refactor: Remove master branch references, use only main
- [`363eca3`](https://github.com/jacaudi/github-actions/commit/363eca3989086db82fd15a52fd9422ae2050dd1b) fix: Add permissions and secrets inherit to ci.yml
- [`2cc0f56`](https://github.com/jacaudi/github-actions/commit/2cc0f561bfbd67fb5457c47349d6e0f5efceb99b) fix: Use full workflow paths in example-caller and example-release-on-tag
- [`9aa64cf`](https://github.com/jacaudi/github-actions/commit/9aa64cff47a6714062615029824f9e6f282d2a5a) fix: Use GitHub App bot for all uplift examples
- [`ac6b508`](https://github.com/jacaudi/github-actions/commit/ac6b5085b93d378d6b8a74ee3052e398edd94393) fix: Use GitHub App bot for uplift permissions
- [`bc44fcb`](https://github.com/jacaudi/github-actions/commit/bc44fcba6cd96a735d3e6b04a25498618b6bd815) docs: Add example workflows for release on tag creation (#12)
- [`2e28504`](https://github.com/jacaudi/github-actions/commit/2e28504599f48e23289bde634b360d5e812b3891) refactor: Rename docs/templates.md to docs/examples.md
- [`811a36a`](https://github.com/jacaudi/github-actions/commit/811a36ae5aa5ff6bc810bc09da3ca30431f3d342) refactor: Move example templates to docs/ directory
- [`16b28d6`](https://github.com/jacaudi/github-actions/commit/16b28d60d91f964782930f7e4d16dfb7d603df9a) refactor: Move workflow templates to dedicated templates/ directory
- [`2d3ae6a`](https://github.com/jacaudi/github-actions/commit/2d3ae6afb987863530d3bca1152463681198dd63) feat: Add self-release CI/CD workflow
- [`e905b3a`](https://github.com/jacaudi/github-actions/commit/e905b3a536a47fde98ce5c492ac1a1d1be3ad3a8) feat: Add image scanning workflow and enhance Docker + Helm pipeline
- [`f3d68bb`](https://github.com/jacaudi/github-actions/commit/f3d68bb9e24c48d3d17ea5a1b9bae26a63f634f8) feat: Add webhook workflow for post-release notifications
- [`104fb89`](https://github.com/jacaudi/github-actions/commit/104fb89c90c7d325195f54549780a1d762246869) docs: Add Docker + Helm release pipeline example
- [`dd7b8a5`](https://github.com/jacaudi/github-actions/commit/dd7b8a57a11fd54b5bd761a21ab21823cb004151) feat: Add dedicated GoReleaser reusable workflow
- [`7b16c28`](https://github.com/jacaudi/github-actions/commit/7b16c280e0c11dd06877d3659a2ac23a8593e78c) docs: Add complete Go SDK release pipeline example
- [`83a3e8b`](https://github.com/jacaudi/github-actions/commit/83a3e8ba5fc3fb7204fdbd999225fe25bb9d000b) docs: Move examples to docs/ directory and add documentation
- [`8de6f2e`](https://github.com/jacaudi/github-actions/commit/8de6f2e97cba8da86328f68b325992f120a22122) docs: Add example workflows for release on tag creation
- [`ae75898`](https://github.com/jacaudi/github-actions/commit/ae758987d1a29e1a1a1597d862593dadb354e90f) feat: Add support for GitHub App authentication in Uplift workflow
- [`573af36`](https://github.com/jacaudi/github-actions/commit/573af36f8336d779649bec1c41efb4e541ffcaf0) Merge pull request #4 from jacaudi/renovate/actions-checkout-6.x
- [`a557998`](https://github.com/jacaudi/github-actions/commit/a557998c58de38e15302a3608e2b30c7259e07a9) fix(test): Fix grep fallback pattern causing bash syntax errors
- [`34d5f4a`](https://github.com/jacaudi/github-actions/commit/34d5f4a1c146773363028500710e634d9d07b6bc) chore(deps): update actions/checkout action to v6
- [`f44a745`](https://github.com/jacaudi/github-actions/commit/f44a745015e3a730c589c39176eeb47b6bbb924f) Merge pull request #2 from jacaudi/auto-claude/001-initial-setup
- [`2fa902c`](https://github.com/jacaudi/github-actions/commit/2fa902ced9d2f01a5e4820107be84775dcef9151) fix: Correct formatting of regex patterns in changelog exclusion list
- [`6a4b83d`](https://github.com/jacaudi/github-actions/commit/6a4b83d7a3c9a153f6f5ed6880d10e9fddc817c7) fix: Remove .gitkeep files and untrack auto-claude security file (qa-requested)
- [`3dc73d8`](https://github.com/jacaudi/github-actions/commit/3dc73d89139beaf414a3727399577a992ec73de8) fix: Address QA issues (qa-requested)
- [`433e47e`](https://github.com/jacaudi/github-actions/commit/433e47e1d9bc0b3f30569b75df648496693de673) auto-claude: subtask-7-3 - Create example caller workflow for testing
- [`1e7ba9c`](https://github.com/jacaudi/github-actions/commit/1e7ba9c5b5eb01144b277c504ecb298690bee203) auto-claude: subtask-7-1 - Create comprehensive README.md with usage examples
- [`b657e4c`](https://github.com/jacaudi/github-actions/commit/b657e4cf1f6688bdfb4044fbd324dd9ec32641db) auto-claude: subtask-6-2 - Create automated release pipeline reusable workflow
- [`e746348`](https://github.com/jacaudi/github-actions/commit/e746348452c7cf249bad0e39da489f520106316c) auto-claude: subtask-6-1 - Create Uplift auto-tagging reusable workflow
- [`371cdf2`](https://github.com/jacaudi/github-actions/commit/371cdf222ceb25a07a571c0bca1d863b960afce4) auto-claude: subtask-5-1 - Create Helm OCI chart publishing reusable workflow
- [`91d1a50`](https://github.com/jacaudi/github-actions/commit/91d1a50a9d38a3a93150a9acaac27b3ee344f7d0) Merge pull request #1 from jacaudi/renovate/configure
- [`ebef7a0`](https://github.com/jacaudi/github-actions/commit/ebef7a07a9a91445159d11c955132323702cbe5a) auto-claude: subtask-4-1 - Create Docker multi-arch build reusable workflow
- [`bef0bfe`](https://github.com/jacaudi/github-actions/commit/bef0bfed3c0b4ae35a1f9cbea840b843f59d7e71) auto-claude: subtask-3-2 - Create configurable test runner reusable workflow
- [`b327d3d`](https://github.com/jacaudi/github-actions/commit/b327d3d3d761457c6f1a7546c286a9950bdcdd2d) auto-claude: subtask-3-1 - Create multi-language lint reusable workflow
- [`fc62118`](https://github.com/jacaudi/github-actions/commit/fc62118f3c7dbf4e7c9e5593bb1b76bdc7c72f9d) auto-claude: subtask-3-1 - Create multi-language lint reusable workflow
- [`bb36cc0`](https://github.com/jacaudi/github-actions/commit/bb36cc0da70f2f8e2574760ce72037c030b63f5f) auto-claude: subtask-2-3 - Create Python script for advanced summary generation
- [`b8fa7b0`](https://github.com/jacaudi/github-actions/commit/b8fa7b0507961f4df4eb2efe5f15aa54815ce796) auto-claude: subtask-2-2 - Create test-summary composite action for generating rich GitHub Actions summaries
- [`a4a4b51`](https://github.com/jacaudi/github-actions/commit/a4a4b5148f86afa432fae8d82c2bd3b087afaba0) auto-claude: subtask-2-1 - Create Docker build composite action with QEMU, Buildx, metadata, and build-push
- [`24ff410`](https://github.com/jacaudi/github-actions/commit/24ff4105fc2abb9fa42c667430746b0d41cf07b1) auto-claude: subtask-1-2 - Create .uplift.yml configuration for this repository
- [`a414cdb`](https://github.com/jacaudi/github-actions/commit/a414cdbff82908fe9a562b80e8c91e6c5c50b552) auto-claude: subtask-1-1 - Create .github directory structure
- [`795922c`](https://github.com/jacaudi/github-actions/commit/795922c16e2b1df9e47c0e7523e026ae30fada2e) Add renovate.json
- [`a1765b8`](https://github.com/jacaudi/github-actions/commit/a1765b8f12b3ce2e2092f300782135d4d70cd02d) Initial commit
