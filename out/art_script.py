#!/usr/bin/env python3
"""The Stack — 2026-07-08 cover art.
Concept "One Desk": a Swiss modular grid of dim offer/parcel cells, one
gold-lit AFICA source-selection cell where the go/no-go lands, with the
three installations labeled and bankable power (a transmission glyph) the
pass/fail variable inside the one lit cell."""

import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as K

SEED = 708

# ---- palette (value spine: dark ground -> slate cells -> steel -> gold -> paper)
GROUND   = "#10141b"
CELL_DIM = "#232c39"
CELL_ID  = "#33404f"
STEEL    = "#6b7d92"
GOLD     = "#f4b13c"
PAPER    = "#f3ead6"
SEAM     = "#0b0e14"
INK_ON_GOLD = "#241a0c"

c = K.Canvas(bg=GROUND, ss=2, size=1080)

# ---- 1. ground depth gradient + paper life ---------------------------
K.gradient_v(c, (0, 0, 1080, 1080), "#141a24", "#0d1116", ease=1.1)
K.mottle(c, strength=0.05, scale=3.0, seed=SEED + 1)

# faint ground texture field (very low contrast) via stipple on a soft mask
gm, gmd = c.mask()
gmd.rectangle([0, 0, c.W, c.W], fill=26)
K.stipple(c, gm, density=0.02, r=(0.5, 1.2), color="#1b2331", seed=SEED + 2)

# ---- grid geometry ---------------------------------------------------
GX0, GY0, GX1, GY1 = 96, 360, 984, 930
COLS, ROWS, GUT = 6, 5, 16
CW = (GX1 - GX0 - (COLS - 1) * GUT) / COLS
CH = (GY1 - GY0 - (ROWS - 1) * GUT) / ROWS

def cell_xy(col, row):
    return GX0 + col * (CW + GUT), GY0 + row * (CH + GUT)

FOCAL = (3, 1)
BASES = {(1, 0): "JBER", (5, 2): "EIELSON", (2, 4): "CLEAR"}
RANKS = {(0, 2): "07", (4, 0): "12", (2, 1): "23", (5, 4): "31", (0, 4): "18"}

def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# collect a mask of all dim cells for one cheap stipple texture pass
dim_mask, dmd = c.mask()

# ---- 2. dim offer/parcel cells (with meso schematic content) ---------
for row in range(ROWS):
    # atmospheric: lower rows sink slightly toward the ground
    fill = K.mix(CELL_DIM, GROUND, 0.10 + 0.06 * row)
    ledger = K.mix(fill, STEEL, 0.32)
    inner = K.mix(fill, STEEL, 0.16)
    for col in range(COLS):
        if (col, row) == FOCAL or (col, row) in BASES:
            continue
        x, y = cell_xy(col, row)
        K.poly(c, rect(x, y, x + CW, y + CH), fill=fill,
               outline=SEAM, width=2)
        dmd.rectangle([c.s(x), c.s(y), c.s(x + CW), c.s(y + CH)], fill=255)
        # inner parcel rect
        ix0, iy0, ix1, iy1 = x + 15, y + 14, x + CW - 15, y + CH - 26
        K.poly(c, rect(ix0, iy0, ix1, iy1), outline=inner, width=1)
        # two faint ledger lines (an offer row + a score bar)
        K.line(c, [(x + 15, y + CH - 17), (x + CW - 34, y + CH - 17)],
               ledger, width=2)
        frac = 0.30 + 0.14 * ((col * 2 + row * 3) % 5)
        K.line(c, [(x + 15, y + CH - 9),
                   (x + 15 + (CW - 49) * frac, y + CH - 9)],
               K.mix(fill, STEEL, 0.5), width=3)
        # a scattered rank number gives the field scoresheet DNA
        if (col, row) in RANKS:
            K.text(c, (x + CW - 20, y + 20), RANKS[(col, row)],
                   K.mono(c, 12), K.mix(fill, STEEL, 0.55),
                   anchor="mm", tracking=0.05)

# one cheap texture pass over all dim cells
K.stipple(c, dim_mask, density=0.05, r=(0.5, 1.3), color="#33404f",
          seed=SEED + 3)

# ---- 3. identified base cells ----------------------------------------
for (col, row), label in BASES.items():
    x, y = cell_xy(col, row)
    K.poly(c, rect(x, y, x + CW, y + CH), fill=CELL_ID, outline=SEAM, width=2)
    # inner frame
    K.poly(c, rect(x + 13, y + 13, x + CW - 13, y + CH - 13),
           outline=K.mix(CELL_ID, STEEL, 0.35), width=1)
    K.text(c, (x + CW / 2, y + CH / 2 - 6), label, K.mono(c, 15, medium=True),
           PAPER, anchor="mm", tracking=0.14)
    K.text(c, (x + CW / 2, y + CH / 2 + 16), "OFFEROR",
           K.mono(c, 8), STEEL, anchor="mm", tracking=0.30)

# ---- 4. focal gold cell (the AFICA source-selection desk) ------------
fcol, frow = FOCAL
fx, fy = cell_xy(fcol, frow)
E = 22  # break the grid: enlarge the focal
fx0, fy0, fx1, fy1 = fx - E, fy - E, fx + CW + E, fy + CH + E
fcx, fcy = (fx0 + fx1) / 2, (fy0 + fy1) / 2

# glow behind (warm light pool spilling onto neighbors)
K.glow(c, fcx, fcy, 190, GOLD, alpha=74)
K.glow(c, fcx, fcy, 104, K.lighten(GOLD, 0.28), alpha=58)

# cell body
K.poly(c, rect(fx0, fy0, fx1, fy1), fill=GOLD, outline=K.darken(GOLD, 0.32),
       width=3)
# subtle inner top highlight (not a hard white bar)
K.line(c, [(fx0 + 10, fy0 + 7), (fx1 - 10, fy0 + 7)],
       K.lighten(GOLD, 0.18), width=2)

# corner label AFICA (the controlling actor)
K.text(c, (fx0 + 14, fy0 + 13), "AFICA", K.mono(c, 12, medium=True),
       INK_ON_GOLD, anchor="la", tracking=0.22)

# transmission-tower glyph (bankable power = the pass/fail variable)
tx = fx0 + (fx1 - fx0) * 0.35
tbase, ttop = fy1 - 26, fy0 + 34
lb, rb = tx - 24, tx + 24       # leg base half-width
lt, rt = tx - 7, tx + 7         # waist half-width
K.line(c, [(lb, tbase), (lt, ttop)], INK_ON_GOLD, width=4)   # left rail
K.line(c, [(rb, tbase), (rt, ttop)], INK_ON_GOLD, width=4)   # right rail
K.line(c, [(lb, tbase), (rb, tbase)], INK_ON_GOLD, width=4)  # ground sill
# horizontal cross members + X bracing between them
levels = [tbase, (tbase * 2 + ttop) / 3, (tbase + ttop * 2) / 3, ttop]
def railx(y, side):
    t = (tbase - y) / (tbase - ttop)
    return (lb + (lt - lb) * t) if side < 0 else (rb + (rt - rb) * t)
for i in range(len(levels) - 1):
    y_a, y_b = levels[i], levels[i + 1]
    K.line(c, [(railx(y_a, -1), y_a), (railx(y_a, 1), y_a)], INK_ON_GOLD, width=2)
    K.line(c, [(railx(y_a, -1), y_a), (railx(y_b, 1), y_b)], INK_ON_GOLD, width=2)
    K.line(c, [(railx(y_a, 1), y_a), (railx(y_b, -1), y_b)], INK_ON_GOLD, width=2)
# two crossarms with insulator ticks
for ay, aw in [(ttop + 6, 26), (ttop + 20, 19)]:
    K.line(c, [(tx - aw, ay), (tx + aw, ay)], INK_ON_GOLD, width=4)
    K.line(c, [(tx - aw, ay), (tx - aw, ay + 6)], INK_ON_GOLD, width=2)
    K.line(c, [(tx + aw, ay), (tx + aw, ay + 6)], INK_ON_GOLD, width=2)
K.line(c, [(tx, ttop), (tx, ttop - 7)], INK_ON_GOLD, width=3)  # mast tip

# the binary decision: a bold check (go)
chx, chy = fx1 - 42, fy0 + 42
K.line(c, [(chx - 11, chy), (chx - 2, chy + 13)], INK_ON_GOLD, width=6)
K.line(c, [(chx - 2, chy + 13), (chx + 17, chy - 13)], INK_ON_GOLD, width=6)

# solicitation number along the bottom inner edge
K.text(c, (fcx, fy1 - 13), "AFCEC-26-R-0006", K.mono(c, 11, medium=True),
       INK_ON_GOLD, anchor="mm", tracking=0.14)

# ---- 5. subtle Alaska ridge between grid and footer ------------------
# far ridge (lighter, atmospheric) then near ridge (darker) -> horizon read
far = K.ridge_pts(950, 20, scale=3.2, octaves=4, seed=SEED + 5,
                  x0=96, x1=984, step=6)
far = [(96, 972)] + far + [(984, 972)]
K.poly(c, far, fill="#212b3a")
near = K.ridge_pts(958, 14, scale=5.5, octaves=4, seed=SEED + 7,
                   x0=96, x1=984, step=6)
near = [(96, 972)] + near + [(984, 972)]
K.poly(c, near, fill="#161d29")

# ---- 6. headline (Swiss, knocked out of the dark) --------------------
HW = 806
hsize = K.fit_size(c, "GATES ALASKA’S AI", HW, lo=48, hi=118,
                   weight=900, opsz=144)
hf = K.fraunces(c, hsize, weight=900, opsz=144)
lead = hsize * 1.04
K.text(c, (96, 84), "ONE FEDERAL DESK", hf, PAPER, anchor="la")
K.text(c, (96, 84 + lead), "GATES ALASKA’S AI", hf, PAPER, anchor="la")

# kicker (mono telemetry)
K.text(c, (98, 90 + 2 * lead + 8), "THE STACK · VEHICLES · 8 JUL 2026",
       K.mono(c, 18), STEEL, anchor="la", tracking=0.22)

# ---- 7. marks --------------------------------------------------------
K.text(c, (96, 986), "ALASKA.AI", K.fraunces(c, 30, weight=900, opsz=40),
       PAPER, anchor="la", tracking=0.02)
K.polaris(c, 984, 96, r=13, color=GOLD, core=K.lighten(GOLD, 0.4), halo=1.7)

# ---- 8. finish -------------------------------------------------------
K.vignette(c, strength=0.14, spread=1.4)
K.grain(c, amount=6.0, seed=SEED + 9)

meta = {
    "date": "8 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "VEHICLES",
    "headline": "One Federal Desk Gates Alaska's AI",
    "byline": "",
    "style_family": "swiss_grid",
    "palette": [GROUND, CELL_DIM, CELL_ID, STEEL, GOLD, PAPER],
    "hue_family": "neutral-cool",
    "composition": "modular_grid",
    "motifs": ["modular offer grid", "single lit source-selection cell",
               "transmission-tower glyph", "go/no-go check",
               "base labels JBER EIELSON CLEAR"],
    "technique_stack": ["gradient_v", "gradient_r", "glow", "mottle",
                        "stipple", "ridge_pts", "grain", "vignette"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 8.52,
         "weakest": "focal/craft (white sheen-strip artifact on the gold "
                    "cell, ambiguous tower glyph, orphan bottom bar)"},
        {"iter": 2, "weighted": 8.94,
         "weakest": "detail (cells uniform by Swiss design; acceptable)"}
    ],
    "eval_final": {
        "weighted": 8.94,
        "scores": {"concept": 9, "focal": 9, "composition": 9, "color": 9,
                   "detail": 8.5, "craft": 9, "typography": 9,
                   "originality": 9, "fidelity": 9},
        "notes": "Fixed the sheen-strip artifact, redrew the transmission "
                 "tower as a clear lattice with crossarms, added scattered "
                 "rank numbers for scoresheet DNA, and turned the bottom "
                 "bar into a subtle double-ridge horizon. No dimension "
                 "below 7; ships above the 8.5 floor."
    },
}
c.finish("out/post_image.png", meta)
print("wrote out/post_image.png")
