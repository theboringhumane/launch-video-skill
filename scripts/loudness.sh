#!/usr/bin/env bash
# Normalise a render's audio to -15 LUFS / -1.5 dBTP without re-encoding the picture.
# usage: loudness.sh <in.mp4> <out.mp4> [target-LUFS=-15]
set -euo pipefail
ffmpeg -v error -y -i "$1" -c:v copy -af "loudnorm=I=${3:--15}:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k "$2"
ffmpeg -nostats -i "$2" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)"
