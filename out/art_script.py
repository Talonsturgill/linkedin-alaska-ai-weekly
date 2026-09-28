"""The Stack — 28 SEP 2026 — VEHICLES
"$272M runs through one desk." An hourglass whose only passage is one
pinched neck: the Rural Health Transformation Program pass-through.
Style: still_life_gouache. See out/art_plan.md.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import art_kit as ak

SEED = 928
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
WALL_DK = ak.oklch(0.20, 0.055, 18)
WALL = ak.oklch(0.30, 0.085, 22)
WALNUT = ak.oklch(0.40, 0.07, 50)
WALNUT_LT = ak.oklch(0.58, 0.08, 62)
GOLD = ak.oklch(0.80, 0.145, 82)
CREAM = ak.oklch(0.94, 0.03, 85)
ICE = ak.oklch(0.86, 0.07, 205)
PALETTE = [WALL_DK, WALL, WALNUT, WALNUT_LT, GOLD, CREAM, ICE]

GOLD_DK = ak.mix(GOLD, WALNUT, 0.45)
GOLD_LT = ak.mix(GOLD, CREAM, 0.45)
WALNUT_DK = ak.mix(WALNUT, WALL_DK, 0.55)

c = ak.Canvas(bg=WALL_DK)
W = c.W
SS = c.ss

# ---------------------------------------------------------------- geometry
CX = 772.0
TOP_Y0, TOP_Y1 = 92.0, 124.0
BOT_Y0, BOT_Y1 = 956.0, 988.0
NECK_Y = 540.0
NECK_W = 8.0
PLATE_X0, PLATE_X1 = 566.0, 978.0
POSTS = [596.0, 948.0]


def bulb_w(y):
    """Half-width of the glass at design y (vectorised)."""
    y = np.asarray(y, float)
    up = y <= NECK_Y
    s = np.where(up, (NECK_Y - y) / (NECK_Y - TOP_Y1),
                 (y - NECK_Y) / (BOT_Y0 - NECK_Y))
    s = np.clip(s, 0, 1)
    s2 = np.clip(s - 0.02, 0, 1)
    core = np.sin(np.pi / 2 * np.minimum(1.0, s2 / 0.58)) ** 1.3
    shoulder = 1 - 0.22 * np.clip((s - 0.58) / 0.42, 0, 1) ** 2
    return NECK_W + 170.0 * core * shoulder


def glass_outline(side, y0, y1, n=220):
    ys = np.linspace(y0, y1, n)
    ws = bulb_w(ys)
    return [(CX + side * w, y) for w, y in zip(ws, ys)]


def glass_poly():
    left = glass_outline(-1, TOP_Y1, BOT_Y0)
    right = glass_outline(1, TOP_Y1, BOT_Y0)[::-1]
    return left + right


# internal-res coordinate grids (design units)
gy, gx = (np.mgrid[0:W, 0:W].astype(np.float32) + 0.5) / SS


def mask_from(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "L")


GLASS = (np.abs(gx - CX) <= bulb_w(gy)) & (gy >= TOP_Y1) & (gy <= BOT_Y0)


def fill_mask(color, m, alpha=255):
    lay = Image.new("RGBA", (W, W), (*ak.hex_to_rgb(color), alpha))
    base = c.img.convert("RGBA")
    a = m if alpha == 255 else m.point(lambda v: v * alpha // 255)
    base.paste(lay, (0, 0), a)
    c.img = base.convert("RGB")
    c.draw = ImageDraw.Draw(c.img, "RGBA")


def paste_rgb(arr, m):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    c.img.paste(im, (0, 0), m)
    c.draw = ImageDraw.Draw(c.img, "RGBA")


# ================================================================ 1. WALL
# raking light from upper-left: oxblood pool behind the glass, wine-black
# corners.
wall_d = np.array(ak.hex_to_rgb(WALL_DK), np.float32)
wall_m = np.array(ak.hex_to_rgb(WALL), np.float32)
d = np.hypot((gx - 700) / 520, (gy - 470) / 600)
t = np.clip(1 - d, 0, 1) ** 1.4
tex = ak.field(3.0, 4, SEED + 1, w=540, h=540)
tex = np.kron(tex, np.ones((4, 4)))[:W, :W].astype(np.float32)
t = np.clip(t * (0.88 + 0.24 * tex), 0, 1)
wall = wall_d[None, None] * (1 - t[..., None]) + wall_m[None, None] * t[..., None]
c.paste_img(Image.fromarray(wall.astype(np.uint8), "RGB"))

# window light falling across the wall from the upper left (soft shaft)
lay, ld = c.layer()
ld.polygon(c.pts([(-40, 40), (250, -20), (980, 860), (620, 1000)]),
           fill=(*ak.hex_to_rgb(ak.mix(WALL, WALNUT_LT, 0.35)), 34))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(60)))
c.composite(lay)
# faint window-mullion shadows inside the shaft
lay, ld = c.layer()
for off_ in (0, 150):
    ld.polygon(c.pts([(60 + off_, 30), (84 + off_, 26), (820 + off_, 900), (796 + off_, 904)]),
               fill=(*ak.hex_to_rgb(WALL_DK), 30))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(14)))
c.composite(lay)

# shelf the hourglass stands on
shelf_top = 986.0
lay, ld = c.layer()
for i in range(int((1080 - shelf_top) * SS)):
    tt = i / ((1080 - shelf_top) * SS)
    col = ak.mix(ak.mix(WALNUT_DK, WALL, 0.35), WALL_DK, tt ** 0.7)
    ld.line([(0, shelf_top * SS + i), (W, shelf_top * SS + i)],
            fill=(*ak.hex_to_rgb(col), 255))
c.composite(lay)
ak.line(c, [(0, shelf_top), (1080, shelf_top)], ak.mix(WALNUT_LT, WALL, 0.5), 1.4)
# shelf wood grain
for k in range(9):
    yy = shelf_top + 8 + k * 9.5 + rng.uniform(-2, 2)
    pts = [(x, yy + 1.6 * math.sin(x / rng.uniform(60, 140) + k)) for x in range(0, 1081, 12)]
    ak.hand_line(c, pts, ak.mix(WALNUT_DK, WALL_DK, 0.3), 0.9, amp=0.8, seed=SEED + 40 + k)

# wall paper-stipple (meso texture for the negative space)
wall_mask = mask_from(((gy < shelf_top)).astype(np.float32) * 0.55)
ak.stipple(c, wall_mask, density=0.22, r=(0.4, 0.9), color=ak.mix(WALL_DK, WALL, 0.25), seed=SEED + 2)
ak.stipple(c, wall_mask, density=0.10, r=(0.4, 0.8), color=ak.mix(WALL, WALNUT_LT, 0.25), seed=SEED + 3)
ak.mottle(c, strength=0.05, scale=2.5, seed=SEED + 4)

# ================================================================ 2. CAST SHADOW
sh, sd = c.mask()
off = (38, 16)
gp = [(x + off[0], y + off[1]) for x, y in glass_poly()]
sd.polygon(c.pts(gp), fill=150)
sd.rectangle([c.s(PLATE_X0 + off[0]), c.s(TOP_Y0 + off[1]),
              c.s(PLATE_X1 + off[0]), c.s(TOP_Y1 + off[1])], fill=170)
for px in POSTS:
    sd.rectangle([c.s(px - 14 + off[0]), c.s(TOP_Y1 + off[1]),
                  c.s(px + 14 + off[0]), c.s(BOT_Y0)], fill=170)
sh = sh.filter(ImageFilter.GaussianBlur(c.s(16)))
cut = mask_from((gy < shelf_top).astype(np.float32))
sh = Image.fromarray((np.asarray(sh, np.float32) * np.asarray(cut, np.float32) / 255).astype(np.uint8))
fill_mask(ak.mix(WALL_DK, "#000000", 0.55), sh)
# contact shadow on the shelf
ct, cd = c.mask()
cd.ellipse([c.s(PLATE_X0 - 10), c.s(shelf_top - 4), c.s(PLATE_X1 + 50), c.s(shelf_top + 22)], fill=200)
ct = ct.filter(ImageFilter.GaussianBlur(c.s(8)))
fill_mask(ak.mix(WALL_DK, "#000000", 0.5), ct)

# ================================================================ 3. BACK POST


def post_r(y):
    y = np.asarray(y, float)
    r = 11.5 + 0 * y
    for yc, amp, wd in [(142, 7.5, 9), (162, 3.5, 5), (540, 7.0, 10), (522, 3.0, 4),
                        (558, 3.0, 4), (918, 3.5, 5), (938, 7.5, 9)]:
        r = r + amp * np.exp(-((y - yc) / wd) ** 2)
    # gentle swell between beads
    r = r + 2.2 * np.sin(np.clip((y - 170) / (510 - 170), 0, 1) * np.pi)
    r = r + 2.2 * np.sin(np.clip((y - 570) / (910 - 570), 0, 1) * np.pi)
    return r


def post_pts(px, scale=1.0):
    ys = np.linspace(TOP_Y1, BOT_Y0, 260)
    rs = post_r(ys) * scale
    return [(px - r, y) for r, y in zip(rs, ys)] + \
           [(px + r, y) for r, y in zip(rs[::-1], ys[::-1])]


ak.poly(c, post_pts(CX, 0.85), fill=ak.mix(WALNUT_DK, WALL_DK, 0.4))

# ================================================================ 4. GLASS INTERIOR
gm = mask_from(GLASS.astype(np.float32))
# glass holds a slightly lifted, cooler version of the wall
inner = np.asarray(c.img, np.float32)
lift = np.array(ak.hex_to_rgb(ak.mix(WALL, CREAM, 0.18)), np.float32)
edge = np.clip(np.abs(gx - CX) / np.maximum(bulb_w(gy), 1), 0, 1) ** 3
k_in = (0.10 + 0.22 * edge)[..., None]
inner = inner * (1 - k_in) + lift[None, None] * k_in
paste_rgb(inner, gm)

# ================================================================ 5. ETCHED MAP (lower bulb)
MAP_CX, MAP_CY, MAP_LAT0, MAP_LON0, S = CX - 6, 778.0, 63.0, -151.0, 13.4


def proj(lon, lat):
    return (MAP_CX + (lon - MAP_LON0) * math.cos(math.radians(lat)) * S,
            MAP_CY - (lat - MAP_LAT0) * S)


COAST = [(-130.0, 55.9), (-130.1, 56.1), (-131.8, 56.6), (-132.5, 57.2), (-133.4, 58.4),
         (-134.9, 59.4), (-135.5, 59.8), (-137.5, 59.2), (-139.0, 60.0), (-141.0, 60.3),
         (-141.0, 69.65), (-143.5, 70.1), (-146.0, 70.2), (-148.5, 70.4), (-151.0, 70.5),
         (-153.0, 70.9), (-156.8, 71.35), (-158.5, 70.8), (-160.0, 70.6), (-162.0, 70.2),
         (-163.8, 69.4), (-165.5, 68.9), (-166.8, 68.35), (-164.5, 67.7), (-163.5, 67.1),
         (-162.5, 66.9), (-161.8, 66.3), (-163.9, 66.2), (-164.7, 66.5), (-166.2, 66.1),
         (-168.1, 65.6), (-166.6, 64.6), (-165.4, 64.5), (-163.2, 64.6), (-161.2, 64.4),
         (-160.8, 63.9), (-161.4, 63.5), (-162.6, 63.6), (-164.3, 63.1), (-165.0, 62.6),
         (-165.8, 61.8), (-165.5, 61.1), (-164.6, 60.8), (-164.9, 60.3), (-164.0, 59.9),
         (-162.3, 60.0), (-161.9, 59.1), (-161.9, 58.7), (-161.0, 58.6), (-160.3, 58.9),
         (-158.9, 58.4), (-157.4, 58.7), (-157.0, 58.4), (-157.6, 57.5), (-158.6, 56.9),
         (-160.0, 56.4), (-161.5, 55.9), (-162.8, 55.3), (-163.9, 54.9), (-163.0, 54.7),
         (-161.2, 55.3), (-159.5, 55.7), (-158.0, 56.2), (-156.6, 56.9), (-155.2, 57.6),
         (-154.0, 58.4), (-153.2, 59.0), (-152.3, 59.8), (-151.9, 60.5), (-150.5, 61.3),
         (-150.0, 61.1), (-151.3, 60.4), (-151.8, 59.8), (-151.8, 59.2), (-150.8, 59.4),
         (-149.6, 59.7), (-148.6, 60.0), (-147.8, 60.3), (-146.3, 60.5), (-145.3, 60.4),
         (-144.2, 60.0), (-142.5, 60.05), (-141.3, 59.9), (-140.2, 59.7), (-139.6, 59.5),
         (-138.3, 58.9), (-137.0, 58.3), (-136.4, 57.9), (-135.8, 57.3), (-135.0, 56.5),
         (-134.6, 56.0), (-133.8, 55.6), (-133.1, 55.0), (-132.0, 54.7), (-130.6, 54.8),
         (-130.0, 55.9)]
ISLANDS = [
    [(-154.6, 57.3), (-153.6, 56.9), (-152.3, 57.4), (-152.1, 57.9), (-153.0, 58.1),
     (-154.2, 57.8), (-154.6, 57.3)],                       # Kodiak
    [(-171.0, 63.5), (-169.7, 63.2), (-168.7, 63.3), (-169.4, 63.8), (-171.0, 63.8),
     (-171.0, 63.5)],                                        # St Lawrence
    [(-166.8, 60.1), (-166.0, 59.8), (-165.5, 60.2), (-166.2, 60.4), (-166.8, 60.1)],  # Nunivak
    [(-135.9, 56.3), (-134.9, 56.3), (-134.8, 57.3), (-135.8, 57.6), (-135.9, 56.3)],  # Baranof-ish
]
VILLAGES = [
    (71.29, -156.79, 1), (68.35, -166.80, 0), (66.90, -162.60, 1), (64.50, -165.40, 1),
    (63.87, -160.79, 0), (60.79, -161.76, 1), (59.04, -158.46, 1), (58.69, -156.66, 0),
    (57.79, -152.40, 1), (55.34, -160.50, 0), (64.74, -156.93, 1), (66.56, -145.25, 1),
    (63.34, -142.99, 0), (62.11, -145.55, 1), (60.54, -145.76, 0), (61.13, -146.35, 0),
    (60.10, -149.44, 0), (59.64, -151.55, 0), (57.05, -135.33, 1), (55.34, -131.64, 0),
    (56.81, -132.96, 0), (56.47, -132.38, 0), (55.48, -133.15, 0), (59.55, -139.73, 0),
    (59.24, -135.44, 0), (62.95, -155.60, 0), (61.58, -159.54, 0), (62.05, -163.17, 0),
    (61.53, -166.10, 1), (62.78, -164.52, 0), (66.60, -160.00, 0), (66.84, -161.03, 0),
    (67.09, -157.85, 0), (68.14, -151.74, 1), (70.13, -143.62, 0), (70.64, -160.04, 0),
    (70.22, -151.00, 0), (65.17, -152.08, 0), (64.04, -145.73, 0), (59.06, -160.38, 0),
    (59.75, -161.90, 0), (61.53, -165.58, 0), (63.69, -170.48, 0), (60.55, -151.26, 0),
]

etch = Image.new("RGBA", (W, W), (0, 0, 0, 0))
ed = ImageDraw.Draw(etch, "RGBA")
cr = ak.hex_to_rgb(CREAM)
gr = ak.hex_to_rgb(GOLD)
coast_pts = ak.wobble_pts([proj(*p) for p in COAST], amp=0.6, seed=SEED + 5)
# faint land tint + coast line
ed.polygon(c.pts(coast_pts), fill=(*cr, 30))
ed.line(c.pts(coast_pts), fill=(*cr, 165), width=int(c.s(1.5)), joint="curve")
for isl in ISLANDS:
    ip = [proj(*p) for p in isl]
    ed.polygon(c.pts(ip), fill=(*cr, 30), outline=(*cr, 140))
# Aleutian chain dots heading west
for i, lon in enumerate(np.linspace(-165.0, -172.5, 8)):
    x, y = proj(lon, 54.1 - 0.22 * i)
    rr = c.s(1.6)
    ed.ellipse([c.s(x) - rr, c.s(y) - rr, c.s(x) + rr, c.s(y) + rr], fill=(*cr, 90))
# graticule whisper
for lat in (60, 65, 70):
    pts = [proj(lon, lat) for lon in np.linspace(-172, -128, 60)]
    for a, b in zip(pts[::2], pts[1::2]):
        ed.line(c.pts([a, b]), fill=(*cr, 34), width=int(c.s(0.8)))
for lon in (-165, -155, -145, -135):
    pts = [proj(lon, lat) for lat in np.linspace(53, 72, 40)]
    for a, b in zip(pts[::2], pts[1::2]):
        ed.line(c.pts([a, b]), fill=(*cr, 30), width=int(c.s(0.8)))
# routes from the neck to every village
neck = (CX, NECK_Y + 6)
vpts = []
for lat, lon, lit in VILLAGES:
    x, y = proj(lon, lat)
    vpts.append((x, y, lit))
    mid = ((neck[0] + x) / 2 + (x - neck[0]) * 0.08, (neck[1] + y) / 2 - 18)
    curve = [((1 - u) ** 2 * neck[0] + 2 * (1 - u) * u * mid[0] + u * u * x,
              (1 - u) ** 2 * neck[1] + 2 * (1 - u) * u * mid[1] + u * u * y)
             for u in np.linspace(0, 1, 40)]
    if lit:
        ed.line(c.pts(curve), fill=(*gr, 120), width=int(c.s(1.1)), joint="curve")
    else:
        for a, b in zip(curve[::3], curve[1::3]):
            ed.line(c.pts([a, b]), fill=(*cr, 44), width=int(c.s(0.8)))
etch_m = Image.fromarray((np.asarray(etch.getchannel("A"), np.float32) *
                          (GLASS & (gy > NECK_Y + 4)).astype(np.float32)).astype(np.uint8))
etch.putalpha(etch_m)
c.composite(etch)

# ================================================================ 6. UPPER SAND
surf = 304 + 20 * np.exp(-((gx - CX) / 125) ** 2) + 12 * np.exp(-((gx - CX) / 20) ** 2) + 3.0 * (ak.field(6, 2, SEED + 7, w=W, h=1)[0][None, :] - 0.5)
SAND_U = GLASS & (gy <= NECK_Y) & (gy >= surf)
su = mask_from(SAND_U.astype(np.float32))
gold = np.array(ak.hex_to_rgb(GOLD), np.float32)
gold_dk = np.array(ak.hex_to_rgb(GOLD_DK), np.float32)
gold_lt = np.array(ak.hex_to_rgb(GOLD_LT), np.float32)
xn = np.clip((gx - CX) / np.maximum(bulb_w(gy), 1), -1, 1)
shade = np.clip(0.5 + 0.55 * xn, 0, 1) ** 1.2          # right side into shadow
toplit = np.clip(1 - (gy - surf) / 26, 0, 1)             # lit skin on the surface
crater = np.exp(-((gx - CX) / 60) ** 2) * np.clip(1 - (gy - surf) / 40, 0, 1)
sfield = ak.field(9, 3, SEED + 8, w=540, h=540)
sfield = np.kron(sfield, np.ones((4, 4)))[:W, :W].astype(np.float32)
arr = gold[None, None] * (1 - shade[..., None] * 0.75) + gold_dk[None, None] * (shade[..., None] * 0.75)
arr = arr * (1 - toplit[..., None] * 0.55) + gold_lt[None, None] * (toplit[..., None] * 0.55)
arr = arr * (1 - crater[..., None] * 0.35) + gold_dk[None, None] * (crater[..., None] * 0.35)
arr = arr * (0.94 + 0.12 * sfield[..., None])
paste_rgb(arr, su)
# sand grain texture
ak.stipple(c, mask_from(SAND_U * (0.35 + 0.6 * shade)), density=2.2, r=(0.35, 0.8),
           color=ak.mix(GOLD_DK, WALNUT, 0.35), seed=SEED + 9)
ak.stipple(c, mask_from(SAND_U * (1 - shade) * 0.8), density=1.2, r=(0.35, 0.75),
           color=GOLD_LT, seed=SEED + 10)
# technology grains scattered through the federal sand
ak.chips(c, 60, (CX - 170, 290, CX + 170, 540), size=(1.2, 2.4), colors=(ICE,),
         seed=SEED + 11, mask_img=su)
# lit skin along the sand surface edge
rim_pts = [(x, 304 + 20 * math.exp(-((x - CX) / 125) ** 2) + 12 * math.exp(-((x - CX) / 20) ** 2))
           for x in np.linspace(CX - 176, CX + 176, 200)]
rim_pts = [(x, y) for x, y in rim_pts if abs(x - CX) < float(bulb_w(y)) - 2]
ak.line(c, rim_pts, GOLD_LT, 1.4)
# slip lines converging on the crater mouth (sand draining to the neck)
sl, sld = c.layer()
for i in range(34):
    ang = rng.uniform(-1, 1)
    x0 = CX + ang * 150
    y0 = 304 + 20 * math.exp(-((x0 - CX) / 125) ** 2) + 12 * math.exp(-((x0 - CX) / 20) ** 2) + rng.uniform(1, 4)
    pts = [(x0 + (CX - x0) * u, y0 + (338 - y0) * u ** 1.6) for u in np.linspace(0, 0.7, 18)]
    col = ak.hex_to_rgb(ak.mix(GOLD_DK, WALNUT, 0.3) if ang > 0 else ak.mix(GOLD_DK, GOLD, 0.3))
    sld.line(c.pts(pts), fill=(*col, 175), width=int(c.s(1.0)), joint="curve")
c.composite(sl)
# ================================================================ 7. LOWER PILE
pile_base = BOT_Y0 - 6
pile = []
for u in np.linspace(-1, 1, 120):
    x = CX + u * 118
    y = 902 + (pile_base - 902) * (abs(u) ** 0.8)
    pile.append((x, y))
pile = [(CX - 118, pile_base)] + pile + [(CX + 118, pile_base)]
pm, pd = c.mask()
pd.polygon(c.pts(ak.wobble_pts(pile, amp=0.8, seed=SEED + 12)), fill=255)
pm_arr = np.asarray(pm, np.float32) / 255 * GLASS
pmask = mask_from(pm_arr)
pshade = np.clip(0.5 + (gx - CX) / 180, 0, 1)
parr = gold[None, None] * (1 - pshade[..., None] * 0.7) + gold_dk[None, None] * (pshade[..., None] * 0.7)
parr = parr * (0.95 + 0.1 * sfield[..., None])
paste_rgb(parr, pmask)
ak.stipple(c, mask_from(pm_arr * (0.3 + 0.6 * pshade)), density=2.0, r=(0.35, 0.8),
           color=ak.mix(GOLD_DK, WALNUT, 0.35), seed=SEED + 13)
ak.chips(c, 8, (CX - 110, 905, CX + 110, 950), size=(1.2, 2.2), colors=(ICE,),
         seed=SEED + 14, mask_img=pmask)

# ================================================================ 8. VILLAGE MARKERS
for x, y, lit in vpts:
    if not GLASS[int(y * SS), int(x * SS)]:
        continue
    if lit:
        ak.glow(c, x, y, 9, GOLD, alpha=70)
        ak.circle(c, x, y, 3.4, fill=GOLD)
        ak.circle(c, x, y, 1.3, fill=CREAM)
    else:
        ak.circle(c, x, y, 3.0, fill=ak.mix(WALL_DK, WALL, 0.5), outline=ak.mix(CREAM, WALL, 0.25), width=1.0)
# technology rides inside some lit markers
for x, y, lit in vpts[::5]:
    if lit and GLASS[int(y * SS), int(x * SS)]:
        ak.circle(c, x, y, 1.2, fill=ICE)

# ================================================================ 9. STREAM + NECK
ak.glow(c, CX, NECK_Y, 70, GOLD, alpha=55)
ak.glow(c, CX, NECK_Y, 26, GOLD_LT, alpha=120)
ak.line(c, [(CX, NECK_Y - 10), (CX, 903)], GOLD, 2.6)
ak.line(c, [(CX - 0.6, NECK_Y - 10), (CX - 0.6, 903)], GOLD_LT, 0.9)
for i in range(26):
    yy = rng.uniform(NECK_Y + 10, 895)
    xx = CX + rng.normal(0, 1.6 + (yy - NECK_Y) / 180)
    ak.circle(c, xx, yy, rng.uniform(0.5, 1.1), fill=GOLD_LT)
# splash crown at the pile apex
for i in range(14):
    a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
    rr = rng.uniform(4, 13)
    ak.circle(c, CX + math.cos(a) * rr, 902 + math.sin(a) * rr * 0.5, rng.uniform(0.5, 1.0), fill=GOLD_LT)

# ================================================================ 10. GLASS RIM + HIGHLIGHTS
left = glass_outline(-1, TOP_Y1, BOT_Y0, 400)
right = glass_outline(1, TOP_Y1, BOT_Y0, 400)
ak.line(c, left, ak.mix(CREAM, WALL, 0.25), 1.8)
ak.line(c, right, ak.mix(CREAM, WALL, 0.62), 1.4)
# inner rim (thickness of glass)
ak.line(c, [(x + 4.5, y) for x, y in left if abs(y - NECK_Y) > 18], ak.mix(CREAM, WALL, 0.7), 0.8)
# long highlight streaks on the lit left shoulder of each bulb
hl, hd = c.layer()
for (ya, yb) in [(150, 470), (610, 930)]:
    ys = np.linspace(ya, yb, 120)
    pts = [(CX - bulb_w(y) * 0.78, y) for y in ys]
    hd.line(c.pts(pts), fill=(*cr, 150), width=int(c.s(3.2)), joint="curve")
    pts2 = [(CX - bulb_w(y) * 0.64, y) for y in ys[20:80]]
    hd.line(c.pts(pts2), fill=(*cr, 70), width=int(c.s(1.4)), joint="curve")
hl = hl.filter(ImageFilter.GaussianBlur(c.s(1.1)))
c.composite(hl)
# specular dots
for (x, y, r) in [(CX - 124, 232, 2.4)]:
    ak.glow(c, x, y, 8, CREAM, alpha=110)
    ak.circle(c, x, y, r * 0.5, fill=CREAM)

# ================================================================ 11. FRONT POSTS
for px in POSTS:
    pts = post_pts(px)
    ak.poly(c, pts, fill=WALNUT)
    pmk, pmd = c.mask()
    pmd.polygon(c.pts(pts), fill=255)
    pa = np.asarray(pmk, np.float32) / 255
    rr = post_r(gy)
    rel = (gx - px) / np.maximum(rr, 1)
    # light from the upper left: highlight band on the left third, shadow right
    hi = np.clip(1 - np.abs(rel + 0.45) / 0.3, 0, 1) * pa
    lo = np.clip((rel - 0.1) / 0.9, 0, 1) * pa
    fill_mask(WALNUT_LT, mask_from(hi * 0.85))
    fill_mask(WALNUT_DK, mask_from(lo * 0.8))
    ak.hatch(c, mask_from((rel > 0.45) * pa), spacing=3.2, angle=80, color=ak.mix(WALNUT_DK, WALL_DK, 0.5), width=0.6)
    # bead ring lines
    for yc in (142, 162, 522, 540, 558, 918, 938):
        r0 = float(post_r(yc))
        ak.line(c, [(px - r0 + 1, yc), (px + r0 - 1, yc)], ak.mix(WALNUT_DK, WALL_DK, 0.3), 0.8)
    ak.line(c, [(px - float(post_r(300)) + 3.5, 180), (px - float(post_r(300)) + 3.5, 500)], ak.mix(WALNUT_LT, CREAM, 0.4), 0.9)
    ak.line(c, [(px - float(post_r(700)) + 3.5, 580), (px - float(post_r(700)) + 3.5, 900)], ak.mix(WALNUT_LT, CREAM, 0.4), 0.9)

# ================================================================ 12. PLATES


def plate(y0, y1, seed):
    ak.poly(c, [(PLATE_X0, y0 + 4), (PLATE_X0 + 4, y0), (PLATE_X1 - 4, y0), (PLATE_X1, y0 + 4),
                (PLATE_X1, y1 - 4), (PLATE_X1 - 4, y1), (PLATE_X0 + 4, y1), (PLATE_X0, y1 - 4)],
            fill=WALNUT)
    # bevel light on top edge, shadow underneath
    ak.line(c, [(PLATE_X0 + 4, y0 + 1.2), (PLATE_X1 - 4, y0 + 1.2)], WALNUT_LT, 2.0)
    ak.line(c, [(PLATE_X0 + 4, y1 - 1.2), (PLATE_X1 - 4, y1 - 1.2)], WALNUT_DK, 2.2)
    # darker right end (light from the left)
    g, gd = c.layer()
    for i in range(80):
        tt = i / 80
        x = PLATE_X1 - 160 + tt * 160
        gd.line([(c.s(x), c.s(y0 + 3)), (c.s(x), c.s(y1 - 3))],
                fill=(*ak.hex_to_rgb(WALNUT_DK), int(150 * tt)), width=int(c.s(2.2)))
    c.composite(g)
    # wood grain
    r2 = np.random.default_rng(seed)
    for k in range(7):
        yy = y0 + 6 + k * (y1 - y0 - 12) / 6
        ph, fr = r2.uniform(0, 6), r2.uniform(40, 90)
        pts = [(x, yy + 1.4 * math.sin(x / fr + ph) + 0.8 * math.sin(x / 13 + ph * 2))
               for x in np.arange(PLATE_X0 + 8, PLATE_X1 - 8, 6)]
        ak.hand_line(c, pts, ak.mix(WALNUT, WALNUT_DK, 0.7), 0.7, amp=0.4, seed=seed + k)
    # a knot
    kx = r2.uniform(PLATE_X0 + 80, PLATE_X1 - 200)
    for j in range(3):
        ak.circle(c, kx, (y0 + y1) / 2, 3 + j * 3, outline=ak.mix(WALNUT, WALNUT_DK, 0.8), width=0.7)


plate(TOP_Y0, TOP_Y1, SEED + 20)
plate(BOT_Y0, BOT_Y1, SEED + 30)
# glass collars where the bulbs meet the plates
for y in (TOP_Y1, BOT_Y0):
    w0 = float(bulb_w(y + (4 if y == TOP_Y1 else -4)))
    ak.poly(c, [(CX - w0 - 6, y - 3), (CX + w0 + 6, y - 3), (CX + w0 + 6, y + 3), (CX - w0 - 6, y + 3)],
            fill=ak.mix(GOLD_DK, WALNUT, 0.35))
    ak.line(c, [(CX - w0 - 6, y - 3), (CX + w0 + 6, y - 3)], GOLD_LT, 0.8)

# ================================================================ 13. TYPE
X0 = 72
kick = ak.mono(c, 16, medium=True)
ak.text(c, (X0, 88), "THE STACK · VEHICLES · 28 SEP 2026", kick, ak.mix(CREAM, GOLD, 0.25), tracking=0.2)
ak.line(c, [(X0, 120), (X0 + 60, 120)], GOLD, 1.6)

big = ak.fraunces(c, 162, weight=900, opsz=144, soft=30)
ak.text(c, (X0 - 6, 148), "$272M", big, GOLD, tracking=-0.02)
f2 = ak.fraunces(c, 74, weight=640, opsz=144, soft=40)
ak.text(c, (X0, 318), "runs through", f2, CREAM, tracking=-0.01)
f3 = ak.fraunces(c, 74, weight=640, opsz=144, soft=40, italic=True)
ak.text(c, (X0, 398), "one desk.", f3, CREAM, tracking=-0.01)

# leader from the neck into the type column
lab = ak.mono(c, 13, medium=True)
lab_col = ak.mix(CREAM, GOLD, 0.35)
ak.text(c, (X0, 520), "FINAL DECISION-MAKING", lab, lab_col, tracking=0.18)
ak.text(c, (X0, 540), "AUTHORITY", lab, lab_col, tracking=0.18)
lx0 = X0 + ak.measure(c, "AUTHORITY", lab, 0.18) + 14
for x in np.arange(lx0, CX - 16, 7):
    ak.line(c, [(x, 548), (min(x + 3.5, CX - 16), 548)], lab_col, 1.1)
ak.circle(c, CX - 12, 548, 2.4, fill=GOLD)
ak.line(c, [(X0, 506), (X0 + 24, 506)], lab_col, 1.0)

# the pass-through rail between the two labels
for yy in np.arange(572, 760, 5):
    ak.line(c, [(X0 + 1, yy), (X0 + 1, yy + 2)], ak.mix(lab_col, WALL, 0.35), 1.0)
for k_, yy in enumerate(np.arange(580, 760, 30)):
    ak.line(c, [(X0 + 1, yy), (X0 + (12 if k_ % 2 == 0 else 7), yy)], ak.mix(lab_col, WALL, 0.35), 1.0)
fn = ak.mono(c, 11)
ak.text(c, (X0 + 20, 640), "CMS ALLOTMENT", fn, ak.mix(CREAM, WALL, 0.45), tracking=0.18)
ak.text(c, (X0 + 20, 656), "DOH COMMISSIONER", fn, ak.mix(CREAM, WALL, 0.45), tracking=0.18)
ak.text(c, (X0 + 20, 672), "ALASKA COMMUNITY FOUNDATION", fn, ak.mix(CREAM, WALL, 0.45), tracking=0.18)
# second label: where it lands
ak.line(c, [(X0, 770), (X0 + 24, 770)], lab_col, 1.0)
ak.text(c, (X0, 784), "RURAL PROVIDERS", lab, lab_col, tracking=0.18)
ak.text(c, (X0, 804), "YEAR 2 · STATE-DIRECTED", lab, ak.mix(CREAM, WALL, 0.35), tracking=0.18)
lx1 = X0 + ak.measure(c, "RURAL PROVIDERS", lab, 0.18) + 14
tgt = min(vpts, key=lambda v: (v[0] - 690) ** 2 + (v[1] - 800) ** 2 + (0 if v[2] else 1e6))
for x in np.arange(lx1, tgt[0] - 10, 7):
    ak.line(c, [(x, 792), (min(x + 3.5, tgt[0] - 10), 792)], ak.mix(lab_col, WALL, 0.3), 1.0)

sup = ak.mono(c, 13)
ak.text(c, (X0, 930), "RURAL HEALTH TRANSFORMATION PROGRAM", sup, ak.mix(CREAM, WALL, 0.3), tracking=0.16)

# ================================================================ 14. MARKS
ak.polaris(c, 84, 1017, r=12, color=GOLD, core=CREAM)
wm = ak.fraunces(c, 30, weight=900, opsz=144)
ak.text(c, (104, 1030), "ALASKA.AI", wm, CREAM, anchor="ls", tracking=0.02)

# ================================================================ 15. FINISH
ak.grain(c, 6.0, seed=SEED + 50)
ak.vignette(c, strength=0.2, spread=1.4)

meta = {
    "date": "28 SEP 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "VEHICLES",
    "byline": "",
    "headline": "$272M runs through one desk.",
    "writer_headline": "$272M Rural Health Fund / Runs Through One Desk",
    "concept": "An hourglass whose only passage is one pinched neck: federal sand (with a few technology grains) must pass the DOH Commissioner's desk before landing on an etched map of rural Alaska, most villages still waiting.",
    "style_family": "still_life_gouache",
    "palette": PALETTE,
    "hue_family": "red",
    "composition": "column_and_icon",
    "motifs": ["hourglass", "pinched glass neck", "gold sand with ice-blue technology grains",
               "etched Alaska map on the lower bulb", "lit and unlit village points",
               "turned walnut posts", "oxblood wall with raking light"],
    "technique_stack": ["numpy wall light field", "field", "stipple", "mottle", "cast shadow blur",
                        "bulb profile polys", "etched map (lon/lat projection)", "chips", "glow",
                        "hatch", "hand_line", "wobble_pts", "fraunces", "mono", "polaris",
                        "grain", "vignette"],
    "seed": SEED,
}
EVAL = {
 "eval_history": [
  {
   "iter": 1,
   "weighted": 8.4,
   "weakest": "detail",
   "fix": "map too faint to read, sand crater reads as a heart, flat wall acreage in the type column"
  },
  {
   "iter": 2,
   "weighted": 8.72,
   "weakest": "detail",
   "fix": "slip lines into the crater, remove star-like stray glints, pass-through rail with the layer chain in the empty type column"
  },
  {
   "iter": 3,
   "weighted": 8.72,
   "weakest": "craft",
   "fix": "sand surface still has a faint heart silhouette and slip lines vanish; flatten crater, lit rim, stronger slip lines"
  },
  {
   "iter": 4,
   "weighted": 8.77,
   "weakest": "detail",
   "fix": "shipped: remaining gains judged marginal (slip lines subtle at arm's length)"
  }
 ],
 "eval_final": {
  "weighted": 8.77,
  "scores": {
   "concept": 9,
   "focal": 8.5,
   "composition": 8.5,
   "color": 8.5,
   "detail": 8.5,
   "craft": 9,
   "typography": 9,
   "originality": 9,
   "fidelity": 9.5
  }
 }
}
meta.update(EVAL)

if __name__ == "__main__":
    c.finish("out/post_image.png", meta)
    print("rendered out/post_image.png")
