# The Stack — cover art pre-production, 4 SEP 2026

**Column marks.** Kicker `THE STACK · FACILITIES · 4 SEP 2026`. Byline `""` (not drawn).
Headline `RENEWAL IS GUARANTEED / THE TERMS ARE NOT`. SEED 904.

---

## 1. Concept statement

The corridor rulebook drawn as an exploded isometric assembly: a heavy locked
floor slab (185(n), the renewal that cannot be refused), an **empty open tray**
above it (185(f), thirty years of terms, still unwritten), and a thin lid
descending onto that tray (the NEPA instrument) with a narrow lit gap still
open between them. The gap is the fifteen-day scoping window. The read in half
a second: the bottom is settled and solid, the middle is empty and about to be
sealed, and there is one bright slot left to reach through.

## 2. Register

Cold, institutional, quietly urgent. Not alarm and not neutrality. The feeling
is a consequential thing being decided in a room nobody walked into. Carried by
a cold blue-steel value structure everywhere except one warm gold light leaking
from the gap and pooling inside the empty tray, which is the only warmth in the
frame and therefore the only place the eye rests.

## 3. Style family

`exploded_iso_docket` — a deliberate iso_cutaway / blueprint hybrid: machined
isometric slabs with three-tone face shading, sparse mono callout labels on
leader lines, dimension ticks.

**Dedup clearance.** Forbidden style families (last 8) are riso_form,
landmark_mesh, hydrographic_claim, voronoi_impoundment, engraved_headworks,
organic_rd_moorage, constructivist_scatter, ukiyo_bokashi. This is none of them,
and no isometric/exploded-assembly piece appears anywhere in the last 18 issues.
Hue `blue` is clear (last 4 are orange, indigo, green, violet). Composition
`exploded_iso_stack` is clear (last 2 are form_field_grid, thirds_focal).
Motifs are all new; deliberately avoiding the 24 JUL geologic strata read by
making every slab a hard-edged machined plate with bevels, never ridged terrain.

## 4. Palette (OKLCH, 6 inks + paper)

| role | oklch | why |
|---|---|---|
| paper | `oklch(0.945, 0.010, 250)` | pale cool ground, cold institutional light |
| field | `oklch(0.835, 0.028, 246)` | upper atmosphere behind the assembly |
| slab_top | `oklch(0.700, 0.042, 248)` | lit top faces |
| slab_left | `oklch(0.495, 0.048, 250)` | shadowed left faces |
| slab_right | `oklch(0.370, 0.045, 253)` | darkest faces, the value floor |
| ink | `oklch(0.195, 0.028, 250)` | outlines, type, dimension rule |
| gold | `oklch(0.795, 0.145, 85)` | THE focal, the open gap and tray interior |
| gold_hi | `oklch(0.920, 0.090, 92)` | gap core highlight |
| gold_dp | `oklch(0.575, 0.130, 70)` | gold shadow inside the tray, leader accents |

**Value spine.** paper .945 → field .835 → slab_top .700 → slab_left .495 →
slab_right .370 → ink .195. The focal wins twice over: gold at L .795 sits
against slab_right at L .370 (a .43 lightness gap) and carries chroma .145
where nothing else exceeds .048. Grayscale check still reads because the gap is
the lightest thing touching the darkest thing.

## 5. Composition map — `exploded_iso_stack`

Canvas 1080. Nothing important within 48px of the edge.

- **Type band, upper left.** `RENEWAL IS` at (84, 92) ~86px Fraunces 900.
  `GUARANTEED` at (84, 178) ~86px. `THE TERMS ARE NOT` at (84, 272) ~46px in
  gold_dp. Kicker mono 17px tracked .20 at (86, 334).
- **The assembly, centre-right and low.** iso origin (622, 596), scale 1.02,
  slab footprint 250×250 units.
  - Floor slab `185(n)`, z=0, dz=34. Solid, densest hatch, reads as bedrock.
  - Empty tray `185(f)`, z=92, dz=40. Four raised walls, hollow interior, gold
    pooling inside, interior ruled with faint blank lines.
  - Lid `NEPA instrument`, z=196, dz=16. Thin plate, tilted read, TAPS zigzag
    engraved across its top face.
  - **The gap** between tray rim (z=132) and lid underside (z=196) is the focal.
    Gold glow concentrated in that band.
- **Second gate, lower left.** A much smaller separate tray at iso origin
  (250, 838), scale 0.42 — visibly its own object on its own base, not part of
  the stack. Labelled `ADL 63574 · 26.1 AC`. Says: second door, second clock.
- **Callout labels.** Mono 15px chips on 1px leader lines: left edge x≈96 to the
  floor slab and the tray; right edge x≈966 to the lid and the gap. Four labels
  maximum, sparse.
- **Wordmark** chip bottom-left (84, 1006). **Polaris** (992, 92) r=13 in gold.

**Eye path.** headline → gold gap → down into the empty tray → left along the
leader line to the small second tray → wordmark.

## 6. Layer build order (back to front)

1. paper fill + subtle vertical gradient (field at top, paper at bottom)
2. mottle pass on paper for tooth
3. ground shadow ellipses under the assembly and under the second tray
4. floor slab (iso_prism) → hatch its faces → dimension ticks
5. gold glow bloom in the gap band (before the tray, so it reads as emitted)
6. empty tray: outer prism, then interior cavity walls, then gold interior fill,
   then faint blank rule lines inside the cavity
7. lid prism, TAPS zigzag engraved on its top face, underside caught in gold
8. second small tray assembly, lower left
9. micro pass: chips debris along slab edges, stipple on shadowed faces, glints
   on the gap rim, tiny crack marks on the floor slab
10. leader lines + mono callout chips
11. grain (restrained, 6.0) + vignette
12. type: headline, kicker, wordmark chip, polaris

## 7. Technique stack

`iso_prism` and `iso` for the assembly, `poly` for cavity walls and bevels,
`gradient_v` for the field, `glow` + `gradient_r` for the gap bloom, `hatch` for
face shading at three densities, `stipple` on the darkest faces, `chips` for
edge debris, `hand_line` for the TAPS zigzag and crack marks so they aren't
mechanically straight, `line` for leader rules and dimension ticks, `mottle`
and `grain` for paper tooth, `vignette`, `chip` for mono labels, `polaris`,
`fraunces` and `mono` for type. Single texture identity: hatch as the shading
language, grain as the finish. No halftone, no riso, no reaction-diffusion.

## 8. Risk list

1. **Iso stack reads as a generic 3D box diagram / crypto-deck clip art.** The
   defence is craft density: three hatch densities per face, bevelled edges,
   chipped corners, dimension ticks, hand-drawn crack marks. Every slab must
   look machined and used, not extruded by default. If it still reads generic
   after render 1, tilt the lid off-axis and open the gap wider.
2. **The empty tray reads as a solid box and the whole metaphor dies.** Mitigation:
   draw the cavity explicitly with visible inner walls and an interior floor
   several units below the rim, and let gold light spill up the inner walls. Check
   at 300px that the tray reads hollow. This is the single most important
   legibility test in the piece.
3. **Headline collides with the assembly.** The type band ends at y≈352 and the
   assembly's topmost geometry starts at y≈380. Only 28px of clearance, so the
   lid must not be allowed to drift upward. Verify the lid's top vertex before
   shipping; if it crosses y=372, drop the iso origin.
4. **Gold glow washes the midtones into mud.** Keep the bloom confined to the gap
   band and the tray interior, alpha ≤ 90, never a full-canvas warm cast.

## 9. Eval loop

Ship bar is weighted ≥ 8.5 with no dimension below 7, and 8.5 is the floor, not
the target. Recent issues have landed 8.56 to 8.94. Iterate while a fix clearly
buys quality, up to 6 passes. Score honestly into `eval_history`.
