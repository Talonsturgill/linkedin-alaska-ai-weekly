# Art plan — The Stack — 10 JUL 2026

## 0. Story absorbed
- What happened: This week the Alaska DOH Commissioner issues final funding decisions on 403 applications for a $272.2M CMS Rural Health Transformation award.
- Why it matters to Alaska: a fixed federal health-capital tranche is routed to a single state officer who alone decides who anchors the state's FHIR-native rural health data (and future health-AI) infrastructure.
- Emotional register: tense, sober, weighty. A vast flow forced through one point. Not triumphant, not snarky. The feeling is *concentration* — everything narrows to a single desk.

## 1. Concept statement
A broad river of federal capital pours downward and is forced through a single luminous throat, one desk, before fanning out below into a field of 403 small applicant plots of which only a handful catch the light. The reader gets, in half a second, "huge money, one gate, few winners."

## 2. Register carried by palette/forms
Dark spruce ground so the gold current glows like money and light. The value gap is severe on purpose. The throat is the single brightest point on the darkest surround, so the eye is dragged to the chokepoint the way the mechanism drags the money there. Forms are flowing streamlines (a current), not a mechanical diagram, because this is a capital flow, not a machine.

## 3. Style family
`flow_field` (angle-field streamlines colored by a ramp). The atlas names it explicitly for "currents: capital, data, migration" — a precise fit for a federal capital flow. WHY it fits: the mechanism IS a flow that narrows. Dedup check: last 3 bespoke Stack pieces were swiss_grid (8 Jul), cadastral_ledger (7 Jul-02), iso_cutaway (7 Jul). flow_field is NOT in the forbidden last-8 style set. hue_family gold is NOT in the forbidden last-4 (neutral-cool, red, blue-teal). Composition `converging_funnel` is NOT in the forbidden last-2 (modular_grid, central_icon). Clean on all cooldowns.

## 4. Palette (OKLCH-built, hue_family = gold)
- paper: #f3ead4 warm cream (L~0.92) — thin edges + type only.
- ground: #10261c deep spruce green-black (L~0.20) — the dark field the current glows against. Value floor.
- current bronze: #6b4a1e (L~0.40) — the coolest/darkest gold, current edges/far.
- current amber: #c8892f (L~0.66) — mid current body.
- current gold: #f0bf55 (L~0.80) — bright current near the throat.
- throat white-gold: #fdeec2 (L~0.94) — the incandescent focal, highest chroma+value, wins the contrast war.
- type gold: #f2c14e for accents.
Value spine: throat (0.94) vs ground (0.20) = a full-range gap at the focal. Grayscale squint test: the throat is the one white blob on black, reads instantly.

## 5. Composition map (`converging_funnel`, 1080 grid)
- Throat / focal (the ONE DESK): center at (566, 648), slightly right-of-center and on the lower-third band, so the headline in the upper-left has clean air and the current sweeps a diagonal into it.
- Upper current: streamlines seeded across the whole top, vector field pulls them DOWN and INWARD toward the throat above y=648 (convergence).
- Lower fan: below y=648 the field pushes streamlines DOWN and OUTWARD (divergence), a widening delta to the bottom edge.
- Throat structure: a small dark horizontal desk-slab glyph (~140px wide, ~26px tall) centered on the throat with a bright knockout gate-slit above it, ringed by a hot glow r~150.
- 403 applicant plots: a fanned scatter of ~403 tiny ticks in the lower delta region (y 720-1000, x 120-960), the vast majority dark bronze, ~18 lit bright gold (the handful of winners). A mono count label "403 APPLICANTS" sits at the fan.
- Headline block: upper-left, quiet zone. "ONE DESK" baseline ~y176, "DECIDES" baseline ~y268, Fraunces Black ~92px, gold-cream, over a soft-panel to guarantee 4.5:1. Supporting mono line "$272M FEDERAL HEALTH AWARD" at (96, 300).
- Wordmark ALASKA.AI: bottom-left chip (96, 1006), mono-adjacent Fraunces ~30px.
- Kicker line "THE STACK · SOVEREIGNTY · 10 JUL 2026": JetBrains Mono ~17px tracked, bottom band centered baseline ~y1028 OR top-right; place bottom-center (540, 1030).
- Polaris colophon: top-right (986, 78) r=13, the one cool spark.
- Eye path: headline (upper-left) → gold current sweeping down-right → THROAT focal (bright, center-low) → fan of 403 below.

## 6. Layer build order (back to front)
1. paper base + vertical ground gradient (green-black, faintly warmer at the throat band).
2. faint far current (low-alpha bronze streamlines, wide, calm) for depth.
3. main current streamlines (amber→gold ramp by proximity to throat), converging above / diverging below.
4. throat glow (hot gold radial) UNDER the desk glyph.
5. 403 applicant fan (dark ticks + ~18 lit) in the lower delta.
6. desk-slab glyph + gate-slit knockout at the throat, crisp edges.
7. micro pass: glints/sparks at the throat, stipple grain in the ground, a few brighter current filaments.
8. texture identity: grain (mono, ~6) over all; gentle vignette to seat the focal.
9. type: soft-panel, headline, supporting line, kicker, wordmark chip, polaris.

## 7. Technique stack
`gradient_v` (ground) · custom analytic angle field (converge/diverge hourglass) + `streamlines` (the current, min_dist packing) · `ramp` (gold value ramp for line color) · `glow` (throat + winner sparks) · `stipple`/`chips` (403 fan + micro) · `grain` + `vignette` (finish) · `soft_panel` + `fraunces`/`mono`/`chip`/`polaris` (type + marks). Params: streamlines n~1100, step~3.0, length (120,420), min_dist~5; grain 6; vignette 0.20.

## 8. Risk list + mitigation
1. Muddy midtones where amber current meets green ground. Mitigation: keep ground very dark (L~0.20) and current gold high-chroma; enforce the value gap; grayscale-check each render.
2. Headline collides with the busy current in the upper-left. Mitigation: seed fewer streamlines in the upper-left quiet zone (mask the seed region) AND lay a soft_panel behind the headline; verify 4.5:1.
3. The throat reads as a vague blob, not a desk/gate. Mitigation: draw a crisp geometric desk-slab + a hard bright gate-slit knockout so the focal has an unmistakable man-made edge against the organic current.
4. 403 fan reads as random noise. Mitigation: arrange the ticks on a fanned radial from the throat (they clearly emanate from the gate), light exactly a small handful bright so the "few winners" reads.
5. flow_field looking like generic Perlin flow (atlas warns against this). Mitigation: the field is a purpose-built converge/diverge hourglass, not smooth Perlin — the pinch is the whole point and is visually explicit.
