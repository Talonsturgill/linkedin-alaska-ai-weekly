"""Anchorage Desk — 2026-07-31 — bespoke cover.

Concept: four hub communities on a low winter horizon, each holding one taut
thread to a single satellite node, while the terrestrial line between them lies
visibly broken. Redundancy bought from one vendor is still a single point.

Style: wpa_layered / minimal_line hybrid. Composition: horizon_band. Hue: orange.
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import ImageChops
from art_kit import (Canvas, field, field_mask, gradient_v, ridge_fill, ridge_pts,
                     hand_line, wobble_pts, line, poly, circle, chips, stipple,
                     hatch, glow, polaris, mottle, grain, vignette, text, chip,
                     fraunces, mono, fit_size, measure, mix, lighten, darken)

SEED = 611  # 11 June, the decision date

# ---------------------------------------------------------------- palette
PAPER   = "#f6e6d2"   # type light / horizon high-light
GLOW    = "#e07a3c"   # horizon band, dominant hue (orange)
EMBER   = "#a8492c"   # mid sky warm shadow, thread ink
FAR     = "#3a2c3a"   # far land band / upper sky mid
NEAR    = "#171320"   # near land, ink
ACCENT  = "#ffeede"   # satellite body, settlement lights
SKYTOP  = "#241d2c"

HORIZON = 726.0
NODE    = (806.0, 322.0)
# uneven spacing so the four hubs read as geography, not as a chart
HUBS    = [(150.0, 706.0), (372.0, 704.0), (606.0, 709.0), (918.0, 703.0)]

c = Canvas(bg=PAPER, ss=2)
rng = np.random.default_rng(SEED)

def fade(lay, t):
    """Scale ONLY the alpha channel. Calling .point() on an RGBA layer scales
    R, G, B and A together, which darkens the colour toward black instead of
    making it translucent."""
    a = lay.getchannel("A").point(lambda p, t=t: int(p * t))
    out = lay.copy()
    out.putalpha(a)
    return out


def clip(lay, mask, t=1.0):
    """Composite a partial layer inside a region mask.

    Canvas.composite(layer, mask) calls img.paste(layer, mask), which uses the
    MASK alone and ignores the layer's own alpha, so every transparent pixel
    inside the mask gets pasted as solid black. Multiply the layer's alpha into
    the mask so only what was actually drawn lands."""
    a = lay.getchannel("A")
    if t != 1.0:
        a = a.point(lambda p, t=t: int(p * t))
    c.composite(lay, ImageChops.multiply(a, mask))


# ---------------------------------------------------------------- 1. sky
gradient_v(c, (0, 0, 1080, HORIZON), SKYTOP, GLOW, ease=1.7)

# low cloud slivers: soft, irregular, PARTIAL width, hugging the horizon only.
# Deliberately not full-width strata (that reads as posterized gradient banding).
from PIL import Image, ImageFilter, ImageDraw, ImageChops
_cr = np.random.default_rng(SEED + 11)
for (yc, x0, x1, hgt, t) in [(596, -40, 430, 15, 0.30), (642, 250, 760, 11, 0.26),
                             (664, 620, 1130, 17, 0.32), (690, 60, 520, 10, 0.24),
                             (700, 700, 1120, 12, 0.22), (566, 540, 900, 12, 0.20)]:
    lay, ld = c.layer()
    xs = np.linspace(x0, x1, 40)
    ph = _cr.uniform(0, 6.28)
    top = [(x, yc - hgt * 0.5 - 4 * math.sin(x / 61.0 + ph)) for x in xs]
    bot = [(x, yc + hgt * 0.5 + 4 * math.sin(x / 47.0 + ph)) for x in xs][::-1]
    poly(c, top + bot, fill=mix(GLOW, PAPER, 0.30), d=ld)
    lay = lay.filter(ImageFilter.GaussianBlur(c.s(7)))
    c.composite(fade(lay, t))

# stars: few, dim, top band only. Kept deliberately sparse so this never reads
# as the legacy aurora/starfield template.
for _ in range(52):
    sx = _cr.uniform(0, 1080)
    sy = _cr.uniform(8, 300)
    r = _cr.uniform(0.7, 1.5)
    a = 0.30 + 0.34 * _cr.random() * (1.0 - sy / 320.0)
    circle(c, sx, sy, r, fill=mix(SKYTOP, PAPER, max(0.10, a)))

# ---------------------------------------------------------------- 2. focal halo
glow(c, NODE[0], NODE[1], 108, ACCENT, alpha=52)
glow(c, NODE[0], NODE[1], 46, ACCENT, alpha=64)

# ---------------------------------------------------------------- 3. land bands
SNOW_HI = "#6d6484"   # lit snow plain, catches sky light
SNOW_LO = "#443e57"   # snow in shadow, just under the crest

ridge_fill(c, 712, 24, FAR, scale=3.4, octaves=4, seed=SEED + 1, bottom=1080)
ridge_fill(c, 758, 30, mix(FAR, NEAR, 0.55), scale=2.8, octaves=4, seed=SEED + 2, bottom=1080)
# the foreground is a dusk-lit SNOW PLAIN, not a black slab: mid value, cool,
# so the warm settlement lamps and the cold steel route both read against it
ridge_fill(c, 812, 26, SNOW_LO, scale=2.2, octaves=5, seed=SEED + 4, bottom=1080)

near_pts = ridge_pts(812, 26, 2.2, 5, SEED + 4)
nm = Image.new("L", (c.W, c.W), 0)
nd = ImageDraw.Draw(nm)
nd.polygon(c.pts(near_pts + [(1080, 1080), (0, 1080)]), fill=255)

# the plain lightens toward the viewer as it catches more sky
lay, ld = c.layer()
gradient_v(c, (0, 812, 1080, 1080), SNOW_LO, SNOW_HI, ease=0.75, d=ld)
clip(lay, nm)

# warm rim-light on each crest facing the horizon glow
for (yb, amp, sc, oc, sd, col, w) in [(712, 24, 3.4, 4, SEED + 1, mix(GLOW, PAPER, 0.34), 3),
                                      (758, 30, 2.8, 4, SEED + 2, mix(GLOW, EMBER, 0.50), 3),
                                      (812, 26, 2.2, 5, SEED + 4, mix(GLOW, PAPER, 0.42), 3)]:
    line(c, ridge_pts(yb, amp, sc, oc, sd), col, width=w)

# meso: two very soft broad swells so the plain is not one flat value.
# Deliberately low contrast and only two, because evenly spaced full-width
# bands read as ruled stripes rather than as snow.
for k, (dy, amp, sc, sd) in enumerate([(96, 17, 1.7, SEED + 31), (232, 13, 1.4, SEED + 33)]):
    dp = ridge_pts(812 + dy, amp, sc, 4, sd)
    lay, ld = c.layer()
    poly(c, dp + [(1080, 1080), (0, 1080)],
         fill=mix(SNOW_HI, PAPER, 0.09 + 0.04 * k), d=ld)
    clip(lay, nm, 0.30)

# meso: sastrugi. Wind-carved snow reads as scattered lens-shaped drifts with a
# lit windward edge and a cool lee shadow, all raked the same direction.
_dr = np.random.default_rng(SEED + 38)
for _ in range(104):
    dx = _dr.uniform(-40, 1120)
    dy = _dr.uniform(826, 1076)
    depth = (dy - 812) / 268.0            # nearer drifts are bigger
    dl = _dr.uniform(26, 78) * (0.45 + depth)
    dh = dl * _dr.uniform(0.10, 0.19)
    tilt = _dr.uniform(-0.10, 0.04)
    pts = []
    for s in range(15):
        a = math.pi * s / 14.0
        pts.append((dx + math.cos(a) * dl, dy - math.sin(a) * dh + tilt * (math.cos(a) * dl)))
    for s in range(15):
        a = math.pi * (1.0 - s / 14.0)
        pts.append((dx + math.cos(a) * dl * 0.92,
                    dy + math.sin(a) * dh * 0.55 + tilt * (math.cos(a) * dl)))
    lay, ld = c.layer()
    _v = _dr.random()
    _fill = (mix(SNOW_HI, PAPER, 0.26 + 0.30 * _v) if _v > 0.34
             else mix(SNOW_LO, SNOW_HI, 0.30 + 0.40 * _v))
    poly(c, pts, fill=_fill, d=ld)
    clip(lay, nm, 0.30 + 0.24 * depth)
    # lee shadow hugging the underside
    line(c, [(dx - dl * 0.86, dy + dh * 0.34 + tilt * -dl * 0.86),
             (dx, dy + dh * 0.52), (dx + dl * 0.86, dy + dh * 0.30 + tilt * dl * 0.86)],
         mix(SNOW_LO, NEAR, 0.22), width=2)

# rock outcrops and willow scrub breaking the drifts
_rr = np.random.default_rng(SEED + 35)
for _ in range(16):
    ox = _rr.uniform(24, 1056)
    oy = _rr.uniform(950, 1054)
    ow = _rr.uniform(7, 17)
    oh = _rr.uniform(4, 9)
    poly(c, [(ox - ow, oy + oh), (ox - ow * 0.5, oy - oh), (ox + ow * 0.3, oy - oh * 0.6),
             (ox + ow, oy + oh)], fill=mix(NEAR, SNOW_LO, 0.30))
    line(c, [(ox - ow * 0.5, oy - oh), (ox + ow * 0.3, oy - oh * 0.6)],
         mix(GLOW, PAPER, 0.25), width=2)

stipple(c, nm, density=0.028, r=(0.5, 1.4), color=mix(SNOW_HI, PAPER, 0.55), seed=SEED + 37)
chips(c, 120, (0, 830, 1080, 1080), size=(2, 4),
      colors=(mix(SNOW_HI, PAPER, 0.30), mix(SNOW_LO, EMBER, 0.20)),
      seed=SEED + 5, mask_img=nm)

# spruce stand along the mid crest, reading as a stand rather than a fringe
mid_crest = ridge_pts(758, 30, 2.8, 4, SEED + 2)
_sr = np.random.default_rng(SEED + 36)
for _ in range(46):
    tx = _sr.uniform(-10, 1090)
    ty = np.interp(tx, [p[0] for p in mid_crest], [p[1] for p in mid_crest]) + _sr.uniform(0, 5)
    th = _sr.uniform(16, 34)
    tw = th * _sr.uniform(0.18, 0.26)
    poly(c, [(tx, ty - th), (tx + tw, ty + 2), (tx - tw, ty + 2)],
         fill=mix(NEAR, "#000000", 0.35))
    line(c, [(tx, ty - th), (tx - tw * 0.75, ty + 1)], mix(GLOW, NEAR, 0.55), width=1)

# mid band gets its own quieter grit
mid_pts = ridge_pts(762, 34, 2.8, 4, SEED + 2)
mm = Image.new("L", (c.W, c.W), 0)
md = ImageDraw.Draw(mm)
md.polygon(c.pts(mid_pts + [(1080, 1080), (0, 1080)]), fill=255)
chips(c, 170, (0, 756, 1080, 880), size=(2, 5),
      colors=(mix(FAR, PAPER, 0.12),), seed=SEED + 6, mask_img=mm)

# ---------------------------------------------------------------- 4. broken ground stitch
# The terrestrial line: cold steel against the warm scene so the broken half of
# the metaphor is a co-star, not a whisper. Three unmistakable severed gaps.
STITCH_Y = 886.0
GAPS = [(238, 322), (474, 556), (726, 806)]
STEEL = "#93a8bd"


def sy(x):
    return STITCH_Y + 9.0 * math.sin(x / 104.0) + 3.5 * math.sin(x / 33.0)


# soft graded shadow under the route so the steel reads off its own bed
for w, off, tone in ((11, 8, 0.14), (7, 6, 0.26), (4, 4, 0.42)):
    line(c, [(x, sy(x) + off) for x in np.arange(-20, 1100, 8.0)],
         mix(SNOW_LO, NEAR, tone), width=w)

x = 18.0
while x < 1062:
    seg = 26.0
    x2 = min(x + seg, 1062)
    if not any(g0 - 8 < x < g1 for g0, g1 in GAPS):
        line(c, [(xx, sy(xx)) for xx in np.linspace(x, x2, 5)], STEEL, width=5)
        line(c, [(xx, sy(xx) - 2) for xx in np.linspace(x, x2, 5)],
             mix(STEEL, PAPER, 0.45), width=2)
    x += seg + 12.0

# severed ends: frayed steel strands curling back from each void
for g0, g1 in GAPS:
    for gx, d in ((g0, -1), (g1, 1)):
        for k in range(4):
            fx = gx + d * (9 + 7 * k)
            line(c, [(gx, sy(gx)), ((gx + fx) / 2, sy(gx) + (k - 1.5) * 5.0),
                     (fx, sy(fx) + (k - 1.5) * 9.0)],
                 mix(STEEL, NEAR, 0.25 + 0.12 * k), width=2)

# relay towers standing over the route, one beside each void
for tx in (206.0, 596.0, 856.0):
    ty = sy(tx)
    line(c, [(tx, ty + 2), (tx, ty - 62)], STEEL, width=4)
    line(c, [(tx - 17, ty + 2), (tx, ty - 62), (tx + 17, ty + 2)],
         mix(STEEL, NEAR, 0.30), width=3)
    for k in (0.34, 0.62):
        line(c, [(tx - 17 * (1 - k), ty + 2 - 64 * k), (tx + 17 * (1 - k), ty + 2 - 64 * k)],
             mix(STEEL, NEAR, 0.20), width=2)
    line(c, [(tx - 13, ty - 54), (tx + 13, ty - 54)], mix(STEEL, PAPER, 0.35), width=3)

# stubs tying each settlement down to the terrestrial route
for (hx, hy) in HUBS:
    line(c, [(hx, hy + 6), (hx + 4, (hy + sy(hx)) / 2), (hx, sy(hx) - 3)],
         mix(STEEL, NEAR, 0.42), width=2)

# ---------------------------------------------------------------- 5. settlements
for i, (hx, hy) in enumerate(HUBS):
    glow(c, hx, hy - 4, 40, GLOW, alpha=56)
    glow(c, hx, hy - 4, 16, ACCENT, alpha=70)
    n = 6 + (i % 3)
    for k in range(n):
        wx = hx + rng.uniform(-26, 26)
        wy = hy - rng.uniform(1, 13)
        w = rng.uniform(2.6, 5.4)
        h = rng.uniform(2.2, 4.4)
        col = ACCENT if k % 3 else mix(ACCENT, GLOW, 0.45)
        poly(c, [(wx, wy), (wx + w, wy), (wx + w, wy + h), (wx, wy + h)], fill=col)
    # a couple of dark roof forms so it reads as a place, not just lights
    for k in range(2):
        rx = hx + rng.uniform(-22, 22)
        poly(c, [(rx - 9, hy + 5), (rx - 6, hy - 5), (rx + 6, hy - 5), (rx + 9, hy + 5)],
             fill=mix(NEAR, FAR, 0.4))

# ---------------------------------------------------------------- 6. thread fan
for i, (hx, hy) in enumerate(HUBS):
    steps = 22
    pts = []
    for s in range(steps + 1):
        t = s / steps
        # slight bow so the lines feel taut but hand-held, each bowing differently
        bow = (14.0 if i % 2 == 0 else -11.0) * math.sin(math.pi * t)
        px = hx + (NODE[0] - hx) * t + bow
        py = (hy - 10) + (NODE[1] - (hy - 10)) * t
        pts.append((px, py))
    col = mix(EMBER, GLOW, 0.25 + 0.12 * i)
    hand_line(c, pts, col, width=2, amp=1.1, seed=SEED + 20 + i)
    # brighter last leg into the node
    hand_line(c, pts[-6:], mix(GLOW, ACCENT, 0.45), width=2, amp=0.7, seed=SEED + 40 + i)

# ---------------------------------------------------------------- 7. satellite node
nx, ny = NODE
# wings first (behind body)
for d in (-1, 1):
    x0 = nx + d * 27
    x1 = nx + d * 75
    poly(c, [(x0, ny - 7), (x1, ny - 13), (x1, ny + 13), (x0, ny + 7)],
         fill=mix(ACCENT, EMBER, 0.42), outline=NEAR, width=2)
    for k in range(1, 4):
        t = k / 4.0
        xa = x0 + (x1 - x0) * t
        line(c, [(xa, ny - 7 - 6 * t), (xa, ny + 7 + 6 * t)], mix(EMBER, NEAR, 0.35), width=2)
# body
poly(c, [(nx - 25, ny - 15), (nx + 25, ny - 15), (nx + 25, ny + 15), (nx - 25, ny + 15)],
     fill=ACCENT, outline=NEAR, width=2)
poly(c, [(nx - 25, ny + 6), (nx + 25, ny + 6), (nx + 25, ny + 15), (nx - 25, ny + 15)],
     fill=mix(ACCENT, EMBER, 0.30))
# downlink horn, points back at the ground
poly(c, [(nx - 9, ny + 15), (nx + 9, ny + 15), (nx + 15, ny + 30), (nx - 15, ny + 30)],
     fill=mix(ACCENT, EMBER, 0.5), outline=NEAR, width=2)
circle(c, nx, ny - 15, 4, fill=NEAR)

# ---------------------------------------------------------------- 8. type
L1, L2 = "GCI Buys Orbit,", "Not Iron"
sz = min(fit_size(c, L1, 560, weight=900, opsz=144),
         fit_size(c, L2, 560, weight=900, opsz=144))
fh = fraunces(c, sz, weight=900, opsz=144)
text(c, (96, 112), L1, fh, PAPER)
text(c, (96, 112 + sz * 1.06), L2, fh, GLOW)

sub = "Wailand’s build-or-buy call"
fs = fraunces(c, 30, weight=500, opsz=72, italic=True)
text(c, (99, 112 + sz * 1.06 + sz * 1.14), sub, fs, mix(PAPER, GLOW, 0.42))

fk = mono(c, 17)
text(c, (96, 112 + sz * 1.06 + sz * 1.14 + 52), "ANCHORAGE DESK · OPERATOR · 31 JUL 2026",
     fk, mix(PAPER, EMBER, 0.36), tracking=0.20)

# wordmark + colophon
fw = fraunces(c, 31, weight=900, opsz=144)
chip(c, (96, 966), "ALASKA.AI", fw, PAPER, mix(NEAR, EMBER, 0.16),
     pad=13, tracking=0.06, radius=7)
polaris(c, 1002, 78, r=11, color="#ffc72c", core="#fff0c8")

# ---------------------------------------------------------------- 9. finish
mottle(c, strength=0.05, scale=3.0, seed=SEED + 7)
grain(c, amount=6.0, seed=SEED + 8)
vignette(c, strength=0.10, spread=1.45)

c.finish("out/post_image.png", {
    "date": "31 JUL 2026",
    "column": "Anchorage Desk",
    "kicker": "ANCHORAGE DESK",
    "middle_slot": "OPERATOR",
    "byline": "",
    "headline": "GCI Buys Orbit, Not Iron / Wailand's build-or-buy call",
    "style_family": "wpa_layered_minimal_line",
    "palette": [PAPER, GLOW, EMBER, FAR, NEAR, ACCENT, SKYTOP],
    "hue_family": "orange",
    "composition": "horizon_band",
    "motifs": ["four lit hub settlements", "single satellite node",
               "four-thread fan to one point", "broken terrestrial stitch",
               "relay towers"],
    "technique_stack": ["gradient_v", "field", "stipple", "ridge_fill", "hatch",
                        "chips", "hand_line", "glow", "mottle", "grain", "vignette"],
    "volume": "OPERATOR",
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 7.26, "weakest": "craft",
         "note": "full-width cloud strata read as posterized banding; starfield too dense and close to the legacy template; broken ground line invisible; lower third dead acreage"},
        {"iter": 2, "weighted": 7.18, "weakest": "composition",
         "note": "sky fixed, but foreground became a near-black slab with visible diagonal hatch stripes"},
        {"iter": 3, "weighted": 7.9, "weakest": "craft",
         "note": "found two real bugs: .point() on an RGBA layer scaled RGB as well as alpha (darkening toward black), and Canvas.composite(layer, mask) ignores layer alpha so transparent pixels pasted as solid black. Foreground rebuilt as a dusk-lit snow plain"},
        {"iter": 4, "weighted": 8.65, "weakest": "craft",
         "note": "ruled drift stripes replaced with scattered sastrugi; route trench softened from a black snake to a graded shadow; wordmark knocked out of a chip for legibility on the lit plain"}
    ],
    "eval_final": {"weighted": 8.65, "scores": {
        "concept": 9, "focal": 9, "composition": 8, "color": 9, "detail": 8,
        "craft": 8, "typography": 9, "originality": 9, "fidelity": 9}},
})
print("rendered out/post_image.png")
