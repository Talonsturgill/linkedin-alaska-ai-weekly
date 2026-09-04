"""The Stack — 2026-09-04 — bespoke cover.

Concept: the corridor rulebook as an exploded isometric assembly. A solid
locked floor slab (30 U.S.C. 185(n), the renewal that cannot be refused), an
EMPTY OPEN TRAY above it (185(f), thirty years of terms still unwritten), and
a thin lid descending onto that tray (the NEPA instrument) with a narrow lit
gap still open between them. The gap is the fifteen-day scoping window.
style_family exploded_iso_docket; hue blue with a single gold focal;
composition exploded_iso_stack. SEED 904.
"""
import sys, math, traceback
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import art_kit as k

SEED = 904

# ---- iso frame ----
S = 1.10                 # iso scale
ORG = (622.0, 620.0)     # iso origin in design space
FP = 250.0               # slab footprint (iso units, square)

def P(x, y, z):
    return k.iso(x, y, z, S, ORG)


def quad(c, pts, fill, outline=None, w=2, d=None):
    k.poly(c, pts, fill=fill, outline=outline, width=w, d=d)


def face_mask(c, pts):
    m, md = c.mask()
    md.polygon(c.pts(pts), fill=255)
    return m


def slab(c, z0, dz, top, left, right, ink, x0=0.0, y0=0.0, sx=FP, sy=FP,
         hatch_top=None, hatch_left=None, hatch_right=None, outline_w=2):
    """A machined isometric plate with three shaded faces, drawn back to front."""
    x1, y1, z1 = x0 + sx, y0 + sy, z0 + dz
    top_pts   = [P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)]
    left_pts  = [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]
    right_pts = [P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)]
    quad(c, left_pts,  left,  outline=ink, w=outline_w)
    quad(c, right_pts, right, outline=ink, w=outline_w)
    quad(c, top_pts,   top,   outline=ink, w=outline_w)
    if hatch_left:
        k.hatch(c, face_mask(c, left_pts), spacing=hatch_left[0],
                angle=hatch_left[1], color=hatch_left[2], width=1.0)
    if hatch_right:
        k.hatch(c, face_mask(c, right_pts), spacing=hatch_right[0],
                angle=hatch_right[1], color=hatch_right[2], width=1.0)
    if hatch_top:
        k.hatch(c, face_mask(c, top_pts), spacing=hatch_top[0],
                angle=hatch_top[1], color=hatch_top[2], width=1.0)
    return top_pts, left_pts, right_pts


def main():
    paper   = k.oklch(0.945, 0.010, 250)
    field   = k.mix(paper, k.oklch(0.700, 0.042, 248), 0.50)  # derived tint, not an ink
    s_top   = k.oklch(0.700, 0.042, 248)
    s_left  = k.oklch(0.495, 0.048, 250)
    s_right = k.oklch(0.370, 0.045, 253)
    ink     = k.oklch(0.195, 0.028, 250)
    gold    = k.oklch(0.795, 0.145, 85)
    gold_hi = k.oklch(0.920, 0.090, 92)
    gold_dp = k.oklch(0.575, 0.130, 70)

    c = k.Canvas(bg=paper, ss=2)

    # ---- 1 field gradient + paper tooth ----
    k.gradient_v(c, (0, 0, 1080, 1080), field, paper, ease=1.35)
    k.mottle(c, strength=0.045, scale=3.2, seed=SEED)
    # faint technical grid, the drafting-table substrate
    grid = k.mix(field, ink, 0.085)
    for gx in range(0, 1081, 54):
        k.line(c, [(gx, 0), (gx, 1080)], grid, width=1)
    for gy in range(0, 1081, 54):
        k.line(c, [(0, gy), (1080, gy)], grid, width=1)
    for gx in range(0, 1081, 270):
        k.line(c, [(gx, 0), (gx, 1080)], k.mix(field, ink, 0.16), width=1)
    for gy in range(0, 1081, 270):
        k.line(c, [(0, gy), (1080, gy)], k.mix(field, ink, 0.16), width=1)
    # corner registration ticks, drafting-sheet furniture rather than a stray route line
    for cx, cy, sx, sy in ((54, 54, 1, 1), (1026, 54, -1, 1),
                           (54, 1026, 1, -1), (1026, 1026, -1, -1)):
        reg = k.mix(field, ink, 0.22)
        k.line(c, [(cx, cy), (cx + 26 * sx, cy)], reg, width=2)
        k.line(c, [(cx, cy), (cx, cy + 26 * sy)], reg, width=2)

    # ---- 2 ground shadows ----
    sh, sd = c.layer()
    base_ctr = P(FP / 2, FP / 2, 0)
    sd.ellipse([c.s(base_ctr[0] - 268), c.s(base_ctr[1] - 44),
                c.s(base_ctr[0] + 268), c.s(base_ctr[1] + 56)],
               fill=(*k.hex_to_rgb(s_right), 62))
    c.composite(sh.filter(k.ImageFilter.GaussianBlur(c.s(26))))

    # ---- 3 floor slab: 185(n), the guaranteed renewal ----
    slab(c, 0, 34, s_top, s_left, s_right, ink,
         hatch_top=(15, -30, k.mix(s_top, ink, 0.20)),
         hatch_left=(7, 30, k.mix(s_left, ink, 0.34)),
         hatch_right=(6, -30, k.mix(s_right, ink, 0.30)),
         outline_w=3)
    # micro: chipped corners + cracks on the floor plate
    for i, (cx, cy) in enumerate([(18, 232), (232, 20), (126, 246)]):
        a = P(cx, cy, 34)
        k.hand_line(c, [(a[0] - 26, a[1]), (a[0] + 4, a[1] - 7), (a[0] + 30, a[1] + 3)],
                    k.mix(s_top, ink, 0.42), width=2, amp=1.5, seed=SEED + 60 + i)
    # composed bevel highlight along the two lit top edges
    k.line(c, [P(0, 0, 34), P(FP, 0, 34)], k.lighten(s_top, 0.10), width=3)
    k.line(c, [P(0, 0, 34), P(0, FP, 34)], k.lighten(s_top, 0.07), width=3)
    # meso: surveyed-ground ticks along the exposed margin of the floor plate,
    # the land the corridor actually crosses
    tick = k.mix(s_top, ink, 0.34)
    for i in range(1, 20):
        u = FP * i / 20.0
        a = P(u, 6, 34); b = P(u, 15, 34)
        k.line(c, [a, b], tick, width=1)
        a2 = P(6, u, 34); b2 = P(15, u, 34)
        k.line(c, [a2, b2], tick, width=1)
    # corner monuments
    for mx, my in ((10, 10), (FP - 10, 10), (10, FP - 10)):
        m = P(mx, my, 34)
        k.circle(c, m[0], m[1], 4.2, outline=k.mix(s_top, ink, 0.52), width=2)

    # ---- 4 the empty tray: 185(f), terms unwritten ----
    TZ, TDZ = 92.0, 40.0
    IN = 32.0                        # wall thickness
    ix0, iy0, ix1, iy1 = IN, IN, FP - IN, FP - IN
    zf = TZ + 3.0                    # cavity floor, sunk deep so the box reads empty
    zr = TZ + TDZ                    # rim

    tray_left  = [P(0, FP, TZ), P(FP, FP, TZ), P(FP, FP, zr), P(0, FP, zr)]
    tray_right = [P(FP, 0, TZ), P(FP, FP, TZ), P(FP, FP, zr), P(FP, 0, zr)]
    quad(c, tray_left,  s_left,  outline=ink, w=3)
    quad(c, tray_right, s_right, outline=ink, w=3)
    k.hatch(c, face_mask(c, tray_left), spacing=8, angle=30,
            color=k.mix(s_left, ink, 0.30), width=1.0)
    k.hatch(c, face_mask(c, tray_right), spacing=7, angle=-30,
            color=k.mix(s_right, ink, 0.26), width=1.0)
    # rim (top face of the walls)
    quad(c, [P(0, 0, zr), P(FP, 0, zr), P(FP, FP, zr), P(0, FP, zr)],
         s_top, outline=ink, w=3)
    # cavity floor — DARK and recessed. An empty box in shadow reads empty.
    cav_dk    = k.oklch(0.255, 0.018, 250)   # cool shadow, the empty floor
    inner_far = k.oklch(0.545, 0.052, 80)    # warm grey-tan, light raking in
    inner_near= k.oklch(0.315, 0.028, 72)    # near wall stays in shadow
    cav = [P(ix0, iy0, zf), P(ix1, iy0, zf), P(ix1, iy1, zf), P(ix0, iy1, zf)]
    quad(c, cav, cav_dk, outline=None)
    k.stipple(c, face_mask(c, cav), density=0.05, r=(0.4, 1.0),
              color=k.lighten(cav_dk, 0.05), seed=SEED + 44)
    # blank ruled lines waiting to be written on
    for t in range(1, 10):
        u = iy0 + (iy1 - iy0) * t / 10.0
        k.line(c, [P(ix0 + 10, u, zf), P(ix1 - 10, u, zf)],
               k.mix(cav_dk, field, 0.38), width=1)
    # inner walls: light rakes down the far wall from the gap, near wall stays dark
    quad(c, [P(ix0, iy0, zf), P(ix1, iy0, zf), P(ix1, iy0, zr), P(ix0, iy0, zr)],
         inner_far, outline=k.mix(cav_dk, ink, 0.4), w=1)
    quad(c, [P(ix0, iy0, zf), P(ix0, iy1, zf), P(ix0, iy1, zr), P(ix0, iy0, zr)],
         inner_near, outline=k.mix(cav_dk, ink, 0.4), w=1)
    # gold catch-light on the rim's inner lip only — light, not material
    k.line(c, [P(ix0, iy0, zr), P(ix1, iy0, zr)], gold_hi, width=3)
    k.line(c, [P(ix0, iy0, zr), P(ix0, iy1, zr)], gold, width=3)
    # rim inner edge
    k.line(c, [P(ix0, iy0, zr), P(ix1, iy0, zr), P(ix1, iy1, zr),
               P(ix0, iy1, zr), P(ix0, iy0, zr)], ink, width=2)

    # ---- 5 light spilling out of the gap ----
    gap_c = P(FP / 2, FP / 2, (zr + 196.0) / 2.0)
    k.glow(c, gap_c[0], gap_c[1], 232, gold, alpha=64)
    k.glow(c, gap_c[0], gap_c[1], 118, gold_hi, alpha=76)

    # ---- 6 the lid: the NEPA instrument, descending ----
    LZ, LDZ = 196.0, 16.0
    lid_top, lid_left, lid_right = slab(
        c, LZ, LDZ, k.lighten(s_top, 0.05), s_left, s_right, ink,
        hatch_top=(17, 30, k.mix(s_top, ink, 0.16)),
        hatch_left=(9, 30, k.mix(s_left, ink, 0.30)),
        hatch_right=(8, -30, k.mix(s_right, ink, 0.26)),
        outline_w=3)
    # meso: panel seams dividing the instrument into sections, iso-aligned
    seam = k.mix(s_top, ink, 0.26)
    for u in (FP / 3.0, 2.0 * FP / 3.0):
        k.line(c, [P(u, 6, LZ + LDZ), P(u, FP - 6, LZ + LDZ)], seam, width=1)
        k.line(c, [P(6, u, LZ + LDZ), P(FP - 6, u, LZ + LDZ)], seam, width=1)
    # micro: fastener marks at the panel intersections
    for ux in (FP / 3.0, 2.0 * FP / 3.0):
        for uy in (FP / 3.0, 2.0 * FP / 3.0):
            f = P(ux, uy, LZ + LDZ)
            k.circle(c, f[0], f[1], 3.4, fill=k.mix(s_top, ink, 0.46))
            k.circle(c, f[0] - 0.8, f[1] - 0.8, 1.5, fill=k.lighten(s_top, 0.18))
    # underside catching gold from the gap
    # only the two LOWER underside edges catch light, because the light is below
    k.line(c, [P(0, FP, LZ), P(FP, FP, LZ)], gold, width=4)
    k.line(c, [P(FP, 0, LZ), P(FP, FP, LZ)], gold_hi, width=4)
    # micro glints where the light breaks over the lid's lower edge
    for t in (0.16, 0.34, 0.52, 0.70, 0.88):
        g1 = P(FP * t, FP, LZ)
        k.circle(c, g1[0], g1[1], 2.4, fill=gold_hi)
        g2 = P(FP, FP * t, LZ)
        k.circle(c, g2[0], g2[1], 2.0, fill=gold_hi)
    # TAPS zigzag engraved across the lid
    zig = []
    for i in range(11):
        t = 14.0 + (FP - 28.0) * i / 10.0
        zig.append(P(t, FP / 2 + (52 if i % 2 == 0 else -52), LZ + LDZ))
    k.hand_line(c, zig, k.mix(s_top, ink, 0.66), width=5, amp=1.5, seed=SEED + 11)
    k.hand_line(c, zig, k.lighten(s_top, 0.16), width=2, amp=1.5, seed=SEED + 11)
    # vertical support piers at each bend, the detail that says pipeline
    for i, pt in enumerate(zig):
        if i % 2 == 0:
            k.line(c, [(pt[0], pt[1]), (pt[0], pt[1] + 11)],
                   k.mix(s_top, ink, 0.52), width=3)

    # ---- 7 the second gate, lower right: ADL 63574 ----
    S2, O2 = 0.40, (884.0, 856.0)
    def P2(x, y, z):
        return k.iso(x, y, z, S2, O2)
    sh2, sd2 = c.layer()
    b2 = P2(FP / 2, FP / 2, 0)
    sd2.ellipse([c.s(b2[0] - 104), c.s(b2[1] - 18), c.s(b2[0] + 104), c.s(b2[1] + 24)],
                fill=(*k.hex_to_rgb(s_right), 55))
    c.composite(sh2.filter(k.ImageFilter.GaussianBlur(c.s(12))))
    for pts, col in (
        ([P2(0, FP, 0), P2(FP, FP, 0), P2(FP, FP, 30), P2(0, FP, 30)], s_left),
        ([P2(FP, 0, 0), P2(FP, FP, 0), P2(FP, FP, 30), P2(FP, 0, 30)], s_right),
        ([P2(0, 0, 30), P2(FP, 0, 30), P2(FP, FP, 30), P2(0, FP, 30)], s_top)):
        quad(c, pts, col, outline=ink, w=2)
    cav2 = [P2(IN, IN, 14), P2(FP - IN, IN, 14), P2(FP - IN, FP - IN, 14), P2(IN, FP - IN, 14)]
    quad(c, cav2, k.oklch(0.255, 0.018, 250), outline=ink, w=1)
    k.line(c, [P2(IN, IN, 30), P2(FP - IN, IN, 30)], gold, width=2)
    k.line(c, [P2(IN, IN, 30), P2(IN, FP - IN, 30)], gold_dp, width=2)

    # ---- 8 the 15-day dimension bracket on the gap ----
    gl_top = P(0, FP, LZ)          # lid left vertex (gap ceiling)
    gl_bot = P(0, FP, zr)          # tray rim left vertex (gap floor)
    bx = gl_top[0] - 34
    k.line(c, [(bx, gl_top[1]), (bx, gl_bot[1])], gold_dp, width=3)
    for yy in (gl_top[1], gl_bot[1]):
        k.line(c, [(bx - 11, yy), (bx + 11, yy)], gold_dp, width=3)
    k.line(c, [(bx + 6, gl_top[1] + 3), (gl_top[0] - 4, gl_top[1] + 3)],
           k.mix(gold_dp, field, 0.45), width=1)
    k.line(c, [(bx + 6, gl_bot[1] - 3), (gl_bot[0] - 4, gl_bot[1] - 3)],
           k.mix(gold_dp, field, 0.45), width=1)

    # ---- 9 stipple on the darkest faces (micro) ----
    k.stipple(c, face_mask(c, [P(FP, 0, 0), P(FP, FP, 0), P(FP, FP, 34), P(FP, 0, 34)]),
              density=0.08, r=(0.5, 1.2), color=k.darken(s_right, 0.06), seed=SEED + 31)

    # ---- 10 grain + vignette ----
    k.grain(c, amount=6.0, seed=SEED)
    k.vignette(c, strength=0.16, spread=1.40)

    # ---- 11 type ----
    hcol = k.ensure_contrast(ink, paper)
    s1 = k.fit_size(c, "RENEWAL IS", 545, lo=60, hi=104, weight=900, opsz=144)
    f1 = k.fraunces(c, s1, weight=900, opsz=144)
    k.text(c, (84, 88), "RENEWAL IS", f1, hcol, anchor="la")
    s2 = k.fit_size(c, "GUARANTEED", 545, lo=60, hi=104, weight=900, opsz=144)
    f2 = k.fraunces(c, s2, weight=900, opsz=144)
    k.text(c, (84, 88 + s1 * 0.98), "GUARANTEED", f2, hcol, anchor="la")
    y3 = 88 + s1 * 0.98 + s2 * 1.02
    s3 = k.fit_size(c, "THE TERMS ARE NOT", 470, lo=32, hi=58, weight=800, opsz=72)
    f3 = k.fraunces(c, s3, weight=800, opsz=72)
    k.text(c, (84, y3), "THE TERMS ARE NOT", f3,
           k.ensure_contrast(gold_dp, paper), anchor="la")

    kf = k.mono(c, 17, medium=True)
    k.text(c, (86, y3 + s3 * 1.30), "THE STACK · FACILITIES · 4 SEP 2026", kf,
           k.ensure_contrast(ink, paper), anchor="la", tracking=0.20)

    lf = k.mono(c, 15, medium=True)
    gf = k.mono(c, 16, medium=True)
    # gap dimension label
    k.text(c, (bx - 20, (gl_top[1] + gl_bot[1]) / 2), "15 DAYS", gf,
           k.ensure_contrast(gold_dp, paper), anchor="rm", tracking=0.12)
    # left callouts + leader lines
    k.chip(c, (96, 664), "185(f) · TERMS UNWRITTEN", lf, paper, ink, pad=8, anchor="lm")
    k.line(c, [(324, 664), (P(0, FP, TZ + 20)[0] - 6, P(0, FP, TZ + 20)[1])],
           k.mix(ink, field, 0.5), width=1)
    k.chip(c, (96, 800), "185(n) · SHALL RENEW", lf, paper, ink, pad=8, anchor="lm")
    k.line(c, [(300, 800), (P(0, FP, 17)[0] - 6, P(0, FP, 17)[1] + 4)],
           k.mix(ink, field, 0.5), width=1)
    # second gate label
    k.text(c, (884, 962), "ADL 63574 · 26.1 AC", lf,
           k.ensure_contrast(ink, paper), anchor="ma", tracking=0.14)
    # docket telemetry under the assembly
    df = k.mono(c, 13)
    k.text(c, (500, 934), "DOI-BLM-AK-9410-2026-0009-EA", df,
           k.mix(ink, field, 0.32), anchor="ma", tracking=0.16)

    wf = k.fraunces(c, 27, weight=900, opsz=40)
    k.chip(c, (84, 1010), "ALASKA.AI", wf, paper, ink, pad=11, anchor="ls")
    k.polaris(c, 992, 92, r=13, color=gold, core=gold_hi)

    meta = {
        "date": "4 SEP 2026", "column": "The Stack", "kicker": "THE STACK",
        "middle_slot": "FACILITIES",
        "headline": "Renewal Is Guaranteed. The Terms Are Not.",
        "byline": "",
        "style_family": "exploded_iso_docket",
        "palette": [paper, s_top, s_left, s_right, ink, gold, gold_dp],
        "hue_family": "blue",
        "composition": "exploded_iso_stack",
        "motifs": ["exploded isometric corridor assembly", "empty stipulations tray",
                   "descending NEPA lid", "lit fifteen-day gap",
                   "TAPS zigzag engraved on the lid", "offset second gate"],
        "technique_stack": ["iso", "iso_prism", "poly", "gradient_v", "mottle",
                            "glow", "hatch", "stipple", "chips", "hand_line",
                            "line", "chip", "grain", "vignette", "polaris"],
        "seed": SEED,
        "eval_history": [
            {"iter": 1, "weighted": 7.06, "weakest": "concept",
             "note": "gold-filled cavity read as a SOLID gold slab, inverting the metaphor "
                     "(unwritten terms looked like stored value); second gate rendered green "
                     "from an RGB mix of gold into blue-grey, an off-palette accident; large "
                     "flat background acreage; debris chips read as dirt specks"},
            {"iter": 2, "weighted": 7.9, "weakest": "color",
             "note": "cavity re-cut deep and dark so the tray reads hollow, which fixed the "
                     "concept; added drafting grid and corridor route for meso structure; but "
                     "naive RGB mixes of navy into saturated gold produced purple and green "
                     "inner walls, worse than the bug they replaced"},
            {"iter": 3, "weighted": 8.39, "weakest": "craft",
             "note": "inner walls redefined as explicit OKLCH warm greys, killing the purple "
                     "and green; gap bloom strengthened; but gold then traced the lid's entire "
                     "perimeter and read as a neon outline rather than light from below, and "
                     "the corridor route line read as a stray smudge"},
            {"iter": 4, "weighted": 8.575, "weakest": "detail",
             "note": "light logic corrected so only the two lower underside edges catch gold; "
                     "route line replaced with corner registration ticks; plate top faces still "
                     "read uniform and the piece edged toward generic exploded-deck territory"},
            {"iter": 5, "weighted": 8.675, "weakest": "originality",
             "note": "meso pass: panel seams and fastener marks machine the instrument plate, "
                     "surveyed-ground ticks and corner monuments on the floor plate margin, "
                     "micro glints where light breaks over the lid edge"},
        ],
        "eval_final": {
            "weighted": 8.675,
            "scores": {"concept": 9.0, "focal": 8.5, "composition": 8.5,
                       "color": 8.5, "detail": 8.5, "craft": 8.5,
                       "typography": 9.0, "originality": 8.5, "fidelity": 9.5},
            "note": "Ships above the 8.5 floor with no dimension below 7. Weakest remaining "
                    "dimensions are originality and the several mid-tone dimensions at 8.5; "
                    "the exploded-isometric register is inherently adjacent to technical-deck "
                    "visual language, mitigated by the empty-tray metaphor and the dimensioned "
                    "fifteen-day gap, which are specific to this story and to no other."
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
