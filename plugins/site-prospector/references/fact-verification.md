# Fact Verification — truth discipline before building or pitching

A demo for a real business carries claims (license, ratings, awards, years,
affiliations). Adam's standard is objective truth, not optimism: every claim is
**verified** or explicitly **labeled aspirational** — never asserted as fact when
it isn't. Getting this wrong embarrasses the prospect (and you) the moment it's
public.

## Contents
- [What to verify + where](#sources)
- [The entity-disambiguation trap](#trap)
- [Verified vs aspirational](#labeling)
- [The demo disclaimer](#disclaimer)

<a id="sources"></a>
## What to verify + where (state/trade-agnostic)
- **Trade / contractor license** — the state licensing board. (ST: the state licensing board at
  `example-business.com` — we found a *delinquent/expired* license that looked
  active on aggregators.) Other states: search "<state> contractor license
  lookup". Confirm: active, not expired, and the name/address match this
  business.
- **Business entity** — the secretary-of-state registry (ST: the state corporate registry). Confirm
  the LLC/Inc is **active** (we found an *inactive* one) and the owner matches.
- **BBB** — accreditation, rating, complaints (`bbb.org`).
- **Manufacturer "find a pro" locators** — for certifications (GAF Master Elite
  for roofing, Trane Comfort Specialist for HVAC, etc.). If a cert is claimed,
  confirm the business is actually listed. We found a Master Elite claim that was
  **not** in GAF's locator.
- **Review platforms** — Google, Yelp, BuildZoom, Angi. Get the *real* rating;
  don't round a 3.0 up to 5★ and call it fact.

<a id="trap"></a>
## The entity-disambiguation trap (this bites)
Common business names repeat across cities and owners. We hit it hard: a
*different* "a roofing client LLC" in another city, owned by a different person,
plus a **wrong license number** on a third-party aggregator. Before trusting any
record, confirm it's THIS business — match on **owner name + address + phone**,
not just the business name. When two records conflict, stop and resolve identity
before building anything.

<a id="labeling"></a>
## Verified vs aspirational
Tag every claim:
- **Verified** — confirmed at the authoritative source. Safe to state.
- **Aspirational** — plausible/claimed but unconfirmed (or confirmed false). On a
  *demo* it can be shown as "what the site could say," but it must not read as
  established fact, and the user confirms it before the site goes public. Surface
  these to the user explicitly.

Never manufacture confidence — if the rating is 4.3, the site says 4.3 (or the
user upgrades it knowingly), not 5.0.

<a id="disclaimer"></a>
## The demo disclaimer
Any demo built before the business has confirmed it carries a quiet, honest
footer line:
> Independent demonstration site — not officially affiliated with or endorsed by
> [Business].

This keeps the spec-build truthful and protects everyone until the owner adopts
it. `site-forge` applies this on prospector-driven demos by default.
