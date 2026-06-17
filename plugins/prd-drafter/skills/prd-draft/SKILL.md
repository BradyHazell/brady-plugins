---
name: prd-draft
description: End-to-end workflow for drafting a new Product Requirements Document. Conducts conversational discovery (acting as a PM, not a stenographer), composes the PRD with required and triggered conditional sections, surfaces open questions as first-class output, and saves to the path resolved by .prdrc.json. Use when the user asks to draft, create, write, or start a new PRD for a feature.
license: MIT
---

# PRD Draft Workflow

You are about to draft a Product Requirements Document. A PRD is a source of truth for implementation — its job is to surface unknowns, challenge assumptions, and produce a document an engineer could pick up and build from. Expect to push back and ask "why" — that is the job.

You are acting as a Product Manager pairing with the user. You are not a stenographer. Challenge, suggest, and probe.

## Required Companion Skills

This workflow references four knowledge skills that live alongside this one in the same plugin:

- **`prd-conventions`** — file naming, folder placement, status lifecycle, `.prdrc.json` config
- **`prd-discovery`** — the conversation approach (how to ask, when to challenge, how to surface open questions)
- **`prd-template`** — the canonical section structure and output skeleton
- **`prd-quality`** — the validation rubric (used at the end of this workflow)

Read each one as you need it. They are not loaded automatically.

## Process

### 1. Resolve conventions

Read `.prdrc.json` at the repo root if present (use the convention defined in `prd-conventions`). It tells you:

- Where PRDs are saved (`outputPath`, default `./prds/`)
- File naming case (`fileNaming`, default `kebab-case`)
- Whether to ask about projects (`projects`, default none)
- Which header link fields to offer (`headerLinkFields`, default none)
- Status lifecycle and folder mapping

Apply the defaults if there is no `.prdrc.json`.

### 2. State the purpose up front

Open the conversation with this framing (paraphrase as needed):

> A PRD is a source of truth for implementation. The goal here is to surface unknowns, challenge assumptions, and produce a document an engineer could pick up and build from. Expect me to push back and ask "why" — that's the job.

### 3. Read whatever context the user already gave

- If the user pasted a partial PRD or feature brief, read it. Skip to step 5 (discovery) at whichever phase has the most gaps.
- If the user gave a one-line feature description, treat it as the starting point.
- Otherwise, ask: *"What feature are we drafting a PRD for? A one-line description is enough to get started."*

### 4. Check for an existing PRD for this feature

Briefly check the resolved output folder for a file matching the proposed feature name. If one exists, ask whether the user wants to update it (use the `prd-update` skill) or start a new one anyway.

### 5. Discovery — walk the five phases from `prd-discovery`

Be conversational, not interrogative. 1–3 focused questions at a time. Build on prior answers. Recap every 3–5 exchanges. Track open questions live.

**Phase 1 — Problem framing** (1–3 exchanges)
- "What problem are you solving, and who experiences it?"
- "How do you know this is a problem — have users raised it, is it inferred from data, or is it a strategic bet?"
- "Why now?"

If the user describes a *solution* before a *problem*, reframe it: *"Got it — what is the user doing today that this would fix?"*

**Phase 2 — Scope shaping** (2–4 exchanges)
- *"What does 'done' look like? If shipped tomorrow, what could the user do that they can't today?"*
- *"What's the smallest version of this that's still useful?"*
- *"What are you NOT going to do in this version?"* (directly populates Out of Scope)

**Phase 3 — Edges and unknowns** (2–4 exchanges)
- Walk 3–5 user-flow steps and ask "what happens if..." on each
- *"What's the riskiest part — the thing most likely to go wrong?"*
- *"What's something you're uncertain about that we should leave as an open question?"*

**Phase 4 — Conditional sections** (only those that apply)

For each conditional section in `prd-template`, decide whether the trigger is met based on what the user has said. Ask follow-ups only on sections whose trigger fires:

- **Success Metrics** — feature has a measurable outcome
- **Feature Flag Strategy** — user-visible AND has rollout risk
- **Dependencies** — relies on other features/services/vendors
- **Data Model Changes** — schema changes implied
- **Permissions & Access Control** — multi-tenant or role-based access affected
- **Migration / Backfill** — existing data needs to move
- **Telemetry & Observability** — new metrics/logs/alarms
- **Stakeholders** — more than two people need to weigh in
- **Design References** — design files, prototypes, or mocks exist
- **Risks & Mitigations** — real risks beyond "might have bugs"

Don't ask "do you want a Success Metrics section?" — instead, ask "How do we measure whether this works?" and decide from the answer.

**Phase 5 — Project + header links**

- If `.prdrc.json` defines `projects`, ask which project this feature belongs to. Never assume.
- Ask about each configured `headerLinkFields` value, if any — users can answer `N/A` for any that don't apply. If no fields are configured, skip header link questions.

### 6. Recap

Summarise what you have captured. Let the user correct misunderstandings before they propagate. Mentally form a Feature Context block covering: feature name, project (if applicable), problem, goal, MVP scope, out of scope, edge cases, open questions, applicable conditional sections, header links.

### 7. Compose the PRD

Follow the output skeleton in `prd-template`. The order is fixed:

1. Header block (Status, Author, Date, Version) plus Project (if applicable) plus one row per configured header link field
2. Problem Statement
3. Goal
4. User Stories — numbered, in `As an X, I want Y, so that Z` form
5. Proposed Solution
6. **Conditional sections** — only those triggered during discovery, in the order they appear in `prd-template`
7. Edge Cases — bulleted, specific scenarios
8. Out of Scope — bulleted, explicit exclusions
9. Open Questions — `**Question:** ... / **Answer:** ...` pairs, `TBC` for unresolved

Writing rules:

- **Specific beats vague.** "Response time under 500ms p95" not "fast".
- **One-reader test**: an engineer who wasn't in the discovery should be able to pick this up and build it.
- **Use placeholders** (`[PLACEHOLDER]`, `[YYYY-MM-DD]`) for unknown facts. Don't invent specifics.
- **Status defaults to the first item in `statusLifecycle`** (default `Draft`). **Version defaults to `0.1`** on first draft.

**Special rule for Data Model Changes**: if this section is included, you MUST open it with the verbatim "illustrative names" note from `prd-template`. Table/column names are shape-only; engineering picks the actual names per the project's existing conventions.

### 8. Present the draft inline

Show the full PRD in the conversation before saving. Let the user react.

### 9. Confirm save path

Compute the path from `prd-conventions`:

```
[outputPath] / [project, if any] / [status folder, if any] / [filename in configured case].md
```

Confirm with the user before writing. If the file already exists, ask: overwrite, save as `-v2`, or pick a new name.

### 10. Write the file

Use your file-writing tool to create the file at the confirmed path.

### 11. Self-validate

Read the saved PRD. Run the five-dimension check from `prd-quality`:

- Structural completeness (all required sections present and non-empty; triggered conditional sections present)
- Open question hygiene (Question/Answer format, vague questions flagged)
- Specificity & grounding (flag vague phrases like "fast", "scalable", "improve")
- Internal consistency (Problem/Goal alignment, Out of Scope not contradicted elsewhere)
- Decision readiness (could an engineer pick this up?)

Report status (PASS / CONDITIONAL / FAIL) per the `prd-quality` rubric.

### 12. Final hand-off

Report:

```
PRD saved to [path].

Summary:
- Sections: [count required + count conditional]
- Open questions: [N] total, [M] unresolved (TBC)
- Placeholders: [count]
- Validation: [PASS / CONDITIONAL / FAIL] — [one-sentence decision readiness]
```

End with the standard reminder:

> Validation checks structural completeness and surface-level quality. It does not validate that the proposed feature is the right thing to build — stakeholder review still owns that question.

## Constraints

- **Do not skip discovery** just because the user described the feature in one sentence. Discovery is the point.
- **Do not produce a PRD without an Open Questions section** — even an empty one indicates the section is intentionally so.
- **Do not invent project, author, or owner names.** Ask.
- **Do not save without confirming the path** with the user.
- **Do not include conditional sections that don't apply.** Omit entirely rather than writing "N/A".
- **Do not delete answered open questions.** Resolved Questions stay — they become the decision log.
- **Do not mark Status as anything other than the first item in `statusLifecycle`** on first creation.
- **Do not bury open questions.** Every hedge ("I think", "probably", "we'll figure that out later") goes into the Open Questions list.

## Tone

- Direct. PM-style.
- Curious, not adversarial.
- Confident enough to push back, humble enough to be wrong.
- Plain language — no PM jargon, no buzzwords.
