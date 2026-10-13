# Remotion promo video — proven end-to-end pipeline

A scene-based promo with a voiceover and karaoke captions, rendered the
**macOS-safe way**. This is the exact pipeline that shipped; generalize the
names/brand. Build the video *after* the site, only if the brief wants one.

Scripts referenced here live in `${CLAUDE_SKILL_DIR}/scripts/` and take
arguments — run them, don't reimplement them.

## Contents
1. [Stack & project shape](#1-stack--project-shape)
2. [Step 1 — Voiceover (edge-tts)](#2-step-1--voiceover-edge-tts)
3. [Step 2 — Karaoke captions](#3-step-2--karaoke-captions)
4. [Step 3 — Audio mix](#4-step-3--audio-mix)
5. [Step 4 — Render (the macOS < 15 workaround)](#5-step-4--render-the-macos--15-workaround)
6. [Composition structure](#6-composition-structure)
7. [Install just-in-time](#7-install-just-in-time)

---

## 1. Stack & project shape
Remotion `4.0.481` + React `18.3.1`. Deps: `remotion`, `@remotion/cli`,
`@remotion/captions`, `@remotion/google-fonts`. A minimal project:

```
video/
├── package.json          # deps above
├── remotion.config.ts
├── tsconfig.json
├── src/
│   ├── index.ts          # registerRoot(RemotionRoot)
│   ├── Root.tsx          # <Composition> config (id, fps, size, durationInFrames)
│   ├── Promo.tsx         # the scenes + <Captions/>
│   └── captions.json     # generated (step 2)
├── public/               # images referenced via staticFile('x.jpg')
└── assets/               # vo-script.txt, vo.mp3, vo.srt, music.mp3, mixed.wav
```

Root.tsx is tiny — one `<Composition id="Promo" component={Promo}
durationInFrames={N} fps={30} width={1920} height={1080} />`. Fonts load via
`loadFont()` from `@remotion/google-fonts/<Family>` (pick distinctive fonts to
match the site's theme).

## 2. Step 1 — Voiceover (edge-tts)
Write the narration to `assets/vo-script.txt` (plain prose, ~1 short paragraph
per ~10s). Generate the audio **and** a sentence-level SRT in one call:

```bash
edge-tts --voice en-US-AndrewNeural --rate=-4% \
  --file assets/vo-script.txt \
  --write-media assets/vo.mp3 \
  --write-subtitles assets/vo.srt
```

`en-US-AndrewNeural` is a warm, credible male VO; `--rate=-4%` slows it slightly.
**This is the house voice. Do not substitute.** ChristopherNeural at +8% was used once on
a small-engine client and Adam's reaction was "the vo voice is horrible? what happened, prev
were always good?". Verify the render by PITCH rather than by ear:

```bash
ffmpeg -v error -i vo.mp3 -t 8 -ac 1 -ar 22050 -f wav /tmp/v.wav -y
# autocorrelate voiced frames; median F0 should land near 110 Hz to match the fleet
```

**Write initialisms for the ear.** `A.T.V.s` is spoken as "a t v s". Write **`A T V's`**.
Same class: phone numbers are always digit-by-digit ("eight six three"), never "eight
hundred sixty three"
for gravitas. Check duration with `ffprobe -v error -show_entries
format=duration -of csv=p=0 assets/vo.mp3` and size the composition to fit
(`durationInFrames ≈ ceil(seconds * fps) + a short tail`).

## 3. Step 2 — Karaoke captions
edge-tts emits **sentence-level** cues. Convert them to **word-level**
`@remotion/captions` tokens (so words light up in sync) with the bundled script:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/build-captions.py
# reads assets/vo.srt  ->  writes src/captions.json
```

It distributes each sentence's exact `[start,end]` across its words weighted by
length — deterministic, stdlib-only, perfectly bounded to the VO. (Run it from
the video project dir, or edit its `HERE`-relative paths.)

In the composition, page the tokens and render a **readable** caption — the two
details that made captions legible over busy footage:

```tsx
import { createTikTokStyleCaptions } from '@remotion/captions';
import captionsJson from './captions.json';
const { pages } = createTikTokStyleCaptions({
  captions: captionsJson as any,
  combineTokensWithinMilliseconds: 1100, // ~one short line per page
});

// inside <Captions/>: find the active page by time, then per token:
//   color: active ? GOLD : 'rgba(255,255,255,.85)'   // karaoke highlight
// and wrap the line in a lozenge so it never washes out on bright frames:
//   backgroundColor: 'rgba(15,30,40,.74)', padding: '18px 42px',
//   borderRadius: 20, boxShadow: '0 12px 34px rgba(0,0,0,.4)'
```

The lozenge/pill background + text-shadow is the fix for "captions hard to read";
the gold-vs-white token color is the karaoke effect.

## 4. Step 3 — Audio mix
Mix the VO over a low music bed and normalize to broadcast loudness:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/mix-audio.sh assets/vo.mp3 assets/music.mp3 assets/mixed.wav
```

(Music at `volume=0.20`, `amix` with `duration=first`, then
`loudnorm=I=-14:TP=-1.5:LRA=11`.) **Do not** put `<Audio>` in the composition —
audio is muxed in post (next step), which is also what dodges the macOS bug.

**`amix` has no `normalize=0` on older ffmpeg** (e.g. 4.3.x): passing it aborts
with `Error initializing complex filters / Option not found`. The trap is that
`amix` *always* normalizes by halving every input, so the obvious "fix" (drop the
option) leaves the whole mix — voice included — too quiet; a too-quiet bed is the
tell that someone worked around it wrong. To mix a bed **under** a voiceover
without `normalize`: pre-attenuate the music, let `amix` halve both, then push the
sum back up so the VO returns to full while the pre-set music sits audibly beneath
it:

```bash
ffmpeg -i vo.mp3 -i music.mp3 \
  -filter_complex "[1:a]volume=0.28[m];[0:a][m]amix=inputs=2:duration=first,volume=2[a]" \
  -map "[a]" mixed.wav
```

## 5. Step 4 — Render (the macOS < 15 workaround)
**Why this is non-obvious:** on macOS older than 15 (Sequoia), a direct
`remotion render <Comp> out.mp4` **aborts** the moment it reads an audio asset.
Remotion's bundled `ffprobe` (`@remotion/compositor-darwin-x64`) links against a
newer AVFoundation symbol that isn't present:

```
dyld[]: Symbol not found: (_AVCaptureDeviceTypeContinuityCamera)
Command was killed with SIGABRT (Aborted): .../compositor-darwin-x64/ffprobe ...
→ Remotion requires macOS 15 (Sequoia) or later.
```

**The fix** (keep the composition silent, render frames, mux audio with *system*
ffmpeg):

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/render-video.sh Promo ./video assets/mixed.wav out/promo.mp4 30
```

That script: renders a JPEG **sequence** (`remotion render Promo out/frames
--sequence --image-format=jpeg`), which never invokes the audio probe, then
stitches frames + `mixed.wav` with the system `ffmpeg` into an H.264 mp4. On
macOS ≥ 15 the direct render works too, but the sequence path is harmless and
portable — prefer it. (Frames are named `element-NNN.jpeg`, 0-indexed.)

To re-render after a copy change: regenerate VO → captions → mix → render. A
narration word change must flow through *all four* (the audio says it, the
captions time to it) — don't edit only `captions.json`.

## 6. Composition structure
Scenes are `<Sequence from={f} durationInFrames={d}>` stacked in one
`<AbsoluteFill>`, each fading via an `interpolate` opacity envelope; entrances
use `spring()`. Useful building blocks (see the shipped `Promo.tsx`): a
`KenBurns` image (scale + pan over time), a `Words` stagger (per-word spring
delay), `Chip` pills, a final contact "card". Put `<Captions/>` and an optional
vignette/grain `<AbsoluteFill>` last so they sit on top.

## 7. Install just-in-time
Only when the brief calls for a video: `npm i` the Remotion deps in the project,
and ensure `edge-tts` (`pip install edge-tts` / `pipx install edge-tts`) and
`ffmpeg` are present. In `auto` mode, if any of these fail or need interaction,
skip the video and flag "upgrade: add a promo video"; in `full`, ask the user to
help install.

---

# Learned rebuilding the LATENT film (2026-07-31)

## The Ken Burns push is the default gesture. Cut it.

A slow scale on every still is what a slideshow does. It says nothing about the
photograph and it is the same gesture every time, which is the definition of
filler. The client's word for it was "the stupid bland zoom".

**Replace it with a real idea from the subject.** On a photography film that is the
FILM ADVANCE: frames held perfectly still, and the cut is the strip pulling up
through the gate with the black rebate passing between frames.

```tsx
const REBATE = height * 0.085;
const travel = height + REBATE;
const y = (1 - inP) * travel - outP * travel;   // inP/outP eased over ~0.34s
```

Render the incoming frame behind the outgoing one so the gate is never empty.

**Verify the hold is genuinely static**: two frames inside one hold must be
pixel-identical in a region away from the type. `max diff 0` or the zoom is still
in there somewhere.

## Portraits in a 16:9 gate lose 55-63%

`object-fit: cover` on a 2:3 portrait in a 1.78 gate keeps 37% of the height, and
on a wedding photograph that is reliably the subject's head. Measure the whole
set before laying out the edit.

Portraits become **plates**: shown whole against the ground, offset to one side,
with the type living in the space beside them. Landscapes still bleed. The film
gets rhythm out of it as a bonus.

## Positioned type: anchor from the correct edge

An absolutely positioned block with `left: 93%` and no width gets **shrink-to-fit
sizing from only the space remaining to its right** (1920 - 1786 = 134px). A
`translate(-100%)` then moves the box back so it LOOKS anchored, but the width was
already decided and `maxWidth: 56%` never got a chance. Result: a four-word
caption set one word per line.

```tsx
...(anchor === 'start' ? { left: x }
  : anchor === 'end'   ? { right: `calc(100% - ${x})` }
  :                      { left: 0, right: 0 })
```

Give `Rise`-style clip wrappers ~0.22em of `padding-bottom`, or `overflow:hidden`
shears every italic descender.

## Type belongs to its frame and must leave with it

Fade captions on the outgoing transition (`opacity: 1 - outP`). Without it the
type stays pinned while the photograph slides away and for a third of a second
one frame's words sit on top of the next frame's picture.

## Match the film's grade to the site's

If the site is a monochrome contact sheet, the film is too, with the same one or
two frames in colour. Otherwise it is a different object that happens to be
embedded. Same for the end card: a paper end card inside a dark film embedded in
an ink band strobes white every 34 seconds.

## Music: measure it, and be honest that you cannot hear it

Two tracks were rejected before this was taken seriously. **You cannot evaluate
audio.** What you CAN do is measure it, and the measurements are decisive:

```python
# onset strength = positive spectral flux; dyn = 20*log10(peak/median rms)
# quiet = share of frames under 8% of peak
```

| | rejected loop | licensed piano |
|---|---|---|
| onset density | 319 | 23 |
| dynamic range | 5.0 dB | 21.6 dB |
| genuine silence | 7% | 48% |

An onset density in the hundreds with 5 dB of range is a wall-to-wall compressed
loop with no quiet section anywhere to cut to. **No re-cut fixes that**, which is
worth saying out loud before spending an hour trying.

Synthesising a replacement is possible (inharmonic partial stack, per-partial
decay, Schroeder reverb) and it got from 319 to 71, but it still missed its own
targets and shipping audio you cannot judge, twice rejected, is a bad bet. Ask.

**Source, then licence properly.** Kevin MacLeod's catalogue is CC BY 4.0 and
downloadable at `https://example-business.com/music/royalty-free/mp3-royaltyfree/<Title>.mp3`.
Score several candidates on the profile above and take the winner. **CC BY
attribution is mandatory**: title, author, source, licence, on a visible page.

## Lock the edit to the track's real tempo

Detect BPM by autocorrelating the onset envelope, then put every cut on a bar
line. Do not force a track onto a grid you already built: re-time the beats. And
pick the WINDOW by measurement too, scoring 20-35s windows for sparseness,
dynamics and silence.

```python
ac = np.correlate(o, o, 'full')[len(o)-1:]
peak = lo + int(np.argmax(ac[lo:hi]))       # lo/hi bound 45-120 BPM
bpm = 60 * (sr/hop) / peak
```
