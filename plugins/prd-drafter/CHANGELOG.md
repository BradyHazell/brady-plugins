# Changelog

All notable changes to the prd-drafter plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-05-26

Initial public release.

### Added
- `/prd-drafter:draft` — conversational PRD discovery and drafting
- `/prd-drafter:update` — three update flows (resolve open questions, scope change, status promotion)
- `/prd-drafter:validate` — structural completeness, open-question hygiene, specificity, consistency, decision readiness
- Four agents: `prd-interviewer`, `prd-drafter`, `prd-updater`, `prd-validator`
- Four skills: `prd-template`, `prd-discovery`, `prd-quality`, `prd-conventions`
- `.prdrc.json` configuration support for custom output paths, multi-project repos, status workflow, naming case, and header link fields
- Released as part of the `brady-plugins` Claude Code marketplace; installable via `/plugin install prd-drafter@brady-plugins`
