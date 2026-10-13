# Docs Ledger — bounded, never grows forever

Durable pipeline state lives in files (they survive compaction and sessions),
and because the runtime won't trim *your* files, the ledger bounds itself: recent
entries stay full, old ones compact to one-liners. This mirrors how Claude Code
itself keeps only a rolling window of recent context.

## Contents
- [Files](#files)
- [Statuses](#statuses)
- [The rollover rule](#rollover)
- [Entry template](#template)

<a id="files"></a>
## Files (in `ledger/`)
- **`index.md`** — one line per business, the at-a-glance board. @-loaded by the
  skill, so keep it small. Pruned to the most recent ~30.
  Format: `- <slug> · <status> · <url-or-—> · <last-touched YYYY-MM-DD>`
- **`active/<slug>.md`** — the full entry while a business is in-flight.
- **`archive.md`** — one-liners for closed/cold/dead businesses (rolled out of
  the index).
- **`lessons.md`** — saved rules accumulated across runs.

<a id="statuses"></a>
## Statuses
`scouted → picked → verified → built → deployed → outreach-drafted → sent →
won | cold`

<a id="rollover"></a>
## The rollover rule (the "never grows forever" bound)
When `index.md` exceeds ~30 lines, move the **oldest / coldest** entries to
`archive.md` as one-liners and delete their `active/<slug>.md` files (the full
detail isn't needed once a business is closed). The index is the working set; the
archive is the long tail. This keeps the @-loaded file cheap forever — the whole
point of a bounded store.

<a id="template"></a>
## Entry template (`active/<slug>.md`)
```markdown
# <Business Name>  (<slug>)
- **Status:** scouted
- **Owner:** <name>
- **Contacts:** email · FB · cell
- **Current web:** <none / parked domain / old site URL>
- **Hook:** <the specific, honest reason to pitch them>
- **Verified facts:** <license #, rating, years — each tagged verified|aspirational>
- **Live demo:** <netlify URL once built>
- **Outreach:** <drafted YYYY-MM-DD / sent? — drafts file path>
- **Pricing offer:** <$0 setup / $79+/mo>
- **Decisions / notes:** <anything non-obvious>
- **$:** <none yet>
```
