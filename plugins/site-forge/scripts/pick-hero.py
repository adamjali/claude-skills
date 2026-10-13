#!/usr/bin/env python3
"""Score every photograph for how well it works as a full-bleed hero.

The previous pass picked the hero by "most colourful plus most contrast", which
sounds right and is not. Those two metrics select for tight, dark, high-ISO night
frames full of bokeh: dramatic, and hostile to type.

The reference hero Adam keeps pointing at works for the opposite reasons. It is a
wide establishing shot, bright, with a large calm region for the headline to sit
in. So the score here is:

  air      how much of the frame is quiet, measured as the share of tiles whose
           local standard deviation is low. A busy frame has nowhere for type.
  calm     the same measure restricted to the lower-left quadrant, where this
           layout actually puts the headline.
  light    mean luminance. Airy beats moody for an opening frame.
  wide     native aspect ratio. A portrait frame in a 16:9 band is 60% thrown away.
  hold     contrast still matters, but only in the type zone, and only enough to
           clear AA-large against white once the scrim is on.

Reported separately so the trade-off is visible rather than hidden in one number.

    python3 src/pick-hero.py
"""
import pathlib
import sys

# vendored into the skill: the site root is wherever you run this from
ROOT = pathlib.Path.cwd()

try:
    from PIL import Image, ImageStat
except ImportError:
    print('Pillow required')
    sys.exit(2)

TILE = 8          # tiles across for the local-variance grid


def score(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    g = im.convert('L').resize((256, int(256 * h / w)) if w >= h
                               else (int(256 * w / h), 256))
    gw, gh = g.size

    # local standard deviation per tile
    stds = []
    quiet_lowleft = []
    for ty in range(TILE):
        for tx in range(TILE):
            box = (tx * gw // TILE, ty * gh // TILE,
                   (tx + 1) * gw // TILE, (ty + 1) * gh // TILE)
            s = ImageStat.Stat(g.crop(box)).stddev[0]
            stds.append(s)
            # lower-left quadrant: where the headline sits
            if ty >= TILE // 2 and tx < TILE // 2:
                quiet_lowleft.append(s)

    busy = sum(stds) / len(stds)
    air = sum(1 for s in stds if s < 30) / len(stds)
    calm = sum(1 for s in quiet_lowleft if s < 30) / len(quiet_lowleft)

    stat = ImageStat.Stat(g)
    light = stat.mean[0] / 255

    # luminance of the type zone only, which is what the scrim has to solve for
    zone = g.crop((0, int(gh * 0.55), int(gw * 0.62), gh))
    zone_l = ImageStat.Stat(zone).mean[0] / 255

    return {
        'name': path.stem.replace('-2400', ''),
        'ratio': w / h,
        'air': air, 'calm': calm, 'light': light,
        'busy': busy, 'zone': zone_l,
    }


def main():
    rows = []
    for p in sorted((ROOT / 'assets' / 'img').glob('*-1200.webp')):
        if '-mono' in p.stem:
            continue
        try:
            rows.append(score(p))
        except Exception as e:
            print(f'  skip {p.name}: {e}')

    # a hero wants: wide, light, calm where the type goes, not busy overall.
    # zone luminance is a penalty at BOTH ends: a blown-out zone needs a heavy
    # scrim, a black zone means the photograph is dead exactly where it shows.
    for r in rows:
        wide = min(r['ratio'] / 1.5, 1.0)
        zone_fit = 1 - abs(r['zone'] - 0.42) / 0.42
        r['total'] = (r['calm'] * 0.34 + r['air'] * 0.20 + wide * 0.18
                      + r['light'] * 0.14 + max(0, zone_fit) * 0.14)

    rows.sort(key=lambda r: -r['total'])
    print(f'{"frame":<16}{"score":>7}{"calm":>7}{"air":>7}{"ratio":>7}'
          f'{"light":>7}{"busy":>7}{"zone":>7}')
    for r in rows[:14]:
        print(f'{r["name"]:<16}{r["total"]:>7.3f}{r["calm"]:>7.2f}{r["air"]:>7.2f}'
              f'{r["ratio"]:>7.2f}{r["light"]:>7.2f}{r["busy"]:>7.1f}{r["zone"]:>7.2f}')
    print('\nworst five, for contrast:')
    for r in rows[-5:]:
        print(f'{r["name"]:<16}{r["total"]:>7.3f}{r["calm"]:>7.2f}{r["air"]:>7.2f}'
              f'{r["ratio"]:>7.2f}{r["light"]:>7.2f}{r["busy"]:>7.1f}{r["zone"]:>7.2f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
