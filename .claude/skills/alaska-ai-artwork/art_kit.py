"""
art_kit — the Alaska.Ai bespoke-artwork rendering library.

Design contract:
  * Everything in the public API works in DESIGN SPACE: a 1080 x 1080
    float coordinate system. The Canvas supersamples internally (default
    2x) and downsamples with Lanczos on finish() for crisp edges.
  * Colors are hex strings ("#0b2545") everywhere in the public API.
  * Every stochastic helper takes an explicit `seed` so a render is
    reproducible from its committed art_script.py + meta.json.
  * Optional deps (opensimplex, shapely, coloraide) are used when
    present and silently replaced with numpy/colorsys fallbacks when
    not, so an unattended run NEVER dies on a missing package.

The kit provides primitives, not compositions. The artist (the model)
writes a fresh art_script.py per issue that composes these into a piece
no prior issue has made. See SKILL.md for the brain.
"""

import colorsys
import datetime as _dt
import json
import math
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import gaussian_filter, zoom

try:
    import opensimplex as _osx
    HAS_SIMPLEX = True
except Exception:
    HAS_SIMPLEX = False

try:
    from shapely.geometry import (LineString, MultiPolygon, Point, Polygon,
                                  box as shp_box)
    from shapely.ops import unary_union
    HAS_SHAPELY = True
except Exception:
    HAS_SHAPELY = False

try:
    from coloraide import Color as _Color
    HAS_COLORAIDE = True
except Exception:
    HAS_COLORAIDE = False

DESIGN = 1080  # design-space edge length


# ----------------------------------------------------------------------
# color — OKLCH-first, perceptually honest
# ----------------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[max(0, min(255, int(round(v)))) for v in rgb])


def oklch(l, c, h):
    """Make a hex color from OKLCH (l 0..1, c 0..0.37ish, h degrees).
    Perceptually uniform: equal l steps LOOK equal across hues."""
    if HAS_COLORAIDE:
        col = _Color("oklch", [l, c, h % 360]).convert("srgb").fit("srgb")
        return col.to_string(hex=True)
    # fallback: HLS approximation (less uniform, still usable)
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, min(1.0, c * 3))
    return rgb_to_hex((r * 255, g * 255, b * 255))


def to_oklch(hexstr):
    """hex -> (l, c, h) tuple. Fallback returns an HLS approximation."""
    if HAS_COLORAIDE:
        c = _Color(hexstr).convert("oklch")
        return (c["lightness"], c["chroma"], c["hue"] if c["hue"] == c["hue"] else 0.0)
    r, g, b = [v / 255 for v in hex_to_rgb(hexstr)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (l, s / 3, h * 360)


def mix(c1, c2, t):
    """Perceptual mix of two hex colors, t in 0..1."""
    if HAS_COLORAIDE:
        i = _Color.interpolate([c1, c2], space="oklch")
        return i(t).convert("srgb").fit("srgb").to_string(hex=True)
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return rgb_to_hex([a[i] + (b[i] - a[i]) * t for i in range(3)])


def ramp(stops, n):
    """n hex colors interpolated through a list of hex stops (OKLCH path)."""
    if n == 1:
        return [stops[0]]
    if HAS_COLORAIDE:
        i = _Color.interpolate(stops, space="oklch")
        return [i(k / (n - 1)).convert("srgb").fit("srgb").to_string(hex=True)
                for k in range(n)]
    out = []
    for k in range(n):
        t = k / (n - 1) * (len(stops) - 1)
        j = min(int(t), len(stops) - 2)
        out.append(mix(stops[j], stops[j + 1], t - j))
    return out


def lighten(c, amt):
    l, ch, h = to_oklch(c)
    return oklch(min(1.0, l + amt), ch, h)


def darken(c, amt):
    return lighten(c, -amt)


def saturate(c, amt):
    l, ch, h = to_oklch(c)
    return oklch(l, max(0.0, ch + amt), h)


def contrast(c1, c2):
    """WCAG 2.1 contrast ratio between two hex colors."""
    def lum(c):
        r, g, b = [v / 255 for v in hex_to_rgb(c)]
        r, g, b = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
                   for v in (r, g, b)]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    l1, l2 = lum(c1), lum(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def ensure_contrast(fg, bg, minimum=4.5):
    """Nudge fg lightness away from bg until the WCAG ratio holds."""
    if contrast(fg, bg) >= minimum:
        return fg
    l, c, h = to_oklch(fg)
    bl, _, _ = to_oklch(bg)
    step = 0.04 if bl < 0.5 else -0.04
    for _ in range(24):
        l = min(1.0, max(0.0, l + step))
        cand = oklch(l, c, h)
        if contrast(cand, bg) >= minimum:
            return cand
    return "#ffffff" if bl < 0.5 else "#111111"


def harmony(base_hue, scheme="complementary"):
    """Return a list of OKLCH hue angles for a named harmony scheme.
    Schemes: complementary, split, triadic, analogous, mono_accent."""
    b = base_hue % 360
    return {
        "complementary": [b, (b + 180) % 360],
        "split":         [b, (b + 150) % 360, (b + 210) % 360],
        "triadic":       [b, (b + 120) % 360, (b + 240) % 360],
        "analogous":     [b, (b + 30) % 360, (b - 30) % 360],
        "mono_accent":   [b, b, (b + 180) % 360],
    }[scheme]


# ----------------------------------------------------------------------
# canvas
# ----------------------------------------------------------------------

class Canvas:
    """Supersampled painting surface. Public coords are design-space
    (1080 x 1080 floats); everything is scaled internally."""

    def __init__(self, bg="#f2ead9", ss=2, size=DESIGN):
        self.size = size
        self.ss = ss
        self.W = size * ss
        self.img = Image.new("RGB", (self.W, self.W), hex_to_rgb(bg))
        self.draw = ImageDraw.Draw(self.img, "RGBA")

    # -- coordinate scaling -------------------------------------------
    def s(self, v):
        return v * self.ss

    def pts(self, pts):
        return [(x * self.ss, y * self.ss) for x, y in pts]

    # -- layers --------------------------------------------------------
    def layer(self):
        """Transparent RGBA layer at internal resolution + its Draw."""
        im = Image.new("RGBA", (self.W, self.W), (0, 0, 0, 0))
        return im, ImageDraw.Draw(im, "RGBA")

    def mask(self):
        """L-mode mask layer (0=off, 255=on) + its Draw."""
        im = Image.new("L", (self.W, self.W), 0)
        return im, ImageDraw.Draw(im)

    def composite(self, layer, mask=None):
        if mask is not None:
            self.img.paste(layer, (0, 0), mask)
        else:
            self.img = Image.alpha_composite(self.img.convert("RGBA"),
                                             layer).convert("RGB")
        self.draw = ImageDraw.Draw(self.img, "RGBA")

    def paste_img(self, im, alpha=1.0):
        im = im.resize((self.W, self.W), Image.LANCZOS) \
            if im.size != (self.W, self.W) else im
        if alpha >= 1.0 and im.mode == "RGB":
            self.img = im.convert("RGB")
        else:
            base = self.img.convert("RGBA")
            over = im.convert("RGBA")
            if alpha < 1.0:
                a = over.getchannel("A").point(lambda v: int(v * alpha))
                over.putalpha(a)
            self.img = Image.alpha_composite(base, over).convert("RGB")
        self.draw = ImageDraw.Draw(self.img, "RGBA")

    # -- finish --------------------------------------------------------
    def finish(self, out_path, meta):
        """Downsample to 1080, save PNG + .meta.json sidecar."""
        final = self.img.resize((self.size, self.size), Image.LANCZOS)
        final.save(out_path, "PNG", optimize=True)
        meta = dict(meta)
        meta.setdefault("canvas", [self.size, self.size])
        meta["rendered_at_utc"] = _dt.datetime.utcnow().isoformat() + "Z"
        meta["out_path"] = str(out_path)
        Path(str(out_path) + ".meta.json").write_text(
            json.dumps(meta, indent=2))
        return out_path


# ----------------------------------------------------------------------
# noise fields (numpy arrays in 0..1, shape (h, w) at design resolution)
# ----------------------------------------------------------------------

def _value_octave(w, h, freq, rng):
    g = rng.random((max(2, int(freq)) + 1, max(2, int(freq)) + 1))
    return zoom(g, (h / g.shape[0], w / g.shape[1]), order=3)[:h, :w]


def field(scale=4.0, octaves=4, seed=0, persistence=0.5, w=DESIGN, h=DESIGN):
    """Fractal noise field. Simplex when available, value-noise fallback."""
    if HAS_SIMPLEX:
        _osx.seed(seed)
        acc = np.zeros((h, w))
        amp, total, freq = 1.0, 0.0, scale
        for _ in range(octaves):
            xs = np.linspace(0, freq, w)
            ys = np.linspace(0, freq, h)
            acc += amp * (_osx.noise2array(xs, ys) * 0.5 + 0.5)
            total += amp
            amp *= persistence
            freq *= 2.0
        return acc / total
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w))
    amp, total, freq = 1.0, 0.0, scale
    for _ in range(octaves):
        acc += amp * _value_octave(w, h, freq, rng)
        total += amp
        amp *= persistence
        freq *= 2.0
    return acc / total


def ridged(f):
    """Turn a 0..1 field into sharp ridges (mountains, veins)."""
    return 1.0 - np.abs(f * 2.0 - 1.0)


def warp(f, strength=60.0, scale=3.0, seed=1):
    """Domain-warp a field by two other noise fields. Organic, non-cliché."""
    h, w = f.shape
    dx = (field(scale, 3, seed + 11, w=w, h=h) - 0.5) * 2 * strength
    dy = (field(scale, 3, seed + 29, w=w, h=h) - 0.5) * 2 * strength
    ys, xs = np.mgrid[0:h, 0:w]
    xs = np.clip(xs + dx, 0, w - 1).astype(int)
    ys = np.clip(ys + dy, 0, h - 1).astype(int)
    return f[ys, xs]


def noise1d(n, scale=4.0, octaves=3, seed=0):
    """1-D fractal noise in 0..1, length n. Ridgelines, torn edges."""
    return field(scale, octaves, seed, w=n, h=1)[0]


def reaction_diffusion(steps=3000, f=0.037, k=0.06, seed=0, res=216,
                       feed_mask=None):
    """Gray-Scott reaction-diffusion. Returns a 0..1 field at design res.
    (f,k) picks the morphology: (0.037,0.06) worms · (0.03,0.062) spots
    · (0.055,0.062) coral/maze · (0.025,0.055) waves. Runs coarse, then
    upsamples — cutting-edge texture for organic/biological metaphors."""
    rng = np.random.default_rng(seed)
    U = np.ones((res, res))
    V = np.zeros((res, res))
    n_seeds = 12
    for _ in range(n_seeds):
        cx, cy = rng.integers(8, res - 8, 2)
        U[cy - 4:cy + 4, cx - 4:cx + 4] = 0.5
        V[cy - 4:cy + 4, cx - 4:cx + 4] = 0.25
    Du, Dv, dt = 0.16, 0.08, 1.0
    fm = f if feed_mask is None else f * (0.6 + 0.8 * zoom(
        feed_mask, (res / feed_mask.shape[0], res / feed_mask.shape[1]),
        order=1)[:res, :res])
    for _ in range(steps):
        Lu = (np.roll(U, 1, 0) + np.roll(U, -1, 0) +
              np.roll(U, 1, 1) + np.roll(U, -1, 1) - 4 * U)
        Lv = (np.roll(V, 1, 0) + np.roll(V, -1, 0) +
              np.roll(V, 1, 1) + np.roll(V, -1, 1) - 4 * V)
        UVV = U * V * V
        U += (Du * Lu - UVV + fm * (1 - U)) * dt
        V += (Dv * Lv + UVV - (fm + k) * V) * dt
    V = (V - V.min()) / (V.max() - V.min() + 1e-9)
    return zoom(V, DESIGN / res, order=3)[:DESIGN, :DESIGN]


def field_img(f, dark, light, gamma=1.0):
    """Map a 0..1 field to an RGB image between two hex colors."""
    f = np.clip(f, 0, 1) ** gamma
    d, l = np.array(hex_to_rgb(dark), float), np.array(hex_to_rgb(light), float)
    arr = (d[None, None] * (1 - f[..., None]) + l[None, None] * f[..., None])
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def field_mask(f, threshold=0.5, soft=0.0):
    """0..1 field -> L mask. soft>0 feathers the cut in field units."""
    if soft <= 0:
        m = (f >= threshold).astype(np.uint8) * 255
    else:
        m = np.clip((f - (threshold - soft)) / (2 * soft), 0, 1) * 255
    return Image.fromarray(m.astype(np.uint8), "L")


# ----------------------------------------------------------------------
# flow fields (Tyler Hobbs-style, with collision option)
# ----------------------------------------------------------------------

def angle_field(scale=3.0, seed=0, turns=1.0, quantize=None, base=0.0):
    """Angle grid (radians) over design space from fractal noise.
    quantize=N snaps angles to N steps -> sculpted/rocky flows."""
    a = field(scale, 4, seed) * math.tau * turns + base
    if quantize:
        step = math.tau / quantize
        a = np.round(a / step) * step
    return a


def streamlines(angles, n=400, step=3.0, length=(60, 240), seed=0,
                min_dist=0.0, margin=0.15, curl=0.0):
    """Trace polylines through an angle field. Returns list[list[(x,y)]].
    min_dist>0 enforces spacing via an occupancy grid (even packing).
    curl adds constant rotation per step (spirals)."""
    h, w = angles.shape
    rng = np.random.default_rng(seed)
    occ = None
    cell = max(2.0, min_dist)
    if min_dist > 0:
        occ = np.zeros((int(h / cell) + 2, int(w / cell) + 2), bool)
    lines = []
    m = margin * w
    for _ in range(n):
        x = rng.uniform(-m, w + m)
        y = rng.uniform(-m, h + m)
        L = rng.uniform(*length) if isinstance(length, tuple) else length
        pts = []
        a_off = 0.0
        for _s in range(int(L / step)):
            xi, yi = int(np.clip(x, 0, w - 1)), int(np.clip(y, 0, h - 1))
            if occ is not None:
                ci, cj = int(y / cell), int(x / cell)
                if 0 <= ci < occ.shape[0] and 0 <= cj < occ.shape[1] and occ[ci, cj]:
                    break
            a = angles[yi, xi] + a_off
            x += math.cos(a) * step
            y += math.sin(a) * step
            a_off += curl
            pts.append((x, y))
        if len(pts) > 4:
            lines.append(pts)
            if occ is not None:
                for px, py in pts[::2]:
                    ci, cj = int(py / cell), int(px / cell)
                    if 0 <= ci < occ.shape[0] and 0 <= cj < occ.shape[1]:
                        occ[ci, cj] = True
    return lines


# ----------------------------------------------------------------------
# print-craft: halftone, riso overprint, grain, paper
# ----------------------------------------------------------------------

def halftone(c, f, cell=12.0, ink="#1a1a1a", angle=22.5, max_r=0.62,
             invert=False, region=None):
    """Draw a classic angled halftone screen of the 0..1 field onto the
    canvas. cell in design px. region=(x0,y0,x1,y1) clips."""
    h, w = f.shape
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    rgb = hex_to_rgb(ink)
    x0, y0, x1, y1 = region or (0, 0, w, h)
    diag = math.hypot(w, h)
    n = int(diag / cell) + 2
    for i in range(-n, n):
        for j in range(-n, n):
            gx, gy = i * cell, j * cell
            x = gx * ca - gy * sa + w / 2
            y = gx * sa + gy * ca + h / 2
            if not (x0 <= x < x1 and y0 <= y < y1):
                continue
            v = f[int(np.clip(y, 0, h - 1)), int(np.clip(x, 0, w - 1))]
            v = 1 - v if invert else v
            r = v * cell * max_r
            if r > 0.35:
                c.draw.ellipse([c.s(x - r), c.s(y - r), c.s(x + r), c.s(y + r)],
                               fill=(*rgb, 255))


def riso(c, paper, layers, seed=0, misreg=2.0):
    """Overprint semi-translucent ink layers multiply-style, each with a
    slight random registration offset — the risograph look.
    layers: list of (mask_L_image, ink_hex, opacity 0..1)."""
    rng = np.random.default_rng(seed)
    out = np.full((c.W, c.W, 3), np.array(hex_to_rgb(paper), float))
    for mask, ink, op in layers:
        dx, dy = rng.uniform(-misreg * c.ss, misreg * c.ss, 2)
        m = mask if mask.size == (c.W, c.W) else mask.resize((c.W, c.W))
        m = m.transform(m.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy))
        cov = np.asarray(m, float)[..., None] / 255.0 * op
        inkv = np.array(hex_to_rgb(ink), float)
        out *= (1 - cov) + cov * (inkv / 255.0)
    c.paste_img(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB"))


def grain(c, amount=7.0, seed=0, mono=True):
    """Film grain. amount = stddev in 8-bit units. Subtle: 4-9."""
    rng = np.random.default_rng(seed)
    arr = np.asarray(c.img, float)
    if mono:
        g = rng.normal(0, amount, arr.shape[:2])[..., None]
    else:
        g = rng.normal(0, amount, arr.shape)
    c.paste_img(Image.fromarray(
        np.clip(arr + g, 0, 255).astype(np.uint8), "RGB"))


def mottle(c, strength=0.06, scale=3.0, seed=3):
    """Big soft paper-tone blotches (multiply). strength 0.03-0.10."""
    f = field(scale, 3, seed, w=c.W // 4, h=c.W // 4)
    f = zoom(f, 4, order=3)[:c.W, :c.W]
    mul = 1.0 - strength * (f - 0.5) * 2
    arr = np.asarray(c.img, float) * mul[..., None]
    c.paste_img(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB"))


def vignette(c, strength=0.18, spread=1.35):
    ys, xs = np.mgrid[0:c.W, 0:c.W].astype(float)
    d = np.hypot(xs - c.W / 2, ys - c.W / 2) / (c.W / 2)
    mul = 1.0 - strength * np.clip(d / spread, 0, 1) ** 2
    arr = np.asarray(c.img, float) * mul[..., None]
    c.paste_img(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB"))


# ----------------------------------------------------------------------
# geometry (design-space; draws onto canvas or a provided draw)
# ----------------------------------------------------------------------

def poly(c, pts, fill=None, outline=None, width=2, d=None):
    dr = d or c.draw
    kw = {}
    if fill:
        kw["fill"] = (*hex_to_rgb(fill), 255) if isinstance(fill, str) else fill
    if outline:
        kw["outline"] = (*hex_to_rgb(outline), 255)
        kw["width"] = int(c.s(width))
    dr.polygon(c.pts(pts), **kw)


def line(c, pts, color, width=3, d=None):
    dr = d or c.draw
    dr.line(c.pts(pts), fill=(*hex_to_rgb(color), 255),
            width=max(1, int(c.s(width))), joint="curve")


def circle(c, cx, cy, r, fill=None, outline=None, width=2, d=None):
    dr = d or c.draw
    kw = {}
    if fill:
        kw["fill"] = (*hex_to_rgb(fill), 255)
    if outline:
        kw["outline"] = (*hex_to_rgb(outline), 255)
        kw["width"] = int(c.s(width))
    dr.ellipse([c.s(cx - r), c.s(cy - r), c.s(cx + r), c.s(cy + r)], **kw)


def blob_pts(cx, cy, r, wobble=0.16, harmonics=(1, 2, 3, 5), points=140,
             seed=0):
    """Organic closed shape: circle with summed sinusoidal radius wobble."""
    rng = np.random.default_rng(seed)
    amps = rng.uniform(0.2, 1.0, len(harmonics)) * wobble
    phases = rng.uniform(0, math.tau, len(harmonics))
    pts = []
    for i in range(points):
        t = i / points * math.tau
        rr = r * (1 + sum(a * math.sin(k * t + p)
                          for a, k, p in zip(amps, harmonics, phases)))
        pts.append((cx + math.cos(t) * rr, cy + math.sin(t) * rr))
    return pts


def ridge_pts(y_base, amp, scale=3.0, octaves=4, seed=0, x0=0, x1=DESIGN,
              step=4, ridge=True):
    """Mountain ridgeline: list of (x, y) across [x0, x1]."""
    n = int((x1 - x0) / step) + 1
    f = noise1d(n, scale, octaves, seed)
    if ridge:
        f = 1.0 - np.abs(f * 2 - 1)
    return [(x0 + i * step, y_base - f[i] * amp) for i in range(n)]


def ridge_fill(c, y_base, amp, fill, scale=3.0, octaves=4, seed=0,
               bottom=DESIGN, d=None):
    """Filled mountain layer down to `bottom`. Stack several with a
    lightness ramp for the layered-landscape (WPA/ukiyo-e) read."""
    pts = ridge_pts(y_base, amp, scale, octaves, seed)
    pts = [(pts[0][0], bottom)] + pts + [(pts[-1][0], bottom)]
    poly(c, pts, fill=fill, d=d)
    return pts


def wobble_pts(pts, amp=2.0, scale=8.0, seed=0):
    """Hand-drawn jitter: displace a polyline along its normals."""
    n = len(pts)
    f = noise1d(n, scale, 3, seed) - 0.5
    out = []
    for i, (x, y) in enumerate(pts):
        x0, y0 = pts[max(0, i - 1)]
        x1, y1 = pts[min(n - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        out.append((x + nx * f[i] * 2 * amp, y + ny * f[i] * 2 * amp))
    return out


def hand_line(c, pts, color, width=3, amp=1.8, seed=0, d=None):
    line(c, wobble_pts(pts, amp=amp, seed=seed), color, width, d=d)


def rays(c, cx, cy, n, r0, r1, color, width_deg=None, jitter=0.0, seed=0,
         d=None):
    """Deco/propaganda sunburst: n wedges radiating from (cx, cy)."""
    rng = np.random.default_rng(seed)
    wd = width_deg if width_deg is not None else 360 / n * 0.45
    for i in range(n):
        a = i / n * 360 + rng.uniform(-jitter, jitter)
        a0, a1 = math.radians(a - wd / 2), math.radians(a + wd / 2)
        pts = [(cx + math.cos(a0) * r0, cy + math.sin(a0) * r0),
               (cx + math.cos(a0) * r1, cy + math.sin(a0) * r1),
               (cx + math.cos(a1) * r1, cy + math.sin(a1) * r1),
               (cx + math.cos(a1) * r0, cy + math.sin(a1) * r0)]
        poly(c, pts, fill=color, d=d)


def iso(x, y, z, scale=1.0, origin=(540, 540)):
    """Isometric projection of (x, y, z) -> design-space (px, py)."""
    px = (x - y) * math.cos(math.radians(30)) * scale + origin[0]
    py = (x + y) * math.sin(math.radians(30)) * scale - z * scale + origin[1]
    return (px, py)


def iso_prism(c, x, y, z, dx, dy, dz, top, left, right, scale=1.0,
              origin=(540, 540), outline=None, d=None):
    """Isometric box with three shaded faces — diagram/cutaway language."""
    P = lambda a, b, cc: iso(a, b, cc, scale, origin)
    poly(c, [P(x, y, z + dz), P(x + dx, y, z + dz),
             P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)],
         fill=top, outline=outline, d=d)
    poly(c, [P(x, y + dy, z), P(x + dx, y + dy, z),
             P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)],
         fill=left, outline=outline, d=d)
    poly(c, [P(x + dx, y, z), P(x + dx, y + dy, z),
             P(x + dx, y + dy, z + dz), P(x + dx, y, z + dz)],
         fill=right, outline=outline, d=d)


def hatch(c, mask_img, spacing=9.0, angle=45.0, color="#222222", width=1.6):
    """Parallel-line shading clipped to an L mask (engraving read)."""
    layer, ld = c.layer()
    rad = math.radians(angle)
    ca, sa = math.cos(rad), math.sin(rad)
    diag = c.W * 1.5
    n = int(diag / c.s(spacing))
    rgb = hex_to_rgb(color)
    for i in range(-n, n):
        off = i * c.s(spacing)
        x0 = c.W / 2 - ca * diag - sa * off
        y0 = c.W / 2 - sa * diag + ca * off
        x1 = c.W / 2 + ca * diag - sa * off
        y1 = c.W / 2 + sa * diag + ca * off
        ld.line([(x0, y0), (x1, y1)], fill=(*rgb, 255),
                width=max(1, int(c.s(width))))
    m = mask_img if mask_img.size == (c.W, c.W) \
        else mask_img.resize((c.W, c.W))
    c.img.paste(layer, (0, 0), Image.composite(
        m, Image.new("L", (c.W, c.W), 0), layer.getchannel("A")))
    c.draw = ImageDraw.Draw(c.img, "RGBA")


def stipple(c, mask_img, density=0.12, r=(0.6, 1.6), color="#222222",
            seed=0):
    """Dot shading clipped to an L mask."""
    rng = np.random.default_rng(seed)
    m = np.asarray(mask_img.resize((c.W, c.W)), float) / 255.0
    n = int(density * (c.W / c.ss) ** 2 / 40)
    rgb = hex_to_rgb(color)
    for _ in range(n):
        x, y = rng.uniform(0, c.W, 2)
        if rng.random() < m[int(y), int(x)]:
            rr = c.s(rng.uniform(*r))
            c.draw.ellipse([x - rr, y - rr, x + rr, y + rr],
                           fill=(*rgb, 255))


def gradient_v(c, box, top, bottom, ease=1.0, bands=None, d=None):
    """Vertical gradient in a design-space box. bands=N posterizes it
    (deco); smooth default is the ukiyo-e bokashi read."""
    x0, y0, x1, y1 = box
    hgt = max(1, int(y1 - y0))
    ts = (np.arange(hgt) / max(1, hgt - 1)) ** ease
    if bands:
        ts = np.floor(ts * bands) / max(1, bands - 1)
    ts = np.clip(ts, 0.0, 1.0)
    cols = ramp([top, bottom], 256)
    dr = d or c.draw
    for i in range(hgt):
        col = cols[int(ts[i] * 255)]
        dr.rectangle([c.s(x0), c.s(y0 + i), c.s(x1), c.s(y0 + i + 1)],
                     fill=(*hex_to_rgb(col), 255))


def gradient_r(c, cx, cy, r, inner, outer, d=None):
    """Radial gradient (glow) drawn as concentric rings."""
    steps = 120
    dr = d or c.draw
    for i in range(steps, 0, -1):
        t = i / steps
        col = mix(inner, outer, t)
        rr = r * t
        dr.ellipse([c.s(cx - rr), c.s(cy - rr), c.s(cx + rr), c.s(cy + rr)],
                   fill=(*hex_to_rgb(col), 255))


def voronoi_polys(n=200, seed=0, bbox=(0, 0, DESIGN, DESIGN), relax=1):
    """n bounded Voronoi cells over bbox as point-lists. Lloyd-relaxed
    `relax` times for even, natural cells (ice floes, mosaic, fields,
    parcel maps). Uses mirrored seed points so every cell is finite."""
    from scipy.spatial import Voronoi
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = bbox
    pts = np.column_stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)])
    for _ in range(max(0, relax) + 1):
        mirrored = np.vstack([
            pts,
            np.column_stack([2 * x0 - pts[:, 0], pts[:, 1]]),
            np.column_stack([2 * x1 - pts[:, 0], pts[:, 1]]),
            np.column_stack([pts[:, 0], 2 * y0 - pts[:, 1]]),
            np.column_stack([pts[:, 0], 2 * y1 - pts[:, 1]]),
        ])
        vor = Voronoi(mirrored)
        cells = []
        new_pts = []
        for i in range(n):
            region = vor.regions[vor.point_region[i]]
            if -1 in region or not region:
                new_pts.append(pts[i])
                continue
            poly_pts = [tuple(vor.vertices[j]) for j in region]
            cells.append(poly_pts)
            new_pts.append(np.mean(poly_pts, axis=0))
        pts = np.array(new_pts)
    return cells


def chips(c, n, region, size=(3, 9), colors=("#dfe8ef",), seed=0,
          mask_img=None):
    """Scatter n small rotated shards (brash ice, gravel, confetti,
    debris) inside region=(x0,y0,x1,y1), optionally gated by an L mask."""
    rng = np.random.default_rng(seed)
    m = None
    if mask_img is not None:
        m = np.asarray(mask_img.resize((c.W, c.W)), float) / 255.0
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if m is not None and rng.random() > m[int(c.s(y)) - 1, int(c.s(x)) - 1]:
            continue
        s = rng.uniform(*size)
        a = rng.uniform(0, math.tau)
        k = rng.integers(3, 6)
        pts = []
        for j in range(k):
            t = a + j / k * math.tau + rng.uniform(-0.3, 0.3)
            rr = s * rng.uniform(0.55, 1.0)
            pts.append((x + math.cos(t) * rr, y + math.sin(t) * rr))
        poly(c, pts, fill=str(rng.choice(colors)))


# ----------------------------------------------------------------------
# shapely bridge (only if available) — boolean composition ops
# ----------------------------------------------------------------------

def geom_draw(c, geom, fill=None, outline=None, width=2, d=None):
    """Draw a shapely (Multi)Polygon with holes onto the canvas."""
    if not HAS_SHAPELY:
        raise RuntimeError("shapely not available")
    geoms = list(geom.geoms) if geom.geom_type.startswith("Multi") else [geom]
    for g in geoms:
        if g.is_empty or g.geom_type != "Polygon":
            continue
        if g.interiors:
            m, md = c.mask()
            md.polygon(c.pts(list(g.exterior.coords)), fill=255)
            for ring in g.interiors:
                md.polygon(c.pts(list(ring.coords)), fill=0)
            if fill:
                lay = Image.new("RGBA", (c.W, c.W),
                                (*hex_to_rgb(fill), 255))
                c.img.paste(lay, (0, 0), m)
                c.draw = ImageDraw.Draw(c.img, "RGBA")
        else:
            poly(c, list(g.exterior.coords), fill=fill, d=d)
        if outline:
            line(c, list(g.exterior.coords), outline, width, d=d)
            for ring in g.interiors:
                line(c, list(ring.coords), outline, width, d=d)


# ----------------------------------------------------------------------
# typography — Fraunces variable (opsz/wght/SOFT/WONK) + JetBrains Mono
# ----------------------------------------------------------------------

_SKILL_DIR = Path(__file__).parent.resolve()
_FONT_DIRS = [_SKILL_DIR / "fonts",
              _SKILL_DIR.parent / "alaska-ai-brief" / "fonts"]
_FONT_URLS = {
    "Fraunces-Var.ttf": ("https://raw.githubusercontent.com/google/fonts/"
                         "main/ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz"
                         "%2Cwght%5D.ttf"),
    "Fraunces-Italic-Var.ttf": ("https://raw.githubusercontent.com/google/"
                                "fonts/main/ofl/fraunces/Fraunces-Italic"
                                "%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf"),
    "JetBrainsMono-Regular.ttf": ("https://raw.githubusercontent.com/"
                                  "JetBrains/JetBrainsMono/master/fonts/ttf/"
                                  "JetBrainsMono-Regular.ttf"),
    "JetBrainsMono-Medium.ttf": ("https://raw.githubusercontent.com/"
                                 "JetBrains/JetBrainsMono/master/fonts/ttf/"
                                 "JetBrainsMono-Medium.ttf"),
}


def ensure_fonts():
    """Find fonts (shared with the brief skill) or download them from
    raw.githubusercontent.com (urllib, then curl as fallback)."""
    for d in _FONT_DIRS:
        if all((d / n).exists() and (d / n).stat().st_size > 1000
               for n in _FONT_URLS):
            return {n: str(d / n) for n in _FONT_URLS}
    d = _FONT_DIRS[0]
    d.mkdir(exist_ok=True)
    for n, url in _FONT_URLS.items():
        p = d / n
        if not p.exists() or p.stat().st_size < 1000:
            print(f"fetching {n}...", file=sys.stderr)
            try:
                urllib.request.urlretrieve(url, p)
            except Exception:
                os.system(f'curl -sfL "{url}" -o "{p}"')
            if not p.exists() or p.stat().st_size < 1000:
                raise RuntimeError(f"could not fetch font {n}")
    return {n: str(d / n) for n in _FONT_URLS}


_FONTS = None


def _fonts():
    global _FONTS
    if _FONTS is None:
        _FONTS = ensure_fonts()
    return _FONTS


def fraunces(c, size, weight=900, opsz=144, soft=0, wonk=0, italic=False):
    """Fraunces at design-space `size`. WONK=1 flips quirky letterforms —
    a flair lever no other feed uses. SOFT 0-100 rounds the serifs.
    Axes are set BY NAME from the font's own axis table, so weight
    always actually applies."""
    f = _fonts()
    name = "Fraunces-Italic-Var.ttf" if italic else "Fraunces-Var.ttf"
    fnt = ImageFont.truetype(f[name], int(c.s(size)))
    want = {"SOFT": soft, "WONK": wonk, "opsz": opsz, "wght": weight}
    try:
        axes = fnt.get_variation_axes()
        vec = []
        for ax in axes:
            nm = ax["name"]
            nm = nm.decode() if isinstance(nm, bytes) else str(nm)
            nm = nm.strip("\x00 ")
            key = {"soft": "SOFT", "softness": "SOFT", "wonk": "WONK",
                   "wonky": "WONK", "optical size": "opsz", "opsz": "opsz",
                   "weight": "wght", "wght": "wght"}.get(nm.lower(), nm)
            v = want.get(key, ax.get("default", 0))
            vec.append(max(ax["minimum"], min(ax["maximum"], v)))
        fnt.set_variation_by_axes(vec)
    except Exception:
        pass
    return fnt


def mono(c, size, medium=False):
    f = _fonts()
    n = "JetBrainsMono-Medium.ttf" if medium else "JetBrainsMono-Regular.ttf"
    return ImageFont.truetype(f[n], int(c.s(size)))


def text(c, xy, s, font, color, anchor="la", tracking=0.0, d=None,
         angle=0.0):
    """Draw text at design-space xy. tracking in em. angle rotates (deg,
    counterclockwise) around the anchor point via a temp layer."""
    dr = d or c.draw
    fill = (*hex_to_rgb(color), 255)
    if angle == 0.0 and tracking == 0.0:
        dr.text((c.s(xy[0]), c.s(xy[1])), s, font=font, fill=fill,
                anchor=anchor)
        return
    if angle == 0.0:
        _tracked(dr, c, xy, s, font, fill, anchor, tracking)
        return
    lay, ld = c.layer()
    _tracked(ld, c, (c.size / 2, c.size / 2), s, font, fill, "mm", tracking)
    lay = lay.rotate(angle, resample=Image.BICUBIC,
                     center=(c.W / 2, c.W / 2))
    dx, dy = c.s(xy[0]) - c.W / 2, c.s(xy[1]) - c.W / 2
    lay = lay.transform(lay.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy))
    c.composite(lay)


def _tracked(dr, c, xy, s, font, fill, anchor, tracking):
    extra = font.size * tracking
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in s]
    total = sum(widths) + extra * (len(s) - 1)
    x, y = c.s(xy[0]), c.s(xy[1])
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    va = anchor[1] if len(anchor) > 1 else "a"
    for ch, wch in zip(s, widths):
        dr.text((x, y), ch, font=font, fill=fill, anchor="l" + va)
        x += wch + extra

def measure(c, s, font, tracking=0.0):
    """Text width in design-space units."""
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in s]
    return (sum(widths) + font.size * tracking * (len(s) - 1)) / c.ss


def fit_size(c, s, max_w, lo=18, hi=200, tracking=0.0, **fr_kwargs):
    """Largest Fraunces size (design units) where s fits in max_w."""
    while hi - lo > 1:
        mid = (lo + hi) // 2
        f = fraunces(c, mid, **fr_kwargs)
        if measure(c, s, f, tracking) <= max_w:
            lo = mid
        else:
            hi = mid
    return lo


def chip(c, xy, s, font, fg, bg, pad=10, anchor="la", tracking=0.0,
         radius=6):
    """Text on a knockout chip — guarantees legibility on busy art."""
    w = measure(c, s, font, tracking)
    h = font.size / c.ss
    x, y = xy
    if anchor[0] == "m":
        x -= w / 2
    elif anchor[0] == "r":
        x -= w
    if len(anchor) > 1 and anchor[1] == "m":
        y -= h / 2
    elif len(anchor) > 1 and anchor[1] in ("s", "d"):
        y -= h
    c.draw.rounded_rectangle(
        [c.s(x - pad), c.s(y - pad * 0.7), c.s(x + w + pad),
         c.s(y + h + pad * 0.7)],
        radius=c.s(radius), fill=(*hex_to_rgb(bg), 255))
    text(c, (x, y), s, font, fg, anchor="la", tracking=tracking)


def soft_panel(c, box, color="#ffffff", alpha=110, blur=26, radius=24):
    """Soft blurred glow panel behind type — guarantees legibility on
    detailed art without a hard chip. box in design space."""
    lay, ld = c.layer()
    x0, y0, x1, y1 = box
    ld.rounded_rectangle([c.s(x0), c.s(y0), c.s(x1), c.s(y1)],
                         radius=c.s(radius),
                         fill=(*hex_to_rgb(color), alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(c.s(blur)))
    c.composite(lay)


def glow(c, cx, cy, r, color, alpha=60):
    """Soft radial light: sun glint, lamp, aurora hint. Non-destructive."""
    lay, ld = c.layer()
    ld.ellipse([c.s(cx - r), c.s(cy - r), c.s(cx + r), c.s(cy + r)],
               fill=(*hex_to_rgb(color), alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(c.s(r * 0.55)))
    c.composite(lay)


def polaris(c, cx, cy, r=16, color="#ffc72c", core="#fff0c8", halo=0.0):
    """The Alaska.Ai colophon: a small 5-point gold star. Every piece
    carries one somewhere — the only fixed pictorial brand element."""
    if halo > 0:
        gradient_r(c, cx, cy, r * halo, color, mix(color, "#000000", 0.999))
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    poly(c, pts, fill=color)
    circle(c, cx, cy, r * 0.22, fill=core)
