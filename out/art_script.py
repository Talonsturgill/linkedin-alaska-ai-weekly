"""The Stack — 7 JUL 2026 — bespoke cover art.
Concept: cadastral state-land disposal document. One vermilion Commissioner
consent seal (the chokepoint) stamped over a surveyed North Slope parcel;
500+ public-comment marks pile against a single closed gate but none pass.
Style family: cadastral_ledger (engraving/blueprint + topo + swiss type).
"""
import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
from PIL import Image, ImageDraw
import numpy as np
import art_kit as K

SEED = 738
rng = np.random.default_rng(SEED)

# ---- palette (value spine: paper light -> ink dark, one red focal) ----
PAPER   = "#ece3cf"   # ledger cream, document ground
PARCH   = "#d8c9a3"   # parcel fill, one value step down
INK     = "#241f18"   # warm near-black, headline + primary line
GRAPH   = "#7a6f57"   # graphite mid, grid / ticks / contour
CONTOUR = "#c6b992"   # faint contour line
VERM    = "#c0341d"   # consent vermilion, the focal
SLATE   = "#4d6473"   # cold restraint, river + a few marks
GOLD    = "#ffc72c"   # polaris colophon only
CREAM   = "#f1e8d4"   # seal ring + seal type

c = K.Canvas(bg=PAPER, ss=2)
W = 1080

def clip_paste(lay, region_mask):
    """Paste RGBA `lay` only where it drew AND inside region_mask (L, c.W)."""
    fm = Image.composite(region_mask, Image.new("L", (c.W, c.W), 0),
                         lay.getchannel("A"))
    c.img.paste(lay, (0, 0), fm)
    c.draw = ImageDraw.Draw(c.img, "RGBA")

# ===================================================================
# 1. paper tone: mottle + a faint large-scale warm/cool field
# ===================================================================
K.mottle(c, strength=0.045, scale=2.4, seed=SEED + 2)
tone = K.warp(K.field(scale=2.2, octaves=3, seed=SEED + 5), strength=40, scale=2.0, seed=SEED + 6)
tone_img = K.field_img(tone, K.darken(PAPER, 0.05), K.lighten(PAPER, 0.03))
c.paste_img(tone_img, alpha=0.28)

# ===================================================================
# 2. faint topo contours across the lower/central ground (calm top)
# ===================================================================
for i, yb in enumerate(range(486, 1010, 62)):
    amp = 14 + (i % 3) * 6
    pts = K.ridge_pts(yb, amp, scale=2.4, octaves=3, seed=SEED + 30 + i,
                      x0=36, x1=1044, step=6)
    col = K.mix(CONTOUR, PAPER, 0.25 if yb > 720 else 0.5)
    K.hand_line(c, pts, col, width=1.2, amp=1.4, seed=SEED + i)

# ===================================================================
# 2.5 document neatline border + margin graticule (legal instrument)
# ===================================================================
def rrect(x0, y0, x1, y1, col, w):
    K.line(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], col, width=w)
rrect(34, 34, 1046, 1046, GRAPH, 1.6)
rrect(41, 41, 1039, 1039, K.mix(GRAPH, PAPER, 0.35), 1.0)
for gx in range(34, 1047, 90):
    K.line(c, [(gx, 34), (gx, 45)], GRAPH, width=1.2)
    K.line(c, [(gx, 1046), (gx, 1035)], GRAPH, width=1.2)
for gy in range(34, 1047, 90):
    K.line(c, [(34, gy), (45, gy)], GRAPH, width=1.2)
    K.line(c, [(1046, gy), (1035, gy)], GRAPH, width=1.2)

# ===================================================================
# 3. the surveyed parcel (irregular tract), lower-center
# ===================================================================
PARCEL = [(168, 560), (470, 486), (742, 470), (930, 604),
          (886, 872), (560, 900), (250, 860)]
# humanize the boundary
bnd = K.wobble_pts(PARCEL + [PARCEL[0]], amp=1.6, scale=6.0, seed=SEED + 3)
# parcel fill
K.poly(c, bnd, fill=PARCH)
# parcel L-mask (for clipping grid / shading)
pm, pmd = c.mask()
pmd.polygon(c.pts(bnd), fill=255)

# section grid clipped to the parcel
glay, gld = c.layer()
gcol = (*K.hex_to_rgb(GRAPH), 150)
for gx in range(150, 960, 66):
    gld.line([(c.s(gx), c.s(455)), (c.s(gx), c.s(915))], fill=gcol, width=max(1, int(c.s(1.1))))
for gy in range(470, 916, 66):
    gld.line([(c.s(150), c.s(gy)), (c.s(960), c.s(gy))], fill=gcol, width=max(1, int(c.s(1.1))))
clip_paste(glay, pm)

# contour hints + river inside the parcel
rlay, rld = c.layer()
rcol = (*K.hex_to_rgb(SLATE), 200)
river = K.wobble_pts([(196, 812), (300, 792), (392, 830), (470, 806), (540, 852)],
                     amp=3.0, scale=5.0, seed=SEED + 8)
rld.line(c.pts(river), fill=rcol, width=max(1, int(c.s(3.0))), joint="curve")
clip_paste(rlay, pm)

# parcel boundary line (firm, drawn over fill + grid)
K.line(c, bnd, INK, width=3.4)

# metes-and-bounds ticks + tiny bearing dots along the boundary
for a, b in zip(bnd[::3], bnd[1::3]):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    K.line(c, [(mx - nx * 7, my - ny * 7), (mx + nx * 7, my + ny * 7)], GRAPH, width=2)

# data-center footprint (unlabeled; size unverified so no dimensions)
fp = [(612, 772), (704, 772), (704, 828), (612, 828)]
K.poly(c, fp, outline=INK, width=2)
flay, fld = c.layer()
fcol = (*K.hex_to_rgb(GRAPH), 130)
for fx in range(614, 704, 8):
    fld.line([(c.s(fx), c.s(772)), (c.s(fx), c.s(828))], fill=fcol, width=max(1, int(c.s(0.9))))
fpm, fpmd = c.mask()
fpmd.polygon(c.pts(fp), fill=255)
clip_paste(flay, fpm)

# ===================================================================
# 4. engraving shading: light stipple tooth in parcel + corner hatch
# ===================================================================
K.stipple(c, pm, density=0.062, r=(0.5, 1.4), color=K.mix(GRAPH, INK, 0.3), seed=SEED + 12)
# bottom-right corner hatch
hm, hmd = c.mask()
hmd.polygon(c.pts([(700, 720), (930, 604), (886, 872), (620, 892)]), fill=255)
hm = Image.composite(hm, Image.new("L", (c.W, c.W), 0), pm)
K.hatch(c, hm, spacing=12.0, angle=32.0, color=K.mix(GRAPH, INK, 0.28), width=1.2)
# bottom-left corner hatch (cross-angle, lighter) for balance
hm2, hmd2 = c.mask()
hmd2.polygon(c.pts([(250, 860), (470, 872), (430, 900), (250, 900)]), fill=255)
hm2 = Image.composite(hm2, Image.new("L", (c.W, c.W), 0), pm)
K.hatch(c, hm2, spacing=14.0, angle=-28.0, color=K.mix(GRAPH, INK, 0.2), width=1.0)

# ===================================================================
# 5. the single GATE in the left boundary + comment drift piling up
# ===================================================================
GATE = (207, 704)
# left-boundary x as a function of y, for placing marks just outside it
def bound_x(y):
    return 168 + (y - 560) / (860 - 560) * (250 - 168)

# gate posts (two short ink posts) + vermilion latch
K.line(c, [(GATE[0] - 3, GATE[1] - 26), (GATE[0] - 3, GATE[1] - 4)], INK, width=5)
K.line(c, [(GATE[0] + 9, GATE[1] + 4), (GATE[0] + 9, GATE[1] + 26)], INK, width=5)
K.line(c, [(GATE[0] - 3, GATE[1] - 4), (GATE[0] + 9, GATE[1] + 4)], VERM, width=4)

# unifying soft mass shadow behind the drift
K.glow(c, 152, 706, 138, K.mix(GRAPH, PAPER, 0.32), alpha=48)
# comment marks: dense orderly tally-ticks piling at the closed gate.
# near-vertical strokes leaning toward the gate; the nearest ranks read
# heaviest, and none pass the fence.
n_marks = 470
placed = 0
for _ in range(n_marks * 4):
    if placed >= n_marks:
        break
    y = float(np.clip(rng.normal(704, 98), 536, 872))
    xmax = bound_x(y) - 9
    gap = abs(rng.normal(0, 46))           # distance back from the fence
    x = float(np.clip(xmax - gap - rng.uniform(1, 6), 62, xmax))
    if x >= xmax:
        continue
    lean = 0.24 if GATE[0] > x else -0.24
    ang = -math.pi / 2 + lean * min(1.0, (704 - abs(y - 704)) / 704 + 0.3) + rng.uniform(-0.14, 0.14)
    L = rng.uniform(6, 11)
    near = gap < 26                        # front ranks pressed on the gate
    if rng.random() < 0.05:
        col = SLATE
    else:
        col = K.mix(GRAPH, INK, rng.uniform(0.45, 0.72) if near else rng.uniform(0.18, 0.5))
    x2, y2 = x + math.cos(ang) * L, y + math.sin(ang) * L
    K.line(c, [(x, y), (x2, y2)], col, width=1.4 if near else 1.2)
    placed += 1
# a scatter of tiny paper "slips" for texture variety
for _ in range(26):
    y = float(np.clip(rng.normal(704, 110), 528, 878))
    xmax = bound_x(y) - 11
    x = float(np.clip(xmax - abs(rng.normal(0, 46)) - 6, 64, xmax - 6))
    w_, h_ = rng.uniform(5, 8), rng.uniform(3, 5)
    K.poly(c, [(x, y), (x + w_, y - 1), (x + w_, y + h_), (x, y + h_ + 1)],
           fill=K.mix(GRAPH, PAPER, 0.15), outline=INK, width=1)

# ===================================================================
# 6. the CONSENT SEAL — vermilion, the focal (central_icon)
# ===================================================================
SX, SY, SR = 632, 606, 148
# emboss shadow
K.glow(c, SX + 7, SY + 12, SR * 1.04, INK, alpha=55)
# inked disc with slightly irregular edge
disc = K.blob_pts(SX, SY, SR, wobble=0.012, harmonics=(1, 2, 3, 7), points=180, seed=SEED + 20)
K.poly(c, disc, fill=VERM)
# subtle inner darkening ring for stamp depth
K.circle(c, SX, SY, SR - 6, outline=K.darken(VERM, 0.18), width=3)
# two cream rings + border ticks between them
K.circle(c, SX, SY, 128, outline=CREAM, width=3)
K.circle(c, SX, SY, 112, outline=CREAM, width=2)
for i in range(48):
    a = i / 48 * math.tau
    K.line(c, [(SX + math.cos(a) * 114, SY + math.sin(a) * 114),
               (SX + math.cos(a) * 126, SY + math.sin(a) * 126)], CREAM, width=2)
# inner text stack (all dossier-grounded)
mono_hd = K.mono(c, 15, medium=True)
K.text(c, (SX, SY - 40), "COMMISSIONER", mono_hd, CREAM, anchor="mm", tracking=0.16)
K.text(c, (SX, SY - 18), "OF NATURAL RESOURCES", K.mono(c, 12, medium=True), CREAM, anchor="mm", tracking=0.14)
fra_seal = K.fraunces(c, 42, weight=850, opsz=144, soft=10)
K.text(c, (SX, SY + 14), "CONSENT", fra_seal, CREAM, anchor="mm", tracking=0.06)
K.line(c, [(SX - 84, SY + 40), (SX + 84, SY + 40)], CREAM, width=1.4)
K.text(c, (SX, SY + 58), "AS 38.05.035(e)", K.mono(c, 15, medium=True), CREAM, anchor="mm", tracking=0.08)

# ===================================================================
# 7. process ladder — the four dossier layers, stage 03 = consent (hot)
# ===================================================================
LX = 974
stages = [496, 568, 640, 712]
K.line(c, [(LX + 13, stages[0]), (LX + 13, stages[-1] + 26)], GRAPH, width=2)
num_f = K.mono(c, 15, medium=True)
for i, sy in enumerate(stages):
    box = [(LX, sy), (LX + 26, sy), (LX + 26, sy + 26), (LX, sy + 26)]
    if i == 2:
        K.poly(c, box, fill=VERM)
        K.poly(c, box, outline=K.darken(VERM, 0.2), width=2)
    else:
        K.poly(c, box, fill=PAPER, outline=GRAPH, width=2)
    K.text(c, (LX - 8, sy + 13), f"0{i+1}", num_f,
           VERM if i == 2 else GRAPH, anchor="rm", tracking=0.05)

# ===================================================================
# 8. north arrow + Polaris colophon (top-right counterweight)
# ===================================================================
NX = 966
K.line(c, [(NX, 176), (NX, 122)], INK, width=4)
K.poly(c, [(NX, 106), (NX - 10, 130), (NX + 10, 130)], fill=INK)
K.polaris(c, NX, 92, r=12, color=GOLD, core="#fff0c8")
K.text(c, (NX, 198), "N", K.mono(c, 16, medium=True), INK, anchor="mm", tracking=0.0)

# ===================================================================
# 9. type — kicker, headline (swiss), 500+ chip, wordmark
# ===================================================================
# kicker
K.text(c, (72, 70), "THE STACK   ·   FACILITIES   ·   7 JUL 2026",
       K.mono(c, 17, medium=True), INK, anchor="la", tracking=0.18)

# headline — two lines, same size, left rag, calm upper zone
hl1, hl2 = "ONE SIGNATURE,", "FIFTY-YEAR GATE"
hz = min(K.fit_size(c, hl1, 940, lo=60, hi=168, weight=900, opsz=144),
         K.fit_size(c, hl2, 940, lo=60, hi=168, weight=900, opsz=144))
fh = K.fraunces(c, hz, weight=900, opsz=144)
K.text(c, (72, 150), hl1, fh, INK, anchor="la")
K.text(c, (72, 150 + hz * 1.05), hl2, fh, INK, anchor="la")

# 500+ comments chip near the drift
K.chip(c, (72, 902), "500+ PUBLIC COMMENTS", K.mono(c, 16, medium=True),
       CREAM, INK, pad=11, anchor="la", tracking=0.12, radius=7)

# wordmark
K.text(c, (72, 1000), "ALASKA.AI", K.fraunces(c, 30, weight=900, opsz=120), INK, anchor="la")

# ===================================================================
# 10. finishing texture identity: grain + light vignette
# ===================================================================
K.grain(c, amount=6.0, seed=SEED + 40, mono=True)
K.vignette(c, strength=0.12, spread=1.4)

meta = {
    "date": "7 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "FACILITIES",
    "headline": "ONE SIGNATURE / FIFTY-YEAR GATE",
    "byline": "",
    "style_family": "cadastral_ledger",
    "palette": [PAPER, PARCH, INK, GRAPH, VERM, SLATE, GOLD],
    "hue_family": "red",
    "composition": "central_icon",
    "motifs": ["cadastral plat", "consent seal", "comment-mark drift",
               "survey ticks", "north arrow"],
    "technique_stack": ["field", "warp", "hatch", "stipple", "hand_line",
                        "grain", "mottle"],
    "seed": SEED,
    "eval_history": [],
    "eval_final": {},
}
c.finish("out/post_image.png", meta)
print("rendered out/post_image.png")
