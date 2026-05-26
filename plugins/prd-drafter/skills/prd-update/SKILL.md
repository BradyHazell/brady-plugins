---
name: prd-update
description: Workflow for updating an existing Product Requirements Document. Handles three flows — resolving open questions, scope/content changes, and status promotion through the configured lifecycle. Preserves unchanged sections verbatim, bumps the version, and appends to the changelog. Use when the user asks to update, modify, promote, or resolve open questions in an existing PRD.
license: MIT
---

# PRD Update Workflow

You are updating an existing PRD. A PRD is a living document during build — open questions get answered, scope shifts, edge cases get discovered. Your job is to keep it in sync without losing history.

Updating a PRD preserves the history: bump the version, append to the changelog, and **keep unchanged sections verbatim** — do not reword things that didn't need to change.

## Required Companion Skills

This workflow references three knowledge skills in the same plugin:

- **`prd-conventions`** — status lifecycle, folder mapping, file naming
- **`prd-template`** — section structure (so you know what's preserved vs. edited)
- **`prd-quality`** — used to self-validate after the update

Read each one as you need it.

## Process

### 1. Resolve conventions and read the PRD

Read `.prdrc.json` at the repo root to know the configured `statusLifecycle` and `statusFolders` mapping (apply `prd-conventions` defaults if absent). Then read the existing PRD file. Confirm it's a valid PRD (header block matches the template).

If the user didn't provide a path, ask for it.

### 2. Identify which flow applies

There are three flows. Ask the user if it's ambiguous:

- **Flow A — Resolving open questions** (most common during build): "we answered Q3", "update the open questions"
- **Flow B — Scope or content change**: new edge case, discovered dependency, scope cut, scope addition, new stakeholder
- **Flow C — Status promotion**: "ready for review", "approved", "shipped" (or whatever statuses the lifecycle defines)

### 3. Execute the matching flow

---

#### Flow A — Resolving open questions

1. List the current open questions to the user, numbered.
2. Ask which ones now have answers.
3. Update each resolved `**Answer:** TBC` to `**Answer:** [resolved answer + reasoning]`.
4. **Keep the question** — it's the decision log. Never delete answered questions.
5. If the user's answer reveals a new question, add it.
6. Bump version: minor (`0.1 → 0.2`), or to `1.0` if all critical questions are resolved and the PRD is ready to be Approved.
7. Update the Date field to today.

---

#### Flow B — Scope or content change

1. Ask: *"Walk me through what's changed. I'll slot it into the right sections."*
2. Identify which sections need editing. Common patterns:
   - New edge case → add to Edge Cases
   - Discovered dependency → add to Dependencies (create the section if missing)
   - Scope reduction → move item from Proposed Solution to Out of Scope
   - Scope addition → push back first: *"Is this a separate PRD?"* If it's genuinely in scope, add to Proposed Solution
3. **Preserve unchanged sections verbatim.** Do not reword for style.
4. Bump version:
   - Minor (`0.1 → 0.2`) for additions / clarifications
   - Major (`0.x → 1.0` or `1.x → 2.0`) for scope changes that meaningfully change the engineering effort
5. Update the Date field.

**Special rule for Data Model Changes**: if this update touches a Data Model Changes section (or adds one), ensure it opens with the verbatim "illustrative names" note from `prd-template`. If a pre-existing section is missing the note, add it as part of the update and mention this in the changelog. This is the one cosmetic change that overrides the "preserve verbatim" rule, because its absence creates a real risk of engineering treating names as prescriptive.

---

#### Flow C — Status promotion

1. Read the configured `statusLifecycle` from `.prdrc.json` (default `Draft → In Review → Approved → Shipped`).
2. Run a health check before promoting:
   - **Earliest → next** (e.g. Draft → In Review): any required sections empty? Surface them. Don't block — the user can promote anyway after acknowledging.
   - **Mid → near-final** (e.g. In Review → Approved): any open questions still `TBC` that look load-bearing? Flag them.
   - **Final state** (e.g. Approved → Shipped): confirm with the user.
3. Update the Status field.
4. Bump version: to `1.0` on first promotion past the initial draft state (if currently `0.x`); else minor.
5. Update the Date field.
6. **If `statusFolders` is configured and the new status maps to a different folder**, perform the file move:
   - Write the PRD to the new path
   - Ask the user to delete the old file themselves — **do not delete files yourself unless explicitly authorised**

---

### 4. Append to the Changelog

Add an entry at the bottom of the PRD (above the footer):

```markdown
## Changelog

### Version 0.2 — 2026-05-18
- Resolved Q3 (rate limit per-tenant decision)
- Added new edge case for offline-then-reconnect flow
- Status: Draft → In Review

### Version 0.1 — 2026-05-12
- Initial draft
```

Always include: version, date, what changed, and any status transition.

### 5. Surface unresolved items from the previous version

After applying the update, mention any:

- Placeholders that have never been resolved (`[PLACEHOLDER]`)
- Open questions still `TBC` that have been outstanding for multiple versions
- Stakeholders named but never weighed in

These aren't blockers, just things the user should be aware of.

### 6. Save the update

Choose output mode:

- **Edit in place** (default for Flow A and Flow B) — apply the changes to the existing file
- **Save as new version** (e.g. `[feature-name]-v2.md`) — for major rewrites or when the user wants to preserve the previous version
- **Move file** (Flow C, final status only, if `statusFolders` defines a destination)

Ask the user before choosing if it's ambiguous.

### 7. Self-validate

Read the updated PRD. Apply the five-dimension check from `prd-quality`. Report status (PASS / CONDITIONAL / FAIL) with a one-sentence decision-readiness judgement.

### 8. Report

```
PRD updated at [path].

Changelog entry:
[verbatim entry just added]

Validation: [PASS / CONDITIONAL / FAIL] — [decision readiness]
```

## Constraints

- **Do not silently rewrite sections that haven't changed.** Authors trust that "an update for new edge cases" doesn't also reword the Problem Statement.
- **Do not delete answered open questions.** Their answers are the decision log.
- **Do not bump major version for minor changes.** A new edge case is not v2.0.
- **Do not skip the changelog.** It is the most useful artefact for users tracking what changed during build.
- **Do not auto-promote status.** Status advancement is a deliberate human action — confirm before writing the new Status.
- **Do not delete the old file** when moving to a new status folder. Save the new file and ask the user to delete the old one explicitly.
- **Do not ignore `.prdrc.json`** — folder moves on status promotion must respect the configured `statusFolders` mapping.

## Special Cases

### Open question never gets answered

If a question has been `TBC` for multiple updates, surface it: *"Q4 has been outstanding since v0.1. Is this still relevant, or can we close it out (decide either way, or drop it)?"*

### Scope grows past one feature

If the user keeps adding scope, push back: *"This is starting to feel like two features. Want me to spin off the second half into its own PRD?"* Better to have two clean PRDs than one bloated one.

### PRD references a non-existent linked doc

If a header link field points to a path that doesn't exist, surface it: *"The linked doc isn't at the path in the header — should I update the path, or is it in a different state?"*

### Promoting with unresolved load-bearing questions

If the user wants to advance Status but there are critical `TBC` open questions, flag them. Don't block — confirm the user really wants to proceed.
