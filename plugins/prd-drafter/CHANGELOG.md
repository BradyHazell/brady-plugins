# Changelog

All notable changes to the prd-drafter plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] — 2026-06-17

### Changed
- PRD headers no longer include Figma or Linear epic link fields by default.
- Additional header link fields are now added only when `headerLinkFields` is defined in `.prdrc.json`.

## [1.2.0] — 2026-06-16

### Added
- `prd-to-html` skill for converting PRD Markdown files into standalone browser-printable HTML documents.
- Bundled `scripts/prd_to_html.py` converter with dark screen styling, light print styling, PRD metadata formatting, Open Questions formatting, lists, tables, code, blockquotes, and links.

### Changed
- Marketplace and plugin descriptions now mention structured updates and HTML export.

## [1.1.0] — 2026-05-26

### Added
- `prd-draft` workflow skill — orchestrates the full new-PRD process (discovery → drafting → validation) for agents that don't have access to the Claude Code slash commands and subagents.
- `prd-update` workflow skill — orchestrates the three update flows (resolve open questions, scope/content change, status promotion) for non-Claude agents.

### Why
The slash commands (`/prd-drafter:draft`, `/prd-drafter:update`) and the named subagents (`prd-interviewer`, `prd-drafter`, `prd-updater`) are Claude Code primitives. Agents installed via `npx skills` (Codex, Cursor, Goose, etc.) get the knowledge skills but were missing the workflow orchestration. The two new skills close that gap by capturing the orchestration logic in agent-agnostic form.

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
