# Outreach — the free-spec-site cold pitch

The highest-converting web-design cold pitch is **mockup-first**: "I already
built it, here's the link." You're not asking for a meeting to maybe make
something — you're handing them a finished thing. Lead with the gift, keep it
short, one low-friction CTA, honest and no-pressure.

## Contents
- [The core pitch](#pitch)
- [Channel sequencing + cross-referencing](#sequence)
- [Timing + follow-up](#timing)
- [Copy rules (from cold-outreach-perm)](#copy)
- [Generating the drafts page](#page)

<a id="pitch"></a>
## The core pitch
One genuine, specific hook (their domain is parked; their FB has no site link;
their reviews praise X). The value in one breath: a modern, mobile site with
their story + a lead form, already live at a URL. The frame: "no catch — made it
as a demo to show what's possible; if you like it I'd make it yours." A
no-pressure exit ("if not, no worries"). One CTA: take a look + reply/call.

<a id="sequence"></a>
## Channel sequencing + cross-referencing
Reach out a couple of ways so it doesn't get buried — but **space them and
cross-reference** so it reads as thoughtful, not spammy:
1. **Facebook DM first** — most solo trades live on FB; most personal. Cold open.
2. **Email** (same day / next) — *references the DM*: "(I also messaged you on
   Facebook, so this doesn't get buried.)"
3. **Text** (2–3 days later, *only if no reply*) — references both: "I sent a FB
   message and an email earlier…"

Each later channel naming the earlier ones turns "3 cold blasts" into "one
persistent, considerate person." A text as a *cold open* reads as spam — it's a
nudge, not a first touch.

<a id="timing"></a>
## Timing + follow-up
- Best windows: early morning (~7–8am) or evening (~6–7pm) — not mid-day when a
  tradesperson is on a job. Tue–Thu.
- **One** gentle follow-up 3–4 days after the text if still nothing — then stop.
  Persistence ≠ pestering.

<a id="copy"></a>
## Copy rules (folded in from cold-outreach-perm)
- **Personalize the body, never the subject** for some verticals — for lawyers, a
  personalized subject cut open rates ~31%. Keep subjects plain and honest
  ("Built you a new website").
- **Don't announce the personalization creepily.** Never write "I used your photo"
  or "a photo of you and [their spouse]" — from a stranger that reads as
  surveillance. Reference their *story, work, and own words* (tagline, years,
  family-owned), and let them *discover* the personal touches (their photo, their
  quote) when they open the site. The site proves you did the homework; the
  message shouldn't sound like you've been collecting their pictures.
- Plain near-black text, system font, one CTA link; no heavy formatting (clients
  strip it; it also reads as marketing).
- **Value-first** — the gift (the live demo) before any ask.
- **Preview before send** — always show the user the exact draft; never auto-send.
  This skill drafts only; the user sends.

<a id="page"></a>
## Generating the drafts page
Run the generator to produce a copy-pastable HTML page (3 sequenced drafts with
Copy buttons, the order/timing, one follow-up, and a "fill in your phone/email"
banner):
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/outreach-page.sh \
  "Business Name" "https://<client>.netlify.app" \
  "owner@example-business.com" "<phone>" "their domain is parked" \
  ~/Desktop/outreach-business.html
```
It writes **outside** any deploy folder (the drafts are private — never deploy
them). Open it, fill in your own contact info, copy, send yourself.
