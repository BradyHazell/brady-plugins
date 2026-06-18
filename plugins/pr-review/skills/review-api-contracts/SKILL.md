---
name: review-api-contracts
description: Review a PR for API, schema, persistence, event, and compatibility contract issues that could break callers, data, integrations, or rollout safety.
license: MIT
---

# Review API And Contracts

Use this pass when a PR changes externally consumed behavior, persistence shape, events, schemas, queues, commands, routes, public functions, feature flags, or configuration.

## What To Look For

- Request or response shape changes without versioning or compatibility handling
- Changed status codes, error codes, error bodies, or retry semantics
- Removed fields, renamed fields, changed nullability, or changed enum values
- Database migrations that are not backwards compatible with deployed code
- Event payload changes that can break downstream consumers
- Queue or job changes that are not idempotent or cannot handle old payloads
- Cache key changes without invalidation or fallback
- Feature flag defaults that expose incomplete behavior
- Config changes without defaults, docs, or rollout sequencing
- Public helper or library API changes that break internal callers
- Serialization/deserialization changes that cannot read old data

## How To Comment

Tie the comment to the contract and the consumer.

Good:

```text
Could we keep accepting the old `status` value during rollout? Existing queued jobs can still contain it, and this branch will reject them after deploy.
```

Good:

```text
This response field looks like it changed from nullable to required. Do we need a compatibility fallback for older clients that do not send it yet?
```

Good:

```text
Should this migration be split into expand and contract steps? Dropping the column in the same deploy can break older app instances that are still reading it.
```

## Severity

- `blocker` for breaking contracts, unsafe migrations, or data incompatibility
- `concern` for rollout sequencing risks
- `question` for unclear compatibility decisions
- `suggestion` for documentation or naming that would prevent misuse
