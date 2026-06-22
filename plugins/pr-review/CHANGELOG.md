# Changelog

All notable changes to the pr-review plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-06-22

### Changed
- Clarified the Azure DevOps metadata command for organization-wide PR lookup with explicit JSON output.

## [1.0.0] - 2026-06-18

Initial public release.

### Added
- `/pr-review:review` command for reviewing a PR from a number or URL.
- `pr-reviewer` agent for fetching PR context from the current repository and drafting review comments.
- Command-equivalent `pr-review` overseer skill for coordinating focused review passes, deduplicating findings, and selecting final comments.
- `pr-diff-intake` skill for GitHub and Azure DevOps PR input handling.
- Focused review-pass skills for obvious issues, tests, security/privacy, API contracts, maintainability, performance/reliability, interesting decisions, and output formatting.
