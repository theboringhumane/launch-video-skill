#!/usr/bin/env bash
# Contact sheet of a video: one tile per 1/fps seconds, 6 columns.
# usage: sheet.sh <video> <out.png> [fps=1] [tile-width=384]
set -euo pipefail
in=$1 out=$2 fps=${3:-1} w=${4:-384}
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
n=$(awk -v d="$dur" -v f="$fps" 'BEGIN{print int(d*f+0.999)}')
rows=$(( (n + 5) / 6 ))
ffmpeg -v error -y -i "$in" -vf "fps=$fps,scale=$w:-1,tile=6x$rows" -frames:v 1 "$out"
echo "$out ($n tiles)"
