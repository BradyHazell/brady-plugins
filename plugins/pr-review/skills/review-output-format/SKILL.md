---
name: review-output-format
description: Format PR review findings as diff-like snippets with file paths and exact conversational comments for the user to add manually, plus file-level and general author questions.
license: MIT
---

# Review Output Format

Use this skill for the final response. The user wants draft comments, not a full report.

## Required Sections

Use these sections when they contain content:

1. `## Inline comments`
2. `## File-level questions`
3. `## General questions`
4. `## Suggested local checks`

Omit empty sections.

## Inline Comment Format

Each inline comment must include:

- Severity label
- File path
- Diff-like snippet
- Exact comment text

Template:

````markdown
### concern - path/to/file.ts

```diff
diff --git a/path/to/file.ts b/path/to/file.ts
@@
+ relevant changed line or nearby context
```

Comment:
Could we handle ...
````

Use these severity labels:

- `blocker`
- `concern`
- `suggestion`
- `question`

## Snippet Rules

- Keep snippets short: usually 3-12 lines.
- Include enough context that the author can find the issue.
- Prefer changed lines with `+` or `-` markers.
- Include nearby unchanged lines only when needed.
- Do not paste huge hunks or entire files.
- If exact line numbers are known, include them in the hunk header. If not, a plain `@@` hunk is acceptable.

## Comment Text Rules

Comments should sound like the user talking directly to the author.

Use:

- "Could we..."
- "Should this..."
- "I might be missing the reason for this, but..."
- "This needs to..."
- "Would it be safer to..."

Avoid:

- "The PR author should..."
- "This code is bad..."
- "As an AI..."
- "In conclusion..."
- Long background paragraphs

## File-Level Questions

Use this when the question applies to a file but not a specific line.

Template:

```markdown
## File-level questions

### path/to/file.ts
Comment:
I might be missing the intended direction here. Could we ...
```

## General Questions

Use this when the question spans multiple files or the overall design.

Template:

```markdown
## General questions

- Could we clarify whether ...
- I might be missing the rollout plan here. Should ...
```

## Suggested Local Checks

Include commands only when they are relevant and safe. Mark whether each was run.

Template:

```markdown
## Suggested local checks

- Not run: `npm test -- path/to/test`
- Run: `npm run typecheck` - passed
```

Do not claim a command passed or failed unless it was actually run.

## No Findings

If there are no useful comments, say:

```markdown
I do not have any inline comments worth adding. Suggested local checks:

- Not run: `...`
```

If there are no comments and no useful checks, say:

```markdown
I do not have any inline comments worth adding from this diff.
```
