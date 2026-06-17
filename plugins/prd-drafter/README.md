# prd-drafter

Drafts Product Requirements Documents through conversational discovery — not template filling — and exports them to browser-printable HTML for review copies.

> **The purpose of a PRD is to make it clear what feature we want to implement, surface unknowns, challenge assumptions, and discuss approaches so the document is genuinely useful as a source of truth for implementation.**

A well-written PRD lets an engineer pick up a feature and build it without re-asking the same questions five times. A poorly written PRD becomes a fiction layer that everyone agrees to ignore. This plugin aims for the former by:

1. **Acting as a PM, not a stenographer** — challenges scope, surfaces hidden assumptions, pushes back on vague language
2. **Treating Open Questions as a first-class output** — questions are kept verbatim with `**Answer:** TBC` until resolved, then become the decision log
3. **Adapting the template to the feature** — backend-only changes don't get a Feature Flag section; user-invisible work doesn't get Success Metrics
4. **Honouring your repo's conventions** — drop a `.prdrc.json` at the repo root to point the plugin at your folder structure, status workflow, and project layout
5. **Exporting clean review copies** — turn PRD Markdown into standalone HTML with a dark screen theme and light print stylesheet for browser PDF export

> This is one plugin in the [`brady-plugins`](https://github.com/BradyHazell/brady-plugins) marketplace.

## Installation

### Claude Code

```
/plugin marketplace add BradyHazell/brady-plugins
/plugin install prd-drafter@brady-plugins
```

### Other agents (Codex, Cursor, Goose, etc.)

```bash
# Auto-detect installed agents
npx skills add BradyHazell/brady-plugins

# Or target a specific agent
npx skills add BradyHazell/brady-plugins -a codex
npx skills add BradyHazell/brady-plugins -a cursor
```


See [`AGENTS.md`](./AGENTS.md) in this folder for the plugin's internal layout.

## Commands

| Command | Description |
|---|---|
| `/prd-drafter:draft` | Entry point — runs discovery interview, drafts the PRD, validates it, saves to the resolved folder |
| `/prd-drafter:update <path>` | Update an existing PRD (resolve open questions, scope change, or status promotion) |
| `/prd-drafter:validate <path>` | Validate a PRD for completeness, open-question hygiene, specificity, and consistency |

## Agents

| Agent | Role |
|---|---|
| `prd-interviewer` | Conversational discovery — problem-framing, scope-shaping, edge-case, and conditional-section questions. Produces a `## Feature Context` block. |
| `prd-drafter` | Reads the Feature Context block and writes the actual PRD with required + triggered conditional sections. |
| `prd-updater` | Updates an existing PRD across three flows: resolve open questions, scope/content change, or status promotion. |
| `prd-validator` | Checks structural completeness, open-question hygiene, specificity, internal consistency, and decision readiness. |

## Skills

Workflow and utility skills (agent-agnostic workflows that can run without slash commands):

| Skill | Purpose |
|---|---|
| `prd-draft` | End-to-end workflow for creating a new PRD (discovery → drafting → validation). Use in non-Claude agents when the slash command isn't available. |
| `prd-update` | Workflow for updating an existing PRD across the three flows (resolve open questions, scope change, status promotion). |
| `prd-to-html` | Converts an existing PRD Markdown file into standalone browser-printable HTML with dark screen styling and light print styling. |

Knowledge skills (reference content the workflow skills lean on):

| Skill | Purpose |
|---|---|
| `prd-template` | The canonical PRD section structure — required sections, conditional sections, header block, output skeleton. |
| `prd-discovery` | The conversation approach — how to ask, when to challenge, how to surface open questions. |
| `prd-quality` | The validator's quality rubric — structural completeness, open-question hygiene, specificity, consistency, decision readiness. |
| `prd-conventions` | File-naming, folder placement, status lifecycle. Reads `.prdrc.json` for per-repo overrides. |

## Configuration: `.prdrc.json`

By default, PRDs save to `./prds/[feature-name].md` with kebab-case names, status tracked in frontmatter, and no extra tool-specific header links. That suits most single-repo projects.

For richer conventions — multi-project repos, status subfolders, custom lifecycle, additional header link fields — drop a `.prdrc.json` at your repo root:

```json
{
  "outputPath": "./docs/prds",
  "fileNaming": "title-case",
  "statusFolders": {
    "Draft": "in-progress",
    "In Review": "in-progress",
    "Approved": "in-progress",
    "Shipped": "shipped"
  },
  "statusLifecycle": ["Draft", "In Review", "Approved", "Shipped"],
  "projects": ["billing", "auth", "notifications"],
  "headerLinkFields": ["Figma", "Linear epic", "Jira ticket"]
}
```

See [`docs/prdrc-schema.md`](./docs/prdrc-schema.md) for the full schema with worked examples, and [`docs/prdrc.example.json`](./docs/prdrc.example.json) for a copy-paste starting point.

## Template Overview

Every PRD produced by this plugin has:

**Required sections** (always):
1. Header (Status, Author, Date, Version + optional Project + any configured link fields)
2. Problem Statement
3. Goal
4. User Stories
5. Proposed Solution
6. Edge Cases
7. Out of Scope
8. Open Questions (`**Question:** ... / **Answer:** ...` pairs, `TBC` for unresolved)

**Conditional sections** (included only when triggered by the feature):
- Success Metrics — when there's a measurable outcome
- Feature Flag Strategy — when user-visible AND has rollout risk
- Dependencies — when other features/services/vendors are involved
- Data Model Changes — when schema changes are needed
- Permissions & Access Control — for multi-tenant or role-based access changes
- Migration / Backfill — when existing data needs to move
- Telemetry & Observability — when new metrics/logs/alarms are needed
- Stakeholders — when more than two people need to weigh in
- Design References — when design files, prototypes, or mocks exist
- Risks & Mitigations — when real risks exist beyond "might have bugs"

Conditional sections that don't apply are **omitted entirely** rather than filled with "N/A".

## Open Questions — The Key Output

The Open Questions section is the most important part of a PRD. It captures:

- Decisions that haven't been made yet (`**Answer:** TBC`)
- Decisions that have been made, with the reasoning (`**Answer:** [decision + why]`)
- Trade-offs surfaced during discovery

When this PRD is later loaded as implementation context (e.g. by a coding agent or a new engineer), the `**Question:** / **Answer:**` format is directly parseable — the engineer can see exactly which assumptions are firm and which are still open.

**Answered questions stay** in the PRD. They become the decision log. Deleting them loses the reasoning.

## Workflows

### New PRD

```
1. User runs /prd-drafter:draft
2. prd-interviewer asks:
   - Which project? (only if .prdrc defines projects)
   - What problem, who experiences it, why now?
   - What's MVP scope, what's out?
   - Walk through user flows, ask "what if..." on each
   - Apply each conditional section trigger
   - Produces a ## Feature Context block
3. prd-drafter:
   - Reads Feature Context
   - Asks 1-3 final clarifications if needed
   - Composes the PRD (required + triggered conditional sections)
   - Shows draft inline
   - Confirms save path with user
   - Writes the file
4. prd-validator runs and reports status
5. PRD is saved to the path resolved from .prdrc.json
```

### Update PRD (resolve open questions)

```
1. User runs /prd-drafter:update <path>
2. prd-updater reads the PRD, confirms Flow A
3. Lists current open questions
4. User provides answers
5. Updates **Answer:** TBC → answer + reasoning
6. Bumps version, appends to Changelog
7. prd-validator confirms
```

### Update PRD (scope change)

```
1. User runs /prd-drafter:update <path>
2. prd-updater reads the PRD, confirms Flow B
3. Asks user to walk through what changed
4. Pushes back if scope is growing past one feature
5. Edits only the affected sections (preserves rest verbatim)
6. Bumps version (minor for additions, major for scope changes)
7. Appends to Changelog
8. prd-validator confirms
```

### Promote status

```
1. User runs /prd-drafter:update <path>
2. prd-updater confirms Flow C (status promotion)
3. Health check before promoting (empty required sections, load-bearing TBCs)
4. Updates Status field, bumps version, appends to Changelog
5. If statusFolders is configured and the new status maps to a folder,
   moves the file to that folder (user deletes the old copy)
```

## Quality Gates

Every drafted PRD is validated against:

1. **Structural completeness** — all 8 required sections present and non-empty; triggered conditional sections present
2. **Open question hygiene** — `**Question:** / **Answer:**` format, vague questions flagged
3. **Specificity & grounding** — vague phrases ("fast", "scalable", "improve") surfaced for sharpening
4. **Internal consistency** — Problem/Goal alignment, Out of Scope not contradicted elsewhere, Open Questions not contradicting body
5. **Decision readiness** — narrative judgement: could an engineer pick this up?

Validator output status:

| Status | Meaning |
|---|---|
| **PASS** | Ready for stakeholder review. `TBC` open questions are fine. |
| **CONDITIONAL** | Usable but should be tightened — specificity, vague questions, or a missing triggered conditional section. |
| **FAIL** | A required section is missing/empty, or the document has internal contradictions. |

The validator never certifies a PRD as "approved" — that's a stakeholder decision.

## Directory Structure

```
prd-drafter/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── prd-interviewer.md
│   ├── prd-drafter.md
│   ├── prd-updater.md
│   └── prd-validator.md
├── commands/
│   ├── draft.md
│   ├── update.md
│   └── validate.md
├── skills/
│   ├── prd-draft/SKILL.md         ← workflow: orchestrates new-PRD creation
│   ├── prd-update/SKILL.md        ← workflow: orchestrates update flows
│   ├── prd-to-html/SKILL.md       ← workflow: exports PRD Markdown to printable HTML
│   ├── prd-template/SKILL.md      ← knowledge: section structure
│   ├── prd-discovery/SKILL.md     ← knowledge: conversation approach
│   ├── prd-quality/SKILL.md       ← knowledge: validation rubric
│   └── prd-conventions/SKILL.md   ← knowledge: file/folder/status rules
├── docs/
│   ├── prdrc-schema.md
│   └── prdrc.example.json
├── AGENTS.md            ← contributor/maintainer guide for AI agents
├── CLAUDE.md            ← @AGENTS.md import for Claude Code
├── CHANGELOG.md
└── README.md            ← this file
```

## Contributing

Issues and pull requests welcome. Particularly interested in:

- Additional `headerLinkFields` patterns from teams using different toolchains
- Conventions schemas for layouts I haven't anticipated
- Better defaults

Before contributing, read [`AGENTS.md`](./AGENTS.md) in this folder — it covers the plugin's layout, where to extend, versioning rules, and style conventions.

## License

MIT — see the repo-root [LICENSE](../../LICENSE).
