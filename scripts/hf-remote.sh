#!/usr/bin/env bash
# Run a HyperFrames command on another machine over SSH and pull the results back.
# usage: HF_REMOTE=user@host hf-remote.sh <project-dir> <hyperframes args...>
# e.g.   HF_REMOTE=me@studio-mac hf-remote.sh ./my-launch render -q delivery -f 60 -o renders/out.mp4
# The remote needs node and ffmpeg. Renders are serialised with a lock so two never overlap.
set -euo pipefail
host=${HF_REMOTE:?set HF_REMOTE=user@host}
proj=$(cd "$1" && pwd); shift
dir="hf-remote/$(basename "$proj")"
ssh -o BatchMode=yes "$host" "mkdir -p ~/$dir"
rsync -az --exclude node_modules --exclude renders "$proj/" "$host:$dir/"
args=$(printf '%q ' "$@")
lock=""
[ "$1" = render ] && lock="until mkdir ~/hf-remote/.lock 2>/dev/null; do sleep 5; done; trap 'rmdir ~/hf-remote/.lock' EXIT;"
rc=0
ssh -o BatchMode=yes "$host" "$lock cd ~/$dir && bash -lc 'npx --yes hyperframes $args'" || rc=$?
rsync -azu --exclude node_modules "$host:$dir/" "$proj/"
exit $rc
