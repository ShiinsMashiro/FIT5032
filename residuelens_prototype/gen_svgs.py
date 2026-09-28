#!/usr/bin/env python3
"""Regenerate the five ResidueLens Figma-prototype SVG screens 1:1 against
Litmus-Mobile source AND a verified runtime render of the real app
(RN-web export against the local Postgres Gold API).

Canvas 390x844 (iPhone 14 logical points). Sans = Inter (Figma default),
mono = Roboto Mono (closest Figma-safe stand-in for Menlo)."""

import json, os

OUT = os.path.join(os.path.dirname(__file__), "figma_prototypes")
os.makedirs(OUT, exist_ok=True)

GLYPHS = json.load(open("/home/ubuntu/glyphs.json"))

# ---- theme.js ----
PAPER   = "#FBFAF7"
SURFACE = "#FFFFFF"
LINE    = "#E2E0D8"
INK     = "#1C1C1A"
MUTED   = "#5F5E5A"
SUBTLE  = "#8A8880"
N100    = "#EFEEE9"
N300    = "#CFCCC1"
N400    = "#A8A69C"
N600    = "#6E6D67"
N800    = "#3A3936"
ACCENT      = "#0F6E56"
ACCENT_TINT = "#E1F5EE"
ACCENT_INK  = "#085041"
ACCENT_MID  = "#1D9E75"
ACCENT_SOFT = "#5DCAA5"
HEADER_INK   = "#12211D"
ON_HEADER    = "#FFFFFF"
ON_HEADER_MUT= "#7FA396"
ARTWORK_LINE = "#2E5346"

SANS = "Inter, -apple-system, 'Segoe UI', Roboto, sans-serif"
MONO = "'Roboto Mono', Menlo, monospace"

W, H = 390, 844

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

class SVG:
    def __init__(self):
        self.parts = []
    def add(self, s): self.parts.append(s)
    def rect(self, x, y, w, h, fill="none", rx=0, stroke=None, sw=1, opacity=None):
        a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
        if rx: a += f' rx="{rx}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        if opacity is not None: a += f' opacity="{opacity}"'
        self.add(a + "/>")
    def line(self, x1, y1, x2, y2, stroke, sw=1):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>')
    def hairline(self, x, y, w, color=LINE):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="0.5" fill="{color}"/>')
    def circle(self, cx, cy, r, fill="none", stroke=None, sw=1, opacity=None):
        a = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
        if stroke: a += f' stroke="{stroke}" stroke-width="{sw}"'
        if opacity is not None: a += f' opacity="{opacity}"'
        self.add(a + "/>")
    def text(self, x, y, s, size, fill=INK, weight=400, ls=None, mono=False,
             anchor="start", transform=None, opacity=None, style=None):
        fam = MONO if mono else SANS
        a = (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
             f'fill="{fill}" font-weight="{weight}"')
        if ls is not None: a += f' letter-spacing="{ls}"'
        if anchor != "start": a += f' text-anchor="{anchor}"'
        if transform: a += f' transform="{transform}"'
        if opacity is not None: a += f' opacity="{opacity}"'
        if style: a += f' style="{style}"'
        self.add(a + f'>{esc(s)}</text>')
    def path(self, d, stroke, sw, fill="none", opacity=None, cap="round"):
        a = f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"'
        if opacity is not None: a += f' opacity="{opacity}"'
        self.add(a + "/>")
    def glyph(self, key, x, y, size):
        """Real Noto/derived produce glyph, 128 box scaled to size."""
        g = GLYPHS[key]
        s = size / g["w"]
        self.add(f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.4f})">{g["body"]}</g>')
    def raw(self, s): self.add(s)
    def clip_open(self, cid, w=W, h=H, y0=0):
        self.add(f'<clipPath id="{cid}"><rect x="0" y="{y0}" width="{w}" height="{h}"/></clipPath>')
    def out(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="390" height="844" '
                'viewBox="0 0 390 844" font-family="' + SANS + '">'
                + "".join(self.parts) + "</svg>")

# ---------- shared chrome ----------

def status_bar(svg, dark=True):
    ink = ON_HEADER if dark else INK
    svg.text(28, 26, "10:24", 15, ink, 600)
    y = 25
    for i, hh in enumerate([5, 7, 9, 11]):
        svg.rect(306 + i * 4, y - hh + 3, 3, hh, ink, rx=0.8)
    svg.path("M335 19 c3 -3 7 -3 10 0 M337 22 c2 -2 4 -2 6 0 M340.5 25 a1.6 1.6 0 1 0 0.01 0",
             ink, 1.6)
    svg.rect(356, 14.5, 22, 11, "none", rx=3, stroke=ink, sw=1, opacity=0.45)
    svg.rect(358, 16.5, 15, 7, ink, rx=1.5)
    svg.rect(379.5, 17.5, 1.6, 5, ink, rx=0.8, opacity=0.45)

def feather(svg, name, cx, cy, size, color):
    u = size / 24.0
    def P(d, sw=2):
        svg.add(f'<g transform="translate({cx-size/2},{cy-size/2}) scale({u})">'
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    if name == "home":
        P("M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"); P("M9 22V12h6v10")
    elif name == "shopping-bag":
        P("M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"); P("M3 6h18"); P("M16 10a4 4 0 0 1-8 0")
    elif name == "book-open":
        P("M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"); P("M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z")
    elif name == "search":
        svg.circle(cx - 1 * u, cy - 1 * u, 7 * u, "none", color, 2 * u)
        svg.line(cx + 4.9 * u, cy + 4.9 * u, cx + 8.2 * u, cy + 8.2 * u, color, 2 * u)
    elif name == "camera":
        P("M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z")
        svg.circle(cx, cy - 1 * u, 3.4 * u, "none", color, 2 * u)
    elif name == "hash":
        P("M4 9h16"); P("M4 15h16"); P("M10 3L8 21"); P("M16 3l-2 18")
    elif name == "list":
        P("M8 6h13"); P("M8 12h13"); P("M8 18h13")
        P("M3.5 6h0.01", 3.4); P("M3.5 12h0.01", 3.4); P("M3.5 18h0.01", 3.4)
    elif name == "chevron-right":
        P("M9 18l6-6-6-6")
    elif name == "chevron-left":
        P("M15 18l-6-6 6-6")
    elif name == "chevron-down":
        P("M6 9l6 6 6-6")
    elif name == "chevron-up":
        P("M18 15l-6-6-6 6")
    elif name == "bookmark":
        P("M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z")
    elif name == "x":
        P("M18 6L6 18"); P("M6 6l12 12")
    elif name == "clock":
        svg.circle(cx, cy, 9 * u, "none", color, 2 * u); P("M12 7v5l3.5 2")
    elif name == "shield":
        P("M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z")
    elif name == "arrow-right":
        P("M5 12h14"); P("M12 5l7 7-7 7")
    elif name == "info":
        svg.circle(cx, cy, 9 * u, "none", color, 2 * u)
        P("M12 16v-4"); P("M12 8h.01", 2.6)
    elif name == "droplet":
        P("M12 2.7l5.7 5.7a8 8 0 1 1-11.4 0z")
    elif name == "compass":
        svg.circle(cx, cy, 9 * u, "none", color, 2 * u)
        P("M16.2 7.8l-2 6.3-6.4 2 2-6.3z")
    elif name == "help-circle":
        svg.circle(cx, cy, 9 * u, "none", color, 2 * u)
        P("M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"); P("M12 17h.01", 2.6)
    else:
        svg.circle(cx, cy, size / 2.4, "none", color, 2 * u)

TABS = [("home", "Home"), ("shopping-bag", "Basket"), ("book-open", "Learn")]

def tab_bar(svg, active):
    top = 780
    svg.rect(0, top, W, 64, SURFACE)
    svg.rect(0, top, W, 0.5, LINE)
    col_w = W / 3
    for i, (icon, label) in enumerate(TABS):
        cx = col_w * i + col_w / 2
        c = ACCENT if label == active else N400
        feather(svg, icon, cx, top + 19, 21, c)
        svg.text(cx, top + 47, label, 10, c, 600, anchor="middle")
    svg.rect(128, 830, 134, 5, INK, rx=2.5)

def hero_leaf(svg, x, y, size=180, opacity=0.55):
    u = size / 120.0
    svg.add(f'<g transform="translate({x},{y}) scale({u})" fill="none" '
            f'stroke="{ARTWORK_LINE}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{opacity}">'
            '<path d="M96 14 C56 18, 24 46, 22 86 C62 88, 96 58, 96 14 Z"/>'
            '<path d="M22 86 C42 66, 68 44, 96 14"/>'
            '<path d="M40 74 C50 70, 58 62, 62 52"/>'
            '<path d="M58 56 C70 52, 78 44, 82 34"/>'
            '<path d="M10 104 C14 98, 18 92, 22 86"/></g>')

def card(svg, x, y, w, h, rx=12):
    svg.rect(x, y, w, h, SURFACE, rx=rx, stroke=LINE, sw=1)

def section_overline(svg, x, y, title, action=None):
    svg.text(x, y, title.upper(), 11, SUBTLE, 600, ls=1.4)
    if action:
        svg.text(372, y, action, 12, ACCENT, 400, anchor="end")

def row_card(svg, x, y, w, title, caption, glyph_key=None, feather_icon=None):
    card(svg, x, y, w, 58, rx=12)
    svg.rect(x + 12, y + 12, 34, 34, ACCENT_TINT, rx=10)
    if glyph_key:
        svg.glyph(glyph_key, x + 18, y + 18, 22)
    else:
        feather(svg, feather_icon or "circle", x + 29, y + 29, 18, ACCENT)
    svg.text(x + 57, y + 26, title, 15, INK, 400)
    if caption:
        svg.text(x + 57, y + 43, caption, 12, SUBTLE, 400)
    feather(svg, "chevron-right", x + w - 18, y + 29, 18, N400)

def text_lines(svg, x, y, s, width_chars, size, fill, weight=400, lh=None, mono=False, ls=None):
    lh = lh or size * 1.35
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if len(t) * size * (0.50 if mono else 0.47) > width_chars:
            lines.append(cur); cur = wd
        else:
            cur = t
    if cur: lines.append(cur)
    for i, ln in enumerate(lines):
        svg.text(x, y + i * lh, ln, size, fill, weight, mono=mono, ls=ls)
    return y + (len(lines) - 1) * lh

def flatten(body, tint):
    import re
    return re.sub(r'fill="(?!none")[^"]*"', f'fill="{tint}"',
                  re.sub(r'stop-color="[^"]*"', f'stop-color="{tint}"', body))

# =====================================================================
# SCREEN 1 — Home (DashboardScreen, verified against live render)
# =====================================================================
def screen_home():
    s = SVG()
    s.rect(0, 0, W, H, PAPER)
    # ---- hero (headerInk block) ----
    s.clip_open("hero")
    s.raw('<g clip-path="url(#hero)">')
    hero_h = 216
    s.rect(0, 0, W, hero_h, HEADER_INK)
    status_bar(s, dark=True)
    hero_leaf(s, 244, 34, 180)
    s.text(18, 66, "Good Morning, You", 30, ON_HEADER, 600, ls=-0.8)
    y = text_lines(s, 18, 92, "Which pesticides have been found on your food",
                   295, 15, ON_HEADER_MUT, lh=22)
    s.rect(18, 168, 354, 40, SURFACE, rx=20)
    feather(s, "search", 34, 188, 17, SUBTLE)
    s.text(56, 193, "Search a fruit or vegetable", 16, SUBTLE)
    s.raw("</g>")
    # ---- ways in (3 cards) ----
    wy = hero_h + 16
    cw = (354 - 16) / 3
    for i, (icon, label) in enumerate([("camera", "Scan"), ("hash", "Type code"), ("list", "Browse")]):
        x = 18 + i * (cw + 8)
        card(s, x, wy, cw, 62, rx=12)
        feather(s, icon, x + cw / 2, wy + 22, 19, ACCENT)
        s.text(x + cw / 2, wy + 48, label, 12, INK, 400, anchor="middle")
    # ---- Your basket (populated: real app text) ----
    sy = wy + 62 + 24
    section_overline(s, 18, sy + 12, "Your basket", action="See all")
    cy = sy + 20
    card(s, 18, cy, 354, 132, rx=12)
    s.text(30, cy + 36, "5", 22, INK, 500)
    s.text(46, cy + 36, "items saved", 12, SUBTLE, 400)
    s.text(30, cy + 56, "Four of them have no Australian results.", 12, MUTED, 400)
    # overlapping glyph tiles with surface ring + "+1"
    tiles = ["blueberries", "leafy-green", "tomato", "red-apple"]
    tx = 30
    for k in tiles:
        s.rect(tx, cy + 66, 40, 40, ACCENT_TINT, rx=12)
        s.glyph(k, tx + 10, cy + 76, 20)
        tx += 44
    s.rect(tx, cy + 66, 40, 40, N100, rx=12)
    s.text(tx + 20, cy + 91, "+1", 12, MUTED, 600, anchor="middle")
    s.text(30, cy + 124, "Most often bought first, tap to open", 11, SUBTLE)
    # ---- What we hold: CoverageMap (66 dots: 4 AU + 62 overseas + 0 none) ----
    wy2 = cy + 132 + 24
    section_overline(s, 18, wy2 + 12, "What we hold")
    cy2 = wy2 + 20
    card(s, 18, cy2, 354, 224, rx=12)
    gx, gy = 30, cy2 + 12
    pattern = [ACCENT] * 4 + [ACCENT_MID] * 62
    for i, c in enumerate(pattern):
        col, row = i % 22, i // 22
        s.circle(gx + col * 15.2 + 7, gy + row * 15.2 + 7, 6.2, c)
    ly = gy + 3 * 15.2 + 14
    for c, lab, n in [(ACCENT, "Tested in Australia", "4"),
                      (ACCENT_MID, "Overseas results only", "62"),
                      (N300, "Nothing published yet", "0")]:
        s.hairline(30, ly, 330)
        s.circle(36.5, ly + 17, 4.5, c)
        s.text(49, ly + 21, lab, 15, INK)
        s.text(322, ly + 21, n, 13, MUTED, 500, mono=True, anchor="end")
        feather(s, "chevron-right", 350, ly + 17, 15, N400)
        ly += 33
    s.text(30, ly + 16, "Most of what we hold was measured in America and Britain.", 12, MUTED)
    s.text(30, ly + 32, "That gap is the reason this app exists.", 12, MUTED)
    # ---- Where the records come from (ProgrammeBar card) ----
    py = cy2 + 224 + 16
    card(s, 18, py, 354, 118, rx=12)
    s.text(30, py + 28, "Where the records come from", 15, INK, 500)
    # track h9 radius4.5: US only 79% / US and UK 16% / UK only 4%
    bx, bw = 30, 330
    segs = [(0.79, ACCENT), (0.16, ACCENT_MID), (0.04, ACCENT_SOFT)]
    xx = bx
    s.rect(bx, py + 44, bw, 9, N100, rx=4.5)
    for frac, c in segs:
        wseg = bw * frac
        s.add(f'<clipPath id="pbar"><rect x="{bx}" y="{py + 44}" width="{bw}" height="9" rx="4.5"/></clipPath>')
        s.add(f'<g clip-path="url(#pbar)"><rect x="{xx:.1f}" y="{py + 44}" width="{wseg:.1f}" height="9" fill="{c}"/></g>')
        xx += wseg
    for i, (lab, pct, c) in enumerate([("US only", "79%", ACCENT),
                                       ("US and UK", "16%", ACCENT_MID),
                                       ("UK only", "4%", ACCENT_SOFT)]):
        lx = 30 + i * 112
        s.circle(lx + 4, py + 80, 4.5, c)
        s.text(lx + 14, py + 84, lab, 11, MUTED)
        s.text(lx + 78, py + 84, pct, 11, INK, 500, mono=True)
    # ---- Learn rowcard ----
    ly2 = py + 118 + 24
    section_overline(s, 18, ly2 + 12, "Learn", action="Open")
    row_card(s, 18, ly2 + 20, 354, "What is an MRL (Maximum Residue…", "Guide of the week",
             feather_icon="book-open")
    tab_bar(s, "Home")
    return s.out()

# =====================================================================
# SCREEN 2 — Packaged scan (Epic-9 concept in real scanner language)
# =====================================================================
def screen_scan():
    s = SVG()
    s.rect(0, 0, W, H, HEADER_INK)
    status_bar(s, dark=True)
    feather(s, "x", 28, 66, 22, SUBTLE)
    s.text(195, 62, "POINT AT THE PACKAGING", 11, ON_HEADER_MUT, 600, ls=1.4, anchor="middle")
    rx0, ry0 = 85, 128
    s.rect(rx0, ry0, 220, 220, "none", rx=16, stroke=ON_HEADER, sw=2, opacity=0.6)
    s.raw('<g transform="translate(158,188) scale(0.55)" opacity="0.35">'
          + GLYPHS["blueberries"]["body"] + "</g>")
    s.rect(rx0 + 12, ry0 + 104, 196, 2, ACCENT_SOFT, rx=1, opacity=0.85)
    s.text(195, 380, "Reading the label…", 12, ON_HEADER_MUT, 400, anchor="middle")
    # ---- bottom result sheet ----
    sh_y = 432
    s.rect(0, sh_y, W, H - sh_y, SURFACE, rx=16)
    s.rect(171, sh_y + 8, 48, 5, N300, rx=2.5)
    s.text(24, sh_y + 44, "SHOPPING SCAN RESULT", 10, ACCENT, 500, ls=1.6, mono=True)
    s.text(24, sh_y + 80, "Blueberry", 30, INK, 400, ls=-0.8)
    s.text(24, sh_y + 102, "OCR CONFIDENCE 92% · PLU 4240", 10, N400, 400, ls=1.1, mono=True)
    card(s, 24, sh_y + 122, 342, 78, rx=10)
    s.glyph("blueberries", 40, sh_y + 136, 26)
    s.text(80, sh_y + 150, "Packaged · 125 g punnet", 15, INK, 600)
    s.text(80, sh_y + 170, "Product of Australia · variety label matched", 12, MUTED)
    feather(s, "chevron-right", 348, sh_y + 161, 18, N400)
    s.rect(24, sh_y + 212, 342, 62, ACCENT_TINT, rx=10)
    feather(s, "droplet", 42, sh_y + 234, 14, ACCENT_INK)
    s.text(60, sh_y + 230, "No washing claims on this pack", 12, ACCENT_INK, 600)
    text_lines(s, 60, sh_y + 248, "The washing estimate shown next describes raw produce, measured from its chemicals.",
               300, 12, ACCENT_INK, lh=17)
    s.rect(24, sh_y + 292, 342, 52, ACCENT, rx=14)
    s.text(195, sh_y + 323, "View produce details", 15, ON_HEADER, 600, anchor="middle")
    s.text(195, sh_y + 376, "Add to basket", 12, ACCENT, 400, anchor="middle",
           style="text-decoration:underline")
    s.rect(128, 830, 134, 5, ON_HEADER, rx=2.5, opacity=0.9)
    return s.out()

# =====================================================================
# SCREEN 3 — Spinach detail (ProduceDetailScreen + WashComparison,
#            real data: median 42%, limited evidence, 9/55 vinegar)
# =====================================================================
def screen_detail():
    s = SVG()
    s.rect(0, 0, W, H, PAPER)
    s.rect(0, 0, W, 118, HEADER_INK)
    status_bar(s, dark=True)
    s.clip_open("dhead", h=118)
    s.raw('<g clip-path="url(#dhead)"><g transform="translate(268,40) scale(1.17)" opacity="0.55">'
          + flatten(GLYPHS["blueberries"]["body"], ARTWORK_LINE) + "</g></g>")
    feather(s, "chevron-left", 26, 96, 20, ON_HEADER_MUT)
    s.text(44, 100, "BLUEBERRY", 11, ON_HEADER_MUT, 600, ls=1.8)
    feather(s, "bookmark", 356, 97, 18, ON_HEADER_MUT)
    # ---- lede: real actionPrimary for blueberry (no produce-specific study) ----
    y = 142
    s.text(18, y, "WHAT TO DO", 10, ACCENT, 500, ls=1.6, mono=True); y += 34
    s.text(18, y, "Wash as usual", 34, INK, 400, ls=-1)
    s.text(18, y + 38, "(general hygiene)", 34, INK, 400, ls=-1); y += 76
    s.rect(18, y, 34, 2, ACCENT, rx=1); y += 30
    y = text_lines(s, 18, y, "No study has measured blueberries directly. This estimate uses measured wash results for the same chemicals found on them.",
                   350, 16, MUTED, lh=24); y += 34
    s.text(18, y, "ESTIMATE · NO BLUEBERRY-SPECIFIC STUDY", 10, N400, 400, ls=1.1, mono=True,
           style="text-decoration:underline"); y += 30
    # ---- open section: washing estimate (US 8.1) ----
    s.hairline(18, y, 354)
    s.text(18, y + 22, "Washing estimate", 15, INK)
    s.text(346, y + 22, "01", 12, N400, 400, mono=True, anchor="end")
    feather(s, "chevron-up", 362, y + 18, 18, N400)
    y += 46
    s.text(18, y + 16, "What washing is likely to do", 19, INK, 600)
    y = text_lines(s, 18, y + 38, "42 chemicals were found on blueberry. 40 of them (95%) have measured wash results on other produce — matched by CAS number and method.",
                   350, 12, SUBTLE, lh=18)
    # segmented control (same component as measured items)
    seg_y = y + 18
    s.rect(18, seg_y, 354, 34, N100, rx=10)
    methods = ["Rinse", "Water soak", "Baking soda", "Vinegar"]
    mw = (354 - 6) / 4
    s.rect(21, seg_y + 3, mw, 28, HEADER_INK, rx=8)
    for i, m in enumerate(methods):
        s.text(21 + i * mw + mw / 2, seg_y + 21, m, 12,
               ON_HEADER if i == 0 else MUTED, 400, anchor="middle")
    fy = seg_y + 62
    s.text(18, fy, "≈45%", 32, INK, 300, ls=-2)
    s.text(132, fy, "estimated reduction", 12, SUBTLE)
    feather(s, "info", 260, fy - 4, 13, N400)
    s.text(18, fy + 28, "where the same chemicals were studied", 12, MUTED)
    # track: dashed to mark estimate
    tr_y = fy + 42
    s.rect(18, tr_y, 354, 10, N100, rx=5)
    s.add(f'<clipPath id="wtrack"><rect x="18" y="{tr_y}" width="354" height="10" rx="5"/></clipPath>')
    s.add(f'<g clip-path="url(#wtrack)"><rect x="{18 + 354 * 0.30:.0f}" y="{tr_y}" width="{354 * 0.30:.0f}" height="10" fill="{ACCENT_MID}" opacity="0.55"/></g>')
    s.text(18, tr_y + 26, "0%", 10, N400)
    s.text(195, tr_y + 26, "50%", 10, N400, anchor="middle")
    s.text(372, tr_y + 26, "100%", 10, N400, anchor="end")
    y = tr_y + 42
    # ---- US 8.2: how accurate has this estimate been ----
    s.rect(18, y - 14, 200, 26, ACCENT_TINT, rx=13)
    s.circle(32, y - 1, 3, ACCENT_INK)
    s.text(42, y + 3, "Estimate · checked against studies", 10, ACCENT_INK, 600, ls=0.3)
    y = text_lines(s, 18, y + 24, "Where this method could be checked against real studies, it came within a median of 12 points of the measured value.",
                   350, 12, SUBTLE, lh=18)
    s.text(18, y + 10, "CHECKED ON 23 ITEMS THAT DO HAVE STUDIES", 9, N400, 400, ls=0.8, mono=True)
    # ---- chemical coverage rows (measured elsewhere) ----
    cy2 = y + 30
    for name, v in [("Boscalid", "48%"), ("Pyraclostrobin", "63%"),
                    ("Cyprodinil", "41%"), ("Fenhexamid", "52%")]:
        s.hairline(18, cy2, 354)
        s.text(18, cy2 + 18, name, 12, MUTED)
        s.text(300, cy2 + 18, "elsewhere", 10, N400, anchor="end")
        s.text(372, cy2 + 18, v, 12, INK, 500, mono=True, anchor="end")
        cy2 += 26
    tab_bar(s, "Home")
    return s.out()

# =====================================================================
# SCREEN 4 — Explore (Epic-10 concept in real design language)
# =====================================================================
def screen_explore():
    s = SVG()
    s.rect(0, 0, W, H, PAPER)
    s.rect(0, 0, W, 168, HEADER_INK)
    status_bar(s, dark=True)
    s.text(18, 66, "PRODUCE DISCOVERY", 10, ON_HEADER_MUT, 500, ls=1.6, mono=True)
    s.text(18, 102, "Explore", 30, ON_HEADER, 600, ls=-0.8)
    text_lines(s, 18, 126, "Age-relevant produce picks, mapped to Australian and New Zealand nutrient references.",
               310, 13, ON_HEADER_MUT, lh=18)
    cy = 188
    chips = [("1–3 years", True), ("4–8 years", False), ("9–13 years", False)]
    cx = 18
    for lab, sel in chips:
        wch = len(lab) * 7 + 24
        s.rect(cx, cy, wch, 30, ACCENT if sel else SURFACE, rx=15,
               stroke=None if sel else LINE, sw=1)
        s.text(cx + wch / 2, cy + 19, lab, 11, ON_HEADER if sel else N800, 600, anchor="middle")
        cx += wch + 8
    s.text(18, cy + 50, "Stays on this phone. Nothing is collected.", 12, SUBTLE)
    # TRY card
    y0 = cy + 70
    card(s, 18, y0, 354, 158, rx=12)
    s.rect(30, y0 + 14, 40, 40, ACCENT_TINT, rx=10)
    s.glyph("roasted-sweet-potato", 36, y0 + 20, 28)
    s.text(80, y0 + 32, "Sweet potato", 15, INK, 600)
    s.text(80, y0 + 50, "Ipomoea batatas", 11, SUBTLE)
    s.rect(310, y0 + 18, 50, 22, ACCENT_TINT, rx=11)
    s.text(335, y0 + 33, "TRY", 10, ACCENT_INK, 600, ls=1.0, anchor="middle")
    text_lines(s, 30, y0 + 74,
               "High in beta-carotene for this age band, and soft enough to serve mashed.",
               320, 12, MUTED, lh=17)
    s.rect(30, y0 + 100, 330, 34, N100, rx=8)
    s.text(42, y0 + 121, "BETA-CAROTENE 850 µg · 81% EAR (1–3 YRS)", 10, N600, 500, ls=0.5, mono=True)
    s.text(30, y0 + 152, "View the evidence", 12, ACCENT, 600)
    feather(s, "arrow-right", 142, y0 + 148, 14, ACCENT)
    # REDISCOVER card
    y1 = y0 + 170
    card(s, 18, y1, 354, 158, rx=12)
    s.rect(30, y1 + 14, 40, 40, N100, rx=10)
    s.glyph("summer-squash", 36, y1 + 20, 28)
    s.text(80, y1 + 32, "Zucchini", 15, INK, 600)
    s.text(80, y1 + 50, "Cucurbita pepo", 11, SUBTLE)
    s.rect(292, y1 + 18, 68, 22, N100, rx=11)
    s.text(326, y1 + 33, "REDISCOVER", 9, N600, 600, ls=0.8, anchor="middle")
    text_lines(s, 30, y1 + 74,
               "Not in the last six weeks of your basket. Mild flavour, easy to grate into pasta.",
               320, 12, MUTED, lh=17)
    s.rect(30, y1 + 100, 330, 34, N100, rx=8)
    s.text(42, y1 + 121, "VITAMIN C 17 mg · 74% EAR (1–3 YRS)", 10, N600, 500, ls=0.5, mono=True)
    s.text(30, y1 + 152, "View the evidence", 12, ACCENT, 600)
    feather(s, "arrow-right", 142, y1 + 148, 14, ACCENT)
    tab_bar(s, "Learn")
    return s.out()

# =====================================================================
# SCREEN 5 — Basket (real render: 1 AU / 3 wash / 2 neither;
#            real row order Blueberry, Spinach, Apple, Tomato…)
# =====================================================================
def screen_basket():
    s = SVG()
    s.rect(0, 0, W, H, PAPER)
    mh = 252
    s.rect(0, 0, W, mh, HEADER_INK)
    status_bar(s, dark=True)
    s.text(18, 66, "Your basket", 30, ON_HEADER, 600, ls=-0.8)
    s.text(18, 92, "5 items, saved on this phone only", 12, ON_HEADER_MUT)
    for i, (count, phrase, tone) in enumerate([
        (1, "of 5 items tested in Australia", ACCENT_MID),
        (3, "of 5 items with a washing study", ACCENT_SOFT)]):
        ty = 122 + i * 56
        s.text(18, ty + 14, str(count), 17, ON_HEADER, 600)
        s.text(30, ty + 14, phrase, 11, ON_HEADER_MUT)
        s.rect(18, ty + 24, 354, 7, "#FFFFFF", rx=3.5, opacity=0.12)
        s.rect(18, ty + 24, 354 * count / 5, 7, tone, rx=3.5)
    s.text(18, 236, "2 items have neither yet.", 11, ON_HEADER_MUT)
    # footnote
    y = mh + 20
    y = text_lines(s, 18, y + 12,
                   "Two separate counts of items with a property in the record. An item can have both, so they are never added together.",
                   350, 12, N400, lh=17)
    fy = y + 30
    s.text(18, fy, "YOUR ITEMS", 11, SUBTLE, 600, ls=1.4)
    chips = [("All 5", True), ("Often 2", False), ("Sometimes 2", False),
             ("Rarely 1", False), ("Not marked 0", False)]
    cx, cy = 18, fy + 12
    for lab, sel in chips:
        wch = len(lab) * 6.4 + 28
        if cx + wch > 372:  # wrap to next row like the real chips row
            cx, cy = 18, cy + 36
        s.rect(cx, cy, wch, 28, ACCENT if sel else SURFACE, rx=14,
               stroke=None if sel else LINE, sw=1)
        s.text(cx + wch / 2, cy + 18, lab, 11, ON_HEADER if sel else N800, 600, anchor="middle")
        cx += wch + 6
    # rows — real basket order & copy
    ry = cy + 40
    rows = [
        ("Blueberry", "blueberries", "42 pesticides · tested in the US and UK only", None),
        ("Spinach", "leafy-green", "55 pesticides · tested in the US and UK only",
         "Washing cut residues by a median of 42% in published studies"),
        ("Apple", "red-apple", "54 pesticides · tested in Australia",
         "Washing cut residues by a median of 38% in published studies"),
        ("Tomato", "tomato", "56 pesticides · tested in the US and UK only",
         "Washing cut residues by a median of 48% in published studies"),
    ]
    for name, g, cov, wash in rows:
        h = 84 if wash else 62
        card(s, 18, ry, 354, h, rx=14)
        s.glyph(g, 32, ry + 18, 26)
        s.text(70, ry + 26, name, 15, INK, 400)
        s.text(70, ry + 43, cov, 11, N600)
        if wash:
            feather(s, "droplet", 72, ry + 60, 11, ACCENT_INK)
            text_lines(s, 84, ry + 63, wash, 270, 10.5, ACCENT_INK, lh=14)
        else:
            s.text(70, ry + 56, "No washing study yet", 10.5, N400)
        feather(s, "chevron-right", 354, ry + h / 2, 16, N300)
        ry += h + 12
    # explainer card peeks like the real screen
    ey = ry + 4
    card(s, 18, ey, 354, 150, rx=10)
    s.text(30, ey + 26, "Why the pattern matters", 15, INK, 600)
    yy = ey + 48
    yy = text_lines(s, 30, yy,
        "A monitoring survey describes single batches on single days. What you buy week after week is the pattern that shapes your overall picture.",
        322, 12, MUTED, lh=17); yy += 22
    text_lines(s, 30, yy,
        "ResidueLens does not calculate your personal exposure and cannot tell you your risk.",
        322, 12, MUTED, lh=17)
    tab_bar(s, "Basket")
    return s.out()

# =====================================================================
screens = {
    "1_home_screen.svg": screen_home(),
    "2_packaged_scan.svg": screen_scan(),
    "3_washing_estimate.svg": screen_detail(),
    "4_explore_discovery.svg": screen_explore(),
    "5_my_basket.svg": screen_basket(),
}
for name, content in screens.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print("wrote", name, len(content), "bytes")
