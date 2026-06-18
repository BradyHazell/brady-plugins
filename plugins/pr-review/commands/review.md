---
description: Review a pull request from a PR number or URL. Fetches the diff from the current repository, inspects changed code, and drafts concise inline comments plus author questions without posting anything.
argument-hint: <PR number or PR URL>
---

# Review a Pull Request

You are running the main entry point of the `pr-review` plugin. The user wants a code review for a pull request and will provide either a PR number or a PR URL.

## Required Input

- A PR number for the current repository, such as `123`
- Or a PR URL, such as a GitHub pull request URL or an Azure DevOps pull request URL

If no PR identifier was provided, ask the user for one concise follow-up question and stop.

## Your Process

1. **Invoke the `pr-reviewer` agent** with the PR identifier and any extra context the user provided.

2. The reviewer agent will:
   - Resolve the PR provider from the input
   - Fetch PR metadata and a unified diff from the repository the agent is running in
   - Inspect changed files and nearby context where needed
   - Run safe local checks only when the repository conventions are obvious
   - Draft review comments without posting them
   - Include blockers, concerns, suggestions, and questions

3. **Return the agent output directly.** Do not reformat the comments into a long report. Preserve the diff-like snippets and conversational review comments.

## Constraints

- Do not post comments, submit reviews, approve, request changes, push commits, or modify the PR.
- Prefer comments on changed lines. Use nearby unchanged context only when it is needed to explain the issue introduced by the PR.
- Keep comments in the user's voice: concise, conversational, and directed at the author.
- Avoid broad summaries unless the reviewer found a general question that belongs outside a specific file.
