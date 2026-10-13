"""Anchorage Desk — 11 SEP 2026 — cover art.

Concept: the missing handrail. A working stair tower of lit consoles (the
Real-Time Crime Center hub) climbs out of an Eagle River spruce line into a
teal dusk, fed by hairlines of light from far-off cameras on the ridge. Its
handrail exists only as a dashed magenta outline. The hub is built and
busy; the rail is still a drawing.

Style family: wpa_scaffold (WPA layered landscape x blueprint dashed-ghost
grammar). Composition: diagonal_thrust. Hue family: teal.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import art_kit as ak  # noqa: E402

SEED = 9111

# ------------------------------------------------------------ palette
PAPER = "#dfe7e2"
SKY_TOP = "#12303a"
SKY_LOW = "#4f9a97"
INK = "#0d1b1d"
SCREEN = "#f4e3b0"
RAIL = "#e04c8b"
GOLD = "#ffc72c"
PALETTE = [PAPER, SKY_TOP, SKY_LOW, INK, SCREEN, RAIL, GOLD]

RIDGE_FAR = ak.mix(SKY_LOW, INK, 0.45)
RIDGE_NEAR = ak.mix(SKY_LOW, INK, 0.68)
CLOUD = ak.mix(SKY_LOW, SKY_TOP, 0.35)
SNOW_SHADE = ak.mix(PAPER, SKY_LOW, 0.35)
STEEL = ak.mix(INK, SKY_LOW, 0.12)
STEEL_LIT = ak.mix(INK, SCREEN, 0.28)

HEAD1, HEAD2 = "Goecker Funds The Hub", "Before The Rules Land"
KICKER = "ANCHORAGE DESK · MUNICIPAL · 11 SEP 2026"
MOTTO = "decisions, not biographies"

# ------------------------------------------------------------ geometry
HORIZON = 720.0
SPRUCE_Y = 745.0
POST_L, POST_R = 640.0, 880.0
BASE_Y, TOP_Y = 905.0, 355.0
PITCH = 110.0
LANDINGS = [BASE_Y - i * PITCH for i in range(6)]  # 905 .. 355

ak.ensure_fonts()
c = ak.Canvas(bg=PAPER, ss=2)
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------ 1. sky
ak.gradient_v(c, (0, 0, 1080, HORIZON), SKY_TOP, SKY_LOW, ease=1.25)

# stars in the quiet upper sky (micro life; tiny, sparse)
star_lay, std = c.layer()
for k in range(70):
    x, y = rng.uniform(20, 1060), rng.uniform(16, 330)
    r = rng.uniform(0.5, 1.4)
    a = int(rng.uniform(90, 200))
    std.ellipse([c.s(x - r), c.s(y - r), c.s(x + r), c.s(y + r)],
                fill=(*ak.hex_to_rgb(PAPER), a))
c.composite(star_lay)

# ------------------------------------------------------------ 2. clouds
for i, (cy, w, h) in enumerate([(340, 520, 14), (392, 760, 18),
                                 (452, 640, 16), (512, 900, 20)]):
    cx = rng.uniform(260, 820)
    pts = []
    for k in range(80):
        t = k / 80 * math.tau
        pts.append((cx + math.cos(t) * w / 2, cy + math.sin(t) * h / 2))
    pts = ak.wobble_pts(pts, amp=5.0, scale=6.0, seed=SEED + i)
    ak.poly(c, pts, fill=ak.mix(CLOUD, SKY_LOW, 0.15 * i))

# last light at the horizon, right of the tower
ak.glow(c, 930, 600, 300, ak.mix(SCREEN, SKY_LOW, 0.55), alpha=34)

# ------------------------------------------------------------ 3. ridges
far = ak.ridge_fill(c, 605, 115, RIDGE_FAR, scale=2.6, octaves=4,
                    seed=3, bottom=HORIZON + 60)


def snowcap(crest, depth_lo, depth_hi, fill, seed, scale=5.0):
    """A snow band hugging a crest: depth varies with noise so it reads as
    drifted snow on the lee faces, not a stripe. Only draws where the
    crest is high (upper slopes), thinning to nothing in the saddles."""
    n = len(crest)
    f = ak.noise1d(n, scale, 3, seed)
    ys = np.array([y for _, y in crest])
    hi, lo = ys.min(), ys.max()
    top = crest
    bottom = []
    for i, (x, y) in enumerate(crest):
        rel = 1.0 - (y - hi) / max(1.0, (lo - hi))  # 1 at the peaks
        d = (depth_lo + (depth_hi - depth_lo) * f[i]) * (rel ** 1.4)
        bottom.append((x, y + d))
    pts = ak.wobble_pts(list(top) + bottom[::-1], amp=1.0, scale=6, seed=seed)
    ak.poly(c, pts, fill=fill)


crest_far = far[1:-1]
snowcap(crest_far, 10, 34, ak.mix(PAPER, RIDGE_FAR, 0.30), SEED + 11)
# fine snow dusting below the caps (tiny, sparse, tapering)
m, md = c.mask()
md.polygon(c.pts([(x, y + 6) for x, y in crest_far] +
                 [(x, y + 60) for x, y in crest_far[::-1]]), fill=110)
ak.stipple(c, m, density=0.08, r=(0.35, 0.8),
           color=ak.mix(PAPER, RIDGE_FAR, 0.45), seed=SEED + 12)
# shadow faces: translucent wedges from crest to base give the far ridge
# its planes (meso structure) without scratchy line work
face_lay, fcd = c.layer()
for k in range(14):
    i = int(rng.uniform(8, len(crest_far) - 8))
    x, y = crest_far[i]
    w = rng.uniform(30, 110)
    fcd.polygon(c.pts([(x, y + 2), (x + w, HORIZON + 40), (x - w * 0.25, HORIZON + 40)]),
                fill=(*ak.hex_to_rgb(SKY_TOP), int(rng.uniform(28, 52))))
c.composite(face_lay)

near = ak.ridge_fill(c, 665, 70, RIDGE_NEAR, scale=3.4, octaves=4,
                     seed=9, bottom=HORIZON + 60)
snowcap(near[1:-1], 5, 14, ak.mix(PAPER, RIDGE_NEAR, 0.55), SEED + 13, scale=7.0)

# ------------------------------------------------------------ 4. cameras + feeds
cam_pts = []
for k in range(26):
    x = rng.uniform(36, 585)
    # sit the point on or just below the near ridge line
    ridge_y = next(y for (rx, y) in near[1:-1] if rx >= x)
    y = ridge_y + rng.uniform(4, 40)
    cam_pts.append((x, y, "L"))
for k in range(7):
    x = rng.uniform(925, 1050)
    ridge_y = next(y for (rx, y) in near[1:-1] if rx >= x)
    cam_pts.append((x, ridge_y + rng.uniform(6, 36), "R"))
feed_lay, fd = c.layer()
for k, (x, y, side) in enumerate(cam_pts):
    ly = LANDINGS[(k % 5) + 1] - 24
    tx = POST_L + 6 if side == "L" else POST_R - 6
    fd.line(c.pts([(x, y), (tx, ly)]), fill=(*ak.hex_to_rgb(SCREEN), 46),
            width=max(1, int(c.s(1.0))))
c.composite(feed_lay)
cam_pts = [(x, y) for x, y, _ in cam_pts]
for (x, y) in cam_pts:
    ak.glow(c, x, y, 9, SCREEN, alpha=90)
    ak.circle(c, x, y, 1.8, fill=SCREEN)

# ------------------------------------------------------------ 5. spruce band
def spruce(x, base, h, seed):
    w = h * rng.uniform(0.28, 0.40)
    pts = [(x, base - h)]
    tiers = 5
    for t in range(1, tiers + 1):
        f = t / tiers
        yy = base - h + h * f
        ww = w * f
        pts.append((x + ww * rng.uniform(0.75, 1.0), yy))
    pts.append((x + w * 0.16, base + 4))
    pts.append((x - w * 0.16, base + 4))
    for t in range(tiers, 0, -1):
        f = t / tiers
        yy = base - h + h * f
        ww = w * f
        pts.append((x - ww * rng.uniform(0.75, 1.0), yy))
    return ak.wobble_pts(pts, amp=1.2, scale=4, seed=seed)

# back row: lighter, shorter, sits a little higher (atmospheric depth)
BACK = ak.mix(INK, RIDGE_NEAR, 0.55)
xs_back = sorted(rng.uniform(-20, 1100, 95))
for i, x in enumerate(xs_back):
    if 600 < x < 930 and rng.random() > 0.35:
        continue
    h = rng.uniform(30, 80)
    ak.poly(c, spruce(x, SPRUCE_Y - 14 + rng.uniform(-5, 5), h, SEED + 200 + i),
            fill=BACK)
# front row
xs = sorted(rng.uniform(-20, 1100, 74))
for i, x in enumerate(xs):
    if 600 < x < 930:
        dens, hs = 0.28, 0.6
    elif x < 560:
        dens, hs = 1.0, 1.0
    else:
        dens, hs = 0.6, 0.85
    if rng.random() > dens:
        continue
    h = rng.uniform(45, 130) * hs
    tone = INK if rng.random() < 0.7 else ak.mix(INK, SKY_TOP, 0.35)
    ak.poly(c, spruce(x, SPRUCE_Y + rng.uniform(-8, 8), h, SEED + i), fill=tone)
# birds, tiny, mid-left sky (well below the headline block)
for k in range(6):
    bx, by = rng.uniform(150, 430), rng.uniform(335, 385)
    s = rng.uniform(4, 7)
    ak.line(c, [(bx - s, by), (bx, by - s * 0.45), (bx + s, by)],
            ak.mix(PAPER, SKY_LOW, 0.3), width=1.1)
# tree-line shadow on the snow: a soft translucent band, not a stripe
tl_lay, tld = c.layer()
for i in range(36):
    a = int(70 * (1 - i / 36) ** 1.5)
    y = SPRUCE_Y + 2 + i
    tld.rectangle([0, c.s(y), c.W, c.s(y + 1)],
                  fill=(*ak.hex_to_rgb(SKY_TOP), a))
c.composite(tl_lay)

# ------------------------------------------------------------ 6. snowfield
# blue-shadow drifts: low wobbled lenses give the field meso structure
for k in range(9):
    cx, cy = rng.uniform(60, 1020), rng.uniform(790, 1050)
    w, h = rng.uniform(160, 420), rng.uniform(9, 20)
    pts = [(cx + math.cos(t) * w / 2, cy + math.sin(t) * h / 2)
           for t in np.linspace(0, math.tau, 90, endpoint=False)]
    pts = ak.wobble_pts(pts, amp=3.0, scale=5.0, seed=SEED + 60 + k)
    ak.poly(c, pts, fill=ak.mix(PAPER, SKY_LOW, 0.13))
    # lit crest on the windward edge
    top = [p for p in pts if p[1] < cy]
    top = sorted(top)
    if len(top) > 4:
        ak.hand_line(c, top, ak.mix(PAPER, "#ffffff", 0.6), width=1.2,
                     amp=0.8, seed=SEED + 70 + k)

# stipple shading that fades with distance from the tree line
arr = np.zeros((c.W, c.W), np.uint8)
y0 = int(c.s(SPRUCE_Y + 18))
ys = np.arange(c.W)
rampv = np.clip(1.0 - (ys - y0) / (c.W - y0), 0, 1) ** 1.8
arr[y0:, :] = (255 * rampv[y0:])[:, None].astype(np.uint8)
snow_mask = Image.fromarray(arr, "L")
ak.stipple(c, snow_mask, density=0.11, r=(0.35, 0.95), color=SNOW_SHADE,
           seed=SEED + 21)
# sastrugi (wind-carved snow) as faint hand lines
for k in range(11):
    y0 = SPRUCE_Y + 50 + k * 28 + rng.uniform(-6, 6)
    x0 = rng.uniform(-40, 420)
    x1 = x0 + rng.uniform(260, 640)
    ak.hand_line(c, [(x0, y0), (x1, y0 + rng.uniform(-10, 10))],
                 ak.mix(SNOW_SHADE, PAPER, 0.2), width=1.3, amp=2.4,
                 seed=SEED + 30 + k)

# tower shadow on the snow (long dusk shadow to the lower-left)
sh_lay, shd = c.layer()
shd.polygon(c.pts([(POST_L + 10, BASE_Y + 6), (POST_R - 10, BASE_Y + 6),
                   (420, 1040), (150, 1040)]),
            fill=(*ak.hex_to_rgb(SKY_TOP), 34))
c.composite(sh_lay)

# ------------------------------------------------------------ 7. steel frame
def steel_line(pts, w=3.2, col=STEEL):
    ak.line(c, pts, col, width=w)

# footings
for px in (POST_L, POST_R):
    ak.poly(c, [(px - 16, BASE_Y + 2), (px + 16, BASE_Y + 2),
                (px + 12, BASE_Y + 12), (px - 12, BASE_Y + 12)], fill=INK)
# posts, with a lit rim on the sun side so they never sink into the spruce
steel_line([(POST_L, BASE_Y), (POST_L, TOP_Y - 30)], w=4.2)
steel_line([(POST_R, BASE_Y), (POST_R, TOP_Y - 30)], w=4.2)
steel_line([(POST_L + 3, BASE_Y), (POST_L + 3, TOP_Y - 30)], w=1.2,
           col=ak.mix(INK, SCREEN, 0.42))
steel_line([(POST_R + 3, BASE_Y), (POST_R + 3, TOP_Y - 30)], w=1.2,
           col=ak.mix(INK, SCREEN, 0.42))
# landings, bracing, flights
flights = []
for i, ly in enumerate(LANDINGS):
    steel_line([(POST_L - 8, ly), (POST_R + 8, ly)], w=3.4)
    # a thin line of snow lying on every landing beam
    ak.hand_line(c, [(POST_L - 6, ly - 2.4), (POST_R + 6, ly - 2.4)],
                 ak.mix(PAPER, SKY_LOW, 0.15), width=1.5, amp=0.5,
                 seed=SEED + 300 + i)
    if i < len(LANDINGS) - 1:
        ny = LANDINGS[i + 1]
        # cross-bracing in the bay
        steel_line([(POST_L, ly), (POST_R, ny)], w=1.4,
                   col=ak.mix(STEEL, SKY_LOW, 0.25))
        steel_line([(POST_R, ly), (POST_L, ny)], w=1.4,
                   col=ak.mix(STEEL, SKY_LOW, 0.25))
        # stair flight zigzag
        if i % 2 == 0:
            a, b = (POST_L + 18, ly), (POST_R - 18, ny)
        else:
            a, b = (POST_R - 18, ly), (POST_L + 18, ny)
        flights.append((a, b))
        steel_line([a, b], w=3.6)
        # treads
        n = 9
        for k in range(1, n):
            t = k / n
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t
            steel_line([(x - 7, y), (x + 7, y)], w=2.2, col=STEEL_LIT)
# roof on the top deck
steel_line([(POST_L - 26, TOP_Y - 30), (POST_R + 26, TOP_Y - 30)], w=4.0)
ak.poly(c, [(POST_L - 26, TOP_Y - 30), (POST_R + 26, TOP_Y - 30),
            (POST_R + 26, TOP_Y - 38), (POST_L - 26, TOP_Y - 38)], fill=INK)
# rivets on posts
for px in (POST_L, POST_R):
    for y in np.arange(TOP_Y - 20, BASE_Y, 22):
        ak.circle(c, px, y, 1.3, fill=STEEL_LIT)

# ------------------------------------------------------------ 8. consoles + screens
def console(x0, y, n=3, glow_r=44):
    w = 16
    gap = 8
    total = n * w + (n - 1) * gap
    ak.glow(c, x0 + total / 2, y - 8, glow_r, SCREEN, alpha=70)
    # console bar
    ak.poly(c, [(x0 - 6, y - 2), (x0 + total + 6, y - 2),
                (x0 + total + 6, y + 4), (x0 - 6, y + 4)], fill=INK)
    for k in range(n):
        x = x0 + k * (w + gap)
        ak.poly(c, [(x, y - 14), (x + w, y - 14), (x + w, y - 3), (x, y - 3)],
                fill=SCREEN)
        # a darker scan band on each screen so it reads as a display
        ak.poly(c, [(x + 2, y - 9), (x + w - 2, y - 9),
                    (x + w - 2, y - 7), (x + 2, y - 7)],
                fill=ak.mix(SCREEN, SKY_LOW, 0.55))

for i, ly in enumerate(LANDINGS[1:], start=1):
    if i % 2 == 1:
        console(POST_L + 26, ly - 2)
    else:
        console(POST_R - 26 - 64, ly - 2)
# top deck: bigger bank and the seated figure
console(POST_L + 20, TOP_Y - 2, n=4, glow_r=58)
fx, fy = POST_R - 28, TOP_Y - 4
ak.circle(c, fx, fy - 30, 6, fill=INK)
ak.poly(c, [(fx - 8, fy - 22), (fx + 8, fy - 22), (fx + 10, fy - 2),
            (fx - 10, fy - 2)], fill=INK)

# ------------------------------------------------------------ 9. the dashed rail (the absence)
def dashed(a, b, dash=14.0, gap=10.0, w=4.0, col=RAIL):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    s = 0.0
    while s < L:
        e = min(L, s + dash)
        ak.line(c, [(a[0] + ux * s, a[1] + uy * s),
                    (a[0] + ux * e, a[1] + uy * e)], col, width=w)
        s += dash + gap

rail_lay, rd = c.layer()
for a, b in flights:
    # soft glow under the rail so it reads at thumbnail
    rd.line(c.pts([(a[0], a[1] - 30), (b[0], b[1] - 30)]),
            fill=(*ak.hex_to_rgb(RAIL), 26), width=int(c.s(16)))
rd.line(c.pts([(POST_L - 26, TOP_Y - 34 - 0), (POST_R + 26, TOP_Y - 34)]),
        fill=(*ak.hex_to_rgb(RAIL), 0), width=1)
c.composite(rail_lay)
for a, b in flights:
    ra, rb = (a[0], a[1] - 30), (b[0], b[1] - 30)
    dashed(ra, rb, w=4.6)
    # end posts of the rail at both landings
    dashed(ra, (ra[0], ra[1] + 30), dash=6, gap=5, w=2.8)
    dashed(rb, (rb[0], rb[1] + 30), dash=6, gap=5, w=2.8)
    # dashed posts every 44 px
    dx, dy = rb[0] - ra[0], rb[1] - ra[1]
    L = math.hypot(dx, dy)
    n = int(L / 44)
    for k in range(1, n):
        t = k / n
        x = ra[0] + dx * t
        y = ra[1] + dy * t
        dashed((x, y), (x, y + 30), dash=6, gap=5, w=2.6)
# top-deck rail (dashed) along the front edge
dashed((POST_L - 20, TOP_Y - 34), (POST_L + 20 + 88, TOP_Y - 34),
       dash=12, gap=8, w=3.4)

# ------------------------------------------------------------ 10. base debris
ak.chips(c, 90, (560, BASE_Y - 4, 960, BASE_Y + 40), size=(2, 6),
         colors=(SNOW_SHADE, ak.mix(INK, PAPER, 0.5)), seed=SEED + 41)
# plowed access road curving in from the lower-left to the tower base:
# the leading line into the focal, and the one human-scale cue
def road_pt(t):
    # quadratic bezier from (−30, 1010) via (330, 1030) to (POST_L − 6, BASE_Y + 14)
    p0, p1, p2 = (-30.0, 1062.0), (340.0, 1064.0), (POST_L - 6, BASE_Y + 14)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y

ts = np.linspace(0, 1, 60)
road = [road_pt(t) for t in ts]
# road bed: slightly darker packed snow, width tapering with distance
bed_lay, bd = c.layer()
left, right = [], []
for i, t in enumerate(ts):
    x, y = road[i]
    hw = 30 * (1 - t) + 12 * t
    left.append((x, y - hw))
    right.append((x, y + hw))
bd.polygon(c.pts(left + right[::-1]),
           fill=(*ak.hex_to_rgb(ak.mix(PAPER, SKY_LOW, 0.22)), 200))
c.composite(bed_lay)
# berms: lit crest lines along both edges
ak.hand_line(c, left, ak.mix(PAPER, "#ffffff", 0.7), width=1.4, amp=1.2,
             seed=SEED + 81)
ak.hand_line(c, right, ak.mix(PAPER, SKY_LOW, 0.4), width=1.6, amp=1.2,
             seed=SEED + 82)
# tire tracks: two parallel dashed hand lines down the bed
for off in (-9, 9):
    trk = [(x, y + off * (1 - 0.5 * t)) for (x, y), t in zip(road, ts)]
    for j in range(0, len(trk) - 3, 3):
        ak.hand_line(c, trk[j:j + 3], ak.mix(PAPER, SKY_LOW, 0.58), width=2.0,
                     amp=0.7, seed=SEED + 90 + j)
# a walker on the road, heading for the tower, with a long dusk shadow
wx, wy = road_pt(0.60)
sh_lay2, shd2 = c.layer()
shd2.polygon(c.pts([(wx - 3, wy), (wx + 3, wy), (wx - 62, wy + 26), (wx - 74, wy + 22)]),
             fill=(*ak.hex_to_rgb(SKY_TOP), 60))
c.composite(sh_lay2)
ak.circle(c, wx, wy - 22, 3.2, fill=INK)
ak.poly(c, [(wx - 4, wy - 18), (wx + 4, wy - 18), (wx + 3, wy - 6), (wx - 3, wy - 6)],
        fill=INK)
ak.line(c, [(wx - 2, wy - 6), (wx - 4, wy)], INK, width=1.6)
ak.line(c, [(wx + 2, wy - 6), (wx + 5, wy - 1)], INK, width=1.6)

# ------------------------------------------------------------ 11. type + marks
size = min(ak.fit_size(c, HEAD1, 620, hi=104, weight=900, opsz=144),
           ak.fit_size(c, HEAD2, 620, hi=104, weight=900, opsz=144))
fh = ak.fraunces(c, size, weight=900, opsz=144)
ak.text(c, (84, 84), HEAD1, fh, PAPER, anchor="la")
ak.text(c, (84, 84 + size * 1.06), HEAD2, fh, ak.mix(PAPER, SKY_LOW, 0.35),
        anchor="la")
kick = ak.mono(c, 16)
ky = 84 + size * 2.26
ak.line(c, [(86, ky - 14), (600, ky - 14)], ak.mix(PAPER, SKY_TOP, 0.55),
        width=1)
ak.text(c, (86, ky), KICKER, kick, ak.mix(PAPER, SKY_TOP, 0.22),
        anchor="la", tracking=0.22)
ital = ak.fraunces(c, 21, weight=500, italic=True)
ak.text(c, (86, ky + 30), MOTTO, ital, ak.mix(PAPER, SKY_LOW, 0.45),
        anchor="la")

wm = ak.fraunces(c, 32, weight=900, opsz=144)
ak.text(c, (84, 1000), "ALASKA.AI", wm, INK, anchor="la", tracking=0.06)
ak.polaris(c, 992, 80, r=13, color=GOLD)

# ------------------------------------------------------------ 12. finishing
ak.mottle(c, strength=0.035, scale=3.0, seed=SEED + 7)
ak.grain(c, amount=5.5, seed=SEED + 8)
ak.vignette(c, strength=0.12, spread=1.42)

c.finish("out/post_image.png", {
    "date": "11 SEP 2026",
    "column": "Anchorage Desk",
    "kicker": "ANCHORAGE DESK",
    "middle_slot": "MUNICIPAL",
    "byline": "",
    "headline": HEAD1 + " / " + HEAD2,
    "style_family": "wpa_scaffold",
    "palette": PALETTE,
    "hue_family": "teal",
    "composition": "diagonal_thrust",
    "motifs": ["stair tower of lit consoles", "dashed uninstalled handrail",
               "hairline camera feeds from the ridge", "Eagle River spruce line",
               "teal dusk", "long tower shadow on snow"],
    "technique_stack": ["gradient_v", "wobble_pts", "ridge_fill", "stipple",
                        "line", "hand_line", "glow", "circle", "chips",
                        "fraunces", "mono", "mottle", "grain", "vignette"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 7.1, "weakest": "detail/craft",
         "note": "ridge and snowfield stipple read as confetti noise; "
                 "tree-line shadow was a hard stripe; rail read as wiring"},
        {"iter": 2, "weighted": 7.9, "weakest": "craft",
         "note": "snow caps and drifts fixed the noise; couloir lines read "
                 "as stray scratches; spruce band flat; posts sank into trees"},
        {"iter": 3, "weighted": 8.3, "weakest": "composition/detail",
         "note": "ridge shadow faces, two spruce rows, lit post rims; "
                 "snowfield still lacked a leading line and human scale"},
        {"iter": 4, "weighted": 8.2, "weakest": "craft",
         "note": "access road and walker added, but the walker landed on "
                 "the wordmark"},
        {"iter": 5, "weighted": 8.48, "weakest": "craft",
         "note": "road rerouted along the bottom edge, walker clear of the "
                 "wordmark, snow on landing beams; tire tracks invisible"},
        {"iter": 6, "weighted": 8.6, "weakest": "originality",
         "note": "tracks deepened so the road carries texture to the focal"}
    ],
    "eval_final": {"weighted": 8.6, "scores": {"concept": 9, "focal": 9,
                   "composition": 8.5, "color": 8.5, "detail": 8.5,
                   "craft": 8.5, "typography": 8.5, "originality": 8,
                   "fidelity": 9}},
})
print("rendered out/post_image.png")
