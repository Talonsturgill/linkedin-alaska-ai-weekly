"""The Stack — 28 AUG 2026 — "The Complete Application".

A municipal permit application seen close: every field satisfied and stamped
except one large open box marked for the electrical utility's statement of
system capacity. Inside that box, two poles with no span between them.

style_family: riso_form   composition: form_field_grid   hue_family: orange
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image
import art_kit as ak
from art_kit import (Canvas, poly, line, circle, hand_line, wobble_pts, chips,
                     stipple, hatch, halftone, grain, mottle, vignette,
                     gradient_v, field, warp, polaris, fraunces, mono, text,
                     measure, fit_size, mix, lighten, darken, hex_to_rgb)

SEED = 828
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
PAPER   = "#f0e6d2"   # L~0.92  sheet, and the focal void
DARK    = "#23190f"   # L~0.16  headline, rules, poles, labels
ORANGE  = "#e8501e"   # L~0.62  stamp blocks, accent  (only high-chroma ink)
GOLD    = "#c8912f"   # L~0.68  secondary ticks, punch rings
MID     = "#8a7355"   # L~0.55  hairline rules, faint interior grid

KICKER   = "THE STACK  ·  FACILITIES  ·  28 AUG 2026"
HEADLINE = ["NO STATEMENT,", "NO HEARING."]
WORDMARK = "ALASKA.AI"

c = Canvas(bg=PAPER, ss=2)

# ============================================================ 1. paper base
# raking light across the sheet, then mottle. never a flat fill.
gradient_v(c, (0, 0, 1080, 1080), lighten(PAPER, 0.05), darken(PAPER, 0.10),
           ease=1.15)
mottle(c, strength=0.045, scale=3.2, seed=SEED)

# faint fibre-direction wash so the paper reads as stock, not as canvas
f_paper = warp(field(scale=2.4, octaves=3, seed=SEED + 5), strength=40,
               scale=2.0, seed=SEED + 6)
lay, ld = c.layer()
for i in range(0, 1080, 6):
    v = float(np.mean(f_paper[min(1079, i), :]))
    if v > 0.52:
        ld.line([(0, c.s(i)), (c.W, c.s(i))],
                fill=(*hex_to_rgb(MID), 10), width=1)
c.composite(lay)

# ============================================ 2. punch perforations (margin)
for py in (470, 590, 710, 830, 950):
    circle(c, 52, py, 13, fill=darken(PAPER, 0.14))
    circle(c, 52, py, 13, outline=GOLD, width=2)
    # inner shadow arc, upper-left, so the hole has depth
    lay, ld = c.layer()
    ld.arc([c.s(52 - 13), c.s(py - 13), c.s(52 + 13), c.s(py + 13)],
           start=150, end=330, fill=(*hex_to_rgb(DARK), 70),
           width=max(1, int(c.s(2.2))))
    c.composite(lay)

# ================================================== 3-5. filled field rows
ROWS_TOP = [
    (448, "ZONING DISTRICT   I-1 / I-2 / I-3"),
    (504, "PEAK DEMAND   20 MW"),
    (560, "SETBACK   200 FT"),
    (616, "NOISE MITIGATION STUDY"),
    (672, "FIRE SUPPRESSION"),
]
ROWS_BOT = [
    (934, "WATER UTILITY STATEMENT"),
    (990, "WASTEWATER UTILITY STATEMENT"),
]
LABEL_X, BLOCK_X0, BLOCK_X1 = 128, 700, 968


def stamp_block(y, seed, satisfied=True):
    """An orange 'received/complete' stamp mass. Never a flat fill: it is
    a wobbled polygon, halftone-screened, hatched, then stippled."""
    h = 26
    box = [(BLOCK_X0, y - h / 2), (BLOCK_X1, y - h / 2),
           (BLOCK_X1, y + h / 2), (BLOCK_X0, y + h / 2)]
    box = wobble_pts(box, amp=1.6, scale=5.0, seed=seed)
    rot = rng.uniform(-0.7, 0.7)
    cx, cy = (BLOCK_X0 + BLOCK_X1) / 2, y
    r = math.radians(rot)
    box = [(cx + (px - cx) * math.cos(r) - (py - cy) * math.sin(r),
            cy + (px - cx) * math.sin(r) + (py - cy) * math.cos(r))
           for px, py in box]
    poly(c, box, fill=ORANGE)

    # meso: halftone screen + hatch inside the block only
    m = Image.new("L", (c.W, c.W), 0)
    from PIL import ImageDraw
    md = ImageDraw.Draw(m)
    md.polygon([(c.s(x), c.s(yy)) for x, yy in box], fill=255)
    fblk = field(scale=7.0, octaves=3, seed=seed + 11)
    halftone(c, fblk, cell=7.5, ink=darken(ORANGE, 0.30), angle=22.5,
             max_r=0.55,
             region=(BLOCK_X0 - 6, y - h / 2 - 4, BLOCK_X1 + 6, y + h / 2 + 4))
    hatch(c, m, spacing=7.0, angle=38.0, color=darken(ORANGE, 0.22), width=1.1)
    stipple(c, m, density=0.10, r=(0.5, 1.2), color=darken(ORANGE, 0.40),
            seed=seed + 3)
    return m


def field_row(y, label, seed):
    # hairline rule under the row
    hand_line(c, [(LABEL_X - 32, y + 20), (968, y + 20)], MID, width=1,
              amp=0.8, seed=seed + 1)
    # tiny tick marks along the rule (micro)
    for tx in range(LABEL_X - 24, 960, 34):
        line(c, [(tx, y + 20), (tx, y + 16)], MID, width=1)
    stamp_block(y, seed)
    text(c, (LABEL_X, y), label, mono(c, 17), DARK, anchor="lm",
         tracking=0.13)


for i, (y, lab) in enumerate(ROWS_TOP):
    field_row(y, lab, SEED + i * 17)
for i, (y, lab) in enumerate(ROWS_BOT):
    field_row(y, lab, SEED + 400 + i * 17)

# =========================================== 6. THE FOCAL — empty field box
BX0, BY0, BX1, BY1 = 96, 716, 984, 902

# interior stays bare paper (the lightest value on the canvas) but carries
# a faint ruled grid so it is never a flat fill
lay, ld = c.layer()
for gx in range(BX0 + 28, BX1, 28):
    ld.line([(c.s(gx), c.s(BY0 + 6)), (c.s(gx), c.s(BY1 - 6))],
            fill=(*hex_to_rgb(MID), 16), width=1)
for gy in range(BY0 + 24, BY1, 24):
    ld.line([(c.s(BX0 + 6), c.s(gy)), (c.s(BX1 - 6), c.s(gy))],
            fill=(*hex_to_rgb(MID), 16), width=1)
c.composite(lay)

# heavy deliberate border, hand-drawn so it never reads as an unfinished render
bpts = wobble_pts([(BX0, BY0), (BX1, BY0), (BX1, BY1), (BX0, BY1), (BX0, BY0)],
                  amp=1.5, scale=6.0, seed=SEED + 71)
hand_line(c, bpts, DARK, width=4, amp=1.0, seed=SEED + 72)

# corner ticks — the register marks that say "this blank is intentional"
T = 26
for (cx0, cy0, sx, sy) in ((BX0, BY0, 1, 1), (BX1, BY0, -1, 1),
                           (BX1, BY1, -1, -1), (BX0, BY1, 1, -1)):
    line(c, [(cx0 + sx * 10, cy0 + sy * 10), (cx0 + sx * T, cy0 + sy * 10)],
         ORANGE, width=3)
    line(c, [(cx0 + sx * 10, cy0 + sy * 10), (cx0 + sx * 10, cy0 + sy * T)],
         ORANGE, width=3)

text(c, (128, 740), "ELECTRICAL UTILITY STATEMENT", mono(c, 19, medium=True),
     DARK, anchor="lm", tracking=0.17)
text(c, (952, 740), "REQUIRED", mono(c, 15), ORANGE, anchor="rm",
     tracking=0.22)

# empty signature hairline
line(c, [(128, 878), (700, 878)], MID, width=2)
for tx in range(128, 700, 30):
    line(c, [(tx, 878), (tx, 874)], MID, width=1)

# ------------------------------------------------- 7. the unbuilt span
POLE_A, POLE_B = 372, 708
FOOT, ARM, TOP = 862, 792, 776


def pole(x, seed):
    hand_line(c, [(x, FOOT), (x, TOP)], DARK, width=6, amp=0.9, seed=seed)
    hand_line(c, [(x - 34, ARM), (x + 34, ARM)], DARK, width=5, amp=0.8,
              seed=seed + 1)
    # cross-brace
    line(c, [(x - 16, ARM + 16), (x, ARM + 2)], DARK, width=2)
    line(c, [(x + 16, ARM + 16), (x, ARM + 2)], DARK, width=2)
    # insulator nubs
    for ix in (x - 27, x + 27):
        circle(c, ix, ARM - 7, 5, fill=DARK)
        circle(c, ix, ARM - 7, 2, fill=PAPER)
    # ground shadow so the pole is planted, not floating
    lay, ld = c.layer()
    ld.ellipse([c.s(x - 22), c.s(FOOT - 4), c.s(x + 22), c.s(FOOT + 5)],
               fill=(*hex_to_rgb(DARK), 46))
    c.composite(lay)


pole(POLE_A, SEED + 90)
pole(POLE_B, SEED + 95)

# conductor stubs that run inward and simply stop — the gap IS the subject
GAP = 150
for x0, x1 in ((POLE_A + 27, 540 - GAP / 2), (540 + GAP / 2, POLE_B - 27)):
    hand_line(c, [(x0, ARM - 7), (x1, 800)], DARK, width=3, amp=1.1,
              seed=SEED + int(x0))
    circle(c, x1, 800, 4, fill=DARK)   # dead-end terminal

# a whisper of where the span would go, dotted, so the absence is legible
for dx in np.arange(540 - GAP / 2 + 12, 540 + GAP / 2 - 6, 13):
    line(c, [(dx, 800), (dx + 5, 800)], MID, width=2)

# ==================================================== 8. zone rule + header
hand_line(c, [(96, 400), (984, 400)], DARK, width=3, amp=1.2, seed=SEED + 44)
for tx in range(96, 985, 22):
    line(c, [(tx, 400), (tx, 394)], DARK, width=1)

# ========================================================= 9. type + marks
text(c, (96, 62), KICKER, mono(c, 15), DARK, anchor="lm", tracking=0.22)
polaris(c, 984, 62, r=13, color=GOLD, core=lighten(GOLD, 0.55))

hsize = min(fit_size(c, HEADLINE[0], 888, lo=60, hi=132, tracking=-0.012,
                     weight=900, opsz=144),
            fit_size(c, HEADLINE[1], 888, lo=60, hi=132, tracking=-0.012,
                     weight=900, opsz=144))
hf = fraunces(c, hsize, weight=900, opsz=144)
text(c, (96, 118), HEADLINE[0], hf, DARK, anchor="la", tracking=-0.012)
text(c, (96, 118 + hsize * 1.06), HEADLINE[1], hf, DARK, anchor="la",
     tracking=-0.012)

text(c, (96, 1042), WORDMARK, fraunces(c, 30, weight=900, opsz=144), DARK,
     anchor="lm", tracking=0.05)

# ============================================== 10. riso overprint pass
# re-print the orange stamp mass slightly off-register, low opacity. touches
# only the stamp band columns so it never crosses the headline or the poles.
lay, ld = c.layer()
for (y, _lab) in ROWS_TOP + ROWS_BOT:
    ld.rectangle([c.s(BLOCK_X0 + 2.2), c.s(y - 13 + 2.2),
                  c.s(BLOCK_X1 + 2.2), c.s(y + 13 + 2.2)],
                 fill=(*hex_to_rgb(ORANGE), 30))
c.composite(lay)

# ================================================= 11. micro finishing
chips(c, 260, (0, 0, 1080, 1080), size=(2, 5),
      colors=(darken(PAPER, 0.16), GOLD, darken(PAPER, 0.07)), seed=SEED + 12)
grain(c, amount=6.5, seed=SEED)
vignette(c, strength=0.14, spread=1.30)

META = {
    "date": "28 AUG 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "FACILITIES",
    "byline": "",
    "headline": "NO STATEMENT, NO HEARING.",
    "style_family": "riso_form",
    "palette": [PAPER, DARK, ORANGE, GOLD, MID],
    "hue_family": "orange",
    "composition": "form_field_grid",
    "motifs": ["permit application form", "unsigned field box",
               "two poles with no span", "stamp blocks",
               "punch perforations"],
    "technique_stack": ["gradient_v", "mottle", "poly", "wobble_pts",
                        "halftone", "hatch", "stipple", "hand_line",
                        "circle", "chips", "riso_overprint", "grain",
                        "vignette", "polaris"],
    "seed": SEED,
    "eval_history": [],
    "eval_final": {},
}

c.finish("out/post_image.png", META)
print("wrote out/post_image.png")
