# CMS options for hand-written static sites

Written 2026-07-30, prompted by the BadgerLayer teardown (they sell "headless CMS, Sanity or
Payload" as the feature that justifies their $7,500 tier) and by the question *"how can a company
offer a CMS if they build custom sites?"*

**CMS = Content Management System.** Software that lets a non-developer create, edit and publish
site content without touching code.

---

## 1. The four ways an agency offers a CMS on a custom-built site

Most explanations list only the first three. **The fourth is the one that fits our stack**, and it
is usually omitted.

| # | Approach | How it works | Examples | Fits our stack? |
|---|---|---|---|---|
| 1 | **Headless CMS** | Custom front end written from scratch, content pulled over an API from a hosted dashboard | Sanity, Contentful, Strapi, Payload | Only with a build step |
| 2 | **Custom theme on an open-source CMS** | Use WordPress/Drupal as the engine, write a bespoke theme, strip the admin down | WordPress + custom theme | **No** — brings the plugin/patching problem we sell against |
| 3 | **Proprietary custom CMS** | Build the database and admin panel yourself | Laravel, Rails, Node | Overkill, and a maintenance liability |
| 4 | **Git-based / flat-file CMS** | An admin UI that reads and writes **markdown/JSON in the site's own repo**; a commit triggers a rebuild and redeploy | **Decap** (ex-Netlify CMS), **Sveltia**, **Pages CMS**, **Tina**, **Keystatic** | **Yes — this is the one** |

**Why #4 is the fit:** it needs no server, no database, and no monthly SaaS bill. The content lives
as files next to the site, the client gets a real web login, and Netlify redeploys on commit. It
is the only category that respects "static HTML, no backend."

**The catch, stated honestly:** our builds currently put content *inline in hand-written HTML*.
A git-based CMS needs content separated into data files plus a template step. Adopting it means
introducing a build step to a stack whose whole advantage is not having one. That is a real
trade, not a free upgrade.

---

## 2. The decision, for local trades specifically

**Default: no CMS. Content changes are included in the monthly. That is a feature, not a gap.**

A lawn care or junk removal business changes its website maybe twice a year: a price, a phone
number, a new service, a seasonal photo. Handing that owner a CMS login means:

- they forget the password within a month,
- the one time they do log in they break the layout, and
- the "self-service" you sold becomes a support call anyway.

Meanwhile **the monthly retainer needs a reason to exist.** "Text me the change and it's live the
same day" is a stronger promise to a 55-year-old tree surgeon than "here is your Sanity dashboard."
Note that BadgerLayer, at $150/mo, includes **2 hours of content changes per month** for exactly
this reason — they sell the CMS *and* still do the edits.

**When a CMS genuinely earns its place:**
- the client publishes **regularly** (a real blog, weekly specials, job listings, an events page),
- they have **staff** who will actually use it (an office manager, not the owner in a truck),
- the site has **many similar pages** that a template plus a data file would generate, or
- they explicitly ask for it and will pay for it as a tier upgrade.

Below that bar, a CMS is a cost we absorb and a support surface we inherit.

---

## 3. What to say when a prospect asks "can I edit it myself?"

Do not get defensive and do not oversell. The honest answer is strong:

> "You can, but most of my clients don't want to. Text or email me the change and it's live the
> same day, and that's included in the monthly. If you're going to be posting regularly, I can add
> a proper editor login and we'll price that in. For a phone number or a price change, me doing it
> in ten minutes beats you learning a dashboard."

That answers the question, defends the retainer, and leaves the upsell open.

---

## 4. If we do add one — the recommended path

1. **Sveltia CMS** or **Decap CMS** — both free, both git-based, both work on Netlify with no
   server. Sveltia is the modern rewrite of Decap and is the better starting point.
2. Auth via **Netlify Identity** or a GitHub OAuth app.
3. Content moves from inline HTML into `content/*.md` or `*.json`; a small build step (Eleventy is
   the lightest that fits our hand-written approach) renders the same static HTML we ship today.
4. Restrict the editable surface hard: expose text, prices, phone, hours and images. **Never
   expose layout or CSS.** The commonest CMS failure is a client with too many controls.
5. Charge for it. It is a tier feature, not a default.

**Do not reach for WordPress.** We sell against it explicitly ("not held together by 42 plugins" is
BadgerLayer's line and it is a good one). Adopting it to solve editing would forfeit the argument.

---

## 5. Vocabulary, so nothing is bluffed

| Term | Meaning |
|---|---|
| **CMS** | Content Management System |
| **Headless** | The content store has no front end of its own; it serves data over an API and you build the presentation separately |
| **Headful / traditional** | CMS ships the admin *and* renders the public site (WordPress, Drupal) |
| **Flat-file / git-based** | Content stored as files in the repo, not in a database |
| **Structured content** | Content stored as fields (price, hours, service name) rather than one blob of HTML — what makes it reusable across pages |
| **Build step** | A process that turns source files into the final static HTML before deploy |
| **Decap** | The current name for Netlify CMS |
