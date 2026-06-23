# Contributing to brady-plugins

This is the human-facing contribution guide for `brady-plugins`. It mirrors the repo-level conventions from `AGENTS.md` so contributors can make changes consistently without reading agent-specific instructions first.

Issues and pull requests are welcome, including suggestions for new plugins, improvements to existing prompts or skills, and compatibility fixes for other agents.

## What this repo is

`brady-plugins` is a personal Claude Code and Codex marketplace. Each plugin lives in `plugins/<name>/` and is also designed to be content-portable to other agents. The prompts, skills, and conventions are written so someone using Cursor, Cline, Aider, or another agent can lift the markdown content directly.

The Claude Code marketplace mechanism (`.claude-plugin/marketplace.json`) and Codex marketplace mechanism (`.agents/plugins/marketplace.json`) are install paths. The content inside each plugin is not tool-specific.

## Repo layout

```text
brady-plugins/
|-- .claude-plugin/
|   `-- marketplace.json          # Claude Code registry of every plugin in this marketplace
|-- .agents/
|   `-- plugins/
|       `-- marketplace.json      # Codex registry of every plugin in this marketplace
|-- plugins/
|   `-- <plugin-name>/
|       |-- .claude-plugin/plugin.json
|       |-- .codex-plugin/plugin.json
|       |-- agents/                # subagent definitions (Claude Code)
|       |-- commands/              # slash commands (Claude Code)
|       |-- skills/<name>/SKILL.md # progressive-disclosure knowledge
|       |-- docs/                  # any reference docs the plugin needs
|       |-- AGENTS.md              # per-plugin maintainer notes
|       |-- CLAUDE.md              # one-liner: @AGENTS.md
|       |-- README.md              # end-user docs
|       `-- CHANGELOG.md           # per-plugin version history
|-- AGENTS.md                      # AI maintainer instructions
|-- CLAUDE.md                      # one-liner: @AGENTS.md
|-- CONTRIBUTING.md                # human contributor guide
|-- README.md                      # marketplace install + plugin index
|-- LICENSE                        # MIT
`-- .gitignore
```

## When to bump versions

Each plugin has its own `version` field in both `plugins/<plugin>/.claude-plugin/plugin.json` and `plugins/<plugin>/.codex-plugin/plugin.json`, plus the matching entry in the repo-root `.claude-plugin/marketplace.json`. All plugin version fields must stay in sync.

Codex marketplace entries do not carry versions. Codex reads the version from `.codex-plugin/plugin.json`. A plugin's `CHANGELOG.md` is the source of truth for what changed.

Follow Semantic Versioning (`MAJOR.MINOR.PATCH`):

| Bump | When |
|---|---|
| PATCH (`1.0.0 -> 1.0.1`) | Prompt or installable-content clarifications that do not change behavior, tightening an example, no schema changes |
| MINOR (`1.0.0 -> 1.1.0`) | New agent, new skill, new command, new optional config field, new conditional section in the template, new behavior that is strictly additive and backward-compatible |
| MAJOR (`1.0.0 -> 2.0.0`) | Removed agent/command/skill, renamed config field, changed default behavior, breaking change to file layout or save-path logic, anything that would surprise an existing user |

When in doubt, lean toward the larger bump. Users tolerate "more" updates better than they tolerate surprise breakage.

README-only installation docs, marketplace docs, typo fixes, and other changes that do not alter installed plugin behavior or agent-consumed content do not require a plugin version bump.

## What to do when you change a plugin

A change to installed plugin behavior or agent-consumed content under `plugins/<name>/` should result in:

1. Update `plugins/<name>/CHANGELOG.md` - add an entry under a new version heading, or under `## [Unreleased]` if you are not bumping yet. Use the Keep a Changelog format already present.
2. Bump the version in both `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/.codex-plugin/plugin.json` per the rules above.
3. Bump the matching version in `/.claude-plugin/marketplace.json`. These version fields must always agree.
4. Update `plugins/<name>/README.md` if the change affects how an end-user uses the plugin.
5. Update `plugins/<name>/AGENTS.md` if the change affects how a contributor or maintaining agent should reason about the plugin.

Do not bundle unrelated changes across plugins in one commit unless they are a coordinated multi-plugin release. Each plugin should have its own release rhythm.

## When to add a new plugin

To add a plugin (`my-plugin`):

1. Create `plugins/my-plugin/` with:
   - `.claude-plugin/plugin.json` with name, version `1.0.0` or `0.1.0`, description, author, license, homepage, repository, and keywords.
   - `.codex-plugin/plugin.json` with the same name, version, and description, plus `skills: "./skills/"` when the plugin has skills and the required `interface` metadata.
   - Plugin content: agents, commands, skills, docs, as needed.
   - `README.md` for end-user docs.
   - `AGENTS.md` for per-plugin maintainer notes: style conventions, layout, and where to extend.
   - `CLAUDE.md` with a single line: `@AGENTS.md`.
   - `CHANGELOG.md` starting at `## [1.0.0] - YYYY-MM-DD`, or `0.1.0` if pre-release.
2. Add an entry to `/.claude-plugin/marketplace.json` under `plugins[]` with name, source (`./plugins/my-plugin`), description, version matching `plugin.json`, category, and keywords.
3. Add an entry to `/.agents/plugins/marketplace.json` under `plugins[]` with name, local source path, policy, and category.
4. Update the Plugins table in `/README.md` with a one-line summary and link.
5. Optionally update `AGENTS.md` if the new plugin introduces a convention worth documenting at the repo level.

A new plugin starts at `1.0.0` if it is reasonably complete and you are confident in the surface area. Use `0.x.y` only if you genuinely expect breaking changes in the near term.

## When to remove a plugin

Do not silently delete. Either:

- Mark it deprecated in its README and bump to a major version with the deprecation noted in `CHANGELOG.md`, then remove in a follow-up release.
- Move the plugin folder out of the repo if it is being graduated to its own standalone repo, and leave a note in `/README.md` pointing at the new home.

## Style conventions

These apply to every plugin in this repo. They are a baseline. Individual plugins can extend them in their own `AGENTS.md`.

### Content portability

- Do not say "Claude" inside prompts, skills, or agent definitions. Use "you", "the agent", or "the assistant".
- The `plugin.json`, `marketplace.json`, and `commands` directory are structurally Claude Code. That is fine; it is the install mechanism. The content an agent reads should be portable.
- If something genuinely only works in Claude Code, such as a reference to `AskUserQuestion`, it is fine to reference it. Prefer general phrasing where possible, such as "ask the user with a multi-choice prompt".

### Prompt writing

- Use direct, second person: `You are X`, `Your job is Y`.
- Lead with the role, then required inputs, then process, then constraints such as `What You Must Not Do`.
- Prefer concrete examples over abstract description.
- Reader test: an agent picking this up cold should know what to do without asking the user follow-ups about the agent's own role.

### File naming

- Plugin folders, agent files, command files, and skill folders use `kebab-case`.
- Use uppercase `SKILL.md` inside each skill folder.
- Use uppercase `README`, `AGENTS`, `CLAUDE`, `LICENSE`, and `CHANGELOG` at repo and plugin roots.

### Frontmatter

- Every agent and skill has YAML frontmatter: `name`, `description`, plus tools, version, tags, or similar fields when relevant.
- The `description` field is what user-facing UI and discovery use. Write it so an agent triaging "is this skill relevant to my task" can decide in one read.

## CLAUDE.md / AGENTS.md relationship

Both at the repo root and inside each plugin, `AGENTS.md` is the source of truth for AI maintainer instructions and `CLAUDE.md` is a one-line file containing only `@AGENTS.md`.

Claude Code resolves the `@` import. Other agents reading the directory can open `AGENTS.md` directly.

Edit `AGENTS.md`, never `CLAUDE.md`, other than the initial single-line `@AGENTS.md` setup.

## Marketplace.json conventions

The repo-root `.claude-plugin/marketplace.json` lists every plugin for Claude Code. Each entry needs:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Single-paragraph summary, same as plugin.json description.",
  "version": "1.0.0",
  "category": "documentation | development | review | other",
  "keywords": ["...", "..."]
}
```

The `description` and `version` in marketplace.json must match the per-plugin `plugin.json`. The category and keywords are repo-level metadata for discovery.

The repo-root `.agents/plugins/marketplace.json` lists every plugin for Codex. Each entry needs:

```json
{
  "name": "plugin-name",
  "source": {
    "source": "local",
    "path": "./plugins/plugin-name"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Documentation"
}
```

Codex marketplace entries should keep `source.path` relative to the marketplace root as `./plugins/<plugin-name>`, include both policy fields, and use UI-friendly title-case categories. Codex reads description and version from `plugins/<plugin>/.codex-plugin/plugin.json`.

## Common mistakes to avoid

- Forgetting to update the Claude marketplace and Codex manifest after bumping a plugin's version. Users install via marketplace metadata, which becomes wrong if this is skipped.
- Adding a plugin to only one marketplace. New plugins should be listed in both `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
- Bundling unrelated plugin changes in one commit. That makes it hard to release each plugin independently.
- Adding "Claude" to a prompt because the plugin is Claude-Code-installed. The mechanism is Claude Code, but the content should stay portable.
- Editing `CLAUDE.md` instead of `AGENTS.md`. `CLAUDE.md` is just an import pointer.
- Skipping the `CHANGELOG.md` entry for a "tiny" behavior or installable-content change. Every behavioral change is worth noting, even patch-level. A four-line changelog is fine; a missing one is not.
- Promoting status or shipping behavior silently in any plugin that touches files. Always confirm with the user before destructive or hard-to-reverse actions.
