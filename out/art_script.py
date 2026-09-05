"""Anchorage Desk — 4 SEP 2026 — cover art.

Concept: a drafted connection that does not touch the thing it claims to
touch. An annotated section of Cook Inlet. The Cook Inlet PowerLink cable
lies solid and continuous on the seabed. A dashed red feeder runs out from
DeepGreen's server hive field toward it and simply terminates in open water.
A drafting dimension measures the distance it never closed.

Style family: halftone_section (halftone_pop x blueprint annotation grammar).
Composition: horizon_band. Hue family: red.
Iteration 2. Iter 1 failed on Concept (the spur arced over the cable and read
as a crossing, not a gap) and Craft (two soft_panel blur smudges).
"""
import math
import sys

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np  # noqa: E402
import art_kit as ak  # noqa: E402

SEED = 4192

# --------------------------------------------------- palette (paper + 5)
PAPER = "#efe7d8"
WATER = "#6f7378"   # halftone ink for the water column
SEABED = "#2f3236"
INK = "#17191c"
HIVE = "#9aa0a6"
RED = "#c02a1f"
GOLD = "#ffc72c"    # polaris colophon only, not a compositional ink

PALETTE = [PAPER, WATER, SEABED, INK, HIVE, RED]

# derived tints, not separate inks
AIR_D = ak.darken(PAPER, 0.06)
WATER_L = ak.mix(PAPER, SEABED, 0.30)
LAND = ak.mix(INK, PAPER, 0.26)

# ------------------------------------------------------------- geometry
WATERLINE = 300.0
BED_TOP = 900.0
FEEDER_Y = 742.0        # the claimed feeder run, in open water
FEEDER_END = 596.0      # where it simply stops
GAP_X = 596.0
MOUND_CX = 838.0

ak.ensure_fonts()
c = ak.Canvas(bg=PAPER, ss=2)
rng = np.random.default_rng(SEED)


def bed_y(x):
    return BED_TOP + 13.0 * math.sin(x / 190.0) + 6.0 * math.sin(x / 61.0)


def cable_y(x):
    return bed_y(x) - 15.0


# --------------------------------------------------------- 1. air + sea
ak.gradient_v(c, (0, 0, 1080, WATERLINE), PAPER, AIR_D, ease=1.7)
ak.gradient_v(c, (0, WATERLINE, 1080, BED_TOP + 30), WATER_L,
              ak.mix(WATER_L, SEABED, 0.62), ease=1.10)

# --------------------------------------------- 2. halftone water column
noise = ak.warp(ak.field(scale=3.0, octaves=5, seed=SEED), strength=54.0,
                scale=2.2, seed=SEED + 1)
rows = np.arange(1080, dtype=float)
depth = np.clip((rows - WATERLINE) / (BED_TOP - WATERLINE), 0.0, 1.0)
bands = 0.5 + 0.5 * np.sin(rows / 26.0)          # current striation, meso
f_water = np.clip(0.06 + 0.50 * depth[:, None]
                  + 0.17 * (noise - 0.5)
                  + 0.07 * bands[:, None] * depth[:, None], 0, 1)
ak.halftone(c, f_water, cell=8.0, ink=WATER, angle=17.0, max_r=0.56,
            region=(0, WATERLINE + 2, 1080, BED_TOP + 26))

# suspended particulate, micro
wmask, wd = c.mask()
wd.rectangle(c.pts([(0, WATERLINE), (1080, BED_TOP)]), fill=255)
ak.stipple(c, wmask, density=0.012, r=(0.6, 1.7),
           color=ak.lighten(WATER, 0.30), seed=SEED + 9)

# slow current striations, meso structure through the open water
for i in range(11):
    yy = 336.0 + i * 46.0
    pts = [(x, yy + 13 * math.sin(x / 210.0 + i * 0.7)
            + 5 * math.sin(x / 63.0 + i)) for x in range(-10, 1092, 14)]
    ak.line(c, pts, ak.mix(WATER_L, WATER, 0.22 + 0.05 * i), width=1)

# ---------------------------------------------- 3. Nikiski shore + water
land = [(-10, WATERLINE)]
for x in range(0, 452, 12):
    land.append((x, 285 - 9 * math.sin(x / 128.0) - 4 * math.sin(x / 33.0)))
land += [(452, WATERLINE), (-10, WATERLINE)]
ak.poly(c, land, fill=LAND)
for tx, tr in ((208, 11), (250, 9)):
    ty = 278 - 9 * math.sin(tx / 128.0)
    ak.poly(c, [(tx - tr, ty), (tx + tr, ty), (tx + tr, ty + 16),
                (tx - tr, ty + 16)], fill=ak.darken(LAND, 0.24))
ak.text(c, (470, 276), "NIKISKI", ak.mono(c, 12),
        ak.mix(INK, PAPER, 0.50), anchor="la", tracking=0.20)
wl = ak.wobble_pts([(x, WATERLINE) for x in range(-10, 1092, 16)],
                   amp=2.2, scale=9.0, seed=SEED + 2)
ak.line(c, wl, ak.mix(INK, WATER_L, 0.40), width=2)

# survey vessel at the surface
vx = 806.0
ak.poly(c, [(vx - 44, 300), (vx + 44, 300), (vx + 34, 282), (vx - 30, 282)],
        fill=ak.mix(INK, PAPER, 0.20))
ak.poly(c, [(vx - 14, 282), (vx + 12, 282), (vx + 12, 266), (vx - 14, 266)],
        fill=ak.mix(INK, PAPER, 0.20))
ak.line(c, [(vx + 6, 266), (vx + 6, 246)], ak.mix(INK, PAPER, 0.20), width=2)

# ------------------------------------------------ 4. depth scale, left
mono_xs = ak.mono(c, 12)
for d_m, yy in ((0, WATERLINE), (40, 490), (80, 680), (120, 868)):
    ak.line(c, [(66, yy), (90, yy)], ak.mix(INK, WATER_L, 0.42), width=2)
    ak.text(c, (66, yy + 6), f"{d_m} M", mono_xs,
            ak.mix(INK, WATER_L, 0.46), anchor="la", tracking=0.16)
ak.line(c, [(66, WATERLINE), (66, 868)], ak.mix(INK, WATER_L, 0.55), width=1)

# ------------------------------------------------------- 5. tidal rotors
for i, (tx, hy, rr) in enumerate(((196.0, 566.0, 62.0), (330.0, 632.0, 52.0),
                                  (452.0, 690.0, 43.0), (556.0, 738.0, 35.0))):
    by = bed_y(tx)
    col = ak.mix(INK, WATER_L, 0.26 + i * 0.09)
    ak.poly(c, [(tx - 11, by), (tx + 11, by), (tx + 5, hy), (tx - 5, hy)],
            fill=col)
    ak.poly(c, [(tx - 26, by), (tx + 26, by), (tx + 20, by - 12),
                (tx - 20, by - 12)], fill=ak.darken(col, 0.14))
    for k in range(3):
        a = math.radians(-90 + k * 120 + i * 26)
        ak.line(c, [(tx, hy), (tx + math.cos(a) * rr, hy + math.sin(a) * rr)],
                col, width=max(3, int(rr / 11)))
    ak.circle(c, tx, hy, rr * 0.13, fill=ak.darken(col, 0.24))

# --------------------------------------------------------- 6. seabed band
bed = [(x, bed_y(x)) for x in range(-10, 1092, 10)]
ak.poly(c, bed + [(1092, 1090), (-10, 1090)], fill=SEABED)
bedmask, bd = c.mask()
bd.polygon(c.pts(bed + [(1092, 1090), (-10, 1090)]), fill=255)
for cell in ak.voronoi_polys(n=130, seed=SEED + 4,
                             bbox=(-20, BED_TOP - 30, 1100, 1090), relax=1):
    v = float(rng.uniform(-0.07, 0.07))
    ak.poly(c, cell, fill=(ak.lighten(SEABED, v) if v > 0
                           else ak.darken(SEABED, -v)),
            outline=ak.darken(SEABED, 0.12), width=1)
ak.stipple(c, bedmask, density=0.05, r=(0.7, 1.9),
           color=ak.lighten(SEABED, 0.18), seed=SEED + 5)
ak.chips(c, 80, (0, BED_TOP - 20, 1080, 1080), size=(3, 8),
         colors=(ak.lighten(SEABED, 0.24), ak.darken(SEABED, 0.16)),
         seed=SEED + 6, mask_img=bedmask)

# ------------------------------------------- 7. the PowerLink cable (real)
cab = [(x, cable_y(x)) for x in range(40, 1046, 8)]
ak.line(c, cab, ak.lighten(INK, 0.50), width=13)
ak.line(c, cab, INK, width=9)
ak.line(c, [(x, y - 3.4) for x, y in cab], ak.lighten(INK, 0.72), width=3)
for ax in (150.0, 470.0, 596.0, 900.0):
    ay = cable_y(ax)
    ak.poly(c, [(ax - 14, ay - 13), (ax + 14, ay - 13),
                (ax + 11, ay + 14), (ax - 11, ay + 14)],
            fill=ak.darken(INK, 0.06), outline=ak.lighten(INK, 0.38), width=1)

# ------------------------------------------------- 8. DeepGreen hive field
hexes = []
for row in range(4):
    n = 9 - row * 2
    for i in range(n):
        hexes.append((MOUND_CX + (i - (n - 1) / 2.0) * 34.0,
                      bed_y(MOUND_CX) - 16.0 - row * 27.0, row))
for hx, hy, row in hexes:
    r = 17.0
    pts = [(hx + math.cos(math.radians(60 * k - 30)) * r,
            hy + math.sin(math.radians(60 * k - 30)) * r * 0.84)
           for k in range(6)]
    ak.poly(c, pts, fill=ak.lighten(HIVE, 0.04 * row),
            outline=ak.darken(HIVE, 0.42), width=2)
    ak.poly(c, [(hx - 8, hy - 5), (hx + 8, hy - 5), (hx + 8, hy - 1),
                (hx - 8, hy - 1)], fill=ak.darken(HIVE, 0.30))
    if row >= 2:
        ak.circle(c, hx + 6, hy + 5, 2.0, fill=ak.lighten(HIVE, 0.45))

# --------------------------------- 9. the claimed feeder, and the gap
riser_x = MOUND_CX - 68.0
top_hive_y = bed_y(MOUND_CX) - 16.0 - 3 * 27.0
run = [(riser_x, top_hive_y - 6), (riser_x, FEEDER_Y), (FEEDER_END, FEEDER_Y)]
# dashed, hand-drawn: this line exists only on paper
pathpts = []
for a, b in zip(run[:-1], run[1:]):
    n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 9.0) + 1
    pathpts += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
                for i in range(n)]
pathpts.append(run[-1])
for i in range(0, len(pathpts) - 1, 2):
    ak.line(c, [pathpts[i], pathpts[i + 1]], RED, width=5)
ak.circle(c, FEEDER_END, FEEDER_Y, 8.0, outline=RED, width=4)

# the dimension that never closed. focal point.
gy0, gy1 = FEEDER_Y + 12.0, cable_y(GAP_X) - 15.0
ak.line(c, [(GAP_X, gy0), (GAP_X, gy1)], RED, width=3)
for yy, s in ((gy0, 1), (gy1, -1)):
    ak.poly(c, [(GAP_X, yy), (GAP_X - 8, yy + 15 * s), (GAP_X + 8, yy + 15 * s)],
            fill=RED)
    ak.line(c, [(GAP_X - 26, yy), (GAP_X + 26, yy)], RED, width=3)
mono_lbl = ak.mono(c, 17, medium=True)
ak.chip(c, (GAP_X + 40, (gy0 + gy1) / 2 - 12), "NO TIE-IN", mono_lbl,
        PAPER, RED, pad=9, anchor="la", tracking=0.20, radius=4)

# blueprint callouts, both traceable to the dossier
mono_c = ak.mono(c, 13)
ak.text(c, (150, cable_y(150) + 40), "COOK INLET POWERLINK  ·  $400M",
        mono_c, ak.lighten(SEABED, 0.78), anchor="la", tracking=0.18)
ak.text(c, (MOUND_CX, top_hive_y - 48), "DEEPGREEN  ·  100 MW  ·  PROPOSED",
        mono_c, ak.lighten(WATER_L, 0.55), anchor="ma", tracking=0.18)

# ------------------------------------------------------- 10. typography
h1, h2 = "AEA Never Got the Call", "The Filing Said Otherwise"
size = min(ak.fit_size(c, h1, 610, hi=112, weight=900, opsz=144),
           ak.fit_size(c, h2, 610, hi=112, weight=900, opsz=144))
fh = ak.fraunces(c, size, weight=900, opsz=144)
ak.text(c, (84, 74), h1, fh, INK, anchor="la")
ak.text(c, (84, 74 + size * 1.06), h2, fh, ak.mix(INK, PAPER, 0.30),
        anchor="la")
kick = ak.mono(c, 16)
ky = 84 + size * 2.22
ak.line(c, [(86, ky - 14), (620, ky - 14)], ak.mix(INK, PAPER, 0.62), width=1)
ak.text(c, (86, ky), "ANCHORAGE DESK · OPERATOR · 4 SEP 2026", kick,
        ak.mix(INK, PAPER, 0.28), anchor="la", tracking=0.22)
ital = ak.fraunces(c, 21, weight=500, italic=True)
ak.text(c, (86, ky + 30), "decisions, not biographies", ital,
        ak.mix(INK, PAPER, 0.44), anchor="la")

wm = ak.fraunces(c, 32, weight=900, opsz=144)
ak.text(c, (84, 1000), "ALASKA.AI", wm, PAPER, anchor="la", tracking=0.06)
ak.polaris(c, 990, 92, r=13, color=GOLD)

# ------------------------------------------------------- 11. finishing
ak.mottle(c, strength=0.032, scale=3.0, seed=SEED + 7)
ak.grain(c, amount=6.0, seed=SEED + 8)
ak.vignette(c, strength=0.12, spread=1.42)

c.finish("out/post_image.png", {
    "date": "4 SEP 2026",
    "column": "Anchorage Desk",
    "kicker": "ANCHORAGE DESK",
    "middle_slot": "OPERATOR",
    "byline": "",
    "headline": "AEA Never Got the Call / The Filing Said Otherwise",
    "style_family": "halftone_section",
    "palette": PALETTE,
    "hue_family": "red",
    "composition": "horizon_band",
    "motifs": ["annotated water-column section", "seabed transmission cable",
               "server hive field", "dashed feeder terminating in open water",
               "the dimension that never closed", "tidal rotor rank"],
    "technique_stack": ["gradient_v", "field", "warp", "halftone",
                        "voronoi_polys", "wobble_pts", "stipple", "chips",
                        "chip", "mottle", "grain", "vignette"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 5.6, "weakest": "concept",
         "note": "spur arced over the cable and read as a crossing; two "
                 "soft_panel blur smudges; flat water acreage"}
        {"iter": 2, "weighted": 7.1, "weakest": "detail",
         "note": "gap read correctly, but motto collided with the shore, "
                 "labels ran dark-on-dark, depth scale sat inside the edge "
                 "margin, and the upper water was empty acreage"}
    ],
    "eval_final": {},
})
print("rendered out/post_image.png")
