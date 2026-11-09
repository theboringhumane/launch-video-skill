---
name: launch-video
description: Make a short product launch or feature video (10–60 s) with HyperFrames, either from scratch or by rebuilding the pacing and motion of a reference video with your own brand. Covers studying a reference clip, the beat map, showing the real product UI, scene-by-scene GSAP motion, a voiceover (Kokoro, free and local), a music bed, sound effects, loudness, review and a 60 fps render. Use for "make a launch video", "promo for this feature/PR", "recreate this video for my product", or "video with voiceover for X".
---

# Launch video

A launch video in this skill is 10–60 seconds, 1920×1080, rendered at 60 fps. It shows the real
product, says one thing, and ends on the name and URL. It's built in
[HyperFrames](https://hyperframes.heygen.com): HTML scenes and a paused GSAP timeline, rendered frame
by frame, so every render comes out the same.

If the `hyperframes` skills are installed, read `/hyperframes` and `/hyperframes-core` once first.
This skill doesn't repeat their contract; it records the workflow and the choices that made these
videos work.

## What you need before starting

- **The subject.** A product URL, a merged PR, a changelog or a brief. A PR is the best source:
  its description tells you what shipped, what's paid, and what isn't live yet.
- **Brand kit.** Logo files (SVG or PNG), 4–6 hex colours, one or two fonts as `.woff2`. Put them
  in `<brand>-kit/` and reuse that folder across videos.
- **Real UI.** Screenshots, or pages you can render yourself (see "Showing the product").
- **Optional reference video.** If someone says "make it like this one", get the file
  (`yt-dlp <url> -o refs/name.mp4`) and follow `references/reference-analysis.md`.
- **Tools:** Node 20+, ffmpeg, `uv` (for the Python helpers), Google Chrome (for UI shots).

## The work loop

1. **Find the one message.** Write it as one sentence before anything else, e.g. "Every newsletter
   can now have its own website." Every scene has to serve it. Read the source for facts and write
   down anything you must not claim: features that aren't live, a competitor's name, plan limits.
2. **Study the reference** if there is one: contact sheet, motion heatmap, cut list.
   `references/reference-analysis.md`.
3. **Write the beat map** in `BEATS.md`: one row per beat, giving the time, what the reference does
   (if any), the motion, and what your version shows. Keep the reference's timing; replace every
   word, logo and screen with your own.
4. **Write the voiceover script** (if any) and generate it **one line per beat**. Measure each
   line, and set the scene durations from the voice, not the other way round.
   `references/audio.md`.
5. **Get the real UI** into `assets/`. Never draw a fake version of something that exists.
6. **Build one sub-composition per beat** in `compositions/`. `references/motion.md` has the patterns
   (word builds, typing, cursor clicks, whips, flick montages, count-ups, end cards) with code.
7. **Add sound:** voice, music bed, and SFX only on visible actions.
8. **Check and review.** Run `npx hyperframes check --json`, take snapshots at every beat, and look
   at them. `references/review.md`.
9. **Render** at 60 fps, normalise loudness to −15 LUFS, then look at a 1 fps sheet of the final
   MP4 before sending it.

## Project layout

```
my-launch/
  index.html             root: scene hosts + every <audio>, nothing else
  compositions/*.html    one scene per beat, each in a <template>
  assets/fonts/          woff2 files, declared with @font-face in each scene
  assets/ui/             real product screenshots
  assets/vo/             l1.wav, l2.wav … one per voiceover line
  assets/bgm/            the music bed
  assets/sfx/            click, pop, whoosh, typing
  BEATS.md               the beat map
  renders/               output
```

Start from `templates/index.html` and `templates/scene.html`.

## Rules that kept these videos clean

- **Your brand only.** When rebuilding a reference, copy its *structure* (timing, motion, layout
  rhythm), never its logo, UI, copy, characters or product shots. After the render, search your
  frames for the reference's name. Only use a reference's soundtrack if you hold a licence for it.
- **Real screens beat mockups.** If the product renders HTML (templates, emails, pages), render it
  with sample data and screenshot it at 1.5× (`scripts/shoot-pages.sh`). If it's an app, take
  screenshots at 2×. Draw a UI only when nothing real exists yet, and keep it plainly generic.
- **Claims come from the source.** Plan names, limits, "coming soon" and integrations all come from
  the PR or the docs. Anything you inferred needs the owner's OK before it goes on screen.
- **Placeholder data must look like placeholder data:** `letters.yourdomain.com`, "Field Notes",
  "Maya". Never use a real person's or company's details.
- **The voice leads.** Visual beats land on the voiceover's words (±0.1 s). Measure them with
  `scripts/pauses.sh`.
- **One idea per scene,** 2–8 s each. A scene that just shows a screen needs something moving
  in it (a scroll, a push-in or a cursor).
- **End card:** the product line, the logo lockup, the URL, held for at least 2 s.

## Rendering

```bash
npx hyperframes check --json                           # fix every error
npx hyperframes snapshot --at 1.5,5,9,14 --json        # look at the frames
npx hyperframes render -q delivery -f 60 -w 2 -o renders/raw.mp4
scripts/loudness.sh renders/raw.mp4 renders/final.mp4  # −15 LUFS, −1.5 dBTP
scripts/sheet.sh renders/final.mp4 sheet.png           # 1 fps contact sheet
```

Heavy renders can run on a second machine over SSH: `scripts/hf-remote.sh` syncs the project,
runs the command there and pulls `renders/` back, with a lock so renders don't overlap.

## Files

- `references/reference-analysis.md`: studying a reference video and building the beat map
- `references/motion.md`: scene patterns with GSAP code, plus easing and timing values
- `references/audio.md`: voiceover with Kokoro, timing from pauses, music, SFX levels, mixing
- `references/review.md`: the check list, and the mistakes these videos actually made
- `scripts/`: `heat.py`, `sheet.sh`, `pauses.sh`, `vo-lines.sh`, `loudness.sh`,
  `shoot-pages.sh`, `hf-remote.sh`
- `templates/`: `index.html` and `scene.html` starting points
