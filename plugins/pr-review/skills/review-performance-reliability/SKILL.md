---
name: review-performance-reliability
description: Review a PR for performance, reliability, scalability, concurrency, observability, timeout, retry, and operational risks.
license: MIT
---

# Review Performance And Reliability

Use this pass for changes that affect latency, throughput, resource use, background processing, external calls, concurrency, or operational visibility.

## What To Look For

- N+1 queries or network calls
- Unbounded loops, recursion, pagination, memory use, or result sets
- Blocking work in request paths or UI render paths
- Expensive work repeated on every render, request, job, or poll
- Missing timeout, cancellation, retry, or backoff for external calls
- Retries that are not idempotent
- Locks, transactions, or concurrent updates that can deadlock or lose writes
- Job processing that cannot resume safely after partial failure
- Cache changes without invalidation or stale-data handling
- Observability gaps for new background jobs, external calls, or critical paths
- Feature rollout that lacks kill switch or degradation path

## How To Comment

Name the operational failure mode.

Good:

```text
Could we batch this lookup before the loop? This now makes one query per item, so larger exports can become much slower and put extra load on the database.
```

Good:

```text
Should this external call have a timeout and retry policy? Without one, a slow provider can hold the request open indefinitely.
```

Good:

```text
Could we make this job idempotent before enabling retries? If it fails after creating the invoice but before marking the task complete, the retry can create a duplicate.
```

## Severity

- `blocker` for likely data duplication, outage risk, runaway resource use, or unsafe retry behavior
- `concern` for scale or reliability risks that should be addressed before merge
- `suggestion` for useful hardening when the risk is moderate
