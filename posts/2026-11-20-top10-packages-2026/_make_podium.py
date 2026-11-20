# Builds _podium.html, a 1600x900 pixel podium for the 2026 top 10 post.
# Render to PNG with headless Chrome:
#   chrome --headless=new --hide-scrollbars --window-size=1600,900 --virtual-time-budget=6000 \
#     --screenshot=podium-2026.png _podium.html
import math, pathlib, random

random.seed(3)
W, H = 1600, 900
BG, PANEL, BORDER, TEXT, MUTED = "#0b0d10", "#12161b", "#262c35", "#cfd5dc", "#7c8692"
MINT, AMBER, PINK, SKY, LILAC = "#6ee7a0", "#f2b84b", "#ff7eb6", "#6cc4ff", "#b69cff"
out = []


def rect(x, y, w, h, c, extra=""):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')


def text(x, y, s, cls, fill=TEXT, anchor="middle"):
    out.append(f'<text x="{x}" y="{y}" class="{cls}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


rect(0, 0, W, H, BG)
out.append('<pattern id="d" width="24" height="24" patternUnits="userSpaceOnUse">'
           '<rect width="2" height="2" fill="rgba(255,255,255,.05)"/></pattern>')
rect(0, 0, W, H, "url(#d)")

# confetti, kept away from the title, hexes and blocks
for _ in range(80):
    x, y = random.randrange(20, W - 30), random.randrange(20, H - 30)
    if 300 < x < 1300 and 40 < y < 170:
        continue
    if 260 < x < 1340 and 200 < y < H:
        continue
    s = random.choice([8, 8, 12, 16])
    rect(x // 4 * 4, y // 4 * 4, s, s, random.choice([MINT, AMBER, PINK, SKY, LILAC]),
         f'opacity="{random.choice([.5, .75, .9])}"')

text(W / 2, 120, "top 10 packages · 2026", "title", "#eef1f4")

# podium blocks: (center x, block top, place, colour, package, icon)
FLOOR = 840
podium = [
    (530, 590, 2, SKY, "ggplot2", "chart"),
    (800, 500, 1, AMBER, "torch", "flame"),
    (1070, 650, 3, PINK, "tidyverse", "hex"),
]
BW = 260


def hexagon(cx, cy, r, fill, stroke):
    pts = " ".join(f"{cx + r * math.cos(math.radians(a)):.1f},{cy + r * math.sin(math.radians(a)):.1f}"
                   for a in range(-90, 270, 60))
    out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="8" '
               f'shape-rendering="geometricPrecision"/>')


def icon(kind, cx, cy, c):
    P = 10
    if kind == "flame":
        rows = ["....X....", "...XX....", "...XXX...", "..XXXX...", "..XXXXX..", ".XXXXXXX.",
                ".XXX.XXX.", "XXX...XXX", "XXX...XXX", ".XXX.XXX.", "..XXXXX.."]
    elif kind == "chart":
        rows = [".........", ".......X.", "......XX.", ".....X.X.", "..X.X....", ".XXX.....",
                "X.X......", ".........", "XXXXXXXXX"]
    else:  # hex of little hexes = a family of packages
        rows = ["...XXX...", "..X...X..", ".X.XXX.X.", "X.X...X.X", "X.X...X.X", ".X.XXX.X.",
                "..X...X..", "...XXX..."]
    h = len(rows)
    for r, row in enumerate(rows):
        for k, ch in enumerate(row):
            if ch == "X":
                rect(cx - 4.5 * P + k * P, cy - h * P / 2 + r * P, P, P, c)


for cx, top, place, c, name, ic in podium:
    x = cx - BW / 2
    rect(x + 12, top + 12, BW, FLOOR - top, "#000", 'opacity=".55"')
    rect(x - 4, top - 4, BW + 8, FLOOR - top + 8, c)
    rect(x, top, BW, FLOOR - top, PANEL)
    text(cx, top + 120, str(place), "place", c)
    hy = top - 160
    hexagon(cx, hy, 138, PANEL, c)
    icon(ic, cx, hy - 26, c)
    text(cx, hy + 76, name, "name", "#eef1f4")

rect(160, FLOOR, W - 320, 8, BORDER)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'shape-rendering="crispEdges">{"".join(out)}</svg>')
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@600&family=Silkscreen&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:{BG}}} svg{{display:block}}
.title{{font:60px Silkscreen,monospace}} .place{{font:110px Silkscreen,monospace}}
.name{{font:600 28px 'IBM Plex Mono',monospace}}</style>
</head><body>{svg}</body></html>"""
pathlib.Path(__file__).with_name("_podium.html").write_text(page, encoding="utf-8")
