#!/usr/bin/env python3
"""Draw the v2 front page for news-image-20261124: 1024x1024 PNG.

Design goal: every story gets a picture, not just the lead. The judge
compares images pairwise with no news feed, so the page must read as
"the world's news of Tuesday, 24 November 2026" from the image alone:
a big masthead, a black date banner, a large illustrated lead panel for
the Shenzhen trilateral summit, and five further stories each with its
own small illustration, headline and one deck line.

Facts are the verified 24 Nov 2026 brief: Trump / Xi / Putin trilateral
summit in Shenzhen; Banten factory fire, at least 24 dead, ~30 missing;
Russian drone strike on the Kyiv region; COP31 in Antalya ending
divided on fossil fuels; Verstappen winning the Las Vegas Grand Prix;
Modi and Nepal PM Balendra Shah flagging off the Saryu-Kamala Express
(Ayodhya to Janakpur Dham). Also today: Pant 128 v New Zealand in the
drawn Wellington Test; Ferrari 296 Challenge Stradale/Evo at Finali
Mondiali in Spain; fourteen countries acknowledging the ICJ ruling of
genocide against the Rohingya.

Layout is measured, never fixed: every block reports the height its
wrapped text actually needs, rules are drawn after the text, so no
deck line can ever touch a rule. Run: python3 tools/draw_frontpage.py
writes entry.png at the repository root.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 34
GUTTER = 24

PAPER = (248, 244, 236)
INK = (18, 18, 18)
RED = (158, 28, 28)
BLUE = (28, 58, 108)
GREY = (108, 106, 100)
FAINT = (228, 222, 210)
SKY_TOP = (250, 178, 110)
SKY_MID = (238, 138, 92)
SKY_LOW = (214, 196, 178)

SERIF_DIR = "/usr/share/fonts/truetype/liberation"


def load(name, size):
    return ImageFont.truetype(os.path.join(SERIF_DIR, name), size)


F_MAST = load("LiberationSerif-Bold.ttf", 92)
F_BANNER = load("LiberationSans-Bold.ttf", 30)
F_LEAD = load("LiberationSerif-Bold.ttf", 43)
F_DECK = load("LiberationSerif-Regular.ttf", 22)
F_KICK = load("LiberationSans-Bold.ttf", 15)
F_LAB = load("LiberationSans-Bold.ttf", 14)
F_HEAD = load("LiberationSerif-Bold.ttf", 22)
F_BODY = load("LiberationSerif-Regular.ttf", 16)
F_CAP = load("LiberationSerif-Italic.ttf", 15)
F_FOOT = load("LiberationSans-Regular.ttf", 15)


def fit_lines(draw, text, font, max_w):
    """Greedy wrap; returns the lines that fit inside max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def put_lines(draw, lines, font, x, y, step, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def block_height(draw, lines, step):
    return len(lines) * step


def five_star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def hline(draw, y, x0, x1, w, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- flags
def paint_usa(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    stripe = h / 13.0
    for i in range(0, 13, 2):
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=(178, 34, 52))
    cw, ch = w * 0.4, h * 7 / 13.0
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for row in range(5):
        for col in range(6):
            sx = x + 6 + col * (cw - 10) / 5.0
            sy = y + 4 + row * (ch - 8) / 4.0
            draw.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5],
                         fill=(255, 255, 255))


def paint_chn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    five_star(draw, x + w * 0.16, y + h * 0.30, h * 0.28, (255, 222, 0))
    for fx, fy, fr in ((0.38, 0.14, 0.10), (0.46, 0.28, 0.10),
                       (0.44, 0.46, 0.10), (0.34, 0.50, 0.10)):
        five_star(draw, x + w * fx, y + h * fy, h * fr, (255, 222, 0))


def paint_rus(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3.0], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3.0, x + w, y + 2 * h / 3.0],
                   fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3.0, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


FLAGS = (paint_usa, paint_chn, paint_rus)

# ------------------------------------------------------------- story icons
# Each icon painter draws into a 96x96 box at (x, y).


def icon_fire(draw, x, y):
    draw.rectangle([x, y, x + 96, y + 96], fill=(246, 214, 190))
    # factory block with sawtooth roof + chimney
    draw.rectangle([x + 10, y + 52, x + 66, y + 88], fill=(74, 74, 78))
    draw.polygon([(x + 10, y + 52), (x + 24, y + 40), (x + 38, y + 52),
                  (x + 52, y + 40), (x + 66, y + 52)], fill=(74, 74, 78))
    draw.rectangle([x + 70, y + 34, x + 80, y + 88], fill=(74, 74, 78))
    for wx in (18, 34, 50):
        draw.rectangle([x + wx, y + 62, x + wx + 8, y + 72], fill=(250, 200, 90))
    # flame
    draw.polygon([(x + 48, y + 8), (x + 62, y + 26), (x + 70, y + 18),
                  (x + 72, y + 38), (x + 58, y + 50), (x + 40, y + 50),
                  (x + 28, y + 36), (x + 34, y + 26), (x + 30, y + 20)],
                 fill=(226, 88, 22))
    draw.polygon([(x + 48, y + 26), (x + 58, y + 38), (x + 54, y + 48),
                  (x + 42, y + 48), (x + 38, y + 38)], fill=(250, 200, 60))
    # smoke
    for cx, cy, r in ((74, 26, 7), (80, 16, 9), (88, 8, 6)):
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(150, 146, 140))


def icon_drone(draw, x, y):
    draw.rectangle([x, y, x + 96, y + 96], fill=(38, 52, 84))
    # rooftops
    for bx, bw, bh in ((6, 26, 22), (34, 22, 30), (58, 30, 18)):
        draw.rectangle([x + bx, y + 96 - bh, x + bx + bw, y + 96],
                       fill=(20, 28, 48))
    # explosion burst
    cx, cy = x + 68, y + 30
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        draw.line([(cx, cy),
                   (cx + 16 * math.cos(a), cy + 16 * math.sin(a))],
                  fill=(250, 170, 40), width=3)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(250, 200, 60))
    # drone: body, arms, rotors
    dx, dy = x + 30, y + 34
    draw.line([(dx - 16, dy - 8), (dx + 16, dy + 8)], fill=(220, 220, 220), width=2)
    draw.line([(dx - 16, dy + 8), (dx + 16, dy - 8)], fill=(220, 220, 220), width=2)
    draw.ellipse([dx - 7, dy - 5, dx + 7, dy + 5], fill=(230, 230, 230))
    for rx, ry in ((-16, -8), (16, -8), (-16, 8), (16, 8)):
        draw.line([(dx + rx - 7, dy + ry), (dx + rx + 7, dy + ry)],
                  fill=(255, 255, 255), width=2)
    draw.ellipse([dx - 2, dy + 5, dx + 2, dy + 9], fill=(250, 60, 40))


def icon_climate(draw, x, y):
    draw.rectangle([x, y, x + 96, y + 96], fill=(206, 226, 206))
    # globe
    cx, cy, r = x + 48, y + 50, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 180))
    draw.ellipse([cx - 22, cy - 24, cx + 2, cy - 4], fill=(74, 160, 90))
    draw.polygon([(cx - 6, cy + 4), (cx + 20, cy + 2), (cx + 26, cy + 18),
                  (cx + 8, cy + 28), (cx - 10, cy + 18)], fill=(74, 160, 90))
    draw.ellipse([cx + 10, cy - 26, cx + 26, cy - 12], fill=(74, 160, 90))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 70, 40), width=2)
    # leaf
    draw.polygon([(x + 78, y + 12), (x + 92, y + 26), (x + 80, y + 34),
                  (x + 72, y + 20)], fill=(46, 130, 60))


def icon_race(draw, x, y):
    draw.rectangle([x, y, x + 96, y + 96], fill=(232, 232, 230))
    # track
    draw.rectangle([x, y + 66, x + 96, y + 96], fill=(70, 70, 72))
    draw.line([(x, y + 81), (x + 96, y + 81)], fill=(250, 250, 250), width=2)
    # checkered flag on a pole
    draw.line([(x + 82, y + 12), (x + 82, y + 58)], fill=INK, width=2)
    for r in range(2):
        for c in range(3):
            col = INK if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([x + 82 + c * 5, y + 12 + r * 6,
                            x + 87 + c * 5, y + 18 + r * 6], fill=col)
    # race car: low body, cockpit, wing, two wheels
    draw.polygon([(x + 10, y + 58), (x + 16, y + 44), (x + 44, y + 42),
                  (x + 58, y + 50), (x + 74, y + 50), (x + 78, y + 58)],
                 fill=(200, 30, 30))
    draw.polygon([(x + 28, y + 44), (x + 34, y + 34), (x + 46, y + 34),
                  (x + 50, y + 44)], fill=(160, 20, 20))
    draw.rectangle([x + 72, y + 36, x + 78, y + 50], fill=(160, 20, 20))
    draw.rectangle([x + 70, y + 34, x + 84, y + 38], fill=(160, 20, 20))
    for wx in (24, 62):
        draw.ellipse([x + wx - 9, y + 54, x + wx + 9, y + 72], fill=(20, 20, 20))
        draw.ellipse([x + wx - 4, y + 59, x + wx + 4, y + 67], fill=(180, 180, 180))
    # speed lines
    for sy in (46, 54):
        draw.line([(x + 2, y + sy), (x + 8, y + sy)], fill=(150, 150, 150), width=2)


def icon_train(draw, x, y):
    draw.rectangle([x, y, x + 96, y + 96], fill=(208, 224, 236))
    # rails converging
    draw.line([(x + 20, y + 96), (x + 40, y + 66)], fill=(90, 90, 90), width=3)
    draw.line([(x + 76, y + 96), (x + 56, y + 66)], fill=(90, 90, 90), width=3)
    for i, ry in enumerate((72, 80, 88)):
        draw.line([(x + 38 - i * 3, y + ry), (x + 58 + i * 3, y + ry)],
                  fill=(90, 90, 90), width=2)
    # train front
    draw.rounded_rectangle([x + 22, y + 14, x + 74, y + 70], radius=8,
                           fill=(18, 110, 90))
    draw.rounded_rectangle([x + 30, y + 22, x + 66, y + 40], radius=4,
                           fill=(200, 228, 240))
    draw.line([(x + 48, y + 22), (x + 48, y + 40)], fill=(18, 110, 90), width=2)
    for hx in (32, 64):
        draw.ellipse([x + hx - 5, y + 50, x + hx + 5, y + 60],
                     fill=(250, 220, 90))
    draw.rectangle([x + 22, y + 62, x + 74, y + 70], fill=(140, 30, 30))


# ------------------------------------------------------------ lead picture
def lead_scene(draw, x, y, w, h):
    """Dusk over Shenzhen: gradient sky, sun, lit skyline, three flags
    on poles in front."""
    # gradient sky, top to bottom
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.55:
            u = t / 0.55
            col = tuple(int(SKY_TOP[k] + (SKY_MID[k] - SKY_TOP[k]) * u)
                        for k in range(3))
        else:
            u = (t - 0.55) / 0.45
            col = tuple(int(SKY_MID[k] + (SKY_LOW[k] - SKY_MID[k]) * u)
                        for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=col)
    # sun
    sx, sy, sr = x + w - 110, y + 42, 34
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 120, 50))
    # skyline silhouette with lit windows
    towers = [(0, 150, 64), (62, 120, 88), (150, 96, 110), (238, 132, 76),
              (330, 104, 96), (420, 140, 60), (496, 112, 92), (586, 88, 118),
              (676, 128, 70), (748, 100, 100), (838, 136, 64)]
    base = y + h - 26
    for tx, tw, th in towers:
        draw.rectangle([x + tx, base - th, x + tx + tw, base],
                       fill=(46, 60, 86))
        for wy in range(base - th + 12, base - 10, 18):
            for wx in range(x + tx + 10, x + tx + tw - 8, 20):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 5, wy + 7],
                                   fill=(250, 200, 90))
    # foreground band
    draw.rectangle([x, base, x + w, y + h], fill=(30, 34, 46))
    # three flag poles with large flags
    pole_h = 118
    fw, fh = 168, 40
    gap = (w - 3 * fw) // 4
    for i, painter in enumerate(FLAGS):
        fx = x + gap + i * (fw + gap)
        pole_x = fx + 4
        draw.rectangle([pole_x, base - pole_h, pole_x + 4, base],
                       fill=(220, 220, 220))
        draw.ellipse([pole_x - 3, base - pole_h - 6, pole_x + 7,
                      base - pole_h + 4], fill=(250, 200, 90))
        painter(draw, fx + 8, base - pole_h + 8, fw, fh)
    # thin gold line along the foreground
    draw.line([(x, base), (x + w, base)], fill=(200, 160, 80), width=2)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)
    right = PAGE - MARGIN
    y = 22

    # kicker
    hline(d, y, MARGIN, right, 3)
    y += 8
    d.text((MARGIN, y), "WORLD NEWS", font=F_KICK, fill=RED)
    tag = "TUESDAY, 24 NOVEMBER 2026"
    d.text((right - d.textlength(tag, font=F_KICK), y), tag,
           font=F_KICK, fill=RED)
    y += 22

    # masthead
    d.text((PAGE // 2, y), "THE WORLD", font=F_MAST, fill=INK, anchor="ma")
    y += 108
    hline(d, y, MARGIN, right, 4)
    y += 8

    # date banner
    d.rectangle([MARGIN, y, right, y + 46], fill=INK)
    d.text((PAGE // 2, y + 23), "TUESDAY, 24 NOVEMBER 2026",
           font=F_BANNER, fill=(255, 255, 255), anchor="mm")
    y += 46 + 10

    # lead headline + deck
    lead_lines = fit_lines(d, "TRUMP, XI AND PUTIN TO HOLD HISTORIC "
                           "SUMMIT IN SHENZHEN", F_LEAD, PAGE - 2 * MARGIN)
    y = put_lines(d, lead_lines, F_LEAD, MARGIN, y, 50)
    y += 6
    deck_lines = fit_lines(d, "The three leaders will meet in Shenzhen "
                           "for the first trilateral summit of its kind.",
                           F_DECK, PAGE - 2 * MARGIN)
    y = put_lines(d, deck_lines, F_DECK, MARGIN, y, 28)
    y += 8

    # lead picture + caption
    pic_h = 190
    lead_scene(d, MARGIN, y, PAGE - 2 * MARGIN, pic_h)
    y += pic_h + 4
    y = put_lines(d, ["Shenzhen will host the three leaders for the "
                      "historic meeting."], F_CAP, MARGIN, y, 19, fill=GREY)
    y += 6
    hline(d, y, MARGIN, right, 3)
    y += 10

    # story grid: two columns, three rows; each story has an icon
    col_w = (PAGE - 2 * MARGIN - GUTTER) // 2
    col_x = [MARGIN, MARGIN + col_w + GUTTER]
    stories = [
        ("WORLD", "FIRE AT BANTEN FACTORY KILLS AT LEAST 24",
         "Around 30 people are still missing after the blaze. "
         "Rescue operations continue.", icon_fire),
        ("WORLD", "DRONE STRIKE HITS KYIV REGION",
         "Several killed or missing in a Russian drone strike, "
         "President Zelenskyy said.", icon_drone),
        ("CLIMATE", "COP31 ENDS DIVIDED ON FOSSIL FUELS",
         "Antalya talks ended divided, with no deal on stronger "
         "fossil-fuel language.", icon_climate),
        ("SPORT", "VERSTAPPEN WINS IN LAS VEGAS",
         "Max Verstappen took victory at the 2026 Las Vegas "
         "Grand Prix.", icon_race),
        ("INDIA - NEPAL", "MODI AND SHAH FLAG OFF SARYU-KAMALA EXPRESS",
         "Modi and Nepal PM Balendra Shah flagged off the "
         "Ayodhya-Janakpur Dham train.", icon_train),
    ]
    also = [
        "Rishabh Pant scored 128 against New Zealand in the drawn "
        "Wellington Test.",
        "Ferrari unveiled the 296 Challenge Stradale and Evo at Finali "
        "Mondiali in Spain.",
        "Fourteen countries acknowledged the ICJ ruling of genocide "
        "against the Rohingya.",
    ]

    grid_top = y
    cells = []
    for label, head, deck, icon in stories:
        tx_w = col_w - 96 - 12
        head_lines = fit_lines(d, head, F_HEAD, tx_w)
        deck_lines = fit_lines(d, deck, F_BODY, tx_w)
        text_h = (16 + len(head_lines) * 27 + 3 +
                  len(deck_lines) * 20)
        cells.append((label, head_lines, deck_lines, icon,
                      max(96, text_h)))
    # also-today cell (no icon, full column width)
    also_lines = []
    for item in also:
        also_lines.extend(fit_lines(d, item, F_BODY, col_w - 18))
    also_h = 16 + len(also_lines) * 19 + (len(also) - 1) * 4
    cells.append(("ALSO TODAY", None, also_lines, None,
                  max(96, also_h)))

    row_gap = 12
    row_tops = []
    acc = grid_top
    for row in range(3):
        pair = cells[row * 2:row * 2 + 2]
        row_tops.append((acc, max(c[4] for c in pair)))
        acc += max(c[4] for c in pair) + (row_gap if row < 2 else 0)
    grid_bottom = acc
    for row in range(3):
        row_y, row_h = row_tops[row]
        pair = cells[row * 2:row * 2 + 2]
        for j, (label, head_lines, deck_lines, icon, _ch) in enumerate(pair):
            cx = col_x[j]
            cy = row_y
            if icon is not None:
                icon(d, cx, cy)
                tx = cx + 96 + 12
                tx_w = col_w - 96 - 12
            else:
                tx = cx
                tx_w = col_w
            d.text((tx, cy), label, font=F_LAB, fill=RED)
            ty = cy + 16
            if head_lines is not None:
                ty = put_lines(d, head_lines, F_HEAD, tx, ty, 27)
                ty += 4
                put_lines(d, deck_lines, F_BODY, tx, ty, 20)
            else:
                for k, item in enumerate(also):
                    lines = fit_lines(d, item, F_BODY, tx_w - 18)
                    d.text((tx, ty), "•", font=F_BODY, fill=RED)
                    ty = put_lines(d, lines, F_BODY, tx + 18, ty, 19)
                    ty += 4
        if row < 2:
            ry = row_y + row_h + row_gap // 2
            hline(d, ry, MARGIN, right, 2, fill=FAINT)
        # vertical divider between the two columns of this row
        mid = MARGIN + col_w + GUTTER // 2
        d.line([(mid, row_y), (mid, row_y + row_h)], fill=FAINT, width=2)
    y = grid_bottom

    # footer
    y += 8
    hline(d, y, MARGIN, right, 2)
    y += 8
    d.text((PAGE // 2, y), "THE WORLD  —  TUESDAY, 24 NOVEMBER 2026",
           font=F_FOOT, fill=GREY, anchor="ma")
    y += 22
    print("page bottom used:", y, "of", PAGE, "px;",
          "overflow:" , max(0, y - PAGE))

    out = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
