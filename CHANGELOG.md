# Changelog

## [0.16.1](https://github.com/jacaudi/github-actions/compare/v0.16.0...v0.16.1) (2026-04-06)

### Bug Fixes

* conform v0.16.0 changelog entry to h2 format and clean up noise ([298fe97](https://github.com/jacaudi/github-actions/commit/298fe9714edc5538853107d96ee352d8a0f69046))
* use h2 heading for changelog version entries ([a88e901](https://github.com/jacaudi/github-actions/commit/a88e9015081fe51631a639d819348be32a1d8c43))

## [0.16.0](https://github.com/jacaudi/github-actions/compare/v0.15.5...v0.16.0) (2026-04-06)

### Breaking Changes

* replace go-semantic-release with JS semantic-release ([0925ea5](https://github.com/jacaudi/github-actions/commit/0925ea54dbcf58917624700b7927346763323e6b))

### Bug Fixes

* keep breaking changes as minor bumps during 0.x.x development ([58b3581](https://github.com/jacaudi/github-actions/commit/58b3581a1c97a51502efc4555326ad4a596e0a41))
* use h2 heading for changelog version entries ([a88e901](https://github.com/jacaudi/github-actions/commit/a88e9015081fe51631a639d819348be32a1d8c43))

## 0.15.5 (2026-04-05)

#### Bug Fixes

* support golangci-lint v2 output flag syntax in JSON save step ([af5736e0](https://github.com/jacaudi/github-actions/commit/af5736e0a94b69d6b4d2c89ba355090322c38187))

## 0.15.4 (2026-04-05)

#### Bug Fixes

* remove document-start markers from example templates ([e3c74f70](https://github.com/jacaudi/github-actions/commit/e3c74f7028d2ed785fa8e1f29064bd095fd749c0))

## 0.15.3 (2026-04-05)

#### Bug Fixes

* use non-conventional commit message for changelog commit ([a1ebee1d](https://github.com/jacaudi/github-actions/commit/a1ebee1d468fc1df69d8e8e5f7fd2b5059889230))

## 0.15.2 (2026-04-05)

#### Bug Fixes

* changelog commit should not appear in release notes ([80167021](https://github.com/jacaudi/github-actions/commit/80167021db60adecd7835c5362ae9b524288567b))

#### Documentation

* conform v0.15.0 and v0.15.1 changelog entries to semrel format ([591f50f4](https://github.com/jacaudi/github-actions/commit/591f50f4b2e01760b6c871bd39aff52cc1cede6c))
* update README, architecture, changelog, and add linked commit hashes ([83b880bb](https://github.com/jacaudi/github-actions/commit/83b880bb97bc93146aacf956ed2fb76594fabc09))

## 0.15.1 (2026-04-04)

#### Bug Fixes

* add changelog-file input to ci.yml semantic release job ([943c1216](https://github.com/jacaudi/github-actions/commit/943c1216))

## 0.15.0 (2026-04-04)

#### Breaking Changes

* replace uplift with go-semantic-release for versioning ([6638b09b](https://github.com/jacaudi/github-actions/commit/6638b09b))
* replace go-semantic-release with uplift, restructure as three-stage pipeline ([809f5933](https://github.com/jacaudi/github-actions/commit/809f5933))

#### Bug Fixes

* add missing permissions for semantic-release in ci workflows ([b3ab80cc](https://github.com/jacaudi/github-actions/commit/b3ab80cc))

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

## [v0.1.2](https://github.com/jacaudi/github-actions/releases/tag/v0.1.2) - 2026-01-21

- [`c36ce3c`](https://github.com/jacaudi/github-actions/commit/c36ce3c621bcb1aa6bc7ff98d565fdad927bbd58) fix: Resolve syntax errors in image-scan.yml workflow

## [v0.1.1](https://github.com/jacaudi/github-actions/releases/tag/v0.1.1) - 2026-01-21

- [`272cdd1`](https://github.com/jacaudi/github-actions/commit/272cdd1197083b9c21d0761371f778b6ac644534) fix: Properly detect version creation in uplift workflow

## [v0.1.0](https://github.com/jacaudi/github-actions/releases/tag/v0.1.0) - 2026-01-21

- Initial release
