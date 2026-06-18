---
name: review-obvious-issues
description: Review a PR diff for likely correctness bugs and behavior regressions, focusing on changed lines and concrete failure modes rather than style preferences.
license: MIT
---

# Review Obvious Issues

Use this pass first. Look for issues that could break behavior, corrupt data, or produce user-visible failures.

## What To Look For

- Null, undefined, empty, or missing-value cases introduced by the change
- Incorrect conditionals, inverted logic, off-by-one errors, and dead branches
- Async mistakes: missing `await`, unhandled promises, races, cancellation gaps
- Error handling that swallows failures or turns recoverable errors into crashes
- State transitions that can skip required validation
- Data mapping mistakes: wrong field, wrong unit, wrong timezone, wrong enum
- Resource leaks: file handles, subscriptions, timers, sockets, listeners
- Incorrect defaults or configuration fallback behavior
- Changes that bypass validation, authorization, or existing guardrails
- Generated or build artifacts changed unintentionally

## How To Comment

Anchor to the changed line whenever possible. State the concrete failure mode.

Good:

```text
Could we handle `items` being undefined here? This will throw before the empty-state branch can render.
```

Good:

```text
This looks like it flips the old condition. Should this still block inactive accounts before creating the session?
```

Avoid:

```text
This code seems bad.
```

## Severity

- `blocker` for likely runtime errors, data corruption, security bypasses, or broken user flows
- `concern` for meaningful edge cases or ambiguous behavior
- `suggestion` for small correctness hardening that is not likely to block merge

If the behavior may be intentional, make it a question.
