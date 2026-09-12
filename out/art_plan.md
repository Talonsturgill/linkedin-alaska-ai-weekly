# Art plan — Anchorage Desk — 11 SEP 2026

## Step 0 — Story absorbed
- What happened: Eagle River Assembly member Jared Goecker voted in the 8-4 majority on Sept. 1 to fund (just under $600,000, Thundercat) the expansion of APD's Real-Time Crime Center, a hub that can reach up to 750 cameras.
- Why it matters: the money moved two weeks before the Assembly returns (Sept. 15) to the ordinance that would gate AI deployment, footage retention and federal data sharing on that platform. Capability installed ahead of its guardrails.
- Register: cautionary but fair, dusk-tense, not alarmist. The hub is real and working (credit); the railing is missing (risk).

## Step 1 — Dedup scan (16 prior ledgers read, see scratch/art_dedup.md)
- Forbidden style families (last 8): woven_fabric, exploded_iso_docket, halftone_section, riso_form, landmark_mesh, hydrographic_claim, voronoi_impoundment, engraved_headworks (+ aurora_field always).
- Forbidden hue families (last 4): gold, blue, red, orange.
- Forbidden compositions (last 2): weave_rupture, exploded_iso_stack.
- Forbidden motifs (last 10): woven cloth, iso corridor, water-column section/server hives, permit form, facial-landmark mesh, surveyed claim over water, spillway gates, stop-log headworks/crane, moored land raft, surveillance camera crowd + ordinance page.
- This piece: style family `wpa_scaffold` (WPA layered landscape × blueprint dashed-ghost grammar), hue family `teal`, composition `diagonal_thrust`, primary motif "stair tower with a dashed, uninstalled handrail". All clear.

## Step 2 — Three concepts
1. **The missing handrail.** A steel stair tower (the new hub) rising diagonally into an Eagle River dusk, every landing lit with monitor banks and fed by hairlines from distant camera points, but the handrail exists only as a dashed magenta outline. Guardrails, literally not installed yet. Reads in half a second, is of this story, and avoids the camera-crowd motif.
2. Cart before horse on Old Glenn Highway. Too cliché, could run on any policy blog. Killed.
3. A 12-panel video wall with 8 lit, 4 dark (the tally) and one blank "rules" panel. Clever but reads as a chart; also flirts with the 8/28 grid/mesh look. Killed.

Pick: concept 1.

## Step 3 — Blueprint

**Concept statement.** A working stair tower of lit consoles climbs out of a spruce line into a teal dusk, fed by thin lines of light from far-off cameras on the ridge. Its handrail is only a dashed magenta outline. The hub is built and busy; the rail is a drawing.

**Register.** Cool teal dusk carries the caution; warm console light carries the credit (the center is real and working). The one hot magenta ink is the absence, so the eye lands on what is missing.

**Style family.** `wpa_scaffold`: flat layered landscape (WPA) for sky, ridges, spruce and snow, with a blueprint grammar (thin ink frame, hairline feeds, dashed ghost rail, mono labels) for the built thing. WPA was last used 12 issues back (7/31) and only as a hybrid; blueprint has not been used in the ledger window. Clears all cooldowns.

**Palette (7 inks incl. colophon).**
- PAPER snow `#dfe7e2` (L≈0.91) — paper/light, snowfield, headline type.
- SKY_TOP `#12303a` (L≈0.25) — deep teal night at the top.
- SKY_LOW `#4f9a97` (L≈0.60) — teal-green dusk band near the horizon.
- INK `#0d1b1d` (L≈0.14) — spruce, steel frame, figure, wordmark.
- SCREEN `#f4e3b0` (L≈0.90, warm) — console light, glow.
- RAIL `#e04c8b` (L≈0.60, highest chroma) — the dashed missing handrail. Focal accent.
- GOLD `#ffc72c` — Polaris colophon only.
Derived (not inks): ridge tones = mix(SKY_LOW, INK, 0.45 / 0.68); cloud bands = mix of the two sky inks.
Value spine: darkest = INK frame/spruce (0.14); lightest = SCREEN and PAPER (0.90). The focal rail wins by chroma against a mid-value teal sky, and the screens win by value against the dark frame. Grayscale check: ridges step 0.45 → 0.35 → spruce 0.14 → snow 0.91.

**Composition map (1080 grid, `diagonal_thrust`).**
- Sky gradient box (0,0)-(1080,720), SKY_TOP → SKY_LOW, ease 1.25.
- Cloud bands: 4 wobbled horizontal lenses between y=330 and y=520, x 0-1080, mix(SKY_LOW, SKY_TOP, 0.35).
- Far ridge: ridge_fill y_base=605, amp=115, seed 3, mix(SKY_LOW, INK, 0.45); snow stipple on its upper 40 px.
- Near ridge: ridge_fill y_base=665, amp=70, seed 9, mix(SKY_LOW, INK, 0.68).
- Camera points: 26 tiny SCREEN dots scattered on the ridges (x 40-560, y 520-660) with hairline feeds converging to the tower landings.
- Spruce band: ~70 individual spruce silhouettes along y_base 745 ± 8, heights 45-130, INK; denser on the left.
- Snowfield: y 735-1080 PAPER, mottled, stipple shading in mix(PAPER, SKY_LOW, 0.35) rising toward the spruce line; chips (gravel/debris) around the tower base.
- Tower: posts at x=640 and x=880, base y=905, top y=345. Six landings at y = 905, 795, 685, 575, 465, 355 (pitch 110). Stair flights zigzag between posts. Cross-bracing in each bay. Each landing: 3 SCREEN monitors (14×10) on a console bar with glow r=44. Top deck: roof line at y=330, a console, a tiny seated INK figure at (855, 340).
- Dashed rail: along every flight, 30 px above the flight line, RAIL ink, dash 14 / gap 10, with dashed posts every 44 px; also along the top deck edge. A faint RAIL glow (alpha 28) under the dashes so they read at thumbnail.
- Tower shadow: a soft INK-tinted diagonal on the snow toward lower-left.
- Headline: two lines, Fraunces 900/opsz 144, PAPER, top-left at (84, 84), fit to 620 px (hi 104). Kicker mono 16 tracked 0.22 under it, then italic motto. Quiet zone: sky y<300 is kept free of ridges and clouds.
- Wordmark ALASKA.AI Fraunces 32, INK, bottom-left (84, 1000). Polaris (992, 80) r=13 GOLD.
- Eye path: headline → lit tower → magenta dashed rail → wordmark.

**Layer build order.** paper → sky gradient → cloud bands → far ridge (+ snow stipple) → near ridge → camera dots + hairline feeds → spruce band → snowfield stipple → tower shadow → steel frame (posts, landings, flights, bracing, treads) → consoles + screens + glow → figure → dashed rail + glow → base chips → type + marks → mottle → grain → vignette.

**Technique stack.** gradient_v, wobble_pts/poly (clouds, spruces), ridge_fill, stipple (mask), line/hand_line (frame, feeds, dashes), glow, circle (camera points), chips, fraunces/mono text, mottle, grain, vignette.

**Risk list.**
1. Tower reads as a dark blob against the spruce → keep the frame thin (3-4 px), let the screens carry value, lift the frame with a mix(INK, SKY_LOW, 0.15) rim, and set the base 160 px above the spruce line so it silhouettes against the ridge, not the trees.
2. Dashed rail disappears at thumbnail → magenta at full chroma, 4 px dashes, underlying soft glow.
3. Headline collides with ridge or clouds → ridge crest never above y=490, clouds start at y=330, headline block ends by ~300.
4. Empty snow acreage → stipple gradient, tracks, chips, the tower shadow, and the wordmark occupy it.
