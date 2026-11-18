#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261118 (round 2).

A dense one-page front page for Wednesday 18 November 2026: 12
illustrated feature stories, a world map with numbered pins, and 30
numbered briefs - 42 stories across six continents. Every illustration
is drawn flat with PIL primitives (no model-rendered lettering anywhere);
every word is crisp vector text.

Stories verified against wire reports of 18 Nov 2026 (Reuters, AP, AFP,
Bloomberg, NASA, IMD): the Gulf drone strikes, Xi greeting Trump on the
Shenzhen tarmac, the second Kerch bridge strike, the EU's EUR45bn Ukraine
loan, Cyclone Akvan, Peltola's Alaska win, the COP31 split, the Board of
Peace Gaza warning, Nvidia's results, Voyager 1's light-day, the Knesset
speaker vote, and the El Obeid drone strikes. Deliberately left out
(see the DATE CHECK footer): the Xi-Carney tariff cuts, the first Kerch
bridge strike, and the US strike on Qeshm - all reported 17 Nov.

Usage: python3 build_image.py [out.png]   (default: entry.png)
Output: 1024x1024 JPEG bytes in a file named entry.png, under the 1 MiB gate.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 241, 227)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
BLUE = (28, 78, 158)
TEAL = (0, 118, 118)
GOLD = (198, 158, 38)
GREY = (92, 86, 76)
LINE = (198, 188, 168)
SKY = (178, 208, 228)
SEA = (126, 178, 205)

W, H = 1024, 1024
M = 24                       # side margin
CW = W - 2 * M               # content width


def font(path, size):
    return ImageFont.truetype(path, int(size))


def fit_font(draw, text, path, start, max_w):
    """Largest size <= start that fits max_w."""
    size = start
    while size > 9:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 9)


def wrap(draw, text, f, max_w):
    """Greedy word wrap into lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def starburst(d, cx, cy, r, color):
    """Small explosion star: 8 spikes."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def dashed_line(d, x0, y0, x1, y1, color, dash=7, width=2):
    n = int(math.hypot(x1 - x0, y1 - y0) / dash)
    for i in range(0, n, 2):
        t0, t1 = i / n, min((i + 1) / n, 1.0)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=color, width=width)


# ---------------------------------------------------------------- stories
# (num, region, headline, deck, scene, pin lat, pin lon)
FEATURES = [
    (1, "MIDDLE EAST \u00b7 IRAN WAR",
     "Iran fires drones at US bases in the Gulf",
     "Tehran says it aimed at Ali Al Salem in Kuwait and a US radar in "
     "Bahrain; both say they intercepted the attacks.",
     "gulf", 29.3, 47.9),
    (2, "ASIA \u00b7 APEC SUMMIT",
     "Xi greets Trump on the tarmac in Shenzhen",
     "A first for Xi with any visiting leader; the trilateral with Putin "
     "is set for Thursday.",
     "tarmac", 22.5, 114.0),
    (3, "EUROPE \u00b7 UKRAINE WAR",
     "Second strike brings down Kerch bridge span",
     "Kyiv says the road arch fell into the sea; Putin lands in Shenzhen "
     "hours later.",
     "bridge", 45.3, 36.5),
    (4, "EUROPE \u00b7 UKRAINE AID",
     "EU proposes \u20ac45bn loan for Ukraine",
     "It would cover two-thirds of Kyiv's 2027 gap, repaid only once "
     "Russia pays reparations.",
     "eu", 50.8, 4.4),
    (5, "ASIA \u00b7 DISASTER",
     "Cyclone Akvan veers north toward Odisha",
     "Landfall due Friday; gusts of 145 km/h, and 204,070 people to be "
     "moved from the coast.",
     "cyclone", 19.8, 85.8),
    (6, "AMERICAS \u00b7 US POLITICS",
     "Peltola wins Alaska; Senate now 56\u201344",
     "She unseats Sullivan in the final race called; a ninth Democratic "
     "gain of the midterms.",
     "senate", 63.0, -152.0),
    (7, "GLOBAL \u00b7 CLIMATE",
     "COP31 splits over fossil-fuel phase-out",
     "Draft seeks net zero by 2030 for rich nations; the EU envoy warns "
     "it could sink the talks.",
     "cop", 36.9, 30.7),
    (8, "MIDDLE EAST \u00b7 GAZA",
     "Board of Peace warns Gaza truce may collapse",
     "Its first report to the Security Council says Israel blocked the "
     "civil administration.",
     "gaza", 31.5, 34.5),
    (9, "US \u00b7 BUSINESS",
     "Nvidia revenue doubles to $115.8bn",
     "Board rules out a return for Jensen Huang and ends H200 chip "
     "shipments to China.",
     "chip", 37.4, -122.0),
    (10, "SPACE \u00b7 SCIENCE",
     "Voyager 1 reaches one light-day from Earth",
     "25.9bn km out at 10:16 GMT \u2014 the first human-made object a full "
     "light-day away.",
     "voyager", 38.9, -77.0),
    (11, "ISRAEL \u00b7 POLITICS",
     "Knesset elects Kahana as speaker, 66\u201352",
     "Kahana, an ally of Gadi Eisenkot, replaces Amir Ohana after a "
     "seven-hour debate.",
     "knesset", 31.8, 35.2),
    (12, "AFRICA \u00b7 SUDAN WAR",
     "RSF drone strikes killed 37 in El Obeid",
     "Amnesty urges a war-crimes inquiry; the RSF denies responsibility.",
     "sudan", 13.2, 30.2),
]

# (num, one-line brief, <= ~56 chars)
BRIEFS = [
    (13, "Manila: Trump hails 'biggest' Philippine trade deal"),
    (14, "Quad leaders meet in Manila, first in two years"),
    (15, "Japan: jets scramble after suspected Russian planes"),
    (16, "UK inflation rises to 3.6%, highest in a year"),
    (17, "Ethiopia\u2013Eritrea mass troops on border"),
    (18, "Bangladesh garment protests shut 55 factories"),
    (19, "Australia sanctions settler leader Daniella Weiss"),
    (20, "Russia fires 141 drones at Ukraine overnight"),
    (21, "Anthropic prices IPO tonight; trades Thursday"),
    (22, "Germany accuses Russia of chemical-weapons breaches"),
    (23, "France: fourth weekend of cost-of-living marches"),
    (24, "UN: 2,230 civilians killed in Sudan this year"),
    (25, "DR Congo: Ebola adds 400\u2013500 cases a week, WHO"),
    (26, "Myanmar to review its ties with ASEAN"),
    (27, "Carney: China trade deal no worry for Trump"),
    (28, "Siberia: An-12 transport crashes; 19 dead"),
    (29, "Riyadh: coalition downs Houthi missile at capital"),
    (30, "Estonia to shut Russia border on 1 Dec"),
    (31, "Berlin: coalition to cut power tax, cap fuel prices"),
    (32, "Dhoni retires \u2014 ends 19-year IPL career; to mentor CSK"),
    (33, "Seoul: court acquits Daegu mayor in martial-law case"),
    (34, "Hong Kong: hospital sorry for ovaries removed in error"),
    (35, "Brazil: police probe Vance-linked donor network"),
    (36, "Ecuador: fishermen sue US over drone attack"),
    (37, "US: loses measles-free status held since 2000"),
    (38, "GTA VI goes on sale at midnight, NZ first"),
    (39, "Cook Islands: Cyclone Xavier reaches Category 5"),
    (40, "New Zealand: tsunami advisory lifted after 60cm surges"),
    (41, "Sydney: Tame Impala sweeps the ARIA Awards"),
    (42, "Brooklyn: Huawei trial closings end; jury out today"),
]


# ---------------------------------------------------------------- scenes
# Each scene draws a flat editorial illustration into box (x, y, w, h).

def scene_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 220, 196))
    d.polygon([(x, y + h * 0.42), (x + w * 0.45, y + h * 0.30),
               (x + w * 0.62, y + h * 0.52), (x + w * 0.55, y + h),
               (x, y + h)], fill=SEA)
    d.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.30),
               (x + w * 0.72, y + h * 0.42), (x + w * 0.62, y + h * 0.28)],
              fill=(214, 196, 160))
    dashed_line(d, x + w * 0.68, y + h * 0.16, x + w * 0.30, y + h * 0.52,
                RED, dash=6)
    starburst(d, x + w * 0.30, y + h * 0.52, 9, (255, 190, 40))
    starburst(d, x + w * 0.52, y + h * 0.66, 8, (255, 190, 40))
    f = font(SANS_BOLD, 10)
    d.text((x + 5, y + 3), "IRAN", font=f, fill=INK)
    d.text((x + w - 52, y + h - 15), "BAHRAIN", font=f, fill=(255, 255, 255))
    d.text((x + 5, y + h - 15), "KUWAIT", font=f, fill=INK)


def scene_tarmac(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 26, y + 6, x + w - 10, y + 22], fill=(255, 214, 90))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(96, 96, 96))
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.62 + 3], fill=(255, 255, 255))
    # plane silhouette: slim fuselage, swept wing, tail fin
    px, py = x + w * 0.06, y + h * 0.34
    d.polygon([(px, py + 4), (px + w * 0.52, py + 4), (px + w * 0.60, py + 8),
               (px + w * 0.52, py + 12), (px, py + 12)], fill=NAVY)
    d.polygon([(px + w * 0.06, py + 4), (px + w * 0.10, py - h * 0.16),
               (px + w * 0.16, py + 4)], fill=NAVY)
    d.polygon([(px + w * 0.24, py + 10), (px + w * 0.36, py + h * 0.30),
               (px + w * 0.44, py + 10)], fill=NAVY)
    d.polygon([(px + w * 0.50, py + 5), (px + w * 0.58, py + 1),
               (px + w * 0.58, py + 11)], fill=NAVY)
    d.rectangle([px + w * 0.08, py + 6, px + w * 0.46, py + 8],
                fill=(255, 255, 255))
    # three flags on poles, bottom right
    for i, cols in enumerate([[(200, 30, 30)], [(200, 30, 30), (255, 255, 255),
                              (30, 60, 160)], [(255, 255, 255), (30, 60, 160),
                              (200, 30, 30)]]):
        fx = x + w * 0.74 + i * 19
        d.line([fx, y + h * 0.40, fx, y + h * 0.62], fill=INK, width=2)
        fh = 12
        for j, c in enumerate(cols):
            d.rectangle([fx, y + h * 0.40 + j * fh / len(cols),
                         fx + 15, y + h * 0.40 + (j + 1) * fh / len(cols)],
                        fill=c)


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    d.rectangle([x + w * 0.04, y + h * 0.30, x + w * 0.42, y + h * 0.40],
                fill=(120, 120, 120))
    d.rectangle([x + w * 0.58, y + h * 0.30, x + w * 0.96, y + h * 0.40],
                fill=(120, 120, 120))
    d.polygon([(x + w * 0.42, y + h * 0.40), (x + w * 0.50, y + h * 0.62),
               (x + w * 0.56, y + h * 0.58), (x + w * 0.50, y + h * 0.34)],
              fill=(90, 90, 90))
    d.arc([x + w * 0.10, y + h * 0.05, x + w * 0.42, y + h * 0.55],
          180, 360, fill=(90, 90, 90), width=3)
    d.arc([x + w * 0.58, y + h * 0.05, x + w * 0.90, y + h * 0.55],
          180, 360, fill=(90, 90, 90), width=3)
    for cx, cy, r in [(x + w * 0.50, y + h * 0.22, 7),
                      (x + w * 0.56, y + h * 0.14, 9),
                      (x + w * 0.47, y + h * 0.12, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 200, 200))
    starburst(d, x + w * 0.50, y + h * 0.38, 8, (255, 190, 40))


def scene_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 120))
    cx, cy = x + w * 0.20, y + h * 0.50
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        starburst(d, sx, sy, 4, (255, 210, 60))
    f = font(SANS_BOLD, 30)
    d.text((x + w * 0.42, y + h * 0.16), "\u20ac45bn", font=f, fill=(255, 255, 255))
    f2 = font(SANS_BOLD, 11)
    d.text((x + w * 0.42, y + h * 0.58), "LOAN FOR UKRAINE", font=f2,
           fill=(255, 210, 60))
    for i in range(4):
        ex = x + w * 0.44 + i * 20
        d.ellipse([ex, y + h - 14, ex + 16, y + h - 2], fill=GOLD)


def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 222))
    cx, cy = x + w * 0.42, y + h * 0.52
    for r, a0, a1 in [(10, 0, 300), (18, 40, 340), (26, 80, 20),
                     (34, 120, 60), (42, 160, 100)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(255, 255, 255),
              width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=NAVY)
    d.polygon([(x + w * 0.62, y + h), (x + w, y + h * 0.55), (x + w, y + h)],
              fill=(222, 200, 150))
    d.text((x + w * 0.66, y + h * 0.62), "INDIA", font=font(SANS_BOLD, 10),
           fill=INK)
    dashed_line(d, x + w * 0.42, y + h * 0.52, x + w * 0.30, y + h * 0.10,
                RED, dash=5)
    d.polygon([(x + w * 0.30, y + h * 0.10), (x + w * 0.24, y + h * 0.16),
               (x + w * 0.32, y + h * 0.18)], fill=RED)


def scene_senate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    ox, oy = x + 10, y + 10
    for r in range(10):
        for c in range(10):
            col = BLUE if r * 10 + c < 56 else RED
            d.ellipse([ox + c * 9, oy + r * 6, ox + c * 9 + 6, oy + r * 6 + 5],
                      fill=col)
    f = font(SANS_BOLD, 26)
    d.text((x + w * 0.52, y + 8), "56\u201344", font=f, fill=NAVY)
    f2 = font(SANS_BOLD, 11)
    d.text((x + w * 0.52, y + 40), "DEMOCRATS", font=f2, fill=BLUE)
    d.text((x + w * 0.52, y + 54), "TAKE SENATE", font=f2, fill=RED)


def scene_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 196))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(120, 130, 110))
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.30, y + h * 0.72],
                fill=(70, 70, 70))
    d.rectangle([x + w * 0.34, y + h * 0.30, x + w * 0.52, y + h * 0.72],
                fill=(90, 90, 90))
    for i, sx in enumerate([0.14, 0.40]):
        d.rectangle([x + w * sx, y + h * 0.18, x + w * (sx + 0.05),
                     y + h * 0.45], fill=(70, 70, 70))
        d.ellipse([x + w * (sx - 0.02), y + h * 0.08, x + w * (sx + 0.09),
                   y + h * 0.22], fill=(230, 230, 230))
    d.rectangle([x + w * 0.58, y + h * 0.14, x + w * 0.95, y + h * 0.52],
                fill=(255, 255, 255), outline=TEAL, width=2)
    f = font(SANS_BOLD, 13)
    d.text((x + w * 0.61, y + h * 0.18), "NET ZERO", font=f, fill=TEAL)
    d.text((x + w * 0.61, y + h * 0.34), "BY 2030", font=f, fill=TEAL)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 216, 178))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(198, 172, 120))
    for i, tx in enumerate([0.08, 0.36, 0.64]):
        d.polygon([(x + w * tx, y + h * 0.70), (x + w * (tx + 0.11), y + h * 0.38),
                   (x + w * (tx + 0.22), y + h * 0.70)], fill=(250, 246, 236),
                  outline=(150, 140, 120))
    d.polygon([(x + w * 0.82, y + h * 0.16), (x + w * 0.94, y + h * 0.44),
               (x + w * 0.70, y + h * 0.44)], fill=(255, 200, 40),
              outline=RED)
    f = font(SANS_BOLD, 20)
    d.text((x + w * 0.805, y + h * 0.22), "!", font=f, fill=RED)


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 40))
    cx, cy = x + w * 0.22, y + h * 0.50
    for dx in (-26, 0, 26):
        d.line([cx + dx, y + 8, cx + dx, cy - 20], fill=GOLD, width=3)
        d.line([cx + dx, cy + 20, cx + dx, y + h - 8], fill=GOLD, width=3)
    for dy in (-20, 0, 20):
        d.line([x + 8, cy + dy, cx - 26, cy + dy], fill=GOLD, width=3)
        d.line([cx + 26, cy + dy, x + w * 0.44, cy + dy], fill=GOLD, width=3)
    d.rectangle([cx - 22, cy - 18, cx + 22, cy + 18], fill=(10, 40, 28),
                outline=GOLD, width=2)
    d.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], fill=(30, 140, 90))
    f = font(SANS_BOLD, 24)
    d.text((x + w * 0.48, y + 10), "$115.8bn", font=f, fill=(255, 255, 255))
    d.line([(x + w * 0.50, y + h - 18), (x + w * 0.62, y + h - 28),
            (x + w * 0.72, y + h - 22), (x + w * 0.88, y + h - 36)],
           fill=(80, 220, 130), width=3)
    d.polygon([(x + w * 0.88, y + h - 36), (x + w * 0.82, y + h - 36),
               (x + w * 0.88, y + h - 28)], fill=(80, 220, 130))


def scene_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for sx, sy, r in [(0.12, 0.18, 1), (0.30, 0.10, 1), (0.55, 0.22, 2),
                      (0.70, 0.10, 1), (0.88, 0.28, 1), (0.45, 0.08, 1),
                      (0.05, 0.45, 1), (0.95, 0.55, 2)]:
        d.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r,
                   y + h * sy + r], fill=(255, 255, 255))
    ex, ey = x + w * 0.16, y + h * 0.72
    d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=(60, 120, 200))
    d.ellipse([ex - 6, ey - 10, ex + 4, ey + 2], fill=(80, 180, 100))
    dashed_line(d, ex + 14, ey - 10, x + w * 0.78, y + h * 0.30, (255, 210, 60))
    px, py = x + w * 0.78, y + h * 0.30
    d.rectangle([px - 5, py - 3, px + 5, py + 3], fill=(220, 220, 220))
    d.line([px - 10, py - 8, px + 10, py + 8], fill=(220, 220, 220), width=2)
    f = font(SANS_BOLD, 11)
    d.text((x + w * 0.52, y + h - 18), "1 LIGHT-DAY", font=f, fill=(255, 210, 60))


def scene_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 20, 64))
    d.rounded_rectangle([x + w * 0.08, y + h * 0.30, x + w * 0.52, y + h * 0.78],
                        radius=12, fill=(20, 20, 20), outline=(150, 150, 150))
    d.ellipse([x + w * 0.15, y + h * 0.42, x + w * 0.23, y + h * 0.56],
              fill=(200, 200, 200))
    for cx, cy, c in [(0.40, 0.44, (255, 80, 80)), (0.45, 0.52, (80, 220, 120)),
                      (0.40, 0.60, (80, 140, 255)), (0.35, 0.52, (255, 210, 60))]:
        d.ellipse([x + w * cx - 4, y + h * cy - 4, x + w * cx + 4,
                   y + h * cy + 4], fill=c)
    f = font(SERIF_BLACK, 44)
    d.text((x + w * 0.58, y + h * 0.10), "VI", font=f, fill=(255, 255, 255))
    f2 = font(SANS_BOLD, 12)
    d.text((x + w * 0.58, y + h * 0.56), "00:00", font=f2, fill=(255, 210, 60))
    d.text((x + w * 0.58, y + h * 0.76), "MIDNIGHT", font=font(SANS_BOLD, 9),
           fill=(200, 200, 200))


def scene_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 178, 120))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(160, 110, 70))
    for bx, bw, bh in [(0.05, 0.18, 0.45), (0.27, 0.14, 0.60),
                       (0.45, 0.20, 0.38), (0.68, 0.16, 0.52)]:
        d.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + bw),
                     y + h * 0.72], fill=(90, 60, 40))
    dx, dy = x + w * 0.78, y + h * 0.28
    d.ellipse([dx - 12, dy - 3, dx + 12, dy + 3], fill=(40, 40, 40))
    d.ellipse([dx - 4, dy - 8, dx + 4, dy - 2], fill=(40, 40, 40))
    for rx, ry in [(-16, -8), (16, -8), (-16, 6), (16, 6)]:
        d.ellipse([dx + rx - 6, dy + ry - 2, dx + rx + 6, dy + ry + 2],
                  fill=(120, 120, 120))
    for cx, cy in [(0.30, 0.30), (0.52, 0.18), (0.60, 0.42)]:
        d.ellipse([x + w * cx - 3, y + h * cy - 3, x + w * cx + 3,
                   y + h * cy + 3], fill=RED)


def scene_knesset(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 220, 240))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(180, 172, 200))
    # parliament building: pediment + columns
    d.polygon([(x + w * 0.14, y + h * 0.42), (x + w * 0.50, y + h * 0.18),
               (x + w * 0.86, y + h * 0.42)], fill=(70, 60, 110))
    for i in range(5):
        cx = x + w * (0.20 + i * 0.15)
        d.rectangle([cx, y + h * 0.44, cx + 9, y + h * 0.70],
                    fill=(240, 236, 248))
    d.rectangle([x + w * 0.10, y + h * 0.70, x + w * 0.90, y + h * 0.76],
                fill=(70, 60, 110))
    # vote tally box
    d.rectangle([x + w * 0.66, y + h * 0.06, x + w * 0.96, y + h * 0.30],
                fill=(255, 255, 255), outline=NAVY, width=2)
    f = font(SANS_BOLD, 15)
    d.text((x + w * 0.69, y + h * 0.08), "66-52", font=f, fill=NAVY)


SCENES = {"gulf": scene_gulf, "tarmac": scene_tarmac, "bridge": scene_bridge,
          "eu": scene_eu, "cyclone": scene_cyclone, "senate": scene_senate,
          "cop": scene_cop, "gaza": scene_gaza, "chip": scene_chip,
          "voyager": scene_voyager, "gta": scene_gta, "sudan": scene_sudan,
          "knesset": scene_knesset}


# ---------------------------------------------------------------- world map
# Dotted world map: land spans per row of a 100 x 43 grid
# (lon -170..190, lat 75..-52). Column = (lon + 170) / 3.6.
DOT_ROWS = {
    0: [(0, 8), (12, 29), (32, 40), (58, 97)],
    1: [(2, 9), (12, 30), (33, 40), (55, 98)],
    2: [(3, 10), (12, 31), (55, 98)],
    3: [(4, 10), (12, 31), (48, 55), (56, 97)],
    4: [(5, 10), (12, 30), (41, 43), (46, 47), (49, 55), (56, 95)],
    5: [(12, 29), (46, 47), (47, 56), (57, 93)],
    6: [(13, 28), (46, 58), (59, 92)],
    7: [(13, 27), (45, 60), (61, 90)],
    8: [(14, 27), (44, 62), (63, 88)],
    9: [(15, 27), (44, 63), (64, 86)],
    10: [(16, 27), (43, 57), (64, 84), (84, 86)],
    11: [(16, 28), (43, 59), (65, 83), (84, 85)],
    12: [(17, 28), (43, 52), (53, 60), (65, 82)],
    13: [(17, 29), (42, 53), (55, 60), (68, 72), (76, 82)],
    14: [(18, 29), (41, 54), (56, 60), (69, 72), (77, 82)],
    15: [(18, 29), (41, 55), (57, 60), (69, 71), (78, 81)],
    16: [(19, 24), (41, 55), (57, 60), (69, 71), (78, 80)],
    17: [(20, 23), (42, 55), (58, 60), (69, 70), (78, 80)],
    18: [(21, 23), (43, 56), (69, 70), (78, 81)],
    19: [(22, 24), (44, 57), (79, 81)],
    20: [(24, 28), (44, 57), (79, 81)],
    21: [(25, 33), (42, 61)],
    22: [(25, 34), (43, 60)],
    23: [(26, 35), (44, 59)],
    24: [(27, 36), (45, 57), (74, 77), (82, 86)],
    25: [(27, 35), (46, 56), (74, 77), (83, 87)],
    26: [(27, 34), (47, 55), (83, 87)],
    27: [(28, 37), (47, 54), (84, 87)],
    28: [(28, 36), (48, 53), (59, 61)],
    29: [(28, 34), (48, 53), (59, 61), (79, 89)],
    30: [(28, 33), (48, 53), (59, 60), (79, 90)],
    31: [(28, 32), (49, 54), (59, 60), (79, 90)],
    32: [(28, 31), (49, 55), (79, 90)],
    33: [(29, 30), (50, 56), (80, 90)],
    34: [(29, 30), (50, 56), (81, 89)],
    35: [(29, 30), (51, 56), (81, 88)],
    36: [(29, 30), (82, 88)],
    37: [(29, 30), (83, 87), (94, 96)],
    38: [(30, 30), (94, 96)],
    39: [(30, 30)],
    40: [(30, 30)],
    41: [(30, 30)],
    42: [(30, 30)],
}
DOT_COLS, DOT_ROWS_N = 100, 43


def project(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 170) / 360.0 * mw,
            my + (75 - lat) / 130.0 * mh)


# ---------------------------------------------------------------- page

def draw_feature(d, x, y, w, num, region, headline, deck, scene):
    SCENES[scene](d, x, y, w, 76)
    ky = y + 82
    d.ellipse([x, ky, x + 17, ky + 17], fill=RED)
    nf = font(SANS_BOLD, 11)
    label = str(num)
    d.text((x + (17 - d.textlength(label, font=nf)) / 2, ky + 2), label,
           font=nf, fill=(255, 255, 255))
    kf = font(SANS_BOLD, 11)
    d.text((x + 22, ky + 2), region, font=kf, fill=RED)
    # headline: shrink until it wraps to at most 2 lines
    size = 19
    while size > 14:
        hf = font(SANS_BOLD, size)
        lines = wrap(d, headline, hf, w)
        if len(lines) <= 2:
            break
        size -= 1
    hy = ky + 22
    for ln in lines[:2]:
        d.text((x, hy), ln, font=hf, fill=INK)
        hy += size + 3
    df = font(SANS, 12)
    dlines = wrap(d, deck, df, w)[:3]
    dy = hy + 2
    for ln in dlines:
        d.text((x, dy), ln, font=df, fill=(50, 48, 44))
        dy += 15


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 238))
    dot = (110, 100, 82)
    for row, spans in DOT_ROWS.items():
        cy = y + (row + 0.5) * h / DOT_ROWS_N
        for c0, c1 in spans:
            for col in range(c0, c1 + 1):
                cx = x + (col + 0.5) * w / DOT_COLS
                d.ellipse([cx - 1.4, cy - 1.4, cx + 1.4, cy + 1.4], fill=dot)
    for num, _reg, _hl, _dk, _sc, lat, lon in FEATURES:
        px, py = project(lon, lat, x, y, w, h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = font(SANS_BOLD, 9)
        label = str(num)
        d.text((px - d.textlength(label, font=nf) / 2, py - 5), label,
               font=nf, fill=(255, 255, 255))


def draw_brief(d, x, y, w, num, text):
    nf = font(SANS_BOLD, 11)
    d.text((x, y), str(num), font=nf, fill=RED)
    tx = x + d.textlength("42 ", font=nf) + 3
    if ": " in text:
        place, rest = text.split(": ", 1)
        pf = font(SANS_BOLD, 11)
        rf = font(SANS, 11)
        d.text((tx, y), place + ": ", font=pf, fill=INK)
        d.text((tx + d.textlength(place + ": ", font=pf), y), rest,
               font=rf, fill=INK)
    else:
        d.text((tx, y), text, font=font(SANS, 11), fill=INK)


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---------------------------------------------------------
    kf = font(SANS_BOLD, 12)
    d.text((M, 10), "THE DAY IN WORLD NEWS", font=kf, fill=RED)
    right = "42 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    d.text((W - M - d.textlength(right, font=kf), 10), right, font=kf,
           fill=GREY)
    title = "Wednesday 18 November 2026"
    mf = fit_font(d, title, SERIF_BLACK, 58, CW)
    d.text(((W - d.textlength(title, font=mf)) / 2, 26), title, font=mf,
           fill=INK)
    d.rectangle([M, 92, M + CW, 95], fill=RED)
    sf = font(SANS, 13)
    sub = ("Every story on this page happened, or was first reported, "
           "on Wednesday 18 November 2026.")
    d.text(((W - d.textlength(sub, font=sf)) / 2, 100), sub, font=sf,
           fill=GREY)

    # --- 12 features, 3 rows of 4 ----------------------------------------
    col_w = (CW - 3 * 10) // 4
    row_h = 196
    for i, feat in enumerate(FEATURES):
        r, c = divmod(i, 4)
        fx = M + c * (col_w + 10)
        fy = 118 + r * row_h
        draw_feature(d, fx, fy, col_w, *feat[:5])
        if c < 3:
            d.line([fx + col_w + 5, fy + 4, fx + col_w + 5,
                    fy + row_h - 14], fill=LINE, width=1)
        if r < 2:
            d.line([fx, fy + row_h - 6, fx + col_w, fy + row_h - 6],
                   fill=LINE, width=1)

    # --- bottom: map + briefs --------------------------------------------
    d.rectangle([M, 710, M + CW, 711], fill=INK)
    hf = font(SANS_BOLD, 12)
    d.text((M, 718), "WHERE IT HAPPENED", font=hf, fill=RED)
    d.text((340, 718), "ALSO ON WEDNESDAY 18 NOVEMBER \u2014 30 MORE STORIES",
           font=hf, fill=RED)
    draw_map(d, M, 738, 300, 188)
    lf = font(SANS, 10)
    d.text((M, 930), "Numbered pins: stories 1-12 above",
           font=lf, fill=GREY)
    for i, (num, text) in enumerate(BRIEFS):
        col, row = divmod(i, 15)
        bx = 340 + col * 324
        by = 738 + row * 14
        draw_brief(d, bx, by, 318, num, text)

    # --- footer: date check + sources ------------------------------------
    d.rectangle([M, 956, M + CW, 957], fill=RED)
    ff = font(SANS_BOLD, 11)
    d.text((M, 962), "DATE CHECK \u2014 ", font=ff, fill=RED)
    lx = M + d.textlength("DATE CHECK \u2014 ", font=ff)
    tf = font(SANS, 11)
    check = ("Left out because they were reported on 17 Nov, not today: the "
             "Xi\u2013Carney tariff cuts; the first Kerch bridge strike; the US "
             "strike on Qeshm on Tuesday night, shown only as the cause of "
             "today's Iranian drones.")
    lines = wrap(d, check, tf, CW - (lx - M))
    ly = 962
    for ln in lines[:2]:
        d.text((lx, ly), ln, font=tf, fill=INK)
        ly += 14
    src = ("Every story happened, or was first reported, on Wednesday 18 November 2026. "
           "Claims by warring sides are attributed.  Sources: Reuters, AP, AFP, BBC, "
           "Bloomberg, NASA, IMD, UN.  Original drawings.")
    sf2 = font(SANS, 10)
    d.text(((W - d.textlength(src, font=sf2)) / 2, 1004), src, font=sf2,
           fill=GREY)

    img.save(out_path, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {img.size} {size} bytes "
          f"({'OK' if size <= 1048576 else 'OVER 1 MiB!'})")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png"))
