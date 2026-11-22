# Builds _thumb.html, a 1600x900 "code to DAG" thumbnail for the targetfy post.
# The graph is the real tar_glimpse() output, _glimpse-dark.png, made with _glimpse.R.
# Render to PNG with headless Chrome:
#   chrome --headless=new --hide-scrollbars --window-size=1600,900 --virtual-time-budget=6000 \
#     --screenshot=targetfy.png _thumb.html
import base64, html, pathlib

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



def panel(x, y, w, h, label, accent):
    rect(x + 10, y + 10, w, h, "#000", 'opacity=".55"')
    rect(x - 4, y - 4, w + 8, h + 8, accent)
    rect(x, y, w, h, PANEL)
    rect(x, y, w, 50, BAR)
    for i, c in enumerate([PINK, AMBER, MINT]):
        rect(x + 20 + i * 24, y + 19, 12, 12, c)
    text(x + 104, y + 33, label, "lbl", MUTED)


# left: the script
PX, PY, PW, PH = 80, 50, 820, 525
panel(PX, PY, PW, PH, "analysis.R", SKY)
lines = [
    ("rm(list = ls())", MUTED, True),
    ("library(stats)", TEXT, False),
    ("df <- read.csv(\"data/sales.csv\")", SKY, False),
    ("df <- df[df$year > 2020, ]", MINT, False),
    ("df$rev <- log(df$rev)", MINT, False),
    ("model <- lm(rev ~ region, df)", AMBER, False),
    ("print(summary(model))", MUTED, True),
    ("model_summary <- summary(model)$coef", LILAC, False),
    ("write.csv(model_summary, \"out/coefs.csv\")", PINK, False),
]
for i, (s, c, strike) in enumerate(lines):
    y = PY + 100 + i * 48
    text(PX + 30, y, f"{i + 1}", "code", BORDER)
    text(PX + 70, y, s, "code strike" if strike else "code", c)

# right: title and a pixel arrow down to the graph
TX = 1215
text(TX, 250, "targetfy", "title", HEAD, "middle")
text(TX, 310, "R scripts in,", "sub", MUTED, "middle")
text(TX, 348, "{targets} pipeline out", "sub", MUTED, "middle")
c = 8
for i in range(8):
    rect(TX - c, 420 + i * c, 2 * c, c, MUTED)
for k, cols in enumerate([range(-4, 4), range(-3, 3), range(-2, 2), range(-1, 1)]):
    for r in cols:
        rect(TX + r * c, 484 + k * c, c, c, MUTED)

# bottom: the real tar_glimpse() of the pipeline (see _glimpse.R)
GX, GY, GW, GH = 80, 625, 1440, 230
panel(GX, GY, GW, GH, "tar_glimpse()", MINT)
img = base64.b64encode(pathlib.Path(__file__).with_name("_glimpse-dark.png").read_bytes()).decode()
iw = 1150; ih = iw * 261 / 1787
out.append(f'<image x="{GX + (GW - iw) / 2}" y="{GY + 50 + (GH - 50 - ih) / 2}" width="{iw}" height="{ih}" '
           f'href="data:image/png;base64,{img}"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'shape-rendering="crispEdges">{"".join(out)}</svg>')
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Silkscreen&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:{BG}}} svg{{display:block}}
.title{{font:72px Silkscreen,monospace}} .sub{{font:500 26px 'IBM Plex Mono',monospace}}
.lbl{{font:600 20px 'IBM Plex Mono',monospace}} .code{{font:500 22px 'IBM Plex Mono',monospace}}
.node{{font:600 20px 'IBM Plex Mono',monospace}} .strike{{text-decoration:line-through}}</style>
</head><body>{svg}</body></html>"""
pathlib.Path(__file__).with_name("_thumb.html").write_text(page, encoding="utf-8")
