# Safety Invariants — 🔴 Never-Touch List

> These are cliffs. No inline user-instruction overrides them. If you say "delete my .ssh" in chat, the skill refuses and points you to edit this file first. The friction is the point.

## Why this exists

Reasoning works for "is this cache regenerable?" It doesn't work for "should I delete the SSH keys?" — the answer is always no, and the smallest doubt should resolve to refuse. This file is the doubt-resolver.

## Categories

### Credential / identity stores

- `~/.ssh/` — SSH keys + known_hosts. Loss = lockout from servers, GitHub, etc.
- `~/.gnupg/` — GPG keyring. Loss = signed-commit history broken, encrypted backups unrecoverable.
- `~/Library/Keychains/` — Apple keychain. Loss = saved passwords gone, app authorizations broken.
- `~/.aws/` — AWS credentials + config. Loss = locked out of AWS until rotation.
- `~/.config/gh/` — GitHub CLI auth.
- `~/.netrc` — generic credential store some tools use.
- `~/.docker/config.json` — Docker registry credentials.

### Your config + memory

- `~/.claude/` — Claude Code global config. Skills, commands, hooks, settings, the whole system.
- `~/.claude/projects/` — auto-memory dirs. Years of context.
- This skill's own files — refuse to delete self.
- `~/.cursor/`, `~/.vscode/` — IDE config (extensions are 🟡, but settings/state is 🔴).

### Your active code + workspaces

- Your primary active code directories (e.g. `~/Documents/`, `~/code/`, `~/src/`).
- Any repo wired to a live automation or routine — don't even browse it casually.
- All paths in `state.md`'s `active-projects` saved rule.

### macOS-critical

- `~/Library/Messages/chat.db` (and `chat.db-shm`, `chat.db-wal`) — iMessage history. Only `Attachments/` subdir is 🟡.
- `~/Library/Application Support/Google/Chrome/*` — Chrome user data: bookmarks, saved logins, history. Only the `Cache/` subdirs are 🟢.
- `~/Library/Mobile Documents/` — iCloud Drive sync state.
- `/System`, `/usr`, `/Library` (top-level) — system dirs. Skill should never write outside `~/` except via Apple-blessed commands (`tmutil`).

### Active git working trees

If a path has a `.git` ancestor and `git status --porcelain` is non-empty, refuse. Uncommitted work is irreplaceable. (Build artifacts inside such trees — `.next`, `dist`, `node_modules` — still go through 🟡 ask, never 🟢 auto.)

### Pattern matches

Any file matching globs in `sensitive-patterns.md` is refused regardless of dir. That file is the second cliff.

## Rationale

Each category above costs hours to days to recover from if deleted by mistake. Disk cleanup gains hours at most. The asymmetry is the whole argument — never trade hours of recovery for minutes of reclaim.
