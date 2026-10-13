# Paid ads, conversion tracking & closed-won attribution

Written 2026-07-29 after Adam was asked, cold: *"Are you feeding CRM closed-won data
back via CAPI, or just optimizing for form fills?"*

That question is a **competence probe**. Whoever asks it already knows the answer they
want to hear, and they are checking whether you actually run performance marketing or
only build lead forms. Read this before answering anyone on paid acquisition.

---

## 1. The question in plain language

> "When someone becomes an actual paying customer, do you tell the ad platform about it?
> Or do you only tell it that somebody filled out a form?"

---

## 2. The vocabulary, built up

**Pixel.** A small piece of JavaScript in the page that watches what visitors do and
reports it to the ad platform **from the browser**. This was the original method and it
has degraded badly: iOS App Tracking Transparency, ad blockers, and Safari's cookie
limits all eat browser-side tracking.

**CAPI — Conversions API.** Meta's answer to that decay. Your **server** sends events
directly to Meta's server, with no browser in the path, so it survives everything above.
Google's equivalents are **Enhanced Conversions for Leads** and **offline conversion
import**. "CAPI" is Meta's name but people use it loosely for the whole server-side idea.

**CRM.** Customer relationship management system — the database where leads live.

**Closed-won.** CRM stage vocabulary. Deals move New → Contacted → Quoted → then either
**Closed Won** (they paid) or Closed Lost. **Closed-won is the only stage that means
money.**

**Click ID.** The identifier appended to your URL when someone clicks an ad: **`fbclid`**
for Meta, **`gclid`** for Google. This is the thread that ties a later sale back to the
original ad.

Put together, **"feeding closed-won data back via CAPI"** means: when a deal is finally
marked paid, your server tells the ad platform *this specific person, from this specific
ad click, produced real revenue.*

---

## 3. Why the distinction is the entire question

**Ad platforms optimize toward whatever signal you feed them, and they are ruthlessly
literal about it.**

- Optimize for **form fills** → the platform finds you people who fill out forms. That is
  a genuinely different population from people who buy: bored browsers, price shoppers,
  bots, and serial form-fillers. Cost-per-lead drops, the dashboard looks great, revenue
  does not move.
- Optimize for **closed-won** → the objective becomes "find more people like the ones who
  actually paid." Cost-per-lead often goes **up**, and that is correct. You are buying
  fewer, better leads.

This is the single most common failure in small-business paid advertising, and it is why
so many owners say "I tried Facebook ads and got a bunch of junk leads." They were not
lied to. They optimized for junk and got it.

---

## 4. The mechanics

1. Someone clicks the ad. The URL picks up `fbclid` / `gclid`.
2. They submit the form. **You store that click ID alongside their email and phone in the
   CRM.** ⚠️ **This is where most setups fail.** No stored click ID means no match, ever,
   and everything downstream becomes impossible. It cannot be retrofitted after the fact.
3. Weeks later, a salesperson marks the deal Closed Won for $4,200.
4. Your server sends the platform an event: hashed email, hashed phone, click ID, event
   name, value $4,200.
5. The platform matches it to the original click and retrains.

**Two details that separate working setups from broken ones:**

- **Deduplication.** If the pixel and CAPI both report the same event, pass a shared
  `event_id` so it is not double-counted.
- **Event match quality.** The platform's score for how confidently it can tie your server
  event to a real person. More identifiers (email, phone, name, IP, user agent) means
  higher match rates.

**Attribution windows** do limit how late a sale can be reported, and the specific numbers
change. **Check current platform docs rather than quoting a figure from memory.**

---

## 5. What this means for Adam's operation

### 5a. The honest answer is "neither" — and that is a fine answer

The current stack is **organic**: Google Business Profile, local SEO, reviews, missed-call
text-back. There is no ad spend to optimize.

If a prospect asks this, **do not bluff.** Say:

> "I don't run paid acquisition. I do organic local visibility — Google Business Profile,
> local SEO and reviews. If you're running paid, closed-won feedback is the right way to
> do it, but it isn't what I'm selling you."

Faking the other answer collapses in two follow-up questions and costs the whole
relationship. This is the same truth-discipline rule that governs reviews and licensing
claims.

### 5b. The volume threshold: why NOT to sell this to trades

**This is the objective reason to decline the work, not an excuse.**

Meta's own documented guidance is that an ad set needs roughly **50 conversions per week**
to exit the learning phase and optimize properly. Google's Smart Bidding wants comparable
volume (its published guidance has historically been in the tens of conversions per month
minimum for Target CPA).

A junk removal operator doing **30 jobs a month** will never come close. Feed a closed-won
signal into an algorithm at that volume and it has nothing to learn from. **The machinery
is built for businesses with hundreds of monthly conversions.**

So for a solo trade the honest recommendation stays what it already is: **GBP and reviews**.
That is not a smaller version of paid ads, it is the correct answer at that volume.

**If a paid-ads tier is ever added to the ladder** (see `monetization.md`), the volume
threshold is the gate. Below ~50 conversions/week, sell organic. Above it, closed-won
feedback is mandatory and is the thing worth charging for.

### 5c. The principle already runs this operation

**The 2026-07-29 converting-lead analysis was closed-won feedback done by hand.**

79 calls → 5 interested, 19 declined. Rather than optimizing for leads that looked good on
paper, the actual converters were examined for what they had in common: established trade,
zero or one review, no GBP, hustling on rented platforms. The scoring rubric was then
rewritten around that. **Factor G was scoring proven demand by review count, which was
actively penalizing the best prospects in the pipeline** (it gave a junk-removal client 3/15). See
`scouting-doctrine.md` section 2d.

That is exactly what CAPI automates: take outcome data, feed it back, change the targeting.
The lesson generalizes well beyond ads:

> **Optimize on the outcome you are paid for, never on the proxy that is easy to measure.**
> Form fills, interested calls, impressions, and traffic are all proxies. Closed-won is
> the outcome.

Applied to prospecting: **judge a lead source by the deals it closes, not the calls it
produces.** Nextdoor and Facebook groups earn their place because a junk-removal client, a lawn-care client,
a lawn-care client and a landscaping client came from there, not because they are easy to search.

---

## 6. Related jargon likely to appear in the same conversation

| Term | What it means |
|---|---|
| **Lookalike audience** | Platform finds users resembling a seed list. Quality is capped by the seed: a closed-won seed beats a form-fill seed. |
| **Offline conversion import** | Uploading real-world sales (phone, in-person) back to the platform. The non-API version of the same idea. |
| **Server-side GTM** | Google Tag Manager running on your server instead of the browser. Common plumbing for CAPI-style setups. |
| **Match rate** | Share of your uploaded records the platform successfully ties to a user. Low match rate makes the whole loop weak. |
| **Learning phase** | Period where the algorithm has too little conversion data to optimize. The ~50/week threshold above. |
| **CPL vs CAC** | Cost per lead vs cost to acquire a paying customer. Optimizing CPL while CAC rises is the exact failure this page describes. |
| **Attribution window** | How long after a click a conversion still counts. Limits how late closed-won data can be reported. |

---

## 7. One-line summary to remember

**You get what you optimize for. Form fills are a proxy; closed-won is the outcome. And
below roughly 50 conversions a week, none of this machinery works at all — which is why
local trades get GBP and reviews, not ads.**
