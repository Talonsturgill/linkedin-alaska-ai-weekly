"""
Alaska.Ai — The Stack — 21 AUG 2026
"Cook Inlet, Banked / Before Alaska Can Object"

Concept: a hard-edged surveyed claim boundary platted across open tidewater,
with the Cook Inlet current pouring straight through it. Physically the line
is not there. Legally it is, and it is the only thing in frame that does not
move. Style family: hydrographic_claim (tidal streamline field x survey
cadastral linework). See out/art_plan.md for the full blueprint.
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image, ImageFilter
import art_kit as k

SEED = 1650  # the corridor acreage, per the dossier

D = k.DESIGN  # 1080

# ---------------------------------------------------------------- palette
PAPER   = "#f0eade"   # cold sand, type zone + brightest rip crests
WATER   = "#7d9187"   # slate green, dominant mass
DEEP    = "#374b43"   # troughs, current shadow
INK     = "#1b2622"   # shoreline wedge, wordmark
ACCENT  = "#c8552c"   # vermilion, claim linework + monuments
HALO    = "#3d1d12"   # dark stroke under accent (grayscale insurance)

PALETTE = [PAPER, WATER, DEEP, INK, ACCENT, HALO]

def lerp_pre(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


c = k.Canvas(bg=PAPER, ss=2)
rng = np.random.default_rng(SEED)

# ================================================================ 1-2. water
# Tonal field: warped fractal noise mapped paper -> deep, so the water has
# large slow value structure before a single streamline is drawn.
f = k.field(scale=2.6, octaves=5, seed=SEED)
f = k.warp(f, strength=88, scale=2.1, seed=SEED + 1)

# Density/darkness ramp: calm + pale upper-left, dense + dark lower-right.
yy, xx = np.mgrid[0:D, 0:D] / float(D)
ramp = np.clip((xx * 0.66 + yy * 0.62) - 0.14, 0, 1) ** 1.28
fw = np.clip(f * 0.42 + ramp * 0.94, 0, 1)

water_img = k.field_img(fw, k.mix(PAPER, WATER, 0.30), DEEP, gamma=1.02)
c.paste_img(water_img, alpha=1.0)

# ============================================================ 3-6. current
# Angle field for the tide. Quantised so the flow reads sculpted and tidal
# rather than smooth decorative Perlin, then given a slight constant curl.
# Dominant diagonal set-and-drift with large meanders plus fine shear, so the
# field braids like a tidal stream instead of falling like rain.
_n1 = k.field(scale=1.35, octaves=3, seed=SEED + 5)   # large meanders
_n2 = k.field(scale=4.20, octaves=4, seed=SEED + 6)   # fine shear
ang = (math.radians(203)
       + (_n1 - 0.5) * math.tau * 0.34
       + (_n2 - 0.5) * math.tau * 0.085)

# The claim overlay goes down BEFORE the current, so the water visibly runs
# over the top of it. Also removes the dead flat fill inside the parcel.
CX, CY = 628.0, 646.0
HW, HH = 215.0, 165.0
ROT = math.radians(-14.0)

def rot(px, py):
    dx, dy = px - CX, py - CY
    return (CX + dx * math.cos(ROT) - dy * math.sin(ROT),
            CY + dx * math.sin(ROT) + dy * math.cos(ROT))

corners = [rot(CX - HW, CY - HH), rot(CX + HW, CY - HH),
           rot(CX + HW, CY + HH), rot(CX - HW, CY + HH)]
k.poly(c, corners, fill=k.mix(WATER, PAPER, 0.13))
# faint interior survey hatching, meso structure inside the big shape
for t in range(1, 9):
    a = lerp_pre(corners[0], corners[3], t / 9.0)
    b = lerp_pre(corners[1], corners[2], t / 9.0)
    k.line(c, [a, b], k.mix(WATER, PAPER, 0.22), width=0.9)


def flow(n, length, width, color, alpha, seed, min_dist=0.0, curl=0.0,
         gate=None):
    """Trace streamlines and draw them, gated by the density ramp so the
    upper-left quiet zone stays open for type."""
    lines = k.streamlines(ang, n=n, step=3.2, length=length, seed=seed,
                          min_dist=min_dist, margin=0.18, curl=curl)
    for pts in lines:
        if not pts:
            continue
        mx = sum(p[0] for p in pts) / len(pts) / D
        my = sum(p[1] for p in pts) / len(pts) / D
        dens = np.clip(mx * 0.62 + my * 0.58 - 0.06, 0, 1)
        if gate is not None and rng.random() > gate(dens):
            continue
        w = width * (0.55 + 0.9 * dens)
        k.line(c, pts, color, width=max(0.7, w))

# MESO a: broad slow current bands, low contrast, establish direction
flow(120, (520, 980), 7.5, k.mix(WATER, DEEP, 0.30), 255, SEED + 11,
     min_dist=15.0, curl=0.0016, gate=lambda t: 0.30 + 0.70 * t)
# MESO a2: broad soft tonal sweeps, near-invisible individually, but they
# give the water body mass so the strands sit ON something
flow(70, (620, 1120), 17.0, k.mix(WATER, DEEP, 0.16), 255, SEED + 16,
     min_dist=26.0, curl=0.0012, gate=lambda t: 0.25 + 0.75 * t)
# MESO b: the main tidal texture
flow(430, (320, 760), 2.7, k.mix(WATER, DEEP, 0.62), 255, SEED + 12,
     min_dist=5.6, curl=0.0022, gate=lambda t: 0.16 + 0.84 * t)
# MESO c: darker deep threads, only in the dense field
flow(300, (240, 560), 2.0, k.mix(DEEP, INK, 0.35), 255, SEED + 13,
     min_dist=4.8, curl=0.0030, gate=lambda t: max(0.0, t * 1.15 - 0.22))
# Tide-rip crests: pale high-value shear lines, the sparkle of the piece
flow(110, (300, 700), 1.8, k.mix(PAPER, WATER, 0.22), 255, SEED + 14,
     min_dist=7.0, curl=0.0035, gate=lambda t: 0.10 + 0.72 * t)
# MICRO: fine hairline eddies, mid-field only
flow(240, (90, 240), 1.0, k.mix(WATER, DEEP, 0.78), 255, SEED + 15,
     min_dist=2.8, curl=0.010,
     gate=lambda t: 0.85 if 0.28 < t < 0.86 else 0.05)

# ============================================================== 7. silt/foam
mid_mask = Image.fromarray(
    (np.clip(ramp * 1.25 - 0.12, 0, 1) * 255).astype(np.uint8), "L")
k.stipple(c, mid_mask, density=0.055, r=(0.5, 1.35),
          color=k.mix(PAPER, WATER, 0.35), seed=SEED + 21)
k.chips(c, 150, (60, 300, D, D - 40), size=(2, 6),
        colors=(k.mix(DEEP, INK, 0.4), k.mix(WATER, DEEP, 0.5)),
        seed=SEED + 22, mask_img=mid_mask)

# ============================================================ 8-9. shoreline
# Kenai shore sliver, bottom-left. Dark anchor + the darkest value in frame.
def tilted_coast(y_base, amp, slope, seed, x1=880, scale=1.9, octaves=6):
    """Ridgeline with a linear tilt added so the shore runs off the BOTTOM
    edge on a diagonal instead of being cut by a vertical canvas seam."""
    pts = k.ridge_pts(y_base=y_base, amp=amp, scale=scale, octaves=octaves,
                      seed=seed, x0=-40, x1=x1, step=4)
    return [(x, y + (x + 40) * slope) for x, y in pts]

# outer wet-sand rim, palest land tone, reads as the tideline
rim = tilted_coast(796, 128, 0.34, SEED + 30)
rim = k.wobble_pts(rim, amp=6.5, scale=5.0, seed=SEED + 34)
k.poly(c, [(-40, D + 60)] + rim + [(880, D + 60)], fill=k.mix(DEEP, PAPER, 0.20))

# main landmass, darkest value in frame
coast = tilted_coast(824, 134, 0.34, SEED + 31)
coast = k.wobble_pts(coast, amp=5.2, scale=6.0, seed=SEED + 32)
k.poly(c, [(-40, D + 60)] + coast + [(880, D + 60)], fill=INK)

# interior tonal banding, meso structure inside the big dark shape
for bi, (yb, am, sl, tone) in enumerate([
        (896, 70, 0.325, 0.19), (968, 50, 0.315, 0.34)]):
    b = tilted_coast(yb, am, sl, SEED + 35 + bi, x1=840, scale=2.6, octaves=5)
    k.poly(c, [(-40, D + 60)] + b + [(840, D + 60)],
           fill=k.mix(INK, DEEP, tone))

# --- land surface detail: mask off the coast polygon and work into it
from PIL import ImageDraw as _ID
_lm = Image.new("L", (D, D), 0)
_ID.Draw(_lm).polygon([(-40, D + 60)] + [(int(x), int(y)) for x, y in coast]
                      + [(880, D + 60)], fill=255)
k.stipple(c, _lm, density=0.085, r=(0.5, 1.5),
          color=k.mix(INK, DEEP, 0.55), seed=SEED + 51)
k.stipple(c, _lm, density=0.030, r=(0.4, 1.0),
          color=k.mix(DEEP, PAPER, 0.30), seed=SEED + 52)
k.chips(c, 220, (-20, 700, 900, D), size=(2, 7),
        colors=(k.mix(INK, DEEP, 0.62), k.mix(INK, PAPER, 0.10)),
        seed=SEED + 53, mask_img=_lm)

# surf debris riding the tideline, micro life where land meets water
for i, (px, py) in enumerate(coast[::7]):
    if rng.random() < 0.55:
        rr = rng.uniform(0.8, 2.1)
        k.circle(c, px + rng.uniform(-5, 5), py + rng.uniform(1, 9), rr,
                 fill=k.mix(DEEP, PAPER, 0.42))

# substation glyph at the Bernice Lake landfall — micro built detail
sx, sy = 132, 858
k.poly(c, [(sx, sy), (sx + 34, sy), (sx + 34, sy + 17), (sx, sy + 17)],
       fill=k.mix(PAPER, WATER, 0.55))
for i in range(4):
    k.line(c, [(sx + 5 + i * 8, sy + 2), (sx + 5 + i * 8, sy + 15)],
           k.mix(DEEP, INK, 0.5), width=1.2)
# little pylon
k.line(c, [(sx + 46, sy + 18), (sx + 46, sy - 12)], k.mix(PAPER, WATER, 0.5), width=1.4)
k.line(c, [(sx + 39, sy - 8), (sx + 53, sy - 8)], k.mix(PAPER, WATER, 0.5), width=1.2)
k.line(c, [(sx + 42, sy - 12), (sx + 50, sy - 12)], k.mix(PAPER, WATER, 0.5), width=1.2)

# ======================================================= 10-12. claim parcel
def lerp(a, b, t):
    return lerp_pre(a, b, t)

# dark halo stroke first — this is what keeps the accent alive in grayscale
for i in range(4):
    a, b = corners[i], corners[(i + 1) % 4]
    k.line(c, [(a[0] + 2.0, a[1] + 2.4), (b[0] + 2.0, b[1] + 2.4)],
           HALO, width=4.6)
# the ruled claim edge
for i in range(4):
    a, b = corners[i], corners[(i + 1) % 4]
    k.line(c, [a, b], ACCENT, width=2.5)

# dimension ticks every ~42px, perpendicular, outward
for i in range(4):
    a, b = corners[i], corners[(i + 1) % 4]
    seg = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uy = (b[0] - a[0]) / seg, (b[1] - a[1]) / seg
    nx, ny = -uy, ux
    n_ticks = int(seg // 42)
    for t in range(1, n_ticks + 1):
        p = lerp(a, b, t / (n_ticks + 1))
        k.line(c, [(p[0] + 2.0, p[1] + 2.4),
                   (p[0] + nx * 7 + 2.0, p[1] + ny * 7 + 2.4)], HALO, width=3.0)
        k.line(c, [p, (p[0] + nx * 7, p[1] + ny * 7)], ACCENT, width=1.6)

# corner monuments — filled squares with a tick cross. Upper-left is FOCAL.
for idx, (mx, my) in enumerate(corners):
    r = 6.0 if idx != 0 else 7.5
    k.poly(c, [(mx - r - 1.4, my - r + 1.6), (mx + r - 1.4, my - r + 1.6),
               (mx + r - 1.4, my + r + 1.6), (mx - r - 1.4, my + r + 1.6)],
           fill=HALO)
    k.poly(c, [(mx - r, my - r), (mx + r, my - r),
               (mx + r, my + r), (mx - r, my + r)], fill=ACCENT)
    k.line(c, [(mx - r - 5, my), (mx + r + 5, my)], ACCENT, width=1.3)
    k.line(c, [(mx, my - r - 5), (mx, my + r + 5)], ACCENT, width=1.3)

# focal emphasis: a whisper of glow at the upper-left monument only
k.glow(c, corners[0][0], corners[0][1], 62, ACCENT, alpha=34)

# ============================================================ 13. mono labels
def leader(p_from, p_to, color):
    k.line(c, [(p_from[0] + 1.6, p_from[1] + 1.8),
               (p_to[0] + 1.6, p_to[1] + 1.8)], HALO, width=2.6)
    k.line(c, [p_from, p_to], color, width=1.3)

# acreage, tagged off the lower edge into open water
acre_edge = lerp(corners[3], corners[2], 0.30)
acre_pt = (acre_edge[0] - 96, acre_edge[1] + 92)
leader(acre_edge, acre_pt, ACCENT)
k.chip(c, (acre_pt[0] - 6, acre_pt[1] + 4), "≈1,650 ACRES", k.mono(c, 16),
       ACCENT, HALO, pad=8, anchor="ra", tracking=0.20)

# what the instrument actually confers, tagged off the upper edge
pr_edge = lerp(corners[0], corners[1], 0.26)
pr_pt = (302.0, 452.0)
leader(pr_edge, (pr_pt[0] + 150, pr_pt[1] + 16), ACCENT)
k.chip(c, (pr_pt[0], pr_pt[1]), "PRIORITY ONLY · NO CONSTRUCTION RIGHT",
       k.mono(c, 12), ACCENT, HALO, pad=8, anchor="la", tracking=0.15)

# ============================================================ 14-15. finish
k.grain(c, amount=6.0, seed=SEED + 41)
k.vignette(c, strength=0.14, spread=1.40)

# ================================================================== 16. type
# Quiet zone is upper-left by construction (density ramp). Headline sits in it.
hl1 = k.fraunces(c, 96, weight=900, opsz=144)
hl2 = k.fraunces(c, 96, weight=900, opsz=144)
k.text(c, (88, 104), "COOK INLET,", hl1, INK, anchor="la", tracking=0.012)
k.text(c, (88, 202), "BANKED", hl2, ACCENT, anchor="la", tracking=0.012)

k.text(c, (90, 322), "BEFORE ALASKA CAN OBJECT",
       k.fraunces(c, 27, weight=600, opsz=72), INK,
       anchor="la", tracking=0.055)

k.text(c, (90, 372), "THE STACK · REGULATORY · 21 AUG 2026",
       k.mono(c, 15), k.mix(INK, DEEP, 0.45), anchor="la", tracking=0.24)

k.text(c, (992, 1006), "ALASKA.AI", k.fraunces(c, 30, weight=900, opsz=144),
       PAPER, anchor="rs", tracking=0.045)

k.polaris(c, 978, 96, r=13, color="#e8b23c", core="#fff3d2", halo=0.30)

# ===================================================================== meta
c.finish("out/post_image.png", {
    "date": "21 AUG 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "REGULATORY",
    "byline": "",
    "headline": "Cook Inlet, Banked / Before Alaska Can Object",
    "style_family": "hydrographic_claim",
    "palette": PALETTE,
    "hue_family": "green",
    "composition": "offset_parcel_drift",
    "motifs": ["surveyed claim quadrilateral over open water",
               "tidal current streamlines", "corner monuments and dimension ticks",
               "Kenai shore sliver", "Bernice Lake substation glyph"],
    "technique_stack": ["field", "warp", "angle_field", "streamlines",
                        "stipple", "chips", "ridge_pts", "wobble_pts",
                        "poly", "glow", "grain", "vignette", "polaris"],
    "seed": SEED,
    "eval_history": [{"iter": 1, "weighted": 6.72, "weakest": "craft", "note": "current read as RAIN not tide (quantized near-vertical angle field); wordmark invisible on dark landmass; straight vertical cut in coast; parcel interior dead flat fill"}, {"iter": 2, "weighted": 7.35, "weakest": "craft", "note": "rebuilt angle field as diagonal set-and-drift with large meanders + fine shear; parcel tint moved UNDER the current so water runs over the claim; braided/curled streamlines"}, {"iter": 3, "weighted": 7.9, "weakest": "craft", "note": "hand-rolled rotated label plates did not register with text rotation; replaced with kit chips + leader lines; fixed 'COOKINLET,' collapse from negative tracking"}, {"iter": 4, "weighted": 8.28, "weakest": "craft", "note": "PRIORITY chip was clipped by right canvas edge, moved into open-water band above parcel; coast slope shallowed and wobble raised to break the ruled look"}, {"iter": 5, "weighted": 8.45, "weakest": "detail", "note": "coast polygons run off the bottom edge, killing the vertical wall artifact; added broad low-contrast tonal sweeps to give the water body mass"}, {"iter": 6, "weighted": 8.565, "weakest": "craft", "note": "landmass was the last near-flat region; added stipple tooth, rock chips, tideline surf debris, stronger interior banding"}],
    "eval_final": {"weighted": 8.565, "scores": {"concept": 8.5, "focal": 8.5, "composition": 8.5, "color": 8.5, "detail": 8.5, "craft": 8.5, "typography": 9, "originality": 8.5, "fidelity": 9}, "bar": 8.5, "passed": true, "note": "Above the 8.5 floor with no dimension below 7. Six iterations; the first render was well short and every pass was a targeted fix of the weakest dimension."},
})
print("wrote out/post_image.png")
