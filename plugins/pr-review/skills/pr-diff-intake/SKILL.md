---
name: pr-diff-intake
description: Resolve a PR number or URL into reviewable metadata and a unified diff using the current repository. Supports GitHub by default and Azure DevOps URLs with safe fallbacks, without posting comments or mutating the PR.
license: MIT
---

# PR Diff Intake

Use this skill to turn a PR number or PR URL into metadata, changed files, and a unified diff.

## Principles

- Work from the repository the agent is already running in.
- Prefer read-only commands.
- Do not post comments, submit reviews, approve, request changes, push commits, or edit files.
- Avoid checking out branches unless the user explicitly asks.
- Preserve the user's dirty worktree. Fetching refs is acceptable; resetting or cleaning is not.

## Provider Detection

### PR number

If the input is only a number:

1. Inspect `git remote -v`.
2. If the primary remote contains `github.com`, treat the number as a GitHub PR number.
3. If the primary remote contains `dev.azure.com` or `visualstudio.com`, treat the number as an Azure DevOps pull request ID.
4. If the remote is ambiguous, ask the user for a PR URL.

### GitHub URL

Recognize URLs like:

```text
https://github.com/org/repo/pull/123
```

### Azure DevOps URL

Recognize URLs like:

```text
https://dev.azure.com/org/project/_git/repo/pullrequest/123
https://org.visualstudio.com/project/_git/repo/pullrequest/123
```

## GitHub Intake

Use the GitHub CLI when available.

Metadata:

```bash
gh pr view <number-or-url> --json number,title,url,author,body,baseRefName,headRefName,headRepository,headRepositoryOwner,isDraft,mergeStateStatus,files,additions,deletions
```

Patch:

```bash
gh pr diff <number-or-url> --patch
```

Useful optional context:

```bash
gh pr checks <number-or-url>
git diff --check
```

If `gh` is unavailable or unauthenticated, ask the user to authenticate or provide the diff. Do not fall back to scraping web pages.

## Azure DevOps Intake

Use the Azure CLI with the DevOps extension when available.

Parse from URL:

- Organization
- Project
- Repository
- Pull request ID

Metadata must be fetched before branch/ref fetches. For Azure DevOps, pull request IDs are organization-scoped for this command, so run this exact shape first:

```bash
az repos pr show --id <id> --org https://dev.azure.com/<org> -o json
```

Do not add `--project` to `az repos pr show`. Some Azure DevOps CLI versions reject it for this subcommand. Use the parsed project only for repository identity checks, URL reconstruction, or later fallback commands that explicitly accept a project argument.

From the metadata, capture:

- `sourceRefName`
- `targetRefName`
- repository name and remote URL
- title, description, author, status

Preferred diff strategy:

1. Fetch the target ref and source ref without checking them out.
2. Run a local diff between target and source.

For same-repository PRs:

```bash
git fetch origin +<targetRefName>:refs/remotes/origin/<target-branch> +<sourceRefName>:refs/remotes/origin/<source-branch>
git diff --no-ext-diff --unified=80 refs/remotes/origin/<target-branch>...refs/remotes/origin/<source-branch>
```

If the source branch is from a fork or the ref fetch fails, use the source repository URL from the PR metadata and fetch into a temporary remote ref:

```bash
git fetch <source-repository-url> +<sourceRefName>:refs/remotes/pr-review/source/<id>
git fetch origin +<targetRefName>:refs/remotes/pr-review/target/<id>
git diff --no-ext-diff --unified=80 refs/remotes/pr-review/target/<id>...refs/remotes/pr-review/source/<id>
```

If neither `az` nor git ref fetching can produce the diff, ask the user for a diff export. Do not guess changed code from metadata alone.

## Diff Handling

When the diff is large:

- Start with the file list and PR description.
- Prioritize executable code, migrations, config, API schemas, generated files that should not have changed, and tests.
- Read full files only when needed.
- Summarize skipped low-risk files briefly only if their omission affects confidence.

## Local Context Commands

Useful read-only commands:

```bash
git status --short
git remote -v
git branch --show-current
git diff --check
rg --files
```

Avoid commands that:

- Delete, reset, clean, rebase, or merge
- Apply patches
- Push to remotes
- Check out branches without explicit user approval
- Run database migrations or deploys
