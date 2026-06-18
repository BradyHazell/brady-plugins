---
name: review-interesting-decisions
description: Review a PR for architectural, dependency, design, and implementation decisions that may be intentional but deserve a concise author question or alternative suggestion.
license: MIT
---

# Review Interesting Decisions

Use this pass to surface thoughtful questions, not accusations. The goal is to help the user ask the author about decisions that affect direction, complexity, or maintainability.

## What To Look For

- New library or framework use where existing code could solve the problem
- Architectural changes that introduce a new pattern beside an existing one
- Moving logic across module boundaries
- Choosing client-side versus server-side ownership for important behavior
- Adding sync work where async/background work may fit better, or vice versa
- Building generic infrastructure for a single narrow use case
- Removing indirection that may have protected a contract
- Feature flag, rollout, or migration decisions that imply a strategy not stated in the PR
- Code that duplicates a platform capability, helper, service, or domain model
- Decisions that may be correct but need a rationale for future readers

## Output Placement

- If the question belongs to a line, output it as an inline `question`.
- If the question applies to a file but not one line, put it under File-level questions.
- If the question applies to the overall design, put it under General questions.

## How To Ask

Use a soft, curious voice unless the trade-off is clearly risky.

Good:

```text
I might be missing the reason for introducing this package. Since we only use it for formatting one value, could we keep this on the existing helper unless there are more cases coming?
```

Good:

```text
Could you walk me through why this validation moved into the UI? Keeping it in the service layer seems like it would protect the API and the background import path too.
```

Good:

```text
Is the intent for this adapter to become the new pattern for all provider calls, or is it specific to this integration? If it is the new pattern, it may be worth naming that in the module/docs so future changes follow it.
```

Avoid:

```text
Why did you do this?
```

## Severity

Most output from this pass should be `question` or `suggestion`. Use `concern` only when the decision creates a concrete maintainability, compatibility, or operational risk.
