---
name: review-security-privacy
description: Review a PR for security and privacy risks such as authorization bypasses, injection, secret exposure, unsafe logging, and unnecessary personal data handling.
license: MIT
---

# Review Security And Privacy

Use this pass to catch risks that could expose data, weaken access control, or create abuse paths.

## What To Look For

- Authorization checks moved, removed, or applied after data is fetched
- Tenant, workspace, organization, or account boundary mistakes
- Authentication assumptions that trust client-provided identity or role data
- SQL, command, path, template, LDAP, or query injection
- Cross-site scripting, open redirect, CSRF, SSRF, or unsafe URL handling
- Secrets, tokens, credentials, keys, or cookies logged or returned
- Personal data added to logs, analytics, events, errors, or support payloads
- Over-broad data selection where narrower fields would do
- Unsafe deserialization or parsing of untrusted input
- Dependency additions that touch auth, crypto, parsing, network, or sandboxing
- Security-sensitive feature flags with insecure defaults

## How To Comment

Be specific and calm. Explain the risk without over-explaining exploit steps.

Good:

```text
This needs to keep the tenant check before returning the record. As written, a user who knows another record ID could read data outside their tenant.
```

Good:

```text
Could we avoid logging the raw email payload here? It can include access tokens and customer PII, and the error ID should be enough to debug this path.
```

Good:

```text
I might be missing a sanitizer upstream, but this value appears to come from user input and then gets rendered as HTML. Could we either escape it here or point to the place that guarantees it is safe?
```

## Severity

- `blocker` for likely access-control bypass, credential exposure, injection, or PII leakage
- `concern` for unclear boundaries or missing safeguards
- `question` when a sanitizer or authorization guarantee may exist elsewhere

Never include detailed exploit instructions beyond what the author needs to understand and fix the issue.
