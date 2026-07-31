# The Stack — Art Plan — 2026-07-31

Column: THE STACK · REGULATORY · 31 JUL 2026
Headline: **ONE BUREAU SETS / ALASKA'S HEALTH / CIRCUIT PRICES**
Byline: `""` (not drawn for this column)

---

## Step 0 — Absorb the story

- **What happened.** The FCC votes 6 August on a third consecutive waiver letting
  Alaska's rural clinics reuse previously approved circuit prices instead of filing
  cost studies, and the Order quietly hands the FY2028 version of that decision to a
  single Wireline Competition Bureau division.
- **Why it matters to Alaska.** 285 of 317 Alaska Telecom Program requests in FY2024
  couldn't use the market-rate methods, so a temporary waiver has become the real rate
  regime for the circuits rural clinics run telehealth and AI-assisted diagnostics on.
- **Emotional register.** Quiet precariousness. Cold, procedural, watchful. Not alarm,
  not triumph. Something load-bearing turns out to be temporary, and almost nobody is
  looking at it. The palette and forms must feel still and a little exposed.

## Step 1 — Dedup scan (obeyed)

Scanned all `origin/claude/linkedin-*` branches carrying a bespoke meta ledger.

| date | column | style_family | hue_family | composition |
|---|---|---|---|---|
| 24 JUL | Stack | geologic_engraving | green | bilateral_gate |
| 24 JUL | Desk | paper_collage | neutral-warm | scatter_field |
| 17 JUL | Stack | bathymetric_blueprint | indigo | submerged_section |
| 10 JUL | Stack | flow_field | gold | converging_funnel |
| 8 JUL | Stack | swiss_grid | neutral-cool | modular_grid |
| 7 JUL (02) | Stack | cadastral_ledger | red | central_icon |
| 7 JUL | Stack | iso_cutaway | blue-teal | thirds_focal |

- **Forbidden style_family (last 8).** geologic_engraving, paper_collage,
  bathymetric_blueprint, flow_field, swiss_grid, cadastral_ledger, iso_cutaway, plus
  aurora_field permanently.
- **Forbidden hue_family (last 4).** green, neutral-warm, indigo, gold.
- **Forbidden composition (last 2).** bilateral_gate, scatter_field.
- **Forbidden motifs (last 10).** ore body, series valves, reticle, geologic strata,
  subsurface conduit, torn paper, red pen, subsea fiber, sluice gate, bathymetric
  contours, capital current, converging funnel, modular grid, transmission tower,
  exploded prism stack, gate iris, data-center block, cadastral plat, consent seal,
  survey ticks, north arrow.

**Chosen and cleared:** style `ukiyo_bokashi` (unused in the visible ledger), hue
`magenta` (clean against the last four), composition `diagonal_thrust` (clean against
the last two). Deliberately steering off the diagram-as-art register this column
usually loves, because the last four Stack pieces were all diagrammatic and the story
this week is about something physical being load-bearing, not about a flow chart.

## Step 2 — Three concepts

1. **The stamped stack.** Three waiver documents stacked, a fourth hovering, the fifth
   slot void. *Rejected.* Paper-and-stamp language is the 24 JUL Desk piece
   (`paper_collage`, torn paper, red pen), and a document pile is a generic policy
   illustration that could front any regulatory blog.
2. **The price cliff as a rate curve.** A literal escarpment shaped like the $485 to
   $2,908 step. *Rejected as a standalone.* It renders one number rather than the
   mechanism, and a chart-shaped landform reads as a hockey-stick chart, which the
   skill kills on sight.
3. **The temporary span. (CHOSEN)** A small lit clinic stands on a high ice terrace.
   The only thing connecting it to the low ground is a slender timber catwalk. Three
   props hold the catwalk up. The fourth socket is empty, and below it is open dark
   water.

**Why concept 3 is true to the story.** The catwalk *is* the waiver: a temporary
structure everyone now walks on as if it were permanent. The three props are the three
funding years already covered. The empty fourth socket is FY2028, the decision that
moves to one Bureau division and off any public agenda. The escarpment does double
duty as the non-linear price step, high ground reachable only by the temporary thing.
**Half-second read:** a small lit building depends on a walkway that is one prop short.

## Step 3 — Pre-production blueprint

### Concept statement
A rural clinic's light burns on the far side of an ice ravine, reachable only by a
slender catwalk propped up three times with the fourth prop missing. The temporary
span is the waiver, and the gap under it is the year nobody has decided yet.

### Register
Quiet precariousness. Cold blue snow against a burning magenta dusk, with one small
warm lamp as the only human warmth in the frame. Forms are flat and still (ukiyo-e
planes), so the single broken rhythm in the prop row does all the unease.

### Style family
`ukiyo_bokashi` with a fine engraved micro pass. Flat colour planes, fine outlines, a
smooth banded `gradient_v` sky (the bokashi), asymmetric composition, and an elevated
three-quarter viewpoint looking across the ravine rather than along it. Fits because
ukiyo-e is the tradition that renders snow, cliff and a small human structure with
maximum stillness and minimum clutter, and stillness is the register. Clears all
cooldowns (see Step 1).

### Palette (OKLCH-built, 6 inks + paper = 7 entries)

| hex | role | approx L |
|---|---|---|
| `#f4e7e3` | paper / lit snow, headline knockout | 0.93 |
| `#f2a98f` | sky low, warm horizon band | 0.79 |
| `#b0587f` | sky mid, magenta dusk | 0.56 |
| `#5a3a63` | sky top, plum | 0.36 |
| `#6a6f96` | snow shadow, cold terrace plane | 0.50 |
| `#22243a` | ice deep, silhouettes, type | 0.17 |
| `#ffb347` | clinic lamp, polaris (focal accent) | 0.78 |

**Value structure.** Darkest dark is `#22243a` (clinic silhouette, catwalk, props,
ravine). Lightest light is `#f4e7e3` (lit snow on the terrace tops). The focal wins the
contrast war three ways at once: it is the only warm hue in a cool/magenta field, it
carries the highest chroma, and it sits as a small bright point directly against the
darkest ink of the clinic silhouette. Grayscale check: the bright horizon band at
`#f2a98f` sits behind dark ridge and clinic silhouettes, so the focal reads even with
hue stripped, and the terrace tops step light/dark/light from front to back.

### Composition map — `diagonal_thrust` on the 1080 grid

- **Sky** `[0, 0, 1080, 640]`, bokashi `gradient_v` `#5a3a63` → `#b0587f` → `#f2a98f`,
  ease 1.25, brightest at the horizon.
- **Far ridge** silhouette, `ridge_pts` baseline y=612, amp 34, mixed 55% toward sky
  for atmosphere.
- **Low terrace (left)**, top surface `ridge_pts` from (0, 826) to (415, 838), amp 9.
  Body fills down to frame bottom in `#6a6f96` over `#22243a`.
- **High terrace (right)**, top surface `ridge_pts` from (648, 700) to (1080, 676),
  amp 8. Body fills down to frame bottom.
- **Ravine**, the gap x ∈ [415, 648], darkest mass `#22243a`, falling to the bottom
  edge. This is the negative space the whole composition pivots on.
- **Catwalk**, deck from (415, 822) to (648, 700). Length ≈ 264px, deck thickness 9px,
  ~22 plank seams, handrail line 26px above the deck on the far side.
- **Props**, verticals under the deck at x = 462, 516, 570, each ~11px wide, running
  from the deck underside down into shadow at y ≈ 1010. Cross-bracing X between
  adjacent props. **The fourth socket at x = 624 is EMPTY**: a broken stub ~26px tall,
  a dark void beneath it, and a hairline crack in the deck directly above.
- **Clinic**, footprint 118w × 74h with its base on the high terrace at (812, 700), so
  body y ∈ [626, 700]. Pitched roof apex at (871, 598). Three lit windows at
  y ≈ 652, each 17 × 22, in `#ffb347`. Stovepipe at (railing) x=916, y=612, with a thin
  smoke wisp.
- **Lamp glow**, `glow()` at (871, 655) r=104 `#ffb347` alpha 66. THE FOCAL.
- **Spruce**, 6 small dark conifers on the high terrace right of the clinic, x from 960
  to 1064, heights 46 down to 26, receding.
- **Headline block**, x ∈ [84, 610], first baseline y = 132, three lines, Fraunces
  wght 900 / opsz 144, leading 1.06, colour `#f4e7e3` knocked out of the plum sky.
  Occupies the quiet upper-left, entirely above the terrace tops and left of the
  clinic.
- **Kicker** `THE STACK · REGULATORY · 31 JUL 2026`, JetBrains Mono 16px, tracking
  0.24em, at (84, headline_bottom + 30), colour `#f2a98f`.
- **Wordmark** `ALASKA.AI`, Fraunces Black 29px, at (84, 1012), colour `#f4e7e3` on the
  dark low-terrace body.
- **Polaris**, (952, 128) r=13, colour `#ffb347`, small, in the plum upper sky.

**Eye path:** headline (upper-left) → down the catwalk's rising diagonal → the lit
clinic (right third) → back down to the missing prop → wordmark (bottom-left).

### Layer build order (back to front)
paper → sky bokashi gradient → stars + sky mottle → polaris → far ridge → high terrace
mass → high terrace voronoi snow-slab meso pass → low terrace mass → low terrace
voronoi meso pass → ravine dark mass + vertical ice hatch → terrace edge chips (broken
ice) → catwalk props + cross-bracing + broken stub → catwalk deck + plank seams +
handrail → clinic silhouette + roof + windows + stovepipe → lamp glow → spruce →
spindrift stipple → grain → headline → kicker → wordmark

### Technique stack
`gradient_v` (bokashi sky, ease 1.25) · `ridge_pts`/`ridge_fill` (terraces, far ridge)
· `voronoi_polys` (snow-slab cells on both terrace tops, ~90 cells each, relax 2, per
cell value jitter ±5%) · `hatch` (vertical ice texture on the ravine walls, spacing
7-9, angle 88) · `stipple` (spindrift and ravine depth, density 0.05-0.10) · `chips`
(broken ice at terrace edges, 40-60 pieces, size 3-8) · `wobble_pts`/`hand_line`
(catwalk, props, spruce, to take the digital edge off) · `glow` (clinic lamp) ·
`mottle` (sky, 0.035) · `grain` (single finishing identity, amount 6) · `polaris`.

### Risk list
1. **The catwalk reads as a generic bridge and the piece loses Alaska.** Mitigation:
   snow-slab terraces, spruce stand, spindrift, a cabin-profile clinic with a stovepipe,
   and a true sub-Arctic winter dusk palette. No generic infrastructure geometry.
2. **Headline collides with busy art.** Mitigation: the headline occupies upper-left
   sky only, x ≤ 610 and y ≤ ~330, while the high terrace top starts at y=676 and the
   catwalk's high end at y=700. The sky there is a smooth gradient with only faint
   mottle, so no chip is needed; `ensure_contrast` will verify `#f4e7e3` against the
   local plum before drawing.
3. **Mud where magenta sky meets blue snow.** Mitigation: hold a hard value gap at the
   horizon by placing the brightest sky band (`#f2a98f`, L≈0.79) directly against the
   dark far ridge and terrace silhouettes, and keep `#6a6f96` clearly cooler and
   darker than any sky value it touches.
4. **The missing fourth prop doesn't read, killing the concept.** Mitigation: three
   props on an even 54px rhythm so the eye expects the fourth; a broken stub at the
   expected position rather than nothing at all; cross-bracing that visibly stops; a
   hairline deck crack directly above the gap; and the darkest value in the frame
   directly beneath it.
