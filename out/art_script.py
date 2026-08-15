"""Anchorage Desk — 14 AUG 2026 — bespoke cover.

Concept: a stop-log gate headworks stands across a braided glacial inflow.
Three slot bays stand EMPTY under engraved deck plates reading COLLECTION /
ACCESS / RETENTION; one bay holds a single weathered beam stamped 2023 (the
facial-recognition ban). The flow pours through the gaps. Above the deck a
gantry has craned in the upgrade — an amber module tagged $600,000 — and
stopped: it hangs on its sling, a HELD · AUG 18 tag swinging beneath.

style_family engraved_headworks · hue_family neutral-cool ·
composition frame_within · SEED 818
"""
import sys, math, traceback
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageFilter
from scipy.ndimage import zoom as ndzoom
import art_kit as k

SEED = 818

# ---------------------------------------------------------------- geometry
BAND_TOP   = 300.0      # top of the water plate (hidden under the ridges)
WATERLINE  = 357.0      # visible pool surface
DECK_TOP   = 600.0
DECK_BOT   = 664.0
BAY_BOT    = 946.0
PIER_CX    = [60.0, 300.0, 540.0, 780.0, 1020.0]
PIER_HW    = 27.0
BAYS       = [(87.0, 273.0), (327.0, 513.0), (567.0, 753.0), (807.0, 993.0)]
CLOSED_BAY = 1                                  # index of the 2023 bay
BEAM_TOP, BEAM_BOT = 786.0, 838.0
LOAD       = (553.0, 440.0, 767.0, 548.0)       # x0,y0,x1,y1 — the focal
GANTRY_LX, GANTRY_RX = 478.0, 842.0
HEADBEAM_Y = 366.0


# ---------------------------------------------------------------- helpers
def paste_masked(c, rgb_1080, mask_1080):
    lay = rgb_1080.resize((c.W, c.W), Image.LANCZOS).convert("RGB")
    m = mask_1080.resize((c.W, c.W), Image.LANCZOS)
    c.img.paste(lay, (0, 0), m)
    c.draw = ImageDraw.Draw(c.img, "RGBA")


def rect(c, x0, y0, x1, y1, fill=None, outline=None, width=2, d=None):
    k.poly(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
           fill=fill, outline=outline, width=width, d=d)


def dashed(c, p0, p1, color, width=2, dash=13, gap=9, d=None):
    x0, y0 = p0
    x1, y1 = p1
    ln = math.hypot(x1 - x0, y1 - y0)
    if ln < 1:
        return
    ux, uy = (x1 - x0) / ln, (y1 - y0) / ln
    t = 0.0
    while t < ln:
        a = (x0 + ux * t, y0 + uy * t)
        t2 = min(ln, t + dash)
        k.line(c, [a, (x0 + ux * t2, y0 + uy * t2)], color, width, d=d)
        t += dash + gap


def rect_mask(c, boxes, soft=0):
    m, md = c.mask()
    for (x0, y0, x1, y1) in boxes:
        md.rectangle([c.s(x0), c.s(y0), c.s(x1), c.s(y1)], fill=255)
    if soft:
        m = m.filter(ImageFilter.GaussianBlur(c.s(soft)))
    return m


# ---------------------------------------------------------------- main
def main():
    # ---------- palette (OKLCH; value spine first) ----------
    paper    = k.oklch(0.950, 0.010, 238)
    haze     = k.oklch(0.872, 0.020, 232)
    ridge_f  = k.oklch(0.822, 0.016, 236)
    ridge_n  = k.oklch(0.645, 0.028, 234)
    concrete = k.oklch(0.745, 0.012, 246)
    conc_dk  = k.oklch(0.615, 0.014, 244)
    conc_lt  = k.oklch(0.855, 0.012, 244)
    water_hi = k.oklch(0.775, 0.022, 226)
    water_md = k.oklch(0.680, 0.028, 228)
    water_dk = k.oklch(0.590, 0.032, 230)
    water_dp = k.oklch(0.505, 0.034, 232)
    ink      = k.oklch(0.175, 0.028, 236)
    amber    = k.oklch(0.775, 0.158, 74)
    amber_dp = k.oklch(0.530, 0.140, 56)
    amber_hi = k.oklch(0.905, 0.098, 84)

    c = k.Canvas(bg=haze, ss=2)

    # =========================================================== 1 sky
    k.gradient_v(c, (0, 0, 1080, 372), paper, haze, ease=1.35)
    # thin high cirrus bands — structure, not noise
    rngK = np.random.default_rng(SEED + 30)
    for i in range(11):
        yy = 96 + i * 17 + rngK.uniform(-3, 3)
        x0 = rngK.uniform(-60, 520)
        k.hand_line(c, [(x0, yy), (x0 + rngK.uniform(260, 700), yy)],
                    k.mix(haze, paper, 0.45), width=rngK.uniform(2.0, 5.0),
                    amp=1.2, seed=SEED + 300 + i)
    sm = np.clip(1.0 - np.mgrid[0:1080, 0:1080][0] / 380.0, 0, 1) ** 1.8
    k.stipple(c, Image.fromarray((sm * 255).astype(np.uint8), "L"),
              density=0.16, r=(0.4, 1.05), color=k.mix(haze, ink, 0.16),
              seed=SEED + 2)
    for yy in range(126, 300, 22):                     # survey ticks
        k.line(c, [(1016, yy), (1030 if (yy // 22) % 2 else 1024, yy)],
               k.mix(haze, ink, 0.22), width=1.5)

    # =========================================================== 2 masthead + headline
    kf = k.mono(c, 17, medium=True)
    k.text(c, (80, 54), "ANCHORAGE DESK · MUNICIPAL · 14 AUG 2026", kf,
           k.mix(ink, haze, 0.16), anchor="la", tracking=0.22)
    k.line(c, [(80, 86), (1000, 86)], k.mix(ink, haze, 0.58), width=1.5)

    H1, H2 = "Anchorage Code Can’t Answer", "What The Cameras Collect"
    hs = k.fit_size(c, H1, 918, lo=40, hi=74, weight=900, opsz=144)
    hf = k.fraunces(c, hs, weight=900, opsz=144)
    hcol = k.ensure_contrast(ink, paper)
    k.text(c, (80, 108), H1, hf, hcol, anchor="la")
    k.text(c, (80, 108 + hs * 1.04), H2, hf, hcol, anchor="la")

    # =========================================================== 3 water plate
    # MACRO: the pool, backed up against the gate — light at the inflow,
    # deep and still where it is held.
    k.gradient_v(c, (0, BAND_TOP, 1080, DECK_TOP), water_hi, water_dp,
                 ease=1.10)

    ys, xs = np.mgrid[0:1080, 0:1080]
    # MESO: the braided inflow, confined to a narrow strip below the ridges.
    # Genuinely anisotropic: take a shallow slice of an isotropic field and
    # stretch it 10x vertically, so channels are long and narrow.
    f0 = k.field(scale=16.0, octaves=3, seed=SEED + 1, w=1080, h=1080)[0:108, :]
    fv = ndzoom(f0, (10.0, 1.0), order=3)[:1080, :1080]
    fv = k.warp(fv, strength=22.0, scale=7.0, seed=SEED + 3)
    t = np.clip((ys - WATERLINE) / (DECK_TOP - WATERLINE), 0, 1)
    xsrc = np.clip(540 + (xs - 540) / (1.0 - 0.22 * t), 0, 1079).astype(int)
    fv = fv[ys, xsrc]
    fv = (fv - fv.min()) / (fv.max() - fv.min() + 1e-9)
    q = np.digitize(fv, [0.40, 0.58])
    lut = np.array([k.hex_to_rgb(x) for x in (water_dk, water_md, water_hi)],
                   np.uint8)
    bm = (np.clip((452 - ys) / 26.0, 0, 1)
          * (ys > BAND_TOP) * 255).astype(np.uint8)
    paste_masked(c, Image.fromarray(lut[q], "RGB"), Image.fromarray(bm, "L"))

    # MICRO: inflow threads — this is what makes the water read as feeds
    ang = (math.pi / 2
           + (540 - xs.astype(float)) / 540.0 * 0.30
           + (k.field(4.0, 3, SEED + 5) - 0.5) * 0.24)
    lines = k.streamlines(ang, n=260, step=3.0, length=(70, 150),
                          seed=SEED + 6, margin=0.03)
    lay, ld = c.layer()
    rngL = np.random.default_rng(SEED + 7)
    for pl in lines:
        pl = [p for p in pl if WATERLINE - 4 < p[1] < 500]
        if len(pl) < 5:
            continue
        ld.line(c.pts(pl), fill=(*k.hex_to_rgb(water_hi),
                                 int(rngL.uniform(65, 125))),
                width=max(1, int(c.s(rngL.uniform(0.8, 1.5)))), joint="curve")
    thr = (np.clip((494 - ys) / 80.0, 0, 1)
           * (ys > WATERLINE - 4) * 255).astype(np.uint8)
    lay.putalpha(ImageChops.multiply(
        lay.getchannel("A"), Image.fromarray(thr, "L").resize((c.W, c.W))))
    c.composite(lay)

    # gravel bars between the upper channels
    gb = ((fv > 0.72) & (ys > WATERLINE) & (ys < 444)).astype(np.uint8) * 255
    k.stipple(c, Image.fromarray(gb, "L"), density=0.34, r=(0.5, 1.4),
              color=k.mix(water_hi, paper, 0.45), seed=SEED + 8)
    k.chips(c, 60, (40, WATERLINE + 6, 1040, 442), size=(1.6, 3.8),
            colors=(paper, water_hi, water_dk), seed=SEED + 9,
            mask_img=Image.fromarray(gb, "L"))

    # slack-water: a graded ripple system, tighter as it nears the gate
    rngR = np.random.default_rng(SEED + 10)
    for i in range(78):
        u = i / 77.0
        yy = 436 + (u ** 0.78) * 162 + rngR.uniform(-0.8, 0.8)
        x0 = rngR.uniform(-70, 520)
        x1 = x0 + rngR.uniform(180, 660)
        pale = (i % 3 == 0)
        k.hand_line(c, [(x0, yy), ((x0 + x1) / 2, yy + rngR.uniform(-1.2, 1.2)),
                        (min(1076, x1), yy)],
                    k.mix(water_hi, paper, 0.34) if pale else
                    k.mix(water_dp, ink, 0.16),
                    width=1.25 if pale else 1.5, amp=0.8, seed=SEED + 40 + i)
    # draw-down: the surface dips into each bay mouth (short, at the sill only)
    for (bx0, bx1) in BAYS:
        bcx = (bx0 + bx1) / 2
        for j in (-56, -19, 19, 56):
            k.hand_line(c, [(bcx + j * 1.35, 572), (bcx + j * 1.0, DECK_TOP - 1)],
                        k.mix(water_dp, ink, 0.22), width=1.5, amp=0.7,
                        seed=SEED + 80 + int(bcx) + j)

    # =========================================================== 4 ridges (over the type)
    far = k.ridge_pts(312, 68, scale=2.6, octaves=5, seed=SEED + 11, step=3)
    k.poly(c, [(far[0][0], 360)] + far + [(far[-1][0], 360)], fill=ridge_f)
    fm, fmd = c.mask()
    fmd.polygon(c.pts([(far[0][0], 360)] + far + [(far[-1][0], 360)]), fill=255)
    rngS = np.random.default_rng(SEED + 12)
    snow, sd2 = c.layer()
    for i in range(15):
        px, py = rngS.uniform(30, 1050), rngS.uniform(268, 344)
        pts = k.blob_pts(px, py, rngS.uniform(10, 27), wobble=0.44,
                         harmonics=(1, 2, 3, 5), points=44, seed=SEED + 60 + i)
        sd2.polygon(c.pts(pts), fill=(*k.hex_to_rgb(paper), 185))
    snow.putalpha(ImageChops.multiply(snow.getchannel("A"), fm))
    c.composite(snow)
    k.hatch(c, fm, spacing=13, angle=68, color=k.mix(ridge_f, ink, 0.22),
            width=1.0)
    k.line(c, far, k.mix(ridge_f, ink, 0.32), width=2)

    near = k.ridge_pts(340, 38, scale=3.4, octaves=5, seed=SEED + 13, step=3)
    k.poly(c, [(near[0][0], 360)] + near + [(near[-1][0], 360)], fill=ridge_n)
    nm, nmd = c.mask()
    nmd.polygon(c.pts([(near[0][0], 360)] + near + [(near[-1][0], 360)]),
                fill=255)
    k.hatch(c, nm, spacing=10, angle=-62, color=k.mix(ridge_n, ink, 0.32),
            width=1.1)
    k.line(c, near, k.mix(ridge_n, ink, 0.42), width=2)
    k.line(c, [(0, WATERLINE + 1), (1080, WATERLINE + 1)],
           k.mix(ink, water_md, 0.42), width=2)
    rect(c, 0, WATERLINE + 2, 1080, WATERLINE + 8,
         fill=k.mix(water_hi, paper, 0.40))

    # =========================================================== 5 inflow gauge
    lab = k.mono(c, 15, medium=True)
    bc = k.mix(ink, water_dp, 0.12)
    k.line(c, [(72, 388), (392, 388)], bc, width=1.8)
    k.line(c, [(72, 381), (72, 401)], bc, width=1.8)
    k.line(c, [(392, 381), (392, 401)], bc, width=1.8)
    k.chip(c, (232, 396), "750 FEEDS", lab, ink, k.mix(paper, water_hi, 0.28),
           pad=9, anchor="ma", tracking=0.18, radius=3)

    # =========================================================== 6 bays + curtains
    bay_dark = k.mix(ink, water_dp, 0.08)
    # the bays are dark apertures: their water sits BELOW the focal in value
    fall_hi = k.mix(water_hi, paper, 0.30)
    fall_md = k.mix(water_md, ink, 0.06)
    fall_lo = k.mix(water_dk, ink, 0.20)
    for i, (bx0, bx1) in enumerate(BAYS):
        closed = (i == CLOSED_BAY)
        rect(c, bx0, DECK_BOT - 4, bx1, BAY_BOT, fill=bay_dark)
        k.gradient_v(c, (bx0, DECK_BOT - 4, bx1, BAY_BOT), bay_dark,
                     k.mix(bay_dark, water_dk, 0.38))
        rngC = np.random.default_rng(SEED + 100 + i)
        n = 20 if closed else (44 if i != 2 else 36)
        stop = BEAM_TOP if closed else BAY_BOT
        for j in range(n):
            x = rngC.uniform(bx0 + 6, bx1 - 6)
            y0 = DECK_BOT + rngC.uniform(0, 20)
            y1 = stop - rngC.uniform(0, 40 if not closed else 6)
            if y1 - y0 < 30:
                continue
            pts = [(x + math.sin(j * 0.8 + s * 0.55) * rngC.uniform(0.8, 2.2),
                    y0 + (y1 - y0) * s / 9.0) for s in range(10)]
            col = (fall_hi if rngC.random() < 0.16 else
                   (fall_md if rngC.random() < 0.55 else fall_lo))
            k.line(c, pts, col, width=rngC.uniform(1.3, 3.6))
        rect(c, bx0, DECK_BOT - 3, bx1, DECK_BOT + 4,
             fill=k.mix(water_hi, paper, 0.18))
        if closed:
            # the beam checks the flow; below it the bay runs dark and quiet
            k.chips(c, 44, (bx0 + 4, BEAM_TOP - 30, bx1 - 4, BEAM_TOP + 4),
                    size=(2.0, 6.4), colors=(fall_hi, fall_md, fall_lo),
                    seed=SEED + 121)
            rect(c, bx0, BEAM_BOT, bx1, BAY_BOT, fill=k.mix(ink, water_dp, 0.06))
            cm = rect_mask(c, [(bx0, BEAM_BOT, bx1, BAY_BOT)])
            k.hatch(c, cm, spacing=11, angle=-72,
                    color=k.mix(ink, water_dp, 0.30), width=1.0)
            for tx in (bx0 + 58, bx0 + 122):     # a thin seep past the seal
                k.line(c, [(tx, BEAM_BOT), (tx + 3, BAY_BOT - 6)],
                       k.mix(water_md, ink, 0.28), width=2)
        else:
            k.chips(c, 60, (bx0 + 4, BAY_BOT - 34, bx1 - 4, BAY_BOT + 16),
                    size=(2.0, 6.0), colors=(fall_hi, fall_md, fall_lo),
                    seed=SEED + 120 + i)

    # the one beam that exists: 2023
    b0, b1 = BAYS[CLOSED_BAY]
    rect(c, b0 - 15, BEAM_TOP, b1 + 15, BEAM_BOT, fill=k.mix(ink, conc_dk, 0.52))
    rect(c, b0 - 15, BEAM_TOP, b1 + 15, BEAM_TOP + 8,
         fill=k.mix(conc_dk, ink, 0.22))
    rect(c, b0 - 15, BEAM_BOT - 7, b1 + 15, BEAM_BOT, fill=ink)
    bmk = rect_mask(c, [(b0 - 15, BEAM_TOP + 8, b1 + 15, BEAM_BOT - 7)])
    k.hatch(c, bmk, spacing=6, angle=0, color=k.mix(ink, conc_dk, 0.28),
            width=0.9)
    k.text(c, ((b0 + b1) / 2, (BEAM_TOP + BEAM_BOT) / 2 + 1), "2023",
           k.mono(c, 20, medium=True), k.mix(paper, conc_dk, 0.18),
           anchor="mm", tracking=0.24)
    for xx in np.arange(b0 - 6, b1 + 12, 32):
        k.circle(c, xx, BEAM_TOP + 4, 2.4, fill=k.mix(conc_dk, paper, 0.35))

    # =========================================================== 7 piers
    pier_boxes = [(cx - PIER_HW, DECK_BOT - 6, cx + PIER_HW, 1080)
                  for cx in PIER_CX]
    for (x0, y0, x1, y1) in pier_boxes:
        rect(c, x0, y0, x1, y1, fill=conc_dk)
        rect(c, x0, y0, x0 + 9, y1, fill=k.mix(concrete, paper, 0.18))
        rect(c, x1 - 7, y0, x1, y1, fill=k.mix(ink, conc_dk, 0.55))
    pm = rect_mask(c, [(b[0] + 9, b[1], b[2] - 7, b[3]) for b in pier_boxes])
    k.hatch(c, pm, spacing=10, angle=-72, color=k.mix(conc_dk, ink, 0.32),
            width=1.0)
    k.stipple(c, pm, density=0.24, r=(0.5, 1.3), color=k.mix(conc_dk, ink, 0.2),
              seed=SEED + 15)
    for (x0, y0, x1, y1) in pier_boxes:
        rect(c, x0, 900, x1, 946, fill=k.mix(conc_dk, ink, 0.34))
        k.hand_line(c, [(x0, 900), (x1, 901)], k.mix(ink, conc_dk, 0.4),
                    width=2, amp=1.4, seed=SEED + 16)
        for yy in (706, 772, 838):
            k.line(c, [(x0, yy), (x1, yy)], k.mix(conc_dk, ink, 0.22),
                   width=1.4)

    # stop-log slot grooves — the empty sockets
    for (bx0, bx1) in BAYS:
        for gx in (bx0 + 4, bx0 + 13, bx1 - 13, bx1 - 4):
            rect(c, gx - 2.5, DECK_BOT + 2, gx + 2.5, BAY_BOT,
                 fill=k.mix(ink, water_dp, 0.42))
        rect(c, bx0 + 6.5, DECK_BOT + 2, bx0 + 10.5, BAY_BOT,
             fill=k.mix(concrete, ink, 0.30))
        rect(c, bx1 - 10.5, DECK_BOT + 2, bx1 - 6.5, BAY_BOT,
             fill=k.mix(concrete, ink, 0.30))

    # =========================================================== 8 tailwater apron
    rect(c, 0, BAY_BOT, 1080, 1080, fill=water_dk)
    k.gradient_v(c, (0, BAY_BOT, 1080, 1080), k.mix(water_dp, ink, 0.56),
                 k.mix(water_md, ink, 0.14), ease=0.75)
    k.line(c, [(0, BAY_BOT), (1080, BAY_BOT)], ink, width=3)   # apron sill
    rngT = np.random.default_rng(SEED + 17)
    for i in range(30):                                        # standing waves
        yy = 958 + rngT.uniform(0, 112)
        x0 = rngT.uniform(-60, 880)
        x1 = x0 + rngT.uniform(150, 520)
        k.hand_line(c, [(x0, yy), ((x0 + x1) / 2, yy - rngT.uniform(1, 6)),
                        (x1, yy)],
                    k.mix(water_md, paper, 0.20) if i % 2 else
                    k.mix(water_dp, ink, 0.34),
                    width=rngT.uniform(1.3, 3.0), amp=1.7, seed=SEED + 200 + i)
    tm = rect_mask(c, [(0, BAY_BOT + 2, 1080, 1080)])
    k.stipple(c, tm, density=0.30, r=(0.5, 1.4),
              color=k.mix(water_md, paper, 0.28), seed=SEED + 18)
    for (bx0, bx1) in BAYS:
        k.chips(c, 42, (bx0, BAY_BOT - 4, bx1, BAY_BOT + 44), size=(2.2, 7.0),
                colors=(fall_hi, fall_md, fall_lo), seed=SEED + 19 + int(bx0))

    # =========================================================== 9 deck slab
    rect(c, 0, DECK_TOP, 1080, DECK_BOT, fill=concrete)
    rect(c, 0, DECK_TOP, 1080, DECK_TOP + 9, fill=conc_lt)
    rect(c, 0, DECK_BOT - 11, 1080, DECK_BOT, fill=k.mix(ink, conc_dk, 0.58))
    dm = rect_mask(c, [(0, DECK_TOP + 9, 1080, DECK_BOT - 11)])
    k.stipple(c, dm, density=0.22, r=(0.4, 1.1), color=k.mix(conc_dk, ink, 0.3),
              seed=SEED + 21)
    for xx in np.arange(14, 1080, 27):
        k.circle(c, xx, DECK_TOP + 14, 2.3, fill=k.mix(conc_dk, ink, 0.38))
        k.circle(c, xx, DECK_BOT - 16, 2.3, fill=k.mix(conc_dk, ink, 0.38))
    k.line(c, [(0, DECK_TOP + 9), (1080, DECK_TOP + 9)],
           k.mix(conc_dk, ink, 0.30), width=1.6)

    plates = ["COLLECTION", "FACIAL REC.", "ACCESS", "RETENTION"]
    pf = k.mono(c, 15, medium=True)
    for i, (bx0, bx1) in enumerate(BAYS):
        cx = (bx0 + bx1) / 2
        w = k.measure(c, plates[i], pf, 0.14)
        px0, px1 = cx - w / 2 - 11, cx + w / 2 + 11
        if i == CLOSED_BAY:
            c.draw.rounded_rectangle(
                [c.s(px0), c.s(624), c.s(px1), c.s(648)], radius=c.s(3),
                fill=(*k.hex_to_rgb(ink), 255))
            k.text(c, (cx, 636), plates[i], pf, conc_lt, anchor="mm",
                   tracking=0.14)
        else:
            c.draw.rounded_rectangle(
                [c.s(px0), c.s(624), c.s(px1), c.s(648)], radius=c.s(3),
                fill=(*k.hex_to_rgb(k.mix(concrete, ink, 0.14)), 255),
                outline=(*k.hex_to_rgb(k.mix(ink, concrete, 0.28)), 255),
                width=int(c.s(1.6)))
            k.text(c, (cx, 636), plates[i], pf,
                   k.mix(ink, concrete, 0.20), anchor="mm", tracking=0.14)

    for (rx0, rx1) in ((6, 430), (890, 1074)):        # rails, outer thirds only
        k.line(c, [(rx0, 578), (rx1, 578)], k.mix(conc_dk, ink, 0.42), width=2)
        k.line(c, [(rx0, 590), (rx1, 590)], k.mix(conc_dk, ink, 0.35), width=1.6)
        for xx in np.arange(rx0 + 6, rx1, 34):
            k.line(c, [(xx, 576), (xx, DECK_TOP)], k.mix(conc_dk, ink, 0.42),
                   width=2)

    # =========================================================== 10 gantry
    gcol = k.mix(concrete, ink, 0.20)
    gdk = k.mix(ink, concrete, 0.26)
    for lx in (GANTRY_LX, GANTRY_RX):
        rect(c, lx - 13, HEADBEAM_Y, lx + 13, DECK_TOP, fill=gcol,
             outline=gdk, width=2)
        for yy in np.arange(HEADBEAM_Y + 8, DECK_TOP - 6, 30):
            k.line(c, [(lx - 12, yy), (lx + 12, yy + 26)], gdk, width=1.6)
            k.line(c, [(lx + 12, yy), (lx - 12, yy + 26)], gdk, width=1.6)
        k.poly(c, [(lx - 32, DECK_TOP), (lx - 13, DECK_TOP - 24),
                   (lx - 13, DECK_TOP)], fill=gdk)
        k.poly(c, [(lx + 32, DECK_TOP), (lx + 13, DECK_TOP - 24),
                   (lx + 13, DECK_TOP)], fill=gdk)
    rect(c, 446, HEADBEAM_Y, 874, HEADBEAM_Y + 7, fill=gdk)
    rect(c, 446, HEADBEAM_Y + 17, 874, HEADBEAM_Y + 24, fill=gdk)
    for xx in np.arange(446, 872, 26):
        k.line(c, [(xx, HEADBEAM_Y + 7), (xx + 13, HEADBEAM_Y + 17)], gdk,
               width=1.8)
        k.line(c, [(xx + 13, HEADBEAM_Y + 17), (xx + 26, HEADBEAM_Y + 7)], gdk,
               width=1.8)
    rect(c, 636, HEADBEAM_Y - 16, 684, HEADBEAM_Y + 2, fill=gcol,
         outline=gdk, width=2)
    k.circle(c, 646, HEADBEAM_Y + 3, 5, fill=gdk)
    k.circle(c, 674, HEADBEAM_Y + 3, 5, fill=gdk)

    # ============================================== 11 the held load (FOCAL)
    lx0, ly0, lx1, ly1 = LOAD
    lcx = (lx0 + lx1) / 2
    k.glow(c, lcx, ly1 + 40, 176, ink, alpha=58)
    k.glow(c, lcx, (ly0 + ly1) / 2, 210, amber, alpha=38)
    # its reflection on the slack water below
    refl, rd = c.layer()
    rd.rectangle([c.s(lx0 + 24), c.s(566), c.s(lx1 - 24), c.s(DECK_TOP - 2)],
                 fill=(*k.hex_to_rgb(amber), 62))
    refl = refl.filter(ImageFilter.GaussianBlur(c.s(11)))
    c.composite(refl)

    # hook block -> a wide angled sling -> shackles: a crane load, mid-lift
    k.line(c, [(660, HEADBEAM_Y + 24), (660, 396)], gdk, width=3)
    rect(c, 646, 394, 674, 412, fill=gdk)
    sk_l, sk_r = lx0 + 16, lx1 - 16
    k.line(c, [(660, 412), (sk_l, ly0 - 6)], ink, width=3)
    k.line(c, [(660, 412), (sk_r, ly0 - 6)], ink, width=3)

    rect(c, lx0, ly0, lx1, ly1, fill=amber)
    rect(c, lx0, ly0, lx1, ly0 + 15, fill=amber_hi)          # lit top deck
    rect(c, lx0, ly1 - 13, lx1, ly1, fill=amber_dp)          # shadowed plinth
    rect(c, lx1 - 17, ly0, lx1, ly1, fill=k.mix(amber, amber_dp, 0.55))
    lm = rect_mask(c, [(lx0, ly0 + 15, lx1 - 17, ly1 - 13)])
    k.hatch(c, lm, spacing=11, angle=-58, color=k.mix(amber, amber_dp, 0.36),
            width=0.9)
    k.line(c, [(lx0, ly0 + 15), (lx1, ly0 + 15)], ink, width=2)
    # asymmetric equipment face: stencil plate left, louvred bay right
    DIV = lx0 + 105
    rect(c, DIV, ly0, DIV + 6, ly1, fill=ink)
    for i in range(7):                                        # louvre slots
        yy = ly0 + 30 + i * 9.5
        k.line(c, [(DIV + 14, yy), (lx1 - 24, yy)], k.mix(ink, amber_dp, 0.18),
               width=3)
    for (cx0, cy0) in ((lx0, ly0), (lx1 - 21, ly0), (lx0, ly1 - 16),
                       (lx1 - 21, ly1 - 16)):                  # corner castings
        rect(c, cx0, cy0, cx0 + 21, cy0 + 16, fill=ink)
    rect(c, lx0, ly0, lx1, ly1, outline=ink, width=3)
    for sx in (sk_l, sk_r):                                    # shackles
        k.circle(c, sx, ly0 - 4, 7.5, outline=ink, width=3)
        rect(c, sx - 4, ly0 - 2, sx + 4, ly0 + 4, fill=ink)
    k.chip(c, ((lx0 + DIV) / 2, 497), "$600,000", k.mono(c, 15, medium=True),
           ink, amber_hi, pad=7, anchor="mm", tracking=0.04, radius=3)

    # the hold tag: wired to the load's underside, swung out into the gap.
    # Pale, not amber — the load keeps the chroma monopoly.
    tf = k.mono(c, 15, medium=True)
    tw = k.measure(c, "HELD · AUG 18", tf, 0.14)
    ax = lx0 + 54                                   # eyelet, right end of tag
    ty0, ty1 = ly1 + 10, ly1 + 40
    tx1, tx0 = ax + 14, ax - 16 - tw - 14
    k.hand_line(c, [(ax, ly1 - 2), (ax, ty0 + 3)], ink, width=2, amp=0.8,
                seed=SEED + 22)
    k.poly(c, [(tx0 + 15, ty0), (tx1, ty0), (tx1, ty1), (tx0 + 15, ty1),
               (tx0, (ty0 + ty1) / 2)], fill=conc_lt, outline=ink, width=2)
    k.poly(c, [(tx0 + 15, ty0), (tx1, ty0), (tx1, ty0 + 5), (tx0 + 15, ty0 + 5),
               (tx0 + 8, ty0 + 3)], fill=amber_dp)
    k.circle(c, ax, (ty0 + ty1) / 2, 4, fill=ink)
    k.text(c, (tx0 + 22, (ty0 + ty1) / 2 + 1), "HELD · AUG 18", tf, ink,
           anchor="lm", tracking=0.14)

    # =========================================================== 12 finish
    k.grain(c, amount=5.5, seed=SEED)
    k.vignette(c, strength=0.14, spread=1.45)

    wf = k.fraunces(c, 28, weight=900, opsz=40)
    k.chip(c, (86, 1016), "ALASKA.AI", wf, paper, ink, pad=12, anchor="ls",
           radius=5)
    k.polaris(c, 996, 62, r=13, color=amber, core=amber_hi)

    meta = {
        "date": "14 AUG 2026",
        "column": "Anchorage Desk",
        "kicker": "ANCHORAGE DESK",
        "middle_slot": "MUNICIPAL",
        "headline": "Anchorage Code Can’t Answer / What The Cameras Collect",
        "byline": "",
        "style_family": "engraved_headworks",
        "palette": [paper, haze, ridge_f, concrete, water_md, ink, amber],
        "hue_family": "neutral-cool",
        "composition": "frame_within",
        "motifs": ["stop-log gate headworks", "three empty slot bays",
                   "suspended crane load (the withheld contract)",
                   "single seated 2023 beam", "braided glacial inflow",
                   "Chugach ridgeline"],
        "technique_stack": ["gradient_v", "field", "warp", "streamlines",
                            "ridge_pts", "hatch", "stipple", "chips",
                            "hand_line", "glow", "grain", "vignette"],
        "seed": SEED,
        "eval_history": EVAL_HISTORY,
        "eval_final": EVAL_FINAL,
    }
    c.finish("out/post_image.png", meta)
    print("rendered out/post_image.png")


EVAL_HISTORY = [
    {"iter": 1, "weighted": 6.51, "weakest": "typography",
     "note": "far ridge sliced headline line 2 in half; posterized water read "
            "as camouflage blobs with rain-like threads over it; gantry legs "
            "caged the focal; 750 FEEDS label dark-on-dark"},
    {"iter": 2, "weighted": 7.77, "weakest": "color",
     "note": "headline, gantry air and the closed bay all fixed; water still "
            "camouflage-blobbed (the field stretch cancelled itself out), "
            "ridges too close in value, HELD tag collided with the deck"},
    {"iter": 3, "weighted": 8.07, "weakest": "craft",
     "note": "water fixed (true anisotropic braid strip over a graded slack "
            "pool); but the draw-down current lines read as scratches, the "
            "tag's eyelet was drawn on top of its own last glyph, and the "
            "load read as a suitcase rather than slung freight"},
    {"iter": 4, "weighted": 8.26, "weakest": "color",
     "note": "scratches, tag eyelet and the suitcase read all fixed (spreader "
            "bar + lifting slings); grayscale check showed the white flow "
            "curtains out-punching the amber focal, and the sling had no "
            "visible air between spreader and load"},
    {"iter": 5, "weighted": 8.30, "weakest": "craft",
     "note": "bays now read as dark apertures and the amber focal wins the "
            "grayscale check; but the spreader bar spanning the load read as "
            "a canopy/roof — the assembly looked like a shelter, not a lift"},
    {"iter": 6, "weighted": 8.58, "weakest": "typography",
     "note": "spreader replaced with a wide angled sling to two shackles and "
            "the load given an asymmetric equipment face (stencil plate left, "
            "louvred bay right) — reads as slung freight mid-lift. Ships."},
]
EVAL_FINAL = {
    "weighted": 8.58,
    "scores": {"concept": 8.5, "focal": 9, "composition": 8.5, "color": 8.5,
               "detail": 8.5, "craft": 8.5, "typography": 8, "originality": 9,
               "fidelity": 9},
    "weakest": "typography",
    "note": "Headline is poster-scale and cleanly legible but sits on the sky "
           "rather than interlocking with the terrain; the planned ridge/"
           "baseline overlap was abandoned in iteration 2 because it was "
           "destroying line 2. Legibility was the right trade.",
}

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
