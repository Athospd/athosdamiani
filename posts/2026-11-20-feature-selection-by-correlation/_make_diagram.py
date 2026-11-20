# Builds _diagram.html, a 1600x900 diagram of the random probe strategy.
# Render to PNG with headless Chrome:
#   chrome --headless=new --window-size=1600,900 --virtual-time-budget=5000 \
#     --screenshot=random-probes.png _diagram.html
import html, pathlib

W, H = 1600, 900
BG, PANEL, BAR, BORDER = "#0b0d10", "#12161b", "#10141a", "#262c35"
TEXT, HEAD, MUTED = "#cfd5dc", "#eef1f4", "#7c8692"
MINT, AMBER, PINK = "#6ee7a0", "#f2b84b", "#ff7eb6"
out = []


def rect(x, y, w, h, c, extra=""):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')


def text(x, y, s, cls, fill=TEXT, anchor="start"):
    out.append(f'<text x="{x}" y="{y}" class="{cls}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>')


# background + dot grid
rect(0, 0, W, H, BG)
out.append('<pattern id="d" width="24" height="24" patternUnits="userSpaceOnUse">'
           '<rect width="2" height="2" fill="rgba(255,255,255,.05)"/></pattern>')
rect(0, 0, W, H, "url(#d)")

text(W / 2, 92, "feature selection with random probes", "title", HEAD, "middle")
text(W / 2, 140, "keep a feature only if the model finds it more useful than pure noise", "sub", MUTED, "middle")

PW, PH, PY = 335, 600, 210
XS = [60, 445, 830, 1215]


def panel(x, n, label, accent):
    rect(x + 10, PY + 10, PW, PH, "#000", 'opacity=".55"')
    rect(x - 4, PY - 4, PW + 8, PH + 8, accent)
    rect(x, PY, PW, PH, PANEL)
    rect(x, PY, PW, 56, BAR)
    rect(x + 20, PY + 16, 24, 24, accent)
    text(x + 32, PY + 35, str(n), "num", BG, "middle")
    text(x + 60, PY + 37, label, "lbl", HEAD)


def arrow(x):
    y = PY + PH / 2
    c = 5
    for i in range(3):
        rect(x + i * c, y - c, c, 2 * c, MUTED)
    for k, rows in enumerate([range(-3, 3), range(-2, 2), range(-1, 1)]):
        for r in rows:
            rect(x + 3 * c + k * c, y + r * c, c, c, MUTED)


feats = ["x1", "x2", "x3", "x4"]
probes = ["random1", "random2", "random3"]

# 1. add probes
x = XS[0]
panel(x, 1, "add random probes", MINT)
y0 = PY + 110
for i, f in enumerate(feats):
    rect(x + 30, y0 + i * 52, PW - 60, 40, BG, f'stroke="{BORDER}" stroke-width="2"')
    text(x + 50, y0 + i * 52 + 28, f, "code", TEXT)
for j, f in enumerate(probes):
    yy = y0 + (len(feats) + j) * 52 + 14
    rect(x + 30, yy, PW - 60, 40, BG, f'stroke="{AMBER}" stroke-width="2" stroke-dasharray="6 5"')
    text(x + 50, yy + 28, f, "code", AMBER)
text(x + PW / 2, PY + PH - 70, "probes = pure noise:", "note", MUTED, "middle")
text(x + PW / 2, PY + PH - 34, "runif() or shuffled copies", "note", MUTED, "middle")

# 2. fit a tree model (pixel tree)
x = XS[1]
panel(x, 2, "fit a tree model", MINT)
P = 14
cx, ty = x + PW / 2, PY + 150
def node(px, py, c):
    rect(px - 2 * P, py, 4 * P, 2 * P, c)
node(cx, ty, MINT)
for dx, dy in [(-1, 2), (-2, 3), (-3, 4), (1, 2), (2, 3), (3, 4)]:
    rect(cx + dx * P - P / 2, ty + dy * P, P, P, MUTED)
lx, rx, ly = cx - 3 * P - P / 2, cx + 3 * P + P / 2, ty + 5 * P
node(lx, ly, MINT)
node(rx, ly, MINT)
for base in (lx, rx):
    for dx, dy in [(-1, 2), (-2, 3), (1, 2), (2, 3)]:
        rect(base + dx * P - P / 2, ly + dy * P, P, P, MUTED)
    for sx in (-2, 2):
        rect(base + sx * P - P, ly + 4 * P, 2 * P, 2 * P, AMBER if (base == rx and sx == 2) else TEXT)
for i, s in enumerate(["random forest,", "LightGBM, xgboost..."]):
    text(cx, PY + 440 + i * 36, s, "code", TEXT, "middle")
text(cx, PY + PH - 70, "trees find interactions", "note", MUTED, "middle")
text(cx, PY + PH - 34, "such as ratios for you", "note", MUTED, "middle")

# 3. rank by importance
x = XS[2]
panel(x, 3, "rank by importance", MINT)
imp = [("x1", .95, MINT), ("x2", .70, MINT), ("x3", .38, MINT),
       ("random2", .12, AMBER), ("x4", .08, MUTED), ("random1", .06, AMBER), ("random3", .04, AMBER)]
bx, bw, by = x + 130, PW - 160, PY + 100
for i, (f, v, c) in enumerate(imp):
    yy = by + i * 56
    text(bx - 12, yy + 27, f, "code", AMBER if c == AMBER else TEXT, "end")
    rect(bx, yy + 8, max(8, int(bw * v)), 26, c)
thr = bx + bw * .12
out.append(f'<line x1="{thr}" y1="{by - 10}" x2="{thr}" y2="{by + 7 * 56}" stroke="{PINK}" stroke-width="3" stroke-dasharray="8 6"/>')
text(x + PW / 2, PY + PH - 70, "threshold = best probe", "note", PINK, "middle")
text(x + PW / 2, PY + PH - 34, "(or mean, or mean + 3 sd)", "note", MUTED, "middle")

# 4. keep / drop
x = XS[3]
panel(x, 4, "keep or drop", MINT)
text(x + 30, PY + 115, "keep: above the line", "lbl2", MINT)
for i, f in enumerate(["x1", "x2", "x3"]):
    rect(x + 30, PY + 135 + i * 52, PW - 60, 40, BG, f'stroke="{MINT}" stroke-width="2"')
    text(x + 50, PY + 163 + i * 52, f, "code", TEXT)
text(x + 30, PY + 330, "drop: below the line", "lbl2", PINK)
for i, f in enumerate(["x4", "random1..3"]):
    rect(x + 30, PY + 350 + i * 52, PW - 60, 40, BG, f'stroke="{BORDER}" stroke-width="2"')
    text(x + 50, PY + 378 + i * 52, f, "code strike", MUTED)
text(x + PW / 2, PY + PH - 106, "repeat over resamples:", "note", MUTED, "middle")
text(x + PW / 2, PY + PH - 70, "{Boruta} (R) or", "note", MUTED, "middle")
text(x + PW / 2, PY + PH - 34, "ProbeFeatureSelection (py)", "note", MUTED, "middle")

for a in (XS[0] + PW + 10, XS[1] + PW + 10, XS[2] + PW + 10):
    arrow(a)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'shape-rendering="crispEdges">{"".join(out)}</svg>')
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Silkscreen&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:{BG}}} svg{{display:block}}
.title{{font:44px Silkscreen,monospace}} .sub{{font:500 24px 'IBM Plex Mono',monospace}}
.lbl{{font:600 22px 'IBM Plex Mono',monospace}} .lbl2{{font:600 21px 'IBM Plex Mono',monospace}}
.num{{font:600 18px 'IBM Plex Mono',monospace}} .code{{font:500 22px 'IBM Plex Mono',monospace}}
.note{{font:500 18px 'IBM Plex Mono',monospace}} .strike{{text-decoration:line-through}}</style>
</head><body>{svg}</body></html>"""
pathlib.Path(__file__).with_name("_diagram.html").write_text(page, encoding="utf-8")
