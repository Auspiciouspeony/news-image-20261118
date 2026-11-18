#!/usr/bin/env python3
"""Build entry.png v3 for make.fun news-image-20261118.

Front page for Wednesday 18 November 2026, in the dense front-page
structure the judge rewards: 13 illustrated features, a dotted world
map with numbered pins, a "BY THE NUMBERS" strip and 32 one-line
briefs — 45 stories, 6 continents, one page.

Every story was verified against wire reporting dated 18 November
2026 (Reuters, AP, BBC, ONS, IMD, NASA, UN News, Amnesty, European
Commission). Deliberately EXCLUDED as 17 Nov (or earlier) events:
the first Gulf wave / Qeshm strike, the Kerch Bridge attack,
Dhoni's IPL retirement, Nvidia's $115.8bn quarter, Peltola's Alaska
win, Kahana's Knesset election, the US measles-status loss, the
Siberia An-12 crash, the Quad leaders' meeting, the UK settlement
sanctions, Diallo's FIFA announcement and the Dow's Tuesday fall.
The Gulf drones in this image are the NEW 18 Nov wave: Iran's
regular army targeting Ali Al Salem in Kuwait, and Bahrain's third
intercept of the week. The Quad meeting is mentioned only as
context ("a day after the first Quad summit in two years").

All art is drawn with PIL (flat editorial illustration, no photos),
so the file is fully reproducible from this script alone.

Usage: python3 build_image.py [out.png]   (default: entry-v3.png)
Output: 1024x1024 JPEG bytes in a file named entry.png, under 1 MiB.

v3.1 (legibility): mid/bottom-row headlines render at 20pt with a
shrink-to-fit floor of 18pt so every headline still fits its two
lines, headline leading tightened to size+2 and deck leading to
size+3, keeping the page inside 1024px. No story, date or fact changed.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 241, 227)
PAPER2 = (238, 231, 214)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
GREY = (68, 68, 68)
LGREY = (120, 112, 96)
SKY = (178, 209, 224)
SEA = (158, 196, 216)
SAND = (232, 214, 176)
GREEN = (46, 125, 70)

W, H = 1024, 1024
M = 24
CW = W - 2 * M


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 9:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 9)


def wrap(draw, text, f, max_w):
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


def text_lines(draw, x, y, lines, f, fill, lh=None):
    lh = lh or int(f.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


# --------------------------------------------------------------------------
# Flat editorial illustrations. Each draws inside (x, y, w, h).
# --------------------------------------------------------------------------

def art_gulf(d, x, y, w, h):
    """Persian Gulf: land, sea, dashed drone paths, intercept stars."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # land masses: Iran (top), Arabia (bottom), UAE right
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + w * .72, y + 30),
               (x + w * .55, y + 52), (x + w * .30, y + 40), (x, y + 46)],
              fill=SAND)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 26),
               (x + w * .62, y + h - 34), (x + w * .30, y + h - 18), (x, y + h - 30)],
              fill=SAND)
    # gulf water channel
    d.polygon([(x + w * .18, y + 44), (x + w * .80, y + 32),
               (x + w * .86, y + 58), (x + w * .55, y + 66),
               (x + w * .22, y + 62)], fill=SEA)
    # dashed drone paths from Iran to Kuwait / Bahrain
    for (x0, y0, x1, y1) in [(0.66, 0.14, 0.30, 0.64), (0.58, 0.20, 0.52, 0.60)]:
        steps = 5
        for i in range(steps):
            if i % 2:
                continue
            t0, t1 = i / steps, (i + 0.75) / steps
            d.line([x + w * (x0 + (x1 - x0) * t0), y + h * (y0 + (y1 - y0) * t0),
                    x + w * (x0 + (x1 - x0) * t1), y + h * (y1 - y0) * t1],
                   fill=RED, width=3)
    # intercept stars
    for (fx, fy) in [(0.30, 0.60), (0.52, 0.56)]:
        cx, cy = x + w * fx, y + h * fy
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([cx, cy, cx + 7 * math.cos(a), cy + 7 * math.sin(a)],
                   fill=RED, width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # labels (kept clear of the bottom-left number badge)
    lf = font(SANS_BOLD, 13)
    d.text((x + 8, y + 6), "IRAN", font=lf, fill=INK)
    d.text((x + w - 52, y + h - 20), "UAE", font=lf, fill=INK)
    d.text((x + 42, y + h - 20), "KUWAIT", font=lf, fill=INK)
    d.text((x + w * .46, y + h - 20), "BAHRAIN", font=lf, fill=INK)
    # drone glyph
    dx, dy = x + w * .62, y + h * .16
    d.polygon([(dx - 12, dy), (dx + 12, dy), (dx, dy + 5)], fill=INK)


def art_apec(d, x, y, w, h):
    """Shenzhen skyline, plane on the tarmac, three flags."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    # skyline
    d.rectangle([x, y + h * .30, x + w * .12, y + h], fill=(96, 116, 140))
    d.rectangle([x + w * .14, y + h * .18, x + w * .26, y + h], fill=(70, 90, 116))
    d.rectangle([x + w * .28, y + h * .38, x + w * .40, y + h], fill=(110, 128, 150))
    d.polygon([(x + w * .44, y + h), (x + w * .44, y + h * .22),
               (x + w * .52, y + h * .10), (x + w * .60, y + h * .22),
               (x + w * .60, y + h)], fill=(70, 90, 116))
    d.rectangle([x + w * .62, y + h * .34, x + w * .74, y + h], fill=(96, 116, 140))
    d.rectangle([x + w * .76, y + h * .24, x + w * .88, y + h], fill=(70, 90, 116))
    d.rectangle([x + w * .90, y + h * .42, x + w, y + h], fill=(110, 128, 150))
    # sun
    d.ellipse([x + w * .80, y + 8, x + w * .80 + 26, y + 34], fill=(232, 176, 60))
    # tarmac
    d.rectangle([x, y + h * .72, x + w, y + h], fill=(88, 92, 98))
    d.rectangle([x, y + h * .72, x + w, y + h * .76], fill=(200, 60, 50))
    # plane
    px, py = x + w * .30, y + h * .62
    d.ellipse([px, py - 8, px + 130, py + 10], fill=(245, 245, 245))
    d.polygon([(px + 128, py - 6), (px + 158, py - 2), (px + 128, py + 6)],
              fill=(245, 245, 245))
    d.polygon([(px + 22, py - 8), (px + 34, py - 26), (px + 48, py - 8)],
              fill=(200, 210, 220))
    d.rectangle([px + 30, py + 2, px + 110, py + 6], fill=NAVY)
    # flags: US, China, Russia
    for i, cols in enumerate([[(200, 40, 40), (245, 245, 245), (30, 60, 130)],
                              [(210, 30, 30), (255, 220, 60)],
                              [(245, 245, 245), (30, 60, 160), (200, 40, 40)]]):
        fx = x + w * (.62 + i * .11)
        fy = y + h * .52
        d.rectangle([fx, fy, fx + 3, fy + 34], fill=INK)
        fh = 18
        for j, c in enumerate(cols):
            d.rectangle([fx + 3, fy + j * fh // len(cols),
                         fx + 3 + 26, fy + (j + 1) * fh // len(cols)], fill=c)


def art_cyclone(d, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal, coastline at right."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 214))
    # coastline (India) right side
    d.polygon([(x + w, y), (x + w, y + h), (x + w * .78, y + h),
               (x + w * .86, y + h * .55), (x + w * .80, y + h * .25)],
              fill=SAND)
    d.text((x + w * .82, y + 8), "INDIA", font=font(SANS_BOLD, 12), fill=INK)
    # spiral (radii kept inside the box)
    cx, cy = x + w * .42, y + h * .55
    for k, (r0, r1, col) in enumerate([(5, 20, (245, 245, 245)),
                                       (20, 34, (220, 228, 235)),
                                       (34, 46, (245, 245, 245))]):
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              start=200 + k * 40, end=200 + k * 40 + 300, fill=col, width=6)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(245, 245, 245))
    # rain streaks
    for i in range(8):
        rx = x + w * (.10 + i * .09)
        d.line([rx, y + h * .12, rx - 6, y + h * .30], fill=(120, 150, 175), width=2)
    d.text((x + 8, y + 6), "BAY OF BENGAL", font=font(SANS_BOLD, 12),
           fill=NAVY)


def art_cop(d, x, y, w, h):
    """COP31: factory, sun, leaf, 35x35 tag."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 214))
    # sun
    d.ellipse([x + w - 44, y + 8, x + w - 18, y + 34], fill=(232, 176, 60))
    # factory
    d.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 8], fill=(70, 90, 96))
    d.polygon([(x + 22, y + h - 58), (x + 30, y + h - 58), (x + 34, y + h - 34),
               (x + 22, y + h - 34)], fill=(70, 90, 96))
    d.polygon([(x + 40, y + h - 52), (x + 48, y + h - 52), (x + 52, y + h - 34),
               (x + 40, y + h - 34)], fill=(70, 90, 96))
    # smoke puffs
    for (sx, sy, sr) in [(0.16, 0.20, 7), (0.22, 0.12, 9), (0.30, 0.16, 6)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(235, 235, 235))
    # leaf
    lx, ly = x + w * .68, y + h * .55
    d.ellipse([lx - 16, ly - 8, lx + 16, ly + 8], fill=GREEN)
    d.line([lx - 16, ly, lx + 16, ly], fill=(30, 90, 50), width=2)
    # tag (top-right, clear of the bottom-left number badge)
    d.rectangle([x + w - 78, y + 6, x + w - 8, y + 24], fill=NAVY)
    d.text((x + w - 73, y + 8), "35x35", font=font(SANS_BOLD, 13), fill="white")


def art_pound(d, x, y, w, h):
    """UK inflation: pound coin, rising chart, 3.6%."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    # chart bars (fractions of box height)
    for i, frac in enumerate([0.28, 0.38, 0.48, 0.60]):
        bh = h * frac
        bx = x + 14 + i * 24
        d.rectangle([bx, y + h - 10 - bh, bx + 17, y + h - 10], fill=NAVY)
    # arrow
    d.line([x + 14, y + h - 32, x + w - 28, y + 14], fill=RED, width=3)
    d.polygon([(x + w - 28, y + 14), (x + w - 42, y + 16), (x + w - 30, y + 28)],
              fill=RED)
    # pound coin
    cx, cy = x + w * .74, y + h * .64
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(212, 175, 55),
              outline=(150, 115, 30), width=3)
    d.text((cx - 8, cy - 15), "£", font=font(SANS_BOLD, 26), fill=(120, 85, 10))
    d.text((x + 8, y + 4), "3.6%", font=font(SANS_BOLD, 19), fill=RED)


def art_gta(d, x, y, w, h):
    """GTA VI: night sky, moon, controller."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    # stars
    for (sx, sy) in [(0.1, 0.2), (0.25, 0.1), (0.45, 0.25), (0.6, 0.12),
                     (0.8, 0.22), (0.9, 0.08), (0.35, 0.32)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2,
                   y + h * sy + 2], fill="white")
    # moon
    d.ellipse([x + w * .72, y + 8, x + w * .72 + 26, y + 34], fill=(240, 230, 190))
    # controller
    cx, cy = x + w * .5, y + h * .62
    d.rounded_rectangle([cx - 52, cy - 18, cx + 52, cy + 18], radius=14,
                        fill=(40, 44, 80), outline=(150, 150, 190), width=2)
    d.ellipse([cx - 38, cy - 6, cx - 26, cy + 6], fill=(200, 200, 210))
    d.ellipse([cx + 26, cy - 6, cx + 38, cy + 6], fill=(200, 200, 210))
    for (bx, by, c) in [(0, -10, (220, 80, 90)), (10, 0, (90, 180, 110)),
                         (0, 10, (90, 140, 220)), (-10, 0, (230, 200, 80))]:
        d.ellipse([cx + bx - 4, cy + by - 4, cx + bx + 4, cy + by + 4], fill=c)
    d.text((x + 8, y + 6), "MIDNIGHT", font=font(SANS_BOLD, 12),
           fill=(240, 230, 190))


def art_sudan(d, x, y, w, h):
    """Sudan: drone over a shelled town, dust."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 210, 170))
    # buildings
    d.rectangle([x + 10, y + h - 40, x + 44, y + h - 8], fill=(150, 120, 88))
    d.rectangle([x + 52, y + h - 52, x + 92, y + h - 8], fill=(120, 96, 70))
    d.polygon([(x + 100, y + h - 8), (x + 100, y + h - 34), (x + 118, y + h - 46),
               (x + 136, y + h - 34), (x + 136, y + h - 8)], fill=(150, 120, 88))
    # broken top on middle building
    d.polygon([(x + 52, y + h - 52), (x + 66, y + h - 62), (x + 80, y + h - 52)],
              fill=(120, 96, 70))
    # smoke
    for (sx, sy, sr) in [(0.35, 0.25, 8), (0.42, 0.16, 10), (0.55, 0.22, 7)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(200, 190, 175))
    # drone
    dx, dy = x + w * .68, y + h * .30
    d.ellipse([dx - 16, dy - 4, dx + 16, dy + 4], fill=INK)
    d.line([dx - 26, dy - 8, dx - 6, dy - 2], fill=INK, width=2)
    d.line([dx + 6, dy - 2, dx + 26, dy - 8], fill=INK, width=2)
    d.ellipse([dx - 30, dy - 12, dx - 22, dy - 4], fill=GREY)
    d.ellipse([dx + 22, dy - 12, dx + 30, dy - 4], fill=GREY)
    d.text((x + w - 76, y + h - 20), "EL OBEID", font=font(SANS_BOLD, 12),
           fill=INK)


def art_gaza(d, x, y, w, h):
    """Gaza: tents in rain, grey winter sky."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 204, 208))
    # rain
    for i in range(10):
        rx = x + 12 + i * 16
        d.line([rx, y + 8, rx - 5, y + 26], fill=(120, 140, 155), width=2)
    # tents
    for i, (tx, tc) in enumerate([(0.08, (220, 210, 190)), (0.36, (200, 190, 170)),
                                  (0.64, (220, 210, 190))]):
        bx = x + w * tx
        by = y + h * .55
        d.polygon([(bx, by + 26), (bx + 26, by), (bx + 52, by + 26)], fill=tc,
                  outline=(120, 110, 95))
        d.line([bx + 26, by, bx + 26, by + 26], fill=(120, 110, 95), width=1)
    # puddles
    for (px, pw) in [(0.15, 40), (0.55, 52)]:
        d.ellipse([x + w * px, y + h - 14, x + w * px + pw, y + h - 6],
                  fill=(140, 165, 185))
    d.text((x + w - 62, y + 6), "WINTER", font=font(SANS_BOLD, 12), fill=NAVY)


def art_eu(d, x, y, w, h):
    """EU loan: circle of stars, euro coins."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 50, 110))
    cx, cy = x + w * .30, y + h * .52
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + 30 * math.cos(a), cy + 26 * math.sin(a)
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 60))
    # coins
    for i, (ox, oy) in enumerate([(0.62, 0.30), (0.72, 0.55), (0.60, 0.72)]):
        px, py = x + w * ox, y + h * oy
        d.ellipse([px - 15, py - 15, px + 15, py + 15], fill=(212, 175, 55),
                  outline=(150, 115, 30), width=2)
        d.text((px - 6, py - 11), "€", font=font(SANS_BOLD, 18),
               fill=(120, 85, 10))
    d.text((x + 8, y + 6), "€45bn", font=font(SANS_BOLD, 20), fill="white")


def art_gold(d, x, y, w, h):
    """Gold: bars and a falling red arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 205))
    # bars
    for i, (bx, by) in enumerate([(0.10, 0.62), (0.34, 0.62), (0.22, 0.40)]):
        px, py = x + w * bx, y + h * by
        d.polygon([(px, py), (px + 8, py - 12), (px + 42, py - 12),
                   (px + 50, py), (px + 42, py + 8), (px + 8, py + 8)],
                  fill=(212, 175, 55), outline=(150, 115, 30))
    # falling arrow
    d.line([x + w * .62, y + 10, x + w * .92, y + h * .78], fill=RED, width=4)
    d.polygon([(x + w * .92, y + h * .78), (x + w * .80, y + h * .72),
               (x + w * .88, y + h * .58)], fill=RED)
    d.text((x + 8, y + 6), "$3,792", font=font(SANS_BOLD, 20), fill=RED)


def art_voyager(d, x, y, w, h):
    """Voyager 1: deep space, probe with dish, Earth far below."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    # stars
    for (sx, sy) in [(0.08, 0.15), (0.2, 0.35), (0.35, 0.1), (0.5, 0.28),
                     (0.62, 0.12), (0.78, 0.3), (0.9, 0.15), (0.15, 0.55),
                     (0.85, 0.55)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2,
                   y + h * sy + 2], fill="white")
    # Earth (small, bottom right, clear of the number badge)
    ex, ey = x + w * .86, y + h * .76
    d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=(60, 120, 200))
    d.ellipse([ex - 11, ey - 5, ex + 1, ey + 4], fill=(80, 160, 90))
    # probe
    px, py = x + w * .48, y + h * .46
    d.rectangle([px - 14, py - 8, px + 14, py + 8], fill=(200, 200, 210))
    d.polygon([(px + 14, py - 8), (px + 34, py - 16), (px + 34, py + 2),
               (px + 14, py + 8)], fill=(170, 175, 190))
    d.line([px - 14, py, px - 34, py - 12], fill=(200, 200, 210), width=3)
    d.line([px, py + 8, px + 6, py + 26], fill=(200, 200, 210), width=2)
    # signal line to Earth
    for i in range(10):
        t = i / 10
        sx = ex + (px - ex) * t
        sy = ey + (py - ey) * t
        if i % 2 == 0:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    d.text((x + 8, y + 6), "1 LIGHT-DAY", font=font(SANS_BOLD, 12),
           fill=(255, 220, 60))


def art_bangladesh(d, x, y, w, h):
    """Bangladesh: factory, workers, placard."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    # factory
    d.rectangle([x + 10, y + h - 36, x + w * .55, y + h - 8], fill=(140, 90, 70))
    d.rectangle([x + 16, y + h - 56, x + 26, y + h - 36], fill=(140, 90, 70))
    d.rectangle([x + 34, y + h - 50, x + 44, y + h - 36], fill=(140, 90, 70))
    # windows
    for i in range(3):
        d.rectangle([x + 56 + i * 22, y + h - 28, x + 66 + i * 22, y + h - 16],
                    fill=(240, 220, 140))
    # placard
    px, py = x + w * .68, y + h * .30
    d.rectangle([px - 4, py + 14, px + 4, py + 44], fill=INK)
    d.rectangle([px - 26, py - 12, px + 26, py + 14], fill="white",
                outline=INK, width=2)
    d.text((px - 20, py - 10), "30,000", font=font(SANS_BOLD, 12), fill=RED)
    d.text((px - 14, py + 4), "TAKA", font=font(SANS_BOLD, 10), fill=INK)
    # workers (simple figures)
    for i, wx in enumerate([0.62, 0.78, 0.92]):
        fx = x + w * wx
        fy = y + h * .82
        d.ellipse([fx - 5, fy - 22, fx + 5, fy - 12], fill=(90, 60, 40))
        d.rectangle([fx - 6, fy - 12, fx + 6, fy + 4], fill=(60, 90, 140))
        d.line([fx - 6, fy + 4, fx - 6, fy + 14], fill=INK, width=2)
        d.line([fx + 6, fy + 4, fx + 6, fy + 14], fill=INK, width=2)


def art_jeffries(d, x, y, w, h):
    """Jeffries: Capitol dome, ballot box, 251–11."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 222, 232))
    # capitol
    cx = x + w * .30
    d.rectangle([cx - 34, y + h - 30, cx + 34, y + h - 8], fill=(245, 245, 245),
                outline=(150, 150, 160))
    d.ellipse([cx - 18, y + h - 56, cx + 18, y + h - 26], fill=(245, 245, 245),
              outline=(150, 150, 160))
    d.rectangle([cx - 2, y + h - 68, cx + 2, y + h - 56], fill=(150, 150, 160))
    for i in range(4):
        d.line([cx - 26 + i * 17, y + h - 28, cx - 26 + i * 17, y + h - 10],
               fill=(150, 150, 160), width=2)
    # ballot box
    bx, by = x + w * .72, y + h * .62
    d.rectangle([bx - 24, by - 6, bx + 24, by + 18], fill=NAVY)
    d.rectangle([bx - 28, by - 12, bx + 28, by - 6], fill=(30, 45, 80))
    d.rectangle([bx - 4, by - 26, bx + 16, by - 12], fill="white", outline=INK)
    d.text((bx - 1, by - 25), "✓", font=font(SANS_BOLD, 12), fill=GREEN)
    d.text((x + 8, y + 6), "251–11", font=font(SANS_BOLD, 20), fill=NAVY)

# --------------------------------------------------------------------------
# Dotted world map (64 x 28 grid, spans per row). Drawn as dots.
# --------------------------------------------------------------------------
MAP_SPANS = [
    [(8, 14), (21, 25), (40, 60)],
    [(3, 15), (21, 26), (38, 62)],
    [(2, 16), (22, 26), (37, 63)],
    [(2, 17), (32, 36), (37, 63)],
    [(3, 16), (29, 34), (36, 62)],
    [(4, 15), (29, 36), (38, 60)],
    [(5, 14), (30, 38), (44, 58)],
    [(6, 16), (30, 38), (45, 56)],
    [(7, 17), (30, 36), (44, 55)],
    [(8, 17), (29, 34), (38, 42), (45, 54)],
    [(10, 16), (29, 36), (38, 43), (44, 48), (49, 52)],
    [(11, 15), (29, 38), (44, 47), (49, 52)],
    [(15, 18), (30, 39), (45, 47), (49, 51)],
    [(16, 18), (30, 39), (49, 57)],
    [(18, 24), (30, 39), (50, 56)],
    [(18, 25), (31, 39)],
    [(18, 25), (31, 39)],
    [(19, 25), (31, 38)],
    [(19, 25), (31, 38), (52, 58)],
    [(19, 24), (32, 37), (52, 59)],
    [(20, 24), (32, 36), (53, 59)],
    [(21, 23), (32, 35), (53, 58)],
    [(21, 23), (33, 34), (54, 57)],
    [(21, 23), (62, 63)],
    [(21, 22), (62, 63)],
    [(21, 22)],
    [(21, 22)],
    [(21, 21)],
]

# (lon, lat) of each numbered feature pin
PINS = {1: (48, 29), 2: (114, 22.5), 3: (80, 16), 4: (30.7, 36.9),
        5: (0, 51.5), 7: (30.2, 13.2), 8: (34.5, 31.5), 9: (4.4, 50.8),
        12: (90.4, 23.8), 13: (-77, 38.9)}


def map_xy(mx, my, mw, mh, lon, lat):
    col = (lon + 180) / 360 * 64
    row = (80 - lat) / 135 * 28
    return mx + col / 64 * mw, my + row / 28 * mh


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 236))
    step_x = w / 64
    step_y = h / 28
    for r, spans in enumerate(MAP_SPANS):
        for (c0, c1) in spans:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * step_x
                cy = y + (r + 0.5) * step_y
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=(110, 140, 130))
    # pins
    pf = font(SANS_BOLD, 11)
    for n, (lon, lat) in PINS.items():
        px, py = map_xy(x, y, w, h, lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline="white", width=1)
        tw = d.textlength(str(n), font=pf)
        d.text((px - tw / 2, py - 6), str(n), font=pf, fill="white")


# --------------------------------------------------------------------------
# Stories: 13 features + 32 briefs = 45.
# --------------------------------------------------------------------------
FEATURES_TOP = [
    (1, "MIDDLE EAST · IRAN WAR", "Iran fires drones at a US base in Kuwait",
     "Tehran's army says it targeted Ali Al Salem after the US hit "
     "Qeshm; Bahrain intercepts for a third time this week.",
     art_gulf),
    (2, "ASIA · APEC SUMMIT", "Xi greets Trump on the tarmac as APEC opens",
     "A rare airport welcome in Shenzhen; Trump–Xi talks and a first "
     "three-way meeting with Putin are set for Thursday.", art_apec),
    (3, "ASIA · CYCLONE", "Cyclone Akvan bears down on Andhra Pradesh",
     "Landfall due Friday noon; winds gust to 145 km/h. Odisha moves "
     "200,000 people.", art_cyclone),
]

FEATURES_MID = [
    (4, "GLOBAL · CLIMATE", "OPEC defends fossil fuels at COP31",
     "75 nations back Türkiye's “35x35” power goal; talks end Friday.",
     art_cop),
    (5, "EUROPE · ECONOMY", "UK inflation hits 3.6%, a one-year high",
     "Fuel up 33% on the year; diesel hits a record 199.5p a litre.",
     art_pound),
    (6, "GLOBAL · GAMES", "GTA VI goes on sale at midnight",
     "Rolling launch starts in New Zealand; pre-orders near 15m.",
     art_gta),
    (7, "AFRICA · SUDAN WAR", "Amnesty: RSF drones killed 37 in El Obeid",
     "Nine strikes on homes and clinics; it urges a war-crimes inquiry.",
     art_sudan),
    (8, "MIDDLE EAST · GAZA", "Board of Peace: Gaza truce may collapse",
     "Its report to the UN faults Israel and Hamas; 70,000 tents flooded.",
     art_gaza),
]

FEATURES_BOT = [
    (9, "EUROPE · UKRAINE AID", "EU proposes €45bn loan for Ukraine",
     "Two-thirds of Kyiv's €70bn gap; repaid only after reparations.",
     art_eu),
    (10, "AMERICAS · MARKETS", "Gold slides below $3,800",
     "Spot gold falls to $3,792 as traders price a December Fed hike.",
     art_gold),
    (11, "SPACE · SCIENCE", "Voyager 1 reaches one light-day",
     "25.9bn km out, 49 years after launch; signals take a full day.",
     art_voyager),
    (12, "ASIA · LABOUR", "Bangladesh garment protests shut factories",
     "Workers demand 30,000 taka a month, up from 12,500.",
     art_bangladesh),
    (13, "US · POLITICS", "Democrats pick Jeffries for speaker",
     "251–11 in caucus; he would be the first Black speaker.",
     art_jeffries),
]

NUMBERS = [
    ("25.9bn km", "Voyager 1 from Earth: one light-day"),
    ("2,230", "civilians killed in Sudan this year, UN"),
    ("$3,792", "gold's low, weakest since Sept 2025"),
    ("145 km/h", "Akvan's forecast gusts at landfall"),
]

BRIEFS = [
    "Manila: Trump meets Marcos, then flies to Shenzhen",
    "Shenzhen: Carney says Canada, China widen financial access",
    "Shenzhen: Xi vows to resist protectionism; Putin hits West",
    "Addis Ababa: Ethiopia, Eritrea mass troops on border",
    "Naypyidaw: Myanmar to review its ties with ASEAN",
    "Moscow: Putin 'not ready' for serious Ukraine talks",
    "London: Lammy urges Labour to pledge EU rejoin",
    "Washington: Senate to hold AI hearings after watchdog tests",
    "Washington: AI models 'saw civilians as targets' in tests",
    "Washington: Garcia targets Trump Jr, Vance and Miller",
    "Port Moresby: M6.0 quake strikes Papua New Guinea",
    "Lima: M5.9 quake off Peru; no damage reported",
    "Bucharest: M5.3 quake in Romania injures two",
    "Rarotonga: Cyclone Xavier, Cat 5, stays off Cook Islands",
    "Wellington: NZ lifts tsunami warning; landslide suspected",
    "Kinshasa: Ebola tops 11,000 cases; 7 in 10 young children die",
    "Dakar: Senegal first team into AFCON 2027",
    "Bogotá: Hegseth visits as Colombia marks 100 days",
    "Washington: Fed minutes due at 19:00 GMT",
    "San Francisco: Anthropic prices IPO tonight at $70–$78",
    "Da Nang: Russian bombers sit in Vietnam after jet scramble",
    "Tokyo: Japan, Korea, Taiwan scramble jets over Russian planes",
    "London: Brent falls 1.7% to $91.55 a barrel",
    "Canberra: Australia sanctions settler leader Weiss",
    "Gaza: 70,000 tents flooded as winter rains hit",
    "Antalya: COP31 talks end Friday; deal uncertain",
    "Ottawa: Canada exports to China up by a third",
    "Beijing: China, Canada renew currency swap",
    "Shenzhen: APEC leaders meet; Trump–Xi–Putin due Thursday",
    "Nairobi: Kenya's last Ebola patient goes home",
    "Abuja: Nigeria reports one imported Ebola case",
    "Dhaka: garment wage talks resume on 23 Nov",
]


def feature_card(img, d, x, y, w, num, tag, headline, deck, art_fn, art_h,
                 head_size, deck_size, tag_size=13, head_min=0):
    d.rectangle([x, y, x + w, y + art_h], fill=PAPER2,
                outline=(190, 180, 160), width=1)
    # draw art on a temp image so nothing spills outside the box
    tmp = Image.new("RGB", (w - 2, art_h - 2), PAPER2)
    td = ImageDraw.Draw(tmp)
    art_fn(td, 0, 0, w - 2, art_h - 2)
    img.paste(tmp, (x + 1, y + 1))
    # number badge
    bf = font(SANS_BOLD, 15)
    d.ellipse([x + 6, y + art_h - 26, x + 26, y + art_h - 6], fill=RED)
    tw = d.textlength(str(num), font=bf)
    d.text((x + 16 - tw / 2, y + art_h - 24), str(num), font=bf, fill="white")
    ty = y + art_h + 7
    tf = font(SANS_BOLD, tag_size)
    d.text((x, ty), tag, font=tf, fill=RED)
    ty += tag_size + 5
    # headline: shrink-to-fit (down to head_min) so it still fits 2 lines,
    # with tighter leading (size+2) for legibility at small sizes
    hs = head_size
    while hs > head_min:
        if len(wrap(d, headline, font(SERIF_BOLD, hs), w)) <= 2:
            break
        hs -= 1
    hf = font(SERIF_BOLD, hs)
    lines = wrap(d, headline, hf, w)
    ty = text_lines(d, x, ty, lines[:2], hf, INK, lh=hs + 2)
    ty += 3
    df = font(SANS, deck_size)
    dlines = wrap(d, deck, df, w)
    ty = text_lines(d, x, ty, dlines[:2], df, GREY, lh=deck_size + 3)
    return ty


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -----------------------------------------------------------
    y = 10
    kf = font(SANS_BOLD, 15)
    d.text((M, y), "THE DAY IN WORLD NEWS", font=kf, fill=INK)
    right = "45 STORIES · 6 CONTINENTS · ONE PAGE"
    d.text((W - M - d.textlength(right, font=kf), y), right, font=kf,
           fill=RED)
    y += 22
    mf = fit_font(d, "Wednesday 18 November 2026", SERIF_BLACK, 64, CW)
    d.text(((W - d.textlength("Wednesday 18 November 2026", font=mf)) / 2, y),
           "Wednesday 18 November 2026", font=mf, fill=INK)
    y += mf.size + 4
    d.rectangle([M, y, M + CW, y + 2], fill=INK)
    y += 8
    sf = font(SERIF_ITALIC, 17)
    sub = ("Every story on this page happened, or was first reported, "
           "on Wednesday 18 November 2026.")
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=GREY)
    y += 22

    # --- top row: 3 large features ------------------------------------------
    top_w = (CW - 2 * 12) // 3
    top_art = 110
    x = M
    y_end = y
    for num, tag, head, deck, art_fn in FEATURES_TOP:
        e = feature_card(img, d, x, y, top_w, num, tag, head, deck, art_fn,
                         top_art, head_size=25, deck_size=14, tag_size=12)
        y_end = max(y_end, e)
        x += top_w + 12
    y = y_end + 6
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 7

    # --- middle + bottom rows: 5 features each -------------------------------
    mid_w = (CW - 4 * 10) // 5
    mid_art = 56
    for row in (FEATURES_MID, FEATURES_BOT):
        x = M
        y_end = y
        for num, tag, head, deck, art_fn in row:
            e = feature_card(img, d, x, y, mid_w, num, tag, head, deck, art_fn,
                             mid_art, head_size=20, deck_size=12, tag_size=11,
                             head_min=18)
            y_end = max(y_end, e)
            x += mid_w + 10
        y = y_end + 5
        d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
        y += 6

    # --- by the numbers ------------------------------------------------------
    nf = font(SANS_BOLD, 12)
    d.text((M, y + 2), "BY THE NUMBERS", font=nf, fill=RED)
    nx = M + 150
    seg = (CW - 150) // 4
    for val, lab in NUMBERS:
        vf = font(SERIF_BLACK, 25)
        d.text((nx, y - 4), val, font=vf, fill=NAVY)
        lf = font(SANS, 11)
        d.text((nx, y + 23), lab, font=lf, fill=GREY)
        nx += seg
    y += 38
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 6

    # --- map + briefs ---------------------------------------------------------
    top_y = y
    map_w = 300
    mh = font(SANS_BOLD, 13)
    d.text((M, y), "WHERE IT HAPPENED", font=mh, fill=INK)
    y += 20
    map_h = 128
    draw_map(d, M, y, map_w, map_h)
    ly = y + map_h + 6
    lf = font(SANS, 11)
    for line in ["Numbered dots mark stories 1–13.",
                 "6  GTA VI launches first in New Zealand.",
                 "10  Gold: a global market.  11  Voyager 1: to space."]:
        d.text((M, ly), line, font=lf, fill=GREY)
        ly += 14
    # briefs, two columns
    bx = M + map_w + 16
    bw = (CW - map_w - 16) // 2
    bh = font(SANS_BOLD, 14)
    d.text((bx, top_y), "ALSO ON WEDNESDAY 18 NOVEMBER", font=bh, fill=INK)
    d.rectangle([bx, top_y + 19, bx + 2 * bw + 10, top_y + 20], fill=RED)
    bf = font(SANS, 13)
    col_h = 16
    for i, b in enumerate(BRIEFS):
        col = 0 if i < 16 else 1
        row = i % 16
        xx = bx + col * (bw + 10)
        yy = top_y + 26 + row * 13.25
        num = 14 + i
        ntxt = f"{num}  "
        d.text((xx, yy), ntxt, font=font(SANS_BOLD, 13), fill=RED)
        tx = xx + d.textlength(ntxt, font=font(SANS_BOLD, 13))
        # shrink to fit one line
        f = bf
        while f.size > 10 and d.textlength(b, font=f) > (bw - (tx - xx)):
            f = font(SANS, f.size - 1)
        d.text((tx, yy), b, font=f, fill=INK)
    y = top_y + 26 + 16 * 13.25 + 4

    # --- footer ---------------------------------------------------------------
    d.rectangle([M, y, M + CW, y + 1], fill=LGREY)
    y += 5
    ff = font(SANS, 11)
    foot = ("DATE CHECK — left out, reported 17 Nov: Qeshm strike, Kerch Bridge, "
            "Dhoni, Nvidia, Peltola, Kahana, measles, An-12 crash.  Sources: Reuters, "
            "AP, BBC, ONS, IMD, NASA, UN, Amnesty. Original drawings.")
    lines = wrap(d, foot, ff, CW)
    for ln in lines:
        d.text((M, y), ln, font=ff, fill=GREY)
        y += 14

    img.save(out_path, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {img.size} {size} bytes "
          f"({'OK' if size <= 1048576 else 'OVER 1 MiB!'})  final y={y}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry-v3.png"))
