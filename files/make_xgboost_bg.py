"""Build files/xgboost-bg.svg: the home hero's animated background.

Re-creates xgboost_tuned.gif (gradient-boosted trees fitting a noisy sine,
one frame per boosting round) as a small, pixel-snapped SVG whose colours come
from CSS variables, so it follows the pixel theme in light and dark mode.

    python files/make_xgboost_bg.py
"""
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------- data + model
rng = np.random.default_rng(42)
N, ROUNDS, ETA, DEPTH, MIN_LEAF = 600, 30, 0.1, 3, 12
x = rng.uniform(-0.5, 0.5, N)
y = np.sin(2 * np.pi * x) + rng.normal(0, 0.3, N)


def fit_tree(x, r, depth):
    """1-D regression tree (squared error). Returns (thresholds, leaf values)."""
    def grow(idx, d):
        if d == 0 or len(idx) < 2 * MIN_LEAF:
            return [], [r[idx].mean()]
        o = idx[np.argsort(x[idx])]
        rs = r[o]
        cs, n = np.cumsum(rs), len(rs)
        k = np.arange(MIN_LEAF, n - MIN_LEAF + 1)
        gain = cs[k - 1] ** 2 / k + (cs[-1] - cs[k - 1]) ** 2 / (n - k)
        best = k[np.argmax(gain)]
        t = (x[o[best - 1]] + x[o[best]]) / 2
        lt, lv = grow(o[:best], d - 1)
        rt, rv = grow(o[best:], d - 1)
        return lt + [t] + rt, lv + rv
    return grow(np.arange(len(x)), depth)


def predict(tree, xs):
    ts, vs = tree
    return np.asarray(vs)[np.searchsorted(ts, xs)]


# ---------------------------------------------------------------- canvas (4px pixel grid)
W, H, PX = 560, 320, 4
X0, X1, Y0, Y1 = 8, W - 8, -1.75, 1.75
snap = lambda v: int(round(v / PX)) * PX
sx = lambda v: snap(X0 + (v + 0.5) * (X1 - X0))
sy = lambda v: snap(H - (v - Y0) / (Y1 - Y0) * H)

cols = np.arange(X0, X1 + 1, PX)                    # one prediction per pixel column
col_x = (cols - X0) / (X1 - X0) - 0.5

pred_pts, pred_cols = np.zeros(N), np.zeros(len(cols))
frames = []
for _ in range(ROUNDS):
    tree = fit_tree(x, y - pred_pts, DEPTH)
    pred_pts += ETA * predict(tree, x)
    pred_cols += ETA * predict(tree, col_x)
    ys = [sy(v) for v in pred_cols]
    d = [f"M{cols[0]} {ys[0]}"]
    for c, a, b in zip(cols[1:], ys, ys[1:]):
        if b != a:
            d.append(f"H{c}V{b}")
    d.append(f"H{cols[-1]}")
    frames.append("".join(d))

# points: deduplicated 4x4 pixels in one path
cells = sorted({(sx(a), sy(b)) for a, b in zip(x, y) if Y0 < b < Y1})
dots = "".join(f"M{a} {b}h{PX}v{PX}h-{PX}z" for a, b in cells)

# true function, as a dashed line
tx = np.linspace(-0.5, 0.5, 241)
truth = "M" + " L".join(f"{X0 + (a + 0.5) * (X1 - X0):.1f} {H - (np.sin(2*np.pi*a) - Y0) / (Y1 - Y0) * H:.1f}" for a in tx)

# ---------------------------------------------------------------- animation timing
STEP, HOLD = 0.2, 2.4                                # seconds per round, pause on the final fit
TOTAL = STEP * (ROUNDS - 1) + HOLD
on = STEP / TOTAL * 100
last_on = HOLD / TOTAL * 100

style = f"""
.xgb-svg{{--_dot:var(--xgb-dot,#7c8692);--_truth:var(--xgb-truth,#7c8692);--_fit:var(--xgb-fit,#6ee7a0);--_label:var(--xgb-label,#7c8692)}}
.xgb-dots{{fill:var(--_dot)}}
.xgb-truth{{fill:none;stroke:var(--_truth);stroke-width:2;stroke-dasharray:4 4}}
.xgb-f path{{fill:none;stroke:var(--_fit);stroke-width:4;stroke-linecap:square;stroke-linejoin:miter}}
.xgb-f text{{fill:var(--_label);font:12px Silkscreen,"IBM Plex Mono",monospace}}
.xgb-f{{opacity:0;animation:xgb-frame {TOTAL:.1f}s step-end infinite}}
.xgb-f:last-child{{animation-name:xgb-last}}
@keyframes xgb-frame{{0%{{opacity:1}}{on:.3f}%,100%{{opacity:0}}}}
@keyframes xgb-last{{0%{{opacity:1}}{last_on:.3f}%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.xgb-f{{animation:none}}.xgb-f:last-child{{opacity:1}}}}
"""

groups = "\n".join(
    f'<g class="xgb-f" style="animation-delay:{i * STEP:.1f}s"><path d="{d}"/>'
    f'<text x="{W - 8}" y="{H - 10}" text-anchor="end">nrounds = {i + 1:02d}</text></g>'
    for i, d in enumerate(frames)
)

svg = f"""<svg class="xgb-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMaxYMid meet" shape-rendering="crispEdges" role="img" aria-label="Gradient-boosted trees fitting a noisy sine curve, one boosting round at a time">
<style>{style.strip()}</style>
<path class="xgb-dots" d="{dots}"/>
<path class="xgb-truth" shape-rendering="geometricPrecision" d="{truth}"/>
{groups}
</svg>
"""

out = Path(__file__).with_name("xgboost-bg.svg")
out.write_text(svg, encoding="utf-8")
# Markdown wrapper so index.qmd can inline it (CSS variables only reach inline SVG):
#   {{< include files/_xgboost-bg.md >}}
out.with_name("_xgboost-bg.md").write_text(
    f'```{{=html}}\n<div class="xgb-bg" aria-hidden="true">\n{svg}</div>\n```\n', encoding="utf-8")
print(f"{out}  {len(svg) / 1024:.1f} KiB, {len(cells)} pixels, {ROUNDS} frames, {TOTAL:.1f}s loop")
