# Motion analysis of a reference video: optical-flow magnitude per frame gives an energy curve,
# a cut list, per-segment spatial heatmaps and a heat-overlay video.
# usage: uv run --with opencv-python-headless --with numpy python -I heat.py <video> <outdir>
import json, os, sys, cv2, numpy as np

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = 320, 180
ok, f = cap.read()
prev = cv2.cvtColor(cv2.resize(f, (W, H)), cv2.COLOR_BGR2GRAY)
vw = cv2.VideoWriter(f"{out}/heat_overlay.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (640, 360))
rows, mags, diffs = [], [], []
while True:
    ok, f = cap.read()
    if not ok:
        break
    small = cv2.resize(f, (W, H))
    g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    diff = float(np.mean(cv2.absdiff(prev, g)))  # pixel change -> cuts/fades
    mags.append(mag); diffs.append(diff)
    m = mag > 0.5
    dx = float(flow[..., 0][m].mean()) if m.any() else 0.0
    dy = float(flow[..., 1][m].mean()) if m.any() else 0.0
    ys, xs = np.nonzero(mag > max(0.5, mag.mean() * 2))
    rows.append(dict(t=round(len(rows) / fps + 1 / fps, 3), flow=round(float(mag.mean()), 3),
                     diff=round(diff, 2), dx=round(dx, 2), dy=round(dy, 2),
                     cx=round(float(xs.mean() / W), 2) if len(xs) else None,
                     cy=round(float(ys.mean() / H), 2) if len(ys) else None))
    hm = cv2.applyColorMap(np.clip(mag * 40, 0, 255).astype(np.uint8), cv2.COLORMAP_JET)
    vw.write(cv2.resize(cv2.addWeighted(small, 0.45, hm, 0.55, 0), (640, 360)))
    prev = g
vw.release()

# cuts: pixel diff spikes well above local median
d = np.array(diffs)
med = np.median(d)
cuts = [rows[i]["t"] for i in range(len(d)) if d[i] > max(18, med * 6)]

# segments between cuts -> accumulated spatial heatmap
bounds = [0.0] + cuts + [rows[-1]["t"]]
segs = []
for a, b in zip(bounds, bounds[1:]):
    idx = [i for i, r in enumerate(rows) if a < r["t"] <= b and r["t"] not in cuts]
    if not idx:
        continue
    acc = np.sum([mags[i] for i in idx], axis=0)
    norm = (acc / (acc.max() + 1e-6) * 255).astype(np.uint8)
    cv2.imwrite(f"{out}/seg_{a:05.2f}.png", cv2.applyColorMap(cv2.resize(norm, (480, 270)), cv2.COLORMAP_INFERNO))
    fl = [rows[i]["flow"] for i in idx]
    segs.append(dict(start=a, end=b, dur=round(b - a, 2), mean_flow=round(float(np.mean(fl)), 3),
                     peak_flow=round(float(np.max(fl)), 3),
                     peak_t=rows[idx[int(np.argmax(fl))]]["t"],
                     dx=round(float(np.mean([rows[i]["dx"] for i in idx])), 2),
                     dy=round(float(np.mean([rows[i]["dy"] for i in idx])), 2)))

# whole-film heatmap
acc = np.sum(mags, axis=0)
cv2.imwrite(f"{out}/heat_total.png", cv2.applyColorMap(cv2.resize((acc / acc.max() * 255).astype(np.uint8), (640, 360)), cv2.COLORMAP_INFERNO))

# energy curve plot (flow = motion, diff = cut/fade)
Wp, Hp = 1200, 300
plot = np.full((Hp, Wp, 3), 20, np.uint8)
T = rows[-1]["t"]
fmax = max(r["flow"] for r in rows) or 1
for i in range(1, len(rows)):
    x0, x1 = int(rows[i - 1]["t"] / T * Wp), int(rows[i]["t"] / T * Wp)
    cv2.line(plot, (x0, Hp - int(rows[i - 1]["flow"] / fmax * (Hp - 20))), (x1, Hp - int(rows[i]["flow"] / fmax * (Hp - 20))), (0, 200, 255), 2)
    cv2.line(plot, (x0, Hp - int(min(diffs[i - 1], 80) / 80 * (Hp - 20))), (x1, Hp - int(min(diffs[i], 80) / 80 * (Hp - 20))), (255, 120, 60), 1)
for c in cuts:
    cv2.line(plot, (int(c / T * Wp), 0), (int(c / T * Wp), Hp), (80, 80, 255), 1)
for s in range(int(T) + 1):
    cv2.putText(plot, str(s), (int(s / T * Wp) + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
cv2.imwrite(f"{out}/energy.png", plot)

json.dump(dict(fps=fps, cuts=cuts, segments=segs, frames=rows), open(f"{out}/motion.json", "w"), indent=1)
print("cuts:", cuts)
for s in segs:
    print(s)
