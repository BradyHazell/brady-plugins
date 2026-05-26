# AGENTS.md — brady-plugins maintainer guide

This file is the instruction manual for any AI agent (Claude, Cursor, Aider, etc.) helping maintain or extend this repo. It captures the conventions and judgment calls a contributor needs to make consistently.

Human contributors should also read it — it doubles as a CONTRIBUTING guide.

## What this repo is

`brady-plugins` is a personal Claude Code marketplace. Each plugin lives in `plugins/<name>/` and is also designed to be **content-portable** to other agents — the prompts, skills, and conventions are written so that someone using Cursor, Cline, Aider, or any other agent can lift the markdown content directly.

The Claude Code marketplace mechanism (`.claude-plugin/marketplace.json`) is the install path; the content inside each plugin is not Claude-specific.

## Repo layout

```
brady-plugins/
├── .claude-plugin/
│   └── marketplace.json          # registry of every plugin in this marketplace
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/plugin.json
│       ├── agents/                # subagent definitions (Claude Code)
│       ├── commands/              # slash commands (Claude Code)
│       ├── skills/<name>/SKILL.md # progressive-disclosure knowledge
│       ├── docs/                  # any reference docs the plugin needs
│       ├── AGENTS.md              # per-plugin maintainer notes
│       ├── CLAUDE.md              # one-liner: @AGENTS.md
│       ├── README.md              # end-user docs
│       └── CHANGELOG.md           # per-plugin version history
├── AGENTS.md                      # this file
├── CLAUDE.md                      # one-liner: @AGENTS.md
├── README.md                      # marketplace install + plugin index
├── LICENSE                        # MIT
└── .gitignore
```

## When to bump versions

Each plugin has its own `version` field in both `plugins/<plugin>/.claude-plugin/plugin.json` and the matching entry in the repo-root `.claude-plugin/marketplace.json`. **Both must stay in sync.** A plugin's CHANGELOG.md is the source of truth for what changed.

Follow Semantic Versioning (`MAJOR.MINOR.PATCH`):

| Bump | When |
|---|---|
| **PATCH** (`1.0.0 → 1.0.1`) | Typo fixes, doc-only changes, prompt clarifications that don't change behaviour, tightening an example, no schema changes |
| **MINOR** (`1.0.0 → 1.1.0`) | New agent, new skill, new command, new optional config field, new conditional section in the template, new behaviour that's strictly additive and backward-compatible |
| **MAJOR** (`1.0.0 → 2.0.0`) | Removed agent/command/skill, renamed config field, changed default behaviour, breaking change to file layout or save-path logic, anything that would surprise an existing user |

When in doubt, lean toward the larger bump — users tolerate "more" updates better than they tolerate surprise breakage.

## What to do when you change a plugin

A change to any file under `plugins/<name>/` should result in:

1. **Update `plugins/<name>/CHANGELOG.md`** — add an entry under a new version heading (or under `## [Unreleased]` if you're not bumping yet). Use the Keep a Changelog format already present.
2. **Bump the version** in `plugins/<name>/.claude-plugin/plugin.json` per the rules above.
3. **Bump the matching version** in `/.claude-plugin/marketplace.json` (top-level marketplace registry) — these two version fields must always agree.
4. **Update `plugins/<name>/README.md`** if the change affects how an end-user uses the plugin.
5. **Update `plugins/<name>/AGENTS.md`** if the change affects how a contributor or maintaining agent should reason about the plugin.

Do not bundle unrelated changes across plugins in one commit unless they're a coordinated multi-plugin release. Each plugin should have its own release rhythm.

## When to add a new plugin

To add a plugin (`my-plugin`):

1. Create `plugins/my-plugin/` with:
   - `.claude-plugin/plugin.json` (name, version `1.0.0` or `0.1.0`, description, author, license, homepage, repository, keywords)
   - Plugin content (agents, commands, skills, docs as needed)
   - `README.md` — end-user docs
   - `AGENTS.md` — per-plugin maintainer notes (style conventions, layout, where to extend)
   - `CLAUDE.md` — single line: `@AGENTS.md`
   - `CHANGELOG.md` — start at `## [1.0.0] — YYYY-MM-DD` (or `0.1.0` if pre-release)
2. Add an entry to `/.claude-plugin/marketplace.json` under `plugins[]` with name, source (`./plugins/my-plugin`), description, version (matching plugin.json), category, keywords.
3. Update the **Plugins** table in `/README.md` with a one-line summary + link.
4. Optionally update this AGENTS.md if the new plugin introduces a convention worth documenting at the repo level.

A new plugin starts at `1.0.0` if it's reasonably complete and you're confident in the surface area. Use `0.x.y` only if you genuinely expect breaking changes in the near term.

## When to remove a plugin

Don't silently delete. Either:
- Mark it deprecated in its README and bump to a major version with the deprecation noted in CHANGELOG, then remove in a follow-up release, or
- Move the plugin folder out of the repo if it's being graduated to its own standalone repo, and leave a note in `/README.md` pointing at the new home.

## Style conventions

These apply to every plugin in this repo. They're a baseline — individual plugins can extend them in their own AGENTS.md.

### Content portability ("agent-agnostic")

- **Don't say "Claude" inside prompts, skills, or agent definitions.** Use "you", "the agent", or "the assistant".
- The plugin.json/marketplace.json/commands directory are structurally Claude Code — that's fine, that's the install mechanism. But the *content* an agent reads should be portable.
- If something genuinely only works in Claude Code (e.g. a reference to `AskUserQuestion`), it's fine to reference it — but prefer general phrasing where possible (e.g. "ask the user with a multi-choice prompt").

### Prompt writing

- Direct, second person (`You are X`, `Your job is Y`).
- Lead with the role, then required inputs, then process, then constraints (`What You Must Not Do`).
- Prefer concrete examples over abstract description.
- One reader test: an agent picking this up cold should know what to do without asking the user follow-ups about the agent's own role.

### File naming

- Plugin folders, agent files, command files, skill folders: `kebab-case`.
- SKILL.md (uppercase) inside each skill folder.
- README, AGENTS, CLAUDE, LICENSE, CHANGELOG at repo and plugin roots: uppercase per the convention they each follow.

### Frontmatter

- Every agent and skill has YAML frontmatter (`name`, `description`, plus tools/version/tags as relevant).
- The `description` field is what the user-facing UI and discovery use — write it so an agent triaging "is this skill relevant to my task" can decide in one read.

## CLAUDE.md / AGENTS.md relationship

Both at the repo root and inside each plugin, there's an AGENTS.md (the source of truth for AI maintainer instructions) and a CLAUDE.md (a one-line file containing only `@AGENTS.md`). Claude Code resolves the `@` import; other agents reading the directory can just open AGENTS.md directly.

**Edit AGENTS.md, never edit CLAUDE.md** (other than the initial single-line `@AGENTS.md` setup).

## Marketplace.json conventions

The repo-root `.claude-plugin/marketplace.json` lists every plugin. Each entry needs:

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

## Common mistakes to avoid

- **Forgetting to update marketplace.json** after bumping a plugin's version — users install via the marketplace registry, which becomes wrong.
- **Bundling unrelated plugin changes** in one commit — makes it hard to release each plugin independently.
- **Adding "Claude" to a prompt** because the plugin is Claude-Code-installed — the *mechanism* is Claude Code, but the *content* should stay portable.
- **Editing CLAUDE.md** instead of AGENTS.md — CLAUDE.md is just an import pointer; edits go to the source.
- **Skipping the CHANGELOG entry** for a "tiny" change — every behavioral change is worth noting, even patch-level. A four-line CHANGELOG is fine; a missing one is not.
- **Promoting status / shipping behaviour silently** in any plugin that touches files — always confirm with the user before destructive or hard-to-reverse actions.
