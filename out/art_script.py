"""Alaska.Ai — The Stack — 11 SEP 2026 — "The Fabric"

The FCC's own statutory artifact is the Broadband Serviceable Location
Fabric. So the cover is literally cloth. Every thread crossing is a
serviceable location. Across the lower third the weave stops: the weft
runs out and the warp hangs loose over a dark void. One brass shuttle
rests on the line where weaving halted, loaded and motionless.

A loom advances one pick at a time and only if the shuttle is thrown.
That is the mechanism: 47 U.S.C. 1702, one officer, approve or don't.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy.ndimage import zoom

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
from art_kit import (  # noqa: E402
    Canvas, chips, circle, field, fit_size, fraunces, glow, hatch,
    hex_to_rgb,
    line, measure, mix, mono, mottle, noise1d, poly, polaris, ramp,
    wobble_pts,
    soft_panel, stipple, text, vignette, warp,
)

SEED = 911

# ---------------------------------------------------------------- palette
PAPER     = "#efe4cc"   # warm bone linen ground
CLOTH_LIT = "#d9a441"   # low-angle September gold, the woven acreage
CLOTH_SHA = "#8a5f28"   # weave seam / shadow
UMBER     = "#3a2614"   # type, selvedge, outlines
VOID      = "#14180f"   # spruce-black, the unwoven absence
BRASS     = "#ffcf5c"   # focal accent, shuttle only
PALETTE = [PAPER, CLOTH_LIT, CLOTH_SHA, UMBER, VOID, BRASS]

HEADLINE = ["OVER 5,000 LOCATIONS.", "ONE SIGNATURE."]
KICKER = "THE STACK  ·  VEHICLES  ·  11 SEP 2026"
LABEL = "47 U.S.C. 1702"

D = 1080
rng = np.random.default_rng(SEED)
c = Canvas(bg=PAPER, ss=2)

# ------------------------------------------------- cloth undulation field
# Built at 360 and zoomed 3x: this field is a large-scale soft gradient, so
# native 1080 buys nothing visible and costs ~110s (field 45s + warp 67s),
# which would eat the whole eval-iteration budget.
_LR = 360
und = warp(field(scale=3.2, octaves=4, seed=SEED, w=_LR, h=_LR),
           strength=48.0 * _LR / D, scale=2.6, seed=SEED + 1)
und = zoom(und, D / _LR, order=3)[:D, :D]
und = (und - und.min()) / (np.ptp(und) + 1e-9)
GOLD = ramp([CLOTH_SHA, CLOTH_LIT, "#f0c877"], 96)


def shade(x, y, lo=0, hi=95):
    """Sample the undulation field at a design-space point -> gold hex."""
    xi = int(min(D - 1, max(0, x)))
    yi = int(min(D - 1, max(0, y)))
    return GOLD[int(lo + und[yi, xi] * (hi - lo))]


# ----------------------------------------------------- the rupture line
# Ragged, non-horizontal, drifting slightly lower toward the right so the
# shuttle sits on a rise.
_n = noise1d(D + 1, scale=2.4, octaves=3, seed=SEED + 5)
RUP = np.array([690.0 + (_n[i] - 0.5) * 2 * 38.0 + (i / D) * 18.0
                for i in range(D + 1)])
# soften so the tear reads as fabric giving way, not as a mountain ridge
RUP = np.convolve(RUP, np.ones(9) / 9.0, mode="same")
RUP[:5], RUP[-5:] = RUP[5], RUP[-6]


def rup(x):
    return float(RUP[int(min(D, max(0, x)))])


# ======================================================== 1. paper + tone
mottle(c, strength=0.05, scale=3.0, seed=SEED + 2)

# ======================================================== 2. cloth ground
ys, xs = np.mgrid[0:D, 0:D]
cloth_m = (ys < RUP[None, :D]).astype(np.uint8) * 255
cloth_mask = Image.fromarray(cloth_m, "L").resize((c.W, c.W), Image.LANCZOS)
void_mask = Image.fromarray(255 - cloth_m, "L").resize((c.W, c.W),
                                                       Image.LANCZOS)

g = np.clip(und, 0, 1)
d_, l_ = np.array(hex_to_rgb(CLOTH_SHA), float), np.array(hex_to_rgb("#e9b95e"), float)
base = Image.fromarray(
    (d_[None, None] * (1 - g[..., None]) + l_[None, None] * g[..., None]
     ).astype(np.uint8), "RGB").resize((c.W, c.W), Image.LANCZOS)
c.img.paste(base, (0, 0), cloth_mask)

void_img = Image.new("RGB", (c.W, c.W), hex_to_rgb(VOID))
c.img.paste(void_img, (0, 0), void_mask)
c.draw = ImageDraw.Draw(c.img, "RGBA")

# ====================== 3. plain weave: warp floats + weft floats
# Iter 2 drew a true checkerboard, which killed the corduroy read but left
# something worse: a mechanical carbon-fibre pattern, plus a HARD-EDGED
# rectangle where the headline quiet zone stopped. Iter 3 fixes both.
#  - quiet zone is now a smooth elliptical falloff, no boundary anywhere
#  - per-thread slub tone, so each warp and weft has its own character
#  - a low-frequency twill drift breaks the relentless 1/1 parity
#  - floats nearly touch, so the base stops showing through as dot-grid
WX = []
x = 2.0
while x < D + 6:
    WX.append(x)
    x += 7.0 + rng.uniform(-1.15, 1.15)
WY = []
y = -4.0
while y < RUP.max() + 8:
    WY.append(y)
    y += 7.0 + rng.uniform(-1.15, 1.15)
NW, NH = len(WX), len(WY)

# every thread gets its own slub character, like real spun yarn
warp_tone = rng.normal(0, 5.2, NW)
weft_tone = rng.normal(0, 5.2, NH)
for _ in range(9):                      # a few pronounced slubs
    k = int(rng.integers(0, NW)); warp_tone[k] += rng.uniform(-13, 13)
    k = int(rng.integers(0, NH)); weft_tone[k] += rng.uniform(-13, 13)

# low-frequency drift that locally flips the weave off strict 1/1
_tw = zoom(field(scale=2.2, octaves=2, seed=SEED + 21, w=90, h=90),
           D / 90.0, order=3)[:D, :D]


def calm(xm, ym):
    """Smooth elliptical quiet zone under the headline. No hard edge."""
    e = ((xm - 430.0) / 600.0) ** 2 + ((ym - 176.0) / 300.0) ** 2
    return math.exp(-e * 1.35)


base_mid = GOLD[58]
for j in range(NH - 1):
    y0, y1 = WY[j], WY[j + 1]
    ym = (y0 + y1) * 0.5
    if ym < -2:
        continue
    yi = int(min(D - 1, max(0, ym)))
    for i in range(NW - 1):
        x0, x1 = WX[i], WX[i + 1]
        xm = (x0 + x1) * 0.5
        if ym > rup(xm) - 1.5:
            continue
        xi = int(min(D - 1, max(0, xm)))
        weft = (i + j + int(_tw[yi, xi] * 3.4)) % 2 == 0
        t = weft_tone[j] if weft else warp_tone[i]
        lo, hi = (34, 95) if weft else (1, 50)
        idx = int(lo + und[yi, xi] * (hi - lo) + t)
        col = GOLD[max(0, min(95, idx))]
        w_calm = calm(xm, ym)
        if w_calm > 0.004:
            col = mix(col, base_mid, 0.62 * w_calm)
        rgb = (*hex_to_rgb(col), 255)
        if weft:
            h = (y1 - y0) * 0.49
            c.draw.rectangle([c.s(x0 - 0.5), c.s(ym - h),
                              c.s(x1 + 0.5), c.s(ym + h)], fill=rgb)
        else:
            w = (x1 - x0) * 0.49
            c.draw.rectangle([c.s(xm - w), c.s(y0 - 0.5),
                              c.s(xm + w), c.s(y1 + 0.5)], fill=rgb)

# faint continuous warp grain over the whole bolt: cloth hangs vertically,
# and the eye wants that directional memory under the interlace.
grain_lay, gl = c.layer()
for i in range(0, NW - 1, 2):
    wx = WX[i] + rng.uniform(-0.6, 0.6)
    yb = rup(wx)
    gl.line([(c.s(wx), c.s(0)), (c.s(wx), c.s(yb))],
            fill=(*hex_to_rgb(CLOTH_SHA), 26),
            width=max(1, int(c.s(1.5))))
c.composite(grain_lay)

# ---- drape folds -------------------------------------------------------
# Iter 6: the upper bolt was ~45% of the canvas carrying only weave texture.
# Real hanging cloth falls in folds, so it now does. Soft multiply bands
# plus sheen between them: adds meso structure to the largest shape, breaks
# the monochrome, and reinforces that this is a bolt hanging, not wallpaper.
fold = Image.new("RGBA", (c.W, c.W), (0, 0, 0, 0))
fd = ImageDraw.Draw(fold, "RGBA")
for fx, fw, fa in ((196, 34, 74), (392, 26, 52), (588, 40, 80),
                   (846, 30, 60), (1010, 26, 44)):
    fd.rectangle([c.s(fx - fw / 2), 0, c.s(fx + fw / 2), c.s(D)],
                 fill=(*hex_to_rgb(mix(CLOTH_SHA, UMBER, 0.38)), fa))
for hx, hw, ha in ((292, 60, 46), (492, 52, 38), (720, 70, 52), (936, 44, 34)):
    fd.rectangle([c.s(hx - hw / 2), 0, c.s(hx + hw / 2), c.s(D)],
                 fill=(*hex_to_rgb("#f7dba4"), ha))
fold = fold.filter(ImageFilter.GaussianBlur(c.s(26)))
fold.putalpha(ImageChops.multiply(fold.getchannel("A"), cloth_mask))
c.composite(fold)

# ===================================================== 5. selvedge (left)
# The finished edge. Proves the cloth was made, not generated.
for k in range(7):
    sx = 44 + k * 3.0
    pts = [(sx + math.sin(y / 90.0) * 1.4, y) for y in np.arange(0, rup(sx), 12)]
    line(c, pts, mix(CLOTH_SHA, UMBER, 0.45 + k * 0.05), width=2.4)
for y in np.arange(10, rup(56) - 8, 9.2):
    c.draw.arc([c.s(46), c.s(y), c.s(60), c.s(y + 7.4)], 92, 268,
               fill=(*hex_to_rgb(mix(CLOTH_SHA, UMBER, 0.5)), 235),
               width=max(1, int(c.s(1.5))))

# ============================================ 6. fraying at the tear edge
for i, wx in enumerate(WX):
    yb = rup(wx)
    for k in range(rng.integers(2, 5)):
        sy = yb - rng.uniform(3, 26)
        w = rng.uniform(3, 11)
        c.draw.line([(c.s(wx - w), c.s(sy)), (c.s(wx + w), c.s(sy))],
                    fill=(*hex_to_rgb(shade(wx, sy, 30, 92)), 210),
                    width=max(1, int(c.s(rng.uniform(1.4, 2.4)))))

# torn edge: a drawn line, so the cloth ends decisively
edge = [(x, rup(x) - 1.0) for x in range(0, D + 1, 4)]
line(c, wobble_pts(edge, amp=1.3, scale=14.0, seed=SEED + 31),
     mix(UMBER, VOID, 0.42), width=2.6)

# ================================== 7. hanging warp threads into the void
# The unserved locations: everything the cloth would have reached.
hang_idx = sorted(rng.choice(NW, size=min(268, NW), replace=False))
for i in hang_idx:
    wx = WX[i]
    yb = rup(wx)
    bias = 0.60 + 0.40 * math.exp(-((wx - 560) / 520.0) ** 2)
    L = rng.uniform(70, 430) * bias
    if rng.random() < 0.14:
        L = rng.uniform(380, 560)
    n = max(3, int(L / 16))
    sway = rng.uniform(-16, 16)
    pts = []
    for t in range(n + 1):
        f = t / n
        pts.append((wx + sway * (f ** 1.9) + math.sin(f * 5 + i) * 2.2,
                    yb + L * f))
    col = mix(shade(wx, yb, 10, 70), VOID, 0.30)
    for t in range(len(pts) - 1):
        f = t / max(1, len(pts) - 1)
        c.draw.line([(c.s(pts[t][0]), c.s(pts[t][1])),
                     (c.s(pts[t + 1][0]), c.s(pts[t + 1][1]))],
                    fill=(*hex_to_rgb(mix(col, VOID, 0.55 * f)), 255),
                    width=max(1, int(c.s(rng.uniform(1.3, 2.2) * (1 - 0.3 * f)))))

# lint and broken fibre at the tear
chips(c, 230, (0, 640, D, 800), size=(1.4, 4.2),
      colors=(CLOTH_LIT, CLOTH_SHA, "#f0c877"), seed=SEED + 7)

# void tooth so the darkness is never a flat fill
stipple(c, void_mask, density=0.055, r=(0.6, 1.6),
        color=mix(VOID, CLOTH_SHA, 0.30), seed=SEED + 8)

# ================================================ 8. the shuttle (FOCAL)
# Iter 4. Iters 1-3 kept reading as an EYE (or a fish) because an oval
# cavity centred in a lens is exactly an iris in a sclera. Fixed by
# building the actual object: flat-bottomed wooden boat, long RECTANGULAR
# pirn well, a visible tapered pirn on its spindle, metal tips. Body
# darkened to bronze so the cream highlight reads as specular rather than
# the whole tool being pale-on-pale against the cloth.
SX, SY, TILT = 648.0, 731.0, -7.0
ca, sa = math.cos(math.radians(TILT)), math.sin(math.radians(TILT))

BRONZE = mix(BRASS, UMBER, 0.54)
WOODLIT = mix(BRASS, "#ffffff", 0.24)
CAV = mix(UMBER, VOID, 0.55)


def R(px, py):
    return (SX + px * ca - py * sa, SY + px * sa + py * ca)


glow(c, SX - 8, SY + 32, 146, "#241708", alpha=112)   # cast shadow
glow(c, SX, SY, 190, BRASS, alpha=44)                 # restrained halo

half, hh = 154.0, 31.0

for sgn in (-1, 1):                                   # steel points
    tip = [R(sgn * (half + 40), -1), R(sgn * half, -10.5), R(sgn * half, 10.0)]
    poly(c, tip, fill=mix(UMBER, "#cfd3cd", 0.60))
    poly(c, tip, outline=mix(UMBER, VOID, 0.35), width=1.6)

# flat-bottomed boat: the underside is a near-straight line, which is what
# separates a shuttle silhouette from a lens or a fish
top_e, bot_e = [], []
for t in np.linspace(-1, 1, 80):
    tp = (1 - abs(t) ** 3.4) ** 0.5
    top_e.append(R(t * half, -hh * tp))
    bot_e.append(R(t * half, 16.0 * (1 - abs(t) ** 7.0) ** 0.30))
body = top_e + bot_e[::-1]
poly(c, body, fill=BRONZE)

bm, bmd = c.mask()
bmd.polygon(c.pts(body), fill=255)
hatch(c, bm, spacing=5.6, angle=-15.0, color=mix(BRONZE, UMBER, 0.45), width=1.0)

face = top_e + [R(half * 0.99, -3.0), R(-half * 0.99, -3.0)][::-1]
poly(c, face, fill=WOODLIT)
poly(c, body, outline=mix(UMBER, VOID, 0.30), width=2.6)

# long rectangular pirn well
wl, wr, wt, wb = -96.0, 96.0, -17.0, 12.0
well = [R(wl, wt), R(wr, wt), R(wr, wb), R(wl, wb)]
poly(c, well, fill=CAV)
poly(c, well, outline=mix(UMBER, VOID, 0.5), width=1.8)

# the pirn: a tapered cop of weft on its spindle, thick end at the left
for k in range(46):
    f = k / 45.0
    px = wl + 8 + f * 174
    hgt = 12.6 * (1.0 - 0.62 * f)
    line(c, [R(px, -hgt), R(px, hgt * 0.86)],
         mix(CLOTH_LIT, "#f8e3ae", ((k % 5) / 5.0) * 0.9), width=1.9)
line(c, [R(wl + 4, -3), R(wr - 4, -3)], mix("#f8e3ae", CLOTH_LIT, 0.35),
     width=1.4)
circle(c, *R(wl + 4, -2), 5.2, fill=mix(UMBER, "#cfd3cd", 0.55))  # spindle

# thread eye in the side wall, and the live thread back to the last pick
eye_c = R(-half * 0.74, 2)
eye = [R(-half * 0.74 - 9, -4), R(-half * 0.74 + 9, -4),
       R(-half * 0.74 + 9, 7), R(-half * 0.74 - 9, 7)]
poly(c, eye, fill=CAV)
poly(c, eye, outline=mix(BRASS, "#ffffff", 0.3), width=1.4)

live = [eye_c, (eye_c[0] - 64, eye_c[1] - 6), (430, rup(430) - 13),
        (356, rup(356) - 8), (292, rup(292) - 15)]
line(c, live, "#f8e3ae", width=3.0)
line(c, [(292, rup(292) - 15), (232, rup(232) - 9)],
     mix("#f8e3ae", CLOTH_LIT, 0.55), width=2.4)

for gx, gy, gr in ((-118, -14, 3.8), (-52, -24, 5.6), (56, -22, 4.6),
                   (128, -12, 3.4)):
    px, py = R(gx, gy)
    c.draw.ellipse([c.s(px - gr), c.s(py - gr), c.s(px + gr), c.s(py + gr)],
                   fill=(255, 253, 240, 238))

# ======================================================== 9. finishing
grain_amt = 6.0
from art_kit import grain  # noqa: E402
grain(c, amount=grain_amt, seed=SEED + 11)
vignette(c, strength=0.14, spread=1.35)

# ============================================================ 10. type
hsize = min(fit_size(c, HEADLINE[0], 754, lo=40, hi=104, tracking=-0.012,
                     weight=900, opsz=144), 92)
hf = fraunces(c, hsize, weight=900, opsz=144)
lh = hsize * 1.06
y0 = 132

# No soft_panel: iter 1's blurred panel read as a smudge. Umber #3a2614 on
# the gold cloth measures ~6:1 contrast unaided, and the weave is already
# calmed toward mid-tone inside the headline zone.
for i, ln in enumerate(HEADLINE):
    text(c, (86, y0 + i * lh), ln, hf, UMBER, anchor="la", tracking=-0.012)

kf = mono(c, 15)
text(c, (88, y0 + lh * 2 + 16), KICKER, kf, mix(UMBER, CLOTH_SHA, 0.42),
     anchor="la", tracking=0.26)

# one small supporting line: the chokepoint statute, straight from the dossier
lf = mono(c, 13, medium=True)
text(c, (SX, 828), LABEL, lf, mix(CLOTH_LIT, PAPER, 0.35), anchor="ma",
     tracking=0.18)

wf = fraunces(c, 30, weight=900, opsz=144)
text(c, (86, 1014), "ALASKA.AI", wf, mix(PAPER, CLOTH_LIT, 0.22),
     anchor="ls", tracking=0.03)

polaris(c, 986, 96, r=13, color=BRASS, core="#fff0c8")

# ============================================================= 11. ship
meta = {
    "date": "11 SEP 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "VEHICLES",
    "byline": "",
    "headline": "Over 5,000 locations. One signature.",
    "style_family": "woven_fabric",
    "palette": PALETTE,
    "hue_family": "gold",
    "composition": "weave_rupture",
    "motifs": ["woven cloth", "unwoven rupture", "hanging warp threads",
               "loom shuttle at rest", "selvedge", "live thread",
               "drape folds"],
    "technique_stack": ["field", "warp", "ramp", "interlaced weft/warp",
                        "slub tone", "twill drift", "drape folds",
                        "selvedge arcs", "hatch", "stipple", "chips",
                        "glow", "mottle", "grain", "vignette", "polaris"],
    "seed": SEED,
    "concept": ("The FCC's Broadband Serviceable Location Fabric rendered "
                "literally as cloth. The weave stops mid-bolt, warp hanging "
                "into the dark. One shuttle rests on the tear line, loaded "
                "and motionless, because a loom advances only when it is "
                "thrown. That is 47 U.S.C. 1702."),
    "eval_history": [
        {"iter": 1, "weighted": 6.73, "weakest": "craft",
         "fix": "soft_panel left a visible smudge halo; weave read as "
                "corduroy stripes; 196px shuttle read as a FISH"},
        {"iter": 2, "weighted": 7.36, "weakest": "craft",
         "fix": "true plain-weave checkerboard killed the stripes but went "
                "mechanical, and the headline quiet zone left a HARD-EDGED "
                "rectangle"},
        {"iter": 3, "weighted": 7.95, "weakest": "focal",
         "fix": "smooth elliptical calm + per-thread slub + twill drift "
                "fixed the cloth; shuttle's oval cavity still read as an eye"},
        {"iter": 4, "weighted": 8.24, "weakest": "focal",
         "fix": "rebuilt as a real loom shuttle (flat bottom, rectangular "
                "pirn well, steel tips); still gold-on-gold, no value gap"},
        {"iter": 5, "weighted": 8.70, "weakest": "craft",
         "fix": "seated the shuttle over the void and darkened body to "
                "bronze; added a drawn torn edge. Cleared the 8.5 floor"},
        {"iter": 6, "weighted": 8.76, "weakest": "craft",
         "fix": "8.5 is the floor not the target: drape folds added meso "
                "structure to the upper ~45% of flat cloth acreage"}
    ],
    "eval_final": {
        "weighted": 8.76,
        "scores": {"concept": 9, "focal": 8.5, "composition": 8.5,
                   "color": 8.5, "detail": 9, "craft": 8.5,
                   "typography": 9, "originality": 9, "fidelity": 9},
        "iterations_used": 6,
        "script_crashes_fixed": 2,
        "note": "Crashes (numpy 2.x ndarray.ptp removal; missing circle "
                "import) were fixed and re-run and do not count as eval "
                "iterations, per the skill."
    },
}
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
