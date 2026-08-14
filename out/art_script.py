"""
Alaska.Ai — The Stack — 14 AUG 2026
FERC non-capacity license amendment, Bradley Lake / Dixon Diversion, P-8221-124

Concept: a monumental frontal elevation of the spillway holding an immense
cell-by-cell mass of water. Seven crest gate bays; exactly one is lit. The
reader sees enormous consequence resting on one small opening before reading
a word. Style family voronoi_impoundment (mosaic_voronoi hybridised toward a
civil-engineering elevation). Full blueprint in out/art_plan.md.
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np
from PIL import Image, ImageFilter
import art_kit as K
from art_kit import (Canvas, oklch, mix, lighten, darken, ramp, poly, line,
                     circle, hand_line, wobble_pts, ridge_pts, gradient_v,
                     voronoi_polys, hatch, stipple, chips, glow, grain,
                     mottle, vignette, fraunces, mono, text, measure, polaris)

SEED = 8221                       # FERC Project No. 8221

# ------------------------------------------------------------------ palette
PAPER  = oklch(0.940, 0.012, 300)   # sky band / headline ground
STONE  = oklch(0.505, 0.032, 291)   # concrete structure (cool grey stone)
STONE_L= oklch(0.620, 0.028, 291)   # lit faces, pier noses, crest cap
FIELD  = oklch(0.440, 0.075, 292)   # mid water
SHADOW = oklch(0.280, 0.065, 288)   # deep water, gate recesses
INK    = oklch(0.160, 0.045, 295)   # darkest water, tailwater, type
ACCENT = oklch(0.790, 0.155,  75)   # the one lit bay, polaris, dimensions
PALETTE = [PAPER, STONE, STONE_L, FIELD, SHADOW, INK, ACCENT]

# ----------------------------------------------------------------- geometry
POOL_NEW = 364.0                  # new normal maximum operating pool
POOL_OLD = 396.0                  # prior pool, the 16 ft raise
CREST    = 560.0                  # top of structure
BAY_TOP, BAY_BOT = 578.0, 790.0
FACE_BOT = 948.0                  # spillway toe / tailwater line

BAY_W, BAY_GAP, N_BAYS = 150.0, 26.0, 5
BAY_SPAN = N_BAYS * BAY_W + (N_BAYS - 1) * BAY_GAP
BAY_X0 = 540.0 - BAY_SPAN / 2.0
BAY_CX = [BAY_X0 + i * (BAY_W + BAY_GAP) + BAY_W / 2 for i in range(N_BAYS)]
LIT = 3                            # the one bay that is lit (right of centre)

HEADLINE = ["38% MORE POWER.", "UNCONTESTED."]
KICKER = "THE STACK  ·  REGULATORY  ·  14 AUG 2026"

c = Canvas(bg=PAPER, ss=2)

# =========================================================== 1. paper + sky
gradient_v(c, (0, 0, 1080, POOL_NEW + 6), PAPER, mix(PAPER, FIELD, 0.30))
mottle(c, strength=0.045, scale=3.2, seed=SEED)

# ============================================ 2. far ridge (Kenai wall) x3
# three ranges, each lighter/flatter with distance -> atmospheric depth
for i, (base, amp, t, sd) in enumerate(
        [(316, 24, 0.72, SEED + 1), (338, 32, 0.55, SEED + 2),
         (358, 40, 0.36, SEED + 3)]):
    col = mix(FIELD, PAPER, t)
    pts = ridge_pts(base, amp, scale=2.0 + i * 0.9, octaves=4, seed=sd,
                    x0=-20, x1=1100)
    poly(c, list(pts) + [(1100, POOL_NEW + 4), (-20, POOL_NEW + 4)], fill=col)
    # meso: a lighter sunlit shoulder along each crest, no hard shapes
    hand_line(c, list(pts), mix(col, PAPER, 0.42), width=2.0, amp=1.6,
              seed=sd + 900)

# ============================================== 3. water mass (the pool)
# voronoi generated in a 2.2x vertically-stretched space, then compressed,
# so cells read as water lying flat rather than as tile.
POOL_H = CREST - POOL_NEW
STRETCH = 3.4
cells = voronoi_polys(n=430, seed=SEED, relax=1,
                      bbox=(-60, 0, 1140, POOL_H * STRETCH))
water_lay, wd = c.layer()
for cell in cells:
    p = [(x, y / STRETCH + POOL_NEW) for (x, y) in cell]
    cy = sum(q[1] for q in p) / len(p)
    t = min(1.0, max(0.0, (cy - POOL_NEW) / POOL_H))
    base = mix(FIELD, SHADOW, t ** 0.85) if t < 0.62 else \
        mix(SHADOW, INK, (t - 0.62) / 0.38)
    jit = (hash((int(cy), int(p[0][0]))) % 100) / 100.0 - 0.5
    col = lighten(base, jit * 0.06)
    wd.polygon(c.pts(p), fill=(*K.hex_to_rgb(col), 255),
               outline=(*K.hex_to_rgb(darken(base, 0.07)), 255),
               width=max(1, int(c.s(1.1))))
c.composite(water_lay)

# ============================================ 4. waterline + the 16 ft raise
# prior pool: a fine ticked line
for x in range(60, 1030, 26):
    line(c, [(x, POOL_OLD), (x + 13, POOL_OLD)], mix(ACCENT, FIELD, 0.45),
         width=1.6)
# new pool: the hard bright edge
line(c, [(0, POOL_NEW), (1080, POOL_NEW)], mix(PAPER, ACCENT, 0.22), width=3.2)
line(c, [(0, POOL_NEW + 3.4), (1080, POOL_NEW + 3.4)],
     mix(FIELD, PAPER, 0.30), width=1.4)
# micro: surface glints riding the new waterline
chips(c, 200, (0, POOL_NEW + 2, 1080, POOL_NEW + 26), size=(1.4, 4.2),
      colors=(mix(FIELD, PAPER, 0.55), mix(FIELD, PAPER, 0.30),
              mix(ACCENT, PAPER, 0.5)), seed=SEED + 11)
# specular streaks lying flat on the pool: the plane cue
sp, spd = c.layer()
sr = np.random.default_rng(SEED + 71)
for _ in range(150):
    t = sr.random() ** 1.5
    yy = POOL_NEW + 8 + t * (CREST - POOL_NEW - 24)
    ln = sr.uniform(26, 150) * (0.45 + t)
    xx = sr.uniform(-40, 1080)
    spd.line([(c.s(xx), c.s(yy)), (c.s(xx + ln), c.s(yy))],
             fill=(*K.hex_to_rgb(mix(FIELD, PAPER, 0.55 - 0.35 * t)),
                   int(58 * (1 - t) + 12)),
             width=max(1, int(c.s(sr.uniform(1.0, 2.2)))))
c.composite(sp.filter(ImageFilter.GaussianBlur(c.s(1.2))))

# dimension: +16 FT between the two pool lines
DX = 138.0
line(c, [(DX, POOL_NEW), (DX, POOL_OLD)], ACCENT, width=1.8)
for yy in (POOL_NEW, POOL_OLD):
    line(c, [(DX - 9, yy), (DX + 9, yy)], ACCENT, width=1.8)
text(c, (DX + 18, POOL_OLD + 12), "+16 FT", mono(c, 15, medium=True),
     ACCENT, anchor="la", tracking=0.16)

# ==================================================== 5. the concrete mass
crest_top = CREST
dam = [(-20, crest_top), (1100, crest_top), (1100, FACE_BOT + 40),
       (-20, FACE_BOT + 40)]
poly(c, dam, fill=STONE)
gradient_v(c, (-20, crest_top, 1100, FACE_BOT + 40),
           lighten(STONE, 0.06), darken(STONE, 0.20))
# crest capping band
poly(c, [(-20, crest_top), (1100, crest_top), (1100, crest_top + 12),
         (-20, crest_top + 12)], fill=lighten(STONE, 0.10))
poly(c, [(-20, crest_top + 12), (1100, crest_top + 12),
         (1100, crest_top + 15), (-20, crest_top + 15)],
     fill=darken(STONE, 0.14))

# crest walkway and handrail: the human-scale line along the top
line(c, [(-20, crest_top + 6), (1100, crest_top + 6)], lighten(STONE_L, 0.06),
     width=2.0)
line(c, [(-20, crest_top - 23.5), (1100, crest_top - 23.5)],
     mix(PAPER, FIELD, 0.28), width=1.8)
for hx in np.arange(-10, 1100, 46.0):
    line(c, [(hx, crest_top - 22), (hx, crest_top - 4)], darken(STONE, 0.30),
         width=1.6)
line(c, [(-20, crest_top - 22), (1100, crest_top - 22)], darken(STONE, 0.24),
     width=1.8)

# meso: stepped spillway courses below the gates
n_steps = 9
for i in range(n_steps):
    y0 = BAY_BOT + i * (FACE_BOT - BAY_BOT) / n_steps
    y1 = BAY_BOT + (i + 1) * (FACE_BOT - BAY_BOT) / n_steps
    sh = 0.04 + 0.115 * (i / n_steps)
    poly(c, [(-20, y0), (1100, y0), (1100, y1), (-20, y1)],
         fill=darken(STONE, sh))
    hand_line(c, [(-20, y0), (1100, y0)], darken(STONE, sh + 0.16),
              width=1.5, amp=1.1, seed=SEED + 40 + i)

# meso: vertical construction joints, on a monolith spacing
for x in range(30, 1080, 74):
    hand_line(c, [(x, crest_top + 16), (x, FACE_BOT)], darken(STONE, 0.13),
              width=1.4, amp=1.0, seed=SEED + 80 + x)

# texture identity pass: hatch clipped to the concrete only
mask, md = c.mask()
md.polygon(c.pts([(-20, crest_top + 16), (1100, crest_top + 16),
                  (1100, FACE_BOT), (-20, FACE_BOT)]), fill=255)
wl, wld = c.layer()
wf = K.warp(K.field(scale=2.6, octaves=4, seed=SEED + 61), strength=40.0,
            scale=2.2, seed=SEED + 62)
wimg = K.field_img(wf, darken(STONE, 0.16), lighten(STONE, 0.10), gamma=1.1)
wl.paste(wimg.convert("RGBA"), (0, 0))
wl.putalpha(96)
c.img.paste(wl, (0, 0), Image.composite(
    mask, Image.new("L", (c.W, c.W), 0), wl.getchannel("A")))
c.draw = K.ImageDraw.Draw(c.img, "RGBA")

hatch(c, mask, spacing=11.0, angle=52.0, color=darken(STONE, 0.16), width=1.3)
stipple(c, mask, density=0.05, r=(0.5, 1.35), color=darken(STONE, 0.30),
        seed=SEED + 5)

# meso: a recessed apron panel under each bay, with its own shadow line
for i in range(N_BAYS):
    ax0, ax1 = BAY_CX[i] - BAY_W / 2 + 2, BAY_CX[i] + BAY_W / 2 - 2
    poly(c, [(ax0, BAY_BOT + 10), (ax1, BAY_BOT + 10),
             (ax1, FACE_BOT - 8), (ax0, FACE_BOT - 8)],
         fill=darken(STONE, 0.05))
    line(c, [(ax0, BAY_BOT + 10), (ax1, BAY_BOT + 10)],
         darken(STONE, 0.26), width=1.6)
    line(c, [(ax0, BAY_BOT + 10), (ax0, FACE_BOT - 8)],
         darken(STONE, 0.22), width=1.4)
    line(c, [(ax1, BAY_BOT + 10), (ax1, FACE_BOT - 8)],
         lighten(STONE, 0.10), width=1.4)

# micro: form-tie holes on the monolith grid, the signature concrete tell
for gx in np.arange(BAY_X0 - 60, 1080, 41.0):
    for gy in np.arange(BAY_BOT + 26, FACE_BOT - 12, 41.0):
        circle(c, gx, gy, 1.9, fill=darken(STONE, 0.30))
        circle(c, gx - 0.6, gy - 0.6, 1.0, fill=lighten(STONE, 0.08))

# micro: hairline cracks and spall on the face
rr = np.random.default_rng(SEED + 7)
for _ in range(26):
    x0 = rr.uniform(20, 1060); y0 = rr.uniform(BAY_BOT + 8, FACE_BOT - 10)
    seg = [(x0, y0)]
    for k in range(rr.integers(2, 5)):
        seg.append((seg[-1][0] + rr.uniform(-24, 24),
                    seg[-1][1] + rr.uniform(6, 22)))
    hand_line(c, seg, darken(STONE, 0.26), width=1.1, amp=1.4,
              seed=SEED + 200 + int(x0))

# ======================================================== 6. the gate bays
def bay(i, lit=False):
    x0 = BAY_CX[i] - BAY_W / 2
    x1 = BAY_CX[i] + BAY_W / 2
    # recess shadow behind the leaf
    poly(c, [(x0 - 4, BAY_TOP - 2), (x1 + 4, BAY_TOP - 2),
             (x1 + 4, BAY_BOT + 4), (x0 - 4, BAY_BOT + 4)],
         fill=darken(STONE, 0.34))
    if lit:
        # the one open bay. the leaf is hoisted into the upper third and
        # light floods the opening beneath it.
        poly(c, [(x0, BAY_TOP), (x1, BAY_TOP), (x1, BAY_BOT), (x0, BAY_BOT)],
             fill=darken(INK, 0.10))
        HOIST = BAY_TOP + 62
        gradient_v(c, (x0, HOIST, x1, BAY_BOT),
                   mix(ACCENT, PAPER, 0.34), mix(ACCENT, PAPER, 0.80))
        # the head of the opening sits in the leaf's shadow, so the light
        # reads as emerging from depth rather than as a flat panel
        hd_, hdd = c.layer()
        for k in range(34):
            t = k / 33.0
            yy = HOIST + t * 84
            hdd.rectangle([c.s(x0), c.s(yy), c.s(x1), c.s(yy + 4)],
                          fill=(*K.hex_to_rgb(INK), int(126 * (1 - t) ** 1.5)))
        c.composite(hd_)
        # jamb shading down both sides of the opening
        for sgn, xe in ((1, x0), (-1, x1)):
            jl, jld = c.layer()
            for k in range(26):
                t = k / 25.0
                ja = xe + sgn * t * 26
                jb = xe + sgn * (t * 26 + 2)
                jld.rectangle([c.s(min(ja, jb)), c.s(HOIST),
                               c.s(max(ja, jb)), c.s(BAY_BOT)],
                              fill=(*K.hex_to_rgb(INK), int(96 * (1 - t) ** 1.4)))
            c.composite(jl)
        # hoisted leaf, seen edge-on and back-lit
        poly(c, [(x0, BAY_TOP + 2), (x1, BAY_TOP + 2), (x1, HOIST),
                 (x0, HOIST)], fill=darken(SHADOW, 0.30))
        for k in range(1, 3):
            yy = BAY_TOP + 2 + k * (HOIST - BAY_TOP - 2) / 3
            line(c, [(x0 + 3, yy), (x1 - 3, yy)], lighten(SHADOW, 0.10),
                 width=1.6)
        line(c, [(x0, HOIST), (x1, HOIST)], mix(ACCENT, PAPER, 0.85),
             width=2.6)
        for sx in (x0 + 9, x1 - 9):
            circle(c, sx, BAY_TOP + 20, 6.0, fill=lighten(SHADOW, 0.24))
        return
    face = mix(SHADOW, INK, 0.42)
    poly(c, [(x0, BAY_TOP), (x1, BAY_TOP), (x1, BAY_BOT), (x0, BAY_BOT)],
         fill=face)
    # meso: four horizontal ribs per leaf
    for k in range(1, 8):
        y = BAY_TOP + k * (BAY_BOT - BAY_TOP) / 8
        line(c, [(x0 + 3, y), (x1 - 3, y)],
             lighten(face, 0.12), width=2.0)
    # meso: trunnion pins
    for sx in (x0 + 9, x1 - 9):
        circle(c, sx, BAY_TOP + 20, 6.0,
               fill=lighten(face, 0.22))
    # meso: vertical stiffeners across the skinplate
    for k in range(1, 4):
        vx = x0 + k * (x1 - x0) / 4
        line(c, [(vx, BAY_TOP + 4), (vx, BAY_BOT - 4)],
             lighten(face, 0.07), width=1.5)
    # meso: sheen down the leaf, brighter at the top
    lay, ld = c.layer()
    for k in range(26):
        t = k / 25.0
        yy = BAY_TOP + t * (BAY_BOT - BAY_TOP)
        a = int(52 * (1 - t) ** 1.6)
        ld.rectangle([c.s(x0), c.s(yy), c.s(x1), c.s(yy + 5)],
                     fill=(*K.hex_to_rgb(FIELD), a))
    c.composite(lay)
    # micro: the common pool-stain waterline across every leaf
    poly(c, [(x0, BAY_TOP + 62), (x1, BAY_TOP + 62), (x1, BAY_TOP + 67),
             (x0, BAY_TOP + 67)], fill=darken(face, 0.14))
    # micro: seating grime at the sill
    poly(c, [(x0, BAY_BOT - 7), (x1, BAY_BOT - 7), (x1, BAY_BOT),
             (x0, BAY_BOT)], fill=darken(face, 0.22))

for i in range(N_BAYS):
    bay(i, lit=(i == LIT))

# meso: staining streaks weeping down the face below every closed bay.
# vertical elements are what break the horizontal banding of an elevation.
st = np.random.default_rng(SEED + 31)
for i in range(N_BAYS):
    if i == LIT:
        continue
    for _ in range(9):
        sx = BAY_CX[i] + st.uniform(-BAY_W / 2 + 5, BAY_W / 2 - 5)
        sl = st.uniform(38, FACE_BOT - BAY_BOT - 6)
        lay, ld = c.layer()
        ld.polygon(c.pts([(sx - st.uniform(1.5, 4.5), BAY_BOT),
                          (sx + st.uniform(1.5, 4.5), BAY_BOT),
                          (sx + st.uniform(2.5, 7.0), BAY_BOT + sl),
                          (sx - st.uniform(2.5, 7.0), BAY_BOT + sl)]),
                   fill=(*K.hex_to_rgb(darken(STONE, 0.20)), 58))
        c.composite(lay.filter(ImageFilter.GaussianBlur(c.s(1.6))))

# piers standing proud of the face between every bay, with lit noses and
# cast shadows. These carry the vertical rhythm and give the wall depth.
PIER_W = 30.0
pier_x = [BAY_X0 - BAY_GAP / 2] + \
         [BAY_CX[i] + BAY_W / 2 + BAY_GAP / 2 for i in range(N_BAYS)]
for px in pier_x:
    # cast shadow thrown to the right
    lay, ld = c.layer()
    ld.polygon(c.pts([(px + PIER_W / 2, crest_top),
                      (px + PIER_W / 2 + 15, crest_top),
                      (px + PIER_W / 2 + 15, FACE_BOT),
                      (px + PIER_W / 2, FACE_BOT)]),
               fill=(*K.hex_to_rgb(INK), 76))
    c.composite(lay.filter(ImageFilter.GaussianBlur(c.s(3.4))))
    # pier body, lit left face and shaded right face
    poly(c, [(px - PIER_W / 2, crest_top - 4), (px, crest_top - 13),
             (px, FACE_BOT + 6), (px - PIER_W / 2, FACE_BOT + 6)],
         fill=STONE_L)
    poly(c, [(px, crest_top - 13), (px + PIER_W / 2, crest_top - 4),
             (px + PIER_W / 2, FACE_BOT + 6), (px, FACE_BOT + 6)],
         fill=darken(STONE, 0.16))
    # nose cap catching the light
    poly(c, [(px - PIER_W / 2, crest_top - 4), (px, crest_top - 13),
             (px + PIER_W / 2, crest_top - 4), (px, crest_top + 3)],
         fill=lighten(STONE_L, 0.09))
    line(c, [(px - PIER_W / 2, crest_top - 4), (px, crest_top - 13)],
         mix(PAPER, STONE_L, 0.55), width=1.8)
    # micro: horizontal lift joints up the pier
    for yy in np.arange(crest_top - 4, FACE_BOT, 34.0):
        line(c, [(px - PIER_W / 2, yy), (px + PIER_W / 2, yy)],
             darken(STONE, 0.24), width=1.1)

# atmosphere: spray haze riding the crest so the water does not butt-join
haze, hd = c.layer()
hd.rectangle([c.s(-20), c.s(crest_top - 26), c.s(1100), c.s(crest_top + 8)],
             fill=(*K.hex_to_rgb(mix(FIELD, PAPER, 0.42)), 54))
c.composite(haze.filter(ImageFilter.GaussianBlur(c.s(11.0))))

# ================================== 7. the lit bay: glow, spill, light shaft
LX = BAY_CX[LIT]
glow(c, LX, (BAY_TOP + BAY_BOT) / 2 + 14, 160, ACCENT, alpha=96)
glow(c, LX, BAY_TOP - 40, 110, ACCENT, alpha=42)      # spill up onto the water
glow(c, LX, BAY_BOT + 60, 120, ACCENT, alpha=48)      # spill down the face

# flared chute below the lit bay: converging-then-diverging training walls.
# the only diagonals in the lower half, and they point at the focal.
for sgn in (-1, 1):
    poly(c, [(LX + sgn * (BAY_W / 2 + 4), BAY_BOT),
             (LX + sgn * (BAY_W / 2 + 30), BAY_BOT),
             (LX + sgn * (BAY_W / 2 + 104), FACE_BOT + 6),
             (LX + sgn * (BAY_W / 2 + 78), FACE_BOT + 6)],
         fill=STONE_L if sgn < 0 else darken(STONE, 0.14))
    hand_line(c, [(LX + sgn * (BAY_W / 2 + 4), BAY_BOT),
                  (LX + sgn * (BAY_W / 2 + 78), FACE_BOT + 6)],
              darken(STONE, 0.30), width=1.6, amp=1.0, seed=SEED + 61 + sgn)

# THE NAPPE. water springing off the sill on a ballistic curve, brightest
# where it leaves the lip and dissolving into spray at the toe. A curved,
# tapering jet is what makes this read as water and not as a ramp.
FALL = FACE_BOT + 30 - BAY_BOT
def nappe_x(t, edge):
    """t in 0..1 down the fall; edge=+-1 for the two sides of the jet."""
    spread = 1.0 + 0.55 * t ** 1.7
    return LX + edge * (BAY_W / 2 - 6) * spread

nap, nd = c.layer()
STEPS = 46
for k in range(STEPS):
    t0, t1 = k / STEPS, (k + 1) / STEPS
    y0 = BAY_BOT + (t0 ** 1.35) * FALL
    y1 = BAY_BOT + (t1 ** 1.35) * FALL
    a = int(232 * (1 - t0) ** 0.72)
    col = mix(mix(ACCENT, PAPER, 0.82), ACCENT, t0 ** 0.8)
    nd.polygon(c.pts([(nappe_x(t0, -1), y0), (nappe_x(t0, 1), y0),
                      (nappe_x(t1, 1), y1), (nappe_x(t1, -1), y1)]),
               fill=(*K.hex_to_rgb(col), a))
# internal filament streaks so the jet has grain and direction
nr = np.random.default_rng(SEED + 55)
for _ in range(300):
    e = nr.uniform(-0.96, 0.96)
    t0 = nr.uniform(0.0, 0.72); t1 = min(1.0, t0 + nr.uniform(0.10, 0.30))
    pa = [(LX + e * (nappe_x(tt, 1) - LX), BAY_BOT + (tt ** 1.35) * FALL)
          for tt in (t0, (t0 + t1) / 2, t1)]
    nd.line([(c.s(x), c.s(y)) for x, y in pa],
            fill=(*K.hex_to_rgb(mix(ACCENT, PAPER, nr.uniform(0.5, 0.95))),
                  int(150 * (1 - t0))),
            width=max(1, int(c.s(nr.uniform(1.0, 2.6)))))
# standing ridges where the sheet folds, the tell that this is falling water
for _ in range(9):
    e = nr.uniform(-0.72, 0.72)
    pa = [(LX + e * (nappe_x(tt, 1) - LX), BAY_BOT + (tt ** 1.35) * FALL)
          for tt in np.linspace(0.04, 0.94, 7)]
    nd.line([(c.s(x), c.s(y)) for x, y in pa],
            fill=(*K.hex_to_rgb(mix(ACCENT, PAPER, 0.95)), 132),
            width=max(1, int(c.s(nr.uniform(2.4, 4.6)))))
nap = nap.filter(ImageFilter.GaussianBlur(c.s(1.7)))
c.composite(nap)
# chute walls cast onto the sheet, so the jet sits inside the structure
for sgn in (-1, 1):
    cw, cwd = c.layer()
    cwd.polygon(c.pts([(LX + sgn * (BAY_W / 2 - 6), BAY_BOT),
                       (LX + sgn * (BAY_W / 2 + 16), BAY_BOT),
                       (LX + sgn * (BAY_W / 2 + 74), FACE_BOT + 20),
                       (LX + sgn * (BAY_W / 2 + 42), FACE_BOT + 20)]),
                fill=(*K.hex_to_rgb(INK), 82))
    c.composite(cw.filter(ImageFilter.GaussianBlur(c.s(6.0))))

# the bright lip where the sheet leaves the sill
line(c, [(LX - BAY_W / 2 + 4, BAY_BOT), (LX + BAY_W / 2 - 4, BAY_BOT)],
     mix(ACCENT, PAPER, 0.92), width=4.0)
glow(c, LX, BAY_BOT + 6, 92, ACCENT, alpha=104)
# spray plume where the jet lands
for r_, a_ in ((132, 62), (86, 78), (52, 96)):
    glow(c, LX, FACE_BOT + 6, r_, mix(ACCENT, PAPER, 0.55), alpha=a_)
spry, spd2 = c.layer()
qr = np.random.default_rng(SEED + 23)
for _ in range(430):
    ang = qr.uniform(0, math.tau)
    rad = abs(qr.normal(0, 1)) * 82
    sx = LX + math.cos(ang) * rad * 1.5
    sy = FACE_BOT + 2 + math.sin(ang) * rad * 0.55 - qr.uniform(0, 34)
    rr_ = qr.uniform(1.0, 3.4)
    a = int(190 * math.exp(-rad / 78))
    spd2.ellipse([c.s(sx - rr_), c.s(sy - rr_), c.s(sx + rr_), c.s(sy + rr_)],
                 fill=(*K.hex_to_rgb(mix(ACCENT, PAPER, qr.uniform(0.4, 0.95))), a))
c.composite(spry.filter(ImageFilter.GaussianBlur(c.s(2.2))))

# bounce: the jet throws warm light back onto the piers that frame it
for sgn in (-1, 1):
    bl, bld = c.layer()
    for k in range(30):
        t = k / 29.0
        bx = LX + sgn * (BAY_W / 2 + 6 + t * 34)
        bld.rectangle([c.s(min(bx, bx + sgn * 2)), c.s(BAY_TOP + 40),
                       c.s(max(bx, bx + sgn * 2)), c.s(FACE_BOT)],
                      fill=(*K.hex_to_rgb(ACCENT), int(74 * (1 - t) ** 1.6)))
    c.composite(bl.filter(ImageFilter.GaussianBlur(c.s(4.0))))

# the deadline, sitting directly on the chokepoint
text(c, (LX, CREST - 26), "28 AUG  ·  5 PM ET", mono(c, 15, medium=True),
     mix(ACCENT, PAPER, 0.25), anchor="ms", tracking=0.18)

# ================================ 8. the 0.3 MW valve (scale contrast micro)
VX, VY = 372.0, 878.0
poly(c, [(VX - 16, VY - 15), (VX + 16, VY - 15), (VX + 16, VY + 15),
         (VX - 16, VY + 15)], fill=darken(STONE, 0.13))
line(c, [(VX - 16, VY - 15), (VX + 16, VY - 15)], lighten(STONE, 0.10), width=1.3)
circle(c, VX, VY, 10.5, fill=darken(STONE, 0.36),
       outline=darken(STONE, 0.54), width=2)
circle(c, VX, VY, 4.0, fill=mix(ACCENT, STONE, 0.55))
line(c, [(VX, VY + 12), (VX, VY + 24)], darken(STONE, 0.40), width=1.4)
text(c, (VX, VY + 28), "0.3 MW", mono(c, 13), darken(STONE, 0.52),
     anchor="ma", tracking=0.16)

# ========================================================= 9. tailwater band
poly(c, [(-20, FACE_BOT), (1100, FACE_BOT), (1100, 1100), (-20, 1100)],
     fill=INK)
poly(c, [(-20, FACE_BOT), (1100, FACE_BOT), (1100, FACE_BOT + 9),
         (-20, FACE_BOT + 9)], fill=mix(INK, SHADOW, 0.6))
# micro: churn and foam, brightest under the lit bay
# horizontal turbulence streaks at the toe, densest under the lit bay
tw = np.random.default_rng(SEED + 21)
tl, tld = c.layer()
for _ in range(170):
    tx = tw.uniform(-20, 1100); ty = tw.uniform(FACE_BOT + 3, 1044)
    d = max(0.0, 1.0 - abs(tx - LX) / 300.0)
    ln = tw.uniform(9, 46) * (0.7 + d)
    col = mix(INK, ACCENT, 0.30 * d) if tw.random() < 0.35 + 0.4 * d \
        else mix(INK, FIELD, tw.uniform(0.18, 0.5))
    tld.line([(c.s(tx), c.s(ty)),
              (c.s(tx + ln), c.s(ty + tw.uniform(-1.6, 1.6)))],
             fill=(*K.hex_to_rgb(col), 205),
             width=max(1, int(c.s(tw.uniform(1.2, 2.8)))))
c.composite(tl.filter(ImageFilter.GaussianBlur(c.s(1.5))))
fw, fwd = c.layer()
fr = np.random.default_rng(SEED + 22)
for _ in range(300):
    fx = LX + fr.normal(0, 118); fy = fr.uniform(FACE_BOT + 4, 1030)
    rr_ = fr.uniform(0.9, 2.8)
    fwd.ellipse([c.s(fx - rr_), c.s(fy - rr_), c.s(fx + rr_), c.s(fy + rr_)],
                fill=(*K.hex_to_rgb(mix(ACCENT, PAPER, fr.uniform(0.3, 0.9))),
                      int(150 * math.exp(-abs(fx - LX) / 130))))
c.composite(fw.filter(ImageFilter.GaussianBlur(c.s(1.8))))
glow(c, LX, FACE_BOT + 18, 96, ACCENT, alpha=40)

# ============================================================== 10. finish
# ground the frame: a soft darkening wash toward the bottom corners
bw, bwd = c.layer()
for k in range(60):
    t = k / 59.0
    yy = FACE_BOT - 120 + t * 260
    bwd.rectangle([c.s(-20), c.s(yy), c.s(1100), c.s(yy + 6)],
                  fill=(*K.hex_to_rgb(mix(INK, FIELD, 0.30)), int(66 * t ** 1.5)))
c.composite(bw.filter(ImageFilter.GaussianBlur(c.s(16.0))))

grain(c, amount=6.0, seed=SEED)
vignette(c, strength=0.14, spread=1.35)

# =============================================================== 11. type
text(c, (96, 64), KICKER, mono(c, 15, medium=True),
     mix(INK, PAPER, 0.34), anchor="la", tracking=0.26)
line(c, [(96, 96), (96 + 96, 96)], ACCENT, width=4.0)

h1 = fraunces(c, 90, weight=900, opsz=144)
text(c, (96, 132), HEADLINE[0], h1, INK, anchor="la", tracking=-0.012)
text(c, (96, 226), HEADLINE[1], h1, INK, anchor="la", tracking=-0.012)

polaris(c, 952, 96, r=13, color=ACCENT, core=mix(ACCENT, PAPER, 0.7))

wm = fraunces(c, 34, weight=900, opsz=144)
text(c, (96, 1002), "ALASKA.AI", wm, mix(PAPER, FIELD, 0.12), anchor="la",
     tracking=0.05)
text(c, (984, 1012), "P-8221-124", mono(c, 14), mix(INK, PAPER, 0.42),
     anchor="ra", tracking=0.20)

# ================================================================ 12. meta
meta = {
    "date": "14 AUG 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "REGULATORY",
    "byline": "",
    "headline": "38% MORE POWER. UNCONTESTED.",
    "style_family": "voronoi_impoundment",
    "palette": PALETTE,
    "hue_family": "violet",
    "composition": "central_icon",
    "motifs": ["spillway elevation", "seven crest gates and piers",
               "one lit bay", "impounded voronoi water",
               "+16 ft pool raise", "falling nappe", "0.3 MW valve"],
    "technique_stack": ["gradient_v", "mottle", "ridge_pts", "voronoi_polys",
                        "hatch", "stipple", "chips", "hand_line", "glow",
                        "nappe curve", "grain", "vignette", "polaris"],
    "seed": SEED,
    "mechanism": ("FERC non-capacity license amendment, Bradley Lake / "
                  "Dixon Diversion, Project No. P-8221-124"),
    "eval_history": [
            {
                    "iter": 1,
                    "weighted": 5.55,
                    "weakest": "craft",
                    "fix": "kicker collided with the headline; six flat horizontal bands; concrete out-brighted the focal; water read as dried mud"
            },
            {
                    "iter": 2,
                    "weighted": 7.26,
                    "weakest": "composition",
                    "fix": "added piers, staining streaks and a flared chute for vertical rhythm; retyped the header to clear the collision"
            },
            {
                    "iter": 3,
                    "weighted": 7.4,
                    "weakest": "color",
                    "fix": "added form ties, recessed apron panels, gate stiffeners and turbulence, but the stone went too light and ate the focal contrast"
            },
            {
                    "iter": 4,
                    "weighted": 7.44,
                    "weakest": "craft",
                    "fix": "darkened the stone and hoisted the lit gate leaf so the bay reads as open, but the shaft still read as a ramp"
            },
            {
                    "iter": 5,
                    "weighted": 7.84,
                    "weakest": "color",
                    "fix": "structural move: cropped in hard, 5 large bays instead of 7 small, and replaced the flat shaft with a ballistic falling nappe"
            },
            {
                    "iter": 6,
                    "weighted": 8.125,
                    "weakest": "craft",
                    "fix": "stone shifted into the violet family, headline cleared off the ridge, spray rebuilt as soft droplets, crest walkway added"
            },
            {
                    "iter": 7,
                    "weighted": 8.39,
                    "weakest": "craft",
                    "fix": "light now emerges from a shadowed head with jamb shading; chute walls cast onto the sheet; closed leaves deepened toward ink"
            },
            {
                    "iter": 8,
                    "weighted": 8.585,
                    "weakest": "none below 8.5",
                    "fix": "shipped: nappe filaments and standing ridges, weathering variation across the apron, bounce light onto the flanking piers"
            }
    ],
    "eval_final": {
            "weighted": 8.585,
            "scores": {
                    "concept": 8.5,
                    "focal": 9.0,
                    "composition": 8.5,
                    "color": 8.5,
                    "detail": 8.5,
                    "craft": 8.5,
                    "typography": 8.5,
                    "originality": 8.5,
                    "fidelity": 9.0
            },
            "bar": 8.5,
            "passed": true,
            "iterations_used": 8,
            "note": "Nominal skill budget is 6 eval iterations. Iterations 7 and 8 were taken deliberately under the routine's exhaustiveness mandate ('8.5 is the FLOOR, not the target; keep iterating while iterations are clearly buying quality') because the score was still climbing (7.84 -> 8.125 -> 8.39 -> 8.585). One script crash occurred between iterations 7 and 8 (rectangle coordinate ordering in the jamb-shading loop); it was fixed and re-run and does not count as an eval iteration."
    },
}
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
