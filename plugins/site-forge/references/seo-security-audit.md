# SEO, local SEO and security: the audit, and what it keeps catching

Run `scripts/audit-seo.py` from the site root. It reports only, deliberately:
several of these are easy to "fix" into something worse.

```bash
python3 ~/.claude/skills/site-forge/scripts/audit-seo.py     # exit 1 on any HIGH
```

It checks indexability vs sitemap membership, title/description length and
uniqueness, one h1, JSON-LD parse + required properties, bare `LocalBusiness`,
`aggregateRating` on your own site, breadcrumbs on inner pages, FAQ schema
matching visible content, `target=_blank` without `noopener`, third-party scripts
without SRI or crossorigin, inline event handlers, and NAP consistency.

---

## The findings that recur

### FAQ schema drifting from the visible page
The single most common real defect. Schema said *"Do you shoot film or digital?"*,
the page said *"Film or digital?"*. Four answers had drifted too. Google requires
the marked-up content to match what the visitor sees; paraphrase is a rich-result
risk and, at the extreme, a manual action.

**Generate the schema FROM the markup rather than writing it twice.** Pull the
questions out of the buttons and the answers out of the panels, then serialise.

### `X-Robots-Tag: index, follow` sent site-wide
It was going out on every response including the two pages carrying a `noindex`
meta tag. The rules combine and the restrictive one should win, but sending an
explicit *index* header for a page you are asking not to be indexed is a
contradiction no crawler should have to resolve.

Indexable is the default. **State only the exception:**

```
/thanks.html
  X-Robots-Tag: noindex, nofollow
/404.html
  X-Robots-Tag: noindex, nofollow
```

### Structured data missing on a page you forgot was indexed
Credits, colophon and licence pages are real indexed pages. They need at least
`WebPage` + `BreadcrumbList`. A `noindex` page needs neither, and the audit
exempts them rather than nagging.

### The business node is thin
`name` + `url` + `address` is not local SEO. What is worth adding, when true:
`geo`, `serviceArea` (a `GeoCircle` for a service-area business), `logo` as an
`ImageObject` with real dimensions, `foundingDate`, `founder`, `knowsAbout`,
`contactPoint`, `additionalType` pointing at a Wikipedia concept,
`currenciesAccepted`.

---

## Local SEO: the three things not to invent

A demo or a thin brief tempts you to fill the schema in. Do not.

1. **No phone number that does not exist.** If the site takes enquiries by form
   only, the `contactPoint` is the form URL. An invented number is worse than an
   absent one: it is the N and the P of NAP, and it is wrong everywhere it is
   scraped.
2. **No `sameAs` without real profiles.** Linking to nothing is worse than not
   linking.
3. **No street address for a service-area business.** This is Google's own
   guidance, not a shortcut. `PostalAddress` with locality, region and country,
   plus `geo` and `serviceArea`, is the correct shape.

## Picking the schema type

Use the narrowest `LocalBusiness` subtype **that actually fits**, and verify
against the page content rather than the business name. But also know when the
narrowing stops: schema.org has **no photographer subtype**, so
`ProfessionalService` is the correct narrowest type there, not a lazy fallback.
Reaching for something more specific than exists is how you end up with
`MotorcycleRepair` on a shop that services mowers.

Never `aggregateRating` on a business's own site: a business that controls the
reviews about itself is ineligible for the star feature, and republishing another
platform's score breaks the "don't aggregate ratings from other websites" rule at
the same time. Show it as visible, linked copy.

---

## Security headers

```
Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none';
  frame-ancestors 'none'; frame-src 'none'; worker-src 'none'; manifest-src 'self';
  form-action 'self'; script-src 'self' <cdn>; style-src 'self' 'unsafe-inline' <fonts>;
  font-src 'self' <fonts>; img-src 'self' data:; media-src 'self'; connect-src 'self';
  upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=(), usb=(),
  magnetometer=(), gyroscope=(), accelerometer=(), midi=(), serial=(), bluetooth=(),
  display-capture=(), idle-detection=(), local-fonts=(), autoplay=(self),
  fullscreen=(self), interest-cohort=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

**Do not add COEP** unless you have checked every cross-origin asset sends CORP.
It breaks Google Fonts.

### Verify the CSP against what the page ACTUALLY requests

Reading the policy and nodding is how a CSP that blocks your own fonts ships.
Parse the header, collect every external origin from the markup **and from
`@import` inside the stylesheet** (fonts are loaded by the imported CSS, not by
the markup, which is exactly the origin people forget), and diff them.

`scripts/audit-seo.py` does the markup half; the CSS `@import` half is worth a
separate three lines whenever the font strategy changes.

A CSP with no `frame-src` silently blocks every embed, which is how a map that
was written down and paid for never appears.
