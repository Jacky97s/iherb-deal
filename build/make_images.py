# -*- coding: utf-8 -*-
"""Generate og.png + PWA icons for the iHerb MPD0133 site."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
GREEN, DARK, LIGHT, GOLD = (31,157,87), (13,92,52), (255,255,255), (246,196,83)


def font(size, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def centered(d, cx, y, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (b[2] - b[0]) / 2, y), text, font=fnt, fill=fill)


# ---- OG image 1200x630 ----
img = Image.new("RGB", (1200, 630), DARK)
d = ImageDraw.Draw(img)
for y in range(630):  # vertical gradient
    t = y / 630
    d.line([(0, y), (1200, y)],
           fill=(int(13 + t * 18), int(92 + t * 30), int(52 + t * 20)))
d.rounded_rectangle([330, 250, 870, 380], 24, fill=LIGHT)
centered(d, 600, 92, "iHerb DISCOUNT CODE", font(46), GOLD)
centered(d, 600, 150, "Save up to 20% on your order", font(58), LIGHT)
centered(d, 600, 276, "MPD0133", font(96), GREEN)
centered(d, 600, 430, "Vitamins · Supplements · Beauty", font(38, False), (200, 230, 210))
centered(d, 600, 492, "Free code · Works in 180+ countries", font(34, False), (170, 210, 185))
img.save(os.path.join(OUT, "og.png"), "PNG")
print("og.png 1200x630")

# ---- App icons ----
for size in (180, 192, 512):
    ic = Image.new("RGB", (size, size), GREEN)
    dd = ImageDraw.Draw(ic)
    centered(dd, size / 2, size * 0.20, "iH", font(int(size * 0.42)), LIGHT)
    centered(dd, size / 2, size * 0.62, "SAVE", font(int(size * 0.16)), (191, 240, 212))
    ic.save(os.path.join(OUT, "icon-%d.png" % size), "PNG")
    print("icon-%d.png" % size)

print("images done ->", os.path.abspath(OUT))
