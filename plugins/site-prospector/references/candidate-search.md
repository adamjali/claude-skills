# Candidate Search — finding local businesses worth a free demo site

> **SUPERSEDED (2026-07-23, amended 2026-07-28). Do not scout from this file.**
> The canonical scope, gates, and 0-100 rubric now live in `scouting-doctrine.md`.
> This file is kept for its funnel/targeting reasoning and its honest-presentation
> guidance only. Anything here about *which* businesses to pick, what geography to
> cover, or how to score is out of date — in particular this file predates the tiered
> review/the state corporate registry bands, gates G1-G4, Factor G (proved demand), and the 2026-07-28
> finding that new filings are spam-saturated.

Find businesses that would genuinely benefit from a new site, so the pitch
writes itself. The whole funnel's conversion lives or dies on *targeting* —
"good cold outreach is 80% targeting, 20% copy." A great-fit candidate with a
mediocre message beats a poor-fit candidate with a perfect one.

## Contents
- [Where to look](#where)
- [The signals — strongest first](#signals)
- [The evaluation rubric](#rubric)
- [Presenting candidates honestly](#present)

<a id="where"></a>
## Where to look
- **Maps / local listings** — Google Maps, Apple Maps, Yelp, Nextdoor, the BBB
  directory, Angi/Thumbtack for a trade + area. These surface name, phone,
  rating, and crucially whether a website link exists.
- **jina search** (Adam's token lives in `~/.claude/skills/jina-image-search/`
  and `~/.claude/CLAUDE.md`; export it as `JINA_TOKEN` or use the
  `jina-image-search` skill):
  ```bash
  curl "https://s.jina.ai/?q=roofers+in+Apollo+Beach+<state>" \
    -H "Authorization: Bearer $JINA_TOKEN" -H "X-Respond-With: no-content"
  ```
- **jina read** to scrape a listing / FB page / parked domain for owner name,
  contacts, story, reviews:
  ```bash
  curl "https://r.jina.ai/https://example-business.com" -H "Authorization: Bearer $JINA_TOKEN"
  ```
- **Facebook / Instagram** — many solo trades run their whole presence on FB
  with no website. That's the ideal candidate.
- For 3+ queries, hand off to the `researcher` agent to keep main context clean.

<a id="signals"></a>
## The signals — strongest first
1. **No working website, or a parked/for-sale domain.** The #1 signal. If their
   listed domain is dead, parked, or a registrar lander, you have a genuine,
   honest hook ("your site isn't live, so I built you one"). Verify by actually
   loading the domain — don't assume. (Several dead domains = an even stronger
   hook — but read it alongside #2.)
2. **Still active — recent signs of life.** The trap the a roofing client case taught:
   a business can look *perfect* (no site, real history, years in business) yet
   be **dormant or winding down**. Check *recency*, not just existence — recent
   reviews (last ~12–18 months), recent social posts, a **current, non-delinquent
   license**. Stale-everything (last review years ago, no posts since 20XX,
   lapsed license, *plus* parked domains) = likely semi-retired or defunct:
   **disqualify**, however good the no-site hook looks. A live pitch needs a
   live business. Online dormancy alone isn't proof (referral trades neglect
   the web), but *operational* staleness — lapsed license, reviews dried up — is
   the tell.
3. **Real reputation** — reviews (even mixed), years in business. Mixed is fine;
   *no* footprint is the red flag (possibly defunct).
4. **Solo / small / local** — owner-operated trades (roofing, HVAC, fencing,
   pool, landscaping, plumbing, detailing…). They decide alone (no committee),
   and a site visibly helps them.
5. **Reachable** — a findable email, FB page, or cell. Contact-channel access is
   what makes outreach possible at all.
6. **A current modern site → skip.** No wedge if they're already well-served.
   Move on fast; don't burn effort on a low-odds pitch.

<a id="rubric"></a>
## The evaluation rubric
Score each candidate to *sort* them (rough banding, not precision):

| Factor | Weight | Look for |
|---|---|---|
| No-website hook | High | Dead/parked/no domain >> outdated site >> decent site (skip) |
| Still active (recency) | High | Recent reviews/posts + current license; dormancy/lapsed license = disqualify |
| Reputation reality | Med | Exists, some reviews, years in business; not defunct |
| Fit | Med | Solo/local trade; decision-maker reachable |
| Ease | Med | Public photos/story to build from; clear service area |
| Channel access | High | Direct email / FB DM / cell >> contact form only |

Banding: **strong** (dead domain + reachable + real) → build first ·
**moderate** (outdated site, or thin contact) → maybe · **skip** (modern site,
no footprint, or unreachable).

<a id="present"></a>
## Presenting candidates honestly
When you surface candidates for the user to pick, lead with the truth, not a
sales pitch (Adam's standard — objective, lean-skeptical, no manufactured
confidence). For each, give: the hook (why them), the reputation reality
(warts included), the fit, and the catch. Surface weak candidates *as weak* —
don't inflate a thin lead to pad the list. The user picks; your job is an honest
board, not a hype reel.
