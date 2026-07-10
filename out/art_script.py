"""The Stack — 10 JUL 2026 — bespoke cover.
Concept: a $272M federal health-capital current forced down through a single
luminous throat (one desk, the DOH Commissioner) and fanning below into 403
applicant plots of which only a handful catch the light.
Style: flow_field convergence funnel. hue_family: gold. Composition:
converging_funnel. See out/art_plan.md.
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import ImageFilter
import art_kit as K

SEED = 272
DESIGN = K.DESIGN  # 1080
rng = np.random.default_rng(SEED)

# ---- palette (hue_family gold) --------------------------------------
PAPER   = "#f3ead4"
GROUND  = "#10261c"
GROUND2 = "#0a1a12"
BRONZE  = "#6b4a1e"
AMBER   = "#c8892f"
GOLD    = "#f0bf55"
WHITEG  = "#fdeec2"
TYPEG   = "#f2c14e"
CREAM   = "#f3ead4"
PALETTE = [PAPER, GROUND, BRONZE, AMBER, GOLD, WHITEG, TYPEG]

# focal throat (the ONE DESK) — lower third so the top two-thirds converge
TX, TY = 540.0, 712.0

c = K.Canvas(bg=PAPER, ss=2)

# ---- 1. ground vertical gradient (dark spruce, faintly warm at throat)
K.gradient_v(c, (0, 0, DESIGN, DESIGN), GROUND2, GROUND, ease=1.1)
# a low warm wash lifted around the throat band so the current reads warmer there
K.glow(c, TX, TY, 430, "#26401f", alpha=42)
K.glow(c, TX, TY - 40, 300, "#3a4a1c", alpha=30)

# ---- build the converge/diverge hourglass angle field ---------------
H = W = DESIGN
ys, xs = np.mgrid[0:H, 0:W].astype(float)
dy = ys - TY
horiz_dir = np.where(dy < 0, (TX - xs), (xs - TX))   # inward above, outward below
# above the throat: strong convergence; below: gentle fan (not a mirror tunnel)
throat_scale = np.where(dy < 0, np.clip(-dy / 340.0, 0.0, 1.0),
                        np.clip(dy / 520.0, 0.0, 0.55))
vx = (horiz_dir / W) * throat_scale * 3.4
vy = np.ones_like(xs) * 1.0
ang = np.arctan2(vy, vx)
# organic life: perturb angles with a low-freq noise, calmer near throat
nz = (K.field(scale=3.0, octaves=4, seed=SEED + 5) - 0.5)
ang = ang + nz * 0.30 * (0.35 + 0.65 * throat_scale)

# proximity-to-throat scalar for coloring (0 far .. 1 at throat)
dist = np.hypot(xs - TX, ys - TY)
prox = np.clip(1.0 - dist / 720.0, 0.0, 1.0)

# gold value ramp for line color
RAMP = K.ramp([BRONZE, AMBER, GOLD, WHITEG], 24)

def line_color(pts):
    # brightest where the line passes closest to the throat
    best = 0.0
    for (x, y) in pts[::3]:
        xi = int(min(max(x, 0), W - 1)); yi = int(min(max(y, 0), H - 1))
        if prox[yi, xi] > best:
            best = prox[yi, xi]
    idx = int(round(best * (len(RAMP) - 1)))
    return RAMP[idx], best

# ---- 2. faint far current (depth) -----------------------------------
far = K.streamlines(ang, n=340, step=3.4, length=(80, 240), seed=SEED + 1,
                    min_dist=10.0, margin=0.10)
lay, ld = c.layer()
for pts in far:
    col, b = line_color(pts)
    w = 1.4 + 1.6 * b
    ld.line(c.pts(pts), fill=(*K.hex_to_rgb(col), 70), width=int(c.s(w)))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(1.4)))
c.composite(lay)

# ---- 3. main current streamlines ------------------------------------
# suppress seeds in the upper-left headline quiet zone
main = K.streamlines(ang, n=1000, step=3.0, length=(110, 360), seed=SEED + 2,
                     min_dist=5.4, margin=0.12)
lay, ld = c.layer()
kept = 0
for pts in main:
    x0, y0 = pts[0]
    # quiet zone: upper-left rectangle x<470, y<330 -> drop most seeds there
    if x0 < 470 and y0 < 330 and rng.random() < 0.85:
        continue
    col, b = line_color(pts)
    w = 1.5 + 3.4 * (b ** 1.3)
    a = int(150 + 95 * b)
    ld.line(c.pts(pts), fill=(*K.hex_to_rgb(col), a), width=int(c.s(w)))
    kept += 1
c.composite(lay)

# a few extra-bright filaments threading the throat (micro hierarchy)
bright = K.streamlines(ang, n=240, step=2.6, length=(200, 520), seed=SEED + 7,
                       min_dist=7.0, margin=0.10)
lay, ld = c.layer()
for pts in bright:
    col, b = line_color(pts)
    if b < 0.62:
        continue
    ld.line(c.pts(pts), fill=(*K.hex_to_rgb(WHITEG), int(120 + 110 * b)),
            width=int(c.s(1.3 + 1.8 * b)))
lay = lay.filter(ImageFilter.GaussianBlur(c.s(0.6)))
c.composite(lay)

# ---- 4. throat glow (under the desk glyph) --------------------------
K.glow(c, TX, TY, 210, WHITEG, alpha=64)
K.glow(c, TX, TY, 120, WHITEG, alpha=92)
K.glow(c, TX, TY - 8, 60, "#ffffff", alpha=100)

# ---- 5. the 403 applicant fan (lower delta) -------------------------
# ticks radiating from the throat into a defined lower delta; ~18 lit winners.
lay, ld = c.layer()
N_APP = 403
lit_idx = set(rng.choice(N_APP, size=18, replace=False).tolist())
win_pts = []
for i in range(N_APP):
    frac = i / (N_APP - 1)
    a = math.radians(90) + math.radians((frac - 0.5) * 2 * 54)  # spread +/-54deg
    r = rng.uniform(96, 300)
    px = TX + math.cos(a) * r
    py = TY + math.sin(a) * r * 0.94
    if py < TY + 30 or py > 992 or px < 104 or px > 976:
        continue
    lit = i in lit_idx
    if lit:
        rr = rng.uniform(3.4, 5.0)
        ld.ellipse([c.s(px-rr), c.s(py-rr), c.s(px+rr), c.s(py+rr)],
                   fill=(*K.hex_to_rgb(WHITEG), 255))
        ld.line([c.s(px), c.s(py),
                 c.s(px - math.cos(a)*14), c.s(py - math.sin(a)*14)],
                fill=(*K.hex_to_rgb(GOLD), 170), width=int(c.s(1.6)))
        win_pts.append((px, py))
    else:
        rr = rng.uniform(1.5, 2.8)
        shade = BRONZE if rng.random() < 0.72 else AMBER
        ld.ellipse([c.s(px-rr), c.s(py-rr), c.s(px+rr), c.s(py+rr)],
                   fill=(*K.hex_to_rgb(shade), int(120 + 95*rng.random())))
c.composite(lay)
# soft halo on each lit winner so the "few funded" reads
for (px, py) in win_pts:
    K.glow(c, px, py, 14, WHITEG, alpha=70)

# ---- 6. desk-slab glyph + gate-slit knockout at the throat ----------
# bright vertical gate slit rising out of the desk (the single point the money passes)
gl, gld = c.layer()
gld.rectangle([c.s(TX-9), c.s(TY-132), c.s(TX+9), c.s(TY-10)],
              fill=(*K.hex_to_rgb(WHITEG), 255))
gl = gl.filter(ImageFilter.GaussianBlur(c.s(2.6)))
c.composite(gl)
# crisp slit core
c.draw.rectangle([c.s(TX-4.2), c.s(TY-126), c.s(TX+4.2), c.s(TY-14)],
                 fill=(*K.hex_to_rgb("#ffffff"), 255))
# the desk slab (dark, man-made, wide — catches a bright top-edge)
slab = [(TX-104, TY+4), (TX+104, TY+4), (TX+128, TY+34), (TX-128, TY+34)]
K.poly(c, slab, fill=GROUND2, outline=None)
# lit front face
face = [(TX-128, TY+34), (TX+128, TY+34), (TX+128, TY+48), (TX-128, TY+48)]
K.poly(c, face, fill="#05100a")
# two short legs so it reads unmistakably as a desk
c.draw.rectangle([c.s(TX-108), c.s(TY+48), c.s(TX-98), c.s(TY+78)], fill=(*K.hex_to_rgb("#05100a"),255))
c.draw.rectangle([c.s(TX+98), c.s(TY+48), c.s(TX+108), c.s(TY+78)], fill=(*K.hex_to_rgb("#05100a"),255))
# bright top edge highlight (where the light hits the desk)
c.draw.line([c.s(TX-104), c.s(TY+4), c.s(TX+104), c.s(TY+4)],
            fill=(*K.hex_to_rgb(WHITEG), 255), width=int(c.s(3.0)))
c.draw.line([c.s(TX-104), c.s(TY+4), c.s(TX-128), c.s(TY+34)],
            fill=(*K.hex_to_rgb(AMBER), 210), width=int(c.s(1.8)))
c.draw.line([c.s(TX+104), c.s(TY+4), c.s(TX+128), c.s(TY+34)],
            fill=(*K.hex_to_rgb(AMBER), 210), width=int(c.s(1.8)))

# ---- 7. micro: sparks at throat + stipple grain in ground -----------
lay, ld = c.layer()
for _ in range(34):
    ang_s = rng.uniform(0, math.tau)
    rr = rng.uniform(20, 150)
    sx = TX + math.cos(ang_s) * rr
    sy = TY + math.sin(ang_s) * rr * 0.7
    s = rng.uniform(0.8, 2.2)
    ld.ellipse([c.s(sx-s), c.s(sy-s), c.s(sx+s), c.s(sy+s)],
               fill=(*K.hex_to_rgb(WHITEG), int(120 + 120*rng.random())))
c.composite(lay)
# faint ground stipple for tactile life in the dark corners
gmask = K.field(scale=7.0, octaves=3, seed=SEED + 3)
mimg = K.field_mask(gmask, threshold=0.62, soft=0.05)
K.stipple(c, mimg, density=0.05, r=(0.5, 1.2), color="#1c3326")

# ---- 8. finish textures ---------------------------------------------
K.grain(c, amount=6.0, seed=SEED)
K.vignette(c, strength=0.30, spread=1.16)

# ---- 9. type + marks ------------------------------------------------
# headline quiet panel (upper-left)
K.soft_panel(c, (66, 118, 520, 330), color="#0a1913", alpha=150, blur=30, radius=26)
hl_size = 96
f_hl = K.fraunces(c, hl_size, weight=900, opsz=144)
K.text(c, (96, 132), "ONE DESK", f_hl, CREAM, anchor="la")
K.text(c, (96, 224), "DECIDES", f_hl, TYPEG, anchor="la")
f_sub = K.mono(c, 18, medium=True)
K.text(c, (100, 320), "$272M FEDERAL HEALTH AWARD", f_sub, GOLD,
       anchor="la", tracking=0.16)

# soft dark band behind the bottom telemetry for legibility
K.soft_panel(c, (150, 946, 930, 1052), color="#081410", alpha=150, blur=24, radius=20)

# count label at the fan
f_cnt = K.mono(c, 16, medium=True)
K.text(c, (TX, 972), "403 APPLICANTS  ·  ~18 FUNDED", f_cnt, "#f9eecb",
       anchor="ma", tracking=0.22)

# kicker line (bottom center)
f_kick = K.mono(c, 17, medium=True)
K.text(c, (540, 1040), "THE STACK  ·  SOVEREIGNTY  ·  10 JUL 2026",
       f_kick, "#f4e6ba", anchor="ma", tracking=0.26)

# wordmark chip (bottom-left)
f_wm = K.fraunces(c, 27, weight=900, opsz=40)
K.chip(c, (70, 992), "ALASKA.AI", f_wm, GROUND2, TYPEG, pad=11, anchor="la",
       radius=7)

# polaris colophon (top-right)
K.polaris(c, 986, 78, r=13, color="#bcd0ff", core="#ffffff", halo=0.5)

# ---- meta ------------------------------------------------------------
meta = {
    "date": "10 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "SOVEREIGNTY",
    "headline": "ONE DESK DECIDES",
    "byline": "",
    "style_family": "flow_field",
    "palette": PALETTE,
    "hue_family": "gold",
    "composition": "converging_funnel",
    "motifs": ["capital current", "converging funnel throat", "single desk gate",
               "403 applicant fan", "handful of lit winners"],
    "technique_stack": ["gradient_v", "angle_field", "streamlines", "ramp",
                         "glow", "stipple", "grain", "vignette"],
    "seed": SEED,
    "concept": "A $272M federal health-capital current forced through one luminous throat (the DOH Commissioner's desk) then fanning to 403 applicant plots, only ~18 lit.",
    "eval_history": [
        {"iter": 1, "weighted": 7.45, "weakest": "focal/composition",
         "note": "read as a symmetric warp-tunnel; desk too small; 403 fan barely visible; bottom type too dark."},
        {"iter": 2, "weighted": 8.47, "weakest": "composition",
         "note": "dropped desk to lower third, enlarged desk+gate, made 403 fan explicit; still faint side-arc tunnel feel and dim bottom type."},
        {"iter": 3, "weighted": 8.78, "weakest": "detail",
         "note": "deeper vignette focused the funnel and killed the tunnel arcs; brightened bottom telemetry to legible cream. Ships."}
    ],
    "eval_final": {"weighted": 8.78, "scores": {
        "concept": 9, "focal": 9, "composition": 8.5, "color": 9,
        "detail": 8, "craft": 9, "typography": 9, "originality": 8.5,
        "fidelity": 9}},
}
K.Path = __import__("pathlib").Path
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
