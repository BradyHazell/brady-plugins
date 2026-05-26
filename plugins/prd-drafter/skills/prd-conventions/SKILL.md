---
name: prd-conventions
description: Conventions for PRD file naming, folder placement, status lifecycle, and project association. Reads .prdrc.json at the repo root for per-repo overrides, otherwise applies sensible defaults. Loaded by every agent in the prd-drafter plugin so drafts land in the right place with consistent naming.
version: 1.0.0
tags: [prd, conventions, file-naming, configuration]
---

# PRD Conventions

## Purpose

A PRD without a consistent home becomes orphaned. This skill defines where PRDs live, how they're named, and how their lifecycle status moves them between folders. Defaults are deliberately simple — most repos can use them unchanged. Larger repos or teams with established conventions configure overrides via `.prdrc.json`.

## When to Use

- Loaded by every drafter, updater, and validator agent in this plugin
- Consulted before suggesting a save path
- Consulted when promoting a PRD between statuses

## Configuration Discovery

Before writing or moving any file, check for a `.prdrc.json` at the repo root (use `Read` with the absolute path; treat a `not found` error as "no config"). If present, parse it. If absent, apply the defaults below.

The full schema is documented in `docs/prdrc-schema.md` at the plugin root.

## Defaults (no `.prdrc.json` present)

| Setting | Default |
|---|---|
| Output path | `./prds/` |
| File naming | `kebab-case` |
| File pattern | `[feature-name].md` (e.g. `alarm-centre.md`) |
| Status folders | none — all PRDs live flat in `./prds/`, status tracked in frontmatter only |
| Status lifecycle | `Draft → In Review → Approved → Shipped` |
| Projects | none — single-repo, no project association required |
| Header link fields | `Figma`, `Linear epic` (offered, both optional) |

So in a fresh repo with no config, a draft PRD for an "Alarm Centre" feature saves to `./prds/alarm-centre.md` with `Status: Draft` in its frontmatter.

## Overriding via `.prdrc.json`

A `.prdrc.json` at the repo root can override any of these. Example for a multi-project repo with status folders:

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

With this config, a Draft PRD for billing would save to `./docs/prds/billing/in-progress/Alarm Centre.md`.

### Supported `fileNaming` values

| Value | Example for "Alarm Centre" |
|---|---|
| `kebab-case` *(default)* | `alarm-centre.md` |
| `snake_case` | `alarm_centre.md` |
| `title-case` | `Alarm Centre.md` |
| `pascal-case` | `AlarmCentre.md` |

If `statusFolders` is set, the file is placed inside the folder matching its status. Folders are auto-created on first save.

### Supported `statusFolders` shapes

- **`null` or omitted** *(default)* — flat layout, no status subfolders
- **Object map** (`{"Draft": "in-progress", ...}`) — map each status to a subfolder name. Multiple statuses can map to the same folder.

### `projects`

- **`null` or empty array** *(default)* — single-project repo; no project association asked
- **Array of project slugs** — multi-project repo; the interviewer asks which project, and the path inserts `/[project]/` between `outputPath` and any status folder

### `headerLinkFields`

The list of optional link fields offered in the PRD header. Defaults to `["Figma", "Linear epic"]`. Common additions: `Jira ticket`, `Notion doc`, `Loom walkthrough`, `Slack thread`. The agent will offer each as an `AskUserQuestion` option during discovery; users can answer `N/A` for any that don't apply.

## Status Lifecycle

Default ladder: `Draft → In Review → Approved → Shipped`. Override with the `statusLifecycle` array if your team uses different states (e.g. `["Drafting", "Stakeholder Review", "Locked", "Live"]`).

The plugin **never advances Status automatically**. It is always a deliberate human action via `/prd-drafter:update`.

| Transition | Trigger | Side effects |
|---|---|---|
| Draft → In Review | Author marks ready for stakeholder feedback | Update Status field; bump minor version (0.1 → 0.2) |
| In Review → Draft | Stakeholders request rework | Update Status; bump minor version |
| In Review → Approved | All stakeholders sign off | Update Status; bump to 1.0 |
| Approved → Shipped | Feature released | Move file to shipped folder (if `statusFolders` set); update Status |

## File Naming Pattern

Default pattern is `[feature-name].md` (with case applied per `fileNaming`). For PRDs that already have multiple versions, append `-v2`, `-v3`, etc. — never overwrite a previous version unless the user explicitly asks.

Examples (default `kebab-case`):
- `alarm-centre.md`
- `multi-tenant-billing.md`
- `bulk-device-import.md`
- `alarm-centre-v2.md`

## Suggested Save Path Logic

When the drafter or updater is ready to save:

1. **Read `.prdrc.json`** (if present) to get overrides.
2. **If `projects` is non-empty**, confirm the project with the user using `AskUserQuestion`. Never assume.
3. **Compute the suggested path** using the resolved settings:
   - `outputPath` + (project folder, if any) + (status folder, if `statusFolders` set) + feature filename
4. **Present to the user for confirmation**, allowing override.
5. **Check whether the file already exists.** If yes, ask: overwrite, save as new version (`-v2`), or pick a new name?

## Linked Documents

A PRD may link to external docs. The default header link fields are `Figma` and `Linear epic`, but `.prdrc.json` can extend this. Common additions:

- **Design**: Figma, Sketch, Penpot
- **Tracking**: Linear, Jira, GitHub issue, Notion task
- **Discussion**: Slack thread, Loom walkthrough
- **Specification**: SRS, ADR, related PRD (use relative paths within the repo)

Use `N/A` (not blank) when a link does not apply, so the field clearly reflects a deliberate decision.

## Common Mistakes

- **Saving without checking `.prdrc.json`** — a config file may exist that the user expects to be honoured.
- **Saving without asking which project** when `projects` is non-empty — never assume.
- **Pasting screenshots into the PRD** instead of linking — bloats the file and breaks AI readability. Always link to the source (Figma URL, etc.).
- **Overwriting a Shipped PRD** when iterating — open a new version (`-v2`) instead. Shipped is a historical artefact.
- **Hardcoding paths in the conversation** — always recompute from the resolved config so future agents stay consistent.
