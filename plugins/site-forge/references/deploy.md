> **Deploy from an explicit `dist/`, never from the project root.** `.netlifyignore` is NOT
> honoured by `netlify deploy --dir .`. Doing so once published `research/BRIEF.md`, which
> contained the client's HOME ADDRESS, plus every build script and the stock image library.
> Recipe and the live 404 proof: `quality-checklist.md#clean-publish`.
>
> ```bash
> python3 scripts/make-dist.py .
> netlify deploy --prod --dir dist
> scripts/verify-published.sh <host> [owner-street-name]
> ```
> `./site-dir` below means the PUBLISH directory, never the project root. On a no-build
> static site those look identical, which is exactly how this went wrong on 8 of 26 sites.

# Deploy

> ## STOP. Deploying is gated.
> **Ask immediately before every deploy, every time.** Approval for one deploy is not
> approval for the next.
>
> **Default is local:** `cd ~/money/<slug> && python3 -m http.server 8080`, then iterate
> at `http://localhost:8080`. Everything except Netlify Forms, the CSP response headers
> and real mobile behaviour works locally.
>
> Deploy only for (1) a **paying client**, or (2) a **scheduled demo** that needs a live
> URL. Then batch every outstanding fix into ONE deploy.
>
> **Why:** 38 one-fix-at-a-time deploys to a single site in one session exhausted the
> 1,000-credit monthly allowance and forced a paid plan upgrade. Credits, not bandwidth,
> are the binding limit on this account.
>
> **Mobile QA happens at that first deploy**, not before. It cannot be verified locally
> and the automation browser renders at a fixed desktop width, so budget a real mobile
> pass on the live URL at demo time.


Netlify is the default host: free, instant, custom subdomain, and — the deciding
factor — **built-in Forms that email leads to ANY address with no recipient
verification** (Web3Forms/Formspree make the recipient confirm first; Netlify
doesn't). Install the CLI only here, at deploy time.

## Contents
- [One-shot script](#one-shot-script)
- [Manual steps](#manual-steps)
- [Enabling Forms (the gotcha)](#enabling-forms-the-gotcha)
- [Netlify CLI/API gotchas](#netlify-cliapi-gotchas)
- [Notification email](#notification-email)
- [Cloudflare Web Analytics (default)](#cloudflare-web-analytics-default--add-on-every-deploy)
- [Submissions & rename](#submissions--rename)
- [here.now alternative](#herenow-alternative)

## One-shot script

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/deploy-netlify.sh ./site-dir my-site-name [account-slug]
```

It ensures the CLI, creates-or-reuses the site, deploys `--prod`, and if it finds
an HTML `<form>` it enables Forms and redeploys so the form is detected. Login is
interactive the first time — if `netlify status` shows logged-out, ask the user
to run `netlify login` (don't try to automate the browser auth).

## Manual steps

```bash
# install (only at deploy time)
npm i -g netlify-cli            # or: npx netlify-cli ...

# create the site (idempotent: reuse if the name exists)
netlify sites:create --name my-site-name --account-slug my-account

# deploy the folder to production
netlify deploy --prod --dir ./site-dir
# → prints the live URL: https://<client>.netlify.app
```

## Enabling Forms (the gotcha)

New sites default `ignore_html_forms: true`, which turns the build-time form
scraper **off** — so a perfectly good `data-netlify="true"` form is never
detected and submissions 404. Flip it, then redeploy (detection happens at deploy):

```bash
netlify api updateSite --data '{"site_id":"<SITE_ID>","processing_settings":{"html":{"ignore_html_forms":false}}}'
netlify deploy --prod --dir ./site-dir   # redeploy so the form registers
```

The form markup itself (see `components.md`) needs: `name="..."
data-netlify="true"`, a hidden `form-name` input matching that name, a honeypot
(`netlify-honeypot="..."`), and real `name=` on every field.

## Netlify CLI/API gotchas

These four cost real debugging time on a multi-page build. Read before touching
`netlify api`.

**`updateSite` SILENTLY IGNORES top-level fields — everything but `site_id`
MUST be wrapped in `body`.** A top-level `name` no-ops (no error, exit 0), so a
*free* subdomain looks "taken" when nothing was ever written. Same trap for the
forms flip. Wrap it:

```bash
# rename — top-level "name" silently does nothing; "body" makes it stick
netlify api updateSite --data '{"site_id":"<SITE_ID>","body":{"name":"newname"}}'
# enable forms — same wrapper
netlify api updateSite --data '{"site_id":"<SITE_ID>","body":{"processing_settings":{"html":{"ignore_html_forms":false}}}}'
```

(The bare-`processing_settings` form in "Enabling Forms" above and the rename in
"Submissions & rename" both have this footgun — use the `body`-wrapped form.)

**If even the `body`-wrapped form silently no-ops** (confirmed on CLI v26.1.0 —
the update call exits 0, but an independent `getSite` right after still shows
the old value), skip the CLI entirely and PATCH the raw REST API with the
account's token:

```bash
TOKEN=$(python3 -c "import json;d=json.load(open('$HOME/Library/Preferences/netlify/config.json'));print(list(d['users'].values())[0]['auth']['token'])")
curl -s -X PATCH "https://example-business.com/api/v1/sites/<SITE_ID>" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"processing_settings":{"html":{"ignore_html_forms":false}}}'
```
This has been 100% reliable when the CLI wrapper wasn't. Verify with an
independent `netlify api getSite` afterward, don't trust the PATCH response
alone.

**`deploy --prod` resolves the site by ID, not name** — `--dir .` alone targets
whatever site is *linked*, which silently isn't the one you just created. Parse
the id and pass it explicitly:

```bash
SITE_ID=$(netlify api listSites | jq -r '.[] | select(.name=="my-site-name") | .id')
netlify deploy --prod --dir ./site-dir --site "$SITE_ID"
```

**Form detection only re-scans HTML files that are RE-UPLOADED in a deploy.** The
CDN diff skips unchanged files, so a page that already existed never gets its
`<form>` registered after you flip `ignore_html_forms`. Force a re-upload —
append a harmless newline so the file's hash changes — then redeploy and verify:

```bash
printf '\n' >> ./site-dir/contact.html      # any byte-level change forces re-upload
netlify deploy --prod --dir ./site-dir --site "$SITE_ID"
netlify api listSiteForms --data '{"site_id":"<SITE_ID>"}'   # confirm the form appears
```

**Delete a stale/registered form — needs BOTH ids.** `form_id` alone errors
`Missing required path variable site_id`:

```bash
netlify api deleteSiteForm --data '{"site_id":"<SITE_ID>","form_id":"<FORM_ID>"}'
```

## Notification email

Send every submission to any inbox — no action required from that inbox:

```bash
# find the form id
netlify api listSiteForms --data '{"site_id":"<SITE_ID>"}'

# create an email notification hook for that form
netlify api createHookBySiteId --data '{
  "site_id":"<SITE_ID>",
  "type":"email",
  "event":"submission_created",
  "data":{"email":"leads@example.com","form_id":"<FORM_ID>"}
}'
```

If that CLI call 422s ("Unprocessable Entity") with no useful detail, POST the
raw endpoint instead (same token-extraction trick as above) — `data.email` is
required, `data.to` 400s with "email can't be blank", and `form_id` is optional
(omit it to notify on every form on the site, useful when there's only one):

```bash
curl -s -X POST "https://example-business.com/api/v1/hooks" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"site_id":"<SITE_ID>","type":"email","event":"submission_created","data":{"email":"leads@example.com"}}'
# list existing hooks (note: NOT /sites/<id>/hooks, that 404s):
curl -s "https://example-business.com/api/v1/hooks?site_id=<SITE_ID>" -H "Authorization: Bearer $TOKEN"
```

That zero-friction routing is why Netlify Forms beats the alternatives for a demo
you're handing to someone else.

## Cloudflare Web Analytics (default — add on every deploy)

Free, privacy-first pageview + referrer tracking, and the **default for every site-forge
deploy** (the user usually wants it). For a demo URL you've handed to one prospect, **any
visit that isn't you means the prospect looked**, and the referrer tells you which channel
they came from (Facebook DM, email, text). No cookies, so no consent banner needed.

It needs a token the user generates — it cannot be scripted. After the first `--prod` deploy:

1. Ask the user: in Cloudflare → **Analytics & Logs → Web Analytics → Add a site**, enter the
   deployed hostname (`<site>.netlify.app`), and paste back the `<script>` snippet.
2. Inject the beacon right before `</body>` (the snippet carries the token):

```html
<!-- Cloudflare Web Analytics -->
<script defer src='https://example-business.com/beacon.min.js' data-cf-beacon='{"token": "THE_TOKEN"}'></script>
<!-- End Cloudflare Web Analytics -->
```

3. Redeploy (`netlify deploy --prod --dir ./site-dir --site "$SITE_ID"`).

**No `integrity=` SRI on this one** — Cloudflare rotates `beacon.min.js`, so a pinned hash
breaks analytics on their next update. This is the documented SRI exception (every other CDN
tag stays SRI-pinned). The token sits in the page in plain sight; that's fine for a private demo.

`auto` mode: this is a "needs the user" step → surface it in the Skipped/upgrade-later list
with the exact hostname to add in Cloudflare. `full` mode: ask for the token at deploy time.

## Security baseline (ship on EVERY build, added 2026-07-28)

Two files in the site root. Free, seconds to add. The whole 22-site portfolio was swept to this standard on 2026-07-28.

### `_headers`

The `/*` block is NOT copy-paste: **the CSP must be generated per site** from what that site actually loads, or it silently breaks GSAP, Lenis, Google Fonts and map embeds. Generate it by scanning every `.html` for `<script src>`, `<link rel=stylesheet>`, `<iframe src>`, `<form action>` and fetch/sendBeacon origins.

```
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; form-action 'self'; script-src 'self' 'unsafe-inline' <cdn origins>; style-src 'self' 'unsafe-inline' <css origins>; img-src 'self' data: blob: https:; font-src 'self' data: <font origins>; connect-src 'self' <beacon origins>; frame-src 'self' <embed origins>; media-src 'self' data: blob: https:; upgrade-insecure-requests
  Cross-Origin-Opener-Policy: same-origin
  X-DNS-Prefetch-Control: off
```

**`'unsafe-inline'` is deliberate, not laziness.** Every build has inline `<script>` and `<style>`. Hash-based CSP is stronger but breaks on every content edit, and monthly edits are literally what the client pays for. A site broken during a routine revision is worse than the marginal gain. The CSP still blocks external scripts from unlisted origins, object/embed, framing, base-tag hijacking, and form exfiltration to other domains.

**Verify before shipping.** A wrong CSP fails silently and just looks like a broken site. Serve locally with the real headers applied, then in the browser confirm `typeof gsap`, `typeof Lenis`, `document.fonts.size`, and the computed `font-family` on `h1`. Do NOT trust an empty console or `transferSize: 0`: cross-origin resources report 0 without `Timing-Allow-Origin`, so that proves nothing either way.

### `robots.txt`

Explicitly ALLOW the AI crawlers. Most agencies block them by reflex; being indexed by answer engines is the point.

```
User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: bingbot
Allow: /

Sitemap: <canonical-host>/sitemap.xml   # only when sitemap.xml exists
```

### Form spam

Honeypot on every form, which the builds already do correctly:
```html
<form data-netlify="true" netlify-honeypot="bot-field" method="POST">
  <input name="bot-field" hidden>
```
Honeypot stops naive bots, not headless ones. Escalate a single site to `data-netlify-recaptcha="true"` only after it actually gets spammed; reCAPTCHA costs conversion.

### Known gap, accepted

Phone and email sit in plain text and get harvested, so clients start getting spam calls and "rank you #1" emails, and they notice it began after the build. Mitigation: route contact through the form, keep `tel:` (unavoidable, and a ringing phone is the goal), avoid a plain `mailto:`.

## Netlify plan reality (checked live 2026-07-28)

The account is **NOT on the free tier**, so the widely-quoted "100 form submissions/month free cap" does not apply.

- Plan: **Personal**, $9/mo showing at **$4.50** until the 50% discount ends 2026-09-23.
- Allowance: **1,000 credits/month**. Billing period runs 23rd to 22nd.
- Projects: **22 of 500**. Concurrent builds 1.
- **Form submissions are effectively zero** (daily chart tops out at 2), so forms are not the constraint anyone assumes they are.

**The real constraint is credits, and it has already been breached.** Usage by period: 337 → **1.4K** → 559 current. The June-July period went **40% over the 1,000 allowance**, and one single day hit 435 credits. Credits are consumed by builds, bandwidth, web requests, compute and image transformations, not by forms.

Practical rule: **watch credits, not form quota.** Video builds and image-heavy rebuilds are what spike it. Check `Usage & billing → Account usage insights → Credits` before a batch of rebuilds.

## Submissions & rename

```bash
netlify api listFormSubmissions --data '{"form_id":"<FORM_ID>"}'   # read leads
netlify api deleteSubmission --data '{"submission_id":"<ID>"}'      # clear a test
netlify api updateSite --data '{"site_id":"<SITE_ID>","name":"cleaner-name"}'  # rename → <client>.netlify.app
```

Prefer a clean subdomain with no dashes when the name is available.

## here.now alternative

`here.now` is an agent-hosting option (publish → upload → finalize via its API/
skill) — fine for a quick static drop, but it has **no built-in forms**, so for
any lead-capture site Netlify wins. Mention it only if Netlify is unavailable.

## AI-crawler opt-in in robots.txt (added 2026-07-30, from the Liquid Agency teardown)

**Ship this block in EVERY `robots.txt`** — ours and every client build. Most sites either ignore
the question or silently block these; liquidagency.eu opts in **by name**, which is why it surfaces
in AI answers.

```
User-Agent: GPTBot
Allow: /

User-Agent: ChatGPT-User
Allow: /

User-Agent: ClaudeBot
Allow: /

User-Agent: anthropic-ai
Allow: /

User-Agent: PerplexityBot
Allow: /

User-Agent: Google-Extended
Allow: /

User-Agent: OAI-SearchBot
Allow: /

User-Agent: Applebot-Extended
Allow: /
```

**Placement:** insert AFTER the `User-agent: *` block and any `Disallow` rules, but BEFORE the
`Sitemap:` line — `Sitemap:` conventionally goes last. Applied to a junk-removal client-v2 and
southern-powersports 2026-07-30 (8/8 agents each).

For a local trade, being quotable by ChatGPT/Claude/Perplexity when someone asks *"who does junk
removal in an exurban town"* is free distribution. There is no downside for a marketing site: the
content is already public and we WANT it repeated with the business name and phone attached.

**It is also a sellable line item.** Liquid productised it as a service page (`/geo-ai-search`)
plus two guides, and sells GEO/Generative Engine Optimization as its own engagement. Our
SEO-PLAYBOOK §9 already covers the technique; this is the packaging.
