"""The Stack — 2026-07-24 — bespoke cover.
Concept: two valves in series on a conduit rising from an AI-pinned
critical-mineral ore body. Value reaches the surface only if BOTH
valves open (NSF TIP money key + NANA ground key). style_family
geologic_engraving; hue green + copper ore focal; composition
bilateral_gate. SEED 724.
"""
import sys, math, traceback
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as k
from PIL import Image, ImageDraw

SEED = 724

def dashed(c, p0, p1, color, width=2, dash=15, gap=11, d=None):
    x0, y0 = p0; x1, y1 = p1
    ln = math.hypot(x1 - x0, y1 - y0)
    if ln < 1: return
    ux, uy = (x1 - x0) / ln, (y1 - y0) / ln
    t = 0.0
    while t < ln:
        a = (x0 + ux * t, y0 + uy * t)
        t2 = min(ln, t + dash)
        b = (x0 + ux * t2, y0 + uy * t2)
        k.line(c, [a, b], color, width, d=d)
        t += dash + gap

def valve(c, vx, vy, r, rim, spoke, hub, dark):
    # handwheel: outer ring, spokes, hub
    k.circle(c, vx, vy, r, outline=dark, width=6)
    k.circle(c, vx, vy, r * 0.86, outline=rim, width=4)
    for i in range(6):
        a = math.radians(i * 60 + 8)
        k.line(c, [(vx + math.cos(a) * r * 0.16, vy + math.sin(a) * r * 0.16),
                   (vx + math.cos(a) * r * 0.84, vy + math.sin(a) * r * 0.84)],
               spoke, width=5)
    k.circle(c, vx, vy, r * 0.20, fill=hub)
    k.circle(c, vx, vy, r * 0.20, outline=dark, width=3)

def main():
    c = k.Canvas(bg="#e7efe5", ss=2)

    # ---- palette (OKLCH; dominant green, warm copper focal) ----
    paper   = k.oklch(0.93, 0.030, 155)   # pale mint sky/light
    sky_lo  = k.oklch(0.80, 0.045, 176)   # teal-green above ground
    ground_line_col = k.oklch(0.42, 0.045, 160)
    strata_light = k.oklch(0.65, 0.052, 158)
    strata_deep  = k.oklch(0.235, 0.042, 158)
    seam    = k.oklch(0.30, 0.040, 158)
    ink     = k.oklch(0.17, 0.030, 158)
    metal   = k.oklch(0.74, 0.030, 165)   # pale metallic for valve rims
    ore     = k.oklch(0.72, 0.150, 62)     # copper focal accent
    ore_hi  = k.oklch(0.86, 0.110, 78)
    ore_dk  = k.oklch(0.46, 0.130, 52)
    NB = 6
    GY = 470.0

    # ---- 1-2 sky ----
    k.gradient_v(c, (0, 0, 1080, GY + 6), paper, sky_lo, ease=1.25)

    # ---- 3 subsurface deep base ----
    k.poly(c, [(0, GY), (1080, GY), (1080, 1080), (0, 1080)], fill=strata_deep)

    # ---- 4 strata bands (ridge_fill stacking: light near surface -> dark deep) ----
    bounds = [GY, 556, 640, 726, 818, 918, 1080]
    band_cols = k.ramp([strata_light, strata_deep], NB)
    for i in range(NB):
        pts = k.ridge_pts(bounds[i], amp=15, scale=2.4, octaves=4, seed=SEED + i * 7)
        poly_pts = [(pts[0][0], 1080)] + pts + [(pts[-1][0], 1080)]
        k.poly(c, poly_pts, fill=band_cols[i])
        # thin seam line along the band top
        k.line(c, pts, seam, width=2)

    # ---- 4b voronoi fracture seams (meso structure inside the ground) ----
    cells = k.voronoi_polys(n=74, seed=SEED, bbox=(-40, GY + 8, 1120, 1080), relax=1)
    seamlay, sd = c.layer()
    for cell in cells:
        if len(cell) >= 3:
            sd.line(c.pts(cell + [cell[0]]), fill=(*k.hex_to_rgb(seam), 90),
                    width=max(1, int(c.s(1.1))), joint="curve")
    c.composite(seamlay)

    # ---- 5 engraving hatch over subsurface (denser deep) ----
    m_top, dtop = c.mask()
    dtop.rectangle([0, c.s(GY), c.W, c.s(760)], fill=255)
    k.hatch(c, m_top, spacing=17, angle=-16, color=seam, width=1.0)
    m_deep, ddeep = c.mask()
    ddeep.rectangle([0, c.s(740), c.W, c.W], fill=255)
    k.hatch(c, m_deep, spacing=11, angle=-16, color=k.darken(seam, 0.05), width=1.2)

    # ---- 6 dark collar around ore ----
    OX, OY = 540.0, 832.0
    collar = k.blob_pts(OX, OY, 210, wobble=0.10, harmonics=(1, 2, 3), points=150, seed=SEED + 3)
    k.poly(c, collar, fill=strata_deep)
    collar2 = k.blob_pts(OX, OY, 150, wobble=0.12, harmonics=(1, 2, 3, 5), points=150, seed=SEED + 4)
    k.poly(c, collar2, fill=k.darken(strata_deep, 0.03))

    # ---- 7 conduit channel (ore -> surface) ----
    CX = 540.0
    k.poly(c, [(CX - 15, GY), (CX + 15, GY), (CX + 12, OY - 10), (CX - 12, OY - 10)],
           fill=k.mix(strata_deep, metal, 0.22))
    k.hand_line(c, [(CX - 15, GY), (CX - 12, OY - 10)], ink, width=3, amp=1.4, seed=SEED + 5)
    k.hand_line(c, [(CX + 15, GY), (CX + 12, OY - 10)], ink, width=3, amp=1.4, seed=SEED + 6)
    # surface manifold cap
    k.poly(c, [(CX - 40, GY - 12), (CX + 40, GY - 12), (CX + 40, GY + 6), (CX - 40, GY + 6)],
           fill=metal, outline=ink, width=3)

    # ---- 8 ore body: glow + lens + vein tendrils + sparkle ----
    k.glow(c, OX, OY, 190, ore, alpha=70)
    k.glow(c, OX, OY, 120, ore_hi, alpha=70)
    lens = k.blob_pts(OX, OY, 104, wobble=0.12, harmonics=(1, 2, 3), points=160, seed=SEED + 8)
    k.poly(c, lens, fill=ore)
    lens_hi = k.blob_pts(OX - 14, OY - 16, 56, wobble=0.13, harmonics=(1, 2, 3), points=140, seed=SEED + 9)
    k.poly(c, lens_hi, fill=ore_hi)
    # internal crystalline facet lines (nose-length structure)
    for fa in [(-60, -30, 70, 40), (30, -50, -40, 55), (-20, 20, 60, -60)]:
        k.line(c, [(OX + fa[0], OY + fa[1]), (OX + fa[2], OY + fa[3])],
               k.mix(ore_hi, ore, 0.4), width=2)
    # vein tendrils out of the lens (irregular, thin, veinlike — not a burst)
    tangles = [18, 74, 129, 196, 251, 312]
    for i, deg in enumerate(tangles):
        a = math.radians(deg)
        r0 = 92; r1 = 92 + 26 + (i % 3) * 18
        mid = ((OX + math.cos(a) * (r0 + r1) / 2 + (12 if i % 2 else -10)),
               (OY + math.sin(a) * (r0 + r1) / 2))
        k.hand_line(c, [(OX + math.cos(a) * r0, OY + math.sin(a) * r0), mid,
                        (OX + math.cos(a) * r1, OY + math.sin(a) * r1)],
                    ore_dk, width=2, amp=2.6, seed=SEED + 20 + i)
    # ore sparkle micro
    m_ore, mo = c.mask()
    mo.polygon(c.pts(lens), fill=255)
    k.stipple(c, m_ore, density=0.16, r=(0.7, 1.7), color=ore_hi, seed=SEED + 30)
    k.chips(c, 46, (OX - 150, OY - 150, OX + 150, OY + 150),
            size=(2.5, 6.5), colors=(ore_hi, ore, ore_dk), seed=SEED + 31)

    # ---- 9 valves in series + stems + node chips ----
    VA = (CX, 690.0)   # lower / deeper valve  -> stem LEFT to NSF TIP
    VB = (CX, 556.0)   # upper valve           -> stem RIGHT to NANA
    # stems
    k.hand_line(c, [VA, (300, 690)], ink, width=4, amp=1.2, seed=SEED + 40)
    k.hand_line(c, [VB, (792, 556)], ink, width=4, amp=1.2, seed=SEED + 41)
    valve(c, VA[0], VA[1], 46, metal, ink, ore, ink)
    valve(c, VB[0], VB[1], 46, metal, ink, ore, ink)

    # ---- 10 AI reticle: sightlines from the right sky converge on the wellhead,
    #        kept clear of the headline/kicker; plumb drops to the ore ----
    TGT = (CX + 6, GY - 4)
    for p in [(772, 306), (872, 328), (972, 356)]:
        dashed(c, p, TGT, k.mix(ink, sky_lo, 0.34), width=2, dash=16, gap=12)
    dashed(c, TGT, (CX, OY - 96), ore_dk, width=2, dash=14, gap=10)
    k.circle(c, TGT[0], TGT[1], 15, outline=ink, width=3)
    k.line(c, [(TGT[0] - 24, TGT[1]), (TGT[0] + 24, TGT[1])], ink, width=2)
    k.line(c, [(TGT[0], TGT[1] - 24), (TGT[0], TGT[1] + 24)], ink, width=2)

    # ---- 11 grain finish (restrained) ----
    k.grain(c, amount=6.0, seed=SEED)

    # ---- 12 type ----
    # eyebrow
    eb = k.fraunces(c, 30, weight=650, opsz=40)
    k.text(c, (86, 96), "ALASKA’S MINERAL ENGINE", eb,
           k.ensure_contrast(ink, paper), anchor="la", tracking=0.02)
    # big headline
    hcol = k.ensure_contrast(ink, paper)
    s1 = k.fit_size(c, "RUNS ON", 560, lo=70, hi=150, weight=900, opsz=144)
    f1 = k.fraunces(c, s1, weight=900, opsz=144)
    k.text(c, (84, 132), "RUNS ON", f1, hcol, anchor="la")
    s2 = k.fit_size(c, "TWO KEYS", 600, lo=70, hi=168, weight=900, opsz=144)
    f2 = k.fraunces(c, s2, weight=900, opsz=144)
    k.text(c, (84, 132 + s1 * 0.96), "TWO KEYS", f2, ore_dk, anchor="la")

    # kicker
    kf = k.mono(c, 18, medium=True)
    k.text(c, (86, 132 + s1 * 0.96 + s2 * 1.02 + 20),
           "THE STACK · VEHICLES · 24 JUL 2026", kf,
           k.ensure_contrast(ink, paper), anchor="la", tracking=0.20)

    # valve labels (chips)
    lf = k.mono(c, 17, medium=True)
    k.chip(c, (296, 690), "NSF TIP · $15M", lf, paper, ink, pad=9, anchor="ra")
    k.chip(c, (796, 556), "NANA · GROUND", lf, paper, ink, pad=9, anchor="la")
    # option tag: the $160M tranche above the valves (legible ghost chip)
    of = k.mono(c, 16, medium=True)
    k.chip(c, (470, 502), "$160M · OPTION", of, ink, strata_light, pad=8, anchor="ra")

    # wordmark chip + polaris colophon
    wf = k.fraunces(c, 27, weight=900, opsz=40)
    k.chip(c, (84, 1006), "ALASKA.AI", wf, paper, ink, pad=11, anchor="ls")
    k.polaris(c, 986, 118, r=13, color=ore, core=ore_hi)

    meta = {
        "date": "24 JUL 2026", "column": "The Stack", "kicker": "THE STACK",
        "middle_slot": "VEHICLES",
        "headline": "Alaska’s Mineral Engine Runs On Two Keys",
        "byline": "",
        "style_family": "geologic_engraving",
        "palette": [paper, sky_lo, strata_light, strata_deep, ink, metal, ore],
        "hue_family": "green",
        "composition": "bilateral_gate",
        "motifs": ["critical-mineral ore body", "two series valves",
                   "AI triangulation reticle", "geologic strata cross-section",
                   "subsurface conduit"],
        "technique_stack": ["gradient_v", "ridge_fill", "voronoi_polys",
                            "hatch", "glow", "stipple", "chips", "hand_line",
                            "grain"],
        "seed": SEED,
        "eval_history": [
            {"iter": 1, "weighted": 8.13, "weakest": "craft",
             "note": "AI sightlines collided with kicker; ore tendrils read as an explosion burst; $160M tag dark-on-dark"},
            {"iter": 2, "weighted": 8.60, "weakest": "detail",
             "note": "collisions fixed; sightlines confined to right sky; ore reads as ore body; option chip legible"},
            {"iter": 3, "weighted": 8.73, "weakest": "typography",
             "note": "$160M tag lifted into the above-the-valves zone; ore given internal crystalline facets"}
        ],
        "eval_final": {
            "weighted": 8.73,
            "scores": {"concept": 9, "focal": 9, "composition": 8.5,
                       "color": 8.5, "detail": 8.5, "craft": 9,
                       "typography": 8.5, "originality": 8.5, "fidelity": 9}
        },
    }
    c.finish("out/post_image.png", meta)
    print("rendered out/post_image.png")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
