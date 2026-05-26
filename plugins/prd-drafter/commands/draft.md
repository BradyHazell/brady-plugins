---
description: Draft a new PRD (Product Requirements Document). Conversational discovery followed by structured drafting, with open questions surfaced explicitly. Saves to the path resolved by .prdrc.json (or ./prds/ by default).
argument-hint: [optional: short feature description, e.g. "alarm centre"]
---

# Draft a PRD

You are running the main entry point of the `prd-drafter` plugin. The user wants to draft a Product Requirements Document for a new feature.

## Your Process

1. **State the purpose up front:**

   > A PRD is a source of truth for implementation. The goal of this conversation is to surface unknowns, challenge assumptions, and produce a document an engineer could pick up and build from. Expect me to push back and ask "why" — that's the job.

2. **Check the conversation for existing context.**
   - If the user pasted a feature brief or partial PRD in the same message, read it. Skip to step 4.
   - If the user provided a short description as the command argument (e.g. "alarm centre"), use it as a starting point.
   - Otherwise, ask: *"What feature are we drafting a PRD for? A one-line description is enough to get started."*

3. **Confirm there is no existing PRD for this feature.** Briefly check the configured `outputPath` (read `.prdrc.json` if present; otherwise default to `./prds/`) for a file matching the proposed feature name. If one exists, ask whether the user wants to update it (use `/prd-drafter:update`) or start a new one.

4. **Invoke the `prd-interviewer` agent.** It will:
   - Read `.prdrc.json` and apply resolved conventions
   - Confirm which project the feature belongs to (only if `.prdrc.json` defines projects)
   - Walk the discovery phases (Problem → Scope → Edges → Conditional sections)
   - Surface open questions live
   - Produce a `## Feature Context` block

5. **Invoke the `prd-drafter` agent.** It will:
   - Read the Feature Context block
   - Ask any remaining clarifications (1–3 questions max)
   - Compose the PRD with all required sections and only the triggered conditional sections
   - Show the draft inline
   - Confirm the save path with the user and write the file

6. **Invoke `prd-validator`** on the saved PRD.

7. **Report**: file path, validation status, decision-readiness, count of open questions (and how many are TBC).

## What You Must Not Do

- Do not skip discovery just because the user described the feature in one sentence. The discovery is the point.
- Do not produce a PRD with no Open Questions section — even an empty one indicates the section is intentionally so.
- Do not invent project, author, or owner names. Ask.
- Do not save the PRD without confirming the path with the user.
- Do not skip the validator step.
