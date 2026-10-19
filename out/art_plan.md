# Anchorage Desk cover art — 2026-08-07

## Step 0 — Absorb the story

- **What happened.** Anchorage Police Chief Sean Case brought a roughly
  $600,000 three-year Thundercat Technology contract to the Assembly on 4
  August 2026 to expand the Real-Time Crime Center, and the vote was
  postponed to 18 August over the absence of any binding surveillance code.
- **Why it matters to Alaska.** The municipality is being asked to fund more
  automated license-plate and object-recognition capability on a network of up
  to 750 cameras before it has written a single enforceable rule on
  collection, access, or retention.
- **Emotional register.** Tense, cautionary, civic. Not triumphant, not
  outraged. The feeling is asymmetry — hardware dense, governance blank.

## Step 1 — Dedup scan

Scanned the 16 most recent `claude/linkedin-*` branches by date.

- **Forbidden style_family (last 8).** organic_rd_moorage, ukiyo_bokashi,
  wpa_layered_minimal_line, geologic_engraving, paper_collage,
  bathymetric_blueprint, flow_field, swiss_grid.
- **Forbidden hue_family (last 4).** teal, magenta, orange, green.
- **Forbidden composition (last 2).** thirds_focal, diagonal_thrust.
- **Recent motifs to avoid.** moored land raft, fraying filament, muskeg,
  catwalk, lit clinic, spruce stand, lit hub settlements, satellite node,
  relay towers, ore body, strata, torn paper drift, red pen, subsea fiber,
  bathymetric contours, capital funnel, modular offer grid, transmission
  tower, exploded fuel stack, gate iris, data-center block.

Chosen `constructivist_scatter` / `blue` / `scatter_field` all clear every
cooldown.

## Step 2 — Concept (three generated, one chosen)

1. **Camera iris containing a blank page.** One huge lens whose pupil holds an
   empty statute page. Rejected — "gate iris" was used on 7 Jul and an iris
   reads as generic tech.
2. **Ordinance page as an architectural slab under a constellation of
   lenses.** Strong, but the slab reads as a monument and softens the tension.
3. **CHOSEN — the crowded field and the empty page.** A dense scatter of
   surveillance cameras fills the night, every one of them aimed at a single
   bone-white ruled page that has nothing written on it. The hardware is
   installed, numerous, and pointed. The page that is supposed to govern it is
   blank.

**Concept statement.** The capability is already built and aimed; the rule
that governs it is an empty ruled page. Read in half a second — many
cameras, one blank sheet, and the blankness is the point.

**Why it's true to the story.** Every guardrail Case cited is internal APD
policy. Anchorage code sets no binding limit on collection, access, or
retention. The negative space in this piece is the governance gap.

## Step 3 — Blueprint

**Register carried by.** Cold night blue for institutional surveillance,
one warm bone rectangle as the only human-scale, hand-made-feeling object.
A single red record dot supplies the charge without turning the piece into
an alarm.

**Style family.** `constructivist_scatter` — a deliberate hybrid of
constructivist geometry (hard-edged forms, strong figure/ground, one
saturated accent) with a `scatter_field` composition. Fits a contested
procurement decision. Clears all cooldowns.

**Palette (value spine first).**

| role | hex | OKLCH-ish L | note |
|---|---|---|---|
| paper / focal | `#ece3d2` | 0.91 | the blank ordinance page, wins the contrast war |
| page shadow | `#b9ad97` | 0.72 | page edge, keeps it from floating |
| lens metal | `#6f7fae` | 0.56 | camera bodies, mid value |
| field mid | `#1b2550` | 0.28 | lower sky, street grid |
| ink / deep | `#0a0f28` | 0.14 | upper night, silhouette darks |
| accent | `#d2402c` | 0.55 high chroma | one record light only |
| brand gold | `#ffc72c` | — | polaris + kicker rule only |

Darkest dark sits top-left and behind the headline. Lightest light is the
page at lower-left. Grayscale squint test still reads because the page is
the only value above 0.8 in the frame.

**Composition map (`scatter_field`, 1080 grid).**

- Night field full bleed, `gradient_v` from `#0a0f28` (y=0) to `#1b2550`
  (y=1080).
- Faint street grid across the whole canvas, rotated 6°, 44px pitch, alpha
  low. Anchorage bowl as substrate, never as subject.
- Headline block `x ∈ [88, 992]`, first baseline y≈150, two lines, Fraunces
  Black auto-fit, leading 1.06. Top band y<300 kept camera-free plus a soft
  dark scrim so type never sits on texture.
- Kicker `ANCHORAGE DESK · MUNICIPAL · 7 AUG 2026` mono 16px, tracked 0.24em,
  centered under the headline at y≈296, with a 120px gold hairline above it.
- **Blank ordinance page** `x ∈ [118, 470]`, `y ∈ [452, 916]`, rotated -2.5°,
  hard offset shadow at +10/+12. 12 ruled lines at 34px pitch, all empty.
  One mono label `ANCHORAGE CODE` at the page head (traceable to the dossier
  line that Anchorage code contains no binding surveillance rules).
- **Camera scatter**, ~108 units, sizes 16 to 58px, occupying the right two
  thirds and the lower band, every unit rotated to aim at the page centroid
  (294, 684). Density highest at the right edge, thinning to nothing within
  70px of the page.
- **Nearest lens** at (566, 742), size 58, carries the single red record dot.
  Secondary focal, terminates the eye path.
- Polaris at (952, 86), r=13.
- `ALASKA.AI` wordmark bottom-left (118, 992), Fraunces Black 30px, bone.

**Eye path.** Headline → blank page (brightest object) → the crowd of lenses
aimed at it → red record dot → wordmark.

**Layer build order.** night gradient → street grid → dark scrim under
headline → camera scatter (back rows small and dimmed toward the field
color, front rows larger and cooler) → page shadow → page → page rules and
label → red dot on nearest lens → grain → vignette → type → brand marks.

**Technique stack.** `gradient_v`, `line` for the grid, `poly` and `circle`
for camera geometry, `wobble_pts` on the page outline for hand-made edge,
`mottle` on the page fill, `chips` for mount debris, `stipple` at the page
tooth, `glow` on the record dot, `grain` 6, `vignette` 0.16, `fraunces`,
`mono`, `polaris`.

**Three scales of detail.**
- MACRO — night field, headline mass, page, camera crowd.
- MESO — each camera is a composed silhouette (housing trapezoid, lens
  cylinder, sun hood, mount arm, wall plate), the page has 12 rules and a
  head label, the grid has streets.
- MICRO — lens glints, housing seams, mount bolts, `chips` debris near
  mounts, `stipple` tooth on the page, glow bloom on the record dot.

**Risk list.**
1. *Camera glyphs read as blobs at 300px.* Mitigation — each unit is a hard
   trapezoid + cylinder + arm, checked as a black fill silhouette; minimum
   feature 2.5 design px; back rows dimmed rather than shrunk below 16px.
2. *Headline collides with the busy scatter.* Mitigation — camera-free band
   above y=300 plus a soft dark scrim, and `ensure_contrast` on the type.
3. *Mud in the midtones between lens metal and field.* Mitigation — only five
   inks, a forced value gap of ~0.28 L between lens metal and field mid, and
   back rows mixed toward the field color so they read as depth not sludge.
