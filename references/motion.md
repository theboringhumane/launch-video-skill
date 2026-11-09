# Motion patterns

Every pattern below is seek-safe: each frame depends only on timeline time. Times are seconds from
the start of the scene. Use `fromTo` for entrances, so seeking backwards works, and add
`immediateRender: false` when an element's `from` state shouldn't apply before its tween starts.

## Timing and easing defaults

| Move | Duration | Ease |
| --- | --- | --- |
| Element enters (fade + 20–40 px rise) | 0.35–0.5 | `power3.out` |
| Element leaves | 0.25–0.3 | `power2.in` |
| Window slide / camera move | 0.55–0.7 | `power3.inOut` |
| Whip out between scenes | 0.25 | `power3.in`, with 14 px blur |
| Chip or badge pop | 0.3 | `back.out(2)` |
| Scroll a page | 1.2–1.6 | `power2.inOut` |
| Push-in on a held screen | 0.6–3 | `power2.out`, scale 1.04 → 1 |

Each scene ends with a 0.3 s exit and the next one opens with an entrance, so the hand-off reads
as one move. Don't add a crossfade on top.

## Word-by-word headline on the voice

```html
<div id="line"><span class="w">Your</span> <span class="w">newsletter</span><br />
<span class="w">just</span> <span class="w">got</span> <span class="w">a</span> <span class="w accent">home.</span></div>
```
```js
const at = [0.6, 0.85, 1.25, 1.4, 1.55, 1.65];      // from the voice's pauses
gsap.utils.toArray("#line .w").forEach((w, i) =>
  tl.fromTo(w, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, at[i]));
```
`.w { display: inline-block; opacity: 0 }`. Pair a serif display face with one italic accent word in
the brand colour.

## Typing text

Hide characters with `display: none`, **not** opacity. Hidden-by-opacity characters still take up
space, so the caret sits at the end of the finished word for the whole run.

```js
const el = document.getElementById("typed");
const chars = [...el.textContent].map((ch) => {
  const s = document.createElement("span"); s.textContent = ch; s.style.display = "none"; return s;
});
el.textContent = ""; chars.forEach((s) => el.appendChild(s));
chars.forEach((s, i) => tl.set(s, { display: "inline" }, 0.6 + i * 0.07));  // ~14 chars/s
```
Blink the caret only while the text is idle: `tl.set(caret,{opacity:0},t).set(caret,{opacity:1},t+0.25)`.

## Cursor click

An SVG arrow, moved with transforms, with a press dip and a reaction on the target:

```js
tl.fromTo("#cursor", { opacity: 1, x: 700, y: 760 }, { opacity: 1, x: 770, y: 630, duration: 0.5, ease: "power2.inOut", immediateRender: false }, 1.3);
tl.to("#cursor", { scale: 0.85, transformOrigin: "10% 8%", duration: 0.05 }, 1.88).to("#cursor", { scale: 1, duration: 0.1 }, 1.93);
tl.to("#button", { backgroundColor: "#5b3cc4", duration: 0.08 }, 1.9);
```
Put the click SFX on the press frame. The cursor's tip is at its top-left, so aim x/y a few pixels
inside the button.

## A window rises into the next scene

The outgoing scene lifts its content and slides a browser frame up. The next scene starts with
the same frame in the same place and carries on moving. Match the frame's size exactly and
show the same screenshot in both, or the hand-off pops.

```js
tl.to(["#headline", "#chip"], { y: -140, opacity: 0, duration: 0.45, ease: "power3.in" }, 3.0);
tl.to("#window", { y: -1090, duration: 0.55, ease: "power3.inOut" }, 3.05);
```

## Browser frame with a real page that scrolls

```html
<div id="win"><div id="bar">…<div id="url">xem.email/<b>field-notes</b></div></div>
  <div id="view"><img id="page" src="assets/ui/home.png" /></div></div>
```
`#view { overflow: hidden }`. Set the image's width to the frame's width and scroll it with `y`
on the beat that names what's further down: `tl.to("#page", { y: -720, duration: 1.4, ease: "power2.inOut" }, 4.45)`.
Put labels (pills) *outside* the frame, so you never need pixel positions inside a screenshot.

## Grid deal then hero flick

For "N templates/integrations/themes":

1. Deal the grid in: each tile goes from `{opacity:0, y:40, scale:0.92}` to its rest state, stagger
   0.06 s.
2. Fade the grid out, then bring in one big frame.
3. Show the items the voice names one at a time, each with a label and a small push-in (scale
   1.04 → 1, y 0 → −60).
4. Flick through the rest every 0.2 s under a single label like "and ten more". Don't give the
   flicked items their own labels: a word on screen for 0.2 s can't be read, and `check` flags it.

Toggle frames with `tl.set(el, {opacity:1}, t)`. These are hard cuts, which is what a flick should be.

## Count-up / tick

For one tick (2,480 → 2,481), stack two spans; the old one leaves upward and the new one arrives
from below:

```js
tl.to("#n1", { opacity: 0, y: -16, duration: 0.2 }, 4.2);
tl.fromTo("#n2", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 4.22);
```
Give the wrapper `position: relative; display: inline-block`, with the old span absolute, so the
text after it keeps its spacing. For a long count, tween a proxy object and write
`Math.round(v)` into the text from `onUpdate`.

## Address or value swap

Two lines stacked in a clipped box. Both move up by one line height together:
`tl.to("#u1", { y: -128, … })` and `tl.fromTo("#u2", { y: 128 }, { y: 0, … })`. Use it for
"xem.email/you → your own domain", "before → after", and plan or price swaps.

## End card

A solid brand-colour background, the product line in the display face, the logo lockup, and a
small uppercase line with the URL and plan:

```js
tl.fromTo("#root", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);
tl.fromTo("#line", { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.35);
tl.fromTo("#lockup", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 1.5);
tl.fromTo("#fine", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.75);
```
Hold the final state at least 2 s. Keep the small line at 28 px or larger.

## Things to avoid

- **Render-time motion blur** (`data-motion-blur`) on text-heavy videos: it smeared type into a
  double image during fast moves. Use a CSS `filter: blur()` tween on the one element that whips.
- **Tweening `left/top/width/height`:** use `x/y/scale`. Never tween `display` or `visibility`
  on a `.clip`.
- **Text under 28 px** that the viewer is meant to read. Small UI text inside a screenshot is fine.
- **Content sitting in the bottom 10%,** where players overlay their controls.
