# Builds _thumb.html, a 1600x900 "code to DAG" thumbnail for the targetfy post.
# Render to PNG with headless Chrome:
#   chrome --headless=new --hide-scrollbars --window-size=1600,900 --virtual-time-budget=6000 \
#     --screenshot=targetfy.png _thumb.html
import html, pathlib

W, H = 1600, 900
BG, PANEL, BAR, BORDER = "#0b0d10", "#12161b", "#10141a", "#262c35"
TEXT, HEAD, MUTED = "#cfd5dc", "#eef1f4", "#7c8692"
MINT, AMBER, PINK, SKY, LILAC = "#6ee7a0", "#f2b84b", "#ff7eb6", "#6cc4ff", "#b69cff"
out = []


def rect(x, y, w, h, c, extra=""):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')


def text(x, y, s, cls, fill=TEXT, anchor="start"):
    out.append(f'<text x="{x}" y="{y}" class="{cls}" fill="{fill}" text-anchor="{anchor}">{html.escape(s)}</text>')


rect(0, 0, W, H, BG)
out.append('<pattern id="d" width="24" height="24" patternUnits="userSpaceOnUse">'
           '<rect width="2" height="2" fill="rgba(255,255,255,.05)"/></pattern>')
rect(0, 0, W, H, "url(#d)")

text(W / 2, 110, "targetfy", "title", HEAD, "middle")
text(W / 2, 160, "R scripts in, {targets} pipeline out", "sub", MUTED, "middle")


def panel(x, y, w, h, label, accent):
    rect(x + 10, y + 10, w, h, "#000", 'opacity=".55"')
    rect(x - 4, y - 4, w + 8, h + 8, accent)
    rect(x, y, w, h, PANEL)
    rect(x, y, w, 50, BAR)
    for i, c in enumerate([PINK, AMBER, MINT]):
        rect(x + 20 + i * 24, y + 19, 12, 12, c)
    text(x + 104, y + 33, label, "lbl", MUTED)


# left: the script
PX, PY, PW, PH = 80, 230, 620, 590
panel(PX, PY, PW, PH, "analysis.R", SKY)
lines = [
    ("rm(list = ls())", MUTED, True),
    ("library(stats)", TEXT, False),
    ("df <- read.csv(\"sales.csv\")", SKY, False),
    ("df <- df[df$year > 2020, ]", MINT, False),
    ("df$rev <- log(df$rev)", MINT, False),
    ("model <- lm(rev ~ region, df)", AMBER, False),
    ("print(summary(model))", MUTED, True),
    ("coefs <- summary(model)$coef", LILAC, False),
    ("write.csv(coefs, \"coefs.csv\")", PINK, False),
]
for i, (s, c, strike) in enumerate(lines):
    y = PY + 110 + i * 54
    text(PX + 30, y, f"{i + 1}", "code", BORDER)
    text(PX + 70, y, s, "code strike" if strike else "code", c)

# arrow
ax, ay, c = 735, PY + PH / 2, 8
for i in range(6):
    rect(ax + i * c, ay - c, c, 2 * c, MUTED)
for k, rows in enumerate([range(-4, 4), range(-3, 3), range(-2, 2), range(-1, 1)]):
    for r in rows:
        rect(ax + 6 * c + k * c, ay + r * c, c, c, MUTED)

# right: the DAG
DX, DW = 860, 660
panel(DX, PY, DW, PH, "tar_glimpse()", MINT)
nodes = [
    ("sales_file", SKY), ("sales", SKY), ("sales_clean", MINT),
    ("model", AMBER), ("model_summary", LILAC), ("coefs_file", PINK),
]
NW, NH = 250, 50
pos = []
for i in range(len(nodes)):
    col = i % 2
    row = i // 2 * 2 + col
    pos.append((DX + 50 + col * 310, PY + 85 + i * 82))
# connectors (pixel elbows)
for (x1, y1), (x2, y2) in zip(pos, pos[1:]):
    sx, sy = x1 + NW / 2, y1 + NH
    ex, ey = x2 + NW / 2, y2
    midy = (sy + ey) / 2
    rect(sx - 3, sy, 6, midy - sy, MUTED)
    rect(min(sx, ex) - 3, midy - 3, abs(ex - sx) + 6, 6, MUTED)
    rect(ex - 3, midy, 6, ey - midy - 6, MUTED)
    for k, w in enumerate([18, 12, 6]):
        rect(ex - w / 2, ey - 10 + k * 3, w, 3, MUTED)
for (x, y), (name, col) in zip(pos, nodes):
    rect(x + 6, y + 6, NW, NH, "#000", 'opacity=".5"')
    rect(x, y, NW, NH, BG, f'stroke="{col}" stroke-width="3"')
    rect(x + 14, y + 19, 12, 12, col)
    text(x + 40, y + 33, name, "node", HEAD)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'shape-rendering="crispEdges">{"".join(out)}</svg>')
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Silkscreen&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:{BG}}} svg{{display:block}}
.title{{font:64px Silkscreen,monospace}} .sub{{font:500 26px 'IBM Plex Mono',monospace}}
.lbl{{font:600 20px 'IBM Plex Mono',monospace}} .code{{font:500 23px 'IBM Plex Mono',monospace}}
.node{{font:600 20px 'IBM Plex Mono',monospace}} .strike{{text-decoration:line-through}}</style>
</head><body>{svg}</body></html>"""
pathlib.Path(__file__).with_name("_thumb.html").write_text(page, encoding="utf-8")
