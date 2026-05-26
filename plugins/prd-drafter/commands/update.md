---
description: Update an existing PRD. Handles three flows — resolving open questions during/after build, scope/content changes, and status promotion through the configured lifecycle. Reads the PRD, asks targeted delta questions, and produces an updated version with a changelog.
argument-hint: <path-to-existing-PRD>
---

# Update an Existing PRD

The user wants to update an existing PRD. The path is in the command argument.

## Your Process

1. **State the disclaimer:**

   > Updating a PRD preserves the history. I'll bump the version, append to the changelog, and keep unchanged sections verbatim — I won't reword things that didn't need to change.

2. **Confirm the path.** If no argument was provided, ask the user for the path to the existing PRD.

3. **Invoke the `prd-updater` agent** with the path. It will:
   - Read `.prdrc.json` if present, to know the resolved status lifecycle and folder mapping
   - Read the existing PRD and confirm it's a valid PRD structure
   - Ask the user which update flow applies:
     - **A** — Resolving open questions (most common during build)
     - **B** — Scope or content change (new edge case, dependency, scope shift)
     - **C** — Status promotion (advance along the configured `statusLifecycle`)
   - Execute the flow-specific process from `prd-updater.md`
   - Preserve unchanged sections verbatim
   - Bump version (minor for additions, major for scope changes)
   - Update the Date field
   - Append to the Changelog
   - Surface any prior unresolved placeholders or long-outstanding TBCs

4. **Invoke `prd-validator`** on the updated PRD.

5. **Ask whether to**:
   - **Edit in place** (default for Flow A and B)
   - **Save as new version** (e.g. `alarm-centre-v2.md` — for major rewrites)
   - **Move to the configured final-status folder** (Flow C, status = final lifecycle state only)

6. **Report**: changelog entry, validation status, file path.

## What to Watch For

- **Scope creep.** If the user keeps adding to Proposed Solution rather than triggering a major version bump, push back: *"This is starting to feel like a v2.0 — want to bump the major version or split into a separate PRD?"*
- **Long-outstanding TBCs.** Surface questions that have been `TBC` for multiple versions. They may have been forgotten.
- **Promoting with unresolved load-bearing questions.** If the user wants to move Status to a near-final state but there are critical `TBC` open questions, flag them. Don't block — confirm the user really wants to proceed.
- **Final-status move.** For Flow C → final status, if `.prdrc.json` defines `statusFolders` with a destination folder for that status, the updater writes the new file to that folder. The user must delete the old copy themselves — the plugin will not delete files.
