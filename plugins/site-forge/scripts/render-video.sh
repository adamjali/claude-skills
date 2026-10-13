#!/usr/bin/env bash
# Render a Remotion composition to mp4 the macOS-safe way: render frames as a
# JPEG sequence (audio NOT in the composition), then stitch with system ffmpeg.
# A direct `remotion render ... out.mp4` ABORTS on macOS < 15 (Sequoia) with a
# dyld _AVCaptureDeviceTypeContinuityCamera SIGABRT in the bundled ffprobe the
# moment it reads audio. The sequence path never invokes that probe.
# Usage: render-video.sh <CompositionId> <projectDir> <audio.wav> <out.mp4> [fps]
set -euo pipefail
COMP="${1:?usage: render-video.sh <CompositionId> <projectDir> <audio.wav> <out.mp4> [fps]}"
DIR="${2:?usage: render-video.sh <CompositionId> <projectDir> <audio.wav> <out.mp4> [fps]}"
AUDIO="${3:?usage: render-video.sh <CompositionId> <projectDir> <audio.wav> <out.mp4> [fps]}"
OUT="${4:?usage: render-video.sh <CompositionId> <projectDir> <audio.wav> <out.mp4> [fps]}"
FPS="${5:-30}"

FRAMES="$DIR/out/frames"
rm -rf "$FRAMES"; mkdir -p "$FRAMES"

# 1) silent frame sequence (no audio probe -> no macOS abort)
( cd "$DIR" && npx remotion render "$COMP" out/frames --sequence --image-format=jpeg --jpeg-quality=90 --concurrency=2 )

# 2) stitch frames + audio with the system ffmpeg.
#    Remotion's --sequence pads element-NNN.jpeg to the WIDTH OF THE FRAME COUNT,
#    so a 900-frame render emits element-000.jpeg but a 1290-frame render emits
#    element-0000.jpeg. Hardcoding %03d silently fails the stitch after a full
#    render ("Could find no file with path ... index in the range 0-4"), which is
#    an expensive way to find out. Derive the width from an actual file instead.
# NOTE: `ls "$FRAMES" | head -1` looks equivalent but dies here — head closes the pipe,
# ls takes SIGPIPE, and `set -o pipefail` turns that into a script abort AFTER a full
# render. Glob into an array instead; no pipe, no signal.
shopt -s nullglob
FRAMEFILES=("$FRAMES"/element-*.jpeg)
FIRST=$(basename "${FRAMEFILES[0]}")             # e.g. element-0000.jpeg
DIGITS=${FIRST#element-}; DIGITS=${DIGITS%.jpeg}
PAD="%0${#DIGITS}d"
echo "frame pattern: element-$PAD.jpeg (${#FRAMEFILES[@]} frames)"

ffmpeg -y -framerate "$FPS" -i "$FRAMES/element-$PAD.jpeg" -i "$AUDIO" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$OUT"

echo "rendered -> $OUT"
