# Monetization — pricing & positioning

Honest framing first (Adam's standard): this model works, but it's a *volume*
game with low cold-conversion — not passive, not "minimal marketing." The
leverage is the reusable template (the next demo is ~45 min), not avoiding the
outreach grind.

## The model
- **Recurring beats one-time.** A one-time build ($500–1500) is quick cash but
  you're always hunting the next sale. The real game is **recurring ~$79–99/mo**
  (hosting + the lead form + small edits) — it compounds, and a static site needs
  almost no upkeep, so it's near-passive once live. Hosting cost ≈ $0 (Netlify
  free tier), so it's almost pure margin.
- **Low upfront friction.** Keep setup $0–300 so it's not a real decision; live
  on the recurring. A skeptical solo tradesperson balks at a $2k check, not at
  "$0 setup, $79/mo, cancel anytime, first month free."

## The math (toward the $1–5K/mo goal)
At ~$79–99/mo: **$1K/mo ≈ 12 clients · $3K ≈ 35 · $5K ≈ 55.** Cold conversion
runs ~1–5%, so 12–55 *sticking* clients means **hundreds** of pitches. Months of
grind, not a weekend. State this plainly; don't manufacture confidence about
"easy passive income."

## The agency ladder above the demo-site offer (added 2026-07-28)

The $79-99/mo above is the **demo-site** offer and it stays. Sitting on top of it is a
retainer ladder, validated against operators running it at volume (Kai Stone ~1,300 clients
at $200-500/mo; Juan 71 clients; Noah Igler at the $1.5m-client tier). Full detail in
`~/.claude/explanations/20260724_valstratis-replication/PLAYBOOK.html`, ranking method in
`SEO-PLAYBOOK.md` beside it.

| Tier | Price | Contents |
|---|---|---|
| **Basics** | $99/mo + $300-500 setup | GBP, website + SEO/local SEO, NAP/listings, Apple + Bing, **review system**, hosting/edits, monthly report |
| **Response** | $249-299/mo | + missed-call text-back, form auto-reply, chat-widget-to-SMS, call tracking. This is Kai Stone's $297 offer |
| **Systems** | $499/mo | + CRM, nurture, booking, photo-to-everywhere, automation |
| **Ads** | +$500-800/mo, client funds spend | Bolt-on, any tier, only once the basics convert |

**The rule that decides tier contents: recurring revenue requires recurring usage.**
Juan's $199/mo offer was killed on a call by *"why would I pay you every month for a website
you build once?"* The price did not fail, the justification did. Every tier needs at least
one thing the client personally touches monthly. At $99 that is the **review link** (costs
nothing to deliver, they use it constantly). Text-back moves up a tier because it carries
real cost: Twilio, per-message fees, and A2P registration taking days per client.

**Two numbers to plan against, not the headline ones:**
- **Churn runs 8-10%/month at low ticket** (Kai's own figure; the higher-ticket agency he
  was talking to runs 3%). You replace the whole base yearly, so retention work outranks
  acquisition sooner than feels natural.
- **Target 1:1 on acquisition:** spend up to one month's fee to win a client, since month
  two is margin. A beginner with no staff can genuinely hit this; at scale it gets hard.

**Commercial / B2B is a separate engagement, not a tier.** Everything above sells inbound
B2C. Commercial work (HOA and property management, GCs, facility managers) is outbound and
relationship-driven, so it prices as a setup project plus a **monthly outbound retainer**, at
Growth/Systems level or standalone. Sell it as "in front of the 60 people who control the
contracts in your county," never as lead flow. Qualify hard first: net-30-to-60 terms and a
$1M COI requirement disqualify most one-truck operators. Full method:
`references/commercial-b2b.md`.

**Setup fee is not optional at $99.** With a hand-built site and a ~10-12 month average
client life, no setup fee means you are underwater on the build for most of the
relationship. Either charge setup, or template the build down to hours.

## Tactics
- **Productize the template.** "$99/mo, modern site + leads, live in 24h," aimed
  at local trades with no working site (there are thousands). Volume + a tight
  pitch beats bespoke artistry per prospect.
- **First client = a test.** Land them or not; if they ghost (common for
  marketing-skeptical trades), move on fast. Don't over-invest in low-odds
  prospects — that's what the prospector pipeline is for.

## Paid ads as a tier — the gate (added 2026-07-29)

Do NOT add a paid-ads tier to the ladder without reading
`paid-ads-and-attribution.md`. The gate is **conversion volume, not price**.

Ad platforms need roughly **50 conversions per week** (Meta's documented learning-phase
threshold; Google Smart Bidding is comparable) before the algorithm can optimize at all.
A trade doing 30 jobs a month is an order of magnitude below that. Selling them ads is
selling a machine that cannot run.

- **Below the threshold → sell organic.** GBP + reviews is not a budget version of ads,
  it is the correct answer at that volume.
- **Above the threshold → closed-won feedback via CAPI is mandatory**, and it is the part
  actually worth charging for. Optimizing for form fills produces cheap junk leads and is
  why owners say "I tried Facebook ads and it didn't work."

If a prospect asks whether you feed closed-won data back via CAPI, the honest answer today
is **"neither, I don't run paid acquisition."** Say it plainly. Bluffing dies in two
follow-up questions.

## Competitor price benchmark: BadgerLayer (verified 2026-07-30)

A real, published, citable competitor price point for a small-business website. Full teardown:
`~/.claude/explanations/20260730_badgerlayer/`.

**a competitor agency** (Whitewater WI, ~2 people, brand <8 months old, domain created 2025-12-04):

| Tier | Price | Timeline |
|---|---|---|
| Starter — 5-7 pages | **$3,500** | 3-4 wks |
| Growth — ≤15 pages + headless CMS ("most common") | **$7,500** | 6-10 wks |
| Custom | **$15,000+** | 8-16 wks |
| Hosting + maintenance retainer (incl. **2 hrs/mo content changes**) | **$150/mo** | ongoing |

**Why this matters to our pricing:**
1. **It is a published number we can cite in a comparison table.** Most agencies hide behind
   "contact us"; BadgerLayer prints it. That makes the agency column of our own comparison table
   factual rather than a guess.
2. **A ~2-person shop under a year old, with no web portfolio and no web-relevant reviews, asks
   $3,500-$15,000 and reads credible** — because one well-built page does the work. The gap between
   them and us is packaging, not capability.
3. **They sell the CMS AND still do the edits** ($150/mo includes 2 hrs of content changes). That
   validates "content changes included in the monthly" as a retainer feature rather than a
   shortcoming. See site-forge `references/cms-options.md`.
4. **Different model, different failure mode.** Project + small retainer means cash upfront but the
   year restarts near zero; our subscription means no cash upfront but month 24 opens already
   booked. Do NOT read their pricing as a target for our tiers — read it as the number to put in
   the *agency* column.

**A CMS is a legitimate tier differentiator.** They gate it behind the $7,500 tier. If we ever add
a higher tier, an editor login is a defensible thing to gate — but only per the cms-options.md bar
(client publishes regularly, has staff who will use it, or explicitly asks and pays).

## The market rate is now confirmed by two independent operators (2026-07-30)

| Operator | Location | Setup | 5-8 page small-business site |
|---|---|---|---|
| **BadgerLayer** | Whitewater, WI | 2 people, web is a side line | **$3,500 – $7,500** |
| **Liquid Agency** | Milano, IT | **1 person, gmail contact address** | **€3,500 – €7,000** |

Two solo-ish operators, two continents, no contact with each other, **the same number**. That is no
longer a data point — treat **~$3,500–7,500 as the market rate for a custom small-business site**,
and use it as the figure in the *agency* column of our comparison table.

**Liquid also proves the ceiling is not gated on apparatus.** One person, no team, no office, and
a **gmail address** as the published business contact, charging €3,500–7,000 with a ~60% demo
conversion rate. The credibility is carried entirely by surface area (51 pages) and writing
quality. Nothing structural is stopping us from the same band.

**Their pricing is published in a GUIDE, not on a pricing page** — `/risorse/quanto-costa-sito-web-2026`,
opening with *"90% of articles about website cost are written to get you to call the agency. This
one isn't."* Then a budget breakdown (strategy+copy 25-35%, design 20-30%, dev 25-35%, technical SEO
5-10%, PM 10-15%) and — the strongest trust move on either competitor's site — **a "what should NOT
cost extra" list**: SSL, sitemap/robots.txt, base schema, automatic backups, mobile responsive.
**Naming what the industry overcharges for buys more credibility than a testimonial**, and we can be
more specific than he is because we actually ship all five.

## Missed-call text-back tier — real economics and the prerequisite angle (2026-07-30)

Full detail: site-forge `references/twilio-a2p-10dlc.md`.

**Per client: ~$19 one-time (brand $4 + campaign vetting $15), then ~$3-12/mo** (campaign $1.50-10,
number $1.15, ~$0.011 per text all-in). Against a $99-$499/mo tier that is **1-12% of revenue**.
Twilio bills our account; it is marked up into their monthly. **Cost is not the constraint.**

**The constraint is time:** brands approve in minutes, **campaigns take SEVERAL WEEKS of manual
vetting**. Never promise text-back live in the first month. Start registration the day they sign.

**🔑 THE PREREQUISITE ANGLE — use this on every text-back pitch.** Two A2P registration fields are
things our prospects do not have: **a live website matching the business name**, and **a business
email on a real domain** (free/personal domains get rejected, and our entire pipeline is gmail).

> "You can't legally text your customers back without a website and a business email on your own
> domain. I do both, and then I turn the texting on."

It is true, not a sales device, and it converts the website from optional to mandatory. **It also
sequences the ladder for us**: website first (because it must come first), text-back second.

**Scaling trap to design around now:** brand registrations must carry **the client's** email and
address. Use ours and the whole business caps at **10 clients**, ecosystem-wide, with no warning.
