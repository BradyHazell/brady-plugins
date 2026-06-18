---
name: review-tests
description: Review a PR for missing or weak test coverage tied to changed behavior, edge cases, regressions, and contract changes.
license: MIT
---

# Review Tests

Use this pass after understanding the behavior change. The goal is not to demand tests for everything. The goal is to catch meaningful risk that lacks coverage.

## What To Look For

- New branches or error paths with no test
- Bug fixes without a regression test
- Behavior changes where existing tests only cover the happy path
- Contract changes without integration, API, schema, or snapshot coverage
- Security or authorization changes without positive and negative cases
- Migration, serialization, parser, or date/time logic without edge cases
- UI state changes without tests for loading, empty, error, or disabled states
- Test updates that remove assertions instead of adapting them
- Test names or fixtures that no longer match the behavior

## How To Judge

Ask:

- What behavior changed?
- What would break if this were implemented incorrectly?
- Is there already nearby test coverage?
- Is the missing coverage important enough to mention?

If the repository has no clear test convention, phrase the comment as a question or put the command under Suggested local checks.

## How To Comment

Good:

```text
Could we add a regression test for the expired-token case? This path is the one that used to fall through, so a targeted test would make sure we do not reintroduce it.
```

Good:

```text
Should we cover both allowed and denied tenants here? The code now moves the tenant check into this helper, so a negative case would catch accidental bypasses.
```

Avoid:

```text
Needs tests.
```

## Severity

- `blocker` when missing tests cover security, data loss, migration safety, or a critical bug fix
- `concern` for meaningful uncovered behavior
- `suggestion` for useful but non-blocking coverage
