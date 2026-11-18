#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261118.

Front page for Wednesday 18 November 2026. Four editorial illustrations
(hero + three panels) were generated for this build and are composed here
with PIL-drawn masthead, headlines and captions, so every word in the
image is crisp vector text, never model-rendered lettering.

Stories (each reported on 18 November 2026, checked against wire reports):
  HERO   Trump lands in Manila - Quad talks open as his Asia trip builds
         toward a China visit (AP / Washington Post / CNN).
  PANEL  Xi meets Carney - Canada and China extend trade deals ahead of
         the APEC summit.
  PANEL  Cyclone Akvan strengthens - a severe cyclonic storm bears down
         on India's east coast (IMD bulletin 17 Nov, in force 18 Nov).
  PANEL  Japan scrambles jets - fighters up after suspected Russian
         military planes near its airspace.
  BRIEFS Britain sanctions Israeli settlement firms; Estonia to close
         its Russia border; new Kyiv-Europe-US talks, Zelensky says.

Deliberately left out: the Crimean Bridge strikes, the Iran-Bahrain
drone attacks and the Dhoni IPL retirement - all verified as 17 Nov
events, not 18 Nov news.

Usage: python3 build_image.py [out.png]   (default: entry.png)
Output: 1024x1024 JPEG bytes in a file named entry.png, under the 1 MiB gate.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 241, 227)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (22, 35, 63)
GREY = (68, 68, 68)

W, H = 1024, 1024
M = 28                      # side margin
CW = W - 2 * M              # content width


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    """Largest size <= start that fits max_w."""
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 10)


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


def cover(im, tw, th):
    """Centre-crop an image to exactly tw x th."""
    iw, ih = im.size
    s = max(tw / iw, th / ih)
    im = im.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th))


def load_panel(name):
    for f in sorted(os.listdir(PANELS)):
        if f.startswith(name) and f.endswith(".webp"):
            return Image.open(os.path.join(PANELS, f)).convert("RGB")
    raise FileNotFoundError(name)


def caption_band(draw, img, x, y, w, h, headline, sub):
    """Navy band with a bold headline and a smaller sub-line (wrapped)."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    pad = 12
    hf = fit_font(draw, headline, SANS_BOLD, 26, w - 2 * pad)
    draw.text((x + pad, y + 8), headline, font=hf, fill="white")
    if sub:
        sf = font(SANS, 17)
        lines = wrap(draw, sub, sf, w - 2 * pad)
        ly = y + 8 + hf.size + 4
        for ln in lines[:2]:
            draw.text((x + pad, ly), ln, font=sf, fill=(214, 220, 235))
            ly += 21
    return y + h


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead: the date is the point of the whole image ---------------
    y = 14
    mf = fit_font(d, "WEDNESDAY 18 NOVEMBER 2026", SERIF_BLACK, 62, CW)
    d.text(((W - d.textlength("WEDNESDAY 18 NOVEMBER 2026", font=mf)) / 2, y),
           "WEDNESDAY 18 NOVEMBER 2026", font=mf, fill=INK)
    y += mf.size + 10
    d.rectangle([M, y, M + CW, y + 3], fill=RED)
    y += 12
    kf = font(SANS_BOLD, 19)
    kicker = "WORLD NEWS  ·  THE DAY IN ONE IMAGE"
    d.text(((W - d.textlength(kicker, font=kf)) / 2, y), kicker,
           font=kf, fill=GREY)
    y += 30

    # --- hero: Trump lands in Manila --------------------------------------
    hero_h = 400
    hero = cover(load_panel("media-generation-hero-manila"), CW, hero_h)
    img.paste(hero, (M, y))
    y += hero_h
    y = caption_band(d, img, M, y, CW, 74,
                     "TRUMP LANDS IN MANILA",
                     "Quad talks open as his Asia trip builds toward a China visit.")
    y += 16

    # --- three story panels ----------------------------------------------
    pw = (CW - 2 * 12) // 3
    ph = 180
    band_h = 92
    panels = [
        ("media-generation-panel-trade", "XI MEETS CARNEY",
         "Canada and China extend trade deals ahead of APEC."),
        ("media-generation-panel-cyclone", "CYCLONE AKVAN STRENGTHENS",
         "Severe storm bears down on India's east coast."),
        ("media-generation-panel-jets", "JAPAN SCRAMBLES JETS",
         "Fighters up after suspected Russian planes."),
    ]
    x = M
    for name, head, sub in panels:
        im = cover(load_panel(name), pw, ph)
        img.paste(im, (x, y))
        caption_band(d, img, x, y + ph, pw, band_h, head, sub)
        x += pw + 12
    y += ph + band_h + 14

    # --- briefs strip ------------------------------------------------------
    d.rectangle([M, y, M + CW, y + 1], fill=(150, 140, 120))
    y += 10
    bf = font(SANS_BOLD, 19)
    label = "ALSO TODAY — "
    d.text((M, y), label, font=bf, fill=RED)
    lx = M + d.textlength(label, font=bf)
    tf = font(SANS, 19)
    briefs = ("Britain sanctions Israeli settlement firms  ·  "
              "Estonia to close its Russia border  ·  "
              "New Kyiv–Europe–US talks, Zelensky says")
    lines = wrap(d, briefs, tf, CW - (lx - M))
    ly = y
    for ln in lines[:2]:
        d.text((lx, ly), ln, font=tf, fill=INK)
        ly += 24
    y = ly + 8

    # --- footer ------------------------------------------------------------
    ff = font(SANS, 14)
    foot = "All stories reported on Wednesday 18 November 2026  ·  AP · BBC · Reuters · DW · IMD"
    d.text(((W - d.textlength(foot, font=ff)) / 2, H - 26), foot,
           font=ff, fill=GREY)

    img.save(out_path, "JPEG", quality=88, optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path}: {img.size} {size} bytes "
          f"({'OK' if size <= 1048576 else 'OVER 1 MiB!'})")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png"))
