#!/usr/bin/env bash
# Extract JPEG frames from a video for a scroll-scrub image sequence (drawn to a
# canvas on scroll — see references/scroll-effects.md). Lanczos downscale keeps
# them crisp and small.
# Usage: extract-frames.sh <input.mp4> <fps> <scaleWidth> <outDir>
#   e.g. extract-frames.sh promo.mp4 12 1200 ./seq   ->  ./seq/frame-001.jpg ...
set -euo pipefail
IN="${1:?usage: extract-frames.sh <input.mp4> <fps> <scaleWidth> <outDir>}"
FPS="${2:?usage: extract-frames.sh <input.mp4> <fps> <scaleWidth> <outDir>}"
W="${3:?usage: extract-frames.sh <input.mp4> <fps> <scaleWidth> <outDir>}"
OUTDIR="${4:?usage: extract-frames.sh <input.mp4> <fps> <scaleWidth> <outDir>}"

mkdir -p "$OUTDIR"
ffmpeg -y -i "$IN" -vf "fps=${FPS},scale=${W}:-2:flags=lanczos" -q:v 4 "$OUTDIR/frame-%03d.jpg"

echo "frames -> $OUTDIR ($(ls "$OUTDIR" | wc -l | tr -d ' ') files)"
