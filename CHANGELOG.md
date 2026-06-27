# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1] - 2026-06-24

### CI/CD
- Add Stage 2 release workflow (TestPyPI upload on `v*` tag)
- Add Gitea Actions CI workflow for automated testing

## [0.2.0] - 2026-06-21

### Features
- `OkwYesNo` enum with `parse_yes_no()` and `assert_exists()` for
  existence checks (YES/TRUE/1 → must exist, NO/FALSE/0 → must not exist)
- `{KEY}` resolver for unified value expansion (`$MEM{KEY}` placeholders)
- WCM matcher changed from substring-contains to `fnmatch` wildcard
  pattern matching (`*` = any chars, `?` = one char)

### Fixes
- Fix duplicate exception classes
- Fix license format to SPDX string

### Docs
- Add AGPL-3.0 license
- Add Python 3.14 classifier
- Update README with YES/NO model and match mode documentation

## [0.1.0] - 2026-05-01

### Features
- Initial release: matchers (EXACT, WCM, REGX) and timeout utilities
