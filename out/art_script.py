import sys, math, json
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import art_kit as k

SEED = 5101
rng = np.random.default_rng(SEED)

PAPER = "#eee5d0"; PALE = "#bcd3c8"; FIELD = "#2f7c78"; SHADOW = "#14403f"
INK = "#0b1a1b"; COPPER = "#c8743a"; SIGNAL = "#ff5f1f"; CERAMIC = "#e4d9bf"

c = k.Canvas(bg=PAPER)
S = 1080

# paper tooth
k.mottle(c, strength=0.05, scale=3.0, seed=SEED)

# ---- faint rays from the hinge ---------------------------------------
HX, HY = 330, 716
lay, ld = c.layer()
k.rays(c, HX, HY, 28, 60, 1500, (*k.hex_to_rgb(PALE), 70), width_deg=4.2, jitter=0.6,
       seed=SEED, d=ld)
c.composite(lay)

# ---- ridges ------------------------------------------------------------
def tilted(y_base, amp, seed, tilt, scale=3.0):
    p = k.ridge_pts(y_base, amp, scale=scale, octaves=4, seed=seed)
    return [(x, y - (x / S) * tilt) for x, y in p]

def fill_ridge(pts, col, bottom=S):
    k.poly(c, [(pts[0][0], bottom)] + pts + [(pts[-1][0], bottom)], fill=col)

far = tilted(585, 70, 11, 150)
mid = tilted(668, 55, 23, 120, scale=2.4)
near = tilted(770, 40, 37, 60, scale=2.0)
fill_ridge(far, k.mix(PAPER, PALE, 0.9))
# far-ridge snow caps (meso)
for x, y in far[::3]:
    pass
fill_ridge(mid, k.mix(PALE, FIELD, 0.55))

# hatch strata on far ridge for texture
m_im, md = c.mask()
md.polygon(c.pts([(far[0][0], S)] + far + [(far[-1][0], S)]), fill=255)
k.hatch(c, m_im, spacing=11, angle=62, color=k.mix(PALE, FIELD, 0.35), width=1.1)
fill_ridge(mid, k.mix(PALE, FIELD, 0.55))

# ---- pylon line on mid ridge -------------------------------------------
def ridge_y(pts, x):
    xs = [p[0] for p in pts]
    return float(np.interp(x, xs, [p[1] for p in pts]))

def tower(cx, base_y, h, col, w=None):
    w = w or h * 0.34
    top = base_y - h
    # legs
    k.line(c, [(cx - w / 2, base_y), (cx - w * 0.12, top + h * .28), (cx - w * .06, top)], col, 1.6)
    k.line(c, [(cx + w / 2, base_y), (cx + w * 0.12, top + h * .28), (cx + w * .06, top)], col, 1.6)
    # bracing
    n = 5
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        yl0 = base_y - h * .72 * t0; yl1 = base_y - h * .72 * t1
        wl0 = w * (1 - t0 * .76) / 2; wl1 = w * (1 - t1 * .76) / 2
        k.line(c, [(cx - wl0, yl0), (cx + wl1, yl1)], col, 1.0)
        k.line(c, [(cx + wl0, yl0), (cx - wl1, yl1)], col, 1.0)
    # crossarms
    arms = []
    for frac, span in ((0.78, 1.0), (0.9, 0.8)):
        ay = base_y - h * frac
        k.line(c, [(cx - w * span, ay), (cx + w * span, ay)], col, 1.8)
        arms += [(cx - w * span, ay + 4), (cx + w * span, ay + 4)]
        for sx in (-1, 1):
            k.line(c, [(cx + sx * w * span, ay), (cx + sx * w * span, ay + 4)], col, 1.2)
    return arms

def sag(p0, p1, col, droop, width=1.1):
    pts = []
    for i in range(25):
        t = i / 24
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t + droop * 4 * t * (1 - t)
        pts.append((x, y))
    k.line(c, pts, col, width)

xs = [58 + i * 91 for i in range(11)]
prev = None
TCOL = k.mix(INK, SHADOW, 0.35)
towers = []
for i, x in enumerate(xs):
    by = ridge_y(mid, x) + 2
    h = 40 + (i % 3) * 5 + (i / 10) * 18
    towers.append((x, by, h))
arm_sets = []
for x, by, h in towers:
    arm_sets.append(tower(x, by, h, TCOL))
for a, b in zip(arm_sets[:-1], arm_sets[1:]):
    for j in range(4):
        sag(a[j + (2 if j < 2 else 0) if False else (2, 3, 0, 1)[j] if False else (1, 3, 1, 3)[j]] if False else a[(1,3,1,3)[j]],
            b[(0,2,0,2)[j]], TCOL, 7)
# lit end: Healy cluster at last tower
hx, hy, hh = towers[-1]
k.glow(c, hx + 6, hy - hh - 6, 40, SIGNAL, alpha=70)

fill_ridge(near, k.mix(FIELD, SHADOW, 0.55))
m2, md2 = c.mask()
md2.polygon(c.pts([(near[0][0], S)] + near + [(near[-1][0], S)]), fill=255)
k.stipple(c, m2, density=0.28, r=(0.4, 1.0), color=k.mix(FIELD, PALE, 0.5), seed=SEED + 1)
k.chips(c, 90, (0, 700, S, 840), size=(1.5, 3.4), colors=(PAPER, PALE), seed=SEED + 2, mask_img=m2)
m4, md4 = c.mask()
md4.polygon(c.pts([(mid[0][0], S)] + mid + [(mid[-1][0], S)]), fill=255)
md4.polygon(c.pts([(0, 720), (S, 700), (S, S), (0, S)]), fill=0)
k.stipple(c, m4, density=0.22, r=(0.4, 1.0), color=k.mix(PALE, PAPER, 0.5), seed=SEED + 9)
k.chips(c, 60, (0, 560, S, 700), size=(1.4, 3.0), colors=(PAPER, PALE), seed=SEED + 10, mask_img=m4)
# strata contour lines on mid and near ridges
for off, col in ((16, k.mix(PALE, FIELD, 0.4)), (34, k.mix(PALE, FIELD, 0.7))):
    k.hand_line(c, [(x, y + off) for x, y in mid], col, 1.4, amp=1.6, seed=off)
for off in (14, 30, 48):
    k.hand_line(c, [(x, y + off) for x, y in near], k.mix(FIELD, PALE, 0.28), 1.3, amp=1.4, seed=off)
# spruce stand along the near ridge
for x in range(8, S, 14):
    yy = ridge_y(near, x) + 6
    hh = 14 + (hash((x, 3)) % 14)
    k.poly(c, [(x - 5, yy), (x, yy - hh), (x + 5, yy)], fill=k.mix(INK, SHADOW, 0.4))
# fog band
lay, ld = c.layer()
k.poly(c, [(0, 640), (S, 600), (S, 700), (0, 740)], fill=(*k.hex_to_rgb(PAPER), 40), d=ld)
lay = lay.filter(ImageFilter.GaussianBlur(26)); c.composite(lay)
# ground below to the base
k.poly(c, [(0, 830), (S, 830), (S, S), (0, S)], fill=SHADOW)
m3, md3 = c.mask(); md3.rectangle(c.pts([(0, 830), (S, S)])[0] + c.pts([(0, 830), (S, S)])[1], fill=255)
k.hatch(c, m3, spacing=9, angle=-28, color=k.mix(SHADOW, INK, 0.45), width=1.2)

# ---- feed wires ---------------------------------------------------------
WIRE = INK
def catenary(p0, p1, droop, col, w):
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t + droop * 4 * t * (1 - t)))
    k.line(c, pts, col, w)

LJ = (HX, HY - 40)              # hinge terminal top
RJ = (850, 676)
catenary((HX - 40, 690), (-10, 560), 40, WIRE, 4)
catenary((RJ[0] + 40, 690), (1090, 520), 30, WIRE, 4)

# ---- base slab ----------------------------------------------------------
k.poly(c, [(170, 842), (1010, 842), (1030, 956), (150, 956)], fill=INK)
k.poly(c, [(170, 842), (1010, 842), (1006, 852), (174, 852)], fill=k.mix(INK, FIELD, 0.45))
# scale ticks along slab top edge
for i in range(0, 61):
    tx = 190 + i * 13
    k.line(c, [(tx, 856), (tx, 856 + (9 if i % 5 == 0 else 5))], k.mix(INK, PALE, 0.42), 1.1)
# bolt heads
for bx in (206, 330, 456, 600, 730, 850, 972):
    k.circle(c, bx, 912, 8, fill=k.mix(INK, PALE, 0.28))
    k.circle(c, bx, 912, 8, outline=k.mix(INK, PALE, 0.6), width=1.4)
    k.line(c, [(bx - 5, 912), (bx + 5, 912)], k.mix(INK, PALE, 0.65), 1.4)
for y in (894, ):
    k.line(c, [(210, y), (970, y)], k.mix(INK, FIELD, 0.28), 1)

# ---- insulator columns --------------------------------------------------
def insulator(cx, y_top, y_bot, w=34):
    # ceramic stack with ribbed sheds
    n = 9
    h = (y_bot - y_top) / n
    k.poly(c, [(cx - w * .3, y_top), (cx + w * .3, y_top), (cx + w * .3, y_bot), (cx - w * .3, y_bot)], fill=k.mix(CERAMIC, INK, 0.25))
    for i in range(n):
        y = y_top + i * h
        sw = w * (0.62 if i % 2 == 0 else 0.5)
        k.poly(c, [(cx - sw, y + h * .2), (cx + sw, y + h * .2), (cx + sw * .88, y + h * .78), (cx - sw * .88, y + h * .78)],
               fill=CERAMIC)
        k.poly(c, [(cx + sw * .18, y + h * .2), (cx + sw, y + h * .2), (cx + sw * .88, y + h * .78), (cx + sw * .18, y + h * .78)],
               fill=k.mix(CERAMIC, SHADOW, 0.35))
        k.line(c, [(cx - sw, y + h * .78), (cx + sw * .88, y + h * .78)], k.mix(CERAMIC, INK, 0.5), 1.2)
    # flange
    k.poly(c, [(cx - w * .75, y_bot - 8), (cx + w * .75, y_bot - 8), (cx + w * .75, y_bot + 6), (cx - w * .75, y_bot + 6)], fill=k.mix(INK, PALE, 0.35))

insulator(HX, 700, 846)
insulator(850, 700, 846)

# hinge terminal block (left)
k.poly(c, [(HX - 46, 676), (HX + 46, 676), (HX + 46, 706), (HX - 46, 706)], fill=COPPER)
k.poly(c, [(HX - 46, 676), (HX + 46, 676), (HX + 46, 683), (HX - 46, 683)], fill=k.lighten(COPPER, 0.25))
k.circle(c, HX, 690, 15, fill=INK)
k.circle(c, HX, 690, 15, outline=k.lighten(COPPER, .3), width=2)
k.circle(c, HX, 690, 5, fill=k.lighten(COPPER, .35))
# jaw (right): two copper clips
JX = 850
k.poly(c, [(JX - 52, 676), (JX + 52, 676), (JX + 52, 706), (JX - 52, 706)], fill=COPPER)
k.poly(c, [(JX - 52, 676), (JX + 52, 676), (JX + 52, 683), (JX - 52, 683)], fill=k.lighten(COPPER, .25))
k.poly(c, [(JX - 24, 676), (JX - 10, 676), (JX - 10, 600), (JX - 24, 600)], fill=k.darken(COPPER, .1))
k.poly(c, [(JX + 10, 676), (JX + 24, 676), (JX + 24, 600), (JX + 10, 600)], fill=COPPER)
k.poly(c, [(JX - 24, 600), (JX - 10, 600), (JX - 18, 586)], fill=k.lighten(COPPER, .15))
k.poly(c, [(JX + 10, 600), (JX + 24, 600), (JX + 18, 586)], fill=k.lighten(COPPER, .15))
k.line(c, [(JX - 10, 604), (JX - 10, 676)], k.darken(COPPER, .35), 1.5)

# ---- blade --------------------------------------------------------------
ang = math.radians(48)
L = 360
tipx, tipy = HX + math.cos(ang) * L, 690 - math.sin(ang) * L
nx, ny = -math.sin(ang), -math.cos(ang)   # normal toward upper-left
bw = 15
def bladepts(w0, w1):
    return [(HX + nx * w0 * -1, 690 + ny * w0 * -1), (tipx + nx * w1 * -1, tipy + ny * w1 * -1),
            (tipx + nx * w1, tipy + ny * w1), (HX + nx * w0, 690 + ny * w0)]
# soft cast shadow on sky
lay, ld = c.layer()
k.poly(c, [(x + 14, y + 12) for x, y in bladepts(bw, bw * .8)], fill=(*k.hex_to_rgb(SHADOW), 60), d=ld)
lay = lay.filter(ImageFilter.GaussianBlur(10)); c.composite(lay)
k.poly(c, bladepts(bw, bw * .8), fill=SIGNAL)
# bevel highlight and dark edge
k.line(c, [(HX + nx * bw * .55, 690 + ny * bw * .55), (tipx + nx * bw * .45, tipy + ny * bw * .45)], k.lighten(SIGNAL, .35), 3)
k.line(c, [(HX - nx * bw * .85, 690 - ny * bw * .85), (tipx - nx * bw * .68, tipy - ny * bw * .68)], k.darken(SIGNAL, .35), 3)
# rivets along the blade
for t in (0.12, 0.3, 0.5, 0.7):
    px, py = HX + math.cos(ang) * L * t, 690 - math.sin(ang) * L * t
    k.circle(c, px, py, 3.2, fill=k.darken(SIGNAL, .4))
    k.circle(c, px - .8, py - .8, 1.4, fill=k.lighten(SIGNAL, .45))
k.glow(c, tipx, tipy, 46, SIGNAL, alpha=55)
# handle ring
k.circle(c, tipx, tipy, 26, outline=INK, width=9)
k.circle(c, tipx, tipy, 26, outline=k.mix(INK, FIELD, .4), width=2)
k.circle(c, tipx, tipy, 6, fill=SIGNAL)
# spark ticks where blade would meet the jaw
for a in (-30, -10, 14, 36):
    r0, r1 = 20, 36
    cx0, cy0 = JX - 6, 580
    k.line(c, [(cx0 + math.cos(math.radians(a - 90)) * r0, cy0 + math.sin(math.radians(a - 90)) * r0),
               (cx0 + math.cos(math.radians(a - 90)) * r1, cy0 + math.sin(math.radians(a - 90)) * r1)], SIGNAL, 2.2)

# hinge pin over blade root
k.circle(c, HX, 690, 12, fill=k.mix(INK, PALE, .2)); k.circle(c, HX, 690, 4, fill=PALE)

# ---- labels (dossier-only) ----------------------------------------------
ml = k.mono(c, 14, medium=True)
k.text(c, (HX - 60, 862), "INTENT TO DEPLOY", ml, PALE, tracking=0.12)
k.text(c, (HX - 60, 880), "UP TO $150M", k.mono(c, 14, medium=True), SIGNAL, tracking=0.12)
k.text(c, (JX - 60, 862), "NON-FEDERAL", ml, PALE, tracking=0.12)
k.text(c, (JX - 60, 880), "$268M", k.mono(c, 14, medium=True), SIGNAL, tracking=0.12)
# slab caption + wordmark
k.text(c, (590, 940), "SEC. OF ENERGY  /  OBLIGATE  Y/N", k.mono(c, 12), k.mix(PALE, INK, .15), tracking=0.18, anchor="mm")

# dimension line + geese (micro)
DL = k.mix(SHADOW, PALE, 0.15)
k.line(c, [(650, 404), (1018, 404)], DL, 1.5)
for xx in (650, 1018):
    k.line(c, [(xx, 396), (xx, 412)], DL, 1.5)
k.text(c, (834, 386), "223 MI  BELUGA TO HEALY", k.mono(c, 13, medium=True), DL, tracking=0.16, anchor="mm")
for gx, gy, gs in ((760, 215, 1.0), (800, 238, .8), (726, 244, .7), (846, 206, .6), (700, 190, .55), (880, 252, .5)):
    k.line(c, [(gx - 11*gs, gy - 5*gs), (gx, gy), (gx + 11*gs, gy - 5*gs)], k.mix(SHADOW, PAPER, .25), 1.8)

# ---- headline ------------------------------------------------------------
hf = k.fraunces(c, 70, weight=900, opsz=144)
lines = ["BELUGA-HEALY", "RIDES  THE", "DEFENSE", "PRODUCTION  ACT"]
size = 70
while max(k.measure(c, s, k.fraunces(c, size, weight=900), 0) for s in lines) > 540:
    size -= 1
hf = k.fraunces(c, size, weight=900, opsz=144)
y = 62
for i, s in enumerate(lines):
    col = INK if i != 3 else SHADOW
    k.text(c, (72, y), s, hf, col, tracking=0.012)
    y += size * 1.03
# orange rule under headline
k.poly(c, [(72, y + 10), (72 + 90, y + 10), (72 + 90, y + 16), (72, y + 16)], fill=SIGNAL)
kick = "THE STACK  ·  VEHICLES  ·  5 OCT 2026"
k.text(c, (72, y + 32), kick, k.mono(c, 15, medium=True), SHADOW, tracking=0.2)

# ---- marks ---------------------------------------------------------------
wf = k.fraunces(c, 30, weight=900, opsz=144)
k.text(c, (72, 1000), "ALASKA.AI", wf, PAPER)
k.polaris(c, 996, 84, r=15, color=SIGNAL, core="#fff0c8")

k.grain(c, amount=6, seed=SEED)

meta = {
    "date": "5 OCT 2026", "column": "The Stack", "kicker": "THE STACK",
    "middle_slot": "VEHICLES", "headline": "Beluga-Healy rides the Defense Production Act",
    "byline": "",
    "style_family": "constructivist_switchgear",
    "palette": [PAPER, PALE, FIELD, SHADOW, INK, COPPER, SIGNAL],
    "hue_family": "teal", "composition": "knife_switch_diagonal",
    "motifs": ["open knife switch", "raised orange blade with insulated ring handle", "ribbed ceramic insulators", "lattice pylon line on ridge", "copper jaw clips", "intent versus obligation"],
    "technique_stack": ["ridge_pts", "hatch", "stipple", "chips", "rays", "glow", "mottle", "grain"],
    "seed": SEED, "eval_history": [], "eval_final": {},
}
import os
if os.path.exists("out/eval_final.json"):
    ev = json.load(open("out/eval_final.json"))
    meta["eval_history"] = ev.get("history", []); meta["eval_final"] = ev.get("final", {})
c.finish("out/post_image.png", meta)
print("rendered")
