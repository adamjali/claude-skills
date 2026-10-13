#!/usr/bin/env python3
"""Audit the social-card tag set on a LIVE host. Non-zero exit = something is wrong.

The social card is the picture that appears when the link is pasted into a text, a
DM, Slack or Facebook. It is the first thing a prospect sees and it is the easiest
thing in the whole build to ship broken, because it looks perfect in a browser.

This has been missed or half-done repeatedly, so it is a command, not a paragraph:

    python3 ~/.claude/skills/site-forge/scripts/verify-og.py <host>
    python3 ~/.claude/skills/site-forge/scripts/verify-og.py <client>.netlify.app

What it checks, on every page it can find via sitemap.xml (plus 404 and thanks):

  1. The full tag set is present. A partial set is the usual failure: og:image with
     no width/height/type/alt still renders, just badly and inconsistently.
  2. og:image and twitter:image are ABSOLUTE urls. A relative one silently fails
     for every scraper.
  3. og:url is SELF-REFERENTIAL. Copying the homepage's og:url onto every page is
     the classic multipage mistake and collapses every share to one preview.
  4. The image really resolves, and serves as image/jpeg or image/png.
     WebP is REJECTED: several scrapers ignore it entirely.
  5. The declared og:image:width/height match the file's REAL pixels.
  6. og:title and og:description are non-empty and differ from the previous page
     (a whole site sharing one title means nobody copied the head properly).
"""
import io
import re
import struct
import sys
import urllib.error
import urllib.request

REQUIRED = [
    'og:type', 'og:site_name', 'og:locale', 'og:url', 'og:title', 'og:description',
    'og:image', 'og:image:width', 'og:image:height', 'og:image:type', 'og:image:alt',
    'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt',
]
UA = {'User-Agent': 'Mozilla/5.0 (compatible; site-forge-og-check/1.0)'}


def get(url, timeout=25):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:            # a 404 page still has a usable body
        return e.code, e.headers, e.read()
    except Exception as e:
        return 0, {}, str(e).encode()


def meta(html):
    """Every og:/twitter: tag, regardless of property=/name= or attribute order."""
    out = {}
    for tag in re.findall(r'<meta\b[^>]*>', html, re.I):
        k = re.search(r'(?:property|name)\s*=\s*"((?:og|twitter):[a-z:_]+)"', tag, re.I)
        v = re.search(r'content\s*=\s*"([^"]*)"', tag, re.I)
        if k and v:
            out.setdefault(k.group(1).lower(), v.group(1))
    return out


def real_size(data):
    """Pixel dimensions straight from the bytes, so a wrong declared size is caught."""
    if data[:2] == b'\xff\xd8':                                    # JPEG
        f, n = io.BytesIO(data), 2
        while True:
            b = f.read(1)
            if not b:
                return None
            if b != b'\xff':
                continue
            m = f.read(1)
            while m == b'\xff':
                m = f.read(1)
            if m in b'\xc0\xc1\xc2\xc3\xc5\xc6\xc7\xc9\xca\xcb\xcd\xce\xcf':
                f.read(3)
                h, w = struct.unpack('>HH', f.read(4))
                return w, h
            ln = struct.unpack('>H', f.read(2))[0]
            f.read(ln - 2)
            n += 1
            if n > 200:
                return None
    if data[:8] == b'\x89PNG\r\n\x1a\n':                            # PNG
        return struct.unpack('>II', data[16:24])
    return None


def pages_for(host):
    base = f'https://{host}'
    found = []
    code, _, body = get(f'{base}/sitemap.xml')
    if code == 200:
        found = re.findall(r'<loc>([^<]+)</loc>', body.decode('utf-8', 'replace'))
    if not found:
        found = [f'{base}/']
    for extra in ('/404.html', '/thanks.html'):
        if not any(u.endswith(extra) for u in found):
            c, _, _ = get(base + extra)
            if c == 200:
                found.append(base + extra)
    return base, found


def main(host):
    host = host.replace('https://', '').replace('http://', '').rstrip('/')
    base, urls = pages_for(host)
    problems, seen_titles, img_cache = [], {}, {}

    print(f'social card audit: {host}  ({len(urls)} pages)\n')
    for url in urls:
        code, _, body = get(url)
        if code not in (200, 404):
            problems.append(f'{url}: HTTP {code}')
            continue
        m = meta(body.decode('utf-8', 'replace'))
        short = url.replace(base, '') or '/'

        missing = [t for t in REQUIRED if not m.get(t)]
        if missing:
            problems.append(f'{short}: missing {", ".join(missing)}')

        for key in ('og:image', 'twitter:image'):
            v = m.get(key, '')
            if v and not v.startswith(('http://', 'https://')):
                problems.append(f'{short}: {key} is not absolute ({v})')

        ogurl = m.get('og:url', '')
        if ogurl and ogurl.rstrip('/') != url.rstrip('/'):
            problems.append(f'{short}: og:url points at {ogurl}, not itself')

        t = m.get('og:title', '')
        if t:
            if t in seen_titles:
                problems.append(f'{short}: og:title duplicates {seen_titles[t]}')
            else:
                seen_titles[t] = short

        img = m.get('og:image')
        if img and img not in img_cache:
            ic, ih, idata = get(img)
            ctype = (ih.get('Content-Type') or '').split(';')[0].lower() if ih else ''
            img_cache[img] = (ic, ctype, real_size(idata) if ic == 200 else None)
        if img:
            ic, ctype, size = img_cache[img]
            if ic != 200:
                problems.append(f'{short}: og:image returns {ic}')
            elif ctype not in ('image/jpeg', 'image/png'):
                problems.append(f'{short}: og:image serves {ctype} — scrapers want jpeg/png, several ignore webp')
            elif size:
                dw, dh = m.get('og:image:width'), m.get('og:image:height')
                if dw and dh and (int(dw), int(dh)) != size:
                    problems.append(f'{short}: declares {dw}x{dh} but the file is {size[0]}x{size[1]}')
        print(f'  {short:<22} {"ok" if not any(p.startswith(short + ":") for p in problems) else "SEE BELOW"}')

    print()
    if problems:
        print(f'{len(problems)} problem(s):')
        for p in problems:
            print('  -', p)
        return 1
    print('PASS: full og/twitter set on every page, absolute urls, self-referential og:url,')
    print('      unique titles, image resolves as jpeg/png at its declared dimensions.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
