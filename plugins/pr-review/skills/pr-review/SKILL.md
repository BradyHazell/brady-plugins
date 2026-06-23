---
name: pr-review
description: Command-equivalent overseer workflow for reviewing a pull request from a PR number or URL. Fetches PR metadata and diff from the current repository, coordinates focused review skills, drafts concise inline comments and author questions, and never posts anything.
license: MIT
---

# PR Review Workflow

Use this skill as the skill-form equivalent of `/pr-review:review <PR number or PR URL>`.

You are reviewing a pull request for the user. The user provides a PR number or PR URL, and your job is to fetch the PR changes from the repository you are running in, coordinate the focused review skills, and draft comments the user can manually add to the PR.

The output is not a long write-up. It is a set of review comments with file paths, diff-like snippets, and conversational comment text.

## Required Input

- A PR number for the current repository
- Or a PR URL from GitHub or Azure DevOps

If the identifier is missing, ask one concise question for it and stop.

## Required Companion Skills

Read these skills as the workflow needs them:

- `pr-diff-intake` - resolve PR input and fetch metadata/diff
- `review-obvious-issues` - correctness and behavior regressions
- `review-tests` - missing or weak test coverage
- `review-security-privacy` - authorization, data exposure, injection, secrets, and privacy
- `review-api-contracts` - compatibility, schemas, events, persistence, and rollout contracts
- `review-maintainability` - best practices, repo conventions, unnecessary complexity, and dependency choices
- `review-performance-reliability` - latency, resource use, concurrency, retries, and operations risk
- `review-interesting-decisions` - questions for design, architecture, or unusual implementation choices
- `review-output-format` - final formatting and comment tone

## Process

### 1. Establish scope

Identify:

- The PR being reviewed
- Any user-specified focus areas
- Whether the user expects only inline comments or also file-level and general questions

Stay anchored to the PR. Do not review unrelated existing code unless the PR makes it relevant.

### 2. Resolve the PR

Use `pr-diff-intake`.

Collect:

- Provider and URL
- PR number or ID
- Title, author, description, base branch, head branch
- Changed file list
- Unified diff

If the input is a number, assume the current GitHub repository unless the remote clearly points at Azure DevOps. If a URL is provided, use the provider implied by the URL.

For Azure DevOps PRs, follow `pr-diff-intake` exactly for metadata lookup. The first metadata command is:

```bash
az repos pr show --id <id> --org https://dev.azure.com/<org> -o json
```

Do not add `--project` to that metadata command.

### 3. Read the code around the diff

Start from the diff. Read full changed files only when the snippet is not enough to understand behavior.

Prefer changed lines as comment anchors. Use nearby unchanged context only when it explains an issue introduced by the PR.

### 4. Inspect before running checks

Look for package files, scripts, test folders, and existing CI conventions. Run safe local checks only when the command is obvious and read-only.

Examples of safe checks:

- A repository-defined lint command
- A repository-defined typecheck command
- A targeted test command for changed tests or changed packages

Do not run deploys, migrations, watch commands, commands requiring cloud credentials, or commands that mutate the PR.

If checks would be useful but are not safe or obvious, list them under Suggested local checks instead.

### 5. Coordinate focused review passes

Always do a quick pass for obvious correctness issues.

Then choose the focused skills based on the diff:

- Behavior changed, tests changed, or bug fixed: use `review-tests`
- Auth, data access, logging, parsing, external input, secrets, or PII: use `review-security-privacy`
- Routes, schemas, migrations, events, jobs, public APIs, config, or feature flags: use `review-api-contracts`
- New patterns, helpers, abstractions, dependencies, or cross-module movement: use `review-maintainability`
- Queries, loops, background work, external calls, retries, timeouts, concurrency, or observability: use `review-performance-reliability`
- Unusual architecture, redundant work, unnecessary library choices, or unclear trade-offs: use `review-interesting-decisions`

Each pass should add only high-signal findings. Include blockers, concerns, and suggestions. A good review comment has a concrete risk, concrete action, or concrete question.

### 6. Deduplicate and calibrate

Before final output:

- Merge duplicate findings that point to the same underlying issue.
- Prefer one strong comment over several weak comments.
- Keep comments anchored to changed lines where possible.
- Convert low-confidence findings into questions.
- Drop comments that are only style preference or generic best practice.
- Keep a mix of blockers, concerns, suggestions, and questions when the diff warrants it.

Severity labels:

- `blocker` - likely bug, data loss, security issue, broken contract, or change that should not merge as-is
- `concern` - meaningful risk or unclear behavior worth resolving before merge
- `suggestion` - improvement that is useful but not required
- `question` - decision or trade-off that needs author context

When confidence is low, prefer `question` over a stated finding.

### 7. Decide placement

- Line-specific issue: Inline comments
- Whole-file decision: File-level questions
- Cross-cutting design, rollout, or testing question: General questions
- Useful command that was not run or should be run by the user/author: Suggested local checks

### 8. Output comments

Use `review-output-format`.

Required output:

- Inline comments with file path, diff-like snippet, and exact comment text
- File-level questions when the question is about a file but not a specific line
- General questions when the question spans multiple files or the overall design
- Suggested local checks when relevant

Omit empty sections.

## Comment Selection Bar

Include a comment only when at least one is true:

- It could prevent a bug, regression, security issue, or broken contract.
- It asks for context on a decision that materially affects architecture, dependencies, rollout, or maintainability.
- It requests a targeted test for changed behavior that has meaningful risk.
- It suggests a simpler local pattern that reduces future churn.

Do not include comments just to prove the whole diff was read.

## Comment Voice

Write as if the user is speaking directly to the PR author:

- "Could we handle the empty response case here?"
- "I might be missing the reason for this, but could we reuse the existing helper instead of adding a new dependency?"
- "This needs to keep the tenant check before returning the record; otherwise a user could read data from another tenant."

Avoid:

- Long review essays
- Generic praise
- "As an AI" language
- Formal audit language
- Provider-specific details unless needed

## Constraints

- Never post, submit, approve, request changes, push commits, or edit files.
- Do not review unrelated existing code unless the PR changes make it relevant.
- Do not invent test results. If a command was not run, say it was suggested, not run.
- Do not assume an architectural decision is wrong. Ask when the trade-off could be intentional.
