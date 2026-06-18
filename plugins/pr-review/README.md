# pr-review

`pr-review` reviews a pull request from a PR number or URL, fetches the diff from the repository you are running in, and drafts comments for the user to add manually.

It is designed for high-signal review comments: blockers, concerns, suggestions, missing tests, best-practice issues, security/privacy risks, API compatibility issues, performance/reliability concerns, and useful questions for interesting code decisions.

It never posts comments or submits a review.

## Usage

Review a PR number in the current GitHub repository:

```text
/pr-review:review 123
```

Review a PR URL:

```text
/pr-review:review https://github.com/org/repo/pull/123
/pr-review:review https://dev.azure.com/org/project/_git/repo/pullrequest/123
```

## Output

The output is built so you can copy individual comments into a PR:

````markdown
## Inline comments

### concern - src/example.ts

```diff
diff --git a/src/example.ts b/src/example.ts
@@
+ const items = response.items.map(toItem)
```

Comment:
Could we handle `response.items` being missing here? This will throw before the empty-state branch can render.
````

Questions that apply to a whole file appear under File-level questions. Questions that apply to the overall change appear under General questions.

## What It Reviews

- Obvious correctness issues and behavior regressions
- Missing or weak tests
- Security and privacy risks
- API, schema, persistence, event, and compatibility contracts
- Maintainability, local best practices, unnecessary dependencies, and avoidable complexity
- Performance and reliability risks
- Interesting code decisions that deserve author context

## Commands

| Command | Purpose |
|---|---|
| `/pr-review:review <PR number or URL>` | Fetch and review a PR, then draft comments without posting them. |

## Agent

| Agent | Purpose |
|---|---|
| `pr-reviewer` | Resolves PR input, fetches metadata and diff, runs focused review passes, and drafts comments. |

## Skills

| Skill | Purpose |
|---|---|
| `pr-review` | Command-equivalent overseer workflow that routes to focused review skills, deduplicates findings, and owns final comment selection. |
| `pr-diff-intake` | Resolves GitHub or Azure DevOps PR input and fetches reviewable diff context. |
| `review-obvious-issues` | Finds likely correctness bugs and behavior regressions. |
| `review-tests` | Finds missing or weak tests tied to changed behavior. |
| `review-security-privacy` | Finds security, authorization, secrets, logging, and privacy risks. |
| `review-api-contracts` | Finds API, schema, persistence, event, and rollout contract issues. |
| `review-maintainability` | Finds maintainability, best-practice, dependency, and complexity concerns. |
| `review-performance-reliability` | Finds performance, concurrency, timeout, retry, and operational risks. |
| `review-interesting-decisions` | Produces author questions for architecture, dependency, and design trade-offs. |
| `review-output-format` | Formats findings as concise review comments with diff-like snippets. |

## Requirements

- Run from inside the repository that contains the PR.
- GitHub PRs use the GitHub CLI (`gh`) by default.
- Azure DevOps PRs use the Azure CLI with the DevOps extension (`az repos`) and git ref fetching.
- If a provider CLI cannot fetch the diff, provide a PR diff export manually.

## Local Checks

The reviewer inspects the diff first. It may run safe local checks only when repository conventions are obvious and the command is read-only, such as a clear lint, typecheck, or targeted test command.

It will not run deploys, migrations, watch commands, destructive git commands, or commands that require unknown external services.

## Safety

`pr-review` is draft-only. It does not:

- Post PR comments
- Submit approvals or requests for changes
- Push commits
- Edit files
- Reset, clean, rebase, or merge branches
