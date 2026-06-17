---
name: prd-template
description: The PRD template and section structure used by the prd-drafter agent. Defines the canonical sections, when each one is required vs optional, and how to phrase open questions for AI-readable downstream consumption. Loaded by every drafter/updater/validator agent in this plugin.
version: 1.0.0
tags: [prd, product, template]
---

# PRD Template

## Purpose

The PRD (Product Requirements Document) is the source of truth for what we want to implement and why. Its job is to:

1. Make the feature clear enough that an engineer can pick it up and build it without re-asking the same questions.
2. **Surface unknowns, challenge assumptions, and force trade-off decisions before implementation begins** — this is the most important job of the PRD.
3. Be a stable reference during implementation, code review, and post-launch retrospectives.

A PRD is not a marketing document, a project plan, or a design spec. It is a contract between Product and Engineering about what is being built.

## When to Use

- A new feature is being scoped by Product
- A user request needs to be turned into something engineering can build
- A spike or discovery effort has produced enough signal to formalise

## When NOT to Use

- For tiny bug fixes or single-line copy changes — overkill
- For pure refactors with no user-visible change — use an ADR instead
- For internal process changes — use a runbook or process doc

## Required Sections

These appear in **every** PRD, regardless of feature type:

1. **Header** — feature name, status, author, date, version
2. **Problem Statement** — what problem, who experiences it, why now
3. **Goal** — what success looks like once shipped
4. **User Stories** — `As an X, I want to Y, so that Z`
5. **Proposed Solution** — high-level description of how the feature addresses the problem
6. **Edge Cases** — what happens when things go wrong, unusual inputs, race conditions, empty states
7. **Out of Scope** — what is explicitly NOT being built (just as important as what IS)
8. **Open Questions** — `**Question:** ... / **Answer:** ...` pairs, with `TBC` for unresolved

## Conditional Sections

Include these **only when relevant**. The drafter should make the judgement call based on the feature, not include them by default:

| Section | Include when |
|---|---|
| **Success Metrics** | The feature has a measurable outcome (adoption, conversion, error rate, time-to-X). Skip for one-off internal tools where success = "it works". |
| **User Impact / Audience** | The feature is user-facing and the audience is not the obvious default (e.g. "admins only", "tenant owners", "external API consumers"). |
| **Feature Flag Strategy** | The feature is user-visible AND has rollout risk (large user impact, irreversible data changes, multi-tenant blast radius). Skip for purely backend changes invisible to users, internal-only tools, or trivially reversible changes. |
| **Dependencies** | The feature relies on other features, services, tables, vendors, or external APIs not already in scope. |
| **Data Model Changes** | The feature requires new tables, new columns, schema migrations, or significant changes to existing data shapes. |
| **Permissions & Access Control** | The feature touches who can see or do what — especially relevant for multi-tenant or role-based products. |
| **Migration / Backfill** | Existing data needs to be migrated, backfilled, or transformed for the feature to work. |
| **Telemetry & Observability** | New metrics, logs, alarms, or dashboards are needed beyond standard request logging. |
| **Stakeholders** | More than two people need to weigh in (e.g. cross-team feature, customer-driven request, ops involvement). |
| **Design References** | A design file, prototype, or mock-up exists. Link to it; do not paste images into the PRD. |
| **Risks & Mitigations** | The feature has real-world risks beyond "it might have bugs" — e.g. data loss, customer escalation, compliance, regression in a sensitive area. |

If a conditional section does not apply, **omit it entirely** rather than writing "N/A". A PRD with eight tight sections beats one with fifteen padded sections.

## Section Specifics

Most conditional sections are self-explanatory from the trigger column. A few have specific formatting requirements:

### Data Model Changes

When this section is included, it must open with the following note, verbatim, before any table or column names appear:

```markdown
## Data Model Changes

> **Note:** Any table names, column names, types, or schema shapes referenced below are illustrative — used here so the PRD can describe the change concretely. They are **not prescriptive**. Engineering should name tables and columns following the project's existing data conventions and is free to deviate from anything in this document without it being treated as a scope change. If the *shape* of the data needs to change, that's a PRD update; if only the *names* change, that's an engineering decision.
```

Then describe the change in whatever form is clearest — bullet list, prose, or a sketch table. Examples:

```markdown
- A new table to store delivered notification events, keyed by tenant + user + timestamp
- Columns to capture: who acknowledged, when, and the ack channel (email, in-app, SMS)
- A foreign key from this table back to the existing users table
```

or, if a sketch table is clearer:

```markdown
| Table (illustrative) | Columns (illustrative) | Notes |
|---|---|---|
| `notification_events` | `id, tenant_id, user_id, raised_at, severity` | one row per event |
| `notification_acks` | `id, event_id, user_id, acked_at, channel` | new — captures acknowledgements |
```

The note must always be present when the section is included, even if the section is short. Engineers should be able to read the section and know the shape is locked but the names are theirs.

## Open Questions — The Critical Section

The Open Questions section is the single most important part of the PRD. It is where:

- Assumptions get challenged before code is written
- Trade-offs get surfaced for stakeholders to decide
- Ambiguity becomes explicit instead of silently propagating

### Format

Every open question must be a `**Question:**` / `**Answer:**` pair. This format is optimised for AI readability — when this PRD is loaded as implementation context, the engineer (or coding agent) can parse it cleanly.

```markdown
**Question:** When a user cancels mid-billing-cycle, do we pro-rate or end-of-period?
**Answer:** End-of-period. Stripe handles this automatically; pro-rating adds complexity for no customer-perceived benefit at this price point.

**Question:** What happens to in-flight uploads when a user deletes their account?
**Answer:** TBC

**Question:** Should admins be able to override the rate limit per-tenant?
**Answer:** TBC — pending decision from the platform lead, see Slack thread linked in header.
```

### Sourcing Open Questions

The drafter should actively look for open questions throughout the conversation. Good sources:

- The user said "I think..." or "probably..." or "we should..." — anything hedged is a candidate
- An edge case was raised but no resolution was given
- A dependency is implied but not confirmed (e.g. "this needs to integrate with X" — has X been built?)
- A stakeholder was named but hasn't actually been consulted
- The implementation has two reasonable approaches and no clear winner
- A metric was implied but no target was set ("we want to improve conversion" — by how much?)

### Resolving Open Questions

When the user answers an open question in the conversation, the drafter should:
1. Update the `**Answer:**` line from `TBC` to the resolved answer
2. Keep the question — it documents the decision and its reasoning for future readers
3. If the answer reveals a new question, add the new question too

**Do not delete answered questions.** They become the decision log.

## Header Block

Every PRD starts with this header, immediately after the title. Fields are populated based on `prd-conventions` (which reads `.prdrc.json` for the configured `headerLinkFields` and whether the repo uses projects):

```markdown
# [Feature Name] PRD

**Status:** Draft | In Review | Approved | Shipped
**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Version:** [Major.Minor]
```

If the repo's `.prdrc.json` defines `projects`, also add:

```markdown
**Project:** [project slug from config]
```

If `.prdrc.json` configures `headerLinkFields`, add one row for each configured value. With no config, do not add Linear, Figma, or any other extra header rows:

```markdown
**[Configured header field]:** [link or N/A]
```

`Status` ladders cleanly along the configured `statusLifecycle` (default: `Draft → In Review → Approved → Shipped`). When status moves to Shipped, the file moves to the shipped folder (if `statusFolders` is set) — see `prd-conventions`.

## Output Skeleton

```markdown
> **PRD — Source of Truth for Implementation**
>
> The purpose of this document is to make it clear what feature we want to implement and to surface unknowns, challenge ideas, discuss approaches and assumptions so that we can use this as a source of truth for implementation.

# [Feature Name] PRD

**Status:** Draft
**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Version:** 0.1
[Optional: **Project:** ...]
[Optional: header link fields per .prdrc.json]

## Problem Statement
[What problem, who experiences it, why now.]

## Goal
[What success looks like once shipped.]

## User Stories
1. As a [role], I want to [action], so that [outcome].

## Proposed Solution
[High-level description.]

[... conditional sections as relevant ...]

## Edge Cases
- [Case 1]
- [Case 2]

## Out of Scope
- [Thing 1]
- [Thing 2]

## Open Questions

**Question:** [...]
**Answer:** TBC

**Question:** [...]
**Answer:** [Resolved answer, with reasoning]

---

*PRD drafted using the `prd-drafter` plugin. Last updated [DATE].*
```

## Best Practices

- **Specific beats vague.** "Users see an error toast within 200ms" beats "fast feedback".
- **Numbered or bulleted user stories**, not paragraphs.
- **One reader test**: could an engineer who wasn't in the original meeting pick this up and build it? If no, the PRD is incomplete.
- **Cross-reference, don't duplicate.** If there's an existing ADR for the auth pattern, link to it. Don't restate it.
- **Keep the PRD living during build.** When an open question gets answered in implementation, update the PRD — don't let it diverge.

## Common Mistakes

- **Including every conditional section "for completeness".** A PRD bloated with "N/A" sections trains readers to skim.
- **Vague open questions** like "How should we handle errors?" — these are not questions, they are reminders. Real questions are specific enough to have a binary or short-list answer.
- **Hiding the actual problem behind solution-language.** "We need a notification system" is not a problem statement; "Users are missing critical events because they only check the dashboard manually" is.
- **Mixing PRD and feature spec.** The PRD is *what and why*. Detailed UI states, error message copy, and exact API shapes belong in the implementation spec or design hand-off.
- **Forgetting Out of Scope.** Without it, scope creeps. Always list 2–4 things that are explicitly NOT in this feature.
- **Treating Open Questions as a TODO list.** They are the decision log — answered questions stay, with the answer recorded for future readers.
