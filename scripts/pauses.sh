#!/usr/bin/env bash
# Print the pauses inside a voiceover line, to time visuals to its phrases.
# usage: pauses.sh <line.wav> [threshold-dB=-35] [min-pause-s=0.12]
set -euo pipefail
ffmpeg -nostats -i "$1" -af "silencedetect=n=${2:--35}dB:d=${3:-0.12}" -f null - 2>&1 |
  grep -oE "silence_(start|end): [0-9.]+" | awk '{v=sprintf("%.2f",$2)} /start/{s=v} /end/{printf "silence %s–%s\n", s, v}'
printf "duration %.2f\n" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1")"
