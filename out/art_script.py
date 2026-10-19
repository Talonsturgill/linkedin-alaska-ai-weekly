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
import time as _t
_T0=_t.time()
def _stage(n): print("  [%6.1fs] %s"%(_t.time()-_T0,n), flush=True)
from art_kit import (Canvas, poly, line, circle, hand_line, wobble_pts, chips,
                     stipple, hatch, halftone, grain, mottle, vignette,
                     gradient_v, field, warp, polaris, fraunces, mono, text,
                     measure, fit_size, mix, lighten, darken, hex_to_rgb)


# --- perf: opensimplex at full 1080^2 costs ~40s per call. These textures are
# soft and low-frequency, so compute at reduced resolution and upscale. Visually
# identical here, roughly 20x faster, and it keeps the whole render under ~60s.
from scipy.ndimage import zoom as _zoom


def fast_field(scale=4.0, octaves=3, seed=0, res=256):
    f = ak.field(scale=scale, octaves=octaves, seed=seed, w=res, h=res)
    return np.clip(_zoom(f, 1080.0 / res, order=3), 0.0, 1.0)


def fast_warp(f, strength=40.0, scale=2.0, seed=1, res=192):
    """art_kit.warp builds two FULL-resolution noise fields (~80s together).
    Same domain warp, displacement fields computed cheaply."""
    h, w = f.shape
    dx = (fast_field(scale, 3, seed + 11, res=res)[:h, :w] - 0.5) * 2 * strength
    dy = (fast_field(scale, 3, seed + 29, res=res)[:h, :w] - 0.5) * 2 * strength
    ys, xs = np.mgrid[0:h, 0:w]
    xs = np.clip(xs + dx, 0, w - 1).astype(int)
    ys = np.clip(ys + dy, 0, h - 1).astype(int)
    return f[ys, xs]


SEED = 828
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
PAPER   = "#f0e6d2"   # L~0.92  sheet, and the focal void
DARK    = "#23190f"   # L~0.16  headline, rules, poles, labels
ORANGE  = "#e8501e"   # L~0.62  stamp blocks, accent  (only high-chroma ink)
GOLD    = "#c8912f"   # L~0.68  secondary ticks, punch rings
MID     = "#8a7355"   # L~0.55  hairline rules, faint interior grid
STAMP   = "#c2603a"   # muted orange for satisfied rows; the pure
                      # ORANGE is reserved for the focal box alone

KICKER   = "THE STACK  ·  FACILITIES  ·  28 AUG 2026"
HEADLINE = ["NO STATEMENT,", "NO HEARING."]
WORDMARK = "ALASKA.AI"

c = Canvas(bg=PAPER, ss=2)

_stage("paper base")
# ============================================================ 1. paper base
# raking light across the sheet, then mottle. never a flat fill.
gradient_v(c, (0, 0, 1080, 1080), lighten(PAPER, 0.05), darken(PAPER, 0.10),
           ease=1.15)
mottle(c, strength=0.045, scale=3.2, seed=SEED)

# faint fibre-direction wash so the paper reads as stock, not as canvas
f_paper = fast_warp(fast_field(scale=2.4, octaves=3, seed=SEED + 5, res=200),
                    strength=40, scale=2.0, seed=SEED + 6)
lay, ld = c.layer()
for i in range(0, 1080, 6):
    v = float(np.mean(f_paper[min(1079, i), :]))
    if v > 0.52:
        ld.line([(0, c.s(i)), (c.W, c.s(i))],
                fill=(*hex_to_rgb(MID), 10), width=1)
c.composite(lay)

_stage("perforations")
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
LABEL_X, BLOCK_X0, BLOCK_X1 = 128, 762, 968

# one shared screen field for every stamp block; each block reads a different
# region of it, so the blocks still differ without paying for 7 noise fields
F_STAMP = fast_field(scale=7.0, octaves=3, seed=SEED + 11, res=256)


def stamp_block(y, seed, wfrac=1.0):
    """An orange 'received/complete' stamp mass. Never a flat fill: it is
    a wobbled polygon, halftone-screened, hatched, then stippled."""
    h = 21
    x1 = BLOCK_X0 + (BLOCK_X1 - BLOCK_X0) * wfrac
    box = [(BLOCK_X0, y - h / 2), (x1, y - h / 2),
           (x1, y + h / 2), (BLOCK_X0, y + h / 2)]
    box = wobble_pts(box, amp=1.6, scale=5.0, seed=seed)
    rot = rng.uniform(-0.7, 0.7)
    cx, cy = (BLOCK_X0 + x1) / 2, y
    r = math.radians(rot)
    box = [(cx + (px - cx) * math.cos(r) - (py - cy) * math.sin(r),
            cy + (px - cx) * math.sin(r) + (py - cy) * math.cos(r))
           for px, py in box]
    poly(c, box, fill=STAMP)

    # meso: halftone screen + hatch inside the block only
    m = Image.new("L", (c.W, c.W), 0)
    from PIL import ImageDraw
    md = ImageDraw.Draw(m)
    md.polygon([(c.s(x), c.s(yy)) for x, yy in box], fill=255)
    halftone(c, F_STAMP, cell=7.5, ink=darken(STAMP, 0.30), angle=22.5,
             max_r=0.55,
             region=(BLOCK_X0 - 6, y - h / 2 - 4, x1 + 6, y + h / 2 + 4))
    hatch(c, m, spacing=7.0, angle=38.0, color=darken(STAMP, 0.22), width=1.1)
    stipple(c, m, density=0.10, r=(0.5, 1.2), color=darken(STAMP, 0.40),
            seed=seed + 3)
    return m


def field_row(y, label, seed, wfrac=1.0):
    # hairline rule under the row
    hand_line(c, [(LABEL_X - 32, y + 20), (968, y + 20)], MID, width=1,
              amp=0.8, seed=seed + 1)
    # tiny tick marks along the rule (micro)
    for tx in range(LABEL_X - 24, 960, 34):
        line(c, [(tx, y + 20), (tx, y + 16)], MID, width=1)
    stamp_block(y, seed, wfrac)
    text(c, (LABEL_X, y), label, mono(c, 17), DARK, anchor="lm",
         tracking=0.13)


_stage("field rows")
WFRACS_TOP = [1.00, 0.82, 0.70, 0.93, 0.61]
WFRACS_BOT = [0.88, 0.76]
for i, (y, lab) in enumerate(ROWS_TOP):
    field_row(y, lab, SEED + i * 17, WFRACS_TOP[i])
for i, (y, lab) in enumerate(ROWS_BOT):
    field_row(y, lab, SEED + 400 + i * 17, WFRACS_BOT[i])

_stage("focal box")
# =========================================== 6. THE FOCAL — empty field box
BX0, BY0, BX1, BY1 = 96, 716, 984, 902

# drop shadow so the box sits ON the sheet rather than being a hole cut in it
lay, ld = c.layer()
for k in range(10, 0, -1):
    ld.rectangle([c.s(BX0 + 3 + k * 0.5), c.s(BY0 + 4 + k * 0.7),
                  c.s(BX1 + 3 + k * 0.5), c.s(BY1 + 4 + k * 0.7)],
                 fill=(*hex_to_rgb(DARK), 4))
c.composite(lay)

# THE VALUE LIFT: the void is painted brighter than the surrounding stock, so
# it wins the contrast war outright instead of merely tying with it.
lay, ld = c.layer()
ld.rectangle([c.s(BX0), c.s(BY0), c.s(BX1), c.s(BY1)],
             fill=(*hex_to_rgb(lighten(PAPER, 0.55)), 232))
c.composite(lay)

# interior carries a visible ruled grid so it is never a flat fill
lay, ld = c.layer()
for gx in range(BX0 + 28, BX1, 28):
    ld.line([(c.s(gx), c.s(BY0 + 6)), (c.s(gx), c.s(BY1 - 6))],
            fill=(*hex_to_rgb(MID), 34), width=1)
for gy in range(BY0 + 24, BY1, 24):
    ld.line([(c.s(BX0 + 6), c.s(gy)), (c.s(BX1 - 6), c.s(gy))],
            fill=(*hex_to_rgb(MID), 34), width=1)
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

# empty signature and date fields — the blank that is still waiting
line(c, [(128, 866), (612, 866)], MID, width=2)
for tx in range(128, 612, 30):
    line(c, [(tx, 866), (tx, 862)], MID, width=1)
text(c, (128, 880), "AUTHORIZED SIGNATURE", mono(c, 11), MID, anchor="lm",
     tracking=0.20)
line(c, [(668, 866), (952, 866)], MID, width=2)
for tx in range(668, 952, 30):
    line(c, [(tx, 866), (tx, 862)], MID, width=1)
text(c, (668, 880), "DATE", mono(c, 11), MID, anchor="lm", tracking=0.20)

_stage("unbuilt span")
# ------------------------------------------------- 7. the unbuilt span
POLE_A, POLE_B = 372, 708
FOOT, ARM, TOP = 850, 784, 768


def pole(x, seed, inward):
    """A drafted distribution pole. inward = +1 if its conductor runs right."""
    hand_line(c, [(x, FOOT), (x, TOP)], DARK, width=7, amp=0.7, seed=seed)
    # two crossarms, the upper one carrying the dead-ended conductor
    hand_line(c, [(x - 40, ARM), (x + 40, ARM)], DARK, width=6, amp=0.6,
              seed=seed + 1)
    hand_line(c, [(x - 27, ARM + 26), (x + 27, ARM + 26)], DARK, width=4,
              amp=0.6, seed=seed + 2)
    # knee braces, drafted symmetrically
    for sgn in (-1, 1):
        line(c, [(x + sgn * 30, ARM + 3), (x + sgn * 5, ARM + 27)], DARK,
             width=3)
    # insulator caps on the upper arm
    for ix in (x - 31, x, x + 31):
        circle(c, ix, ARM - 8, 6, fill=DARK)
        circle(c, ix, ARM - 10, 2.4, fill=lighten(PAPER, 0.5))
    # guy wire down to an anchor, away from the gap
    gx = x - inward * 52
    line(c, [(x, TOP + 12), (gx, FOOT - 2)], DARK, width=2)
    line(c, [(gx - 7, FOOT - 2), (gx + 7, FOOT - 2)], DARK, width=3)
    # ground shadow so the pole is planted, not floating
    lay, ld = c.layer()
    ld.ellipse([c.s(x - 22), c.s(FOOT - 4), c.s(x + 22), c.s(FOOT + 5)],
               fill=(*hex_to_rgb(DARK), 46))
    c.composite(lay)


pole(POLE_A, SEED + 90, +1)
pole(POLE_B, SEED + 95, -1)

# conductor stubs that run inward and simply stop — the gap IS the subject
GAP = 168
CY = ARM - 8

# feeder lines arriving from off-form, through each pole, so the grid reads as
# continuous everywhere except the one span that was never built
for xa, xb in ((BX0 + 14, POLE_A - 31), (POLE_B + 31, BX1 - 14)):
    hand_line(c, [(xa, CY), (xb, CY)], DARK, width=4, amp=0.5,
              seed=SEED + int(xa) + 3)
    # intermediate suspension insulators along the arriving spans
    for t in (0.34, 0.68):
        ix = xa + (xb - xa) * t
        circle(c, ix, CY, 3.4, fill=DARK)
        line(c, [(ix, CY - 3), (ix, CY - 11)], DARK, width=2)
for x0, x1 in ((POLE_A + 31, 540 - GAP / 2), (540 + GAP / 2, POLE_B - 31)):
    hand_line(c, [(x0, CY), (x1, CY)], DARK, width=4, amp=0.5,
              seed=SEED + int(x0))
    # dead-end: a bell insulator and a short curled tail, drafted
    circle(c, x1, CY, 5.5, fill=DARK)
    tail = -8 if x1 < 540 else 8
    line(c, [(x1, CY), (x1 + tail, CY + 13)], DARK, width=2)

# a whisper of where the span would go, dotted, so the absence is legible
for dx in np.arange(540 - GAP / 2 + 11, 540 + GAP / 2 - 6, 14):
    line(c, [(dx, CY), (dx + 6, CY)], ORANGE, width=3)

_stage("zone rule")
# ==================================================== 8. zone rule + header
hand_line(c, [(96, 400), (984, 400)], DARK, width=3, amp=1.2, seed=SEED + 44)
for tx in range(96, 985, 22):
    line(c, [(tx, 400), (tx, 394)], DARK, width=1)

_stage("type")
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

_stage("riso overprint")
# ============================================== 10. riso overprint pass
# re-print the orange stamp mass slightly off-register, low opacity. touches
# only the stamp band columns so it never crosses the headline or the poles.
lay, ld = c.layer()
_span = BLOCK_X1 - BLOCK_X0
for (y, _lab), wf in zip(ROWS_TOP + ROWS_BOT, WFRACS_TOP + WFRACS_BOT):
    ld.rectangle([c.s(BLOCK_X0 + 2.2), c.s(y - 10.5 + 2.2),
                  c.s(BLOCK_X0 + _span * wf + 2.2), c.s(y + 10.5 + 2.2)],
                 fill=(*hex_to_rgb(STAMP), 26))
c.composite(lay)

_stage("micro finishing")
# ================================================= 11. micro finishing
chips(c, 70, (0, 0, 1080, 300), size=(2, 4),
      colors=(darken(PAPER, 0.13), darken(PAPER, 0.06)), seed=SEED + 12)
chips(c, 26, (300, 1012, 1080, 1074), size=(2, 3),
      colors=(darken(PAPER, 0.11),), seed=SEED + 13)
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
    "eval_history": [
        {"iter": 1, "weighted": 7.48, "weakest": "focal hierarchy",
         "fix": "seven identical high-chroma orange bars out-shouted the empty "
                "box; the box was the same paper tone as the sheet so it never "
                "lifted"},
        {"iter": 2, "weighted": 8.12, "weakest": "craft",
         "fix": "riso overprint ignored the new varied bar widths, leaving a "
                "pink tail past every stamp that read as a bug"},
        {"iter": 3, "weighted": 8.31, "weakest": "detail",
         "fix": "signature fields crowded the box border and empty acreage "
                "flanked the poles"},
        {"iter": 4, "weighted": 8.76, "weakest": "craft",
         "fix": "conductor line crowded the field label and the REQUIRED tick"},
        {"iter": 5, "weighted": 8.81, "weakest": "focal hierarchy",
         "fix": "shipped"},
    ],
    "eval_final": {
        "weighted": 8.81,
        "scores": {"concept": 9.5, "focal": 8.5, "composition": 8.5,
                   "color": 8.5, "detail": 8.5, "craft": 8.5,
                   "typography": 9.0, "originality": 9.0, "fidelity": 9.5},
        "bar": "weighted >= 8.5 with no dimension below 7 — met",
        "dedup_clearance": {
            "style_family": "riso_form — riso absent from the visible ledger; "
                            "clears the last-8 cooldown",
            "hue_family": "orange — last used 31 JUL (Desk), 6 issues back; "
                          "green/neutral-cool/violet/blue were forbidden",
            "composition": "form_field_grid — never used",
            "motif_note": "literal gates and valves were BANNED to this piece: "
                          "gate/valve motifs appear in 4 of the last 10 issues "
                          "(stop-log headworks, crest gates, series valves, "
                          "gate iris). A form field and an unbuilt span reach "
                          "the same idea by a fresh route.",
        },
    },
}

_stage("finish")
c.finish("out/post_image.png", META)
print("wrote out/post_image.png")
