"""Anchorage Desk, 24 SEP 2026 — trail markers behind the trail.
Ben Shier / UA draft system-wide AI policy. See out/art_plan.md."""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as K

SEED = 924
rng = np.random.default_rng(SEED)

PAPER = "#efe8d8"
INK = "#1f2a4d"
SHADE = "#6f7fa6"
MIST = "#b9c2d6"
ACCENT = "#d0452f"
STAR = "#e0a526"
SNOW2 = "#e2ddd4"  # faint cool snow tint
SNOW3 = "#c9ccd6"  # trough / cups
SHD2 = "#9aa5c0"   # shadow fill
FAR = "#dcdcdf"    # far ridge fill

c = K.Canvas(bg=PAPER)
W = c.W


def fast_field(scale=4.0, octaves=4, seed=0, persistence=0.5):
    """Fast value noise (numpy + scipy zoom); simplex field() is ~54s here."""
    from scipy.ndimage import zoom
    r = np.random.default_rng(seed)
    out = np.zeros((1080, 1080))
    amp, tot, freq = 1.0, 0.0, scale
    for _ in range(octaves):
        n = max(2, int(freq)) + 2
        g = r.random((n, n))
        z = zoom(g, 1080 / (n - 1), order=3)[:1080, :1080]
        out += amp * z
        tot += amp
        amp *= persistence
        freq *= 2
    out /= tot
    out = (out - out.min()) / (out.max() - out.min() + 1e-9)
    return out


def peaks(base, spec, seed, jag=6.0, step=6):
    """Polyline of mountain peaks: spec = [(x_center, height, half_width)]."""
    r = np.random.default_rng(seed)
    xs = np.arange(-10, 1091, step)
    ys = np.full(xs.shape, float(base))
    for cx, hgt, hw in spec:
        skew = r.uniform(0.65, 1.45)
        d = np.where(xs < cx, (cx - xs) / (hw * skew), (xs - cx) / (hw / skew))
        prof = np.clip(1 - d, 0, None) ** r.uniform(1.05, 1.6)
        ys = np.minimum(ys, base - hgt * prof)
    ys += np.cumsum(r.normal(0, jag * 0.35, xs.shape)) * 0.5 + r.normal(0, jag * 0.5, xs.shape) * (base - ys > 20)
    ys -= np.linspace(0, ys[-1] - ys[0] - (ys[-1] - ys[0]), xs.shape[0]) * 0
    ys = np.convolve(ys, np.ones(2) / 2, mode="same")
    ys[0], ys[-1] = ys[1], ys[-2]
    return list(zip(xs.tolist(), ys.tolist()))


def mask_poly(pts):
    m, md = c.mask()
    md.polygon(c.pts(pts), fill=255)
    return m


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


# ---- sky: engraved horizontal lines fading toward the ridge ----------
sky = np.zeros((1080, 1080), np.uint8)
for y in range(335, 560):
    sky[y, :] = int(255 * min(1.0, (y - 335) / 170) ** 1.3)
K.hatch(c, Image.fromarray(sky), spacing=7.5, angle=0, color=MIST, width=1.0)

# ---- far ridge (mist) --------------------------------------------------
far = peaks(470, [(90, 70, 150), (300, 120, 170), (520, 95, 150), (760, 140, 190), (990, 90, 170)], SEED + 1, jag=4)
far_poly = far + [(1090, 600), (-10, 600)]
fm = mask_poly(far_poly)
K.poly(c, far_poly, fill=FAR)
K.hatch(c, fm, spacing=5.5, angle=40, color=MIST, width=1.0)
K.line(c, far, SHADE, width=1.6)

# snowcaps on the far range: paper wedges under the highest crests
far_arr = np.array(far)
capr = np.random.default_rng(SEED + 5)
for k in range(1, len(far_arr) - 1):
    pass
top_idx = [k for k in range(2, len(far_arr) - 2) if far_arr[k, 1] < 470 - 70
           and far_arr[k, 1] <= far_arr[k - 2:k + 3, 1].min() + 0.01]
for k in top_idx:
    px, py = far_arr[k]
    dep = 28 + capr.uniform(0, 22)
    cap = [(far_arr[j, 0], far_arr[j, 1]) for j in range(max(0, k - 9), min(len(far_arr), k + 10))]
    zig = []
    for j, (qx, qy) in enumerate(reversed(cap)):
        zig.append((qx, max(qy, py + dep * (0.55 + 0.45 * (j % 2)))))
    capp = cap + zig
    capm = mask_poly(capp)
    carr = np.asarray(capm, float) * (np.asarray(fm, float) / 255.0)
    K.poly(c, capp, fill=PAPER)
    K.hatch(c, Image.fromarray(carr.astype(np.uint8)), spacing=11, angle=40, color=MIST, width=0.8)
K.line(c, far, SHADE, width=1.6)

# ---- near ridge (ink hatch, snow faces left open) ----------------------
near = peaks(560, [(180, 110, 230), (470, 70, 200), (660, 125, 210), (930, 85, 220)], SEED + 2, jag=5)
near_poly = near + [(1090, 640), (-10, 640)]
nm = mask_poly(near_poly)
K.poly(c, near_poly, fill=PAPER)
rock = fast_field(scale=6.0, octaves=4, seed=SEED + 3)
rockm = K.field_mask(rock, threshold=0.52, soft=0.04)
rock_arr = np.asarray(rockm.resize((W, W)), float) / 255.0
near_arr = np.asarray(nm, float) / 255.0
fade = np.clip((620 * 2 - np.arange(W)[:, None]) / (2 * 110.0), 0, 1)
near_arr = near_arr * fade
rm = Image.fromarray((rock_arr * near_arr * 255).astype(np.uint8))
K.hatch(c, rm, spacing=4.2, angle=-35, color=INK, width=1.2)
lower = Image.fromarray((near_arr * (1 - rock_arr) * 150).astype(np.uint8))
K.hatch(c, lower, spacing=9, angle=-35, color=SHADE, width=0.9)
narr = np.array(near)
ys_s = np.convolve(narr[:, 1], np.ones(9) / 9, mode="same")
slm, sld = c.mask()
for k in range(4, len(narr) - 5):
    (x0, y0), (x1, y1) = narr[k], narr[k + 1]
    if ys_s[k + 1] > ys_s[k] + 0.3 and y0 < 545:
        d0, d1 = 50 + (545 - y0) * 0.3, 50 + (545 - y1) * 0.3
        sl = [(x0 - 1, y0), (x1 + 1, y1), (x1 + 1, y1 + d1), (x0 - 1, y0 + d0)]
        sld.polygon(c.pts(sl), fill=255)
from PIL import ImageFilter
slm = slm.filter(ImageFilter.GaussianBlur(c.s(6)))
sla = np.asarray(slm, float) * (np.asarray(nm, float) / 255.0)
K.hatch(c, Image.fromarray(sla.astype(np.uint8)), spacing=3.0, angle=-35, color=INK, width=1.0)
K.line(c, near, INK, width=2.2)

# snow apron where ridge meets field

# ---- snowfield: drift contours + stipple hollows -----------------------
for i, y0 in enumerate([640, 740, 870, 1000]):
    amp = 10 + i * 5
    pts = K.ridge_pts(y0, amp * 1.6, scale=2.6 + i * 0.3, octaves=3, seed=SEED + 10 + i)
    seg = []
    for j, q in enumerate(pts):
        if (j // 7 + i) % 2 == 1:
            if len(seg) > 2:
                K.hand_line(c, seg, SHD2, width=0.8 + i * 0.15, amp=1.4, seed=SEED + 20 + i + j)
            seg = []
        else:
            seg.append(q)
    if len(seg) > 2:
        K.hand_line(c, seg, SHD2, width=0.8 + i * 0.15, amp=1.4, seed=SEED + 99 + i)
    band = pts + [(1080, y0 + 40 + i * 8), (0, y0 + 40 + i * 8)]
    bm = mask_poly(band)
    hol = fast_field(scale=5, octaves=3, seed=SEED + 30 + i)
    hm = np.asarray(K.field_mask(hol, 0.55, 0.1).resize((W, W)), float) / 255.0
    bm = Image.fromarray((np.asarray(bm, float) * hm * 0.9).astype(np.uint8))
    K.stipple(c, bm, density=0.10 + i * 0.015, r=(0.5, 1.1 + i * 0.1), color=SHADE, seed=SEED + 40 + i)

# ---- the trail ---------------------------------------------------------
P0, P1, P2, P3 = (150, 1110), (640, 930), (380, 690), (820, 548)


def path(t):
    return bez(P0, P1, P2, P3, t)


def tangent(t):
    a, b = path(max(0, t - 0.002)), path(min(1, t + 0.002))
    d = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    return (b[0] - a[0]) / d, (b[1] - a[1]) / d


def width_at(t):
    return 44 * (1 - t) ** 1.3 + 3


def footprint(x, y, tx, ty, s, color):
    ang = math.atan2(ty, tx)
    pts = []
    for k in range(18):
        a = 2 * math.pi * k / 18
        ex, ey = math.cos(a) * 6.2 * s, math.sin(a) * 3.0 * s
        # heel narrower than toe
        if ex < 0:
            ey *= 0.78
        pts.append((x + ex * math.cos(ang) - ey * math.sin(ang),
                    y + ex * math.sin(ang) + ey * math.cos(ang)))
    K.poly(c, pts, fill=color)



# trough (packed, slightly shaded)
left, right = [], []
for t in np.linspace(0, 1, 160):
    x, y = path(t)
    tx, ty = tangent(t)
    nx, ny = -ty, tx
    w = width_at(t)
    left.append((x + nx * w, y + ny * w))
    right.append((x - nx * w, y - ny * w))
trough = left + right[::-1]
K.poly(c, trough, fill=SNOW2)
tm = mask_poly(trough)
K.hatch(c, tm, spacing=6, angle=-12, color=SNOW3, width=0.8)
K.hand_line(c, left, SHD2, width=1.2, amp=1.0, seed=SEED + 50)
K.hand_line(c, right, SHD2, width=1.2, amp=1.0, seed=SEED + 51)


# a fainter side trail peeling off to the right: use spreading past the markers
B0 = path(0.47)
B1, B2, B3 = (700, 760), (860, 700), (1100, 690)
for side_k in range(2):
    tt = 0.0
    sd = 1
    while tt < 1.0:
        bx, by = bez(B0, B1, B2, B3, tt)
        ax2, ay2 = bez(B0, B1, B2, B3, min(1, tt + 0.01))
        dx, dy = ax2 - bx, ay2 - by
        dd = math.hypot(dx, dy) or 1
        dx, dy = dx / dd, dy / dd
        sc = 0.62 - 0.25 * tt
        ox = (side_k - 0.5) * 9 + sd * 4 * sc
        footprint(bx - dy * ox, by + dx * ox, dx, dy, sc, SHD2)
        sd *= -1
        tt += 0.022

# many walkers: several interleaved tracks inside the trough
for track in range(4):
    off = (track - 1.5) / 1.5 * 0.55
    phase = rng.uniform(0, 0.02)
    t = 0.015 + phase
    side = 1
    while t < 0.995:
        x, y = path(t)
        tx, ty = tangent(t)
        nx, ny = -ty, tx
        w = width_at(t)
        s = 1.25 * (1 - t) ** 1.1 + 0.16
        jx = rng.normal(0, 1.2 * s)
        px = x + nx * (w * off + side * 7 * s) + jx
        py = y + ny * (w * off + side * 7 * s) + jx
        col = INK if t < 0.35 else SHADE
        footprint(px, py, tx, ty, s, col)
        side *= -1
        t += 0.012 * (s ** 0.9) + 0.002

# ---- markers (tripods) with long shadows --------------------------------
MARKERS = [((236, 968), 226), ((372, 806), 140), ((486, 676), 86)]
for (fx, fy), h in MARKERS:
    sp = h * 0.2
    feet = [(fx - sp, fy + h * 0.02), (fx + sp * 0.9, fy + h * 0.05), (fx + sp * 0.15, fy - h * 0.06)]
    apex = (fx + h * 0.02, fy - h)
    top = (apex[0] + h * 0.05, apex[1] - h * 0.12)
    # shadow toward lower right (low sun upper-left)
    shx, shy = h * 1.35, h * 0.30
    sh = [(fx - sp * 0.7, fy), (fx + sp * 0.9, fy + 5), (fx + shx + 10, fy + shy + 6), (fx + shx - 8, fy + shy - 4)]
    K.poly(c, sh, fill=SHD2)
    K.hatch(c, mask_poly(sh), spacing=3.2, angle=-12, color=SHADE, width=0.9)
    # poles
    wpx = max(2.4, h / 40)
    for (ax, ay) in feet:
        tipx = apex[0] + (apex[0] - ax) * 0.13
        tipy = apex[1] + (apex[1] - ay) * 0.13
        K.hand_line(c, [(ax, ay), (tipx, tipy)], INK, width=wpx, amp=0.6, seed=int(ax))
        # snow cup at foot
        K.circle(c, ax, ay + 1, wpx * 1.4, fill=SNOW3)
    # lashing
    for k in range(4):
        yy = apex[1] + h * 0.03 + k * wpx * 0.9
        K.line(c, [(apex[0] - wpx * 1.6, yy), (apex[0] + wpx * 1.6, yy + wpx * 0.5)], PAPER, width=max(1, wpx * 0.35))
    # flagging tape fluttering downwind (right)
    ty0 = apex[1] + h * 0.02
    tape = []
    L = h * 0.42
    for k in range(14):
        u = k / 13
        tape.append((apex[0] + u * L, ty0 + math.sin(u * 5.2 + h) * h * 0.035 + u * h * 0.06))
    back = [(x, y + max(3.2, h * 0.045) * (1 - 0.4 * i / 13)) for i, (x, y) in enumerate(tape)]
    K.poly(c, tape + back[::-1], fill=ACCENT)
    K.line(c, tape, K.darken(ACCENT, 0.12), width=1.0)

# ---- micro: wind-blown snow chips + tiny raven over the ridge ----------
K.chips(c, 90, (0, 560, 1080, 1080), size=(1.5, 4), colors=(SNOW3,), seed=SEED + 60)
rv = [(612, 372), (622, 366), (628, 370), (634, 365), (645, 371)]
K.line(c, rv, INK, width=1.8)

K.grain(c, amount=5, seed=SEED + 70)

# ---- type --------------------------------------------------------------
hf = K.fraunces(c, 80, weight=900, opsz=144)
K.text(c, (70, 150), "UA Drafts Its AI Rules", hf, INK, anchor="ls")
hf2 = K.fraunces(c, 80, weight=900, opsz=144, italic=True)
K.text(c, (70, 242), "UAA Would Write a Plan", hf2, INK, anchor="ls")
K.line(c, [(72, 272), (150, 272)], ACCENT, width=4)
kf = K.mono(c, 17, medium=True)
K.text(c, (72, 306), "ANCHORAGE DESK · RESEARCH · 24 SEP 2026", kf, INK, anchor="ls", tracking=0.2)
K.polaris(c, 992, 94, r=15, color=STAR)
wf = K.fraunces(c, 30, weight=900, opsz=144)
K.chip(c, (1004, 1012), "ALASKA.AI", wf, PAPER, INK, pad=11, anchor="rs", tracking=0.04)

meta = {
    "date": "24 SEP 2026", "column": "Anchorage Desk", "kicker": "ANCHORAGE DESK",
    "middle_slot": "RESEARCH", "volume": "RESEARCH", "byline": "",
    "headline": "UA Drafts Its AI Rules / UAA Would Write a Plan",
    "style_family": "engraving_trail", "palette": [PAPER, INK, SHADE, MIST, ACCENT, STAR],
    "hue_family": "blue", "composition": "diagonal_thrust",
    "motifs": ["trail-marker tripods", "packed footprint trail running past the markers",
               "red flagging tape", "engraved Chugach-style ridge", "long low-sun shadows", "lone raven"],
    "technique_stack": ["hatch", "stipple", "field", "field_mask", "ridge_pts", "hand_line", "chips", "grain"],
    "seed": SEED,
}
if __name__ == "__main__":
    import json, pathlib
    hist = pathlib.Path("out/art_eval.json")
    if hist.exists():
        meta.update(json.loads(hist.read_text()))
    c.finish("out/post_image.png", meta)
    print("rendered")
