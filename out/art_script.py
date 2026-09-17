"""Anchorage Desk — 17 SEP 2026 — "Ruaro Wants The Land / Before The Tenant"
Style: pixel_dither_aerial. Ordered-dithered satellite raster of the Mat-Su
lowland north of Houston with one parcel lifted off the map to blank paper.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as k  # noqa: E402

SEED = 91726
HEADLINE = ["Ruaro Wants The Land", "Before The Tenant"]
KICKER = "ANCHORAGE DESK  ·  MUNICIPAL  ·  17 SEP 2026"
DATE = "17 SEP 2026"

# ---- palette (OKLCH-built, then logged as hex) --------------------------
PAPER = k.oklch(0.945, 0.020, 90)
WATER = k.oklch(0.865, 0.035, 165)
BIRCH = k.oklch(0.735, 0.085, 130)
MUSKEG = k.oklch(0.530, 0.085, 140)
SPRUCE = k.oklch(0.300, 0.060, 155)
FIREWEED = k.oklch(0.560, 0.190, 350)
GOLD = "#ffc72c"
INKS = [PAPER, WATER, BIRCH, MUSKEG, SPRUCE, FIREWEED, GOLD]

W = 1080
CELL = 6                     # raster cell in design px
N = W // CELL                # 180 cells across
rng = np.random.default_rng(SEED)

c = k.Canvas(bg=PAPER, ss=2)

# ---- 1. land classes at cell resolution --------------------------------
# base terrain: warped fractal field -> 0..1
terr = k.field(3.2, 5, SEED, persistence=0.55, w=N, h=N)
terr = k.warp(terr, strength=14, scale=2.5, seed=SEED + 3)
# muskeg ponds: a second field, thresholded, concentrated lower-left
pond = k.field(5.0, 3, SEED + 7, w=N, h=N)
yy, xx = np.mgrid[0:N, 0:N] / N
pond_bias = np.clip(1.1 - (xx * 0.9 + (1 - yy) * 0.9), 0, 1)
pond_v = pond + 0.14 * pond_bias

# river: braided band from upper-left to lower-right, two channels
def river_mask():
    m = np.zeros((N, N))
    t = np.linspace(0, 1, 400)
    n1 = k.noise1d(400, 2.5, 3, SEED + 11) - 0.5
    n2 = k.noise1d(400, 4.0, 3, SEED + 13) - 0.5
    cx = t * N
    cy = (0.24 + 0.62 * t) * N + n1 * 34
    cy2 = cy + 9 + n2 * 22
    n3 = k.noise1d(400, 3.0, 3, SEED + 17) - 0.5
    cy3 = cy - 7 + n3 * 18
    for i in range(400):
        for ch, wid in ((cy[i], 2.2 + 1.6 * abs(n2[i])), (cy2[i], 1.4 + 1.2 * abs(n1[i])),
                        (cy3[i], 1.2 + 1.0 * abs(n3[i]))):
            x0, y0 = int(cx[i]), int(ch)
            r = int(wid)
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = x0 + dx, y0 + dy
                        if 0 <= px < N and 0 <= py < N:
                            m[py, px] = 1
    return m

riv = river_mask()

# corridor: straight pale swath, utility corridor (existing)
def corridor_mask(width=2.6):
    m = np.zeros((N, N))
    ax, ay = 900 / CELL, N        # bottom, right of parcel
    bx, by = 1050 / CELL, 0       # top-right
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy)
    for y in range(N):
        for x in range(N):
            d = abs(dy * (x - ax) - dx * (y - ay)) / L
            if d < width:
                m[y, x] = 1
    return m

cor = corridor_mask()

# continuous "value" per cell that we posterize with a dither:
# 0 water, 1 birch, 2 muskeg, 3 spruce  (paper is reserved for the parcel)
v = terr.copy()
v = (v - v.min()) / (v.max() - v.min())
# class thresholds on v: spruce (dark) high, birch low; ponds override to water
bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
B = np.tile(bayer, (N // 4 + 1, N // 4 + 1))[:N, :N]

cls = np.full((N, N), 1, dtype=int)  # birch default
# muskeg vs birch boundary ~0.50, spruce above ~0.68 with dither bands
edge = 0.07
m_mix = np.clip((v - (0.50 - edge)) / (2 * edge), 0, 1)
cls = np.where(m_mix > B, 2, 1)
s_mix = np.clip((v - (0.70 - edge)) / (2 * edge), 0, 1)
cls = np.where(s_mix > B, 3, cls)
# ponds -> water, with dithered rim
p_mix = np.clip((pond_v - (0.78 - 0.04)) / 0.08, 0, 1)
cls = np.where(p_mix > B, 0, cls)
# river -> water; gravel bars (birch specks) inside river handled later
cls = np.where(riv > 0, 0, cls)
# corridor -> cleared gravel strip (own class 4)
cls = np.where(cor > 0, 4, cls)
# a thin road from the left edge to the corridor (class 4, one cell wide, wobbled)
rd = k.noise1d(N, 3.0, 2, SEED + 23) - 0.5
for x in range(N):
    y = int(0.80 * N + rd[x] * 10)
    if 0 <= y < N and cls[y, x] != 0:
        cls[y, x] = 4
CLEARED = k.lighten(BIRCH, 0.11)
CLASS_COL = {0: WATER, 1: BIRCH, 2: MUSKEG, 3: SPRUCE, 4: CLEARED}

# ---- 2. rasterize cells --------------------------------------------------
lay, ld = c.layer()
for y in range(N):
    for x in range(N):
        col = CLASS_COL[int(cls[y, x])]
        # subtle per-cell tonal jitter so flats aren't dead
        j = rng.uniform(-0.018, 0.018)
        col = k.lighten(col, j) if abs(j) > 0.012 else col
        ld.rectangle([c.s(x * CELL), c.s(y * CELL),
                      c.s((x + 1) * CELL) - 1, c.s((y + 1) * CELL) - 1],
                     fill=(*k.hex_to_rgb(col), 255))
c.composite(lay)

# micro: gravel bars along river as pale chips, and pond-edge sedge specks
riv_img = Image.fromarray((riv * 255).astype(np.uint8), "L").resize((W, W), Image.NEAREST)
k.chips(c, 420, (0, 0, W, W), size=(2, 5), colors=(k.lighten(WATER, 0.05), BIRCH),
        seed=SEED + 21, mask_img=riv_img)
# corridor tower dots (existing utility line)
ax, ay, bx, by = 900, 1080, 1050, 0
L = math.hypot(bx - ax, by - ay)
nt = int(L / 64)
for i in range(nt + 1):
    t = i / nt
    px, py = ax + (bx - ax) * t, ay + (by - ay) * t
    k.circle(c, px, py, 3.4, fill=SPRUCE)
    k.circle(c, px, py, 1.4, fill=PAPER)
    # tiny cross-arm so the dots read as towers, and a faint wire between them
    k.line(c, [(px - 6, py), (px + 6, py)], SPRUCE, 1.4)
    if i < nt:
        t2 = (i + 1) / nt
        k.line(c, [(px, py), (ax + (bx - ax) * t2, ay + (by - ay) * t2)],
               k.mix(SPRUCE, CLEARED, 0.45), 1.0)

# micro: sedge specks around pond rims and spruce speckle inside muskeg
pond_img = Image.fromarray(((cls == 0) * 255).astype(np.uint8), "L").resize((W, W), Image.NEAREST)
rim = pond_img.filter(__import__("PIL.ImageFilter", fromlist=["MaxFilter"]).MaxFilter(15))
rim = Image.fromarray(np.clip(np.asarray(rim, int) - np.asarray(pond_img, int), 0, 255).astype(np.uint8), "L")
k.chips(c, 900, (0, 0, W, W), size=(1.5, 3.5), colors=(MUSKEG, k.darken(BIRCH, 0.12)),
        seed=SEED + 31, mask_img=rim)
musk_img = Image.fromarray(((cls == 2) * 255).astype(np.uint8), "L").resize((W, W), Image.NEAREST)
k.stipple(c, musk_img, density=0.05, r=(0.8, 1.6), color=SPRUCE, seed=SEED + 33)
# scale cues along the road: a handful of tiny paper structures
r3 = np.random.default_rng(SEED + 41)
for x in range(60, 880, 110):
    y = int(0.80 * N + rd[min(N - 1, x // CELL)] * 10) * CELL
    if cls[min(N - 1, y // CELL), min(N - 1, x // CELL)] != 0:
        off = r3.integers(-16, -8)
        k.poly(c, [(x, y + off), (x + 7, y + off), (x + 7, y + off + 6), (x, y + off + 6)], fill=PAPER)
        k.line(c, [(x + 3, y + off + 6), (x + 3, y)], k.mix(CLEARED, SPRUCE, 0.4), 1.0)
# a small gravel pit near the corridor, lower right
pit = k.blob_pts(1000, 900, 26, wobble=0.22, seed=SEED + 43)
k.poly(c, pit, fill=k.lighten(CLEARED, 0.05))
k.chips(c, 40, (970, 870, 1030, 930), size=(1.5, 3), colors=(BIRCH, MUSKEG), seed=SEED + 45)
k.grain(c, amount=4.5, seed=SEED + 2)

# ---- 3. the parcel, lifted to paper ---------------------------------------
# rectilinear township-style polygon with two section jogs
P = [(300, 214), (820, 214), (820, 262), (940, 262), (940, 700),
     (420, 700), (420, 640), (300, 640)]
# cast shadow: the parcel is lifted off the map, so it throws a soft shadow down-right
shl, shd = c.layer()
shd.polygon(c.pts([(x + 9, y + 11) for x, y in P]), fill=(*k.hex_to_rgb(SPRUCE), 120))
shl = shl.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(c.s(5)))
c.composite(shl)
k.poly(c, P, fill=PAPER)
# faint paper mottle inside the parcel only
mask_img, md = c.mask()
md.polygon(c.pts(P), fill=255)
mot = k.field(3.0, 3, SEED + 5, w=W // 4, h=W // 4)
from scipy.ndimage import zoom  # noqa: E402
mot = zoom(mot, 4 * c.ss, order=1)[:c.W, :c.W]
arr = np.asarray(c.img, float)
mul = 1.0 - 0.07 * (mot - 0.5) * 2
mm = np.asarray(mask_img, float)[..., None] / 255.0
arr = arr * (1 - mm) + arr * mul[..., None] * mm
c.paste_img(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB"))

# faint township section lines showing through the paper (very low contrast)
SEC = k.mix(PAPER, MUSKEG, 0.10)
secl, sd = c.layer()
for gx in range(300, 941, 160):
    k.line(c, [(gx, 214), (gx, 700)], SEC, 1.0, d=sd)
for gy in range(214, 701, 160):
    k.line(c, [(300, gy), (940, gy)], SEC, 1.0, d=sd)
c.img.paste(secl, (0, 0), Image.composite(mask_img, Image.new("L", (c.W, c.W), 0), secl.getchannel("A")))
c.draw = ImageDraw.Draw(c.img, "RGBA")
# tiny dimension ticks along the inside of each edge (surveyor's chain marks)
TICK = k.mix(PAPER, MUSKEG, 0.28)
for (x0, y0), (x1, y1) in zip(P, P[1:] + P[:1]):
    seg = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
    nx, ny = -uy, ux
    # inward normal: toward parcel centroid
    cxp, cyp = 620, 457
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if (mx + nx * 10 - cxp) ** 2 + (my + ny * 10 - cyp) ** 2 > (mx - nx * 10 - cxp) ** 2 + (my - ny * 10 - cyp) ** 2:
        nx, ny = -nx, -ny
    n = int(seg / 40)
    for i in range(1, n):
        t = i * 40
        px, py = x0 + ux * t, y0 + uy * t
        ln = 9 if i % 4 == 0 else 5
        k.line(c, [(px + nx * 5, py + ny * 5), (px + nx * (5 + ln), py + ny * (5 + ln))], TICK, 1.0)
# inner shadow line (1 px, muskeg at low alpha) just inside the edge
ins = [(x + (2 if x < 600 else -2), y + (2 if y < 450 else -2)) for x, y in P]
k.line(c, ins + [ins[0]], k.mix(PAPER, MUSKEG, 0.35), width=1.2)

# dashed fireweed boundary with hand jitter
def dashed(pts, dash=14, gap=9, width=4, color=FIREWEED, seed=0):
    r2 = np.random.default_rng(seed)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        seg = math.hypot(x1 - x0, y1 - y0)
        n = int(seg / (dash + gap))
        for i in range(n + 1):
            s0 = i * (dash + gap)
            s1 = min(seg, s0 + dash)
            if s1 <= s0:
                continue
            ux, uy = (x1 - x0) / seg, (y1 - y0) / seg
            jx, jy = r2.uniform(-0.8, 0.8, 2)
            k.line(c, [(x0 + ux * s0 + jx, y0 + uy * s0 + jy),
                       (x0 + ux * s1 + jx, y0 + uy * s1 + jy)], color, width)

dashed(P, seed=SEED + 8)
# corner ticks
for x, y in P:
    k.line(c, [(x - 9, y), (x + 9, y)], FIREWEED, 2.2)
    k.line(c, [(x, y - 9), (x, y + 9)], FIREWEED, 2.2)

# ghost tenant footprint (dotted), and a dotted pad line toward the corridor
def dotted_rect(x, y, w, h, step=6.0, r=1.4, color=FIREWEED):
    per = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    for (x0, y0), (x1, y1) in zip(per, per[1:] + per[:1]):
        seg = math.hypot(x1 - x0, y1 - y0)
        n = int(seg / step)
        for i in range(n + 1):
            t = i / n
            k.circle(c, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, fill=color)

GX, GY, GW, GH = 760, 585, 96, 64
dotted_rect(GX, GY, GW, GH)
# inner bays (three dotted verticals) so it reads as a building pad
for i in (1, 2):
    x = GX + GW * i / 3
    for j in range(0, GH, 6):
        k.circle(c, x, GY + j, 1.0, fill=k.mix(FIREWEED, PAPER, 0.35))
# pad line to corridor (dotted), toward the corridor point nearest the pad
tx, ty = 966, 617   # on-corridor point just outside the parcel's right edge
for i in range(0, 60):
    t = i / 60
    px, py = GX + GW + (tx - GX - GW) * t, GY + GH / 2 + (ty - GY - GH / 2) * t
    if i % 2 == 0:
        k.circle(c, px, py, 1.1, fill=FIREWEED)

# one survey stake with a small flag, and a dotted access track up from the road
for i in range(0, 40):
    t = i / 40
    px, py = 356 + (356 - 356) * t, 858 - (858 - 700) * t
    if i % 2 == 0:
        k.circle(c, px, py, 1.0, fill=k.mix(FIREWEED, PAPER, 0.25))
k.line(c, [(356, 700), (356, 636)], FIREWEED, 3.2)
k.poly(c, [(356, 636), (382, 644), (356, 652)], fill=FIREWEED)
k.circle(c, 356, 700, 3.5, fill=FIREWEED)

# ---- 4. type -------------------------------------------------------------
X0, Y0, MAXW = 340, 262, 560
f_size = min(k.fit_size(c, HEADLINE[0], MAXW, lo=40, hi=110, opsz=144, weight=900),
             k.fit_size(c, HEADLINE[1], MAXW, lo=40, hi=110, opsz=144, weight=900))
f_size = min(f_size, 84)
fh = k.fraunces(c, f_size, weight=900, opsz=144)
lead = f_size * 1.06
for i, ln in enumerate(HEADLINE):
    k.text(c, (X0, Y0 + i * lead), ln, fh, SPRUCE, anchor="la", tracking=-0.01)
ky = Y0 + len(HEADLINE) * lead + 18
fm = k.mono(c, 15, medium=True)
k.text(c, (X0 + 2, ky), KICKER, fm, k.mix(SPRUCE, PAPER, 0.25), anchor="la",
       tracking=0.14)
# thin rule under kicker
k.line(c, [(X0 + 2, ky + 30), (X0 + 122, ky + 30)], FIREWEED, 2)

# wordmark chip bottom-left
fw = k.fraunces(c, 30, weight=900, opsz=144)
k.chip(c, (72, 1000), "ALASKA.AI", fw, PAPER, SPRUCE, pad=12, anchor="lm",
       tracking=0.02, radius=5)

# polaris top-right with a soft paper halo so it reads on the raster
k.glow(c, 1008, 72, 30, PAPER, alpha=120)
k.polaris(c, 1008, 72, r=13, color=GOLD)

k.vignette(c, strength=0.10, spread=1.4)

META = {
    "date": DATE, "column": "Anchorage Desk", "kicker": "ANCHORAGE DESK",
    "middle_slot": "MUNICIPAL", "volume": "MUNICIPAL", "byline": "",
    "headline": " / ".join(HEADLINE),
    "style_family": "pixel_dither_aerial", "palette": INKS,
    "hue_family": "green", "composition": "aerial_plan_view",
    "motifs": ["dithered aerial land raster", "braided river", "muskeg ponds",
               "utility corridor with tower dots along the parcel edge", "wobbled access road", "township section lines", "parcel lifted to blank paper",
               "dashed fireweed boundary", "ghost tenant footprint", "lone survey stake with access track", "tiny road structures", "gravel pit"],
    "technique_stack": ["field", "warp", "noise1d", "bayer_dither", "chips", "stipple", "blob_pts", "cast_shadow",
                        "grain", "mottle", "line", "circle", "fraunces", "mono",
                        "chip", "glow", "polaris", "vignette"],
    "seed": SEED,
    "eval_history": [{"iter": 1, "weighted": 7.3, "weakest": "detail/composition", "note": "river a blobby pale mass, corridor hidden under the parcel, dead paper inside the parcel"}, {"iter": 2, "weighted": 8.27, "weakest": "detail", "note": "braided river, corridor with towers along the parcel edge, section lines; raster still flat away from the focal"}, {"iter": 3, "weighted": 8.33, "weakest": "composition/craft", "note": "sedge rims, muskeg stipple, road structures, gravel pit, access track; parcel still reads pasted rather than lifted"}],
    "eval_final": {"weighted": 8.6, "scores": {"concept": 9, "focal": 8.5, "composition": 8.5, "color": 8, "detail": 8.5, "craft": 8.5, "typography": 9, "originality": 8.5, "fidelity": 9}},
}
c.finish("out/post_image.png", META)
print("rendered", f_size)
