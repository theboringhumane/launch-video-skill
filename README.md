# launch-video

A Claude Code skill for making short product launch videos with
[HyperFrames](https://hyperframes.heygen.com): study a reference, write a beat map, show the real
product, add a voiceover, music and sound effects, and render at 60 fps.

## Install

Copy this folder into your skills directory:

```bash
cp -r launch-video ~/.claude/skills/launch-video
```

Then ask Claude for something like "make a 30-second launch video for this PR, with a voiceover".

## Needs

Node 20+, ffmpeg, [uv](https://docs.astral.sh/uv/), and Google Chrome (only for `shoot-pages.sh`).
The HyperFrames skills (`npx hyperframes skills update`) are recommended alongside this one.

## What's inside

- `SKILL.md`: the workflow
- `references/`: reference analysis, motion patterns with code, audio and mixing, review checklist
- `scripts/`: motion heatmap, contact sheets, voice-line timing, Kokoro lines, loudness,
  page screenshots, remote render over SSH
- `templates/`: a root composition and a scene to start from

Use reference videos for pacing and structure only. Don't copy other brands' logos, UI or copy,
and only use music you have a licence for.

## License

MIT
