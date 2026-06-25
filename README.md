# brady-plugins

A personal Claude Code and Codex plugin marketplace. The plugins also install into other agents (Cursor, Goose, etc.) via the open-plugin `npx plugins` CLI or the legacy `npx skills` CLI.

## Install

### Claude Code

Bash:

```bash
claude plugins marketplace add BradyHazell/brady-plugins
claude plugins install prd-drafter@brady-plugins
claude plugins install pr-review@brady-plugins
```

Slash commands:

```text
/plugin marketplace add BradyHazell/brady-plugins
/plugin install prd-drafter@brady-plugins
/plugin install pr-review@brady-plugins
```

### Codex

Add the marketplace, then install the plugins:

Bash:

```bash
codex plugins add marketplace BradyHazell/brady-plugins
codex plugins add prd-drafter@brady-plugins
codex plugins add pr-review@brady-plugins
```

Slash commands:

```text
/plugins add marketplace BradyHazell/brady-plugins
/plugins add prd-drafter@brady-plugins
/plugins add pr-review@brady-plugins
```

### Other agents (Cursor, Goose, etc.)

Preferred open-plugin CLI:

```bash
# Confirm the repo is discoverable
npx plugins discover BradyHazell/brady-plugins

# Auto-detect installed targets
npx plugins add BradyHazell/brady-plugins

# If auto-detect says "No supported targets detected", choose one explicitly
npx plugins add BradyHazell/brady-plugins --target codex
npx plugins add BradyHazell/brady-plugins --target cursor
npx plugins add BradyHazell/brady-plugins --target claude-code
```

The auto-detect path requires the target binary to be on `PATH`. Use `--target` when the CLI cannot find `claude`, `cursor`, or `codex` automatically.

Legacy skills CLI:

```bash
# Auto-detect installed agents
npx skills add BradyHazell/brady-plugins

# Or target a specific agent
npx skills add BradyHazell/brady-plugins -a codex
npx skills add BradyHazell/brady-plugins -a cursor
```

## Plugins

| Plugin | Version | Summary |
|---|---|---|
| [**prd-drafter**](./plugins/prd-drafter) | 2.0.0 | Drafts Product Requirements Documents through conversational discovery, supports structured updates, and exports PRDs to browser-printable HTML. Configurable per-repo via `.prdrc.json`. |
| [**pr-review**](./plugins/pr-review) | 1.0.2 | Reviews pull requests from a PR number or URL, fetches the diff from the current repo, and drafts concise inline review comments and author questions without posting anything. |

Each plugin has its own README with full details — click the plugin name above.

## Standalone Skills

Standalone skills live under `skills/` when they are useful on their own and do not need a full plugin wrapper.

| Skill | Summary |
|---|---|
| [**humanize**](./skills/humanize) | Rewrites AI-generated text into natural, human-to-human wording while preserving important meaning and formatting. |

## Contributing

This is a personal repo, but issues and pull requests are open for suggestions, new plugin ideas, prompt improvements, and compatibility fixes for other agents.

- **Human contributors**: see [`CONTRIBUTING.md`](./CONTRIBUTING.md) for conventions, versioning rules, and how to add a new plugin.
- **AI agents helping maintain the repo**: see [`AGENTS.md`](./AGENTS.md) for the agent instruction manual.

## License

[MIT](./LICENSE) — use, fork, modify freely with attribution.
