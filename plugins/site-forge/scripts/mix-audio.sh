#!/usr/bin/env bash
# Mix a voiceover over a music bed and normalize to broadcast loudness.
# Usage: mix-audio.sh <vo.mp3> <music.mp3> <out.wav>
set -euo pipefail
VO="${1:?usage: mix-audio.sh <vo.mp3> <music.mp3> <out.wav>}"
MUSIC="${2:?usage: mix-audio.sh <vo.mp3> <music.mp3> <out.wav>}"
OUT="${3:?usage: mix-audio.sh <vo.mp3> <music.mp3> <out.wav>}"

ffmpeg -y -i "$VO" -i "$MUSIC" \
  -filter_complex "[1:a]volume=0.20[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[a]" -ar 48000 "$OUT"

echo "mixed -> $OUT"
