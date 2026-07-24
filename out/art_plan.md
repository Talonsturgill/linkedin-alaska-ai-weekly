# The Stack — Art Plan — 2026-07-24

## Story (Step 0)
- What happened: NSF seeded a UAF Geophysical Institute-led AI mineral-discovery Engine in Alaska, $15M over two years, up to $160M over a decade if it clears milestones.
- Why it matters to Alaska: whether AI-driven critical-mineral exploration scales depends on TWO independent go/no-go decisions, NSF TIP's continuation call (money) and NANA's ANCSA subsurface-estate access (ground). Alaska holds 56 of 60 USGS critical minerals.
- Register: cold, analytical, contingent. Not triumphant, not bleak. The deposit is found (AI did its job); the value is locked behind two gates that both must turn. Tension of optionality.

## Concept (Step 2 — three considered)
- A. Two valves in series on a conduit rising from a glowing ore body: value reaches the surface only if BOTH valves open (series = AND gate). One valve is the federal money key (NSF TIP), one is the ground key (NANA). AI triangulation reticle has already pinned the ore. **CHOSEN.** Metaphor + synecdoche, of-Alaska (pipeline valves, tundra ground, ore), of-this-story (two independent gates, AI discovery, optionality).
- B. Funding ladder with a solid $15M base and a ghosted $160M tranche behind a gate. Rejected: too close to 07-10 converging_funnel capital-gate and 07-08 offer-grid.
- C. Geologic map with AI scan grid lighting deposits. Rejected: underplays the two-key chokepoint tension that is the actual story.

Concept statement: A single conduit rises from an AI-pinned critical-mineral ore body through two valve wheels set in series, each on its own control stem to a different named actor. The reader reads in half a second that the prize is found but that two independent hands, federal money and Native-corporation ground, must both open before any value flows.

## Register carry
Cold spruce-teal green ground carries the analytical, contingent mood; the lone warm copper ore-glow is the found prize and the only hope-color, deliberately locked below the two valves. Value structure (dark deep ground vs bright ore) does the emotional work.

## Style family
`geologic_engraving` — a deliberate hybrid: wpa flat-layered geologic strata + engraving hatch/stipple craft + a spare schematic overlay for the conduit, valves and AI reticle. WHY it fits: the story is an engineered mechanism sitting inside Alaska ground, so a print-like engraved cross-section with schematic gate glyphs reads both as landscape and as machinery. Dedup: clears the last-8 forbidden set (iso_cutaway, swiss_grid, flow_field, cadastral_ledger, bathymetric_blueprint). Not a subsea/waterline section (07-17 was submerged bathymetric; this is a dry geologic strata section with a vertical conduit spine, different composition and palette).

## Palette (OKLCH value spine; dominant hue = green)
- paper / pale sky: `oklch(0.93, 0.03, 155)` cold mint  → ~#e6efe4 (top light, headline quiet zone)
- sky field: `oklch(0.80, 0.045, 175)` soft teal-green → mid-light above ground
- strata mid: `oklch(0.60, 0.05, 158)` spruce-teal band
- strata mid-2: `oklch(0.48, 0.05, 160)` deeper band
- deep ground / shadow: `oklch(0.26, 0.04, 158)` near-black spruce (darkest dark, surrounds ore)
- ink / type: `oklch(0.17, 0.03, 158)` near-black green
- FOCAL accent (ore glow): `oklch(0.72, 0.15, 62)` warm copper/amber — highest chroma, only warm, sits against the deep-ground darkest dark for max value gap. Small area (< 6% canvas).
Value spine: darkest dark = deep ground ring around ore (L .26); lightest light = mint sky/headline zone (L .93); focal wins via warm hue + a ~0.45 L jump from its dark collar. Grayscale squint: bright ore blob on dark ground reads instantly.
hue_family bucket: green.

## Composition map (1080 grid) — pattern: bilateral_gate (central conduit spine, two flanking valve stems, focal ore low-center)
- Ground/surface line: y=470, gently undulating (ridge_pts, low amp), separates pale sky (above) from strata (below).
- Sky zone (y 0..470): headline block top-left x∈[84,720], line1 top y≈96, line2 y≈188 ("ALASKA'S MINERAL ENGINE" / "RUNS ON TWO KEYS"), Fraunces poster wght 900 opsz 144, ~2 words/line ragged. Kicker mono under it at y≈270. AI triangulation reticle occupies upper-right sky: three thin sightlines from ~(560,150),(760,175),(900,240) converging to a small target reticle at the ground-pierce point (620,455), dashed/hand-drawn, then a single dashed plumb continues down to the ore. Keeps clear of the headline quiet zone on the left.
- Conduit spine: a narrow vertical channel centered x≈540 from the ore up to the surface manifold at y≈470.
- Ore body (FOCAL): glowing copper lens/vein at center (540, 830), ~200px across, embedded in the darkest deep-ground collar, micro ore-sparkle stipple, hatched vein tendrils. This is the one focal point.
- Valve A (lower, deeper) on the conduit at (540, 660): valve wheel r≈46 (circle + 6 spokes + hub), control stem running LEFT to a labeled node chip at (past 300) — mono label "NSF TIP" and tiny "$15M". This is the money key.
- Valve B (upper) on the conduit at (540, 545): valve wheel r≈46, control stem running RIGHT to a labeled node chip near (770,545) — mono label "NANA" and tiny "GROUND". This is the ground key.
- Optionality mark: a ghosted/dashed "$160M" mono tag near the surface top of the conduit (y≈500, faint), signalling the option-not-a-commitment tranche above the valves.
- Polaris star: (980, 120) r=12, colophon.
- Wordmark ALASKA.AI: bottom-left (84, 1004) small in a chip, knocked into the deep ground.
Eye path: headline (top-left) → reticle sightlines (upper-right) down the dashed plumb → glowing ore focal (center-low) → up the conduit through valve A then valve B → the two labeled keys → wordmark.

## Layer build order (back to front)
1. paper base (mint) 
2. sky gradient_v (mint→teal-green down to ground line)
3. subsurface fill (deep ground base) 
4. strata bands: voronoi_polys clipped into horizontal-ish bands + per-band lighten ramp + dark seams (meso structure inside the big ground shape)
5. hatch pass on strata bands (engraving craft), lighter near surface, denser deep
6. deep-ground collar/darkening around the ore center (radial darken)
7. conduit channel (hand_line walls, faint)
8. ore body: glow + copper lens fill + vein tendrils (hatch) + micro sparkle stipple + chips rubble
9. valve wheels A & B (circles, spokes, hubs) + control stems (hand_line) + node chips
10. AI reticle sightlines (hand_line dashed) + target mark + plumb line
11. ghosted $160M option tag
12. grain finishing pass (mono, restrained) 
13. type: headline (Fraunces), kicker + valve labels + option tag (mono), wordmark chip, polaris

## Technique stack
gradient_v (sky), voronoi_polys (strata cells), ridge_pts (ground line + band boundaries), lighten/mix ramp (atmospheric strata depth), hatch (engraving on strata + ore tendrils), stipple/chips (ore sparkle + rubble micro), glow (ore focal), hand_line (conduit, valve stems, reticle sightlines — hand-drawn schematic), circle/poly (valve wheels), grain (finish, amount ~6), chip/soft_panel (labels, wordmark), polaris, fraunces + mono type. ONE finishing texture identity: grain + engraving hatch.

## Risk list + mitigation
1. Mud in the many cold greens → enforce hard value gaps between strata bands via the lighten ramp; keep the ore the ONLY warm/bright element; grayscale-check the focal wins.
2. Headline collides with busy reticle/strata → reserve a pale quiet zone top-left (sky is lightest there, reticle pushed to upper-right, no strata above ground line).
3. Valves read as generic lock/gear icons or clutter → only TWO, rendered as clean composed valve wheels (industrial, pipeline-country, not padlocks), each clearly labeled to its named actor; conduit+ore stay the dominant thumbnail read so the icons are support, not subject.
4. Two valves read as one → separate them in depth (y 660 vs 545), opposite lateral stems (left vs right), distinct labels.
5. AI reticle over-busy → keep sightlines thin, dashed, few (3), converging to one small target; it's a whisper that AI pinned the ore, not a second focal.

SEED = 724
