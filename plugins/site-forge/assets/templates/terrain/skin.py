#!/usr/bin/env python3
"""Re-skin the terrain template so it never ships twice looking the same.

The template locks the COMPOSITION (photo headers, wave dividers, rotating photo
masks, layered cards, utility bar + dropdown nav, no text-only bands). This file
varies the SKIN: palette, type pairing and the divider curve.

    python3 skin.py --list
    python3 skin.py --skin slate-clay --font editorial --wave 2
    python3 skin.py --slug a lawn-care client-lawn        # deterministic pick from the slug

Deterministic mode is the one to use in a fleet: the same client always gets the
same skin, and two different clients are very unlikely to collide.
"""
import argparse
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- palettes
# Deliberately NOT the reference site's green + red. Each is a complete role
# set: primary surface green-equivalent, deep variant, accent (CTA), tint.
SKINS = {
    "forest-ember": dict(
        primary="#25603C", primary_d="#1A492C", primary_l="#2F7A4B",
        accent="#D2542B", accent_d="#B0421F",
        tint="rgba(37,96,60,.05)", note="deep forest + ember orange. Warm, grounded."),
    "slate-clay": dict(
        primary="#33484F", primary_d="#243539", primary_l="#415A63",
        accent="#C0592F", accent_d="#9E4623",
        tint="rgba(51,72,79,.05)", note="cool slate + terracotta. Reads premium, less 'lawn'."),
    "olive-brick": dict(
        primary="#4A5A2B", primary_d="#374420", primary_l="#5D7038",
        accent="#A8362C", accent_d="#8A2A21",
        tint="rgba(74,90,43,.05)", note="muted olive + brick. Agricultural, honest."),
    "pine-brass": dict(
        primary="#1F4739", primary_d="#15332A", primary_l="#2A5C4A",
        accent="#B0802F", accent_d="#8F6624",
        tint="rgba(31,71,57,.05)", note="pine + brass. The most 'established' feeling."),
    "ink-lime": dict(
        primary="#1E2A24", primary_d="#141C18", primary_l="#2C3D34",
        accent="#5E8C1F", accent_d="#4A7016",
        tint="rgba(30,42,36,.05)", note="near-black + field lime. Modern, high contrast."),
    "harbor-rust": dict(
        primary="#22505E", primary_d="#173A45", primary_l="#2E6577",
        accent="#C25A28", accent_d="#A0461D",
        tint="rgba(34,80,94,.05)", note="harbour blue + rust. Good for coastal/marine trades."),
}

# ---------------------------------------------------------------- type
# Display face carries the personality. Body stays quiet and readable.
# Roboto is deliberately absent: it trips the overused-font detector.
FONTS = {
    "editorial": dict(
        display="Playfair Display", display_w="ital,wght@0,600;0,700;1,500",
        body="Source Sans 3", body_w="wght@400;600;700",
        note="high-contrast serif. Traditional, trustworthy, closest to the reference."),
    "grotesk": dict(
        display="Bricolage Grotesque", display_w="opsz,wght@12..96,600;12..96,700;12..96,800",
        body="Instrument Sans", body_w="wght@400;500;600;700",
        note="chunky variable sans. Modern, confident, no serif at all."),
    "slab": dict(
        display="Zilla Slab", display_w="wght@600;700",
        body="Public Sans", body_w="wght@400;600;700",
        note="slab serif. Sturdy and industrial, good for trades and construction."),
    "humanist": dict(
        display="Fraunces", display_w="opsz,wght@9..144,600;9..144,700",
        body="Figtree", body_w="wght@400;600;700",
        note="soft optical serif. Warmer, good for residential and family-facing."),
    "condensed": dict(
        display="Archivo", display_w="wght@600;700;800",
        body="Karla", body_w="wght@400;600;700",
        note="tight grotesque. Utilitarian, reads as efficient rather than premium."),
}

# ---------------------------------------------------------------- dividers
WAVES = [
    "M0,54 C220,110 420,6 720,44 C1010,80 1220,18 1440,52 L1440,110 L0,110 Z",
    "M0,72 C180,18 380,96 700,58 C980,26 1200,92 1440,44 L1440,110 L0,110 Z",
    "M0,40 C260,96 480,20 760,66 C1040,110 1240,34 1440,74 L1440,110 L0,110 Z",
    "M0,88 C200,34 460,88 720,40 C990,-8 1230,70 1440,30 L1440,110 L0,110 Z",
]



REGISTRY = ROOT / "assigned-skins.json"


def assign(slug):
    """Pick a combo for `slug` that no other client in the fleet already has.

    Independent modulo on three hash bytes wastes the space and collides badly:
    across 15 real fleet slugs it produced a THREE-way identical assignment
    (170, 14 and 80 all land on 2 mod 6). Instead the hash indexes the FLATTENED
    combo space, then linear-probes past anything already taken and records the
    result, so two live sites can never look the same until all combos are used.
    """
    space = [(sk, fo, wv) for sk in SKINS for fo in FONTS for wv in range(len(WAVES))]
    try:
        taken = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        taken = {}
    if slug in taken:
        sk, fo, wv = taken[slug]
        return sk, fo, wv
    used = {tuple(v) for v in taken.values()}
    start = int.from_bytes(hashlib.sha256(slug.encode()).digest()[:4], "big") % len(space)
    for i in range(len(space)):
        cand = space[(start + i) % len(space)]
        if cand not in used:
            taken[slug] = list(cand)
            REGISTRY.write_text(json.dumps(taken, indent=2, sort_keys=True), encoding="utf-8")
            return cand
    raise SystemExit(f"all {len(space)} skin combos are assigned; add palettes or fonts")


def apply(skin_key, font_key, wave_idx, files):
    s, f = SKINS[skin_key], FONTS[font_key]
    wave = WAVES[wave_idx % len(WAVES)]
    changed = []
    for p in files:
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        orig = t
        # palette: rewrite only the token declarations, never other colour usage
        t = re.sub(r"--green:#[0-9A-Fa-f]{6}", f"--green:{s['primary']}", t)
        t = re.sub(r"--green-d:#[0-9A-Fa-f]{6}", f"--green-d:{s['primary_d']}", t)
        t = re.sub(r"--green-l:#[0-9A-Fa-f]{6}", f"--green-l:{s['primary_l']}", t)
        t = re.sub(r"--red:#[0-9A-Fa-f]{6}", f"--red:{s['accent']}", t)
        t = re.sub(r"--red-d:#[0-9A-Fa-f]{6}", f"--red-d:{s['accent_d']}", t)
        t = re.sub(r"--tint:rgba\([^)]*\)", f"--tint:{s['tint']}", t)
        # type
        t = re.sub(r"--serif:'[^']+'", f"--serif:'{f['display']}'", t)
        t = re.sub(r"--sans:'[^']+'", f"--sans:'{f['body']}'", t)
        t = re.sub(
            r"https://fonts\.googleapis\.com/css2\?family=[^\"]+",
            f"https://example-business.com/css2?family={f['display'].replace(' ', '+')}:{f['display_w']}"
            f"&family={f['body'].replace(' ', '+')}:{f['body_w']}&display=swap", t)
        # theme-color meta follows the primary
        t = re.sub(r'(<meta name="theme-color" content=")#[0-9A-Fa-f]{6}', r"\1" + s["primary"], t)
        # divider curve
        t = re.sub(r'd="M0,\d+ C[^"]+Z"', f'd="{wave}"', t)
        if t != orig:
            p.write_text(t, encoding="utf-8")
            changed.append(p.name)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--skin", choices=SKINS)
    ap.add_argument("--font", choices=FONTS)
    ap.add_argument("--wave", type=int, default=0)
    ap.add_argument("--slug", help="derive a deterministic skin from a client slug")
    a = ap.parse_args()

    if a.list:
        print("PALETTES")
        for k, v in SKINS.items():
            print(f"  {k:14} {v['primary']} + {v['accent']}   {v['note']}")
        print("\nTYPE PAIRINGS")
        for k, v in FONTS.items():
            print(f"  {k:12} {v['display']} / {v['body']}   {v['note']}")
        print(f"\nWAVES: {len(WAVES)} curve variants (--wave 0..{len(WAVES)-1})")
        return

    if a.slug:
        skin, font, wave = assign(a.slug)
    else:
        skin, font, wave = a.skin or "forest-ember", a.font or "editorial", a.wave

    files = [ROOT / "index.html"] + sorted(ROOT.glob("*/index.html")) + sorted(ROOT.glob("*/*/index.html"))
    changed = apply(skin, font, wave, files)
    print(f"skin={skin}  font={font}  wave={wave}")
    print(f"  {SKINS[skin]['note']}")
    print(f"  {FONTS[font]['note']}")
    print(f"  rewrote {len(changed)} file(s)")
    print("  now run: python3 build.py")


if __name__ == "__main__":
    main()
