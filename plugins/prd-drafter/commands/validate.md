---
description: Validate a PRD for structural completeness, open-question hygiene, specificity, and internal consistency. Produces a validation report with a status (PASS / CONDITIONAL / FAIL) and a decision-readiness judgement.
argument-hint: [path-to-PRD]
---

# Validate a PRD

The user wants a PRD validated. The path is in the command argument, or the user just drafted one inline.

## Your Process

1. **Determine the source.**
   - If a path is provided in the argument, the validator will read the file.
   - If no path but a draft exists inline in the conversation, validate the inline draft.
   - If neither, ask the user for the path.

2. **Invoke the `prd-validator` agent.** It will:
   - Read `.prdrc.json` and resolve conventions
   - Read the PRD
   - Confirm it's a valid PRD (header block matches template)
   - Run the five quality checks (Structural Completeness, Open Question Hygiene, Specificity, Consistency, Decision Readiness)
   - Check filename and folder against the resolved conventions
   - Produce a structured validation report with a status (PASS / CONDITIONAL / FAIL)

3. **Display the report** to the user.

4. **If FAIL or CONDITIONAL**, recommend remediation:
   - **Missing required sections** → suggest re-running `/prd-drafter:draft` to extend, or edit directly
   - **Vague language** → suggest specific rephrasings inline (the validator should already have provided these)
   - **Missing triggered conditional sections** → suggest `/prd-drafter:update` to add them
   - **Filename or path issues** → suggest the corrected name per the resolved conventions
   - **Open question format issues** → suggest the `**Question:** ... / **Answer:** ...` pair format

5. **Always end with the reminder**, regardless of status:

   > Validation checks structural completeness and surface-level quality. It does not validate that the proposed feature is the right thing to build — stakeholder review still owns that question.

## What You Must Not Do

- Do not modify the PRD during validation. The validator is read-only.
- Do not certify the PRD as "approved" or "ready to ship". Approval is a human stakeholder decision.
- Do not lower the validation status because there are `TBC` open questions. TBC is healthy.
- Do not skip the decision-readiness narrative judgement — it is the most useful signal for the user.
