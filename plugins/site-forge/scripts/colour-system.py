#!/usr/bin/env python3
"""Enforce one treatment per photograph, site-wide.

The old rule was contextual: photographs were colour in a panel and monochrome in
the contact sheet. It was a real rule and it still read as random, because the
SAME photograph appeared both ways. wedding-25 was warm orange in the hero and
grey in the reel; wedding-17 was colour in the map panel and grey in the reel. No
viewer can infer a rule they can see contradicted on one screen.

Third pass, and the one with a point. A wall of colour photographs from mixed
sources has mixed white balance, mixed grade and mixed era; no CSS filter makes
them agree, so the page reads as a collection of other people's pictures. The
site is a CONTACT SHEET instead:

    everything is a proof, printed grey
    `sel` is the verdict that a frame got circled and printed, and keeps colour

Colour is therefore information, not decoration: each page's opening frame plus
the six circled frames on the reel. A given photograph looks the same everywhere
it appears.

    python3 src/colour-system.py            # audit
    python3 src/colour-system.py --write
"""
import pathlib
import re
import sys
from collections import defaultdict

# vendored into the skill: the site root is wherever you run this from
ROOT = pathlib.Path.cwd()

# process imagery: equipment and materials, never a photograph of the day
PROCESS = ('craft-',)
GRADES = ('work', 'proof', 'quiet', 'grade', 'grade-hard', 'keep')


def wanted(src, tag=''):
    """The one treatment this photograph gets, everywhere.

    The site is a contact sheet now: everything is a proof, printed grey. `sel` is
    the verdict that a frame got printed and kept its colour, so it is set
    deliberately in the markup (each page's opening frame, and the circled frames
    on the reel) and this must never overwrite it back to grey.
    """
    if re.search(r'class="[^"]*\bkeep\b', tag):
        return 'keep'
    name = src.rsplit('/', 1)[-1]
    if name.startswith(PROCESS):
        return 'proof'
    return 'work'


def recolour(src):
    """Point a hard-baked -mono file at its colour original where the rule says colour.

    This is the hole the first version of this script had. It only looked at CSS
    classes, so it happily reported "one treatment site-wide" while every inner
    page opened on a `-mono-2000.webp` FILE. wedding-25 was grey on contact.html
    and warm in the reel on the homepage, and the audit called that consistent.
    A treatment is the class AND the file, so check both.
    """
    if '-mono' not in src or wanted(src) == 'proof':
        return src
    cand = src.replace('-mono-', '-')
    return cand if (ROOT / cand).exists() else src


def main():
    write = '--write' in sys.argv
    seen = defaultdict(set)
    was = defaultdict(set)
    changes = defaultdict(int)
    per_page = {}

    for page in sorted(ROOT.glob('*.html')):
        html = page.read_text(encoding='utf-8')
        out = html

        def fix(m):
            tag = m.group(0)
            src = re.search(r'src="([^"]+)"', tag)
            if not src or '/img/' not in src.group(1):
                return tag
            base = re.sub(r'-(?:mono-)?\d+\.webp$', '', src.group(1).rsplit('/', 1)[-1])
            base = re.sub(r'-mono$', '', base)
            want = wanted(src.group(1), tag)

            # what ships RIGHT NOW, before this script touches anything. Recording
            # the post-fix state here would make the audit unable to ever fail.
            cls0 = re.search(r'class="([^"]*)"', tag)
            have0 = [c for c in (cls0.group(1).split() if cls0 else []) if c in GRADES]
            was[base].add('proof' if ('-mono' in tag or have0 == ['proof']) else 'work')

            # repoint any hard-baked monochrome file, in src and in srcset
            for path in set(re.findall(r'assets/img/[A-Za-z0-9_-]+\.webp', tag)):
                fixed = recolour(path)
                if fixed != path:
                    tag = tag.replace(path, fixed)
                    changes[page.name] += 1
            # what actually ships now, file included
            seen[base].add('keep' if want == 'keep'
                           else ('proof' if '-mono' in tag or want == 'proof' else 'work'))

            cls = re.search(r'class="([^"]*)"', tag)
            have = [c for c in (cls.group(1).split() if cls else []) if c in GRADES]
            if have == [want]:
                return tag
            changes[page.name] += 1
            keep = [c for c in (cls.group(1).split() if cls else []) if c not in GRADES]
            new = ' '.join([want] + keep)
            if cls:
                return tag[:cls.start(1)] + new + tag[cls.end(1):]
            return tag[:4] + f' class="{new}"' + tag[4:]

        out = re.sub(r'<img\b[^>]*>', fix, out)
        per_page[page.name] = out
        if write and out != html:
            page.write_text(out, encoding='utf-8')

    # a photograph carrying two treatments is the defect this script exists for
    split = {k: v for k, v in was.items() if len(v) > 1}
    print(f'{len(seen)} distinct photographs referenced')
    sel = sum(1 for v in seen.values() if v == {'keep'})
    print(f'{sel} in colour (selects), '
          f'{sum(1 for v in seen.values() if v != {"keep"})} printed grey'
          f'   -> {sel / max(1, len(seen)):.0%} colour')
    if split:
        print('\nWAS SPLIT across two treatments (class or baked -mono file):')
        for k, v in sorted(split.items()):
            print(f'  {k}: {sorted(v)}')
    else:
        print('every photograph carries exactly one treatment site-wide')

    total = sum(changes.values())
    if changes:
        print(f'\n{"applied" if write else "would change"}:')
        for p, n in sorted(changes.items()):
            print(f'  {p:<26} {n}')
    print(f'\n{total} image(s) {"changed" if write else "would change"}')
    if not write and total:
        print('re-run with --write to apply')
    return 1 if split else 0


if __name__ == '__main__':
    sys.exit(main())
