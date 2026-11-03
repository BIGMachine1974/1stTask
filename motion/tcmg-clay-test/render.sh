#!/usr/bin/env bash
# Assemble the clay poses into the review video: 12 poses a second, each held for 2 frames at 24 fps (on twos),
# upscaled to 1080x1920, with the cost video's music bed under it.
#   usage: BLENDER=/path/to/blender bash render.sh      (renders any missing poses first, then muxes)
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
if [ -n "${BLENDER:-}" ]; then "$BLENDER" -b -P make_clay.py -- poses --res 540 --samples 10; fi
mkdir -p REVIEW
ffmpeg -v error -y -framerate 12 -i poses/p%03d.png -i ../tcmg-cost-v2/bed_c.mp3 \
  -vf "fps=24,scale=1080:1920:flags=lanczos,format=yuv420p" -c:v libx264 -crf 18 -preset medium \
  -af "afade=t=in:d=0.3,afade=t=out:st=5.2:d=0.8" -c:a aac -b:a 192k -shortest \
  REVIEW/01-tcmg-clay-test-find-your-street-9x16.mp4
echo "wrote $D/REVIEW/01-tcmg-clay-test-find-your-street-9x16.mp4"
