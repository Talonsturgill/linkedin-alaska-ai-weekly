"""
The Stack — 17 JUL 2026 — bespoke cover.
Concept: the real gate is off the docket surface. A subsea fiber line
descends from a lit institutional "docket surface" (three visible FCC
layers) into dark Arctic water, where the single lit element is a
submerged sluice gate the line must pass — the executive-branch
(Team Telecom) national-security veto. Style: bathymetric_blueprint
(topo_map + blueprint hybrid). Hue: indigo deep, one warm amber focal.
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import art_kit as ak
from art_kit import (Canvas, oklch, hex_to_rgb, lighten, darken, mix,
                     field, warp, ridge_pts, gradient_v, glow, gradient_r,
                     circle, poly, line, hand_line, wobble_pts, chips,
                     grain, vignette, soft_panel, polaris, fraunces, mono,
                     text, measure, fit_size, chip, DESIGN)

SEED = 419

# ---- palette (OKLCH -> hex; value spine first) ----
paper_deep   = oklch(0.16, 0.055, 262)   # deepest sea / darkest dark
water_mid    = oklch(0.37, 0.075, 258)   # water body
water_bottom = oklch(0.11, 0.050, 264)   # abyss floor tone
surface_top  = oklch(0.74, 0.030, 232)   # docket surface (pale steel)
surface_low  = oklch(0.52, 0.055, 246)   # waterline transition
contour      = oklch(0.80, 0.075, 214)   # bathymetric ink / schematic
cable_core   = oklch(0.87, 0.055, 210)   # fiber core
amber        = oklch(0.76, 0.150, 72)    # focal gate (only hot hue)
hot          = oklch(0.94, 0.090, 88)    # gate hot core
typelight    = oklch(0.95, 0.012, 220)   # headline / wordmark
seabed_ink   = darken(paper_deep, 0.035)

WL = 298  # waterline y


def radial_glow(canvas, cx, cy, r, color, maxalpha=110, gamma=2.0,
                sx=1.0, sy=1.0):
    """Cheap numpy radial light (no GaussianBlur). Anisotropic via sx/sy."""
    ys, xs = np.mgrid[0:DESIGN, 0:DESIGN].astype(np.float32)
    d = np.hypot((xs - cx) / sx, (ys - cy) / sy) / r
    a = (np.clip(1.0 - d, 0, 1) ** gamma * maxalpha).astype(np.uint8)
    rgb = hex_to_rgb(color)
    lay = np.zeros((DESIGN, DESIGN, 4), np.uint8)
    lay[..., 0], lay[..., 1], lay[..., 2] = rgb
    lay[..., 3] = a
    canvas.composite(Image.fromarray(lay, "RGBA").resize(
        (canvas.W, canvas.W), Image.BILINEAR))


c = Canvas(bg=paper_deep, ss=2)

# ---- 1. surface band (docket) + deep water gradient ----
gradient_v(c, (0, 0, DESIGN, WL + 2), surface_top, surface_low, ease=1.15)
gradient_v(c, (0, WL, DESIGN, DESIGN), water_mid, water_bottom, ease=1.35)

# ---- 2. bathymetric contours in the deep ----
def draw_contours(canvas, f, levels, color, alpha, clear_boxes):
    rgb = hex_to_rgb(color)
    acc = Image.new("RGBA", (DESIGN, DESIGN), (0, 0, 0, 0))
    for lv in levels:
        m = (f < lv).astype(np.uint8) * 255
        edge = np.asarray(Image.fromarray(m, "L").filter(ImageFilter.FIND_EDGES))
        lay = np.zeros((DESIGN, DESIGN, 4), np.uint8)
        sel = edge > 40
        lay[sel] = [rgb[0], rgb[1], rgb[2], alpha]
        acc = Image.alpha_composite(acc, Image.fromarray(lay, "RGBA"))
    for (x0, y0, x1, y1) in clear_boxes:
        acc.paste((0, 0, 0, 0), (int(x0), int(y0), int(x1), int(y1)))
    # detail hierarchy: keep contours strongest left-center (the story),
    # calmer toward the right so they never compete with the headline
    arr = np.asarray(acc).astype(np.float32)
    xs = np.arange(DESIGN, dtype=np.float32)[None, :]
    wx = 1.0 - 0.42 * np.clip((xs - 620) / 460.0, 0, 1)
    arr[..., 3] *= wx
    acc = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    canvas.composite(acc.resize((canvas.W, canvas.W), Image.NEAREST))

fld = warp(field(scale=2.4, octaves=4, seed=SEED + 3),
           strength=110, scale=2.5, seed=SEED + 7)
# two contour passes: broad depth bands (stronger) + fine intermediate lines
draw_contours(c, fld, np.linspace(0.10, 0.92, 11), contour, 96,
              clear_boxes=[(0, 0, DESIGN, WL + 4),          # surface band
                           (550, 350, 1016, 576)])          # headline quiet zone
draw_contours(c, fld, np.linspace(0.145, 0.885, 10),
              mix(contour, water_mid, 0.45), 60,
              clear_boxes=[(0, 0, DESIGN, WL + 4),
                           (550, 350, 1016, 576)])

# ---- 3. seabed ridge silhouette ----
sb = ridge_pts(966, 66, scale=2.6, octaves=4, seed=SEED + 5)
sb = [(0, DESIGN)] + sb + [(DESIGN, DESIGN)]
poly(c, sb, fill=seabed_ink)
# faint contour lip on the seabed crest
line(c, ak.ridge_pts(966, 66, scale=2.6, octaves=4, seed=SEED + 5),
     mix(contour, water_mid, 0.5), width=1)

# ---- 4a. faint echo-sounding depth lines (dashed) — bathymetric telemetry ----
_snow_rng = np.random.default_rng(SEED + 21)
for dy in range(WL + 70, 900, 96):
    xx = 30
    while xx < 1050:
        seg = _snow_rng.uniform(14, 30)
        if not (556 < xx < 1012 and 356 < dy < 566):   # skip headline zone
            line(c, [(xx, dy + _snow_rng.uniform(-2, 2)),
                     (xx + seg, dy + _snow_rng.uniform(-2, 2))],
                 mix(contour, water_mid, 0.62), width=1)
        xx += seg + _snow_rng.uniform(20, 40)

# ---- 4b. marine snow — fine particulate, denser in the gate light column ----
GATE = (356, 662)
for _ in range(620):
    x = _snow_rng.uniform(24, 1056)
    y = _snow_rng.uniform(WL + 14, 1058)
    if 556 < x < 1012 and 356 < y < 566:               # keep headline clean
        continue
    dg = math.hypot(x - GATE[0], (y - GATE[1]) * 0.8)
    p = 0.16 + 0.7 * math.exp(-(dg / 240.0) ** 2)      # bias toward the gate
    if _snow_rng.random() > p:
        continue
    s = _snow_rng.uniform(0.7, 2.6)
    col = mix(cable_core, contour, _snow_rng.random())
    if dg < 150:
        col = mix(col, hot, 0.25)                       # lit motes near the gate
    circle(c, x, y, s, fill=col)

# ---- 5. waterline strip ----
wl_pts = wobble_pts([(x, WL) for x in range(0, DESIGN + 1, 12)],
                    amp=1.6, scale=6.0, seed=SEED + 9)
line(c, wl_pts, mix(surface_low, contour, 0.5), width=3)
line(c, [(p[0], p[1] - 3) for p in wl_pts], lighten(surface_top, 0.03), width=1)

# ---- geometry: cable path (bezier sag) ----
def bez(p0, p1, p2, n=64):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in np.linspace(0, 1, n)]

M2 = (486, WL)             # surface application entry
GATE = (356, 662)          # focal submerged gate center
gate_top = (356, 576)
gate_bot = (356, 748)
LAND = (884, 986)          # Alaska landing

span_up = bez(M2, (398, 476), gate_top, 64)          # surface -> gate top
span_dn = bez(gate_bot, (566, 902), LAND, 72)        # gate bottom -> landing

# ---- 6. cable: dark casing halo then pale core ----
for seg in (span_up, span_dn):
    hand_line(c, seg, darken(paper_deep, 0.02), width=9, amp=1.1, seed=SEED + 31)
hand_line(c, span_up, cable_core, width=4, amp=1.1, seed=SEED + 31)
hand_line(c, span_dn, mix(cable_core, water_mid, 0.35), width=3, amp=1.1, seed=SEED + 33)

# dimension ticks along the upper span (blueprint telemetry)
for i in range(6, len(span_up) - 4, 8):
    x0, y0 = span_up[i - 1]; x1, y1 = span_up[i + 1]
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    px, py = span_up[i]
    line(c, [(px - nx * 8, py - ny * 8), (px + nx * 8, py + ny * 8)],
         mix(contour, water_mid, 0.35), width=1)

# ---- 7. three surface markers (visible FCC layers) ----
mk_font = mono(c, 13)
markers = [(232, "1921 ACT"), (486, "OI 24-523"), (742, "FCC 25-49")]
for mx, tag in markers:
    line(c, [(mx, 252), (mx, WL)], mix(surface_low, contour, 0.6), width=2)
    radial_glow(c, mx, 250, 32, mix(contour, surface_top, 0.4), maxalpha=46)
    circle(c, mx, 250, 10, outline=contour, width=2)
    circle(c, mx, 250, 3.4, fill=lighten(contour, 0.05))
    text(c, (mx, 236), tag, mk_font, darken(surface_low, 0.16),
         anchor="ms", tracking=0.12)

# ---- 8. focal gate — the one lit object ----
# rising light column (anisotropic, tall) so the gate reads as a source
radial_glow(c, GATE[0], GATE[1] - 70, 300, amber, maxalpha=34, gamma=1.7,
            sx=0.62, sy=1.35)
radial_glow(c, GATE[0], GATE[1], 236, amber, maxalpha=64, gamma=1.9)
radial_glow(c, GATE[0], GATE[1], 120, amber, maxalpha=88, gamma=2.1)
# housing (schematic blueprint)
hx0, hx1, hy0, hy1 = 281, 431, 574, 750
poly(c, [(hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0, hy1)],
     outline=contour, width=3)
# inner side rails
line(c, [(hx0 + 20, hy0), (hx0 + 20, hy1)], mix(contour, water_mid, 0.4), width=1)
line(c, [(hx1 - 20, hy0), (hx1 - 20, hy1)], mix(contour, water_mid, 0.4), width=1)
# throat opening (cable passes through center)
line(c, [(GATE[0], hy0), (GATE[0], 640)], cable_core, width=4)
line(c, [(GATE[0], 686), (GATE[0], hy1)], mix(cable_core, water_mid, 0.35), width=3)
# CLOSED barrier plate across the throat
poly(c, [(hx0 + 20, 640), (hx1 - 20, 640), (hx1 - 20, 686), (hx0 + 20, 686)],
     fill=amber, outline=hot, width=2)
# lock ribs on the plate
for ry in (650, 662, 674):
    line(c, [(hx0 + 30, ry), (hx1 - 30, ry)], darken(amber, 0.12), width=1)
# bright rim on the housing so the focal wins over the headline
poly(c, [(hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0, hy1)],
     outline=mix(amber, hot, 0.5), width=1)
# hot core
radial_glow(c, GATE[0], 663, 44, hot, maxalpha=192, gamma=2.0)
circle(c, GATE[0], 663, 8.5, fill=hot)
# corner ticks (blueprint housing detail)
for (cx, cy) in [(hx0, hy0), (hx1, hy0), (hx0, hy1), (hx1, hy1)]:
    sx = 12 if cx == hx0 else -12
    sy = 12 if cy == hy0 else -12
    line(c, [(cx, cy), (cx + sx, cy)], contour, width=2)
    line(c, [(cx, cy), (cx, cy + sy)], contour, width=2)

# gate labels (amber telemetry)
gl = mono(c, 15, medium=True)
gl2 = mono(c, 12)
soft_panel(c, (262, 758, 452, 804), color=water_bottom, alpha=120, blur=16,
           radius=10)
text(c, (GATE[0], 772), "TEAM TELECOM", gl, amber, anchor="ms", tracking=0.16)
text(c, (GATE[0], 792), "CAFP · AG CHAIR", gl2, mix(amber, contour, 0.35),
     anchor="ms", tracking=0.14)

# ---- 9. landing node ----
radial_glow(c, LAND[0], LAND[1], 40, mix(contour, surface_top, 0.3), maxalpha=52)
poly(c, [(LAND[0] - 12, LAND[1] - 12), (LAND[0] + 12, LAND[1] - 12),
         (LAND[0] + 12, LAND[1] + 12), (LAND[0] - 12, LAND[1] + 12)],
     outline=contour, width=2)
circle(c, LAND[0], LAND[1], 3.2, fill=lighten(contour, 0.05))
text(c, (LAND[0], LAND[1] + 30), "AK LANDING", gl2, mix(contour, water_mid, 0.3),
     anchor="ms", tracking=0.14)

# ---- 10. glints on the cable near the focal ----
for gx, gy in [(430, 520), (356, 600), (500, 852)]:
    radial_glow(c, gx, gy, 13, hot, maxalpha=95)
    circle(c, gx, gy, 2.0, fill=hot)

# ---- 11. finishing texture ----
grain(c, amount=6.0, seed=SEED + 41)
vignette(c, strength=0.24, spread=1.28)

# ---- 12. typography ----
# headline in the dark deep (literally below the docket surface)
soft_panel(c, (548, 348, 1018, 578), color=water_bottom, alpha=104, blur=52, radius=26)
hl = ["THE REAL GATE", "IS OFF", "THE DOCKET"]
hx = 566
hsize = fit_size(c, "THE REAL GATE", 430, lo=40, hi=110, weight=900, opsz=144)
hf = fraunces(c, hsize, weight=900, opsz=144)
lead = hsize * 1.06
y = 392
for ln in hl:
    text(c, (hx, y), ln, hf, typelight, anchor="la")
    y += lead

# kicker (mono, on the pale surface band)
kf = mono(c, 16, medium=True)
text(c, (96, 40), "THE STACK · REGULATORY · 17 JUL 2026", kf,
     darken(surface_low, 0.20), anchor="la", tracking=0.16)

# wordmark (bottom-left, knock chip for legibility on dark water)
wf = fraunces(c, 30, weight=900, opsz=120)
chip(c, (96, 1012), "ALASKA.AI", wf, typelight, darken(paper_deep, 0.03),
     pad=12, anchor="la", tracking=0.02)

# polaris colophon — a north star over the sea
polaris(c, 992, 66, r=13, color=oklch(0.86, 0.12, 88), core=hot)

# ---- meta ----
palette = [paper_deep, water_mid, surface_top, contour, amber, hot, typelight]
meta = {
    "date": "17 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "REGULATORY",
    "headline": "The Real Gate Is Off The Docket",
    "byline": "",
    "style_family": "bathymetric_blueprint",
    "palette": palette,
    "hue_family": "indigo",
    "composition": "submerged_section",
    "motifs": ["subsea fiber section", "submerged sluice gate",
               "bathymetric contours", "docket surface waterline",
               "three FCC surface markers", "Arctic landing node"],
    "technique_stack": ["gradient_v", "field", "warp", "contour_edges",
                        "ridge_pts", "hand_line", "radial_glow",
                        "echo_lines", "fine_particulate", "grain",
                        "vignette", "soft_panel"],
    "seed": SEED,
    "concept": ("Subsea fiber descends from a lit docket surface (three "
                "visible FCC layers) into dark Arctic water where the one "
                "lit element is a submerged gate the line must pass — the "
                "Team Telecom national-security veto."),
    "eval_history": [],
    "eval_final": {},
}
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
