# Studying a reference video

When someone says "make it like this", the goal is the same *feel*: the same pace, the same kind of
motion, and the same rhythm of holds and hits. The content is entirely yours. Spend 15 minutes
here; it saves hours of guessing later.

## 1. Get the file and its facts

```bash
yt-dlp "<url>" -o refs/name.mp4
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of csv=p=0 refs/name.mp4
```

Write down the duration, frame rate and size, and whether it has an audio stream. Some don't; then
your version is SFX-only, or you bring your own music.

## 2. Look at it

A 1 fps contact sheet shows the scene structure at a glance:

```bash
scripts/sheet.sh refs/name.mp4 refs/name-sheet.png          # 1 fps, 6 columns
scripts/sheet.sh refs/name.mp4 refs/name-fast.png 4         # 4 fps for fast stretches
```

For a stretch that moves fast (a whip, a burst, a typing run), take 4–10 fps of just that range:
`ffmpeg -ss 12 -t 2 -i refs/name.mp4 -vf fps=10,scale=480:-1,tile=5x4 burst.png`.

## 3. Measure the motion

`scripts/heat.py` runs optical flow on every frame and writes:

- `motion.json`: per frame, the flow magnitude (how much moves), the pixel diff (cuts and fades),
  the mean direction (dx, dy) and where the motion is (cx, cy); plus a cut list and per-segment stats.
- `energy.png`: the motion curve (orange) with the diff curve and cut lines over it. The peaks
  are your hits.
- `seg_*.png`: where each segment moves. A heatmap concentrated in one corner means a corner
  element moves while everything else holds.
- `heat_overlay.mp4`: the clip with a heat overlay.

```bash
uv run --with opencv-python-headless --with numpy python -I scripts/heat.py refs/name.mp4 analysis/
```

How to read it:

- **Cuts** (diff spikes) are scene boundaries. Copy their times into the beat map exactly.
- **Big dx at a boundary** is a whip or slide; the sign gives the direction (dx < 0 means it moves left).
- **Flow that rises and then decays** is an ease-out entrance. A sharp spike followed by stillness
  is a hit or snap.
- **Long low-flow stretches** are holds. Keep them: holds are what make a fast video feel calm.

## 4. Write the beat map

`BEATS.md`, one row per beat:

| t (s) | Reference beat | Motion | Your beat |
| --- | --- | --- | --- |
| 0.00–0.73 | giant gradient word rises, cropped | letters stagger up, power3.out; hard cut | giant **YOU** |
| 0.73–1.50 | glass blob, white words type in | blob pops 0.7→1, breathes | "You wrote" |

Above the table, state the reference's look in one line (e.g. "near-black, small white type built
word by word, faint HUD grid") and your message in one line.

## 5. Shortening a long reference

When the reference runs 90–130 s and you want 45–60 s:

- Keep its opening and its ending whole. Those carry the feel.
- Drop middle beats that make the same point twice. Keep one example of each motion idea.
- Cut the music at phrase boundaries (listen, or find bar lines with `npx hyperframes beats`),
  crossfade 0.3–0.5 s, and fade out over the last 2 s.

## 6. Compare as you build

`npx hyperframes snapshot --at 3,7,12 --against refs/name.mp4` puts your frame next to the
reference's at the same time. Use it for timing and composition only. Look at your own frames on
their own too: a side-by-side sheet once made someone think the reference's brand had leaked into
the video.
