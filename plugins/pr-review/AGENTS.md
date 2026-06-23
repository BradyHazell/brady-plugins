# AGENTS.md - pr-review maintainer notes

Plugin-specific guidance for any AI agent maintaining or extending `pr-review`. The repo-root [`AGENTS.md`](../../AGENTS.md) covers cross-plugin conventions; this file covers what is unique to this plugin.

## What this plugin does

Reviews pull requests from a PR number or URL, using the repository the agent is running in. It fetches PR metadata and diff context, runs focused review passes, and drafts concise comments the user can add manually.

The plugin is intentionally draft-only. It must not post comments, submit reviews, approve, request changes, push commits, or modify the PR.

## Layout

```
pr-review/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── agents/
│   └── pr-reviewer.md
├── commands/
│   └── review.md
├── skills/
│   ├── pr-review/SKILL.md
│   ├── pr-diff-intake/SKILL.md
│   ├── review-obvious-issues/SKILL.md
│   ├── review-tests/SKILL.md
│   ├── review-security-privacy/SKILL.md
│   ├── review-api-contracts/SKILL.md
│   ├── review-maintainability/SKILL.md
│   ├── review-performance-reliability/SKILL.md
│   ├── review-interesting-decisions/SKILL.md
│   └── review-output-format/SKILL.md
├── AGENTS.md
├── CLAUDE.md
├── README.md
└── CHANGELOG.md
```

## Where each thing belongs

| Adding... | Where it goes | Bumps |
|---|---|---|
| A new review pass | New `skills/review-*/SKILL.md`, plus references in `skills/pr-review/SKILL.md`, `agents/pr-reviewer.md`, README, and this file | MINOR |
| A new orchestration rule | `skills/pr-review/SKILL.md`, plus mirror any required workflow change in `agents/pr-reviewer.md` and `commands/review.md` | MINOR if behavior changes, PATCH for clarification |
| A new provider intake path | `skills/pr-diff-intake/SKILL.md`, plus README requirements if user-facing | MINOR |
| A change to output format | `skills/review-output-format/SKILL.md`, plus `agents/pr-reviewer.md`, `skills/pr-review/SKILL.md`, and README examples | MINOR if behavior changes, PATCH for clarification |
| A new slash command | `commands/<name>.md`, README, and this file | MINOR |
| A new agent | `agents/<name>.md`, command references, README, and this file | MINOR |
| Prompt clarification with no behavior change | The relevant command, agent, or skill | PATCH |

The command, the named agent, and the portable `pr-review` skill are parallel descriptions of the same behavior. Keep them in sync.

## Review philosophy

- High signal over completeness.
- Review the PR, not the entire codebase.
- Prefer changed-line comments; use nearby context only when needed.
- Include blockers, concerns, suggestions, and useful questions.
- Phrase low-confidence findings as questions.
- Ask about interesting decisions when a trade-off may be intentional.
- Comments should sound like the user speaking to the author, not like a formal report.

## Provider behavior

GitHub is the default for numeric PR inputs when the current remote is GitHub. Azure DevOps is supported for PR URLs and numeric inputs when the remote clearly points at Azure DevOps.

Provider logic lives in `skills/pr-diff-intake/SKILL.md`. Keep command snippets read-only and avoid checkout-based flows unless the user explicitly asks.

For Azure DevOps metadata, keep the command shape as `az repos pr show --id <id> --org https://dev.azure.com/<org> -o json`. Do not add `--project`; the PR URL contains a project, but this metadata subcommand can reject the project flag.

## Local checks

The reviewer may run safe checks only after inspecting the repository conventions. Good candidates are explicit lint, typecheck, or targeted test scripts.

Never add instructions that run:

- Deploys
- Migrations
- Watchers
- Destructive git commands
- Commands that need unknown external services or secrets

## Output contract

The output should use `review-output-format`:

- `## Inline comments`
- `## File-level questions`
- `## General questions`
- `## Suggested local checks`

Inline comments must include a severity label, file path, short diff-like snippet, and exact comment text. Omit empty sections.

## Content portability

Keep prompts, skills, and agent definitions agent-agnostic. Do not introduce product-specific wording into the reusable review instructions unless it is describing the repository installation mechanism.

## Testing changes

There is no automated test suite for this plugin yet. Verify changes by:

1. Running `/pr-review:review <github-pr-number>` in a GitHub-backed test repository.
2. Running `/pr-review:review <github-pr-url>` in a GitHub-backed test repository.
3. Running `/pr-review:review <azure-devops-pr-url>` in an Azure DevOps-backed test repository when available.
4. Confirming the output contains draft comments only and does not attempt to post anything.
5. Confirming empty sections are omitted and suggested checks are marked as run or not run accurately.

## What this plugin should not do

- It should not submit reviews or comments.
- It should not edit code.
- It should not run broad, risky, or destructive local commands.
- It should not invent provider data or test results.
- It should not turn every preference into a review comment.
