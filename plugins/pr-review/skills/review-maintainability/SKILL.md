---
name: review-maintainability
description: Review a PR for maintainability, repo conventions, best practices, unnecessary abstractions, dependency choices, and avoidable complexity without nitpicking style.
license: MIT
---

# Review Maintainability

Use this pass to keep the codebase easier to understand and change. Prefer local repo conventions over generic preferences.

## What To Look For

- New code that bypasses existing helpers, patterns, or abstractions without a clear reason
- Duplicate logic that will drift
- Overly broad abstractions for one call site
- Tight coupling between modules that are otherwise separate
- Business logic hidden in UI, handlers, config, or migration scripts
- Hard-coded values that should be named, configured, or derived
- Error messages or names that obscure the real behavior
- Large functions where a small extraction would clarify control flow
- Added dependencies for behavior the repo already implements simply
- Library choices that increase bundle size, security surface, or maintenance cost without enough benefit
- Best-practice issues that affect future safety, not personal style

## How To Comment

Point to the repo pattern or maintenance cost.

Good:

```text
Could we reuse `parseDateRange` here instead of adding a second parser? Keeping one path should make the timezone edge cases easier to maintain.
```

Good:

```text
I might be missing the reason for the new dependency, but this looks like it only replaces a small amount of existing helper logic. Could we avoid adding it unless we need more of the library?
```

Good:

```text
Could we keep the mapping close to the API adapter instead of the component? That matches the existing screens and keeps response-shape changes out of the view layer.
```

Avoid:

```text
I prefer a different style.
```

## Severity

- `concern` for maintainability issues that will likely cause bugs or churn
- `suggestion` for simpler structure or stronger alignment with local patterns
- `question` when the author may have had a good trade-off in mind
