#!/usr/bin/env bash
# Generate one Kokoro voiceover file per line of a script file.
# usage: vo-lines.sh <script.txt> <out-dir> [voice=af_heart] [speed=1.0]
# needs: HYPERFRAMES_PYTHON pointing at a Python with kokoro-onnx and soundfile (see references/audio.md)
set -euo pipefail
script=$1 out=$2 voice=${3:-af_heart} speed=${4:-1.0}
mkdir -p "$out"; i=0
while IFS= read -r line || [ -n "$line" ]; do
  [ -z "$line" ] && continue
  i=$((i + 1))
  npx --yes hyperframes tts "$line" -v "$voice" -s "$speed" -o "$out/l$i.wav" --json >/dev/null
  printf "l%-3s %6.2fs  %s\n" "$i" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/l$i.wav")" "$line"
done < "$script"
