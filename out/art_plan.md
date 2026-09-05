# Art plan — Anchorage Desk — 4 SEP 2026

## Step 0 — Absorb the story
- **What happened.** A developer told FERC its 100 MW underwater AI data center
  off Nikiski was designed to tie into AEA's $400 million Cook Inlet PowerLink,
  and AEA's CEO said publicly that AEA was never contacted and the filing was
  wrong.
- **Why it matters to Alaska.** A claimed interconnection to a state-backed
  Railbelt asset does real work in a federal permitting record, and Alaska is
  simultaneously courting exactly this class of load.
- **Register.** Cool, corrective, dry. Not alarm, not triumph. The tone of a
  drafting correction made in public.

## Step 1 — Dedup check (cleared)
Forbidden style families (last 8): exploded_iso_docket, landmark_mesh, riso_form,
hydrographic_claim, engraved_headworks, voronoi_impoundment, constructivist_scatter,
organic_rd_moorage. Forbidden hues (last 4): blue, indigo, orange, green.
Forbidden compositions (last 2): exploded_iso_stack, thirds_focal.
This plan uses **halftone_section** (halftone_pop hybridized with blueprint line
grammar), hue family **red**, composition **horizon_band**. All clear.
Nearest prior neighbour is `bathymetric_blueprint` (stack, 17 JUL, 13 issues back,
outside every cooldown); differentiated hard by dropping the blue/contour language
entirely for a cream-and-graphite halftone section with a single red accent.

## Step 2 — Concept (three generated, one chosen)
1. **The gap that was asserted.** A water-column section. The PowerLink cable is
   solid, continuous, indifferent. A dashed "proposed" spur rises from a cluster of
   server hives, reaches for the cable, and stops short. The unclosed gap is the
   subject. **CHOSEN.**
2. An unanswered handset. Killed, generic, could run on any blog.
3. A hive field with no feed at all. Weaker, the absence has no edge to read against.

**Concept statement.** A drafted connection that does not touch the thing it
claims to touch. The reader gets it in half a second because the whole composition
is calm except for one small red gap that refuses to close.

## Step 3 — Blueprint
- **Style family.** `halftone_section`. Halftone-screened water field carries mass;
  blueprint line grammar (dashed spur, dimension ticks, small mono callouts) carries
  the claim. The screen says "real matter," the line says "paper assertion." That
  split IS the story.
- **Palette (OKLCH-built, logged as hex).**
  - paper cream `#efe7d8` (L≈0.93) — ground
  - water field graphite `#6f7378` (L≈0.62) — halftone mass, mid value
  - seabed shadow `#2f3236` (L≈0.30) — lower band, anchors composition
  - ink `#17191c` (L≈0.15) — cable, hives, turbine silhouettes, headline
  - correction red `#c02a1f` — ONLY on the dashed spur and the gap tick. Highest
    chroma in the piece, used on under 2% of the canvas.
  Value spine: paper 0.93 / field 0.62 / shadow 0.30 / ink 0.15. Grayscale check
  still reads because the gap is a light-on-dark void, not a hue trick.
- **Composition map (1080 grid), `horizon_band`.**
  - waterline y=300, thin Nikiski shore sliver x∈[0,240] at y≈292
  - water column band y∈[300,830], halftone screened, density rising with depth
  - seabed band y∈[830,1010], shadow value, `voronoi_polys` cobble cells + stipple
  - PowerLink cable, solid ink, y≈846, x∈[70,1010], slight `wobble_pts` sag
  - hive cluster centered (300, 905), 66 small hexagons in a low mound, ink,
    meso shading per hex, micro glints on ~8 of them
  - dashed red spur leaves the mound at (352, 880), arcs up-right, terminates at
    (612, 858). Cable at that x sits at y≈846. **Gap = 12px vertical, held in a
    deliberately quiet pocket of paper-light water.** Two red dimension ticks
    bracket it.
  - turbine rank, 5 rotors in silhouette, y≈470, x∈[640,1000], scale-diminishing
  - headline block x∈[84,600], top at y=96, knocked into the calm upper water
  - kicker line under headline at y≈232
  - wordmark bottom-left (84, 1000); polaris (966, 92) r=13
  - Eye path: headline → down the red dashes → the gap → along the cable out right
    → turbines → wordmark.
- **Layer build order.** paper + grain → water gradient → halftone screen pass →
  waterline + shore sliver → turbine silhouettes → seabed band → cobble cells →
  cable → hive mound (macro → per-hex meso → glint micro) → red spur + ticks →
  headline + kicker → wordmark + polaris → final grain.
- **Technique stack.** `gradient_v`, `field` + `warp` for water mottle, `halftone`
  (single texture identity), `voronoi_polys` for seabed cobble, `wobble_pts` for
  cable sag, `hand_line` for the dashed spur, `stipple` + `chips` micro, `grain` 6.
- **Risk list.**
  1. *The gap reads as an accident, not a statement.* Mitigation: red dimension
     ticks bracket it, and it sits in the lightest pocket of the water field so it
     is the highest local contrast on the canvas.
  2. *Halftone mud in the midtones.* Mitigation: one screen only, cell size varies
     with depth, and the seabed band is solid shadow rather than screened.
  3. *Headline collides with busy screen texture.* Mitigation: upper water column
     is deliberately the calmest zone, screen density ramped down above y=300.

## Headline
`AEA Never Got the Call` / `The Filing Said Otherwise`
(22 and 24 characters, two lines.)
