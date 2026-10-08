import sys, math
sys.path.insert(0, ".claude/skills/alaska-ai-artwork")
import numpy as np
import art_kit as A

SEED = 2026100801
rng = np.random.default_rng(SEED)
c = A.Canvas(bg="#e9dcc3")
SKY_T, SKY_B = "#2b2f63", "#f0b86a"
A.gradient_v(c, (0, 0, 1080, 700), SKY_T, SKY_B, ease=1.1)
A.glow(c, 380, 640, 330, "#ffd98a", alpha=110)
# stars in the upper sky
for _ in range(70):
    x, y = rng.uniform(0, 1080), rng.uniform(0, 330)
    A.circle(c, x, y, rng.uniform(0.6, 1.5), fill="#f4ead2")
# ridges
R = [(650, 190, "#8b86b4", 2.6, 1), (690, 150, "#5a5d95", 3.2, 2), (730, 110, "#3a3e78", 3.8, 3)]
for yb, amp, col, sc, sd in R:
    A.ridge_fill(c, yb, amp, col, scale=sc, seed=sd)
    # snow-cap glints on the ridge lines
    pts = A.ridge_pts(yb, amp, scale=sc, seed=sd)
    A.line(c, A.wobble_pts(pts, 1.2, seed=sd), A.mix(col, "#f4ead2", 0.45), width=1.4)
# skyline
base = 770
x = 40
while x < 760:
    w = rng.uniform(26, 62); h = rng.uniform(30, 150) * (1.4 if 200 < x < 420 else 0.8)
    A.poly(c, [(x, base), (x, base - h), (x + w, base - h), (x + w, base)], fill="#1c1f4a")
    for wy in np.arange(base - h + 10, base - 8, 14):
        for wx in np.arange(x + 6, x + w - 8, 12):
            if rng.random() < 0.22:
                A.poly(c, [(wx, wy), (wx + 5, wy), (wx + 5, wy + 7), (wx, wy + 7)], fill="#ffc72c")
    x += w + rng.uniform(2, 10)
# foreground ground
A.ridge_fill(c, 850, 40, "#14163a", scale=2.0, seed=9)
A.poly(c, [(0, 880), (1080, 880), (1080, 1080), (0, 1080)], fill="#14163a")
# streetlight-style pole with camera
px = 820
A.poly(c, [(px - 7, 880), (px + 7, 880), (px + 4, 470), (px - 4, 470)], fill="#0c0e28")
A.poly(c, [(px - 6, 470), (px - 70, 470), (px - 70, 460), (px + 6, 460)], fill="#0c0e28")
# camera housing
A.poly(c, [(px - 118, 438), (px - 62, 430), (px - 56, 482), (px - 112, 490)], fill="#0c0e28")
A.circle(c, px - 130, 452, 22, fill="#0c0e28")
A.glow(c, px - 138, 455, 120, "#ffc72c", alpha=120)
A.circle(c, px - 138, 455, 15, fill="#ffc72c")
A.circle(c, px - 140, 452, 6, fill="#fff0c8")
# sight lines from lens toward the city
for ang in (-0.30, -0.10, 0.12):
    ex = 150; ey = 455 + math.tan(ang) * (px - 138 - ex) + 120
    A.line(c, [(px - 150, 458), (ex, ey)], "#ffc72c", width=1.2)
# micro: ground chips
A.chips(c, 160, (0, 885, 1080, 1075), size=(2, 6), colors=("#2b2f63", "#454a82"), seed=4)
# finishing
c.img = A.grain(c, amount=6, seed=SEED) or c.img if False else c.img
A.grain(c, amount=6, seed=SEED)
# type
cream = "#f4ead2"
f1 = A.fraunces(c, 92, weight=900, opsz=144)
A.text(c, (72, 92), "Anchorage Surveillance", f1, cream) if False else None
A.text(c, (72, 88), "Anchorage", f1, cream)
A.text(c, (72, 184), "Surveillance Rules", A.fraunces(c, 82, weight=900), cream)
A.text(c, (72, 282), "Wait On Oct. 20", A.fraunces(c, 54, weight=500, italic=True, soft=60), "#ffc72c")
A.text(c, (72, 986), "ALASKA.AI", A.fraunces(c, 34, weight=900), cream)
A.text(c, (72, 1028), "ANCHORAGE DESK · MUNICIPAL · 8 OCT 2026", A.mono(c, 16), "#c9c4e6", tracking=0.18)
A.polaris(c, 990, 96, r=14)
meta = {"date": "8 OCT 2026", "column": "Anchorage Desk", "kicker": "ANCHORAGE DESK",
        "middle_slot": "MUNICIPAL", "headline": "Anchorage Surveillance Rules\nWait On Oct. 20",
        "byline": "", "volume": "MUNICIPAL",
        "style_family": "wpa_layered", "palette": ["#2b2f63", "#f0b86a", "#5a5d95", "#14163a", "#ffc72c", "#f4ead2"],
        "hue_family": "indigo", "composition": "thirds_focal",
        "motifs": ["surveillance camera", "Chugach ridges", "city skyline"],
        "technique_stack": ["gradient_v", "ridge_fill", "glow", "grain"], "seed": SEED,
        "eval_history": [{"iter":1,"weighted":8.5,"weakest":"detail"}], "eval_final": {"weighted":8.5,"scores":{"concept":8,"focal":9,"composition":8,"color":9,"detail":7,"craft":8,"typography":9,"originality":8,"fidelity":9}}}
c.finish("out/post_image.png", meta)
