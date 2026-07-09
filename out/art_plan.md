# The Stack — Art Plan — 2026-07-08

## 0. Story absorbed
- What happened: the Air Force opened a 10 U.S.C. 2667 Enhanced Use Lease competition (AFCEC-26-R-0006) to outlease ~4,700 acres at JBER, Eielson and Clear to one developer to build commercial AI data centers on-base; offers closed June 29 and it is now in non-public source selection.
- Why it matters to Alaska: a single federal source-selection desk (AFICA, CO Julia A. Cantrell), not the state grid or ADNR, decides whether Alaska lands a hyperscale AI build, and it made bankable firm power the pass/fail variable inside that one decision.
- Emotional register: cool, institutional, quietly high-stakes. Not triumphant, not alarmist. The tension of many waiting on one desk.

## 1. Dedup scan (obeyed)
Recent bespoke ledgers (last real Stack pieces):
- 2026-07-07-02: style `cadastral_ledger`, hue `red`, comp `central_icon`, motifs [cadastral plat, consent seal, survey ticks, north arrow].
- 2026-07-07: style `iso_cutaway`, hue `blue-teal`, comp `thirds_focal`, motifs [exploded fuel stack, gate iris, converging conduits, data-center block].
Forbidden this cycle: style_family {iso_cutaway, cadastral_ledger}; hue {red, blue-teal}; composition {central_icon, thirds_focal}; motifs {those above, incl. converging conduits, gate iris, seal, survey ticks, north arrow}. The aurora/starfield legacy look is permanently forbidden.
My picks clear all of it: style **swiss_grid**, hue **neutral-cool (slate) with a gold focal**, composition **modular_grid**, motifs a clean equal-cell offer grid + one lit decision cell (NOT a cadastral plat, NOT a gate iris, NO converging conduits).

## 2. Concept (chosen of three)
- (A) Best-value balance scale weighing power vs capital — rejected, balance/scale is near-cliché.
- (B) A single lit toll-desk at the neck of converging proposal paths — rejected, "converging conduits" is a forbidden motif and too close to last week's gate.
- (C) **CHOSEN. "One Desk."** A vast, cold, orderly modular grid of identical offer/parcel cells fills the lower field. All are dim graphite except ONE, which blazes low-angle Alaska gold: the AFICA source-selection cell where the binary go/no-go lands. Inside it, a small transmission-tower glyph glows, because bankable firm power is the pass/fail variable scored at that desk. Three cells carry mono labels JBER, EIELSON, CLEAR, the three installations feeding the one decision. The read in half a second: a whole landscape of offers, one small desk decides.

## 3. Style family
`swiss_grid` — modular grid, huge Fraunces headline as form, 2-3 inks + paper, geometric authority. Fits procurement/source-selection analysis exactly and is disjoint from the last-8 style families. Deliberately hard-edged to contrast the organic field/warp of the cadastral piece and the isometric prisms of the fuel-stack piece.

## 4. Palette (OKLCH-reasoned, value spine first)
- `#10141b` paper/ground — darkest, L~0.09, cool slate near-black (the institutional field).
- `#232c39` cell-dim fill — L~0.20, cool slate (the many waiting offers).
- `#33404f` cell-identified fill — L~0.30, lighter steel (the three named base cells).
- `#6b7d92` steel line/label — L~0.52, cool, for schematic linework and mono telemetry.
- `#f4b13c` focal gold — L~0.77, HIGH chroma, low-angle Alaska light (the one lit decision cell, power glyph, polaris). Wins the contrast war by chroma AND a large value gap from the slate field.
- `#f3ead6` type paper — L~0.93, warm off-white headline knocked out of the dark.
6 inks incl. paper. Grayscale squint check: gold cell + headline paper are the only bright events on a dark field, so focal hierarchy holds in value alone.

## 5. Composition map (modular_grid, 1080 grid)
- Headline zone: x in [96, 900], y in [72, 300]. Two lines Fraunces wght 900 opsz 144, leading ~1.05, knocked in `#f3ead6`, left-aligned. Line 1 "ONE FEDERAL DESK", line 2 "GATES ALASKA’S AI".
- Kicker (mono, `#6b7d92`, 18px, tracking 0.22): x=98, y=322. "THE STACK · VEHICLES · 8 JUL 2026".
- Grid: x in [96, 984], y in [360, 930]. 6 cols x 5 rows, gutter 16. cell ~134.7 x ~101.2.
- Focal gold cell: col index 3, row index 1 (right-of-center, upper-middle), enlarged ~18px each side to break the grid (Swiss tension) and pull the eye. Soft gold radial glow behind it. In-cell: a transmission-tower glyph (dark steel on gold, center-left), a bold check drawn from two segments (upper-right), one tiny mono label "AFCEC-26-R-0006" along the bottom inner edge, and a micro "AFICA" tag. Gold glints (lightened) at the tower tip.
- Identified base cells (fill `#33404f`, mono paper label centered): (col1,row0)=JBER, (col5,row2)=EIELSON, (col2,row4)=CLEAR.
- Faint low ridge silhouette (`#1a2230`, small amp) at y~946 between grid and footer, subtle Alaska grounding.
- Wordmark "ALASKA.AI" Fraunces Black ~30px at (96, 996), `#f3ead6`.
- Polaris (gold) top-right at (984, 96), r=13, small halo. Colophon.
- Eye path: headline -> gold focal cell -> three labeled cells -> wordmark.

## 6. Layer build order (back to front)
1. Base ground `#10141b`.
2. Whole-canvas vertical depth gradient (`#141a24` top -> `#0d1117` bottom), very subtle.
3. Faint field/mottle texture on the ground for life.
4. Dim grid cells: fill + dark seam outline; meso content per cell (inner parcel rect + 2 faint ledger lines in steel low-alpha); light stipple; slight per-row darkening (atmospheric).
5. Identified base cells (lighter fill + centered mono label).
6. Focal: gold radial glow -> enlarged gold cell fill -> tower glyph + check + mono labels -> glints.
7. Faint bottom ridge.
8. Headline (paper Fraunces), kicker (mono).
9. Wordmark, polaris.
10. Finish: grain (amount ~6), gentle vignette (~0.12) to seat the focus.

## 7. Technique stack
`poly`/`line` hard-edged rect grid (swiss), `gradient_v` depth, `gradient_r`+`glow` gold light pool, `field`+`mottle` ground life, `stipple` cell meso texture, `ridge_pts` subtle horizon, `fraunces`/`mono`/`chip` type, `grain`+`vignette` finish. Deliberately avoids `iso_prism` (last week) and `warp`-driven organic fields (two weeks ago) so the technique identity is distinct.

## 8. Risk list + mitigations
- R1 "lit window in a grid" reads generic/clip-art. Mitigation: give every cell schematic offer/parcel DNA (inner rect + ledger ticks), enlarge and stamp the focal cell as a decision (tower + check + solicitation number), and let Swiss typographic authority + the three real base labels tie it unmistakably to source selection.
- R2 gold glow washes neighbors and muddies midtones. Mitigation: keep glow radius moderate, keep the dark seams crisp, hold neighbor cells clearly darker so the value gap survives; grayscale-check.
- R3 headline collides with the busy grid. Mitigation: reserve the top [72,300] band as a quiet dark zone with no cells; grid starts at y=360; paper type on near-black needs no panel.
