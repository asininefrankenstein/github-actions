# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [](https://github.com/jacaudi/github-actions/releases/tag/) - 0001-01-01

- [`da69b04`](https://github.com/jacaudi/github-actions/commit/da69b0427e48b04f6e3eb42652e77e9021898d6b) fix: Configure Renovate to use fix(deps) for version bumps

## [](https://github.com/jacaudi/github-actions/releases/tag/) - 0001-01-01

- [`c36ce3c`](https://github.com/jacaudi/github-actions/commit/c36ce3c621bcb1aa6bc7ff98d565fdad927bbd58) fix: Resolve syntax errors in image-scan.yml workflow

## [](https://github.com/jacaudi/github-actions/releases/tag/) - 0001-01-01

- [`272cdd1`](https://github.com/jacaudi/github-actions/commit/272cdd1197083b9c21d0761371f778b6ac644534) fix: Properly detect version creation in uplift workflow

## [](https://github.com/jacaudi/github-actions/releases/tag/) - 0001-01-01

- [`fab2b76`](https://github.com/jacaudi/github-actions/commit/fab2b766506787c7b7dd77f84dd7448f1dfa39a2) fix: Add yamllint config and resolve linting issues
- [`6361810`](https://github.com/jacaudi/github-actions/commit/63618102feef2e8ed8dae1f75eb447a201d36cc4) fix: Add packages write permission to CI/CD workflow
- [`ed8ddb3`](https://github.com/jacaudi/github-actions/commit/ed8ddb3d610ae2f9abeb726580d337b87c7ce234) Merge branch 'claude/review-release-workflow-idq4m'
- [`1016dd4`](https://github.com/jacaudi/github-actions/commit/1016dd40e56653eaf718097cbb4d3945f63c7a94) refactor: Remove master branch references, use only main
- [`363eca3`](https://github.com/jacaudi/github-actions/commit/363eca3989086db82fd15a52fd9422ae2050dd1b) fix: Add permissions and secrets inherit to ci.yml
- [`2cc0f56`](https://github.com/jacaudi/github-actions/commit/2cc0f561bfbd67fb5457c47349d6e0f5efceb99b) fix: Use full workflow paths in example-caller and example-release-on-tag
- [`9aa64cf`](https://github.com/jacaudi/github-actions/commit/9aa64cff47a6714062615029824f9e6f282d2a5a) fix: Use GitHub App bot for all uplift examples
- [`ac6b508`](https://github.com/jacaudi/github-actions/commit/ac6b5085b93d378d6b8a74ee3052e398edd94393) fix: Use GitHub App bot for uplift permissions
- [`2e28504`](https://github.com/jacaudi/github-actions/commit/2e28504599f48e23289bde634b360d5e812b3891) refactor: Rename docs/templates.md to docs/examples.md
- [`811a36a`](https://github.com/jacaudi/github-actions/commit/811a36ae5aa5ff6bc810bc09da3ca30431f3d342) refactor: Move example templates to docs/ directory
- [`16b28d6`](https://github.com/jacaudi/github-actions/commit/16b28d60d91f964782930f7e4d16dfb7d603df9a) refactor: Move workflow templates to dedicated templates/ directory
- [`2d3ae6a`](https://github.com/jacaudi/github-actions/commit/2d3ae6afb987863530d3bca1152463681198dd63) feat: Add self-release CI/CD workflow
- [`e905b3a`](https://github.com/jacaudi/github-actions/commit/e905b3a536a47fde98ce5c492ac1a1d1be3ad3a8) feat: Add image scanning workflow and enhance Docker + Helm pipeline
- [`f3d68bb`](https://github.com/jacaudi/github-actions/commit/f3d68bb9e24c48d3d17ea5a1b9bae26a63f634f8) feat: Add webhook workflow for post-release notifications
- [`dd7b8a5`](https://github.com/jacaudi/github-actions/commit/dd7b8a57a11fd54b5bd761a21ab21823cb004151) feat: Add dedicated GoReleaser reusable workflow
- [`ae75898`](https://github.com/jacaudi/github-actions/commit/ae758987d1a29e1a1a1597d862593dadb354e90f) feat: Add support for GitHub App authentication in Uplift workflow
- [`573af36`](https://github.com/jacaudi/github-actions/commit/573af36f8336d779649bec1c41efb4e541ffcaf0) Merge pull request #4 from jacaudi/renovate/actions-checkout-6.x
- [`a557998`](https://github.com/jacaudi/github-actions/commit/a557998c58de38e15302a3608e2b30c7259e07a9) fix(test): Fix grep fallback pattern causing bash syntax errors
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
