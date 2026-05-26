# brady-plugins

A personal Claude Code plugin marketplace. The plugins also install into other agents (Codex, Cursor, Goose, etc.) via the `npx skills` CLI.

## Install

### Claude Code

```
/plugin marketplace add BradyHazell/brady-plugins
/plugin install prd-drafter@brady-plugins
```

Update later:

```
/plugin marketplace update brady-plugins
/plugin update prd-drafter@brady-plugins
```

### Other agents (Codex, Cursor, etc.)

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
| [**prd-drafter**](./plugins/prd-drafter) | 1.0.0 | Drafts Product Requirements Documents through conversational discovery. Acts as a PM, not a stenographer — challenges scope, surfaces hidden assumptions, treats Open Questions as a first-class output. Configurable per-repo via `.prdrc.json`. |

Each plugin has its own README with full details — click the plugin name above.

## Contributing

This is a personal repo, but issues and PRs are welcome.

- **Contributors**: see [`AGENTS.md`](./AGENTS.md) at the repo root for conventions, versioning rules, and how to add a new plugin.
- **AI agents helping maintain the repo**: the same `AGENTS.md` is your instruction manual.

## License

[MIT](./LICENSE) — use, fork, modify freely with attribution.
