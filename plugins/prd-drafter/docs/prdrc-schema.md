# `.prdrc.json` Configuration Schema

The `prd-drafter` plugin reads an optional `.prdrc.json` at the repo root to override its defaults. Drop this file in any repo where the defaults don't fit your team's conventions.

All fields are optional. Omit a field to fall back to the default for that field.

## Full schema

```json
{
  "outputPath": "./prds",
  "fileNaming": "kebab-case",
  "statusFolders": null,
  "statusLifecycle": ["Draft", "In Review", "Approved", "Shipped"],
  "projects": [],
  "headerLinkFields": ["Figma", "Linear epic"]
}
```

## Field-by-field

### `outputPath` *(string, default `"./prds"`)*

Where PRDs are saved, relative to the repo root.

```json
"outputPath": "./docs/prds"
```

Anything path-like works: `./prds`, `./docs/prds`, `./specs/product`, etc.

### `fileNaming` *(string, default `"kebab-case"`)*

Case convention for filenames. The drafter takes the feature name from the conversation and converts it to this case before saving.

| Value | "Alarm Centre" becomes |
|---|---|
| `"kebab-case"` *(default)* | `product-feature.md` |
| `"snake_case"` | `product_feature.md` |
| `"title-case"` | `Product Feature.md` |
| `"pascal-case"` | `ProductFeature.md` |

### `statusFolders` *(object or `null`, default `null`)*

If set, PRDs are placed in subfolders by status. Omit or set to `null` for a flat layout (status only tracked in frontmatter).

```json
"statusFolders": {
  "Draft": "in-progress",
  "In Review": "in-progress",
  "Approved": "in-progress",
  "Shipped": "shipped"
}
```

Multiple statuses can map to the same folder (above, the first three all live in `in-progress`). Folders are created on first save.

Any backlog-style folder needs to be added explicitly:

```json
"statusFolders": {
  "Draft": "in-progress",
  "Shipped": "shipped",
  "Backlog": "backlog"
}
```

### `statusLifecycle` *(array, default `["Draft", "In Review", "Approved", "Shipped"]`)*

The full status ladder, in order. The updater uses this when promoting status. Custom states work fine:

```json
"statusLifecycle": ["Idea", "Drafting", "Stakeholder Review", "Locked", "Live"]
```

If you customize this, also customize `statusFolders` so every status has a folder mapping (or use the flat layout with `statusFolders: null`).

### `projects` *(array of strings, default `[]`)*

Multi-project repos can list their project slugs here. When non-empty, the interviewer asks which project a PRD belongs to and inserts `/[project]/` into the save path.

```json
"projects": ["billing", "auth", "notifications"]
```

A PRD for the `billing` project saves to `[outputPath]/billing/[status-folder]/[feature].md` (or omitting the status folder if `statusFolders` is null).

Use a flat array of slug strings. If you need richer project metadata (description, owner), open an issue — the schema can be extended.

### `headerLinkFields` *(array of strings, default `["Figma", "Linear epic"]`)*

Optional link fields offered in the PRD header. The interviewer asks about each during discovery; users can answer `N/A` for any that don't apply.

```json
"headerLinkFields": ["Figma", "Linear epic", "Jira ticket", "Loom walkthrough"]
```

Common additions:
- **Design**: `Figma`, `Sketch`, `Penpot`
- **Tracking**: `Linear epic`, `Jira ticket`, `GitHub issue`, `Notion task`
- **Discussion**: `Slack thread`, `Loom walkthrough`
- **Specification**: `SRS`, `ADR`, `Related PRD`

## Worked examples

### Example 1 — Tiny single-repo project (no config)

No `.prdrc.json`. Defaults apply. A draft PRD for "User Onboarding" saves to:

```
./prds/user-onboarding.md
```

### Example 2 — Docs-folder convention

```json
{
  "outputPath": "./docs/prds",
  "fileNaming": "title-case"
}
```

Saves to:

```
./docs/prds/User Onboarding.md
```

### Example 3 — Multi-project with status folders

```json
{
  "outputPath": "./product",
  "fileNaming": "title-case",
  "statusFolders": {
    "Draft": "in-progress",
    "In Review": "in-progress",
    "Approved": "in-progress",
    "Shipped": "shipped"
  },
  "projects": ["billing", "auth", "notifications"]
}
```

A Draft PRD for "Webhook Retries" in the `billing` project saves to:

```
./product/billing/in-progress/Webhook Retries.md
```

### Example 4 — Custom status lifecycle for a smaller team

```json
{
  "statusLifecycle": ["Idea", "Drafting", "Locked", "Shipped"],
  "statusFolders": {
    "Idea": "backlog",
    "Drafting": "active",
    "Locked": "active",
    "Shipped": "shipped"
  }
}
```

## What happens if `.prdrc.json` is malformed?

The plugin surfaces the parse error and asks whether to proceed with defaults or stop. It never silently ignores a broken config — that's how files end up in surprising places.
