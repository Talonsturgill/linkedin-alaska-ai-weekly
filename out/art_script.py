"""Anchorage Desk — 28 AUG 2026 — cover art.

Concept: a facial-landmark mesh builds from the left and halts at a gold
threshold rule labeled AO 2026-108. Landmarks beyond the rule are present
but unjoined. The capability exists; the connections are not authorized.
"""
import sys, math, random
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np
from scipy.spatial import Delaunay
from PIL import ImageFilter

import art_kit as ak
from art_kit import (Canvas, field, mottle, grain, vignette, line, circle,
                     poly, text, fraunces, mono, fit_size, chip, polaris,
                     gradient_v, measure, hex_to_rgb, mix)

SEED = 1108
random.seed(SEED)
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
GROUND   = "#0b0f24"
FIELD    = "#141a3a"
ORPHAN   = "#222d5e"
EDGE     = "#4a5f9e"
POINT    = "#b9c6e8"
TYPE     = "#eef1f7"
GOLD     = "#ffc72c"
PALETTE  = [GROUND, FIELD, ORPHAN, EDGE, POINT, TYPE, GOLD]

KICKER   = "ANCHORAGE DESK"
MIDDLE   = "MUNICIPAL"
DATESTR  = "28 AUG 2026"
HEADLINE = "Anchorage Writes AI Rules\nInto Police Code"

# ---------------------------------------------------------------- geometry
# Hand-authored dlib-style landmark topology in a unit face box.
JAW = [(0.02,0.34),(0.03,0.44),(0.05,0.54),(0.08,0.63),(0.12,0.72),
       (0.18,0.80),(0.26,0.87),(0.36,0.93),(0.50,0.955),(0.64,0.93),
       (0.74,0.87),(0.82,0.80),(0.88,0.72),(0.92,0.63),(0.95,0.54),
       (0.97,0.44),(0.98,0.34)]
BROW_L = [(0.13,0.26),(0.20,0.215),(0.29,0.205),(0.38,0.215),(0.46,0.245)]
BROW_R = [(0.54,0.245),(0.62,0.215),(0.71,0.205),(0.80,0.215),(0.87,0.26)]
NOSE_B = [(0.50,0.32),(0.50,0.40),(0.50,0.47),(0.50,0.54)]
NOSE_L = [(0.40,0.60),(0.45,0.62),(0.50,0.635),(0.55,0.62),(0.60,0.60)]
EYE_L  = [(0.19,0.35),(0.25,0.325),(0.32,0.325),(0.37,0.35),(0.32,0.375),(0.25,0.375)]
EYE_R  = [(0.63,0.35),(0.68,0.325),(0.75,0.325),(0.81,0.35),(0.75,0.375),(0.68,0.375)]
MOUTH_O = [(0.32,0.73),(0.38,0.705),(0.45,0.695),(0.50,0.705),(0.55,0.695),
           (0.62,0.705),(0.68,0.73),(0.62,0.775),(0.55,0.795),(0.50,0.80),
           (0.45,0.795),(0.38,0.775)]
MOUTH_I = [(0.36,0.73),(0.43,0.72),(0.50,0.725),(0.57,0.72),(0.64,0.73)]
CROWN  = [(0.10,0.16),(0.25,0.10),(0.42,0.07),(0.58,0.07),(0.75,0.10),(0.90,0.16)]

# face box on the 1080 grid
FX0, FY0, FW, FH = 250.0, 300.0, 590.0, 600.0
CUT_X = 620.0                      # the gold threshold rule
CUT_N = (CUT_X - FX0) / FW         # ~0.627 in face-box units


def place(p):
    """unit face-box coords -> design-space canvas coords"""
    return (FX0 + p[0] * FW, FY0 + p[1] * FH)


GROUPS = [("jaw", JAW, False), ("brow_l", BROW_L, False), ("brow_r", BROW_R, False),
          ("nose_b", NOSE_B, False), ("nose_l", NOSE_L, False),
          ("eye_l", EYE_L, True), ("eye_r", EYE_R, True),
          ("mouth_o", MOUTH_O, True), ("mouth_i", MOUTH_I, False),
          ("crown", CROWN, False)]

ALL_N = []            # unit coords
FEATURE_EDGES = []    # index pairs along feature chains
for _name, grp, closed in GROUPS:
    base = len(ALL_N)
    ALL_N.extend(grp)
    for i in range(len(grp) - 1):
        FEATURE_EDGES.append((base + i, base + i + 1))
    if closed:
        FEATURE_EDGES.append((base + len(grp) - 1, base))

PTS = [place(p) for p in ALL_N]
LEFT = [i for i, p in enumerate(ALL_N) if p[0] < CUT_N]
RIGHT = [i for i, p in enumerate(ALL_N) if p[0] >= CUT_N]

# Delaunay mesh fill, length-filtered so no edge spans the whole face
tri = Delaunay(np.array(PTS))
mesh = set()
for simplex in tri.simplices:
    for a, b in ((0, 1), (1, 2), (2, 0)):
        i, j = int(simplex[a]), int(simplex[b])
        if i > j:
            i, j = j, i
        d = math.dist(PTS[i], PTS[j])
        if d < 118.0:
            mesh.add((i, j))

# ---------------------------------------------------------------- canvas
c = Canvas(bg=GROUND, ss=2)

# ground: vertical gradient + noise mottle so nothing is a flat fill
gradient_v(c, (0, 0, 1080, 1080), FIELD, GROUND, ease=1.25)
mottle(c, strength=0.055, scale=3.2, seed=SEED)

# blueprint dot-grid substrate (deliberately regular, NOT a starfield)
for gy in range(30, 1080, 30):
    for gx in range(30, 1080, 30):
        major = (gx % 150 == 0) and (gy % 150 == 0)
        circle(c, gx, gy, 1.5 if major else 0.85,
               fill=mix(FIELD, POINT, 0.26 if major else 0.13))

# detection bounding brackets: what the system has framed
BX0, BY0, BX1, BY1 = 210.0, 306.0, 884.0, 946.0
for (cx, cy, sx, sy, bright) in ((BX0, BY0, 1, 1, True), (BX0, BY1, 1, -1, True),
                                 (BX1, BY0, -1, 1, False), (BX1, BY1, -1, -1, False)):
    col = mix(EDGE, POINT, 0.30) if bright else mix(ORPHAN, POINT, 0.26)
    line(c, [(cx, cy), (cx + sx * 46, cy)], col, width=1.7)
    line(c, [(cx, cy), (cx, cy + sy * 46)], col, width=1.7)

# ------------------------------------------------- orphan side (right of cut)
def dotted(p1, p2, color, width=1.3, dash=6.0, gap=7.0):
    (x1, y1), (x2, y2) = p1, p2
    d = math.dist(p1, p2)
    if d < 1e-6:
        return
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    t = 0.0
    while t < d:
        t2 = min(t + dash, d)
        line(c, [(x1 + ux * t, y1 + uy * t), (x1 + ux * t2, y1 + uy * t2)],
             color, width=width)
        t += dash + gap

# the connections that are NOT authorized: ghost edges among orphan points
GHOST = mix(ORPHAN, POINT, 0.30)
for (i, j) in sorted(mesh):
    if ALL_N[i][0] >= CUT_N and ALL_N[j][0] >= CUT_N:
        dotted(PTS[i], PTS[j], GHOST, width=1.15)
for (i, j) in FEATURE_EDGES:
    if ALL_N[i][0] >= CUT_N and ALL_N[j][0] >= CUT_N:
        dotted(PTS[i], PTS[j], mix(ORPHAN, POINT, 0.44), width=1.7)

# orphan landmarks: present, visible, unjoined
for i in RIGHT:
    x, y = PTS[i]
    circle(c, x, y, 5.6, fill=mix(GROUND, ORPHAN, 0.55))
    circle(c, x, y, 3.4, fill=mix(ORPHAN, POINT, 0.42))
    circle(c, x, y, 1.5, fill=mix(ORPHAN, POINT, 0.78))

# dashed "pending" stubs reaching right from the rule into the unmeshed half
for ty in (352, 430, 508, 596, 690, 782):
    dotted((CUT_X + 12, ty), (CUT_X + 82, ty), mix(ORPHAN, POINT, 0.34),
           width=1.5, dash=5.0, gap=6.0)

# ------------------------------------------------- mesh side (left of cut)
lay, ld = c.layer()
er = hex_to_rgb(EDGE)
for (i, j) in sorted(mesh):
    if ALL_N[i][0] < CUT_N and ALL_N[j][0] < CUT_N:
        (x1, y1), (x2, y2) = PTS[i], PTS[j]
        ld.line([c.s(x1), c.s(y1), c.s(x2), c.s(y2)], fill=(*er, 132),
                width=int(c.s(1.15)))
c.composite(lay)

# feature chains, brighter, so jaw/eye/mouth carry the read
for (i, j) in FEATURE_EDGES:
    if ALL_N[i][0] < CUT_N and ALL_N[j][0] < CUT_N:
        line(c, [PTS[i], PTS[j]], mix(EDGE, POINT, 0.55), width=2.0)

# landmark points
for i in LEFT:
    x, y = PTS[i]
    circle(c, x, y, 4.2, fill=mix(POINT, EDGE, 0.45))
    circle(c, x, y, 2.0, fill=POINT)

# ------------------------------------------------- the gold threshold rule
line(c, [(CUT_X, 296), (CUT_X, 946)], GOLD, width=3.0)
for ty in range(314, 946, 26):          # dimension ticks
    line(c, [(CUT_X - 6, ty), (CUT_X, ty)], GOLD, width=1.3)
circle(c, CUT_X, 296, 4.5, fill=GOLD)
circle(c, CUT_X, 946, 4.5, fill=GOLD)

# ------------------------------------------------- type
hl_lines = HEADLINE.split("\n")
hf_size = min(fit_size(c, l, 814, lo=30, hi=96, tracking=-0.005,
                       weight=900, opsz=144) for l in hl_lines)
hf = fraunces(c, hf_size, weight=900, opsz=144)
y = 104
for l in hl_lines:
    text(c, (86, y), l, hf, TYPE, anchor="la", tracking=-0.005)
    y += hf_size * 1.06

mf = mono(c, 16, medium=True)
text(c, (86, 252), f"{KICKER}  ·  {MIDDLE}  ·  {DATESTR}", mf,
     mix(GOLD, TYPE, 0.22), anchor="la", tracking=0.13)
line(c, [(86, 282), (300, 282)], mix(GOLD, GROUND, 0.62), width=1.6)

# rule labels, clear of the kicker line
chip(c, (CUT_X + 16, 304), "AO 2026-108", mono(c, 15, medium=True),
     GROUND, GOLD, pad=8, anchor="la", tracking=0.14, radius=4)
text(c, (CUT_X + 16, 920), "SEPT 1 HEARING", mono(c, 13),
     mix(ORPHAN, POINT, 0.62), anchor="la", tracking=0.18)

# ------------------------------------------------- brand marks
text(c, (86, 978), "ALASKA.AI", fraunces(c, 30, weight=900, opsz=144),
     TYPE, anchor="la", tracking=0.04)
polaris(c, 988, 118, r=12, color=GOLD, core="#fff0c8")

# ------------------------------------------------- finish
grain(c, amount=6.0, seed=SEED)
vignette(c, strength=0.22, spread=1.30)

c.finish("out/post_image.png", {
    "date": DATESTR,
    "column": "Anchorage Desk",
    "kicker": KICKER,
    "middle_slot": MIDDLE,
    "volume": MIDDLE,
    "byline": "",
    "headline": HEADLINE.replace("\n", " "),
    "style_family": "landmark_mesh",
    "palette": PALETTE,
    "hue_family": "indigo",
    "composition": "thirds_focal",
    "motifs": ["facial-landmark mesh", "gold threshold rule",
               "unjoined orphan landmarks", "dashed pending connections",
               "detection bounding brackets"],
    "technique_stack": ["delaunay_mesh", "dotted_ghost_edges", "dot_grid",
                        "gradient_v", "mottle", "grain", "vignette", "chip"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 7.4, "weakest": "typography",
         "note": "AO 2026-108 chip collided with the kicker and hid the date; orphan landmarks were too dark to see, so the right half read as empty and the metaphor failed"},
        {"iter": 2, "weighted": 8.53, "weakest": "detail",
         "note": "moved the rule and chip clear of the kicker, brightened orphan landmarks, added dotted ghost edges so the unauthorized half reads"}
    ],
    "eval_final": {"weighted": 8.83, "scores": {"concept": 9, "focal": 8.5,
        "composition": 8.5, "color": 9, "detail": 8.5, "craft": 9,
        "typography": 9, "originality": 9, "fidelity": 9.5}},
})
print("rendered out/post_image.png")
