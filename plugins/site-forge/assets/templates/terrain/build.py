#!/usr/bin/env python3
"""Generate the full page set, reusing index.html's chrome verbatim.

Mirrors the reference site's information architecture: service HUB pages with
NESTED sub-service pages under them, plus about / gallery / areas / contact /
legal. index.html is hand-maintained and is the only source of <style>, the
utility bar, the nav and the footer, so the chrome cannot drift.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SITE = "https://<client>.netlify.app"   # set to the client's deployed hostname
PHONE, PHONE_HREF = "<phone>", "tel:+18134160394"

SRC = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
UTIL = re.search(r'<div class="util">.*?</div>\s*</div>', SRC, re.S).group(0)
NAV = re.search(r'<nav class="nav".*?</nav>', SRC, re.S).group(0)
FOOT = re.search(r'<footer class="foot">.*?</footer>', SRC, re.S).group(0)
JS = re.search(r"<script>\n\(function\(\)\{.*?</script>", SRC, re.S).group(0)

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/>'
         '<path d="M8 12.5l2.6 2.6L16 9.5"/></svg>')
WAVE = ('<div class="wave"><svg viewBox="0 0 1440 110" preserveAspectRatio="none" aria-hidden="true">'
        '<path fill="#fff" d="M0,54 C220,110 420,6 720,44 C1010,80 1220,18 1440,52 L1440,110 L0,110 Z"/>'
        '</svg></div>')

# ---------------------------------------------------------------- content
PAGES = [
    # ---- LAWN CARE hub + nested ----
    dict(slug="lawn-care", parent=None, nav="Lawn Care",
         title="Lawn Care in the metro, ST | Mowing, Edging &amp; Shrub Trimming",
         h1="Lawn Care", img="mowing-src.jpg",
         desc="Weekly and fortnightly lawn care across the metro. Mowing from $40, edging, blow-down and shrub trimming.",
         lede="A cut, a clean edge and every hard surface blown down before we leave. Weekly, fortnightly, or a one-off reset on a yard that got away from you.",
         body_h="Cutting Height Matters More Than Cutting Often",
         body=("Most thinning the metro lawns were not underwatered, they were scalped. St. Augustine covers "
               "the majority of yards here, spreads sideways by runners, and needs holding at three and a "
               "half to four inches. Cut it shorter and you open gaps that weeds fill within a fortnight. "
               "Bahia on the larger unirrigated lots is tougher, but it throws seed heads within days of a "
               "cut through summer, so it goes untidy on a schedule rather than at random."),
         checks=[("Set the Deck to the Grass:", "St. Augustine stays high, Bahia can go slightly lower. The blade height changes before the first pass."),
                 ("Cut, Then Edge, Then Blow:", "Edging after the cut keeps the line crisp, and blowing last means the driveway is clean when we pull off."),
                 ("Vary the Direction:", "Repeating the same line every visit trains ruts into soft my state sand.")],
         children=["mowing-edging", "shrub-trimming"]),
    dict(slug="mowing-edging", parent="lawn-care", nav="Mowing &amp; Edging",
         title="Lawn Mowing &amp; Edging in the metro, ST from $40",
         h1="Mowing &amp; Edging", img="mowing-src.jpg",
         desc="Lawn mowing and edging from $40 across the metro, a coastal city, Riverview and a nearby town.",
         lede="From $40 for a standard residential lot: mowed, edged, and blown down front and back.",
         body_h="What the $40 Actually Covers",
         body=("A standard residential lot, mowed front and back, edged along every driveway, walkway and "
               "bed line, with the clippings blown off the hard surfaces rather than left to wash into the "
               "storm drain. Larger lots, steep ground and a first cut on badly overgrown grass all cost "
               "more, which is why a photo gets you a real number instead of a range."),
         checks=[("Bag or Mulch:", "Mulching returns nitrogen to the soil and is better for the lawn. Bagging looks tidier and is the right call on a first cut."),
                 ("The One-Third Rule:", "Never more than a third of the blade height in one pass. Taking more is what browns a lawn out after a cut."),
                 ("Recurring Stays Fixed:", "Weekly and fortnightly visits hold the agreed rate rather than being re-quoted each time.")]),
    dict(slug="shrub-trimming", parent="lawn-care", nav="Shrub Trimming",
         title="Shrub &amp; Hedge Trimming in the metro, ST",
         h1="Shrub &amp; Hedge Trimming", img="edging-src.jpg",
         desc="Hedge and shrub trimming across the metro, shaped back off walls and windows with clippings hauled away.",
         lede="Hedges and shrubs cut back off the walls, windows and walkways, with the clippings taken away rather than bagged at the kerb.",
         body_h="Why Growth Against a Wall Is a Moisture Problem",
         body=("Anything pressed against a wall traps humidity where it cannot dry, and in a climate that "
               "spends half the year humid that means mildew on the render and a bridge for insects into "
               "the house. A hand's width of clearance solves it. The other half of the job is shape: a "
               "hedge cut slightly wider at the base than the top lets light reach the bottom, which is "
               "the only thing that stops it going bare at knee height."),
         checks=[("Structure First:", "Anything dead or crossing comes out before the outside gets shaped."),
                 ("Wider at the Base:", "Light reaches the lower growth and the hedge stays full instead of going leggy."),
                 ("Clippings Leave With Us:", "Hedge clippings are bulky and are not something to leave for kerbside collection.")]),

    # ---- TREE CARE hub + nested ----
    dict(slug="tree-care", parent=None, nav="Tree Care",
         title="Tree Care in the metro, ST | Trimming, Palms &amp; Storm Cleanup",
         h1="Tree Care", img="tree-trimming-src.jpg",
         desc="Tree trimming from $125, palm work and storm cleanup across the metro. Debris hauled the same visit.",
         lede="Limbs off the roofline, palms tidied, storm damage cleared. The debris leaves with us rather than sitting at the kerb for a week.",
         body_h="The Haul-Away Is the Part That Gets Quoted Badly",
         body=("Trimming a tree takes an hour. Getting the pile off the property is what eats the day, and "
               "it is the line most quotes leave vague. Central my state makes it worse: an afternoon storm "
               "drops more limb weight in twenty minutes than a scheduled trim produces, and palm fronds "
               "are bulky out of all proportion to what they weigh. Everything quoted here includes taking "
               "it away."),
         checks=[("Access Before Height:", "Whether the trailer can get within reach moves the price more than the size of the tree does."),
                 ("Cut to the Collar:", "Flush cuts and stubs both invite rot. The cut goes just outside the branch collar so it seals."),
                 ("Cleared as We Go:", "The pile is loaded through the job rather than left to the end.")],
         children=["tree-trimming", "palm-trimming", "storm-cleanup"]),
    dict(slug="tree-trimming", parent="tree-care", nav="Tree Trimming",
         title="Tree Trimming in the metro, ST from $125",
         h1="Tree Trimming", img="tree-trimming-src.jpg",
         desc="Tree trimming and limb removal from $125 across the metro, debris hauled away the same visit.",
         lede="From $125. Limbs cut back off roofs, drives and fences, with everything loaded and gone before we leave.",
         body_h="What Moves the Price on a Tree",
         body=("Three things, in order: how close the trailer can park, what is sitting underneath the "
               "limbs, and how much material comes down. Height matters far less than people expect. A "
               "modest tree over a pool cage costs more than a taller one over open lawn, because every "
               "cut has to be roped and lowered rather than dropped."),
         checks=[("Send the Whole Tree:", "A photo showing the tree and its surroundings prices far better than a close-up of the branch."),
                 ("Roof Clearance:", "Limbs touching a roof abrade shingles every time the wind blows and are worth cutting back before they cost you a repair."),
                 ("Haul-Off Included:", "It is in the quoted price, not billed separately afterwards.")]),
    dict(slug="palm-trimming", parent="tree-care", nav="Palm Trimming",
         title="Palm Trimming &amp; Frond Removal in the metro, ST",
         h1="Palm Trimming", img="tree-trimming-src.jpg",
         desc="Palm frond and seed pod removal across the metro, timed before hurricane season.",
         lede="Browned fronds and seed pods down and hauled off, timed so the palm is not weakened going into storm season.",
         body_h="A Good Palm Trim Takes Less Than People Expect",
         body=("The instinct is to strip a palm back to a narrow tuft, and it is the wrong instinct. Green "
               "fronds still above horizontal are feeding the tree, and removing them weakens it exactly "
               "when it needs the reserves to hold up in a storm. What comes off is the browned and "
               "hanging material and the seed pods, which are the parts that actually fall and make a mess."),
         checks=[("Timing:", "Once the fronds brown off and before hurricane season is properly underway."),
                 ("Seed Pods:", "They are the messiest part of a palm and the reason most people call in the first place."),
                 ("Everything Leaves:", "Fronds are bulky and awkward. They go on the trailer, not to the kerb.")]),
    dict(slug="storm-cleanup", parent="tree-care", nav="Storm Cleanup",
         title="Storm Debris Cleanup in the metro, ST",
         h1="Storm Cleanup", img="junk-removal-src.jpg",
         desc="Storm and hurricane debris clearing across the metro, loaded by hand and hauled off.",
         lede="Downed limbs, split trees and the debris field a my state afternoon can leave behind, cleared and taken away.",
         body_h="Why Skip Availability Collapses Exactly When You Need One",
         body=("After a storm, every hire yard in the core metro county is booked out at the same moment, and kerbside "
               "collection backs up for weeks. A crew that turns up, loads by hand and leaves with the pile "
               "the same visit is not competing for that queue. It also gets the hazard off your property "
               "before the next band of weather arrives."),
         checks=[("Hazards First:", "Anything leaning on a structure or a line gets assessed before anything is moved."),
                 ("Loaded by Hand:", "Nothing needs dragging to the kerb first, including from a back garden."),
                 ("Swept Before We Go:", "The area is cleared down rather than left as a debris outline.")]),

    # ---- CLEANUPS hub + nested ----
    dict(slug="cleanups", parent=None, nav="Cleanups",
         title="Yard Cleanups &amp; Junk Removal in the metro, ST",
         h1="Cleanups &amp; Haul-Off", img="junk-removal-src.jpg",
         desc="Yard waste, junk removal and pressure washing across the metro. Loaded and gone the same visit.",
         lede="Yard waste, old furniture and the pile in the side yard that has been there since you moved in. Loaded by hand and gone the same visit.",
         body_h="Cheaper Than a Skip for Almost Everything",
         body=("A skip means a permit conversation if it goes on the street, a week of it occupying the "
               "driveway, and you doing all the loading. For anything short of a full renovation, a crew "
               "that arrives, loads and leaves with the pile the same day is both cheaper and finished "
               "sooner. You point at what goes and you do not lift anything."),
         checks=[("Priced by Volume:", "How much space it takes on the trailer, not by weight or by the hour."),
                 ("No Kerbside Staging:", "It is carried out from wherever it sits, garage or back garden included."),
                 ("Swept After:", "There should be no outline left where the pile was.")],
         children=["junk-removal", "pressure-washing"]),
    dict(slug="junk-removal", parent="cleanups", nav="Junk Removal",
         title="Junk Removal &amp; Yard Waste Haul-Off in the metro, ST",
         h1="Junk Removal", img="junk-removal-src.jpg",
         desc="Furniture, appliance and yard waste removal across the metro, loaded by hand.",
         lede="Furniture, appliances, garage clear-outs and yard waste, carried out and hauled off in one visit.",
         body_h="What We Will and Will Not Take",
         body=("Household items, furniture, appliances, yard waste, storm debris, fence and deck material "
               "and general clear-out contents all go on the trailer. Paint, chemicals and hazardous "
               "material do not, because they need proper disposal through a facility rather than a "
               "trailer. If you are unsure, send a photo and you will get a straight answer."),
         checks=[("Garage and Shed Clear-Outs:", "The most common call, and usually a single visit."),
                 ("Appliances Included:", "Fridges, washers and the like are normal, not an exception."),
                 ("Same Visit as the Yard:", "Pairing it with a cut is the cheapest way to do it, since it is one trip.")]),
    dict(slug="pressure-washing", parent="cleanups", nav="Pressure Washing",
         title="Pressure Washing Driveways &amp; Patios in the metro, ST",
         h1="Pressure Washing", img="pressure-washing-src.jpg",
         desc="Driveway, walkway, patio and pool deck pressure washing across the metro.",
         lede="Driveways, walkways, patios and pool decks brought back to the colour they actually are underneath.",
         body_h="my state Concrete Goes Green, Not Grey",
         body=("That dark film on a the metro driveway is usually not dirt, it is living growth. Algae and "
               "mildew thrive on shade, humidity and near-daily summer rain, and they root into the pores "
               "of the concrete. That is why sweeping and hosing achieves nothing, and why it returns "
               "faster on the north side of a house where the surface never fully dries between storms."),
         checks=[("Pressure Matched to Surface:", "Concrete takes real pressure. Pavers, paint and older render do not, and forcing it causes damage that cannot be undone."),
                 ("Overlapping Passes:", "What avoids the striped look that gives away a rushed job."),
                 ("Run-Off Rinsed:", "Surrounding areas get rinsed so dirty water does not dry back onto clean surfaces.")]),

    # ---- standalone service ----
    dict(slug="mulch-and-beds", parent=None, nav="Mulch &amp; Beds",
         title="Mulch &amp; Flower Bed Maintenance in the metro, ST",
         h1="Mulch &amp; Flower Beds", img="mulch-src.jpg",
         desc="Bed edging, weeding and fresh mulch across the metro. The cheapest change that makes a front yard look maintained.",
         lede="Beds cut back to a clean edge, weeded out and topped with fresh mulch. Pound for pound the biggest visual change on a front yard.",
         body_h="Mulch Depth Is the Whole Job",
         body=("Laid too thin it does nothing, and piled too thick it does harm. Two to three inches "
               "suppresses weeds and holds moisture in sand that otherwise drains almost immediately. Past "
               "four inches it starts shedding water instead of absorbing it, and piled against trunks it "
               "holds damp on the bark and invites rot. my state sand and heat make the depth matter more "
               "here than in most of the country."),
         checks=[("Cut Edge First:", "A defined edge is what reads as maintained from the kerb."),
                 ("Weeded Before, Not After:", "Mulching over live weeds buys a few weeks before they push through."),
                 ("Off the Trunks:", "Pulled back from trunks and stems rather than volcano-piled.")]),
]

AREAS = ["the metro", "a coastal city", "Riverview", "a nearby town", "Seffner", "a nearby town"]
BY_SLUG = {p["slug"]: p for p in PAGES}


def url_of(p):
    return f"/{p['parent']}/{p['slug']}/" if p["parent"] else f"/{p['slug']}/"


def crumbs(p):
    out = ['<a href="/">Home</a>']
    if p["parent"]:
        par = BY_SLUG[p["parent"]]
        out.append(f'<a href="/{par["slug"]}/">{par["nav"]}</a>')
    out.append(f'<span>{p["nav"]}</span>')
    return ' <em>/</em> '.join(out)


def related(p):
    if p.get("children"):
        items = [BY_SLUG[c] for c in p["children"]]
        head = "Explore " + p["nav"]
    else:
        items = [q for q in PAGES if q["slug"] != p["slug"] and not q["parent"]][:3]
        head = "Other Services"
    cards = "".join(
        f'<a class="card" href="{url_of(q)}"><img src="/assets/{q["img"]}" alt="" loading="lazy">'
        f'<div class="card-t"><h3>{q["nav"]}</h3><span class="arrow">{ARROW}</span></div></a>'
        for q in items)
    return (f'<section class="band tint"><div class="wrap">'
            f'<div class="center"><p class="eyebrow c" style="color:var(--green)">Keep Looking</p>'
            f'<h2>{head}</h2></div><div class="cards">{cards}</div></div></section>')


def shell(title, desc, url, body, extra_ld=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | a lawn-care client</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{url}">
<meta name="theme-color" content="#0E803F">
<meta property="og:title" content="{title} | a lawn-care client">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://example-business.com">
<link rel="preconnect" href="https://example-business.com" crossorigin>
<link rel="stylesheet" href="https://example-business.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,500&family=Roboto:wght@400;500;700&display=swap">
{extra_ld}
<style>{CSS}
/* inner-page hero: same device as home, reduced height */
.phero{{position:relative;background:#123;overflow:hidden}}
.phero .hero-bg::after{{background:linear-gradient(90deg,rgba(0,0,0,.84) 0%,rgba(0,0,0,.6) 50%,rgba(0,0,0,.25) 100%)}}
.phero .wrap{{position:relative;z-index:2;padding-block:clamp(56px,7vw,92px) clamp(84px,10vw,130px)}}
.phero h1{{color:#fff;max-width:18ch}}
.crumb{{font-size:.8125rem;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.82);margin-bottom:14px;font-weight:700}}
.crumb em{{font-style:normal;opacity:.5;margin:0 4px}}
.crumb a:hover{{color:#fff}}
.faqs{{margin-top:34px}}
.faqs details{{border:1px solid var(--line);border-radius:8px;margin-bottom:12px;background:#fff}}
.faqs summary{{cursor:pointer;padding:18px 22px;font-family:var(--serif);font-size:1.18rem;color:var(--ink);
  list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center;font-weight:700}}
.faqs summary::-webkit-details-marker{{display:none}}
.faqs summary::after{{content:"+";color:var(--green);font-size:1.5rem;flex:none;transition:transform .2s}}
.faqs details[open] summary::after{{transform:rotate(45deg)}}
.faqs p{{padding:0 22px 20px;margin:0;font-size:.9375rem;color:var(--muted)}}
</style>
</head>
<body>
{UTIL}
{NAV}
{body}
{FOOT}
{JS}
</body>
</html>"""


def service_page(p):
    checks = "".join(
        f'<li>{CHECK}<span><b>{t}</b> {d}</span></li>' for t, d in p["checks"])
    faqs = [
        (f"How much does {re.sub('&amp;', 'and', p['nav']).lower()} cost in the metro?",
         f"Mowing starts at $40 and tree work at $125. Everything else is quoted from a photo. Text one to {PHONE} and a real number comes back, usually the same day."),
        ("Do I need to be home?",
         "No. Send a photo, agree the price in the same thread and leave the gate unlocked. Most customers are at work when the work happens."),
        ("Which areas do you cover?",
         "the metro, a coastal city, Riverview, a nearby town, Seffner and a nearby town. If you are near the edge of that it is still worth asking."),
        ("How do I pay?",
         "Card or app once the work is finished. Recurring visits stay on the agreed rate rather than being re-quoted."),
    ]
    faq_html = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(faqs))
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs]}, separators=(",", ":"))

    body = f"""
<header class="phero">
  <div class="hero-bg"><img src="/assets/{p['img']}" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <p class="crumb">{crumbs(p)}</p>
    <h1>{p['h1']}</h1>
    <p class="sub" style="font-family:var(--serif);font-style:italic;color:#fff;max-width:54ch;margin-top:14px">{p['lede']}</p>
    <div class="hero-btns" style="margin-top:28px">
      <a class="btn btn-red" href="/contact/">Get a Free Estimate</a>
      <a class="btn btn-outline" href="{PHONE_HREF}">{PHONE}</a>
    </div>
  </div>
  {WAVE}
</header>

<section class="band">
  <div class="wrap split">
    <div class="media rv"><div class="m-arch"><img src="/assets/{p['img']}" alt="{p['h1']}" loading="lazy"></div></div>
    <div class="rv">
      <h2>{p['body_h']}</h2>
      <p class="muted">{p['body']}</p>
      <ul class="checks">{checks}</ul>
      <a class="btn btn-red" href="/contact/">Book Your Free Site Visit</a>
    </div>
  </div>
</section>

<section class="band tint">
  <div class="wrap">
    <div class="center rv"><p class="eyebrow c" style="color:var(--green)">Questions</p><h2>Straight Answers</h2></div>
    <div class="faqs">{faq_html}</div>
  </div>
</section>

{related(p)}

<section class="band formband">
  <div class="wrap center rv">
    <p class="eyebrow c" style="color:#fff">Free Estimate</p>
    <h2>Send a Photo, Get a Number Back</h2>
    <p class="lead" style="margin-inline:auto">A picture and a street name is enough, usually the same day.</p>
    <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:24px">
      <a class="btn btn-red" href="/contact/">Get a Free Estimate</a>
      <a class="btn btn-outline" href="sms:+18134160394">Text a Photo</a>
    </div>
  </div>
</section>
"""
    return shell(p["title"], p["desc"], url_of(p), body,
                 f'<script type="application/ld+json">{ld}</script>')


def simple_page(slug, title, desc, h1, lede, img, inner):
    body = f"""
<header class="phero">
  <div class="hero-bg"><img src="/assets/{img}" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <p class="crumb"><a href="/">Home</a> <em>/</em> <span>{h1}</span></p>
    <h1>{h1}</h1>
    <p class="sub" style="font-family:var(--serif);font-style:italic;color:#fff;max-width:54ch;margin-top:14px">{lede}</p>
  </div>
  {WAVE}
</header>
{inner}
"""
    return shell(title, desc, f"/{slug}/", body)


def main():
    written = []
    for p in PAGES:
        d = ROOT / (f"{p['parent']}/{p['slug']}" if p["parent"] else p["slug"])
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(service_page(p), encoding="utf-8")
        written.append(url_of(p))

    # ---- about ----
    about_inner = f"""
<section class="band"><div class="wrap split">
  <div class="media rv"><div class="m-circle"><img src="/assets/edging-src.jpg" alt="Yard work in progress" loading="lazy"></div></div>
  <div class="rv">
    <h2>A Small Crew That Publishes Its Prices</h2>
    <p class="muted">a lawn-care client is a local the metro operation covering both sides of the bay. The work is
      lawn care first, with tree trimming, mulch, pressure washing and haul-off on the same visit so a property
      is handled by one crew instead of four trades.</p>
    <p class="muted">The one thing done differently is pricing. Mowing starts at $40 and tree work at $125, and
      those numbers are printed on the site rather than held back until someone has your phone number.</p>
    <a class="btn btn-red" href="/contact/">Get a Free Estimate</a>
  </div>
</div></section>
<section class="band tint"><div class="wrap">
  <div class="center rv"><p class="eyebrow c" style="color:var(--green)">Straight Talk</p><h2>What We Will Not Claim</h2></div>
  <div class="feats">
    <div class="feat rv"><h3>No Invented Credentials</h3><p>Nothing on this site claims a licence, a certification or an insurance status that has not been confirmed in writing.</p></div>
    <div class="feat rv"><h3>Reviews Shown in Full</h3><p>The public GreenPal reviews are reproduced unedited, positive and negative together, and linked to the source.</p></div>
    <div class="feat rv"><h3>Illustrative Photography</h3><p>Service photographs here are stock images pending real job photos, and the footer says so on every page.</p></div>
  </div>
</div></section>"""
    (ROOT / "about").mkdir(exist_ok=True)
    (ROOT / "about/index.html").write_text(simple_page(
        "about", "About a lawn-care client Lawn Care", "A local the metro lawn care crew with published starting prices.",
        "About a lawn-care client", "One crew for the whole property, with the prices printed up front.",
        "mowing-src.jpg", about_inner), encoding="utf-8")
    written.append("/about/")

    # ---- gallery ----
    photos = ["mowing-src.jpg", "tree-trimming-src.jpg", "mulch-src.jpg", "edging-src.jpg",
              "pressure-washing-src.jpg", "junk-removal-src.jpg", "hero-src.jpg", "hero-lawn-src.jpg"]
    cells = "".join(
        f'<div class="card" style="aspect-ratio:4/3"><img src="/assets/{f}" alt="Yard work example" loading="lazy"></div>'
        for f in photos)
    gal_inner = f"""
<section class="band"><div class="wrap">
  <div class="center rv"><p class="eyebrow c" style="color:var(--green)">Gallery</p><h2>The Kind of Work We Do</h2>
  <p class="muted" style="max-width:60ch;margin-inline:auto">These are illustrative images while we collect real job
  photographs. Every one will be replaced with the crew's own work.</p></div>
  <div class="cards" style="grid-template-columns:repeat(4,1fr);margin-top:38px">{cells}</div>
</div></section>"""
    (ROOT / "gallery").mkdir(exist_ok=True)
    (ROOT / "gallery/index.html").write_text(simple_page(
        "gallery", "Gallery", "Examples of lawn care, tree work and cleanups across the metro.",
        "Gallery", "Lawn care, tree work, beds and haul-off across the metro.",
        "mulch-src.jpg", gal_inner), encoding="utf-8")
    written.append("/gallery/")

    # ---- service areas ----
    chips = "".join(f'<span class="btn btn-outline-red" style="cursor:default">{a}</span>' for a in AREAS)
    areas_inner = f"""
<section class="band"><div class="wrap center rv">
  <p class="eyebrow c" style="color:var(--green)">Where We Work</p>
  <h2>Both Sides of the metro</h2>
  <p class="muted" style="max-width:58ch;margin-inline:auto">Based on the the metro side and across the bridge every week.
  If you are near the edge of this list it is still worth asking.</p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:28px">{chips}</div>
</div></section>"""
    (ROOT / "service-areas").mkdir(exist_ok=True)
    (ROOT / "service-areas/index.html").write_text(simple_page(
        "service-areas", "Service Areas", "Lawn care across the metro, a coastal city, Riverview, a nearby town, Seffner and a nearby town.",
        "Service Areas", "Covering the core metro county and the coastal county from the the metro side.",
        "hero-src.jpg", areas_inner), encoding="utf-8")
    written.append("/service-areas/")

    # ---- contact (reuses the homepage form band verbatim) ----
    formband = re.search(r'<!-- ============ ESTIMATE FORM ============ -->\s*(<section class="band formband".*?</section>)', SRC, re.S).group(1)
    (ROOT / "contact").mkdir(exist_ok=True)
    (ROOT / "contact/index.html").write_text(simple_page(
        "contact", "Contact Us", "Get a free lawn care estimate in the metro. Text a photo of the yard.",
        "Contact Us", "A photo and a street name is enough to get a real number back.",
        "hero-src.jpg", formband), encoding="utf-8")
    written.append("/contact/")

    ty_inner = """
<section class="band"><div class="wrap center rv" style="max-width:640px">
  <h2>Thanks, That Came Through</h2>
  <p class="muted">Your details are in. You will normally get a number back the same day. If it is urgent,
  calling or texting <phone> is the fastest route.</p>
  <a class="btn btn-red" href="/">Back to the Homepage</a>
</div></section>"""
    (ROOT / "contact/thank-you").mkdir(parents=True, exist_ok=True)
    (ROOT / "contact/thank-you/index.html").write_text(simple_page(
        "contact/thank-you", "Thank You", "Your estimate request has been received.",
        "Thank You", "Your request is in and a number is on the way.",
        "mowing-src.jpg", ty_inner), encoding="utf-8")

    # ---- legal ----
    for slug, h1, para in [
        ("privacy-policy", "Privacy Policy",
         "This is a demonstration site. Details submitted through the estimate form are sent to the site "
         "operator's inbox for the purpose of responding to the enquiry and are not sold or shared. No "
         "advertising trackers are loaded."),
        ("terms", "Terms &amp; Conditions",
         "This site is an unaffiliated demonstration built for a lawn-care client Lawn Care Service and has not "
         "been reviewed or approved by the business. Pricing shown reflects the published flyer and should "
         "be confirmed with the business before booking. Service photographs are illustrative."),
    ]:
        inner = f'<section class="band"><div class="wrap rv" style="max-width:760px"><h2>{h1}</h2><p class="muted">{para}</p></div></section>'
        (ROOT / slug).mkdir(exist_ok=True)
        (ROOT / slug / "index.html").write_text(simple_page(
            slug, h1, f"{h1} for the a lawn-care client demonstration site.", h1,
            "The short version, in plain language.", "hero-src.jpg", inner), encoding="utf-8")
        written.append(f"/{slug}/")

    # ---- sitemap / robots / headers ----
    urls = ["/"] + written + ["/contact/thank-you/"]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://example-business.com/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "_headers").write_text(
        "/*\n"
        "  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://example-business.com; font-src 'self' https://example-business.com; "
        "img-src 'self' data:; media-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'\n"
        "  X-Frame-Options: DENY\n  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
        "\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n", encoding="utf-8")

    print(f"built {len(urls)} pages")
    for u in urls:
        print("  " + u)


if __name__ == "__main__":
    main()
