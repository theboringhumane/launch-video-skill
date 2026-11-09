# Sound: voiceover, music, effects, mix

A launch video has up to three layers. The voice sits on top and stays clear. Music sits under it
at about a fifth of its level. Effects only mark things you can see happen: a click, a pop, a whoosh
on a whip, typing while text types.

## Voiceover with Kokoro (free, local)

Kokoro-82M runs on the CPU. The HyperFrames CLI wraps it:

```bash
uv venv -p 3.12 .kokoro && uv pip install -p .kokoro/bin/python kokoro-onnx soundfile
export HYPERFRAMES_PYTHON=$PWD/.kokoro/bin/python
npx hyperframes tts "Your newsletter just got a home on the web." -v af_heart -o assets/vo/l1.wav
```

Voices: `af_heart` (warm, the best all-rounder), `af_nova`, `af_sky`, `am_adam`, `am_michael`,
`bf_emma`, `bm_george`. `-s 1.05` speeds a voice up a little if it drags.

**One file per line, one line per beat.** `scripts/vo-lines.sh script.txt assets/vo af_heart` reads
one line per row and prints each line's duration. Separate files let you place each line exactly
and change one line without touching the rest.

### Writing for the voice

- About 2.5 words per second. A 35 s video holds about 80 words with breathing room.
- Short sentences, said the way a person says them: "Publish at xem dot email, slash your name."
  Write URLs and symbols the way you'd say them out loud.
- List items with full stops ("Paper. Midnight. Bento.") give Kokoro a pause after each, which
  gives you a beat to cut on.
- The first line is the hook (under 3 s). The last line is the product name.

### Timing visuals to words

Kokoro doesn't return word timings, but the pauses are clean, so measure them:

```bash
scripts/pauses.sh assets/vo/l3.wav
# silence 1.49–1.92 | 2.91–3.19 | 4.35–4.65
```

Each pause sits between phrases. "Pick from fourteen templates. | Paper. Midnight. | Bento.
Terminal. | Each with a layout of its own." means "Paper" starts at 1.92, so add the line's
`data-start` and put the cut there. Need every word? `npx hyperframes transcribe` gives word
timestamps.

Place lines in the root with a little air: about 0.3 s after a scene starts and 0.4 s before it
ends.

```html
<audio id="vo3" src="assets/vo/l3.wav" data-start="11.9" data-duration="6.12" data-track-index="2" data-volume="1"></audio>
```

## Music bed

- Use a track you made, licensed, or took from a royalty-free library. A reference video's
  soundtrack is allowed only if its owner licensed it to you.
- Pull audio out of a reference you hold rights to: `ffmpeg -i ref.mp4 -vn -c:a copy assets/bgm/track.m4a`.
- **Under a voice:** `data-volume="0.18"`–`0.22`, `data-fade-in="0.4"`, `data-fade-out="2"`.
- **No voice:** the music carries the video at full level, and hits land on its beats
  (`npx hyperframes beats assets/bgm/track.m4a`).
- If the track is shorter than the video, end the video when the music ends, or let the end card
  hold over the fade. Never loop a bar you can hear repeating.

## Effects

Keep effects about 25% quieter than you first think. They should be felt, not noticed.

| Effect | When | Volume |
| --- | --- | --- |
| whoosh-short | a whip, a slide-out, a window rising | 0.3–0.35 |
| click-soft | the frame where the cursor presses | 0.5 |
| pop | a chip or badge appears, a count ticks | 0.4 |
| typing | while characters appear, trimmed to the typing length | 0.3 |
| impact / riser | the logo landing, once per video at most | 0.4 |

Set `data-duration` to the clip's real length or shorter; `check` warns when a slot runs longer
than the media. Line effects up with the frame of the action. Two frames late reads as lag.

## Mix and loudness

Aim for **−15 LUFS integrated, true peak −1.5 dBTP**, which suits social and web players. Render,
then normalise without touching the picture:

```bash
scripts/loudness.sh renders/raw.mp4 renders/final.mp4
```

Check it: `ffmpeg -i final.mp4 -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:"`.

A video with effects only lands near −25 LUFS. That's fine for a silent-autoplay feed. Raise it
with the same script if it plays next to louder videos.
