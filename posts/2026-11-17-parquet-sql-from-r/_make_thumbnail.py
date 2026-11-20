# Builds thumb.html: 1600x900 thumbnail for the parquet-sql-from-r post.
import random, html, pathlib
random.seed(7)
W, H = 1600, 900
BG, PANEL, BORDER, TEXT, MUTED = "#0b0d10", "#12161b", "#262c35", "#cfd5dc", "#7c8692"
MINT, AMBER, PINK, SKY, LILAC = "#6ee7a0", "#f2b84b", "#ff7eb6", "#6cc4ff", "#b69cff"
out = []
R = lambda x, y, w, h, c, extra="": out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>')

# background + dot grid
R(0, 0, W, H, BG)
out.append('<pattern id="d" width="24" height="24" patternUnits="userSpaceOnUse"><rect x="0" y="0" width="2" height="2" fill="rgba(255,255,255,.05)"/></pattern>')
R(0, 0, W, H, "url(#d)")

# confetti (kept out of the panels and title)
cols = [MINT, AMBER, PINK, SKY, LILAC]
for _ in range(95):
    x, y = random.randrange(20, W - 30), random.randrange(20, H - 30)
    in_panel = (60 < x < 660 or 940 < x < 1540) and 230 < y < 690
    in_title = 380 < x < 1220 and 60 < y < 200
    in_duck = 650 < x < 960 and 290 < y < 690
    if in_panel or in_title or in_duck: continue
    s = random.choice([8, 8, 12, 12, 16])
    R(x // 4 * 4, y // 4 * 4, s, s, random.choice(cols), f'opacity="{random.choice([.55, .75, .9])}"')

def sparkle(cx, cy, c, p=8):
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]:
        R(cx + dx * p, cy + dy * p, p, p, c)
for cx, cy, c in [(700, 250, AMBER), (905, 215, PINK), (640, 760, SKY), (960, 740, MINT), (300, 780, LILAC), (1300, 790, AMBER), (210, 140, PINK), (1390, 150, SKY)]:
    sparkle(cx, cy, c)

# panels: pixel ring (2px) + hard shadow, terminal title bar
def panel(x, y, w, h, label, accent):
    R(x + 10, y + 10, w, h, "#000", 'opacity=".55"')
    R(x - 4, y - 4, w + 8, h + 8, accent)
    R(x, y, w, h, PANEL)
    R(x, y, w, 52, "#10141a")
    for i, c in enumerate([PINK, AMBER, MINT]):
        R(x + 22 + i * 26, y + 18, 16, 16, c)
    out.append(f'<text x="{x + w - 24}" y="{y + 35}" text-anchor="end" class="lbl" fill="{MUTED}">{label}</text>')

def code(x, y, lines):
    for i, segs in enumerate(lines):
        spans = "".join(f'<tspan fill="{c}">{html.escape(t)}</tspan>' for t, c in segs)
        out.append(f'<text x="{x}" y="{y + i * 46}" class="code" xml:space="preserve">{spans}</text>')

panel(70, 250, 570, 430, "R · dplyr", MINT)
code(102, 350, [
    [("tx ", TEXT), ("|>", PINK)],
    [("  group_by", MINT), ("(month) ", TEXT), ("|>", PINK)],
    [("  summarise", MINT), ("(", TEXT)],
    [("    n_tx = ", TEXT), ("n", MINT), ("(),", TEXT)],
    [("    revenue = ", TEXT), ("sum", MINT), ("(amount)", TEXT)],
    [("  )", TEXT)],
])
panel(960, 250, 570, 430, "SQL", AMBER)
code(992, 350, [
    [("SELECT ", AMBER), ("month,", TEXT)],
    [("  COUNT", AMBER), ("(*) ", TEXT), ("AS ", AMBER), ("n_tx,", TEXT)],
    [("  SUM", AMBER), ("(amount) ", TEXT), ("AS ", AMBER), ("revenue", TEXT)],
    [("FROM ", AMBER), ("tx", TEXT)],
    [("GROUP BY ", AMBER), ("month", TEXT)],
])

# rainbow pixel arrow between the panels
P = 16
ax0, ay = 664, 584
rain = [MINT, SKY, LILAC, PINK, AMBER]
n = 14
for i in range(n):
    R(ax0 + i * P, ay, P, P, rain[i * len(rain) // n])
    R(ax0 + i * P, ay + P, P, P, rain[i * len(rain) // n])
hx = ax0 + n * P
for k, (rows) in enumerate([range(-2, 4), range(-1, 3), range(0, 2)]):
    for r in rows:
        R(hx + k * P, ay + r * P, P, P, AMBER)
out.append(f'<text x="{ax0 + (n * P) // 2 + 20}" y="{ay + 82}" text-anchor="middle" class="qry" fill="{MUTED}">show_query()</text>')

# happy pixel duck riding the arrow
duck = [
    "......YYYY......",
    ".....YYYYYY.....",
    ".....YYKYYYY....",
    ".....YPYYYYOOO..",
    ".....YYYYYYOOOO.",
    "......YYYYYOO...",
    ".......YYYY.....",
    ".YY...YYYYYY....",
    ".YYYYYYYYYYYY...",
    ".YYYYYDDDDYYYY..",
    "..YYYYYDDDYYYY..",
    "..YYYYYYYYYYY...",
    "....YYYYYYYYY...",
    ".....OO...OO....",
]
pal = {"Y": "#ffd84d", "O": "#ff9f43", "K": "#0b0d10", "P": PINK, "D": "#f2b84b"}
c = 12
dx, dy = 800 - 8 * c, ay - len(duck) * c
for r, row in enumerate(duck):
    for col, ch in enumerate(row):
        if ch in pal:
            R(dx + col * c, dy + r * c, c, c, pal[ch])
# little music notes = joy
for nx, ny, col in [(905, 330, PINK), (690, 345, SKY)]:
    R(nx, ny, 8, 36, col); R(nx - 16, ny + 28, 20, 16, col); R(nx + 8, ny, 16, 8, col)

# title
out.append(f'<text x="800" y="160" text-anchor="middle" class="title"><tspan fill="{MINT}">dplyr</tspan><tspan fill="{TEXT}"> → </tspan><tspan fill="{AMBER}">SQL</tspan></text>')

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">{"".join(out)}</svg>'
page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Silkscreen&display=block" rel="stylesheet">
<style>html,body{{margin:0;background:{BG}}} svg{{display:block}}
.code{{font:500 31px 'IBM Plex Mono',Consolas,monospace}} .lbl{{font:22px Silkscreen,monospace;letter-spacing:.04em}}
.qry{{font:500 24px 'IBM Plex Mono',Consolas,monospace}} .title{{font:76px Silkscreen,monospace}}</style></head><body>{svg}</body></html>"""
pathlib.Path(__file__).with_name("thumb.html").write_text(page, encoding="utf-8")
