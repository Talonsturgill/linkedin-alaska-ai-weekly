"""Anchorage Desk — 24 JUL 2026 — "the red pen through the drift".

A vast drift of torn public-comment paper sweeps across the frame. A single
vermilion pen stroke cuts through it. On the far side, three scraps sit
alone, marked and kept. Everything else is set aside.

style_family: paper_collage | hue_family: neutral-warm | composition: scatter_field
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as K  # noqa: E402

SEED = 724

# ---------------------------------------------------------------- palette
PAPER = "#ece3d1"   # warm bone ground
SCRAP_L = "#dbd0b8"  # scrap light
SCRAP_M = "#c3b394"  # scrap mid
SCRAP_D = "#9d8b6c"  # scrap dark / shadow side
HORIZON = "#6b5c46"  # far ridge, atmospheric
INK = "#332b21"     # type, seams, deep shadow
VERM = "#cf4520"    # the pen. only high-chroma ink in the piece

KICKER = "ANCHORAGE DESK"
MIDDLE = "OPERATOR"
DATE = "24 JUL 2026"
HEADLINE = ["Ex-Commissioner Grades", "His Own Lease Opposition"]

rng = np.random.default_rng(SEED)
c = K.Canvas(bg=PAPER, ss=2)


# ------------------------------------------------------------ torn scraps
def torn_quad(cx, cy, w, h, ang, seed, tear=1.0):
    """A document-shaped scrap with torn edges. Rectilinear on purpose so
    it reads as paper, never as confetti."""
    base = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    # densify each side so wobble_pts has something to chew on
    dense = []
    for i in range(4):
        x0, y0 = base[i]
        x1, y1 = base[(i + 1) % 4]
        for t in np.linspace(0, 1, 7, endpoint=False):
            dense.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    dense = K.wobble_pts(dense, amp=max(0.9, w * 0.055) * tear,
                         scale=9.0, seed=seed)
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in dense]


# -------------------------------------------------------- 1. paper ground
K.mottle(c, strength=0.05, scale=3.4, seed=SEED)

# ------------------------------------------- 2. far ground (atmospheric)
# No hard horizon band. Iteration 2 read as a scan line. The drift crest
# does the horizon work; this is only a faint warm wash so the upper paper
# doesn't sit dead flat against it.
wash, wd = c.layer()
wd.rectangle([0, c.s(500), c.W, c.s(700)],
             fill=(*K.hex_to_rgb(HORIZON), 16))
from PIL import ImageFilter  # noqa: E402
wash = wash.filter(ImageFilter.GaussianBlur(c.s(70)))
c.composite(wash)

# ------------------------------------------------------ 3. the drift mass
# A real drift, not a scatter. A filled dune whose crest silhouette rises
# from the left edge to a peak under the pen stroke and falls away right.
# Scraps ride ON the mass, so it groups as ONE shape at thumbnail (risk #1)
# and never reads as confetti (risk #4).

DRIFT_TOP = 470
STROKE_A = (248.0, 946.0)
STROKE_B = (872.0, 566.0)

crest = K.ridge_pts(y_base=742, amp=118, scale=2.4, octaves=4,
                    seed=SEED + 11, x0=-40, x1=1120, step=6)
# tilt the whole crest so it sweeps down to the right like a wind drift
crest = [(x, y + (x / 1080.0) * 168 - 34) for x, y in crest]
crest = K.wobble_pts(crest, amp=3.0, scale=14.0, seed=SEED + 12)


def crest_y(x):
    i = min(len(crest) - 1, max(0, int((x + 40) / 6)))
    return crest[i][1]


# the mass itself, in two value bands for depth
body = [(-40, 1120)] + crest + [(1120, 1120)]
K.poly(c, body, fill=K.mix(SCRAP_M, SCRAP_L, 0.45))
lower = [(-40, 1120)] + [(x, y + 96 + (x / 1080.0) * 40) for x, y in crest] \
    + [(1120, 1120)]
K.poly(c, lower, fill=SCRAP_M)
deep = [(-40, 1120)] + [(x, y + 214 + (x / 1080.0) * 30) for x, y in crest] \
    + [(1120, 1120)]
K.poly(c, deep, fill=K.mix(SCRAP_M, SCRAP_D, 0.55))

# soft shadow where the mass meets the paper, so it sits rather than floats
sh, shd = c.layer()
shd.polygon(c.pts([(-40, 1120)] + [(x, y + 6) for x, y in crest]
                  + [(1120, 1120)]),
            fill=(*K.hex_to_rgb(INK), 40))
from PIL import ImageFilter  # noqa: E402
sh = sh.filter(ImageFilter.GaussianBlur(c.s(16)))
c.composite(sh)


def stroke_side(x, y):
    ax, ay = STROKE_A
    bx, by = STROKE_B
    return (bx - ax) * (y - ay) - (by - ay) * (x - ax)


# --- scraps riding on the drift -------------------------------------
scraps = []
for i in range(720):
    x = rng.uniform(-40, 1120)
    cy = crest_y(x)
    y = rng.uniform(cy - 34, 1110)
    if y < DRIFT_TOP:
        continue
    depth = float(np.clip((y - cy) / (1110 - cy + 1e-6), 0.0, 1.0))
    if stroke_side(x, y) < 0 and rng.random() < 0.90:
        continue
    scraps.append((x, y, depth, i))

# a few loose sheets tumbling above the crest, so the mass has air
for i in range(26):
    x = rng.uniform(20, 1060)
    cy = crest_y(x)
    y = rng.uniform(max(DRIFT_TOP, cy - 150), cy - 18)
    if stroke_side(x, y) < 0 and rng.random() < 0.86:
        continue
    scraps.append((x, y, rng.uniform(0.16, 0.42), 3000 + i))

scraps.sort(key=lambda s: s[1])

for x, y, depth, i in scraps:
    # aggressive scale ramp: real documents in the foreground
    w = 11 + depth * depth * 74 + depth * 20
    h = w * rng.uniform(0.66, 0.94)
    ang = rng.uniform(-0.55, 0.55)
    if depth < 0.30:
        base = K.mix(SCRAP_L, PAPER, 0.34)
    elif depth < 0.62:
        base = K.mix(SCRAP_L, SCRAP_M, rng.uniform(0.15, 0.75))
    else:
        base = K.mix(SCRAP_M, SCRAP_D, rng.uniform(0.05, 0.70))
    pts = torn_quad(x, y, w, h, ang, i)
    # cast shadow per scrap, tight and directional
    if w > 15:
        K.poly(c, torn_quad(x + w * 0.055, y + h * 0.085, w, h, ang, i),
               fill=K.darken(base, 0.30))
    K.poly(c, pts, fill=base)
    ca, sa = math.cos(ang), math.sin(ang)
    # meso: a folded/shaded corner so each sheet has form
    if w > 20:
        K.poly(c, torn_quad(x + w * 0.30, y + h * 0.27, w * 0.46, h * 0.40,
                            ang, i + 9000), fill=K.darken(base, 0.13))
    # micro: ruled lines, so these are documents and not gravel
    if w > 22:
        ru = K.mix(base, INK, 0.34)
        nlines = 3 if w < 40 else 4
        for k in np.linspace(-0.26, 0.24, nlines):
            seg = [(x + px * ca - (h * k) * sa, y + px * sa + (h * k) * ca)
                   for px in (-w * 0.29, w * 0.25)]
            K.line(c, seg, ru, width=max(1.0, w * 0.030))


# a squall of sheets lifting off the crest on the left, low contrast, to
# bridge the quiet middle band without competing with the headline
squall = []
for i in range(40):
    x = rng.uniform(40, 640)
    y = rng.uniform(392, 672)
    if y > crest_y(x) - 14:
        continue
    # strong size variance: a few near sheets carry scale, the rest recede
    roll = rng.random()
    if roll < 0.18:
        w = rng.uniform(40, 62)          # near, reads as a document
    elif roll < 0.52:
        w = rng.uniform(22, 36)
    else:
        w = rng.uniform(10, 19)          # far, just tumbling grit
    squall.append((x, y, w, i))
squall.sort(key=lambda s: s[2])          # small (far) first, big (near) last

for x, y, w, i in squall:
    h = w * rng.uniform(0.66, 0.92)
    ang = rng.uniform(-0.9, 0.9)
    fade = float(np.clip((y - 380) / 300.0, 0.0, 1.0))
    near = float(np.clip((w - 10) / 52.0, 0.0, 1.0))
    base = K.mix(PAPER, SCRAP_M, 0.16 + fade * 0.42 + near * 0.26)
    K.poly(c, torn_quad(x + 2 + near * 3, y + 3 + near * 4, w, h, ang,
                        7000 + i), fill=K.darken(base, 0.12))
    K.poly(c, torn_quad(x, y, w, h, ang, 7000 + i), fill=base)
    # the near sheets get ruled lines too, so scale reads as distance
    if w > 34:
        ca, sa = math.cos(ang), math.sin(ang)
        ru = K.mix(base, INK, 0.26)
        for k in (-0.22, -0.02, 0.18):
            seg = [(x + px * ca - (h * k) * sa, y + px * sa + (h * k) * ca)
                   for px in (-w * 0.28, w * 0.22)]
            K.line(c, seg, ru, width=1.3)

# micro: paper dust in the drift hollows
K.chips(c, 240, region=(0, 620, 1080, 1080), size=(1.5, 4.6),
        colors=(K.mix(SCRAP_L, PAPER, 0.25), SCRAP_M, K.lighten(SCRAP_D, 0.12)),
        seed=SEED + 5)

# ---------------------------------------------------- 4. the red pen mark
# A filled stroke with a real width profile, thin at the touch-down, swelling
# through the middle, lifting off thin at the end. Iterations 1 and 2 stacked
# uniform-width lines and read as a rod lying on the pile.
def stroke_poly(maxw, bow, t0=0.0, t1=1.0, jitter=0.0, seed=0):
    r = np.random.default_rng(seed)
    left, right = [], []
    n = 130
    for k in range(n):
        u = k / (n - 1)
        tt = t0 + (t1 - t0) * u
        x = STROKE_A[0] + (STROKE_B[0] - STROKE_A[0]) * tt
        y = STROKE_A[1] + (STROKE_B[1] - STROKE_A[1]) * tt
        x += math.sin(tt * math.pi) * bow
        y += math.sin(tt * math.pi) * bow * 0.42
        # width profile: swell in the middle, taper hard at both ends,
        # with the lift-off end thinner than the touch-down end
        prof = math.sin(math.pi * u) ** 0.42
        prof *= 1.0 - 0.30 * u
        w = maxw * prof + r.uniform(-jitter, jitter)
        dx = (STROKE_B[0] - STROKE_A[0])
        dy = (STROKE_B[1] - STROKE_A[1])
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        left.append((x + nx * w / 2, y + ny * w / 2))
        right.append((x - nx * w / 2, y - ny * w / 2))
    return left + right[::-1]


# soft cast shadow (blurred, not an offset outline -- iteration 3 read as a
# hard black rim along the lower flank)
pshadow, psd = c.layer()
psd.polygon(c.pts([(x + 5, y + 7) for x, y in
                   stroke_poly(19, 22, jitter=0.4, seed=SEED + 6)]),
            fill=(*K.hex_to_rgb(INK), 70))
pshadow = pshadow.filter(ImageFilter.GaussianBlur(c.s(9)))
c.composite(pshadow)

# the stroke: a deep warm red underlay, then the vermilion body just inside
# it, so the edge darkens like real ink pooling rather than outlining
K.poly(c, stroke_poly(18, 22, jitter=0.5, seed=SEED + 6),
       fill="#8f2a12")
K.poly(c, [(x - 0.8, y - 1.1) for x, y in
           stroke_poly(15.5, 22, jitter=0.6, seed=SEED + 7)], fill=VERM)
# wet-edge highlight along the upper flank, where a felt tip pools less ink
K.poly(c, [(x - 5.0, y - 6.2) for x, y in
           stroke_poly(6.5, 22, t0=0.10, t1=0.86, jitter=0.5, seed=SEED + 8)],
       fill=K.lighten(VERM, 0.20))

# ------------------------------------------------- 5. the three kept scraps
# The focal. Big, isolated in clean paper past the stroke's end, each ticked.
KEPT = [(902, 604, 80, -0.13), (982, 512, 66, 0.18), (876, 486, 58, 0.04)]
kshadow, ksd = c.layer()
for j, (x, y, w, a) in enumerate(KEPT):
    ksd.polygon(c.pts(torn_quad(x + 8, y + 11, w, w * 0.76, a, 500 + j)),
                fill=(*K.hex_to_rgb(INK), 84))
kshadow = kshadow.filter(ImageFilter.GaussianBlur(c.s(8)))
c.composite(kshadow)

for j, (x, y, w, a) in enumerate(KEPT):
    h = w * 0.76
    K.poly(c, torn_quad(x, y, w, h, a, 500 + j), fill="#f8f3e7")
    ca, sa = math.cos(a), math.sin(a)
    for k in (-0.28, -0.10, 0.08, 0.26):
        seg = [(x + px * ca - (h * k) * sa, y + px * sa + (h * k) * ca)
               for px in (-w * 0.31, w * 0.20)]
        K.line(c, seg, K.mix(SCRAP_D, "#f8f3e7", 0.38), width=1.7)
    # the vermilion tick: kept
    for px, py in [(-0.20, 0.16)]:
        bx, by = x + px * w, y + py * h
        tick = [(bx - 9, by - 1), (bx - 3, by + 7), (bx + 11, by - 12)]
        tick = [(x + (tx - x) * ca - (ty - y) * sa,
                 y + (tx - x) * sa + (ty - y) * ca) for tx, ty in tick]
        K.line(c, tick, VERM, width=3.6)

# ------------------------------------------------------------ 6. finishing
K.grain(c, amount=6.0, seed=SEED, mono=True)
K.vignette(c, strength=0.13, spread=1.5)

# ------------------------------------------------------------------ 7. type
K.ensure_fonts()

# Headline: poster Fraunces, sitting in the protected quiet zone up top.
f_head = K.fraunces(c, 82, weight=900, opsz=144)
size = 82
while max(K.measure(c, ln, f_head) for ln in HEADLINE) > 858 and size > 52:
    size -= 3
    f_head = K.fraunces(c, size, weight=900, opsz=144)

y = 112
for ln in HEADLINE:
    K.text(c, (86, y), ln, f_head, INK, anchor="la")
    y += size * 1.08

# Kicker telemetry
f_mono = K.mono(c, 17, medium=True)
K.text(c, (88, 322), f"{KICKER}  ·  {MIDDLE}  ·  {DATE}", f_mono,
       K.mix(INK, PAPER, 0.28), anchor="la", tracking=0.22)
K.line(c, [(88, 352), (300, 352)], K.mix(VERM, PAPER, 0.15), width=2.5)

# Wordmark, small and integrated, bottom left on the quiet flank
f_mark = K.fraunces(c, 31, weight=900, opsz=144)
K.text(c, (86, 1030), "ALASKA.AI", f_mark, "#f4ecd9", anchor="ls", tracking=0.04)

# Polaris colophon
K.polaris(c, 998, 88, r=13, color="#d9a227", core="#f6e2ae")

# ------------------------------------------------------------------ 8. save
c.finish("out/post_image.png", {
    "date": DATE,
    "column": "Anchorage Desk",
    "kicker": KICKER,
    "middle_slot": MIDDLE,
    "byline": "",
    "headline": " ".join(HEADLINE),
    "style_family": "paper_collage",
    "palette": [PAPER, SCRAP_L, SCRAP_M, SCRAP_D, HORIZON, INK, VERM],
    "hue_family": "neutral-warm",
    "composition": "scatter_field",
    "motifs": ["torn public-comment paper drift", "red pen stroke",
               "three kept scraps", "North Slope horizon"],
    "technique_stack": ["mottle", "ridge_fill", "wobble_pts torn quads",
                        "layered poly scraps", "chips", "hand_line", "grain",
                        "vignette"],
    "seed": SEED,
    "eval_history": [],
    "eval_final": {},
})
print("rendered out/post_image.png")
