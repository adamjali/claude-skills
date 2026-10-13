#!/usr/bin/env python3
"""Catch images that are being cropped badly by their frame.

Every `.frame` / `.plate-media` sets a fixed `aspect-ratio` and the image inside
is `object-fit: cover`. That means the frame's ratio, not the photograph's,
decides what you see. Drop a 2:3 portrait into a 2.4:1 pan and cover throws away
roughly 78% of it, usually including the subject's head.

Nothing else in the toolchain catches this: the file exists, the markup is valid,
the page renders, and the verifier passes. It only looks wrong.

    python3 src/check-crops.py            # report
    python3 src/check-crops.py --strict   # non-zero exit on any severe crop
"""
import pathlib
import re
import sys

# vendored into the skill: the site root is wherever you run this from
ROOT = pathlib.Path.cwd()

# the aspect-ratio each frame class enforces, from site.css
FRAMES = {
    'm-35': 3 / 2, 'm-35p': 2 / 3, 'm-645': 4 / 5, 'm-sq': 1.0,
    'm-pan': 2.4, 'm-tall': 5 / 8,
}
SEVERE = 0.40      # more than 40% of the photograph discarded
WARN = 0.25


def native_ratios():
    """width/height for every shipped webp, keyed by base name."""
    out = {}
    try:
        from PIL import Image
    except ImportError:
        print('Pillow required')
        sys.exit(2)
    for p in (ROOT / 'assets' / 'img').glob('*-1200.webp'):
        base = p.stem[:-5]
        try:
            w, h = Image.open(p).size
            out[base] = w / h
        except Exception:
            pass
    return out


def crop_loss(img_ratio, frame_ratio):
    """Fraction of the photograph's area that object-fit:cover discards."""
    if img_ratio > frame_ratio:            # image wider: sides are cut
        return 1 - (frame_ratio / img_ratio)
    return 1 - (img_ratio / frame_ratio)   # image taller: top and bottom are cut


def main():
    strict = '--strict' in sys.argv
    ratios = native_ratios()
    severe, warn = [], []

    for page in sorted(ROOT.glob('*.html')):
        html = page.read_text(encoding='utf-8')
        # a framed element and the first image inside it
        for m in re.finditer(
                r'<(?:figure|div)[^>]*class="([^"]*(?:frame|plate-media)[^"]*)"[^>]*>(.*?)</(?:figure|div)>',
                html, re.S):
            cls, body = m.group(1), m.group(2)
            frame = next((c for c in cls.split() if c in FRAMES), None)
            if not frame:
                continue
            im = re.search(r'src="assets/img/([a-z]+-\d+)(?:-mono)?-\d+\.webp"', body)
            if not im:
                continue
            name = im.group(1)
            r = ratios.get(name)
            if not r:
                continue
            loss = crop_loss(r, FRAMES[frame])
            row = (page.name, name, f'{r:.2f}', frame, f'{FRAMES[frame]:.2f}', f'{loss:.0%}')
            if loss >= SEVERE:
                severe.append(row)
            elif loss >= WARN:
                warn.append(row)

    def table(rows, title):
        if not rows:
            return
        print(f'\n{title}')
        print(f'  {"page":<26}{"image":<14}{"native":>7}{"frame":>9}{"forced":>8}{"lost":>7}')
        for r in rows:
            print(f'  {r[0]:<26}{r[1]:<14}{r[2]:>7}{r[3]:>9}{r[4]:>8}{r[5]:>7}')

    table(severe, f'SEVERE, over {SEVERE:.0%} of the photograph discarded:')
    table(warn, f'worth a look, over {WARN:.0%} discarded:')

    print(f'\n{len(severe)} severe, {len(warn)} borderline')
    if severe:
        print('\nFix by giving the frame the ratio the photograph actually has, or by')
        print('choosing a photograph shaped for the frame. Never by cropping harder.')
    return 1 if (strict and severe) else 0


if __name__ == '__main__':
    sys.exit(main())
