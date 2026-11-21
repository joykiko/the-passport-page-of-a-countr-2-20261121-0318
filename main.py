#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Draws one invented passport spread (data page + visa/stamp page) for the
Republic of Talmar, a small Atlantic fishing republic that does not exist,
and writes it to /output/entry.png (1024x1024, <= 1 MiB).

Deterministic: fixed coordinates, no randomness, no network, stdlib + PIL
only. Running twice produces byte-identical output.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LIB_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    for base in (FONT_DIR, LIB_DIR):
        p = Path(base) / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)
ITALIC = lambda s: font("LiberationSans-Italic.ttf", s)

INK = (32, 38, 52)          # near-black blue ink
NAVY = (28, 52, 96)
GREY = (110, 108, 96)
PAGE = (246, 241, 227)      # cream passport paper
DESK = (56, 62, 72)         # dark slate desk
GOLD = (146, 110, 52)


# ---------------------------------------------------------------- MRZ
def _val(ch):
    if ch == "<":
        return 0
    if ch.isdigit():
        return int(ch)
    return ord(ch) - 55  # A=10 ... Z=35


def mrz_check(text):
    total = 0
    for i, ch in enumerate(text):
        total += _val(ch) * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<TLMVENN<<MARA<ILSA" + "<" * 24
    doc = "TLM004821"
    dob = "870314"   # 14 MAR 1987
    exp = "360601"   # 01 JUN 2036
    pers = "<" * 14
    c_doc = mrz_check(doc)
    c_dob = mrz_check(dob)
    c_exp = mrz_check(exp)
    c_pers = mrz_check(pers)
    composite = mrz_check(doc + c_doc + dob + c_dob + exp + c_exp + pers + c_pers)
    line2 = doc + c_doc + "TAL" + dob + c_dob + "F" + exp + c_exp + pers + c_pers + composite
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# ---------------------------------------------------------------- helpers
def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def wrap(draw, s, f, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def stamp(base, box, angle, colour, lines, size=13):
    """An ink entry/exit stamp, drawn on its own layer and rotated."""
    w, h = box[2] - box[0], box[3] - box[1]
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = layer.width // 2, layer.height // 2
    d.rounded_rectangle([20, 20, w + 20, h + 20], radius=8,
                        outline=colour + (235,), width=3)
    d.rounded_rectangle([26, 26, w + 14, h + 14], radius=5,
                        outline=colour + (200,), width=1)
    y = 20 + (h - len(lines) * (size + 5)) // 2 + 2
    for i, (s, f) in enumerate(lines):
        d.text((cx, y + i * (size + 5)), s, font=f, fill=colour + (235,),
               anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(layer, (box[0] - 20, box[1] - 20))


# ---------------------------------------------------------------- portrait
def draw_portrait(img, box):
    """Flat-style passport photograph of Mara Ilsa Venn, 38, of Port Anselm:
    dark bob, grey-blue sea light, navy jacket with a white collar.
    Drawn on its own layer so nothing spills past the photo frame."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (w, h), (168, 188, 205, 255))
    d = ImageDraw.Draw(layer)
    # faint guilloche arcs behind the head, clipped to the frame
    for r in range(30, 130, 16):
        d.arc([70 - r, 60 - r, 70 + r, 60 + r], 200, 340,
              fill=(140, 165, 190, 255), width=1)
    # shoulders / navy jacket
    d.pieslice([-30, h - 95, w + 30, h + 60], 180, 360, fill=(38, 58, 96, 255))
    # white collar
    d.polygon([(70, h - 62), (52, h - 28), (70, h - 12), (88, h - 28)],
              fill=(238, 236, 228, 255))
    # neck
    d.rectangle([62, h - 78, 78, h - 52], fill=(214, 178, 148, 255))
    # face
    d.ellipse([44, 34, 96, 116], fill=(222, 186, 156, 255))
    # dark bob hair: back mass + fringe
    d.pieslice([38, 22, 102, 108], 180, 360, fill=(52, 40, 34, 255))
    d.polygon([(40, 70), (44, 118), (52, 118), (50, 66)], fill=(52, 40, 34, 255))
    d.polygon([(100, 70), (96, 118), (88, 118), (90, 66)], fill=(52, 40, 34, 255))
    # brows, eyes, nose, mouth -- kept minimal, passport-photo plain
    d.line([54, 76, 63, 75], fill=(52, 40, 34, 255), width=2)
    d.line([77, 75, 86, 76], fill=(52, 40, 34, 255), width=2)
    d.line([55, 82, 62, 82], fill=(52, 40, 34, 255), width=2)
    d.line([78, 82, 85, 82], fill=(52, 40, 34, 255), width=2)
    d.line([70, 84, 69, 94], fill=(176, 138, 110, 255), width=2)
    d.line([62, 102, 78, 102], fill=(150, 90, 80, 255), width=2)
    # soft cheek light
    d.ellipse([48, 88, 58, 96], fill=(228, 196, 168, 255))
    d.ellipse([82, 88, 92, 96], fill=(228, 196, 168, 255))
    img.alpha_composite(layer, (x0, y0))


# ---------------------------------------------------------------- coat of arms
def draw_arms(draw, cx, top, scale=1.0):
    """Talmar arms: a shield, a lighthouse over three waves, one star."""
    w, h = int(64 * scale), int(76 * scale)
    x0, y0 = cx - w // 2, top
    x1, y1 = cx + w // 2, top + h
    draw.polygon([(x0, y0), (x1, y0), (x1, y0 + h - 18),
                  (cx, y1), (x0, y0 + h - 18)], outline=NAVY, width=3)
    draw.polygon([(x0 + 4, y0 + 4), (x1 - 4, y0 + 4), (x1 - 4, y0 + h - 20),
                  (cx, y1 - 4), (x0 + 4, y0 + h - 20)], outline=GOLD, width=1)
    # star
    sx, sy, r = cx, y0 + 14, 6
    draw.polygon([(sx, sy - r), (sx + 2, sy - 2), (sx + r, sy), (sx + 2, sy + 2),
                  (sx, sy + r), (sx - 2, sy + 2), (sx - r, sy), (sx - 2, sy - 2)],
                 fill=GOLD)
    # lighthouse
    draw.polygon([(cx - 6, y0 + 44), (cx - 4, y0 + 22), (cx + 4, y0 + 22),
                  (cx + 6, y0 + 44)], fill=NAVY)
    draw.rectangle([cx - 6, y0 + 18, cx + 6, y0 + 23], fill=NAVY)
    draw.line([cx - 12, y0 + 24, cx - 20, y0 + 18], fill=GOLD, width=2)
    draw.line([cx + 12, y0 + 24, cx + 20, y0 + 18], fill=GOLD, width=2)
    # three waves
    for i, wy in enumerate((y0 + 50, y0 + 58, y0 + 66)):
        draw.arc([x0 + 8, wy, x1 - 8, wy + 12], 180, 360,
                 fill=NAVY if i != 1 else GOLD, width=2)


# ---------------------------------------------------------------- data page
def data_page(img, draw):
    x0, y0, x1, y1 = 52, 140, 512, 884
    draw.rectangle([x0, y0, x1, y1], fill=PAGE)
    # faint guilloche
    for yy in range(y0 + 8, y1 - 8, 26):
        draw.line([x0 + 10, yy, x1 - 10, yy + 10], fill=(232, 226, 208), width=1)
    draw.rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], outline=(138, 127, 99), width=1)

    draw_arms(draw, 282, y0 + 22, scale=0.9)
    text(draw, (282, y0 + 108), "REPUBLIC OF TALMAR", SERIF_B(25), fill=NAVY, anchor="ma")
    text(draw, (282, y0 + 136), "R E P U B L I K A   T A L M A R", SANS(10), fill=GREY, anchor="ma")
    text(draw, (282, y0 + 156), "PASSPORT  •  PASPORTA", SANS_B(12), fill=INK, anchor="ma")
    draw.line([x0 + 40, y0 + 182, x1 - 40, y0 + 182], fill=NAVY, width=2)

    # photograph
    photo = (x0 + 26, y0 + 200, x0 + 166, y0 + 390)
    draw_portrait(img, photo)
    draw.rectangle(photo, outline=NAVY, width=2)
    text(draw, (photo[0] + 70, y0 + 398), "PHOTOGRAPH", SANS(8), fill=GREY, anchor="ma")

    fx = x0 + 186  # field column
    def field(y, label, value, vsize=15, lx=None):
        text(draw, (lx or fx, y), label, SANS(9), fill=GREY)
        text(draw, (lx or fx, y + 13), value, SANS_B(vsize), fill=INK)

    field(y0 + 200, "TYPE", "P")
    field(y0 + 200, "CODE / KODA", "TLM", lx=fx + 56)
    field(y0 + 200, "PASSPORT No. / BR.", "TLM 0048217", lx=fx + 126)
    field(y0 + 248, "SURNAME / PREZIME", "VENN")
    field(y0 + 296, "GIVEN NAMES / IMENA", "MARA ILSA")
    field(y0 + 344, "NATIONALITY / DRŽAVLJANSTVO", "TALMARIAN")
    field(y0 + 392, "DATE OF BIRTH / ROĐENJE", "14 MAR 1987")
    field(y0 + 392, "PLACE OF BIRTH / MJESTO", "PORT ANSELM", lx=fx + 130)
    field(y0 + 440, "SEX / SPOL", "F")
    field(y0 + 440, "DATE OF ISSUE", "02 JUN 2026", lx=fx + 64)
    field(y0 + 440, "DATE OF EXPIRY", "01 JUN 2036", vsize=12, lx=fx + 172)
    field(y0 + 488, "AUTHORITY / TIJELO", "PASSPORT OFFICE — PORT ANSELM", vsize=13)

    # signature
    draw.line([fx, y0 + 556, fx + 190, y0 + 556], fill=INK, width=1)
    # a quick hand: M. Venn in a single stroke-like polyline
    pts = [(fx + 8, y0 + 552), (fx + 16, y0 + 536), (fx + 24, y0 + 552),
           (fx + 32, y0 + 538), (fx + 40, y0 + 552), (fx + 52, y0 + 548),
           (fx + 60, y0 + 540), (fx + 72, y0 + 552), (fx + 84, y0 + 542),
           (fx + 96, y0 + 552), (fx + 118, y0 + 546), (fx + 150, y0 + 550)]
    draw.line(pts, fill=(40, 60, 120), width=2, joint="curve")
    text(draw, (fx, y0 + 562), "SIGNATURE OF BEARER / POTPIS", SANS(9), fill=GREY)

    # machine-readable zone
    l1, l2 = mrz_lines()
    draw.rectangle([x0 + 26, y0 + 620, x1 - 26, y0 + 686], fill=(238, 233, 216))
    text(draw, (x0 + 30, y0 + 626), l1, MONO(15), fill=INK)
    text(draw, (x0 + 30, y0 + 650), l2, MONO(15), fill=INK)
    text(draw, (x0 + 26, y1 - 30), "2", SANS(11), fill=GREY)


# ---------------------------------------------------------------- visa page
def visa_page(img, draw):
    x0, y0, x1, y1 = 512, 140, 972, 884
    draw.rectangle([x0, y0, x1, y1], fill=PAGE)
    for yy in range(y0 + 8, y1 - 8, 26):
        draw.line([x0 + 10, yy, x1 - 10, yy + 10], fill=(232, 226, 208), width=1)
    draw.rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], outline=(138, 127, 99), width=1)
    # dog-eared top corner: a worn, well-travelled passport
    draw.polygon([(x1 - 2, y0 + 2), (x1 - 34, y0 + 2), (x1 - 2, y0 + 34)],
                 fill=(214, 206, 184))
    draw.line([x1 - 34, y0 + 2, x1 - 2, y0 + 34], fill=(180, 170, 146), width=1)

    text(draw, ((x0 + x1) // 2, y0 + 26), "VISAS", SERIF_B(20), fill=NAVY, anchor="ma")
    text(draw, ((x0 + x1) // 2, y0 + 52), "VIZE  •  ENDORSEMENTS", SANS(10), fill=GREY, anchor="ma")
    draw.line([x0 + 40, y0 + 74, x1 - 40, y0 + 74], fill=NAVY, width=2)

    # --- Arvost visa sticker
    vx0, vy0, vx1, vy1 = x0 + 36, y0 + 92, x1 - 36, y0 + 236
    draw.rectangle([vx0, vy0, vx1, vy1], fill=(223, 231, 242))
    draw.rectangle([vx0, vy0, vx1, vy1], outline=NAVY, width=2)
    draw.rectangle([vx0 + 6, vy0 + 6, vx1 - 6, vy1 - 6], outline=NAVY, width=1)
    text(draw, (vx0 + 16, vy0 + 14), "KINGDOM OF ARVOST", SANS_B(14), fill=NAVY)
    text(draw, (vx1 - 16, vy0 + 14), "No. AV-221408", MONO(11), fill=NAVY, anchor="ra")
    text(draw, ((vx0 + vx1) // 2, vy0 + 40), "V I S A", SERIF_B(24), fill=NAVY, anchor="ma")
    text(draw, (vx0 + 16, vy0 + 76), "Single entry  •  30 days", SANS(12), fill=INK)
    text(draw, (vx0 + 16, vy0 + 94), "Valid  18 AUG 2026  to  17 SEP 2026", SANS(12), fill=INK)
    text(draw, (vx0 + 16, vy0 + 112), "Fee  40 TAL  —  PAID", SANS_B(12), fill=INK)
    # small consular seal
    cx, cy = vx1 - 44, vy0 + 100
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=NAVY, width=2)
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=NAVY, width=1)
    draw.polygon([(cx, cy - 9), (cx + 3, cy - 3), (cx + 9, cy), (cx + 3, cy + 3),
                  (cx, cy + 9), (cx - 3, cy + 3), (cx - 9, cy), (cx - 3, cy - 3)],
                 fill=NAVY)

    # --- stamps: a plausible trip, every date after issue 02 JUN 2026
    blue = (28, 78, 160)
    purple = (110, 60, 150)
    green = (28, 110, 70)
    red = (178, 44, 36)
    stamp(img, (x0 + 30, y0 + 258, x0 + 216, y0 + 348), -7, blue, [
        ("ARRIVED", SANS_B(13)), ("ARVOST", SANS_B(13)),
        ("PORT KESTREL", SANS(11)), ("18 AUG 2026", SANS_B(12))])
    stamp(img, (x0 + 234, y0 + 258, x0 + 420, y0 + 348), 5, purple, [
        ("DEPARTED", SANS_B(13)), ("ARVOST", SANS_B(13)),
        ("PORT KESTREL", SANS(11)), ("02 SEP 2026", SANS_B(12))])
    stamp(img, (x0 + 30, y0 + 366, x0 + 216, y0 + 456), 4, green, [
        ("ARRIVED", SANS_B(13)), ("SELKIRK", SANS_B(13)),
        ("HARBOUR GATE", SANS(11)), ("05 SEP 2026", SANS_B(12))])
    stamp(img, (x0 + 234, y0 + 366, x0 + 420, y0 + 456), -6, red, [
        ("DEPARTED", SANS_B(13)), ("SELKIRK", SANS_B(13)),
        ("HARBOUR GATE", SANS(11)), ("20 SEP 2026", SANS_B(12))])

    # --- the telling detail: a condition of entry that says what Talmar is
    bx0, by0, bx1, by1 = x0 + 36, y0 + 478, x1 - 36, y0 + 586
    draw.rectangle([bx0, by0, bx1, by1], outline=NAVY, width=2)
    draw.rectangle([bx0, by0, bx1, by0 + 24], fill=NAVY)
    text(draw, (bx0 + 10, by0 + 5), "CONDITION OF ENTRY  —  ART. 7, ALIENS ACT", SANS_B(11), fill=(246, 241, 227))
    cond = ("Employment prohibited. Fishing in Talmar territorial waters "
            "requires a permit from the Harbour Office, Port Anselm. "
            "Permits are stamped on page 14.")
    lines = wrap(draw, cond, SANS(12), bx1 - bx0 - 24)
    yy = by0 + 34
    for ln in lines:
        text(draw, (bx0 + 12, yy), ln, SANS(12), fill=INK)
        yy += 17

    # --- handwritten note in the margin: the human detail
    note = Image.new("RGBA", (420, 40), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.text((10, 8), "Mara — ring when you land. — E.", font=ITALIC(16),
            fill=(36, 70, 140, 235))
    note = note.rotate(-4, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(note, (x0 + 30, y0 + 604))

    # --- fee stamp, bottom right
    stamp(img, (x0 + 280, y0 + 622, x0 + 420, y0 + 676), 8, red, [
        ("FEE PAID", SANS_B(12)), ("25 TAL", SANS_B(13)),
        ("STAMP DUTY", SANS(10))], size=12)
    text(draw, (x0 + 30, y0 + 700),
         "This passport remains the property of the Republic of Talmar.",
         SANS(10), fill=GREY)
    text(draw, (x1 - 26, y1 - 30), "3", SANS(11), fill=GREY, anchor="ra")


# ---------------------------------------------------------------- main
def main():
    img = Image.new("RGBA", (W, H), DESK + (255,))
    draw = ImageDraw.Draw(img, "RGBA")
    # soft shadow under the spread
    draw.rounded_rectangle([62, 152, 982, 894], radius=4, fill=(30, 34, 40))
    data_page(img, draw)
    visa_page(img, draw)
    # centre gutter shadow
    for i in range(6):
        draw.line([512 - i, 140, 512 - i, 884], fill=(0, 0, 0, 10))
        draw.line([512 + i, 140, 512 + i, 884], fill=(0, 0, 0, 10))
    out = Path(os.environ.get("OUTPUT", "/output/entry.png"))
    if not out.parent.exists():
        out = Path("output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
