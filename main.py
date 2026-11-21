#!/usr/bin/env python3
"""News front page for Saturday, 21 November 2026.

Draws a single 1024x1024 PNG newspaper front page with seven verified
world news stories, using only Pillow and system fonts. No network access.
Deterministic: same input always produces byte-identical output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"

# Palette: warm paper, dark ink, one strong accent red.
PAPER = (247, 241, 227)
PAPER_DARK = (238, 230, 210)
INK = (26, 24, 22)
INK_SOFT = (74, 68, 60)
ACCENT = (179, 38, 30)
ACCENT_DARK = (140, 28, 22)
GOLD = (176, 132, 40)
SKY = (178, 205, 222)
SEA = (46, 98, 130)
GREEN = (46, 110, 62)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FONT_DIR, "liberation/LiberationSerif-Regular.ttf")
SERIF_B = os.path.join(FONT_DIR, "liberation/LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FONT_DIR, "liberation/LiberationSerif-Italic.ttf")
SANS = os.path.join(FONT_DIR, "liberation/LiberationSans-Regular.ttf")
SANS_B = os.path.join(FONT_DIR, "liberation/LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def text_h(draw, text, fnt, max_w):
    """Height of wrapped text block."""
    return len(wrap(draw, text, fnt, max_w)) * int(fnt.size * 1.18)


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def panel_frame(draw, x, y, w, h, fill=(255, 253, 246)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)
    draw.rectangle([x + 3, y + 3, x + w - 3, y + h - 3],
                   outline=(120, 110, 95), width=1)


def tag(draw, x, y, label, fill=ACCENT):
    """Small white-on-accent kicker tag; returns width used."""
    fnt = font(SANS_B, 15)
    tw = int(draw.textlength(label, font=fnt)) + 16
    draw.rectangle([x, y, x + tw, y + 22], fill=fill)
    draw.text((x + 8, y + 3), label, font=fnt, fill=(255, 255, 255))
    return tw


def draw_masthead(draw):
    rule(draw, 28, 26, 996, 3)
    draw.text((512, 36), "THE WORLD TODAY", font=font(SERIF_B, 66),
              fill=INK, anchor="ma")
    rule(draw, 28, 118, 996, 2)
    draw.text((512, 126), "SATURDAY, 21 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE",
              font=font(SANS_B, 17), fill=INK_SOFT, anchor="ma")
    rule(draw, 28, 152, 996, 3)


def draw_hero(draw):
    """Dominant hero panel: magnitude 6.8 Peru earthquake."""
    x, y, w, h = 28, 164, 968, 312
    panel_frame(draw, x, y, w, h)
    # --- illustration zone on the right: shaking ground + tilted buildings
    ix, iy, iw, ih = x + 588, y + 14, 366, h - 28
    draw.rectangle([ix, iy, ix + iw, iy + ih], fill=SKY, outline=INK, width=2)
    # sun / moon glow
    draw.ellipse([ix + iw - 78, iy + 16, ix + iw - 26, iy + 68], fill=(250, 214, 120),
                 outline=INK, width=2)
    # distant mountains
    draw.polygon([(ix, iy + 150), (ix + 90, iy + 80), (ix + 180, iy + 150)],
                 fill=(120, 140, 130))
    draw.polygon([(ix + 120, iy + 150), (ix + 230, iy + 66), (ix + 340, iy + 150)],
                 fill=(96, 118, 108))
    # ground with a wide crack
    draw.rectangle([ix, iy + 150, ix + iw, iy + ih], fill=(196, 164, 120))
    crack = [(ix + 150, iy + 150), (ix + 138, iy + 185), (ix + 168, iy + 205),
             (ix + 150, iy + 235), (ix + 178, iy + 260), (ix + 160, iy + ih)]
    draw.line(crack, fill=INK, width=7, joint="curve")
    draw.line(crack, fill=(60, 40, 26), width=3, joint="curve")
    # tilted buildings either side of the crack
    draw.polygon([(ix + 30, iy + 150), (ix + 96, iy + 128), (ix + 118, iy + 150)],
                 fill=(90, 70, 60))
    draw.rectangle([ix + 34, iy + 96, ix + 104, iy + 150], fill=(214, 196, 168),
                   outline=INK, width=2)
    draw.rectangle([ix + 216, iy + 88, ix + 306, iy + 150], fill=(198, 178, 148),
                   outline=INK, width=2)
    for bx in (44, 66, 88):
        draw.rectangle([ix + bx, iy + 106, ix + bx + 12, iy + 122],
                       fill=(70, 90, 110))
    for bx in (228, 252, 276):
        draw.rectangle([ix + bx, iy + 98, ix + bx + 12, iy + 114],
                       fill=(70, 90, 110))
    # shaking motion marks
    for mx, my in ((ix + 128, iy + 96), (ix + 196, iy + 108), (ix + 320, iy + 96)):
        draw.arc([mx - 14, my - 10, mx + 14, my + 10], -60, 60,
                 fill=ACCENT, width=4)
    # big magnitude badge
    draw.rectangle([ix + 12, iy + ih - 62, ix + 128, iy + ih - 12], fill=ACCENT)
    draw.text((ix + 70, iy + ih - 58), "M 6.8", font=font(SERIF_B, 34),
              fill=(255, 255, 255), anchor="ma")
    # --- text zone on the left
    tx = x + 22
    tag(draw, tx, y + 16, "BREAKING  \u2022  PERU")
    draw_wrapped(draw, "Strong Quake Shakes Peru",
                 font(SERIF_B, 44), tx, y + 48, 552)
    draw_wrapped(draw, "Magnitude 6.8 strikes near Carhuamayo",
                 font(SERIF_B, 30), tx, y + 106, 552)
    rule(draw, tx, y + 172, tx + 552, 1, fill=(150, 138, 118))
    draw_wrapped(draw, "Deep tremor felt as far as Lima; no deaths or major "
                 "damage reported.",
                 font(SANS, 21), tx, y + 186, 552)
    draw.text((tx, y + 262), "Just after midnight UTC  \u2022  Depth over 100 km",
              font=font(SANS_B, 18), fill=ACCENT_DARK)


def illu_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 240), outline=INK, width=2)
    cx, cy, r = x + 62, y + h // 2 + 4, 38
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 200),
                 outline=INK, width=2)
    draw.ellipse([cx - 20, cy - 26, cx + 2, cy - 6], fill=GREEN)
    draw.ellipse([cx + 4, cy + 6, cx + 24, cy + 28], fill=GREEN)
    draw.ellipse([cx - 26, cy + 12, cx - 8, cy + 26], fill=GREEN)
    draw.text((x + w - 104, y + 8), "COP31", font=font(SANS_B, 24), fill=ACCENT_DARK)
    draw.text((x + w - 104, y + 38), "ANTALYA", font=font(SANS_B, 15), fill=INK_SOFT)
    # rising thermometer
    draw.rectangle([x + 118, y + 12, x + 128, y + 62], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.ellipse([x + 112, y + 56, x + 134, y + 78], fill=ACCENT, outline=INK, width=2)
    draw.rectangle([x + 121, y + 30, x + 125, y + 62], fill=ACCENT)


def illu_saudi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(40, 36, 34), outline=INK, width=2)
    # cooling tower / plant block
    draw.polygon([(x + 30, y + h), (x + 42, y + 26), (x + 78, y + 26),
                  (x + 90, y + h)], fill=(150, 148, 142), outline=INK)
    draw.rectangle([x + 118, y + 48, x + 178, y + h], fill=(120, 116, 110),
                   outline=INK, width=2)
    # flame + smoke
    draw.polygon([(x + 52, y + 26), (x + 60, y + 4), (x + 68, y + 26)],
                 fill=(255, 176, 32))
    draw.polygon([(x + 58, y + 26), (x + 62, y + 12), (x + 66, y + 26)],
                 fill=ACCENT)
    for sx, sy, sr in ((x + 150, y + 22, 10), (x + 168, y + 10, 12),
                       (x + 190, y + 26, 9)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200))
    # interceptor arc
    draw.arc([x + 200, y + 8, x + 280, y + 78], 180, 320, fill=(255, 214, 64),
             width=4)
    draw.text((x + 196, y + h - 26), "INTERCEPTED", font=font(SANS_B, 13),
              fill=(255, 214, 64))


def illu_cricket(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(126, 178, 96), outline=INK, width=2)
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(96, 140, 70))
    # pitch strip
    draw.rectangle([x + 90, y + 8, x + 190, y + h - 26], fill=(222, 200, 150),
                   outline=INK, width=1)
    # bat
    draw.polygon([(x + 118, y + 12), (x + 138, y + 18), (x + 118, y + 78),
                  (x + 100, y + 70)], fill=(210, 170, 110), outline=INK, width=2)
    draw.line([(x + 128, y + 14), (x + 142, y + 2)], fill=(150, 110, 60), width=6)
    # red ball
    draw.ellipse([x + 196, y + 52, x + 218, y + 74], fill=ACCENT, outline=INK,
                 width=2)
    draw.text((x + 16, y + 10), "100", font=font(SERIF_B, 40), fill=(255, 255, 255))
    draw.text((x + 16, y + 52), "RUNS", font=font(SANS_B, 14), fill=(255, 255, 255))


def illu_lebanon(draw, x, y, w, h):
    # flag bands: red / white / red
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 18], fill=ACCENT)
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=ACCENT)
    # cedar tree
    cx, cy = x + w // 2, y + h // 2
    draw.polygon([(cx, cy - 30), (cx + 26, cy - 2), (cx + 12, cy - 2),
                  (cx + 30, cy + 14), (cx + 10, cy + 14), (cx + 16, cy + 26),
                  (cx - 16, cy + 26), (cx - 10, cy + 14), (cx - 30, cy + 14),
                  (cx - 12, cy - 2), (cx - 26, cy - 2)], fill=GREEN)
    draw.rectangle([cx - 3, cy + 26, cx + 3, cy + 34], fill=(110, 80, 50))
    draw.text((x + 10, y + h - 17), "83 YEARS", font=font(SANS_B, 13),
              fill=(255, 255, 255))


def illu_vests(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 220, 205), outline=INK, width=2)
    # crowd silhouettes
    for hx in (x + 24, x + 58, x + 92, x + 196, x + 230, x + 264):
        draw.ellipse([hx - 9, y + 52, hx + 9, y + 70], fill=INK_SOFT)
        draw.rectangle([hx - 12, y + 70, hx + 12, y + h], fill=INK_SOFT)
    # high-vis vest in the middle
    draw.polygon([(x + 128, y + 8), (x + 176, y + 8), (x + 186, y + 22),
                  (x + 168, y + 26), (x + 168, y + h - 4), (x + 136, y + h - 4),
                  (x + 136, y + 26), (x + 118, y + 22)], fill=(255, 214, 0),
                 outline=INK, width=2)
    draw.rectangle([x + 136, y + 40, x + 168, y + 48], fill=(220, 220, 220))
    draw.rectangle([x + 136, y + 58, x + 168, y + 66], fill=(220, 220, 220))
    draw.text((x + 10, y + 8), "8 YEARS", font=font(SANS_B, 14), fill=INK)


def illu_dragon(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 220), outline=INK, width=2)
    # parachute canopy
    draw.pieslice([x + 96, y - 34, x + 208, y + 46], 0, 180, fill=(255, 120, 40),
                  outline=INK, width=2)
    draw.pieslice([x + 124, y - 34, x + 180, y + 46], 0, 180, fill=(255, 255, 255),
                  outline=INK, width=2)
    draw.line([(x + 96, y + 44), (x + 140, y + 66)], fill=INK, width=2)
    draw.line([(x + 208, y + 44), (x + 164, y + 66)], fill=INK, width=2)
    draw.line([(x + 152, y + 46), (x + 152, y + 66)], fill=INK, width=2)
    # ocean waves (drawn before the capsule so the capsule sits on top)
    for wy in (y + h - 16, y + h - 8):
        draw.arc([x - 10, wy - 8, x + 60, wy + 8], 180, 360, fill=SEA, width=3)
        draw.arc([x + 70, wy - 8, x + 140, wy + 8], 180, 360, fill=SEA, width=3)
        draw.arc([x + 150, wy - 8, x + 220, wy + 8], 180, 360, fill=SEA, width=3)
        draw.arc([x + 230, wy - 8, x + 300, wy + 8], 180, 360, fill=SEA, width=3)
    # capsule
    draw.polygon([(x + 132, y + 66), (x + 172, y + 66), (x + 164, y + 88),
                  (x + 140, y + 88)], fill=(230, 230, 230), outline=INK, width=2)


PANELS = [
    ("CLIMATE \u2022 ANTALYA", "COP31 Talks Run Past Deadline",
     "Draft drops fossil-fuel phase-out and the $120bn fund.", illu_cop31),
    ("MIDDLE EAST", "Missiles Hit Saudi Power Plant",
     "Al-Shuqaiq plant burns; three missiles downed near Riyadh.", illu_saudi),
    ("CRICKET \u2022 WELLINGTON", "Rahul's Ton Makes SENA History",
     "First India opener with a Test hundred in all four SENA nations.",
     illu_cricket),
    ("LEBANON", "Lebanon Marks 83 Years Free",
     "President Aoun addresses the nation; Trump urges renewal.", illu_lebanon),
    ("FRANCE", "Yellow Vests March, Eight Years On",
     "70,000 police deployed; Paris march runs R\u00e9publique to Nation.",
     illu_vests),
    ("SPACE", "Dragon Splashes Down Off California",
     "6,000+ lb of research home, incl. 3D-printed blood vessels.",
     illu_dragon),
]


def draw_grid(draw):
    pw, ph, gap = 313, 224, 14
    for i, (kicker, headline, fact, illu) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = 28 + col * (pw + gap)
        y = 492 + row * (ph + gap)
        panel_frame(draw, x, y, pw, ph)
        illu(draw, x + 8, y + 8, pw - 16, 88)
        draw.text((x + 12, y + 104), kicker, font=font(SANS_B, 13),
                  fill=ACCENT_DARK)
        draw_wrapped(draw, headline, font(SERIF_B, 24), x + 12, y + 124, pw - 24)
        draw_wrapped(draw, fact, font(SANS, 16), x + 12, y + 182, pw - 24)


def draw_footer(draw):
    rule(draw, 28, 962, 996, 2)
    draw.text((512, 972),
              "Sources: USGS \u2022 COP31 presidency briefings \u2022 Saudi Press Agency "
              "\u2022 ICC / NZC match reports",
              font=font(SANS, 14), fill=INK_SOFT, anchor="ma")
    draw.text((512, 992),
              "Lebanese presidency \u2022 French Interior Ministry \u2022 NASA / SpaceX "
              "splashdown coverage",
              font=font(SANS, 14), fill=INK_SOFT, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    draw_grid(draw)
    draw_footer(draw)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
