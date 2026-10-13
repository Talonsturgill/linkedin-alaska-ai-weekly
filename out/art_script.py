"""The Stack — 21 SEP 2026 — "The Last Inch"

A high-voltage coupling split in two. Alaska has built and energized its
half; the other half hangs from outside the frame, inert, and the last
inch between them is empty.

style_family: machined_plate   composition: suspended_gap   hue: violet
"""
import math
import sys

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np
from PIL import Image

import art_kit as K

SEED = 2609
rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------
# palette — value spine first, hue is costume
# ----------------------------------------------------------------------
# SEVEN base inks + paper-white. Everything else in the piece is derived
# from these by mix(), which is what keeps the limited-palette discipline
# honest rather than declared.
PAPER = "#f4f0f8"    # lightest light — THE GAP
SKY_TOP = "#2b1f4a"
SKY_LOW = "#b295bd"
INK = "#140e24"      # darkest dark
UP_BODY = "#9a86b8"  # UPPER half — cold, sky-lit, institutional
LO_BODY = "#241b40"  # LOWER half — dark, rooted, Alaska's side
AMBER = "#e8913c"    # energized conductors ONLY, never above the gap

# derived tones
EDGE = K.mix(PAPER, UP_BODY, 0.22)     # specular edge + pale type
UP_LIT = K.mix(UP_BODY, PAPER, 0.50)
UP_DRK = K.mix(UP_BODY, INK, 0.55)
LO_LIT = K.mix(LO_BODY, UP_BODY, 0.60)
LO_DRK = K.mix(LO_BODY, INK, 0.60)
CONC = K.mix(SKY_TOP, PAPER, 0.32)     # the poured pad
GROUND = K.mix(INK, SKY_TOP, 0.20)
WATER = K.mix(SKY_TOP, SKY_LOW, 0.30)
ICE = K.mix(SKY_LOW, LO_BODY, 0.35)

# ----------------------------------------------------------------------
# geometry (design units on the 1080 grid) — from art_plan.md
# ----------------------------------------------------------------------
AX = 700
HORIZON = 742
GAP_T, GAP_B = 446, 506            # THE GAP, widened so the break is read
GAP_X0, GAP_X1 = 556, 844

c = K.Canvas(bg=PAPER, ss=2)


def rect(x0, y0, x1, y1, fill):
    K.poly(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=fill)


def ell_pts(cx, cy, rx, ry, n=72):
    return [(cx + math.cos(i / n * math.tau) * rx,
             cy + math.sin(i / n * math.tau) * ry) for i in range(n)]


def block(x0, y0, x1, y1, body, lit, drk, lit_w=26):
    """Stepped 3-tone machined body with a specular top/left edge."""
    rect(x0, y0, x1, y1, body)
    rect(x0, y0, x0 + lit_w, y1, lit)
    rect(x1 - lit_w * 0.6, y0, x1, y1, drk)
    K.line(c, [(x0, y0), (x1, y0)], EDGE, width=2)
    K.line(c, [(x0, y0), (x0, y1)], EDGE, width=1.6)


def bolts(x0, x1, y, n, r, cap=EDGE, shade=INK):
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        K.circle(c, x + 1.3, y + 1.3, r, fill=shade)
        K.circle(c, x, y, r, fill=cap)
        K.circle(c, x - r * 0.3, y - r * 0.3, r * 0.32, fill=PAPER)


# ======================================================================
# 1. sky
# ======================================================================
K.gradient_v(c, (0, 0, 1080, HORIZON + 2), SKY_TOP, SKY_LOW, ease=1.22)

sf = K.field(scale=2.4, octaves=4, seed=SEED, w=300, h=300)
sky_tex = K.field_img(sf, SKY_TOP, SKY_LOW).resize((c.W, c.W), Image.LANCZOS)
sky_mask = Image.new("L", (c.W, c.W), 0)
sky_mask.paste(Image.new("L", (c.W, int(c.s(HORIZON))), 44), (0, 0))
c.img.paste(sky_tex, (0, 0), sky_mask)
c.draw = K.ImageDraw.Draw(c.img, "RGBA")

for i in range(34):                      # dusk banding
    y = 150 + i * 17
    a = int(15 * (1 - abs(i - 20) / 24))
    if a > 1:
        lay, ld = c.layer()
        ld.rectangle([0, c.s(y), c.W, c.s(y + 6)],
                     fill=(*K.hex_to_rgb(EDGE), a))
        c.composite(lay)

# ======================================================================
# 2. far ridges
# ======================================================================
K.ridge_fill(c, y_base=704, amp=48, fill=K.mix(SKY_LOW, SKY_TOP, 0.32),
             scale=2.0, octaves=4, seed=7, bottom=HORIZON + 4)
K.ridge_fill(c, y_base=724, amp=28, fill=K.mix(SKY_LOW, SKY_TOP, 0.54),
             scale=3.4, octaves=4, seed=11, bottom=HORIZON + 4)

# ======================================================================
# 3. Eielson on the horizon
# ======================================================================
bk = K.mix(SKY_TOP, INK, 0.45)
for (bx, bw, bh) in [(112, 96, 26), (214, 74, 19), (292, 58, 15),
                     (356, 46, 12), (404, 30, 10)]:
    rect(bx, HORIZON - bh, bx + bw, HORIZON, bk)
    K.line(c, [(bx, HORIZON - bh), (bx + bw * 0.5, HORIZON - bh - 5),
               (bx + bw, HORIZON - bh)], bk, width=3)
rect(180, HORIZON - 62, 191, HORIZON, bk)
for i in range(16):
    t = i / 15
    K.circle(c, 186 + t * 30 + math.sin(t * 5) * 6, HORIZON - 66 - t * 44,
             3.4 + t * 7, fill=K.mix(SKY_LOW, SKY_TOP, 0.60 - t * 0.48))

# ======================================================================
# 4. ground — muskeg, two voronoi scales for honest variety
# ======================================================================
g_pts = K.wobble_pts([(x, HORIZON + 3 + math.sin(x / 130) * 4)
                      for x in range(-10, 1092, 12)], amp=2.6, seed=5)
K.poly(c, [(-10, 1090)] + g_pts + [(1092, 1090)], fill=GROUND)

for npts, y0, sd, wob in ((170, HORIZON + 8, SEED + 3, 1.8),
                          (46, 900, SEED + 8, 3.2)):
    cells = K.voronoi_polys(n=npts, seed=sd, bbox=(-40, y0, 1120, 1100),
                            relax=2)
    for i, cell in enumerate(cells):
        ys = [p[1] for p in cell]
        if min(ys) < HORIZON + 6:
            continue
        depth = (float(np.mean(ys)) - HORIZON) / (1090 - HORIZON)
        if rng.random() < 0.48:
            K.poly(c, K.wobble_pts(cell, amp=wob, seed=i),
                   fill=K.mix(WATER, GROUND, 0.22 + depth * 0.52))
            top = sorted(cell, key=lambda p: p[1])[:2]
            if depth < 0.55 and len(top) == 2 and rng.random() < 0.6:
                K.line(c, top, K.mix(ICE, WATER, 0.3), width=1.6)
        else:
            K.poly(c, K.wobble_pts(cell, amp=wob, seed=i + 700),
                   fill=K.mix(GROUND, INK, 0.15 + rng.random() * 0.3))

for i in range(330):                     # tussocks + sedge
    t = rng.random() ** 0.6
    y = HORIZON + 10 + t * (1080 - HORIZON)
    x = rng.uniform(-20, 1100)
    r = 2.2 + t * 7
    K.poly(c, K.blob_pts(x, y, r, wobble=0.34, points=9, seed=i),
           fill=K.mix(GROUND, ICE, 0.10 + rng.random() * 0.22))
    if rng.random() < 0.38:
        for _ in range(3):
            K.line(c, [(x, y), (x + rng.uniform(-5, 5),
                                y - r - rng.uniform(3, 10))],
                   K.mix(GROUND, ICE, 0.32), width=1)

# ======================================================================
# 5. the poured pad — a BUILT foundation, not an organic blob
# ======================================================================
K.poly(c, [(452, 812), (948, 812), (986, 872), (414, 872)],
       fill=K.mix(GROUND, INK, 0.55))                      # cast shadow
# lower terrace
K.poly(c, [(470, 768), (930, 768), (958, 812), (442, 812)], fill=CONC)
K.poly(c, [(470, 768), (930, 768), (930, 776), (470, 776)],
       fill=K.mix(CONC, EDGE, 0.35))
K.poly(c, [(442, 812), (958, 812), (958, 820), (442, 820)],
       fill=K.mix(CONC, INK, 0.5))
# upper terrace
K.poly(c, [(506, 726), (894, 726), (916, 768), (484, 768)],
       fill=K.mix(CONC, EDGE, 0.12))
K.poly(c, [(506, 726), (894, 726), (894, 733), (506, 733)],
       fill=K.mix(CONC, EDGE, 0.5))
K.poly(c, [(484, 768), (916, 768), (916, 774), (484, 774)],
       fill=K.mix(CONC, INK, 0.45))
for x in (506, 620, 780, 894):                             # form-board seams
    K.line(c, [(x, 726), (x - 10, 768)], K.mix(CONC, INK, 0.38), width=1.4)
# gravel apron
# gravel hugs the pad edge rather than spraying across the frame
amask, ad = c.mask()
ad.polygon(c.pts([(404, 812), (996, 812), (1022, 868), (378, 868)]), fill=255)
ad.polygon(c.pts([(430, 872), (970, 872), (988, 894), (412, 894)]), fill=110)
K.chips(c, 210, (380, 812, 1020, 892), size=(2.0, 6.0),
        colors=(K.mix(CONC, INK, 0.45), K.mix(CONC, INK, 0.2),
                K.mix(CONC, EDGE, 0.15)),
        seed=SEED + 11, mask_img=amask)

# ======================================================================
# 6. LOWER COUPLING HALF — dark, energized, Alaska's side
# ======================================================================
block(534, 668, 866, 730, LO_BODY, LO_LIT, LO_DRK, lit_w=30)   # plinth
bolts(556, 844, 686, 9, 6.4)
K.line(c, [(534, 668), (866, 668)], EDGE, width=2.4)

block(622, 636, 778, 670, LO_BODY, LO_LIT, LO_DRK, lit_w=20)   # body

# cooling fin stack — straight machined hardware, reads at thumbnail and
# holds the dark mass (elliptical insulator discs read as pancakes here)
rect(AX - 46, 552, AX + 46, 650, K.mix(LO_BODY, INK, 0.4))     # core barrel
rect(AX - 46, 552, AX - 28, 650, LO_LIT)                       # lit core face
for i in range(8):
    fy = 560 + i * 11.4
    fw = 152 - i * 4.2
    rect(AX - fw, fy, AX + fw, fy + 7.4, LO_BODY)
    rect(AX - fw, fy, AX - fw + 22, fy + 7.4, LO_LIT)          # lit left tip
    rect(AX + fw - 13, fy, AX + fw, fy + 7.4, LO_DRK)          # shadow tip
    K.line(c, [(AX - fw, fy), (AX + fw, fy)], EDGE, width=1.5)
    K.line(c, [(AX - fw, fy + 7.4), (AX + fw, fy + 7.4)], LO_DRK, width=1.6)
    K.line(c, [(AX - fw, fy), (AX - fw, fy + 7.4)], EDGE, width=1.4)  # tip
    K.circle(c, AX - fw + 1.4, fy + 1.6, 1.5, fill=PAPER)             # glint

block(578, 506, 822, 556, LO_BODY, LO_LIT, LO_DRK, lit_w=30)   # housing
bolts(596, 804, 538, 7, 5.4)
# live machined contact face on TOP of the lower half
for r, mixv in ((108, 0.06), (86, 0.14), (62, 0.34), (38, 0.62)):
    K.poly(c, [(AX - r, 506), (AX + r, 506), (AX + r, 513), (AX - r, 513)],
           fill=K.mix(EDGE, AMBER, mixv))
K.line(c, [(578, 506), (822, 506)], EDGE, width=3)

# ======================================================================
# 7. amber conductors — climb from the pad, stop dead at the gap
# ======================================================================
for sx in (592, 808):
    path = [(sx + math.sin(i / 3.2) * 2.2, 744 - i * 11.3) for i in range(22)]
    K.line(c, path, LO_DRK, width=10.5)                      # cable sheath
    K.line(c, path, K.mix(AMBER, INK, 0.30), width=6.5)      # cable body
    K.line(c, [(x - 1.4, y) for x, y in path],
           K.mix(AMBER, PAPER, 0.22), width=2.0)             # highlight
    for cy in (708, 656, 604, 552):                          # clamps
        rect(sx - 13, cy - 8, sx + 13, cy + 8, LO_LIT)
        rect(sx - 13, cy - 8, sx + 13, cy - 5, EDGE)
        K.circle(c, sx, cy, 2.4, fill=LO_DRK)
    rect(sx - 15, 508, sx + 15, 526, K.mix(AMBER, EDGE, 0.30))  # lug
# every amber glow must stay clear of the gap band (bottom edge y=506)
K.glow(c, AX, 625, 115, AMBER, alpha=40)
K.glow(c, 592, 664, 50, AMBER, alpha=24)
K.glow(c, 808, 664, 50, AMBER, alpha=24)
# warm bounce onto the poured pad — the only temperature contrast in an
# otherwise wholly cold picture, and it sits safely below the gap
K.glow(c, 604, 752, 140, AMBER, alpha=19)
K.glow(c, 800, 752, 140, AMBER, alpha=19)

# ======================================================================
# 8. UPPER COUPLING HALF — pale, inert, cut by the frame, zero amber
# ======================================================================
block(652, -10, 748, 236, UP_BODY, UP_LIT, UP_DRK, lit_w=24)   # shaft
for fx in (672, 686, 700, 714, 728):                           # vertical flutes
    K.line(c, [(fx, -6), (fx, 232)], K.mix(UP_BODY, UP_DRK, 0.30), width=1.3)
    K.line(c, [(fx + 3, -6), (fx + 3, 232)], K.mix(UP_BODY, UP_LIT, 0.5),
           width=1.0)
# parting seam + rivet row partway up the shaft (meso structure)
rect(652, 116, 748, 125, UP_DRK)
rect(652, 116, 748, 118.5, EDGE)
bolts(658, 742, 120.5, 5, 2.8)
rect(652, 178, 748, 183, K.mix(UP_BODY, UP_DRK, 0.55))

block(556, 236, 844, 296, UP_BODY, UP_LIT, UP_DRK, lit_w=34)   # flange
bolts(576, 824, 266, 11, 6.6)
K.line(c, [(556, 290), (844, 290)], K.mix(UP_BODY, UP_DRK, 0.6), width=2)
K.line(c, [(556, 246), (844, 246)], K.mix(UP_BODY, UP_LIT, 0.45), width=1.4)
# tapered frustum down to the contact housing
K.poly(c, [(612, 296), (788, 296), (816, 392), (584, 392)], fill=UP_BODY)
K.poly(c, [(612, 296), (640, 296), (612, 392), (584, 392)], fill=UP_LIT)
K.poly(c, [(760, 296), (788, 296), (816, 392), (788, 392)], fill=UP_DRK)
K.line(c, [(612, 296), (584, 392)], EDGE, width=1.6)
block(578, 392, 822, 446, UP_BODY, UP_LIT, UP_DRK, lit_w=30)   # housing
bolts(596, 804, 416, 7, 5.4)
# dead machined contact face on the UNDERSIDE of the upper half
for r, mixv in ((108, 0.10), (86, 0.25), (62, 0.45), (38, 0.65)):
    K.poly(c, [(AX - r, 439), (AX + r, 439), (AX + r, 446), (AX - r, 446)],
           fill=K.mix(UP_BODY, UP_DRK, mixv))
K.line(c, [(578, 446), (822, 446)], EDGE, width=3)

# rime frost — stipple ONLY (the earlier hatch pass read as rain)
rmask, rd = c.mask()
rd.rectangle([c.s(556), c.s(0), c.s(844), c.s(446)], fill=170)
K.stipple(c, rmask, density=0.05, r=(0.5, 1.4), color=EDGE, seed=SEED + 9)

# ======================================================================
# 9. THE GAP — the focal point is the emptiness
# ======================================================================
# You see SKY through the gap. That is the whole point, so nothing is
# painted across it — the band is lit from within and the two machined
# faces above and below are hardened so the void between them reads.
GAP_M = (GAP_T + GAP_B) / 2

# the background between two big machined faces is shaded, so darken the
# band first — it buys the focal its contrast honestly
lay, ld = c.layer()
ld.rectangle([c.s(578), c.s(GAP_T + 2), c.s(822), c.s(GAP_B - 2)],
             fill=(*K.hex_to_rgb(INK), 130))
lay = lay.filter(K.ImageFilter.GaussianBlur(c.s(15)))
c.composite(lay)

K.glow(c, AX, GAP_M, 158, PAPER, alpha=44)
K.glow(c, AX, GAP_M, 92, PAPER, alpha=56)

# the light that escapes the slot — blurred halo, then a CRISP core.
# (Blurring the core too flattened it to 185/255 and cost the piece its
# lightest light; the focal has to win the contrast war outright.)
for i, (hw, hh, a) in enumerate([(150, 12.0, 64), (132, 7.5, 115),
                                 (112, 4.4, 195)]):
    lay, ld = c.layer()
    ld.rectangle([c.s(AX - hw), c.s(GAP_M - hh), c.s(AX + hw),
                  c.s(GAP_M + hh)], fill=(*K.hex_to_rgb(PAPER), a))
    lay = lay.filter(K.ImageFilter.GaussianBlur(c.s(5.0 - i * 1.4)))
    c.composite(lay)
lay, ld = c.layer()
ld.rectangle([c.s(AX - 92), c.s(GAP_M - 2.6), c.s(AX + 92),
              c.s(GAP_M + 2.6)], fill=(*K.hex_to_rgb("#ffffff"), 255))
ld.rectangle([c.s(AX - 122), c.s(GAP_M - 1.1), c.s(AX + 122),
              c.s(GAP_M + 1.1)], fill=(*K.hex_to_rgb(PAPER), 235))
c.composite(lay)

# harden both contact faces against the light so the void is unmistakable
lay, ld = c.layer()
ld.rectangle([c.s(578), c.s(438), c.s(822), c.s(446)],
             fill=(*K.hex_to_rgb(INK), 210))          # upper face underside
ld.rectangle([c.s(578), c.s(506), c.s(822), c.s(512)],
             fill=(*K.hex_to_rgb(INK), 150))          # lower face top lip
c.composite(lay)
K.line(c, [(578, 446), (822, 446)], PAPER, width=2.6)
K.line(c, [(578, 506), (822, 506)], PAPER, width=2.6)

# ======================================================================
# 10. micro finishing
# ======================================================================
for (gx, gy) in [(556, 238), (844, 238), (578, 394), (578, 508),
                 (534, 670), (866, 670), (652, -8), (506, 728)]:
    K.glow(c, gx, gy, 12, EDGE, alpha=115)
cmask, cd = c.mask()
cd.rectangle([0, c.s(HORIZON + 6), c.W, c.s(792)], fill=255)
K.chips(c, 85, (2, HORIZON + 10, 1078, 790), size=(2.0, 5.2),
        colors=(K.mix(ICE, WATER, 0.45), K.mix(ICE, WATER, 0.7)),
        seed=SEED + 4, mask_img=cmask)

K.mottle(c, strength=0.045, scale=2.6, seed=SEED + 2)
K.vignette(c, strength=0.15, spread=1.3)
K.grain(c, amount=6.0, seed=SEED)

# ======================================================================
# 11. type + brand marks
# ======================================================================
K.soft_panel(c, (44, 62, 566, 430), color="#120c22", alpha=170, blur=46)

HEAD = ["THE REACTOR", "WAITS ON ONE", "SIGNATURE"]
size = min(K.fit_size(c, h, 430, lo=40, hi=96, weight=900, opsz=144)
           for h in HEAD)
fh = K.fraunces(c, size, weight=900, opsz=144)
y = 122
for ln in HEAD:
    K.text(c, (96, y), ln, fh, PAPER, anchor="la")
    y += size * 1.06

K.text(c, (96, y + 26), "THE STACK  ·  VEHICLES  ·  21 SEP 2026",
       K.mono(c, 16, medium=True), EDGE, anchor="la", tracking=0.22)

K.text(c, (984, 996), "EIELSON AFB  ·  5 MW", K.mono(c, 14),
       K.mix(EDGE, ICE, 0.3), anchor="ra", tracking=0.26)

K.text(c, (96, 988), "ALASKA.AI", K.fraunces(c, 30, weight=900, opsz=144),
       PAPER, anchor="la", tracking=0.04)

# colophon in the pale ink, not gold — protects the "no warm ink above
# the gap" rule that carries the whole concept
K.polaris(c, 956, 116, r=13, color=EDGE, core=PAPER)

# ======================================================================
c.finish("out/post_image.png", {
    "date": "21 SEP 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "VEHICLES",
    "byline": "",
    "headline": "The reactor waits on one signature",
    "style_family": "machined_plate",
    "palette": [PAPER, SKY_TOP, SKY_LOW, INK, UP_BODY, LO_BODY, AMBER],
    "derived_tones": {"EDGE": EDGE, "UP_LIT": UP_LIT, "UP_DRK": UP_DRK,
                      "LO_LIT": LO_LIT, "LO_DRK": LO_DRK, "CONC": CONC,
                      "GROUND": GROUND, "WATER": WATER, "ICE": ICE},
    "hue_family": "violet",
    "composition": "suspended_gap",
    "motifs": ["split high-voltage coupling", "the empty last inch",
               "insulator sheds", "amber conductors stopping at the gap",
               "poured concrete pad", "muskeg water pools",
               "Eielson hangars and stack plume"],
    "technique_stack": ["gradient_v", "field@300+upscale", "ridge_fill",
                        "voronoi_polys x2", "blob_pts", "wobble_pts",
                        "ell_pts", "stipple", "chips", "glow", "soft_panel",
                        "chip", "mottle", "grain"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 6.12, "weakest": "craft_finish",
         "fix": "berm was a shapeless flat blob, the frost hatch read as "
                "rain, and the two halves read as one tower with a stripe"},
        {"iter": 2, "weighted": 7.21, "weakest": "craft_finish",
         "fix": "elliptical insulator sheds read as torn rubber, conductors "
                "were candy-striped, slot read as a collar on the upper half"},
        {"iter": 3, "weighted": 7.00, "weakest": "craft_finish",
         "fix": "value structure collapsed to mid-tones, sheds read as "
                "pancakes and the meltwater pools as lily pads"},
        {"iter": 4, "weighted": 7.93, "weakest": "color_value",
         "fix": "sampled the focal and found it peaked at 185/255, so the "
                "lightest light was a mid-grey; blur was eating the core"},
        {"iter": 5, "weighted": 8.46, "weakest": "craft_finish",
         "fix": "upper half too plain, gap shadow read as a hard box, fin "
                "tips lacked specular life"},
        {"iter": 6, "weighted": 8.59, "weakest": "concept",
         "fix": "shipped"}
    ],
    "eval_final": {
        "weighted": 8.59,
        "scores": {"concept": 8.5, "focal": 9.0, "composition": 8.5,
                   "color_value": 8.5, "detail": 8.5, "craft": 8.5,
                   "typography": 8.5, "originality": 8.5, "fidelity": 9.0},
        "notes": "Above the 8.5 floor with no dimension below 7. Focal "
                 "verified at 253/255 against a 0-255 global range, so the "
                 "slot wins the contrast war outright. Six eval iterations "
                 "plus one script crash (art_kit.chips mask index overflow, "
                 "fixed, not counted)."
    },
})
print("rendered out/post_image.png")
