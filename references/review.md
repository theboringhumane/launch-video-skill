# Review before you send

## Every time

1. `npx hyperframes check --json`: zero errors. Read each warning and fix it or accept it on
   purpose (small UI text inside a screenshot is fine; an unreadable headline isn't).
2. Snapshot every beat: `npx hyperframes snapshot --at <one time per beat> --json`, then open
   the contact sheet it writes and look at it.
3. Render, then normalise loudness (`scripts/loudness.sh`).
4. Make a 1 fps sheet **of the final MP4** (`scripts/sheet.sh final.mp4 sheet.png`) and look at
   every tile. A render can differ from a snapshot: fonts load late, a media frame is missing.
5. Run `ffprobe` on the file: 1920×1080, 60/1, an audio stream, and the duration you expect.
6. Measure loudness: about −15 LUFS, peak at or below −1 dBTP.

## Ask the owner before sending

- Every claim on screen or in the voice: plan names, "coming soon", integrations, numbers.
- Anything that depends on setup not yet done, like custom domains that need DNS or a CDN step.
- Music you didn't make: confirm the licence.

## Mistakes these videos actually made

| What happened | Cause | Fix |
| --- | --- | --- |
| Text smeared into a double image for 3 s | render-time motion blur on the root | remove `data-motion-blur`; blur only the element that whips |
| Typing caret stuck at the end of the word | characters hidden with opacity still take space | hide with `display: none` |
| "2,480READERS": the space vanished | the absolutely positioned old number gave its wrapper no width | wrapper `position: relative; display: inline-block` |
| A blank white box for 0.4 s between scenes | the rising window in scene A was empty; scene B's had the page | put the same screenshot and size in both |
| Ten flicked labels flagged unreadable | 0.2 s per label | one shared label ("and ten more") |
| Someone saw another brand's name "in the video" | it was the reference half of a side-by-side sheet | review your own frames on their own |
| Voice too quiet next to other videos (−19.5 LUFS) | mixed by ear | normalise to −15 after rendering |
| Music ran out before the end | the bed was 20 s, the video 35 s | pick a bed at least as long as the video, or cut the video to the music |

## Shell gotchas (zsh)

- `"$sha:client/…"` breaks, because `:c` is a zsh modifier. Write `"${sha}:client/…"`.
- `set -- $var` doesn't split words in zsh. Pass arguments directly, or use `${=var}`.
- Seeking with `ffmpeg -ss .72` fails when `bc` prints a leading dot. Use `printf "%.3f"`.
