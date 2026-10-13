# Sensitive File Patterns — Always Prompt Before Delete

> Globs that trigger keep-list prompt regardless of containing dir. These are not 🔴 (the file might genuinely be expired/redundant), but the cost of accidental deletion is high enough that a one-line confirmation is cheap insurance.

## Authentication & secrets

- `*recovery-codes*`, `*backup-codes*` — 2FA recovery codes
- `*credentials*`, `client_secret*`, `*credentials*.json` — OAuth/service-account credentials
- `*.pem`, `*.key`, `*.crt`, `*.cer`, `*.p12`, `*.pfx`, `*.keystore` — TLS certs and private keys
- `kaggle.json`, `*kaggle*.json` — Kaggle API token
- `*firebase-adminsdk*`, `*service-account*` — Firebase / GCP service accounts
- `.env*` (except `.env.example`, `.env.template`) — env files often hold secrets
- `id_rsa*`, `id_ed25519*`, `id_ecdsa*` — SSH key files (also covered by `~/.ssh` cliff, but pattern catches misplaced copies)

## Legal / personal documents

- `*MOTION*`, `*PETITION*`, `*AFFIDAVIT*`, `*subpoena*`
- `*passport*`, `*visa*`, `*green-card*`, `*greencard*`
- `*birth*certificate*`, `*marriage*certificate*`
- `*ssn*`, `*social-security*`
- `*court*order*`, `*settlement*agreement*`
- `*power*of*attorney*`

## Medical / academic

- `*certificate_of_enrollment*`, `*enrollment*verification*`
- `*transcript*`, `*diploma*`, `*degree*`
- `*prescription*`, `*medical*record*`, `*health*record*`
- `*letter*of*recommendation*`

## Financial

- `*tax*return*`, `*1099*`, `*W-2*`, `*W2*`
- `*bank*statement*`, `*paystub*`, `*pay-stub*`
- `*1040*`, `*1098*`
- `*invoice*` (often disposable but sometimes business-critical — ask)

## When pattern doesn't match but file looks personal

If a filename looks personal/legal/medical/financial but doesn't match a pattern above, ask anyway. Better to over-ask once than nuke something irreplaceable. Examples that wouldn't match patterns but should still trigger ask:

- `Eviction Notice 2026.pdf`
- `Final Will.docx`
- `Insurance Claim 04.27.pdf`

These should bias you toward `🟡 ask`, not `🟢 auto`.

## Tactic

On match: don't auto-delete. Cross-check `state.md`'s `downloads-keep` / `desktop-keep` saved rules:

- Match in saved rules → silent keep (still log to findings)
- New match → AskUserQuestion: **Keep** / **Delete**. The answer becomes a saved rule.

After the user decides, propose adding to saved rules so the same question doesn't get asked next time.
