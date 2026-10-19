"""Anchorage Desk cover art, 2026-08-07.

Concept: the crowded field and the empty page. A dense scatter of
surveillance cameras fills the night, every one aimed at a single bone
ruled page that has nothing written on it. The capability is installed
and pointed; the rule that governs it is blank.

Style family: constructivist_scatter   Composition: scatter_field
Hue family: blue                       Seed: 2608
"""
import math
import sys
from PIL import Image, ImageFilter

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
import art_kit as K

SEED = 2608
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
PAPER = "#ece3d2"   # the blank ordinance page, focal
PAGE_SH = "#b9ad97"  # page rules / edge shadow
METAL = "#6f7fae"   # camera bodies
FIELD = "#1b2550"   # lower night
INK = "#0a0f28"     # upper night, silhouette darks
RED = "#d2402c"     # single record light
GOLD = "#ffc72c"    # brand marks only

HEADLINE = ["Anchorage Buys The Cameras", "Before It Writes The Rules"]
KICKER = "ANCHORAGE DESK  ·  MUNICIPAL  ·  7 AUG 2026"

PAGE_X0, PAGE_Y0, PAGE_X1, PAGE_Y1 = 118.0, 452.0, 470.0, 916.0
PAGE_CX = (PAGE_X0 + PAGE_X1) / 2.0
PAGE_CY = (PAGE_Y0 + PAGE_Y1) / 2.0
PAGE_ROT = math.radians(-2.5)

c = K.Canvas(bg=INK, ss=2)

# ------------------------------------------------------- 1. night gradient
K.gradient_v(c, (0, 0, 1080, 1080), INK, FIELD, ease=1.25)

# ------------------------------------------------- 2. street grid substrate
# Two line weights plus faint parcel infill so the night carries meso
# structure instead of flat acreage.
ang = math.radians(6.0)
ca, sa = math.cos(ang), math.sin(ang)


def grid_pt(u, v):
    """Grid-space (u along arterials, v across) to canvas."""
    return (540 + u * ca - v * sa, 540 + u * sa + v * ca)


parcel_layer, pd = c.layer()
for i in range(-26, 27):
    for j in range(-26, 27):
        if rng.random() > 0.34:
            continue
        u0, v0 = i * 44.0, j * 44.0
        quad = [grid_pt(u0 + 3, v0 + 3), grid_pt(u0 + 41, v0 + 3),
                grid_pt(u0 + 41, v0 + 41), grid_pt(u0 + 3, v0 + 41)]
        tone = K.lighten(FIELD, 0.09) if rng.random() < 0.55 else K.darken(INK, 0.12)
        pd.polygon(c.pts(quad), fill=(*K.hex_to_rgb(tone),
                                      int(rng.integers(10, 24))))
c.composite(parcel_layer)

grid_layer, gd = c.layer()
L = 1700
for i in range(-30, 40):
    off = i * 44.0
    major = (i % 4 == 0)
    col = (*K.hex_to_rgb(K.lighten(FIELD, 0.16 if major else 0.09)),
           74 if major else 40)
    wdt = max(1, int(c.s(1.9 if major else 1.0)))
    for (dx, dy) in ((ca, sa), (-sa, ca)):
        px, py = -dy * off + 540, dx * off + 540
        gd.line([(c.s(px - dx * L), c.s(py - dy * L)),
                 (c.s(px + dx * L), c.s(py + dy * L))],
                fill=col, width=wdt)
c.composite(grid_layer)

# --------------------------------------------- 3. dark scrim under type
scrim, sd = c.layer()
sd.rectangle([0, 0, c.W, c.s(360)], fill=(*K.hex_to_rgb(INK), 190))
scrim = scrim.filter(ImageFilter.GaussianBlur(c.s(46)))
c.composite(scrim)


# ------------------------------------------------------- camera glyph
def dome(cv, x, y, s, aim, body, lens, dark, glint):
    """Dome housing variant. Same read at thumbnail, different silhouette
    up close, so the crowd never looks like one stamp repeated."""
    ca_, sa_ = math.cos(aim), math.sin(aim)

    def P(px, py):
        return (x + s * (px * ca_ - py * sa_), y + s * (px * sa_ + py * ca_))

    K.poly(cv, [P(-0.60, -0.15), P(-0.50, -0.15), P(-0.50, 0.15),
                P(-0.60, 0.15)], fill=dark)
    K.poly(cv, [P(-0.54, -0.05), P(-0.24, -0.08), P(-0.24, 0.05),
                P(-0.54, 0.06)], fill=dark)
    # collar
    K.poly(cv, [P(-0.30, -0.30), P(0.04, -0.30), P(0.04, 0.30),
                P(-0.30, 0.30)], fill=K.lighten(body, 0.10))
    # dome
    dx_, dy_ = P(0.10, 0.0)
    K.circle(cv, dx_, dy_, s * 0.30, fill=body)
    K.circle(cv, dx_, dy_, s * 0.30, outline=K.darken(body, 0.34), width=max(1.0, s * 0.03))
    lx, ly = P(0.19, 0.04)
    K.circle(cv, lx, ly, s * 0.135, fill=dark)
    gx, gy = P(0.03, -0.13)
    K.circle(cv, gx, gy, max(0.9, s * 0.055), fill=glint)


def camera(cv, x, y, s, aim, body, lens, dark, glint):
    """One surveillance camera aimed along `aim` radians. Composed of
    hard primitives so the silhouette reads as a black fill."""
    ca_, sa_ = math.cos(aim), math.sin(aim)

    def P(px, py):
        return (x + s * (px * ca_ - py * sa_), y + s * (px * sa_ + py * ca_))

    # wall plate + mount arm (behind)
    K.poly(cv, [P(-0.62, -0.17), P(-0.52, -0.17), P(-0.52, 0.17),
                P(-0.62, 0.17)], fill=dark)
    K.poly(cv, [P(-0.55, -0.05), P(-0.30, -0.09), P(-0.30, 0.05),
                P(-0.55, 0.06)], fill=dark)
    # housing
    K.poly(cv, [P(-0.42, -0.26), P(0.30, -0.21), P(0.30, 0.21),
                P(-0.42, 0.27)], fill=body)
    # sun hood, one value up
    K.poly(cv, [P(-0.44, -0.30), P(0.40, -0.24), P(0.40, -0.15),
                P(-0.44, -0.20)], fill=K.lighten(body, 0.16))
    # housing seam
    K.line(cv, [P(-0.30, -0.02), P(0.26, 0.0)], K.darken(body, 0.30),
           width=max(1.0, s * 0.035))
    # lens barrel + face
    K.poly(cv, [P(0.30, -0.155), P(0.52, -0.125), P(0.52, 0.125),
                P(0.30, 0.155)], fill=K.darken(body, 0.18))
    lx, ly = P(0.545, 0.0)
    K.circle(cv, lx, ly, s * 0.145, fill=dark)
    K.circle(cv, lx, ly, s * 0.085, fill=K.darken(lens, 0.25))
    gx, gy = P(0.575, -0.05)
    K.circle(cv, gx, gy, max(0.9, s * 0.042), fill=glint)


# ------------------------------------------------ 4. camera scatter
def too_close(x, y, placed, r):
    for (px, py, pr) in placed:
        if (x - px) ** 2 + (y - py) ** 2 < (r + pr) ** 2:
            return True
    return False


NEAR_X, NEAR_Y, NEAR_S = 566.0, 742.0, 58.0

placed = [(NEAR_X, NEAR_Y, NEAR_S * 1.15)]  # reserve the hero lens
cams = []
margin = 74.0
tries = 0
while len(cams) < 116 and tries < 40000:
    tries += 1
    x = rng.uniform(46, 1034)
    y = rng.uniform(336, 1034)
    # keep the page and its breathing room clear
    if (PAGE_X0 - margin < x < PAGE_X1 + margin
            and PAGE_Y0 - margin < y < PAGE_Y1 + margin):
        continue
    # density gradient: thin out close to the page, crowd the far field
    dpage = math.hypot(x - PAGE_CX, y - PAGE_CY)
    if rng.random() > np.clip((dpage - 210.0) / 420.0, 0.14, 1.0):
        continue
    depth = np.clip((y - 336.0) / 700.0, 0.0, 1.0)
    s = float(rng.uniform(15, 24) + depth * rng.uniform(14, 34))
    s = float(np.clip(s, 15.0, 54.0))
    if too_close(x, y, placed, s * 0.92):
        continue
    placed.append((x, y, s * 0.92))
    cams.append((x, y, s))

# ---- sight lines: every lens aimed at the blank page, drawn as a faint
# ---- cone. Converging structure fills the night and makes the aim legible.
cone_layer, cd = c.layer()
for (x, y, s) in cams + [(NEAR_X, NEAR_Y, NEAR_S)]:
    aim = math.atan2(PAGE_CY - y, PAGE_CX - x)
    dist = math.hypot(PAGE_CX - x, PAGE_CY - y)
    spread = math.radians(3.4)
    tip = (x + math.cos(aim) * s * 0.55, y + math.sin(aim) * s * 0.55)
    far = dist * 0.97
    p1 = (x + math.cos(aim - spread) * far, y + math.sin(aim - spread) * far)
    p2 = (x + math.cos(aim + spread) * far, y + math.sin(aim + spread) * far)
    a = int(np.clip(15.0 * (s / 40.0), 6, 20))
    cd.polygon(c.pts([tip, p1, p2]), fill=(*K.hex_to_rgb(METAL), a))
cone_layer = cone_layer.filter(ImageFilter.GaussianBlur(c.s(1.4)))
c.composite(cone_layer)

cams.sort(key=lambda t: t[2])  # small/far first, large/near last
for idx, (x, y, s) in enumerate(cams):
    t = 1.0 - np.clip((s - 15.0) / 39.0, 0.0, 1.0)   # 1 = far
    body = K.mix(METAL, FIELD, 0.74 * t)
    dark = K.mix(K.darken(INK, 0.10), FIELD, 0.55 * t)
    lens = K.mix(METAL, FIELD, 0.5 * t)
    glint = K.mix(PAPER, FIELD, 0.62 * t)
    # a handful of near units read as live, a cool glint rather than red
    if s > 34 and rng.random() < 0.22:
        glint = K.mix(PAPER, METAL, 0.15)
    aim = math.atan2(PAGE_CY - y, PAGE_CX - x)
    (dome if rng.random() < 0.26 else camera)(c, x, y, s, aim, body, lens,
                                              dark, glint)

# mount debris, micro pass
K.chips(c, 90, (520, 620, 1090, 1090), size=(1.4, 3.4),
        colors=(K.mix(METAL, FIELD, 0.35), K.mix(INK, FIELD, 0.3)), seed=7)
K.chips(c, 50, (0, 900, 1090, 1090), size=(1.2, 3.0),
        colors=(K.mix(METAL, FIELD, 0.45),), seed=11)


# ------------------------------------------------------ 5. the blank page
def page_pts(inset=0.0, wob=True):
    corners = [(PAGE_X0 + inset, PAGE_Y0 + inset), (PAGE_X1 - inset, PAGE_Y0 + inset),
               (PAGE_X1 - inset, PAGE_Y1 - inset), (PAGE_X0 + inset, PAGE_Y1 - inset)]
    dense = []
    for i in range(4):
        ax, ay = corners[i]
        bx, by = corners[(i + 1) % 4]
        for k in range(18):
            f = k / 18.0
            dense.append((ax + (bx - ax) * f, ay + (by - ay) * f))
    out = []
    cr, sr = math.cos(PAGE_ROT), math.sin(PAGE_ROT)
    for (px, py) in dense:
        dx, dy = px - PAGE_CX, py - PAGE_CY
        out.append((PAGE_CX + dx * cr - dy * sr, PAGE_CY + dx * sr + dy * cr))
    return K.wobble_pts(out, amp=1.6, scale=9.0, seed=SEED) if wob else out


def rot_pt(px, py):
    cr, sr = math.cos(PAGE_ROT), math.sin(PAGE_ROT)
    dx, dy = px - PAGE_CX, py - PAGE_CY
    return (PAGE_CX + dx * cr - dy * sr, PAGE_CY + dx * sr + dy * cr)


pg = page_pts()
# hard constructivist drop shadow
K.poly(c, [(x + 11, y + 13) for (x, y) in pg], fill=K.darken(INK, 0.45))
K.poly(c, pg, fill=PAPER)

# paper tooth
pmask, pmd = c.mask()
pmd.polygon(c.pts(pg), fill=140)
K.stipple(c, pmask, density=0.16, r=(0.5, 1.2), color=PAGE_SH, seed=SEED + 3)

# head label + rule, both traceable to the dossier's "Anchorage code" line
mono_s = K.mono(c, 15, medium=True)
lx, ly = rot_pt(PAGE_X0 + 34, PAGE_Y0 + 34)
K.text(c, (lx, ly), "ANCHORAGE CODE", mono_s, K.darken(PAGE_SH, 0.34),
       tracking=0.26, angle=-PAGE_ROT * 180 / math.pi)
r0 = rot_pt(PAGE_X0 + 34, PAGE_Y0 + 66)
r1 = rot_pt(PAGE_X1 - 34, PAGE_Y0 + 66)
K.line(c, [r0, r1], K.darken(PAGE_SH, 0.18), width=2.0)

# twelve empty rules
for i in range(12):
    yy = PAGE_Y0 + 108 + i * 34.0
    if yy > PAGE_Y1 - 40:
        break
    a = rot_pt(PAGE_X0 + 34, yy)
    b = rot_pt(PAGE_X1 - 34, yy)
    K.line(c, K.wobble_pts([a, b], amp=0.7, scale=14.0, seed=SEED + i),
           PAGE_SH, width=1.5)

# page edge
K.line(c, pg + [pg[0]], K.darken(PAGE_SH, 0.22), width=1.6)

# ------------------------------------------- 6. nearest lens, record light
nx, ny, ns = NEAR_X, NEAR_Y, NEAR_S
naim = math.atan2(PAGE_CY - ny, PAGE_CX - nx)
# a touch of separation so the hero lens never merges with its neighbours
K.glow(c, nx, ny, ns * 1.15, INK, alpha=78)
camera(c, nx, ny, ns, naim, K.lighten(METAL, 0.07), METAL,
       K.darken(INK, 0.16), PAPER)


def near_pt(px, py):
    return (nx + ns * (px * math.cos(naim) - py * math.sin(naim)),
            ny + ns * (px * math.sin(naim) + py * math.cos(naim)))


rx, ry = near_pt(0.06, -0.335)
K.glow(c, rx, ry, 26, RED, alpha=110)
K.circle(c, rx, ry, 3.6, fill=RED)
K.circle(c, rx, ry, 1.5, fill=K.lighten(RED, 0.55))

# ------------------------------------------------------- 7. finishing
K.mottle(c, strength=0.05, scale=3.2, seed=SEED + 5)
K.grain(c, amount=6.0, seed=SEED, mono=True)
K.vignette(c, strength=0.16, spread=1.3)

# ----------------------------------------------------------- 8. typography
size = min(K.fit_size(c, HEADLINE[0], 904, lo=40, hi=96, weight=900, opsz=144),
           K.fit_size(c, HEADLINE[1], 904, lo=40, hi=96, weight=900, opsz=144))
fh = K.fraunces(c, size, weight=900, opsz=144)
lead = size * 1.06
hy = 104.0
head_col = K.ensure_contrast(PAPER, INK, 4.5)
for i, ln in enumerate(HEADLINE):
    K.text(c, (88, hy + i * lead), ln, fh, head_col, anchor="la")

ky = hy + lead + size * 1.34
K.line(c, [(90, ky), (210, ky)], GOLD, width=2.0)
K.text(c, (90, ky + 20), KICKER, K.mono(c, 15, medium=True),
       K.mix(GOLD, PAPER, 0.25), tracking=0.22, anchor="la")

# brand marks
K.polaris(c, 952, 86, r=13, color=GOLD, core="#fff0c8", halo=0.0)
K.text(c, (118, 992), "ALASKA.AI", K.fraunces(c, 30, weight=900, opsz=144),
       PAPER, tracking=0.06, anchor="la")

# --------------------------------------------------------------- 9. meta
c.finish("out/post_image.png", {
    "date": "7 AUG 2026",
    "column": "Anchorage Desk",
    "kicker": "ANCHORAGE DESK",
    "middle_slot": "MUNICIPAL",
    "volume": "MUNICIPAL",
    "byline": "",
    "headline": "Anchorage Buys The Cameras / Before It Writes The Rules",
    "style_family": "constructivist_scatter",
    "palette": [PAPER, PAGE_SH, METAL, FIELD, INK, RED, GOLD],
    "hue_family": "blue",
    "composition": "scatter_field",
    "motifs": ["surveillance camera crowd", "blank ruled ordinance page",
               "single red record light", "street grid substrate"],
    "technique_stack": ["gradient_v", "line grid", "poly camera glyphs",
                        "wobble_pts", "stipple", "chips", "glow", "mottle",
                        "grain", "vignette"],
    "seed": SEED,
    "camera_count": len(cams),
    "eval_history": [
        {"iter": 1, "weighted": 7.56, "weakest": "detail richness",
         "note": "flat night acreage, convergence not legible, hero lens muddy, gold rule read as an underline"},
        {"iter": 2, "weighted": 8.53, "weakest": "craft and finish",
         "note": "added sight cones, parcel grid, density gradient, cleaned hero lens and moved the kicker rule"},
        {"iter": 3, "weighted": 8.64, "weakest": "originality",
         "note": "dome housing variant at 26 percent breaks the repeated stamp, softer hero separation glow"}
    ],
    "eval_final": {
        "weighted": 8.64,
        "scores": {"concept": 9, "focal": 8.5, "composition": 8.5,
                   "color": 8.5, "detail": 8.5, "craft": 8.5,
                   "typography": 9, "originality": 8, "fidelity": 9.5}
    },
})
print("rendered", len(cams), "cameras, headline size", size)
