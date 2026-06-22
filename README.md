# brady-plugins

A personal Claude Code plugin marketplace. The plugins also install into other agents (Codex, Cursor, Goose, etc.) via the open-plugin `npx plugins` CLI or the legacy `npx skills` CLI.

## Install

### Claude Code

```
/plugin marketplace add BradyHazell/brady-plugins
/plugin install prd-drafter@brady-plugins
/plugin install pr-review@brady-plugins
```

Update later:

```
/plugin marketplace update brady-plugins
/plugin update prd-drafter@brady-plugins
/plugin update pr-review@brady-plugins
```

### Other agents (Codex, Cursor, etc.)

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
| [**pr-review**](./plugins/pr-review) | 1.0.0 | Reviews pull requests from a PR number or URL, fetches the diff from the current repo, and drafts concise inline review comments and author questions without posting anything. |

Each plugin has its own README with full details — click the plugin name above.

## Contributing

This is a personal repo, but issues and PRs are welcome.

- **Contributors**: see [`AGENTS.md`](./AGENTS.md) at the repo root for conventions, versioning rules, and how to add a new plugin.
- **AI agents helping maintain the repo**: the same `AGENTS.md` is your instruction manual.

## License

[MIT](./LICENSE) — use, fork, modify freely with attribution.
