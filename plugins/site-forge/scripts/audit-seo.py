#!/usr/bin/env python3
"""Audit SEO, local SEO and security across every page.

Reports only. Nothing here edits the site: the point is to see the true state
before changing anything, because several of these (schema type, noindex, NAP
consistency) are easy to "fix" into something worse.

    python3 src/audit-seo.py
"""
import json
import pathlib
import re
import sys
from collections import defaultdict

# vendored into the skill: the site root is wherever you run this from
ROOT = pathlib.Path.cwd()
PAGES = sorted(ROOT.glob('*.html'))


def _site():
    """Read the origin from the site being audited, never a hardcoded one.

    This was pinned to a previous project's domain, so every page on the NEXT
    build reported "missing from sitemap.xml" against a host it had never heard
    of. A stale constant in a checker is worse than no checker: it produces a
    confident wall of false positives that trains you to skim the output.
    """
    if len(sys.argv) > 1 and sys.argv[1].startswith('http'):
        return sys.argv[1].rstrip('/')
    for p in PAGES:
        m = re.search(r'<link rel="canonical" href="(https?://[^/"]+)',
                      p.read_text(errors='ignore'))
        if m:
            return m.group(1)
    return ''


SITE = _site()

# pages that must NOT be indexed: thin, duplicate, or post-action
NOINDEX_EXPECTED = {'thanks.html', '404.html'}

issues = []
notes = []


def add(sev, page, msg):
    issues.append((sev, page, msg))


def head(t):
    return t.split('</head>', 1)[0] if '</head>' in t else t


def main():
    sitemap = (ROOT / 'sitemap.xml').read_text() if (ROOT / 'sitemap.xml').exists() else ''
    in_sitemap = set(re.findall(r'<loc>([^<]+)</loc>', sitemap))

    schema_types = defaultdict(list)
    phones, titles, descs = set(), {}, {}

    for p in PAGES:
        t = p.read_text(encoding='utf-8')
        h = head(t)
        name = p.name

        # ---- indexability -------------------------------------------------
        robots = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', h, re.I)
        noindexed = bool(robots and 'noindex' in robots.group(1).lower())
        if name in NOINDEX_EXPECTED and not noindexed:
            add('HIGH', name, 'thin/post-action page is indexable; needs meta robots noindex')
        if name not in NOINDEX_EXPECTED and noindexed:
            add('HIGH', name, 'real page is noindexed')

        # ---- sitemap coverage ---------------------------------------------
        url = SITE + '/' + ('' if name == 'index.html' else name)
        if name not in NOINDEX_EXPECTED:
            if url not in in_sitemap:
                add('MED', name, f'missing from sitemap.xml ({url})')
        else:
            if url in in_sitemap:
                add('MED', name, 'noindex page is listed in sitemap.xml')

        # ---- title / description -------------------------------------------
        ti = re.search(r'<title>(.*?)</title>', h, re.S)
        de = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h)
        if not ti:
            add('HIGH', name, 'no <title>')
        else:
            v = ti.group(1).strip()
            titles.setdefault(v, []).append(name)
            if len(v) > 62:
                add('LOW', name, f'title {len(v)} chars, truncates in SERP (~60)')
        if not de:
            add('HIGH', name, 'no meta description')
        else:
            v = de.group(1).strip()
            descs.setdefault(v, []).append(name)
            if not (70 <= len(v) <= 165):
                add('LOW', name, f'description {len(v)} chars, outside 70-165')

        # ---- headings -------------------------------------------------------
        h1s = re.findall(r'<h1[^>]*>', t)
        if len(h1s) == 0:
            add('HIGH', name, 'no h1')
        elif len(h1s) > 1:
            add('MED', name, f'{len(h1s)} h1 elements; should be one')

        # ---- structured data -------------------------------------------------
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
        if not blocks and name not in NOINDEX_EXPECTED:
            add('HIGH', name, 'no JSON-LD at all')
        for b in blocks:
            try:
                data = json.loads(b)
            except Exception as e:
                add('HIGH', name, f'JSON-LD does not parse: {e}')
                continue
            graph = data.get('@graph', [data]) if isinstance(data, dict) else data
            for node in graph:
                ty = node.get('@type')
                tys = ty if isinstance(ty, list) else [ty]
                for one in tys:
                    schema_types[one].append(name)
                if 'aggregateRating' in json.dumps(node):
                    add('HIGH', name, 'aggregateRating on own site: ineligible and against Google policy')
                if one == 'LocalBusiness':
                    add('MED', name, 'bare LocalBusiness; use the narrowest fitting subtype')
                tel = node.get('telephone')
                if tel:
                    phones.add(tel)

        # breadcrumbs on inner pages
        # breadcrumbs help the SERP; a page that is not in the SERP does not need them
        if (name != 'index.html' and name not in NOINDEX_EXPECTED
                and 'BreadcrumbList' not in t):
            add('MED', name, 'no BreadcrumbList schema on an inner page')

        # a visible FAQ must carry FAQPage, and FAQPage must have a visible FAQ
        has_faq_markup = 'class="faq"' in t
        has_faq_schema = 'FAQPage' in t
        if has_faq_markup and not has_faq_schema:
            add('MED', name, 'visible FAQ with no FAQPage schema')
        if has_faq_schema and not has_faq_markup:
            add('HIGH', name, 'FAQPage schema with no visible FAQ: policy violation')

        # ---- security ---------------------------------------------------------
        for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', t):
            if 'rel=' not in m.group(0) or 'noopener' not in m.group(0):
                add('MED', name, 'target=_blank without rel=noopener')
                break
        for m in re.finditer(r'<script\b[^>]*\bsrc="https?://[^"]+"[^>]*>', t):
            if 'integrity=' not in m.group(0):
                add('HIGH', name, f'third-party script without SRI: {m.group(0)[:70]}')
            if 'crossorigin=' not in m.group(0):
                add('MED', name, 'third-party script without crossorigin')
        if re.search(r'\son(click|load|error|mouseover)\s*=', t):
            add('MED', name, 'inline event handler attribute (fights a strict CSP)')

    # ---- cross page ------------------------------------------------------------
    for v, pgs in titles.items():
        if len(pgs) > 1:
            add('HIGH', 'site', f'duplicate <title> on {", ".join(pgs)}')
    for v, pgs in descs.items():
        if len(pgs) > 1:
            add('MED', 'site', f'duplicate meta description on {", ".join(pgs)}')
    if len(phones) > 1:
        add('HIGH', 'site', f'NAP inconsistency: {len(phones)} different phone numbers {phones}')

    print('SCHEMA TYPES IN USE')
    for k, v in sorted(schema_types.items(), key=lambda kv: -len(kv[1])):
        print(f'  {str(k):<22} {len(v):>2} page(s)')

    print('\nFINDINGS')
    order = {'HIGH': 0, 'MED': 1, 'LOW': 2}
    for sev, page, msg in sorted(issues, key=lambda i: (order[i[0]], i[1])):
        print(f'  [{sev:<4}] {page:<26} {msg}')
    highs = sum(1 for i in issues if i[0] == 'HIGH')
    print(f'\n{len(issues)} finding(s): {highs} high, '
          f'{sum(1 for i in issues if i[0] == "MED")} medium, '
          f'{sum(1 for i in issues if i[0] == "LOW")} low')
    return 1 if highs else 0


if __name__ == '__main__':
    sys.exit(main())
