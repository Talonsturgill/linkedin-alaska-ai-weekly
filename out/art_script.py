"""The Stack — 2026-07-07 — bespoke cover.
Exploded isometric fuel stack: many gas conduits funnel (7->5->3->1)
through one amber iris (the RCA cost-recovery gate) and a single conduit
survives to power a lit data-center block. iso_cutaway + blueprint."""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as K

SEED = 47

# ---- palette (7 inks incl. paper) ------------------------------------
NAVY   = "#0b1a2a"
NAVY2  = "#10263a"
TEAL_D = "#16394d"
TEAL_M = "#2e6f8e"
TEAL_L = "#5f9cb8"
CYAN   = "#cfe8f2"
AMBER  = "#ffb703"
AMBER_C= "#ffe3a3"
PALETTE = [NAVY, NAVY2, TEAL_M, TEAL_L, CYAN, AMBER, AMBER_C]

c = K.Canvas(bg=NAVY, ss=2)
W = K.DESIGN

# ---- 1. field gradient ------------------------------------------------
K.gradient_v(c, (0, 0, W, W), NAVY2, "#081320", ease=1.25)

# ---- 2. faint blueprint tick grid, right half only -------------------
lay, ld = c.layer()
gc = (*K.hex_to_rgb("#22506b"), 42)
for gx in range(556, W + 1, 70):
    ld.line([(c.s(gx), c.s(40)), (c.s(gx), c.s(1010))], fill=gc, width=max(1, int(c.s(0.8))))
for gy in range(70, W, 70):
    ld.line([(c.s(556), c.s(gy)), (c.s(1010), c.s(gy))], fill=gc, width=max(1, int(c.s(0.8))))
c.composite(lay)

# ---- iso setup --------------------------------------------------------
ORIG = (712, 648)
SCALE = 50.0
def P(x, y, z):
    return K.iso(x, y, z, SCALE, ORIG)

# slab spec: (z0, z1, half, top, left, right, tag, tag_col)
SLABS = [
    (0.00, 1.00, 1.42, "#3f8299", TEAL_M, TEAL_D, "GAS", CYAN),
    (1.80, 2.60, 1.20, "#4f93af", TEAL_M, TEAL_D, "TERMINAL", CYAN),
    (3.40, 4.20, 1.20, "#4f93af", TEAL_M, TEAL_D, "UTILITY", CYAN),
    (5.00, 5.85, 1.34, TEAL_L,    "#3a7d99", "#20475c", "RCA GATE", AMBER_C),
    (7.45, 8.05, 0.62, "#1c4d64", TEAL_D, "#0f2a3a", "AI LOAD", AMBER_C),
]
gate = SLABS[3]
load = SLABS[4]
gate_top = P(0, 0, gate[1])
gate_bot = P(0, 0, gate[0])
load_base = P(0, 0, load[0])

# ---- 3. grounding shadow under the base ------------------------------
lay, ld = c.layer()
bx, by = P(0, 0, 0)
ld.ellipse([c.s(bx - 190), c.s(by + 62), c.s(bx + 190), c.s(by + 150)],
           fill=(0, 0, 0, 120))
lay = lay.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(c.s(20)))
c.composite(lay)

# ---- 4. amber glow behind the gate -----------------------------------
K.glow(c, gate_top[0], gate_top[1] + 6, 170, AMBER, alpha=80)
K.glow(c, gate_top[0], gate_top[1] + 6, 92, AMBER_C, alpha=72)

# ---- helpers ----------------------------------------------------------
def slab(z0, z1, h, top, left, right, **_):
    K.iso_prism(c, -h, -h, z0, 2 * h, 2 * h, z1 - z0, top, left, right,
                scale=SCALE, origin=ORIG, outline=NAVY)

def face_seams(z0, z1, h, n=3, col=None):
    col = col or K.mix(TEAL_D, NAVY, 0.35)
    for k in range(1, n + 1):
        z = z0 + (z1 - z0) * k / (n + 1)
        K.line(c, [P(-h, h, z), P(h, h, z)], col, width=1)     # left face
        K.line(c, [P(h, -h, z), P(h, h, z)], K.mix(NAVY, "#000000", 0.2), width=1)  # right face

def edge_ticks(z0, z1, h):
    for k in range(6):
        z = z0 + (z1 - z0) * k / 5
        x0, y0 = P(h, h, z)
        K.line(c, [(x0, y0), (x0 + 8, y0 + 2)], CYAN, width=1)

def conduit_gap(z_lo, z_hi, n, spread_lo, spread_hi, col, wd, seed):
    for i in range(n):
        t = 0.0 if n == 1 else (i - (n - 1) / 2) / (n - 1)
        p0 = P(t * spread_lo, 0, z_lo)
        p1 = P(t * spread_hi, 0, z_hi)
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 2)
        K.hand_line(c, [p0, mid, p1], col, width=wd, amp=1.0, seed=seed + i)

# ---- 5. slabs (bottom -> top) with meso detail -----------------------
# GAS: strata + rising bubbles
slab(*SLABS[0][:6])
face_seams(*SLABS[0][:3], n=4)
edge_ticks(*SLABS[0][:3])
gz0, gz1, gh = SLABS[0][:3]
for zt in (0.25, 0.5, 0.75):                       # extra strata bands on top face
    z = gz0 + (gz1 - gz0) * zt
    K.line(c, [P(-gh, -gh, z), P(-gh, gh, z)], K.mix(TEAL_M, NAVY, 0.25), width=1)
rng = np.random.default_rng(SEED + 5)              # rising bubbles inside gas
for _ in range(46):
    mx, my = rng.uniform(-gh * 0.8, gh * 0.8), rng.uniform(-gh * 0.8, gh * 0.8)
    z = rng.uniform(gz0 + 0.1, gz1)
    px, py = P(mx, my, z)
    K.circle(c, px, py, rng.uniform(1.2, 2.6), fill=K.mix(CYAN, TEAL_M, rng.uniform(0, .6)))

# TERMINAL: two small storage tanks on the top face
slab(*SLABS[1][:6])
edge_ticks(*SLABS[1][:3])
tz1 = SLABS[1][1]
for tx, ty in ((-0.5, 0.2), (0.35, -0.35)):
    K.iso_prism(c, tx - 0.22, ty - 0.22, tz1, 0.44, 0.44, 0.5,
                "#8fbfd4", "#5f9cb8", "#3a7d99", scale=SCALE, origin=ORIG, outline=NAVY)

# UTILITY: a 2x2 transformer block cluster on the top face
slab(*SLABS[2][:6])
edge_ticks(*SLABS[2][:3])
uz1 = SLABS[2][1]
for ux in (-0.42, 0.14):
    for uy in (-0.42, 0.14):
        K.iso_prism(c, ux, uy, uz1, 0.28, 0.28, 0.36,
                    "#7fb2c9", "#4f93af", "#2e6f8e", scale=SCALE, origin=ORIG, outline=NAVY)

# ---- 6. conduit funnel in the gaps (7 -> 5 -> 3) ---------------------
conduit_gap(1.00, 1.80, 7, 1.15, 0.55, CYAN, 2, SEED + 10)
conduit_gap(2.60, 3.40, 5, 0.80, 0.38, CYAN, 2, SEED + 30)
conduit_gap(4.20, 5.00, 3, 0.50, 0.12, AMBER_C, 3, SEED + 50)

# GATE slab (focal)
slab(*gate[:6])
edge_ticks(*gate[:3])

# ---- 7. single amber conduit above the gate (the one that survives) --
# soft glow sheath along the stem, then the bright core line
lay, ld = c.layer()
ld.line([(c.s(gate_top[0]), c.s(gate_top[1] - 4)),
         (c.s(load_base[0]), c.s(load_base[1] + 6))],
        fill=(*K.hex_to_rgb(AMBER), 150), width=int(c.s(16)))
lay = lay.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(c.s(7)))
c.composite(lay)
K.line(c, [(gate_top[0], gate_top[1] - 4), (load_base[0], load_base[1] + 6)], AMBER, width=8)
K.line(c, [(gate_top[0], gate_top[1] - 4), (load_base[0], load_base[1] + 6)], AMBER_C, width=3)
# small flow chevrons rising along the stem
for zt in (6.15, 6.55, 6.95):
    cxp, cyp = P(0, 0, zt)
    K.line(c, [(cxp - 7, cyp + 6), (cxp, cyp), (cxp + 7, cyp + 6)], AMBER_C, width=2)

# ---- 8. AI-load slab with lit windows --------------------------------
slab(*load[:6])
lh, lz0, lz1 = load[2], load[0], load[1]
for row in (0.28, 0.52, 0.76):
    z = lz0 + (lz1 - lz0) * row
    for xf in (-0.55, -0.15, 0.25):                 # left face windows
        wx, wy = P(xf, lh, z)
        K.circle(c, wx, wy, 3.2, fill=AMBER_C)
    for yf in (-0.15, 0.25):                          # right face windows
        wx, wy = P(lh, yf, z)
        K.circle(c, wx, wy, 3.0, fill=AMBER)

# ---- 9. gate iris (focal) --------------------------------------------
gx, gy = gate_top
K.circle(c, gx, gy, 50, fill=None, outline=K.mix(AMBER, NAVY, 0.35), width=3)
K.rays(c, gx, gy, 6, 19, 47, AMBER, width_deg=36, jitter=0, seed=SEED)
K.circle(c, gx, gy, 19, fill=AMBER_C)
K.circle(c, gx, gy, 8, fill="#fff6e0")

# ---- 10. tiny slab labels --------------------------------------------
mono_s = K.mono(c, 15, medium=True)
for (z0, z1, h, top, left, right, tag, tcol) in SLABS:
    zx, zy = P(h, -h, (z0 + z1) / 2)
    K.text(c, (zx + 15, zy - 5), tag, mono_s, tcol, anchor="lm", tracking=0.14)
gsx, gsy = P(gate[2], -gate[2], gate[0] + 0.16)
K.text(c, (gsx + 15, gsy + 15), "AS 42.05.141", K.mono(c, 12), CYAN, anchor="lm", tracking=0.10)

# ---- 11. headline ----------------------------------------------------
hl1, hl2 = "Alaska AI’s Power", "Runs on One Vote"
maxw = 452
sz = min(K.fit_size(c, hl1, maxw, hi=112, weight=900, opsz=144),
         K.fit_size(c, hl2, maxw, hi=112, weight=900, opsz=144))
fnt = K.fraunces(c, sz, weight=900, opsz=144)
hy = 436
K.text(c, (92, hy), hl1, fnt, CYAN, anchor="la")
K.text(c, (92, hy + sz * 1.05), hl2, fnt, AMBER, anchor="la")
# supporting line (one small moment)
K.text(c, (94, hy + sz * 1.05 + sz * 0.98 + 14),
       "one terminal · one cost-recovery vote", K.mono(c, 16), TEAL_L,
       anchor="la", tracking=0.10)

# kicker
K.text(c, (96, 150), "THE STACK · FACILITIES · 7 JUL 2026",
       K.mono(c, 17, medium=True), CYAN, anchor="la", tracking=0.20)

# ---- 12. wordmark + coords + polaris ---------------------------------
K.text(c, (96, 986), "ALASKA.AI", K.fraunces(c, 30, weight=900, opsz=40),
       CYAN, anchor="la", tracking=0.02)
K.text(c, (984, 998), "61°13′N · 149°54′W", K.mono(c, 13), TEAL_L,
       anchor="ra", tracking=0.10)
K.polaris(c, 980, 96, r=13, color=AMBER, core=AMBER_C)

# ---- 13. finishing ----------------------------------------------------
K.grain(c, amount=6.0, seed=SEED, mono=True)
K.vignette(c, strength=0.22, spread=1.4)

meta = {
    "date": "7 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "FACILITIES",
    "byline": "",
    "headline": "Alaska AI's Power\nRuns on One Vote",
    "style_family": "iso_cutaway",
    "palette": PALETTE,
    "hue_family": "blue-teal",
    "composition": "thirds_focal",
    "motifs": ["exploded fuel stack", "gate iris", "converging conduits", "data-center block"],
    "technique_stack": ["iso_prism", "gradient_v", "hand_line", "glow", "rays", "grain", "vignette"],
    "seed": SEED,
    "eval_history": [
        {"iter": 1, "weighted": 7.7, "weakest": "concept-legibility"},
        {"iter": 2, "weighted": 8.3, "weakest": "output-conduit-payoff"},
        {"iter": 3, "weighted": 8.68, "weakest": "detail-richness"}
    ],
    "eval_final": {
        "weighted": 8.68,
        "scores": {"concept": 9, "focal": 9, "composition": 8.5, "color": 9,
                   "detail": 8, "craft": 8, "typography": 9, "originality": 8.5,
                   "fidelity": 9}
    },
}
K.ensure_fonts()
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
