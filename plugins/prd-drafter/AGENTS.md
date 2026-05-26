# AGENTS.md — prd-drafter maintainer notes

Plugin-specific guidance for any AI agent maintaining or extending `prd-drafter`. The repo-root [`AGENTS.md`](../../AGENTS.md) covers cross-plugin conventions; this file covers what's unique to this plugin.

## What this plugin does

Walks a user through a conversational PRD discovery, drafts the document, validates it, and supports updates over time. Output is a markdown file with structured sections, `**Question:** / **Answer:** TBC` open questions, and a changelog.

Behavioural philosophy: act like a PM, not a stenographer. Challenge scope, surface assumptions, push back on vague language, treat Open Questions as first-class output.

## Layout

```
prd-drafter/
├── .claude-plugin/plugin.json   # plugin manifest (name, version, author, MIT)
├── agents/
│   ├── prd-interviewer.md       # Phase 1 — conversational discovery
│   ├── prd-drafter.md           # Phase 2 — turns Feature Context block into the PRD
│   ├── prd-updater.md           # Updates (resolve Qs / scope change / status promote)
│   └── prd-validator.md         # Read-only quality check
├── commands/
│   ├── draft.md                 # /prd-drafter:draft — full pipeline
│   ├── update.md                # /prd-drafter:update <path>
│   └── validate.md              # /prd-drafter:validate <path>
├── skills/
│   ├── prd-draft/SKILL.md       # WORKFLOW — orchestrates new-PRD creation (Claude-agnostic)
│   ├── prd-update/SKILL.md      # WORKFLOW — orchestrates update flows (Claude-agnostic)
│   ├── prd-template/SKILL.md    # knowledge — canonical section structure + output skeleton
│   ├── prd-discovery/SKILL.md   # knowledge — how to conduct the interview
│   ├── prd-quality/SKILL.md     # knowledge — validator's rubric
│   └── prd-conventions/SKILL.md # knowledge — file/folder/status conventions (reads .prdrc.json)
├── docs/
│   ├── prdrc-schema.md          # full .prdrc.json schema reference
│   └── prdrc.example.json       # copy-paste starting point
├── AGENTS.md                    # this file
├── CLAUDE.md                    # @AGENTS.md import
├── README.md                    # end-user docs
└── CHANGELOG.md                 # per-plugin version history
```

## Where each thing belongs

When a contributor (or you, an AI agent) extends the plugin, the destination depends on what's being added:

| Adding... | Where it goes | Bumps |
|---|---|---|
| A new conditional section in the PRD template | `skills/prd-template/SKILL.md` (add to the table + trigger list) AND `agents/prd-interviewer.md` (Phase 4 trigger list) AND `skills/prd-draft/SKILL.md` (Phase 4 list) | MINOR |
| A new validation check | `skills/prd-quality/SKILL.md` (rubric) AND `agents/prd-validator.md` (Process step) | MINOR |
| A new `.prdrc.json` config field | `skills/prd-conventions/SKILL.md` (defaults) AND `docs/prdrc-schema.md` (schema doc) AND `docs/prdrc.example.json` if it's commonly used | MINOR for additive, MAJOR if it changes a default |
| A new interview question for an existing phase | `skills/prd-discovery/SKILL.md` AND mirror in `skills/prd-draft/SKILL.md` (Phase X block) | PATCH (clarification) or MINOR (new mandatory question) |
| A change to the new-PRD workflow itself | `skills/prd-draft/SKILL.md` AND the corresponding `agents/prd-interviewer.md` + `agents/prd-drafter.md` + `commands/draft.md` so Claude and non-Claude users stay in sync | MINOR (additive) or MAJOR (behavior change) |
| A change to the update workflow | `skills/prd-update/SKILL.md` AND `agents/prd-updater.md` + `commands/update.md` | MINOR or MAJOR per above |
| A new slash command | `commands/<name>.md` + reference in `README.md` + reference in `AGENTS.md` here. If it has cross-agent value, add a parallel workflow skill in `skills/`. | MINOR |
| A new agent | `agents/<name>.md` + reference in any command that should invoke it | MINOR |
| Typo / clarification / no-behavior-change edit | wherever the typo is | PATCH |

**Critical**: the workflow skills (`prd-draft`, `prd-update`) and the Claude-Code primitives (commands + named agents) are parallel implementations of the same behavior. When one changes, the other must change too. Drift between them means Claude users and non-Claude users get different behavior, which is the worst possible outcome.

## Versioning rules (plugin-specific elaboration)

The repo-root AGENTS.md sets the general SemVer rules. Specific to `prd-drafter`:

- **Changing the default `outputPath` or `fileNaming`** → MAJOR. Existing users have files in the old location.
- **Adding a new conditional section** (e.g. a "Compliance Considerations" section) → MINOR.
- **Renaming a section** in the template → MAJOR. Validators would fail on existing PRDs.
- **Loosening a validation rule** → PATCH (no user breakage).
- **Tightening a validation rule** → MINOR if it just adds a CONDITIONAL warning; MAJOR if it makes previously-PASS PRDs newly FAIL.
- **Changing the "illustrative names" note in Data Model Changes** → MINOR (it's appended to existing PRDs by the updater, so existing docs get it on their next update).

## Style conventions specific to this plugin

### Discovery questions are batched, not interrogated

The interviewer should ask 1–3 questions at a time and build on prior answers. Adding a new mandatory question to `prd-discovery` means thinking about which phase it belongs in and how it batches with existing questions. Don't append a new bullet to the end of a phase — slot it in.

### Open Questions are sacred

Every change to the validator, drafter, or updater must preserve these rules:
- `**Question:** / **Answer:**` pair format
- Resolved questions are *kept*, not deleted (they're the decision log)
- `TBC` is healthy and does not lower validation status

If a proposed change conflicts with these, escalate to a discussion — don't silently change them.

### Conditional sections are opt-in, not default

The drafter must judge whether each conditional section applies before including it. A PRD bloated with "N/A" sections trains readers to skim. Adding a new conditional section means adding both the trigger (when to include) and the omission policy (when to leave out).

### Status advancement is human

The updater never auto-advances Status. Always confirm with the user. This rule should not be relaxed.

### File operations confirm before writing

The drafter and updater always confirm the save path with the user before writing. The updater never deletes the old file when moving to a new status folder — it writes the new file and asks the user to delete the old. This rule should not be relaxed.

## Configuration: `.prdrc.json`

The plugin reads an optional `.prdrc.json` at the **target repo root** (not this plugin's root) for per-repo overrides. See [`docs/prdrc-schema.md`](./docs/prdrc-schema.md) for the full schema.

When changing the conventions skill or adding a new config field:

1. Update `skills/prd-conventions/SKILL.md` — the Defaults table and the "Overriding via `.prdrc.json`" section.
2. Update `docs/prdrc-schema.md` — the field-by-field reference.
3. Optionally update `docs/prdrc.example.json` if the new field is commonly set.
4. Update every agent that needs to know about the new field — usually the drafter and validator.

## Cross-references in the plugin

These need to stay consistent when you rename or restructure anything:

- `commands/*.md` reference agents by name (`prd-interviewer`, `prd-drafter`, `prd-updater`, `prd-validator`). Rename → break.
- `agents/*.md` reference skills by name (`prd-conventions`, `prd-template`, `prd-discovery`, `prd-quality`). Rename → break.
- Slash commands are namespaced under `prd-drafter:` (the plugin name from `plugin.json`). Renaming the plugin → all commands change → users have to relearn the namespace.
- `README.md` documents all commands, agents, and skills. Any addition/rename/removal must update README.

If you rename anything, grep the plugin folder for the old name first and update every reference.

## Testing changes

There's no automated test suite (yet). Verify changes by:

1. Installing the plugin locally (`claude --plugin-dir ./plugins/prd-drafter`) or via the marketplace mechanism.
2. Running `/prd-drafter:draft` on a test feature both with and without a `.prdrc.json` at the test repo's root.
3. Running `/prd-drafter:update` against an existing PRD (try all three flows).
4. Running `/prd-drafter:validate` against PRDs in good and bad shape.
5. Checking that the validator catches what the change was supposed to introduce.

## What this plugin should NOT do

- **Should not certify a PRD as approved.** Approval is a human decision; validation only checks structural completeness and surface quality.
- **Should not invent specifics.** Use `[PLACEHOLDER]` for unknown facts. Don't make up numbers, dates, owners.
- **Should not delete files.** Even when promoting to Shipped or saving a new version, the user deletes old files.
- **Should not write Claude-specific language into output PRDs.** The generated PRD footer says "drafted using the `prd-drafter` plugin", not "Claude Code plugin" — the PRDs themselves should be agent-agnostic artifacts.

## Open questions / known limitations

Worth knowing if you're considering extensions:

- **No automated tests.** A test harness that runs the agents against canned inputs would be valuable but doesn't exist.
- **`.prdrc.json` parsing is implicit** — there's no schema-validation step that warns on unknown fields. Worth adding when the config grows past a handful of fields.
- **Multi-project repos aren't deeply modeled.** The `projects` array is a flat list of slugs; richer project metadata (owners, descriptions) would need a schema extension.
- **No internationalisation.** All prompts and templates are English.
