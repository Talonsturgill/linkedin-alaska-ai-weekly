"""The Stack — 2026-07-31 — bespoke cover.

Concept: THE TEMPORARY SPAN. A small lit clinic stands on a high ice
terrace above a ravine. The only way across is a slender timber catwalk
held up by three props. The fourth prop socket is empty, a broken stub
over open dark. The catwalk is the FY2027 waiver; the props are the
funding years already covered; the empty socket is FY2028, the decision
that moves to one Bureau division and off any public agenda.

Style: ukiyo_bokashi (flat planes, fine outlines, smooth banded sky)
with a fine engraved micro pass. Palette: winter dusk magenta over cold
blue snow, one warm lamp as the single focal accent.
"""

import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as ak  # noqa: E402

SEED = 731
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- palette
PAPER = "#f4e7e3"   # lit snow, headline knockout
SKY_LO = "#f2a98f"  # warm horizon band
SKY_MD = "#b0587f"  # magenta dusk
SKY_HI = "#5a3a63"  # plum
SNOW = "#6a6f96"    # cold terrace plane
ICE = "#22243a"     # deep ice, silhouettes, type
LAMP = "#ffb347"    # clinic lamp, polaris — THE focal accent
PALETTE = [PAPER, SKY_LO, SKY_MD, SKY_HI, SNOW, ICE, LAMP]

HEADLINE = ["ONE BUREAU SETS", "ALASKA’S HEALTH", "CIRCUIT PRICES"]
KICKER = "THE STACK  ·  REGULATORY  ·  31 JUL 2026"

c = ak.Canvas(bg=SKY_HI, ss=2)


def poly_mask(pts):
    """L mask from a design-space point list."""
    m, md = c.mask()
    md.polygon(c.pts(pts), fill=255)
    return m


def rect_mask(box):
    m, md = c.mask()
    md.rectangle([c.s(box[0]), c.s(box[1]), c.s(box[2]), c.s(box[3])],
                 fill=255)
    return m


# ============================================================ 1. sky bokashi
ak.gradient_v(c, [0, 0, 1080, 430], SKY_HI, SKY_MD, ease=1.15)
ak.gradient_v(c, [0, 430, 1080, 712], SKY_MD, SKY_LO, ease=0.80)

# stars in the plum upper band
for _ in range(90):
    x, y = rng.uniform(0, 1080), rng.uniform(10, 330)
    r = rng.uniform(0.7, 1.7)
    fade = 1.0 - (y / 330.0)
    if rng.random() < 0.25 + 0.6 * fade:
        ak.circle(c, x, y, r, fill=ak.mix(SKY_HI, PAPER, 0.35 + 0.5 * fade))

# soft cloud banding — the bokashi signature, and it stops the mid-sky
# from reading as dead gradient
for i, (cy_, hh, al) in enumerate([(372, 15, 30), (438, 11, 26),
                                   (486, 20, 34), (546, 9, 22)]):
    lay_c, ld_c = c.layer()
    pts_c = ak.ridge_pts(cy_, hh, scale=1.5, octaves=2, seed=SEED + 80 + i,
                         x0=-40, x1=1120, step=8)
    ld_c.polygon(c.pts(pts_c + [(1120, cy_ + hh + 26), (-40, cy_ + hh + 26)]),
                 fill=(*ak.hex_to_rgb(ak.mix(SKY_LO, PAPER, 0.30)), al))
    lay_c = lay_c.filter(ak.ImageFilter.GaussianBlur(c.s(9)))
    c.composite(lay_c)

ak.mottle(c, strength=0.035, scale=3.0, seed=SEED + 4)

# colophon
ak.polaris(c, 952, 128, r=13, color=LAMP, halo=0.0)

# ====================================================== 2. far ridge (haze)
far = ak.mix(SKY_LO, ICE, 0.42)
ak.ridge_fill(c, 622, 44, far, scale=2.6, octaves=4, seed=SEED + 1,
              bottom=1080)
mid = ak.mix(SKY_LO, ICE, 0.62)
ak.ridge_fill(c, 652, 26, mid, scale=4.0, octaves=3, seed=SEED + 2,
              bottom=1080)

# ==================================== 3. the ravine and the two cliffs
RAV_L, RAV_R = 296.0, 806.0
LO_TOP, HI_TOP = 838.0, 706.0
FLOOR = 1042.0

# --- canyon interior: a slot of dark that deepens downward -------------
canyon = [(RAV_L, LO_TOP), (RAV_R, HI_TOP), (RAV_R, 1080), (RAV_L, 1080)]
cmask = poly_mask(canyon)
lay, ld = c.layer()
top_c = ak.mix(ICE, SKY_LO, 0.26)
for i in range(int(HI_TOP) - 6, 1081):
    t = np.clip((i - (HI_TOP - 6)) / (FLOOR - HI_TOP + 60), 0, 1) ** 0.72
    col = ak.mix(top_c, ak.darken(ICE, 0.72), float(t))
    ld.rectangle([c.s(RAV_L - 4), c.s(i), c.s(RAV_R + 4), c.s(i + 1)],
                 fill=(*ak.hex_to_rgb(col), 255))
c.img.paste(lay, (0, 0), ak.Image.composite(
    cmask, ak.Image.new("L", (c.W, c.W), 0), lay.getchannel("A")))
c.draw = ak.ImageDraw.Draw(c.img, "RGBA")

# strata in the far wall — depth cues, fading as they drop
for i in range(11):
    yy = HI_TOP + 34 + i * 30 + rng.uniform(-5, 5)
    fade = 1.0 - i / 11.0
    ak.line(c, [(RAV_L + 6, yy + 26), (RAV_R - 6, yy)],
            ak.mix(ak.darken(ICE, 0.5), top_c, 0.30 * fade), width=1.5)
ak.stipple(c, cmask, density=0.05, r=(0.4, 1.1),
           color=ak.mix(ICE, SKY_LO, 0.42), seed=SEED + 7)

# ravine floor, snow-lit, so the props have something to stand on
ak.poly(c, [(RAV_L, FLOOR + 16), (RAV_R, FLOOR - 4),
            (RAV_R, 1080), (RAV_L, 1080)], fill=ak.mix(ICE, SNOW, 0.30))
ak.chips(c, 34, (RAV_L + 6, FLOOR - 6, RAV_R - 6, 1072), size=(2, 6),
         colors=(ak.mix(SNOW, PAPER, 0.4), SNOW), seed=SEED + 33)
# cold mist pooling in the bottom of the slot
ak.glow(c, (RAV_L + RAV_R) / 2, FLOOR + 10, 196,
        ak.mix(SKY_MD, PAPER, 0.34), alpha=52)


def cliff(x0, x1, y_top, seed, cells, tone=0.42, snow_h=52):
    """A solid snow-capped ice cliff: lit slab cap over a fractured face.

    The face is built from elongated ice blocks and irregular cracks, not
    from ruled hatching, which reads as corduroy at this scale."""
    top_pts = ak.ridge_pts(y_top, 11, scale=2.3, octaves=3, seed=seed,
                           x0=x0, x1=x1, step=4)
    body = [(x0, 1080)] + top_pts + [(x1, 1080)]
    face_base = ak.mix(ICE, SNOW, tone)
    ak.poly(c, body, fill=face_base)
    bmask = poly_mask(body)

    # value falls off downward so the mass has air in it
    lay0, ld0 = c.layer()
    for i in range(int(y_top), 1081):
        t = np.clip((i - y_top) / (1080 - y_top), 0, 1) ** 0.9
        col = ak.mix(face_base, ak.darken(ICE, 0.34), float(t) * 0.85)
        ld0.rectangle([c.s(x0), c.s(i), c.s(x1), c.s(i + 1)],
                      fill=(*ak.hex_to_rgb(col), 255))
    c.img.paste(lay0, (0, 0), ak.Image.composite(
        bmask, ak.Image.new("L", (c.W, c.W), 0), lay0.getchannel("A")))
    c.draw = ak.ImageDraw.Draw(c.img, "RGBA")

    # meso: elongated ice blocks across the face
    lay1, ld1 = c.layer()
    fbox = (x0 - 6, y_top + snow_h - 14, x1 + 6, 1086)
    for cell in ak.voronoi_polys(n=cells, seed=seed + 17, bbox=fbox, relax=1):
        cy = sum(p[1] for p in cell) / len(cell)
        depth = float(np.clip((cy - y_top) / (1080 - y_top), 0, 1))
        j = float(np.clip(rng.normal(0.5, 0.16), 0.05, 0.95))
        col = ak.mix(face_base, ak.darken(ICE, 0.34), depth * 0.85)
        col = ak.mix(col, ak.lighten(col, 0.16), j)
        ld1.polygon(c.pts(cell), fill=(*ak.hex_to_rgb(col), 255),
                    outline=(*ak.hex_to_rgb(ak.darken(ICE, 0.42)), 70),
                    width=max(1, int(c.s(0.8))))
    c.img.paste(lay1, (0, 0), ak.Image.composite(
        bmask, ak.Image.new("L", (c.W, c.W), 0), lay1.getchannel("A")))
    c.draw = ak.ImageDraw.Draw(c.img, "RGBA")

    # micro: irregular vertical fracture lines, never evenly spaced
    lay2, ld2 = c.layer()
    xx = x0 + rng.uniform(6, 26)
    while xx < x1 - 6:
        y_a = y_top + snow_h + rng.uniform(-6, 30)
        y_b = min(1080, y_a + rng.uniform(90, 420))
        pts = [(xx + rng.uniform(-2, 2), y)
               for y in np.linspace(y_a, y_b, 7)]
        shade = ak.darken(ICE, rng.uniform(0.22, 0.48))
        ak.line(c, ak.wobble_pts(pts, amp=1.6, seed=int(xx) + seed),
                shade, width=float(rng.uniform(0.9, 2.0)), d=ld2)
        xx += rng.uniform(26, 78)
    c.img.paste(lay2, (0, 0), ak.Image.composite(
        bmask, ak.Image.new("L", (c.W, c.W), 0), lay2.getchannel("A")))
    c.draw = ak.ImageDraw.Draw(c.img, "RGBA")

    # horizontal bedding, stronger near the top where light rakes it
    for i in range(9):
        yy = y_top + snow_h + 22 + i * 40 + rng.uniform(-7, 7)
        if yy > 1070:
            break
        f = 1.0 - i / 10.0
        ak.line(c, [(x0, yy + rng.uniform(-5, 5)), (x1, yy)],
                ak.mix(ak.darken(ICE, 0.3), SNOW, 0.55 * f),
                width=float(1.0 + f))
    ak.stipple(c, bmask, density=0.055, r=(0.4, 1.2),
               color=ak.mix(ICE, SNOW, 0.62), seed=seed + 5)

    # the lit snow cap: voronoi slabs in a band under the rim only
    cap = [(x0, y_top + snow_h)] + top_pts + [(x1, y_top + snow_h)]
    cmk = poly_mask(cap)
    lay2, ld2 = c.layer()
    bbox = (x0 - 8, y_top - 26, x1 + 8, y_top + snow_h + 10)
    for cell in ak.voronoi_polys(n=cells, seed=seed + 9, bbox=bbox, relax=2):
        t = float(np.clip(rng.normal(0.55, 0.18), 0.05, 0.95))
        col = ak.mix(SNOW, PAPER, t)
        ld2.polygon(c.pts(cell), fill=(*ak.hex_to_rgb(col), 255),
                    outline=(*ak.hex_to_rgb(ak.mix(SNOW, ICE, 0.45)), 170),
                    width=max(1, int(c.s(0.9))))
    c.img.paste(lay2, (0, 0), ak.Image.composite(
        cmk, ak.Image.new("L", (c.W, c.W), 0), lay2.getchannel("A")))
    c.draw = ak.ImageDraw.Draw(c.img, "RGBA")

    ak.line(c, top_pts, PAPER, width=2.8)          # crisp lit rim
    return top_pts


hi_top_pts = cliff(RAV_R, 1080, HI_TOP, SEED + 11, 34, tone=0.46)
lo_top_pts = cliff(0, RAV_L, LO_TOP, SEED + 12, 26, tone=0.28)

# broken ice along both rims
ak.chips(c, 40, (0, LO_TOP - 16, RAV_L - 6, LO_TOP + 16), size=(3, 7),
         colors=(PAPER, ak.mix(PAPER, SNOW, 0.4)), seed=SEED + 31)
ak.chips(c, 46, (RAV_R + 6, HI_TOP - 16, 1080, HI_TOP + 16), size=(3, 7),
         colors=(PAPER, ak.mix(PAPER, SNOW, 0.4)), seed=SEED + 32)

# ============================================ 4. props under the catwalk
DECK_L = (RAV_L, LO_TOP)
DECK_R = (RAV_R, HI_TOP)


def deck_y(x):
    t = (x - DECK_L[0]) / (DECK_R[0] - DECK_L[0])
    y = DECK_L[1] + t * (DECK_R[1] - DECK_L[1])
    # the reach past the last prop is unsupported, so it dips
    if 602.0 < x < 806.0:
        y += 19.0 * math.sin(math.pi * (x - 602.0) / (806.0 - 602.0))
    return y


PROP_X = [398.0, 500.0, 602.0]
GAP_X = 704.0                      # the socket that is empty
prop_dark = ak.darken(ICE, 0.42)
prop_lit = ak.mix(SNOW, PAPER, 0.30)   # posts catch the dusk, read light

# cross-bracing first, so the posts sit on top of it
for a, b in zip(PROP_X, PROP_X[1:]):
    ya, yb = deck_y(a) + 12, deck_y(b) + 12
    ak.line(c, [(a, ya), (b, FLOOR - 6)], prop_dark, width=2.6)
    ak.line(c, [(b, yb), (a, FLOOR - 6)], prop_dark, width=2.6)

for px in PROP_X:
    top = deck_y(px) + 8
    ak.poly(c, [(px - 5.0, top), (px + 5.0, top),
                (px + 6.6, FLOOR + 2), (px - 6.6, FLOOR + 2)], fill=prop_lit)
    ak.line(c, [(px + 3.6, top), (px + 4.9, FLOOR)],
            ak.mix(prop_lit, ICE, 0.42), width=1.7)      # shaded edge
    # snow drift banked against the footing
    ak.poly(c, ak.wobble_pts(
        [(px - 17, FLOOR + 12), (px - 7, FLOOR - 3), (px + 7, FLOOR - 3),
         (px + 17, FLOOR + 12)], amp=1.2, seed=SEED + int(px)),
        fill=ak.mix(SNOW, PAPER, 0.45))

for px in PROP_X:                      # snow caps on the prop heads
    ak.line(c, [(px - 6, deck_y(px) + 15), (px + 6, deck_y(px) + 15)],
            ak.mix(SNOW, PAPER, 0.5), width=2.0)

# THE MISSING FOURTH PROP — the concept's whole payload, so make it read.
# A void under the unsupported reach, then a snapped stump lit at the crown.
ak.glow(c, GAP_X, deck_y(GAP_X) + 150, 150, ak.darken(ICE, 0.85), alpha=140)

stub_h = 74.0
stub_top = FLOOR - stub_h
ak.poly(c, [(GAP_X - 7.0, stub_top + 10), (GAP_X + 7.0, stub_top),
            (GAP_X + 9.0, FLOOR + 2), (GAP_X - 9.0, FLOOR + 2)],
        fill=ak.mix(prop_lit, ICE, 0.34))
ak.line(c, [(GAP_X + 5.0, stub_top + 2), (GAP_X + 6.6, FLOOR)],
        ak.mix(prop_lit, ICE, 0.55), width=1.8)
# splintered crown, brightly lit so the eye finds the break
for _ in range(14):
    sx = GAP_X + rng.uniform(-7, 7)
    ak.line(c, [(sx, stub_top + rng.uniform(2, 14)),
                (sx + rng.uniform(-3.5, 3.5),
                 stub_top - rng.uniform(5, 21))],
            ak.mix(PAPER, SNOW, 0.30), width=float(rng.uniform(1.1, 2.1)))
ak.poly(c, ak.wobble_pts(
    [(GAP_X - 22, FLOOR + 14), (GAP_X - 9, FLOOR - 3), (GAP_X + 9, FLOOR - 3),
     (GAP_X + 22, FLOOR + 14)], amp=1.3, seed=SEED + 91),
    fill=ak.mix(SNOW, PAPER, 0.40))

# ==================================================== 5. the catwalk deck
DX0, DX1 = DECK_L[0] - 18, DECK_R[0] + 18
deck_w = ak.mix(ICE, SNOW, 0.42)
sx_list = list(np.linspace(DX0, DX1, 120))
top_edge = [(x, deck_y(x)) for x in sx_list]

# deck slab, following the sag
ak.poly(c, top_edge + [(x, deck_y(x) + 10.0) for x in reversed(sx_list)],
        fill=deck_w)
ak.poly(c, [(x, deck_y(x) + 10.0) for x in sx_list]
        + [(x, deck_y(x) + 14.5) for x in reversed(sx_list)],
        fill=ak.darken(ICE, 0.22))
# snow lying along the walked edge
ak.line(c, [(x, deck_y(x) - 1.2) for x in sx_list],
        ak.mix(PAPER, SNOW, 0.32), width=2.0)

# plank seams
for i in range(1, 40):
    t = i / 40
    px = DX0 + t * (DX1 - DX0)
    ak.line(c, [(px, deck_y(px)), (px + 2.4, deck_y(px) + 10.0)],
            ak.darken(ICE, 0.3), width=1.0)

# hairline crack in the deck directly above the missing prop
ak.hand_line(c, [(GAP_X - 26, deck_y(GAP_X - 26) + 1),
                 (GAP_X + 2, deck_y(GAP_X + 2) + 6),
                 (GAP_X + 28, deck_y(GAP_X + 28) + 2)],
             ak.darken(ICE, 0.5), width=2.2, amp=1.2, seed=SEED + 44)

# handrail on the far side, following the sag
rail_h = 30
rx = list(np.linspace(DECK_L[0] + 4, DECK_R[0] - 4, 80))
ak.line(c, [(x, deck_y(x) - rail_h) for x in rx], deck_w, width=2.2)
for i in range(9):
    t = (i + 0.5) / 9
    px = DECK_L[0] + 6 + t * (DECK_R[0] - DECK_L[0] - 12)
    ak.line(c, [(px, deck_y(px)), (px, deck_y(px) - rail_h)],
            deck_w, width=1.8)

# ======================================================= 6. the clinic
BX, BY = 842.0, 704.0          # base-left corner on the high terrace
BW, BH = 140.0, 88.0
apex = (BX + BW / 2, BY - BH - 38)

ak.glow(c, BX + BW / 2, BY - BH * 0.55, 104, LAMP, alpha=66)
ak.glow(c, BX + BW / 2, BY - BH * 0.55, 46, LAMP, alpha=54)

ak.poly(c, [(BX, BY), (BX + BW, BY), (BX + BW, BY - BH), (BX, BY - BH)],
        fill=ICE)
ak.poly(c, [(BX - 11, BY - BH + 3), (BX + BW + 11, BY - BH + 3), apex],
        fill=ak.darken(ICE, 0.28))
# snow load on the roof pitch
ak.poly(c, [(BX - 11, BY - BH + 3), (apex[0], apex[1]),
            (apex[0] - 4, apex[1] + 7), (BX - 5, BY - BH + 9)],
        fill=ak.mix(PAPER, SNOW, 0.30))

# lit windows
for i in range(3):
    wx = BX + 19 + i * 39
    ak.poly(c, [(wx, BY - 62), (wx + 21, BY - 62),
                (wx + 21, BY - 34), (wx, BY - 34)], fill=LAMP)
    ak.line(c, [(wx + 10.5, BY - 62), (wx + 10.5, BY - 34)],
            ak.darken(ICE, 0.1), width=1.4)
# light spilling onto the snow
ak.poly(c, [(BX + 8, BY), (BX + BW - 4, BY), (BX + BW + 30, BY + 15),
            (BX - 16, BY + 15)], fill=ak.mix(SNOW, LAMP, 0.30))

# stovepipe + wisp
ak.poly(c, [(BX + 108, BY - BH - 16), (BX + 117, BY - BH - 16),
            (BX + 117, BY - BH + 2), (BX + 108, BY - BH + 2)], fill=ICE)
ak.hand_line(c, [(BX + 112, BY - BH - 22), (BX + 121, BY - BH - 44),
                 (BX + 113, BY - BH - 66), (BX + 125, BY - BH - 90)],
             ak.mix(SKY_LO, PAPER, 0.35), width=2.0, amp=1.6, seed=SEED + 51)

# ========================================================== 7. spruce
SPRUCE_X = [1000, 1021, 1044, 1066]
for i, bx_ in enumerate(SPRUCE_X):
    sx = bx_ + rng.uniform(-4, 4)
    h = rng.uniform(26, 52)
    base_y = 702 - i * 1.6 + rng.uniform(-3, 3)
    w = h * 0.40
    ak.poly(c, ak.wobble_pts(
        [(sx - w, base_y), (sx, base_y - h), (sx + w, base_y)],
        amp=1.0, seed=SEED + 60 + i), fill=ak.mix(ICE, SNOW, 0.10))
    ak.line(c, [(sx, base_y), (sx, base_y - h * 0.25)], ICE, width=1.4)

# ==================================================== 8. spindrift + grain
ak.stipple(c, rect_mask([0, 300, 1080, 1080]), density=0.030, r=(0.4, 1.1),
           color=ak.mix(PAPER, SKY_LO, 0.4), seed=SEED + 71)
ak.grain(c, amount=6.0, seed=SEED, mono=True)

# ========================================================== 9. typography
HL_X, HL_TOP, HL_MAXW = 84, 118, 528
size = ak.fit_size(c, max(HEADLINE, key=len), HL_MAXW, lo=30, hi=92,
                   tracking=0.005, weight=900, opsz=144)
hf = ak.fraunces(c, size, weight=900, opsz=144)
hl_col = ak.ensure_contrast(PAPER, SKY_HI, 4.5)
lead = size * 1.06
for i, ln in enumerate(HEADLINE):
    ak.text(c, (HL_X, HL_TOP + i * lead), ln, hf, hl_col,
            anchor="la", tracking=0.005)

kick_y = HL_TOP + len(HEADLINE) * lead + 24
ak.text(c, (HL_X + 3, kick_y), KICKER, ak.mono(c, 15, medium=True),
        ak.ensure_contrast(SKY_LO, SKY_HI, 3.0), anchor="la", tracking=0.24)

ak.text(c, (HL_X, 998), "ALASKA.AI", ak.fraunces(c, 29, weight=900, opsz=144),
        ak.ensure_contrast(PAPER, ICE, 4.5), anchor="la", tracking=0.05)

# ============================================================== 10. finish
c.finish("out/post_image.png", {
    "date": "31 JUL 2026",
    "column": "The Stack",
    "kicker": "THE STACK",
    "middle_slot": "REGULATORY",
    "byline": "",
    "headline": "One Bureau Sets Alaska’s Health Circuit Prices",
    "style_family": "ukiyo_bokashi",
    "palette": PALETTE,
    "hue_family": "magenta",
    "composition": "diagonal_thrust",
    "motifs": ["temporary catwalk", "three props and one empty socket",
               "lit clinic on an ice terrace", "winter dusk ravine",
               "spruce stand"],
    "technique_stack": ["gradient_v", "ridge_pts", "ridge_fill",
                        "voronoi_polys", "hatch", "stipple", "chips",
                        "wobble_pts", "hand_line", "glow", "mottle",
                        "grain", "polaris"],
    "seed": SEED,
    "concept": ("The catwalk is the FY2027 waiver, the three props are the "
                "funding years already covered, and the empty fourth socket "
                "is FY2028, the decision that moves to one Bureau division "
                "and off any public agenda."),
    "eval_history": [
        {"iter": 1, "weighted": 6.42, "weakest": "craft",
         "note": "props hung from the deck like pendulums with floating "
                 "black footings; ravine was a flat dark rectangle; "
                 "terraces read as pack ice, not two sides of a chasm"},
        {"iter": 2, "weighted": 7.31, "weakest": "craft",
         "note": "landform rebuilt as two snow-capped cliffs over a "
                 "deepening slot, props now standing on a floor; but the "
                 "ruled vertical hatch on the faces read as corduroy"},
        {"iter": 3, "weighted": 7.51, "weakest": "composition",
         "note": "hatch replaced by ice blocks and irregular fracture, "
                 "but uniform block texture now covered ~45% of canvas "
                 "as undifferentiated noise"},
        {"iter": 4, "weighted": 8.16, "weakest": "craft",
         "note": "ravine widened to 510px so span and void dominate, face "
                 "texture calmed toward the edges; missing prop still "
                 "illegible"},
        {"iter": 5, "weighted": 8.35, "weakest": "craft",
         "note": "added sag across the unsupported reach, enlarged stump "
                 "with lit splintered crown; residual horizontal seam "
                 "artifact at y~800 and splinters read as flame"},
        {"iter": 6, "weighted": 8.66, "weakest": "detail",
         "note": "seam removed, splinters retinted to timber, sag "
                 "deepened, bokashi cloud banding added to the mid-sky"}
    ],
    "eval_final": {
        "weighted": 8.66,
        "scores": {"concept": 9, "focal": 8.5, "composition": 8.5,
                   "color": 9, "detail": 8, "craft": 8.5,
                   "typography": 9, "originality": 8.5, "fidelity": 9},
        "ship_bar": 8.5,
        "iterations_used": 6
    },
})
print("rendered out/post_image.png")
