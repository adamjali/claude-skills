#!/usr/bin/env python3
"""Solve for the LIGHTEST hero scrim that still clears the contrast floor.

A scrim is a tax on the photograph. The usual move is to pick a comfortable
number like 45% and stop thinking, which is why so many photo heroes look muddy.
This composites the real hero frame under a candidate scrim, samples the actual
region the headline occupies, and reports the worst-case contrast for white type,
so the scrim can be set to the smallest value that passes rather than the first
value that felt safe.

Floors: 4.5:1 for the eyebrow (17px and under counts as body text),
3:1 for the headline (large text).

    python3 src/hero-scrim.py [image] [--tall]
"""
import pathlib
import sys

# vendored into the skill: the site root is wherever you run this from
ROOT = pathlib.Path.cwd()

try:
    from PIL import Image
except ImportError:
    print('Pillow required')
    sys.exit(2)


def rel_lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_white(rgb):
    return 1.05 / (rel_lum(rgb) + 0.05)


def composite(px, alpha, scrim=(6, 6, 7)):
    return tuple(round(p * (1 - alpha) + s * alpha) for p, s in zip(px, scrim))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    src = args[0] if args else 'assets/img/hero-05-2400.webp'
    im = Image.open(ROOT / src).convert('RGB')

    # the hero band is 100svh; the frame is cropped to the band's ratio by cover.
    # 1440x661 is the laptop case that has bitten this layout before.
    band_w, band_h = 1440, 661
    scale = max(band_w / im.width, band_h / im.height)
    im2 = im.resize((round(im.width * scale), round(im.height * scale)))
    left = (im2.width - band_w) // 2
    top = (im2.height - band_h) // 2
    band = im2.crop((left, top, left + band_w, top + band_h))

    # where the type actually sits: eyebrow and two display lines, lower left
    zones = {
        'eyebrow': (72, 300, 620, 335),
        'line 1': (72, 336, 620, 430),
        'line 2': (72, 430, 700, 590),
    }
    floors = {'eyebrow': 4.5, 'line 1': 3.0, 'line 2': 3.0}

    print(f'{src}   band {band_w}x{band_h}\n')
    for alpha in (0.0, 0.08, 0.14, 0.20, 0.26, 0.34, 0.46):
        worst = {}
        for name, box in zones.items():
            reg = band.crop(box)
            small = reg.resize((max(1, reg.width // 8), max(1, reg.height // 8)))
            # worst case is the BRIGHTEST pixel block under white type
            lo = min(contrast_white(composite(p, alpha)) for p in small.getdata())
            worst[name] = lo
        ok = all(worst[k] >= floors[k] for k in worst)
        line = '  '.join(f'{k} {v:5.2f}' for k, v in worst.items())
        print(f'  scrim {alpha:>5.0%}   {line}   {"PASS" if ok else "fail"}')

    print('\nFloors: eyebrow 4.5:1, display 3:1 (AA large).')
    print('Take the smallest PASS. Every point above it is contrast you are')
    print('buying with the photograph.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
