# Art plan — The Stack — 28 SEP 2026 — VEHICLES

## Step 0 — Story absorbed
- **What happened:** Alaska DOH is opening Year 2 of the $272M Rural Health Transformation Program before it has finished distributing Year 1 (ADN, 26 Sep 2026).
- **Why it matters to Alaska:** a federal fund with a written technology tilt reaches rural providers through ONE discretionary office, the DOH Commissioner, who holds final authority on every award and sets the Year 2 criteria. Tech vendors only get in through provider projects.
- **Register:** measured, clarifying, a little tense (a bottleneck and a clock), constructive not accusatory.

## Step 1 — Dedup scan (16 most recent claude/linkedin-* ledgers)
- Forbidden style_family (last 8): engraving_trail, machined_plate, pixel_dither_aerial, wpa_scaffold, woven_fabric, halftone_section, exploded_iso_docket, landmark_mesh (+ aurora_field permanently).
- Forbidden hue_family (last 4): blue, violet, green, teal.
- Forbidden composition (last 2): diagonal_thrust, suspended_gap.
- Forbidden primary motifs (last 10): trail tripods, HV coupling gap, dithered aerial raster, console stair tower, woven cloth/threads, water-column section, exploded iso corridor, landmark mesh, permit form, surveyed claim quadrilateral.
- Clears: style `still_life_gouache` (new: a lit museum-object still life, gouache-flat planes + stipple modelling), hue `red` (oxblood; last used 4 SEP, 5 issues back), composition `column_and_icon` (new), motif `hourglass` (never used).

## Step 2 — Three concepts
1. **The hourglass (CHOSEN).** Federal gold sand fills the upper bulb; the whole fund must pass one pinched neck (the Commissioner's desk) grain by grain; the lower bulb holds a faint etched map of Alaska where rural village points wait, some lit, many still dark, and only a small pile has landed. A few ice-blue "technology" grains are mixed through the gold and, below, sit *inside* the lit village markers (tech rides inside care projects). Reads in half a second: one narrow neck, a lot of money, a clock. It is specific: the lag in the trigger, the deadlines, the single office.
2. Airline-route-poster map with every route converging on one hub desk then fanning to villages. Killed: route-map/convergence is close to the 31 JUL "four-thread fan" and 17 SEP aerial map cooldowns.
3. A prism splitting a "technology" beam into three colored beams (pay-for-value, care coordination, EMS), none of them the tech color. Killed: prism reads as a record-cover cliché and loses the Alaska specificity.

## Step 3 — Blueprint

1. **Concept statement.** A $272M federal hourglass whose only passage is one pinched neck. The sand that has made it through is still a small pile, and the Alaska below it is mostly still waiting.
2. **Register.** Quiet museum still life on a deep oxblood wall: the gravity of a single lit object. Warm gold is the only high-chroma thing; everything else recedes into wine-dark shadow. The mood is a clock ticking, not an alarm.
3. **Style family.** `still_life_gouache`: flat gouache planes for the wall, wood and glass, modelled with stipple and fine hand lines, a single raking warm light from upper left. It fits a story about one object (one office) that governs a flow, and it clears every cooldown.
4. **Palette (OKLCH).**
   - Wall dark `oklch(0.20,0.055,18)`: darkest dark, the field and the vignette corners.
   - Wall mid `oklch(0.30,0.085,22)` oxblood: the glow field behind the glass.
   - Walnut `oklch(0.40,0.07,50)` + walnut light `oklch(0.58,0.08,62)`: the frame.
   - Gold sand `oklch(0.80,0.145,82)`: FOCAL accent, highest chroma.
   - Cream `oklch(0.94,0.03,85)`: glass highlights and headline type (lightest light).
   - Ice `oklch(0.86,0.07,205)`: tiny "technology" grains only (<1% area, so hue_family stays red).
   - Value spine: wall 0.20-0.30 / walnut 0.40-0.58 / sand 0.80 / cream 0.94. The focal neck wins because the gold stream (L .80, C .145) meets the darkest wall directly behind the neck, plus a soft glow.
5. **Composition map (`column_and_icon`).** Left type column x∈[72, 500]; hourglass icon on the right third.
   - Hourglass axis cx=772. Top plate y∈[92,124], x∈[566,978]; bottom plate y∈[956,988], same x. Plates are 60px+ from the canvas edge.
   - Posts at x=596 and x=948 (front pair, radius ~15 with turned beads at y=190, 540, 890); a faint third post behind at cx.
   - Upper bulb y∈[124,540], max half-width 178 at y≈300; neck at (772, 540), half-width 8.
   - Lower bulb y∈[540,956], mirror profile.
   - Upper sand: surface y=292 at the walls dipping to a crater at y≈338 on the axis, filling down to the neck.
   - Stream: 3px gold line from (772,540) to the pile apex (772,902).
   - Lower pile: cone base y=950, apex y=902, half-width 118.
   - Etched Alaska map in the lower bulb, centered (770, 770), scale 11.5 px/deg-lat; ~44 rural village points; faint etched routes from the neck to each point; ~14 points lit gold, the rest hollow rings.
   - Headline block: "$272M" Fraunces 900 opsz 144, ~150px gold, top at y=150; "runs through" / "one desk." cream ~76px at y≈330 and 410 ("one desk." italic).
   - Supporting mono line at y≈520: "RURAL HEALTH TRANSFORMATION PROGRAM".
   - Kicker "THE STACK · VEHICLES · 28 SEP 2026" mono 16, tracked 0.2, at (72, 96).
   - Labels (telemetry, dossier-true): "YEAR 1 · $272,174,856" at the upper bulb's left edge; "FINAL DECISION-MAKING AUTHORITY" on a leader line from the neck to the left column (y=540); "RURAL PROVIDERS" at the lower-bulb left edge.
   - Wordmark ALASKA.AI Fraunces 900 size 32 at (100, 992) baseline-left; polaris r=12 at (82, 980).
   - Eye path: $272M → the leader line → the glowing neck → down the stream → lit villages → wordmark.
6. **Layer build order.** Wall gradient + radial glow → mottle → cast shadow of the hourglass on the wall (offset right-down, blurred) → back post → glass interior tint → lower-bulb etched map + routes + villages → upper sand mass with stipple and crater → lower pile → stream + falling grains + neck glow → glass rim lines + highlight streaks → front posts (turned profile, hatch shade side) → plates (bevels, wood grain) → type + leader + labels → marks → grain + vignette.
7. **Technique stack.** gradient_v, glow, mottle, poly (bulb profile), stipple (sand modelling, wall grain), chips (sand grains and ice grains), hand_line (map coast, wood grain, leader), hatch (post shadow sides), circle (villages), fraunces, mono, polaris, grain 6, vignette 0.2. Map coastline from a hand-coded lon/lat outline projected with cos(lat) scaling.
8. **Risk list.**
   - The glass reads as a flat outline, not glass. Mitigation: a tinted interior, a double rim line (bright on the lit left, dim on the right), two curved highlight streaks, and the wall showing through slightly darker.
   - The map in the lower bulb turns to mush at thumbnail. Mitigation: keep it an etched whisper (low alpha); only the lit village dots and pile carry value, so the map is nose-length detail.
   - The headline column feels empty below the type. Mitigation: the leader line from the neck crosses into the column, the mono labels sit on a vertical tick rail, and the wall carries stipple texture.
