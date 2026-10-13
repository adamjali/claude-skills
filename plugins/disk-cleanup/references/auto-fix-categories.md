# 🟢 Auto-Fix Categories — Regenerable Caches

> Catalog of paths that are safely auto-deletable. Use as a starting point — when you encounter something not listed but obviously regenerable (a tool-managed cache dir whose docs say "safe to delete"), reason about it and add to `findings.json` with rationale. The user reviews the rationale at preview time.

## Node / JavaScript

| Path | Tool | Notes |
|---|---|---|
| `~/.npm/_cacache`, `~/.npm/_npx` | npm | Re-downloaded on next install. |
| `~/Library/pnpm/store` orphans | pnpm | `pnpm store prune` — only orphans, not the whole store. The store is content-addressable; projects link into it. |
| `~/Library/Caches/node-gyp` | node-gyp | Native build artifacts. Rebuilds on next install. |
| `~/.bun/install/cache` | Bun | Bun pkg cache. |
| `<project>/node_modules` (non-active project only) | npm/pnpm/yarn | Active projects → 🟡 (forces reinstall before next dev session). |
| `<project>/.next` | Next.js | Build cache. Rebuilds on next dev/build. |
| `<project>/dist`, `<project>/build`, `<project>/out` | Various build tools | Build outputs. |

## Python

| Path | Tool | Notes |
|---|---|---|
| `~/.cache/uv` | uv | `uv cache clean` — rebuilds. |
| `~/Library/Caches/pip` | pip | `pip3 cache purge`. |
| `__pycache__` outside active projects | CPython | `find ~ -name __pycache__ -prune -exec rm -rf {} +` (skip your active-project paths). |
| `.pytest_cache`, `.mypy_cache`, `.ruff_cache` | pytest/mypy/ruff | Tool caches. Rebuilt on next run. |

## macOS system caches (regenerable)

| Path | Notes |
|---|---|
| `~/Library/Caches/com.apple.MobileSMS` | Messages thumbnail cache. Rebuilds. |
| `~/Library/Caches/Google` (excluding `Profile *` dirs while Chrome running) | Chrome cache. Rebuilds. |
| `~/Library/Caches/typescript` | TS server cache. |
| `~/Library/Caches/Homebrew` | Brew download cache. Better via `brew cleanup`. |

## Homebrew (tool-managed)

- `brew cleanup -s --prune=all` — old versions + cached downloads + lock files
- `brew autoremove` — uninstall formulae installed only as dependencies that are no longer needed

## VSCode

- Old extension version duplicates in `~/.vscode/extensions/` — only when same extension-id has a newer version present. Heuristic: `<id>-<oldver>` is stale if `<id>-<newver>` exists with `newver > oldver`. Don't delete the only-version of any extension.

## Trivial sweeps

- `find ~ -name .DS_Store -not -path '*/.git/*' -delete` (skip active-project trees)

## When in doubt

If you find something cache-shaped that's not listed:

1. Check if it's tool-managed (e.g., does the tool have its own cleanup command? Use it instead of `rm`).
2. Check if it's documented as safe-to-delete (read the README in the dir, or the tool's docs).
3. If still unsure → 🟡, with rationale, let the user decide.

## Anti-pattern

Don't try to be clever about partial cache cleanup. Either clear the whole cache (regenerates) or leave it (still works). Selective deletion based on age/size of individual files inside a cache is fragile and tool-specific — defer to the tool's own cleanup command.
