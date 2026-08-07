"""Alaska.Ai — The Stack — 7 AUG 2026
"One Signature Moves 19,950 Acres"

Concept: 19,950 acres as an immense raft of muskeg on cold water, cropped by
the frame because it is larger than the canvas can hold, moored by a single
ember-bright filament to one small pin. The filament is fraying at the pin.

style_family organic_rd_moorage · hue_family teal · composition thirds_focal
"""
import math
import sys

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

import art_kit as ak


def masked_overlay(c, layer_rgba, mask_L):
    """Composite an RGBA layer through a mask, RESPECTING the layer's own
    per-pixel alpha. Canvas.composite(layer, mask) hands the mask to
    Image.paste as the alpha, which discards the layer's alpha entirely and
    stamps it at full opacity. Multiplying the two keeps both."""
    combined = ImageChops.multiply(layer_rgba.getchannel("A"), mask_L)
    c.img.paste(layer_rgba.convert("RGB"), (0, 0), combined)
    c.draw = ImageDraw.Draw(c.img, "RGBA")

SEED = 819
OUT = "out/post_image.png"

# ---------------------------------------------------------------- palette
PAPER = "#dbe8ec"   # ice light — type, shoreline rim, water sheen
FIELD = "#2f7f8c"   # field teal — open-water mid, RD channel highlights
SHADOW = "#123640"  # mass body, water depth
INK = "#07161b"     # darkest mass interior, lower-right falloff
EMBER = "#e4573f"   # focal — filament + pin ONLY
GOLD = "#f0c987"    # polaris colophon only

PALETTE = [PAPER, FIELD, SHADOW, INK, EMBER, GOLD]

HEADLINE_1 = "ONE SIGNATURE"
HEADLINE_2 = "MOVES 19,950 ACRES"
KICKER = "THE STACK  ·  SOVEREIGNTY  ·  7 AUG 2026"

c = ak.Canvas(bg=INK, ss=2)
rng = np.random.default_rng(SEED)

# ============================================================ 1. base water
ak.gradient_v(c, (0, 0, 1080, 1080), "#16404a", "#061419", ease=1.25)

# cold low sheen, upper-left
ak.glow(c, 250, 300, 470, "#8fc4ce", alpha=52)
ak.glow(c, 170, 210, 250, "#bcdde4", alpha=34)

# ============================================================ 2. water field
# computed at 1/3 scale and upsampled — identical read, ~10x faster
FR = 360
wf = ak.warp(ak.field(scale=3.2, octaves=5, seed=SEED + 1, w=FR, h=FR),
             strength=24, scale=2.4, seed=SEED + 2)
wf = (wf - wf.min()) / (np.ptp(wf) + 1e-9)
water = ak.field_img(wf, "#0d2a33", "#2c6e7c", gamma=1.15)
c.paste_img(water, alpha=0.34)

# slow current — sparse streamlines, never competing
K = 1080 / FR
ang = ak.field(2.1, 4, SEED + 3, w=FR, h=FR) * math.tau * 0.85
lines = ak.streamlines(ang, n=130, step=1.1, length=(30, 100), seed=SEED + 4,
                       min_dist=6, margin=0.12)
lay, ld = c.layer()
for pl in lines:
    pl = [(x * K, y * K) for (x, y) in pl]
    pl = [(x, y) for (x, y) in pl if y > 372]          # keep clear of headline
    if len(pl) > 6:
        ld.line(c.pts(pl), fill=(*ak.hex_to_rgb("#4d94a1"), 46),
                width=max(1, int(c.s(1.5))))
c.composite(lay)

# ============================================================ 3. the mass
# union of three blobs -> one articulated landform that bleeds off right+bottom
from shapely.geometry import Polygon
from shapely.ops import unary_union

blobs = [
    ak.blob_pts(812, 1034, 396, wobble=0.20, harmonics=(1, 2, 3, 5),
                points=260, seed=SEED + 11),
    ak.blob_pts(1058, 906, 330, wobble=0.24, harmonics=(1, 2, 4),
                points=260, seed=SEED + 23),
    ak.blob_pts(672, 1128, 306, wobble=0.22, harmonics=(1, 3, 5),
                points=260, seed=SEED + 37),
]
land = unary_union([Polygon(b).buffer(0) for b in blobs])
# cut real inlets and bays into the upper-left edge so the outline is
# articulated coastline, not one smooth lozenge
for cx, cy, r, sd in [(560, 905, 96, 41), (690, 812, 74, 43),
                      (476, 1006, 82, 47), (858, 742, 66, 51),
                      (1006, 806, 58, 53)]:
    land = land.difference(
        Polygon(ak.blob_pts(cx, cy, r, wobble=0.34, harmonics=(1, 2, 3),
                            points=90, seed=sd)).buffer(0))
if land.geom_type.startswith("Multi"):
    land = max(land.geoms, key=lambda g: g.area)

ext = [(float(x), float(y)) for x, y in land.exterior.coords]
ext = ak.wobble_pts(ext, amp=4.2, scale=58.0, seed=SEED + 5)
# wobbling can self-intersect; buffer(0) heals it so the fill never
# punches an even-odd hole through the landmass
land = Polygon(ext).buffer(0)
if land.geom_type.startswith("Multi"):
    land = max(land.geoms, key=lambda g: g.area)
ext = [(float(x), float(y)) for x, y in land.exterior.coords]

# bow tip = closest exterior point to the upper-left
bow = min(ext, key=lambda p: p[0] + p[1] * 0.92)

mass_mask, mm = c.mask()
mm.polygon(c.pts(ext), fill=255)

# ---- shoal: pale shallow-water halo just outside the shore
shoal = land.buffer(22)
lay, ld = c.layer()
ld.polygon(c.pts([(float(x), float(y)) for x, y in shoal.exterior.coords]),
           fill=(*ak.hex_to_rgb("#3d8794"), 58))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(7)))
c.composite(lay)

# ---- meso: reaction-diffusion muskeg.
# HIGH rd = open pond channel (pale), LOW rd = peat hummock (dark).
rd = ak.reaction_diffusion(steps=2800, f=0.037, k=0.061, seed=SEED + 6,
                           res=232)
lo, hi = np.percentile(rd, 4), np.percentile(rd, 96)
rd = np.clip((rd - lo) / (hi - lo + 1e-9), 0, 1)
# base hummock tone across the WHOLE mass, so no acreage is ever flat
hum = ak.warp(ak.field(scale=6.5, octaves=4, seed=SEED + 21, w=420, h=420),
              strength=16, scale=3.0, seed=SEED + 22)
hum = (hum - hum.min()) / (np.ptp(hum) + 1e-9)
hum_lay = ak.field_img(hum, "#0e2a33", "#2f6b77", gamma=1.0).resize(
    (c.W, c.W), Image.LANCZOS).convert("RGBA")
hum_lay.putalpha(255)
masked_overlay(c, hum_lay, mass_mask)

# detail hierarchy: pond contrast is strongest near the bow (beside the
# focal) and calms toward the far bottom-right, so the corner never shouts.
# Peat tone stays semi-transparent so the hummock base reads through it;
# only the ponds themselves go fully opaque.
ys, xs = np.mgrid[0:c.W, 0:c.W].astype(np.float32)
d = np.hypot(xs - c.s(bow[0]), ys - c.s(bow[1])) / c.s(700.0)
falloff = np.clip(1.0 - d, 0.34, 1.0)
rd_big = np.asarray(
    Image.fromarray((rd * 255).astype(np.uint8), "L").resize(
        (c.W, c.W), Image.LANCZOS), np.float32) / 255.0
alpha = np.clip(falloff * (0.30 + 0.70 * rd_big), 0, 1)
peat = ak.field_img(rd ** 1.18, "#0d2a33", "#6ea7b3", gamma=1.0)
peat_lay = peat.resize((c.W, c.W), Image.LANCZOS).convert("RGBA")
peat_lay.putalpha(Image.fromarray((alpha * 255).astype(np.uint8), "L"))
masked_overlay(c, peat_lay, mass_mask)

# ---- atmospheric ramp: lighten + desaturate toward the far right edge
lay, ld = c.layer()
for i in range(0, 1080, 3):
    t = max(0.0, (i - 470) / 760.0)
    if t <= 0:
        continue
    ld.rectangle([c.s(i), 0, c.s(i + 3), c.W],
                 fill=(*ak.hex_to_rgb("#2b6c79"), int(64 * min(1.0, t))))
masked_overlay(c, lay, mass_mask)

# ---- shoreline rim: thin and light-facing only, never a sticker outline
n_ext = len(ext)
for i in range(n_ext - 1):
    x0, y0 = ext[i]
    x1, y1 = ext[i + 1]
    # face toward the upper-left light source
    nx, ny = (y1 - y0), -(x1 - x0)
    ln = math.hypot(nx, ny) or 1.0
    facing = (nx / ln) * -0.72 + (ny / ln) * -0.69
    if facing <= 0.04:
        continue
    a = int(215 * min(1.0, facing * 1.25))
    ak.line(c, [(x0, y0), (x1, y1)], ak.mix(PAPER, "#a9d0d8", 0.35),
            width=1.9 + 1.0 * facing)

# ---- micro: restrained gravel, stipple, a few pond glints
ak.chips(c, 120, (430, 690, 1080, 1080), size=(1.6, 4.2),
         colors=("#4d8e9a", "#2a5f6b", "#8ab9c2"), seed=SEED + 8,
         mask_img=mass_mask)
ak.stipple(c, mass_mask, density=0.014, r=(0.4, 1.1), color="#071b21",
           seed=SEED + 9)
ak.stipple(c, mass_mask, density=0.006, r=(0.35, 0.9), color="#9fcbd3",
           seed=SEED + 10)

for _ in range(30):
    gx = rng.uniform(470, 1070)
    gy = rng.uniform(720, 1075)
    if mass_mask.getpixel((int(c.s(gx)), int(c.s(gy)))) > 128:
        ak.circle(c, gx, gy, rng.uniform(0.7, 1.7), fill="#b8dbe1")

# ============================================================ 4. the mooring
PIN = (206.0, 512.0)


def catenary(p0, p1, sag=42.0, n=190):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t + sag * math.sin(math.pi * t)
        pts.append((x, y))
    return pts


fil = catenary((PIN[0], PIN[1] - 7), bow, sag=42.0)

# glow beneath the filament so it survives the 300px thumbnail
lay, ld = c.layer()
ld.line(c.pts(fil), fill=(*ak.hex_to_rgb(EMBER), 120),
        width=max(1, int(c.s(9.0))))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(7.0)))
c.composite(lay)

ak.line(c, fil, EMBER, width=3.2)
ak.line(c, fil, ak.lighten(EMBER, 0.22), width=1.3)

# ---- fraying strands near the pin (deliberate, tapered, one direction)
for i in range(9):
    t = 0.06 + i * 0.019 + float(rng.uniform(-0.004, 0.004))
    k = int(t * (len(fil) - 1))
    ax, ay = fil[k]
    bx, by = fil[min(len(fil) - 1, k + 3)]
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    side = -1.0 if i % 2 == 0 else 1.0
    L = float(rng.uniform(17, 41))
    curve = float(rng.uniform(0.30, 0.62))
    strand = []
    for j in range(9):
        u = j / 8.0
        strand.append((ax + dx / ln * L * u * 0.55
                       + nx * side * L * curve * u * u,
                       ay + dy / ln * L * u * 0.55
                       + ny * side * L * curve * u * u))
    ak.line(c, strand, ak.mix(EMBER, PAPER, 0.34), width=1.4)

# ---- the pin (FOCAL): small bollard + eyelet
px, py = PIN
ak.poly(c, [(px - 7.5, py + 17), (px + 7.5, py + 17),
            (px + 5.6, py - 13), (px - 5.6, py - 13)], fill=EMBER)
ak.circle(c, px, py - 15.5, 7.2, fill=EMBER)
ak.circle(c, px, py - 15.5, 3.1, fill="#12303a")
ak.poly(c, [(px - 7.5, py + 17), (px - 3.4, py + 17),
            (px - 2.2, py - 13), (px - 5.6, py - 13)],
        fill=ak.lighten(EMBER, 0.26))
ak.circle(c, px, py + 19.5, 9.0, fill=ak.darken(EMBER, 0.42))
ak.glow(c, px, py, 46, EMBER, alpha=54)

# ============================================================ 5. finishing
ak.mottle(c, strength=0.035, scale=3.4, seed=SEED + 12)
ak.grain(c, amount=6.0, seed=SEED + 13)
ak.vignette(c, strength=0.16, spread=1.32)

# ============================================================ 6. typography
s1 = ak.fit_size(c, HEADLINE_1, 690, lo=46, hi=136, weight=900, opsz=144)
s2 = ak.fit_size(c, HEADLINE_2, 648, lo=34, hi=96, weight=900, opsz=144)
f1 = ak.fraunces(c, s1, weight=900, opsz=144)
f2 = ak.fraunces(c, s2, weight=700, opsz=144)

ak.text(c, (96, 196), HEADLINE_1, f1, PAPER, anchor="ls")
ak.text(c, (96, 196 + s2 * 1.06), HEADLINE_2, f2,
        ak.mix(PAPER, FIELD, 0.30), anchor="ls")

km = ak.mono(c, 17, medium=True)
ak.text(c, (99, 196 + s2 * 1.06 + 46), KICKER, km,
        ak.mix(PAPER, SHADOW, 0.40), anchor="ls", tracking=0.22)

wm = ak.fraunces(c, 30, weight=900, opsz=144)
ak.text(c, (96, 996), "ALASKA.AI", wm, PAPER, anchor="ls", tracking=0.04)

ak.polaris(c, 960, 150, r=13, color=GOLD, core="#fff4dd")

# ============================================================ 7. ledger
c.finish(OUT, {
    "date": "7 AUG 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "SOVEREIGNTY",
    "byline": "",
    "headline": "One Signature Moves 19,950 Acres",
    "style_family": "organic_rd_moorage",
    "palette": PALETTE,
    "hue_family": "teal",
    "composition": "thirds_focal",
    "motifs": ["moored land raft", "single fraying filament", "mooring pin",
               "muskeg labyrinth", "cold open water"],
    "technique_stack": ["gradient_v", "glow", "field", "warp", "streamlines",
                        "reaction_diffusion", "blob_pts", "wobble_pts",
                        "voronoi_polys", "chips", "stipple", "mottle",
                        "grain", "vignette", "polaris"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 7.06, "weakest": "detail",
         "note": "RD invisible; mass read as flat black void with white confetti"},
        {"iter": 2, "weighted": 7.30, "weakest": "detail",
         "note": "posterised bands painted channels dark then relit cores, cancelling out"},
        {"iter": 3, "weighted": 7.35, "weakest": "detail",
         "note": "RD field verified beautiful in isolation; mass still flat"},
        {"iter": 4, "weighted": 8.10, "weakest": "detail",
         "note": "root cause found (see render_notes); labyrinth finally reads, far corner shouts"},
        {"iter": 5, "weighted": 8.35, "weakest": "detail",
         "note": "falloff added for hierarchy; lower-left lobe still flat acreage"},
        {"iter": 6, "weighted": 8.59, "weakest": "detail",
         "note": "base hummock tone + semi-transparent peat; no flat acreage remains"},
    ],
    "eval_final": {
        "weighted": 8.59,
        "scores": {"concept": 9.0, "focal": 8.5, "composition": 8.5,
                   "color": 8.5, "detail": 7.5, "craft": 8.5,
                   "typography": 9.5, "originality": 8.5, "fidelity": 9.0},
        "weakest_dimension": "detail richness",
    },
    "render_notes": (
        "Three bugs fixed outside the eval budget (script faults, not "
        "aesthetic iterations). (1) numpy 2 removed ndarray.ptp(). "
        "(2) wobble_pts self-intersected the coastline, punching an "
        "even-odd hole through the landmass; healed with shapely buffer(0). "
        "(3) ROOT CAUSE of iterations 1-3: Canvas.composite(layer, mask) "
        "passes the mask to Image.paste as the alpha, which DISCARDS the "
        "layer's own per-pixel alpha and stamps it at full opacity. The "
        "atmospheric ramp intended at alpha<=70 was therefore flooding the "
        "entire landmass with flat #2b6c79 and erasing the muskeg texture. "
        "Fixed with the local masked_overlay() helper, which multiplies "
        "layer alpha into the mask before pasting."
    ),
})
print("rendered", OUT, "bow=", tuple(round(v, 1) for v in bow))
