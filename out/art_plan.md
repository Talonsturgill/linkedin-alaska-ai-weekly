# Art plan — Anchorage Desk — 17 SEP 2026 — Ruaro / AIDEA land conveyance

## Step 0 — Story absorbed
- What happened: AIDEA's Randy Ruaro is pushing a no-cost, noncompetitive transfer of nearly 20,000 acres of state land north of Houston into AIDEA's hands for an "industrial and energy development district" that lists scalable data centers among its uses, while telling DNR there is no data center project planned.
- Why it matters to Alaska: whoever holds that land decides where large, always-on AI loads land on a Railbelt grid that is already short of gas, and the land moves before any tenant or project-level review exists.
- Register: cautionary and wry. Vast, real land. An empty promise drawn in dotted line.

## Step 1 — Dedup scan (see scratch art_dedup.md)
- Forbidden style (last 8): wpa_scaffold, woven_fabric, halftone_section, exploded_iso_docket, landmark_mesh, riso_form, hydrographic_claim, engraved_headworks (+ aurora permanently).
- Forbidden hue (last 4): teal, gold, red, blue.
- Forbidden composition (last 2): diagonal_thrust, weave_rupture.
- Forbidden motifs (last 10): consoles, camera feeds, woven cloth, water-column section, seabed cable, server hive field, tidal rotors, isometric corridor, facial mesh, permit form, surveyed claim quadrilateral over water, stop-log gate, spillway gates, surveillance cameras.
- Chosen: style_family `pixel_dither_aerial` (never used), hue_family `green` (last used 08-21, 5th back, clear), composition `aerial_plan_view` (new name; not a scatter field, not a plat over water).

## Step 2 — Concepts considered
1. **Aerial parcel, blank.** A posterized, ordered-dithered satellite view of the Houston lowlands (braided river, muskeg ponds, birch and spruce, a straight utility corridor). One enormous parcel is knocked out to bare paper with a dashed boundary, as if the land had already been lifted off the map. Inside it, tiny, a dotted ghost footprint where a tenant would go. Scale contrast plus juxtaposition. CHOSEN.
2. A lone survey stake in an immense flat muskeg under a huge sky, minimal_line. True but too quiet for the detail bar and the stake motif reads generic.
3. A power line corridor marching to a blank billboard. Transmission towers were used on 07-08 and 07-31 and the billboard is a stock gag. Killed.

## Step 3 — Blueprint
1. **Concept statement.** From above, the Mat-Su lowland is a dense living raster of birch, muskeg and braided water, and one rectangle of it has gone blank paper with a dashed edge, lifted off the state map before anyone wrote a name inside. The read in half a second: a lot of real land, one empty box.
2. **Register.** Cautionary, wry. Cool spruce greens and pale water carry the land's reality; the paper-blank parcel carries the absence; one warm fireweed-magenta dashed boundary and ghost footprint carry the alarm without shouting.
3. **Style family.** `pixel_dither_aerial`: coarse ordered dither (Bayer 4x4) between 5 land classes rendered as 6 px cells, the satellite-tile / early-GIS raster look. Fits a land-conveyance story literally (this is how DNR's own parcel viewers look) and clears every cooldown.
4. **Palette (OKLCH-built, hex logged in meta).**
   - paper `#f3eee2` (L≈0.94) — the blank parcel and type field
   - water `#c9dccf` (L≈0.86) — braided channels and ponds
   - birch `#9fbb86` (L≈0.73) — mid field
   - muskeg `#587a4a` (L≈0.52) — mid-dark field
   - spruce `#1d3a2a` (L≈0.30) — dark field, headline ink
   - fireweed `#c8386f` (L≈0.55, high chroma) — focal accent: dashed boundary, ghost footprint, stake
   - polaris gold `#ffc72c` — colophon only
   Value spine: paper (light) > water > birch > muskeg > spruce (dark). The parcel is the lightest large area, so it wins the contrast war against the mid-value raster; the headline in spruce ink sits on the paper at >10:1.
5. **Composition map (1080 grid), pattern `aerial_plan_view`.**
   - Whole canvas: dithered land raster. River: a warped diagonal band entering top-left (~x 0, y 260) and exiting bottom-right (~x 1080, y 900), 40–90 px wide with side channels. Ponds: dark-water blobs where a second field exceeds a threshold, concentrated bottom-left. Corridor: a straight 26 px pale swath from (150, 1080) to (1010, 0) with tower dots every 64 px (existing utility corridor).
   - Parcel: irregular rectilinear township-style polygon, roughly x∈[300, 940], y∈[210, 700] with two section-line jogs (a notch out of the top-right and a step in the lower-left), filled paper. Dashed boundary in fireweed, 14 px dash / 9 px gap, 4 px wide. Corner ticks at each vertex.
   - Ghost footprint: dotted rectangle 96×64 at (760, 585), 2 px, fireweed, with a tiny dotted "pad" line to the corridor. No label.
   - Survey stake: one 3 px fireweed vertical with a small flag at (356, 655), the only "human" mark.
   - Headline block: Fraunces Black, two lines, left-aligned at x=340, top y=270, fit to width ≤ 560, spruce ink on paper. Kicker in mono, spruce at 70%, at (340, headline_bottom + 26).
   - Wordmark `ALASKA.AI` Fraunces Black 30 px, paper on a spruce chip, bottom-left (72, 1000).
   - Polaris r=13 at (1008, 72) with a soft paper halo so it reads on the dark raster.
   - Eye path: headline → dashed parcel edge → ghost footprint → corridor → wordmark.
6. **Layer build order.** paper base → class map (numpy: warped fields → 5 classes, river/pond/corridor overrides) → Bayer dither → rasterize cells → subtle grain on raster only → parcel fill (paper, with faint paper mottle) → parcel dashed edge + corner ticks → ghost footprint + pad line → survey stake → headline + kicker → wordmark chip → polaris → vignette 0.10.
7. **Technique stack.** `field`, `warp`, `ridged` (river), numpy Bayer dither, `poly`/`line` rasterization, `chips` (gravel bars along the river), `mottle`, `grain`, `fraunces`, `mono`, `chip`, `polaris`, `vignette`.
8. **Risks.** (a) Dither reads as noise mush → keep cells 6 px, only dither at class boundaries (blend band ±0.06), keep 5 classes with honest value gaps. (b) Parcel reads as a paste-on white box → add faint mottle and a 1 px inner shadow line, let the river run under its edge (visible on both sides), keep the dashed edge hand-jittered. (c) Headline collides with parcel notch → parcel top is straight across the headline zone; notch is top-right beyond x 820.
