---
name: prd-quality
description: Quality checks for a drafted PRD. Defines structural completeness, open-question hygiene, common anti-patterns, and the validator's scoring rubric. Loaded by the prd-validator agent.
version: 1.0.0
tags: [prd, quality, validation]
---

# PRD Quality Checks

## Purpose

A PRD is only valuable if it is actually readable, technically grounded, and surfaces the right unknowns. This skill defines the validator's checklist — what makes a PRD ready to hand to engineering vs. needing more work.

## When to Use

- Loaded by the `prd-validator` agent
- Referenced after any drafter or updater finishes
- Triggered explicitly by `/prd-drafter:validate`

## Quality Dimensions

The validator checks five dimensions, in order:

### A. Structural Completeness

Required sections present?

| Section | Required | Notes |
|---|---|---|
| Header (Status, Author, Date, Version) | ✅ always | Plus Project if `.prdrc` defines projects; plus configured header link fields |
| Problem Statement | ✅ always | Non-empty, specific (not "improve the experience") |
| Goal | ✅ always | Describes outcome, not output |
| User Stories | ✅ always | At least one, in `As an X, I want Y, so that Z` form |
| Proposed Solution | ✅ always | Non-empty |
| Edge Cases | ✅ always | At least one — or explicit "No edge cases identified" with reasoning |
| Out of Scope | ✅ always | At least one — or explicit "Nothing notable out of scope" with reasoning |
| Open Questions | ✅ always | Section present, even if all resolved |

Conditional sections (must be present **when triggered** — see `prd-template`):

| Section | Trigger |
|---|---|
| Success Metrics | Feature has measurable outcome |
| Feature Flag Strategy | User-visible AND has rollout risk |
| Data Model Changes | Schema changes needed |
| Permissions & Access Control | Touches access/visibility |
| Dependencies | Relies on other features/services/vendors |
| Migration / Backfill | Existing data must be migrated |
| Telemetry & Observability | New metrics/logs/alarms needed |
| Stakeholders | More than two people need to weigh in |
| Design References | Design file, prototype, or mock-up exists |
| Risks & Mitigations | Real risks beyond "might have bugs" |

The validator flags a missing conditional section only when it has evidence the trigger is met (e.g. PRD mentions "new tables" but no Data Model Changes section).

### B. Open Question Hygiene

This is the most important quality dimension. A PRD with no open questions is suspicious — either the feature is trivial, or assumptions are being hidden.

Checks:

1. **Format check** — every open question uses `**Question:** ... / **Answer:** ...` pairs. No bare questions, no missing answers.
2. **TBC count** — how many questions are still unresolved? Surface this prominently.
3. **Vagueness check** — flag questions that are too vague to be answerable:
   - ❌ "How should we handle errors?"
   - ✅ "When the upload fails after 3 retries, do we keep the partial data or roll back?"
4. **Empty section warning** — if Open Questions is empty, surface a soft warning. It's allowed, but rare and worth confirming.

### C. Specificity & Grounding

Flag language that is too vague to act on:

| Vague | Better |
|---|---|
| "Make it fast" | "Response time under 500ms p95" |
| "Improve the UX" | "Reduce clicks-to-completion from 5 to 2" |
| "Better error handling" | "Show a toast within 200ms; retry button in the toast" |
| "Notify the user" | "Email + in-app banner; throttle to 1/day" |
| "Scalable" | "Supports 10× current write load without re-architecting" |

The validator lists 3–5 of the most vague phrases and suggests sharpening, but does not block PASS for this — it's a CONDITIONAL flag.

### D. Internal Consistency

Cross-section contradictions to catch:

1. Problem says "users can't see X" but Goal says "improve discoverability of Y" — mismatched.
2. Out of Scope lists something that the Proposed Solution then describes.
3. User Stories describe a flow that the Edge Cases section never covers.
4. Dependencies mention service X, but the answers to Open Questions assume X behaves a different way.
5. Conditional section is included but trivially empty (e.g. Success Metrics section says "TBD" with no further detail).

### E. Decision Readiness

The litmus test: **could an engineer pick this up and start work without asking the author follow-ups beyond the explicit Open Questions?**

The validator does not run this check programmatically, but produces a short narrative judgment at the end:

> *Decision readiness:* High / Medium / Low — with one sentence of reasoning.

## Status Computation

After all checks, the validator computes a single status:

| Status | Criteria |
|---|---|
| **PASS** | All required sections present and non-empty. No format issues. Open Questions section has well-formed questions (TBC is fine — that's expected). Decision readiness Medium or High. |
| **CONDITIONAL** | Required sections present, but specificity concerns OR open questions are vague OR a triggered conditional section is missing. Document is usable but should be tightened. |
| **FAIL** | A required section is missing or empty. Open Questions section is malformed. There is an internal contradiction the author should resolve before engineering picks it up. |

Important: **TBC open questions do NOT lower the status.** They are expected. A PRD with 8 open questions is not worse than one with 0 — provided the questions are well-formed.

## Validator Output Format

```markdown
## PRD Validation Report

**PRD:** [Title]
**Project:** [from header, or "n/a" if repo is single-project]
**Version:** [from header]
**Status:** [PASS / CONDITIONAL / FAIL]
**Decision readiness:** High / Medium / Low

### Structural Completeness

| Section | Present | Notes |
|---|---|---|
| Header | ✅ | |
| Problem Statement | ✅ | |
| Goal | ✅ | |
| User Stories | ✅ | 3 stories |
| Proposed Solution | ✅ | |
| Edge Cases | ✅ | 4 cases |
| Out of Scope | ✅ | 3 items |
| Open Questions | ✅ | 6 total, 2 TBC |
| *(triggered conditional sections)* | | |
| Success Metrics | ✅ | |
| Data Model Changes | ❌ | Proposed Solution mentions new `events` table — section missing |

### Open Question Hygiene

- Total questions: 6
- Unresolved (TBC): 2
- Vague (consider sharpening):
  - Q4: "How should we handle errors?" — recommend rephrasing to a specific failure mode

### Specificity Flags

- "Better performance" in Goal — quantify (target latency, target throughput, etc.)
- "Notify users" in Proposed Solution — specify channel and timing

### Consistency Issues

- [None] OR [List with section references]

### Recommended Next Actions

1. [Most important fix]
2. [Second]
3. [Third]

---

*Validation by `prd-validator`. This checks structural completeness and surface-level quality; it does not validate that the proposed solution is the right one — that is the job of stakeholder review.*
```

## What the Validator Does NOT Do

- **Does not pass judgement on whether the feature should be built.** That's stakeholder review, not validation.
- **Does not estimate effort or timeline.** That's engineering's job.
- **Does not check technical feasibility.** That's the engineer or architect who picks it up.
- **Does not certify the PRD as "approved".** Approval is a stakeholder action, not a validator action — moving status from Draft → In Review → Approved is a human decision.

## Best Practices for the Validator

- **Be specific in flagged issues.** Cite the section. "Goal is vague" is unhelpful; "Goal — 'improve UX' is not measurable, consider 'reduce X to Y'" is actionable.
- **Don't over-flag.** Pick the 3–5 most impactful issues. A 30-item list gets ignored.
- **Soft warnings vs hard fails.** Use ❌ for required sections missing; use ⚠️ for specificity/consistency soft flags.
- **Always end with the reminder:** validation checks structural completeness, not whether the feature is the right one.
