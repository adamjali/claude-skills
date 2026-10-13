# Contributing

Thanks for your interest! This is a marketplace of [Claude Code](https://code.claude.com) skills, each packaged as its own plugin.

## Reporting issues
Open an issue with steps to reproduce, your Claude Code version (`claude --version`), and which skill is involved.

## Adding or changing a skill
- Each skill is a plugin under `plugins/<name>/` with a `SKILL.md` at its root and a `.claude-plugin/plugin.json`.
- Validate before opening a PR: `claude plugin validate ./plugins/<name> --strict` (and the marketplace: `claude plugin validate . --strict`).
- Keep skills self-contained and **secret-free** — bring-your-own-key via environment variables, and use `${CLAUDE_SKILL_DIR}` / `${CLAUDE_PLUGIN_ROOT}` for bundled file paths (never absolute home paths).
- Register the plugin in `.claude-plugin/marketplace.json` and add a row to the README table.

## License
By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
