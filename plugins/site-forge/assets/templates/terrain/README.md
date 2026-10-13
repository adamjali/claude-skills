# terrain — the "not empty" multipage template

A production multipage template for home-services trades: lawn and landscape,
tree work, junk removal, pressure washing, screens, gutters, roofing, pools.

It exists because five earlier fleet builds were described as feeling **empty**,
and the diagnosis is written up in `../../references/page-composition.md`. This
template is that doctrine already implemented.

**The template locks the composition. `skin.py` forces the skin to vary.** That
split is the point: the thing that makes it good is reusable, the thing that
would make it repetitive is not.

---

## Use it

```bash
cp -r <this dir> ~/money/<client-slug>
cd ~/money/<client-slug>
cp /path/to/client/photos/*.jpg assets/          # see assets/README.txt for names
python3 skin.py --slug <client-slug>             # unique palette + type + wave
# edit index.html: business name, phone, copy, service names
python3 build.py                                 # regenerates all 18 inner pages
netlify deploy --prod --dir .
```

`build.py` reads the `<style>`, utility bar, nav and footer out of `index.html`
and stamps them into every generated page, so **edit chrome in `index.html` only**
and rebuild. The chrome cannot drift; verify with an md5 of the `<style>` block
across pages.

---

## What ships

19 pages in the reference site's information architecture, hubs with **nested**
sub-services:

```
/                     /about/        /gallery/     /service-areas/
/lawn-care/         → mowing-edging, shrub-trimming
/tree-care/         → tree-trimming, palm-trimming, storm-cleanup
/cleanups/          → junk-removal, pressure-washing
/mulch-and-beds/
/contact/           → thank-you
/privacy-policy/  /terms/
```

Plus `sitemap.xml`, `robots.txt`, `_headers` (CSP, HSTS, XFO, nosniff,
Permissions-Policy), `FAQPage` schema on every service page, a Netlify form, and
a demo disclaimer in the footer.

Rename the hubs and children in `build.py`'s `PAGES` list for a different trade.
A roofer becomes `/roofing/ → shingle-repair, flat-roof, storm-damage`; the
skeleton does not change.

---

## Re-skinning

```bash
python3 skin.py --list                      # see every palette and pairing
python3 skin.py --slug a lawn-care client-lawn         # deterministic, registry-backed
python3 skin.py --skin harbor-rust --font slab --wave 3   # manual override
```

6 palettes x 5 type pairings x 4 divider curves = **120 combinations**.

**Assignment is registry-backed, not plain hashing.** Independent modulo on three
hash bytes wastes the space and collides badly: across 15 real fleet slugs it
produced a three-way identical assignment. `skin.py` now indexes the flattened
combo space and linear-probes past anything already taken, recording the result
in `assigned-skins.json` (created on first use). **Two live sites cannot share a
skin** until all 120 combos are consumed.

None of the palettes are the reference site's green-and-red, and `Roboto` is
deliberately absent from the pairings because it trips the overused-font
detector.

---

## The rules this template encodes

Do not undo these when customising. Full reasoning in `page-composition.md`.

1. **No band is text-only.** Every section carries a photo, a masked image, an
   illustrated card grid or a layered composition.
2. **Photo-background header on every page**, not just the homepage, each ending
   in an organic wave divider.
3. **Rotate the photo masks** — circle, arch, blob, overlapping pair — rather
   than repeating one rounded rectangle.
4. **One deliberate overlap per major section** (a card straddling a photo edge,
   the seal crossing the wave). Overlap reads as composition.
5. **Vary band heights.** If every section measures within 10% of the others the
   page reads flat regardless of content quality. Do **not** collapse this to a
   single padding value; that target belongs to article pages and is what
   flattened the earlier builds.
6. **Card grids need images in their cells.** The 2x2 photo-card grid is one of
   the strongest patterns here. A grid of text boxes is the weakest.
7. **Utility bar + hover dropdowns stay.** They are a scope signal: they tell a
   visitor there are nineteen pages here, not one.

---

## Gotchas already fixed in this code

- **Hero images must be landscape.** A portrait source in a landscape band
  crops to its middle; a 1600x2400 lawn photo rendered as roofline.
- **The seal is a `textPath` and will clip.** Check
  `getComputedTextLength()` against `getTotalLength()` of the arc after changing
  the wording.
- `button.btn` explicitly resets `background`/`appearance`, or a real `<button>`
  inherits the UA `buttonface` fill and ships invisible.
- All form controls are 16px so iOS does not zoom on focus.
- `picture{display:contents}` wherever a masked image is wrapped in `<picture>`.
