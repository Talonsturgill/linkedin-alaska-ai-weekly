# Art plan — The Stack — 17 JUL 2026

## Step 0 — Story absorbed
- What happened. On July 8, 2026 the FCC's second-phase submarine cable landing license rules took effect (DA-26-684), and the GCI Liberty and Quintillion cable-landing transfers that carry Alaska's only Arctic fiber sit inside that regime.
- Why it matters to Alaska. The transfers cannot close until a DOJ-chaired interagency committee (Team Telecom) clears them, so the connectivity substrate under every North Slope and Railbelt AI-data-center thesis runs through a single national-security veto that never appears on the FCC docket surface.
- Emotional register. Tense, structural, quietly ominous. The real power is submerged and off-frame. Cold institutional surface, one hot point of leverage hidden in the deep.

## Step 1 — Dedup (cooldowns obeyed)
Recent Stack ledgers: 07-10 flow_field / gold / converging_funnel; 07-08 swiss_grid / neutral-cool / modular_grid; 07-07-02 cadastral_ledger / red / central_icon; 07-07 iso_cutaway / blue-teal / thirds_focal.
- style_family forbidden (last 8): flow_field, swiss_grid, cadastral_ledger, iso_cutaway. -> choosing a bathymetric_blueprint hybrid (topo_map + blueprint), unused.
- hue_family forbidden (last 4): gold, neutral-cool, red, blue-teal. -> choosing INDIGO dominant with a warm amber focal (indigo bucket is clear; the amber is a small accent, not the dominant bucket).
- composition forbidden (last 2): converging_funnel, modular_grid. -> choosing a submerged_section (waterline splits a cold surface band from a deep field), unused.
- Permanent-forbidden aurora/starfield: not used.
- gate motif appeared before as "single desk gate" (07-10) and "gate iris" (07-07); mine is a SUBMERGED SLUICE/VALVE in bathymetric water, a visually distinct object, and the primary motif here is the subsea fiber section, not the gate glyph.

## Step 2 — Concepts (three, pick one)
1. Bathymetric section. Subsea fiber descends from a lit "docket surface" through dark Arctic water; three cool surface markers are the visible FCC layers, but the single lit element is a submerged gate in the deep that the line must pass. Reads in <1s: the real gate is below the surface. CHOSEN.
2. Exploded license stack. Four stacked plates, three cool, the fourth hot and offset. Rejected: too close to the iso_cutaway register just used (07-07) and the swiss modular grid (07-08).
3. Single breaker on a map. A wall map of Alaska with one interconnection-style breaker. Rejected: generic, and map-with-one-anomaly risks reading like the cadastral plat (07-07-02).

Winner: Concept 1. Metaphor (mechanism -> image) plus scale contrast (vast cold deep vs one small hot gate) plus juxtaposition (visible surface docket vs hidden deep veto). The headline sits literally below the waterline — off the docket surface.

## Step 3 — Register + palette
Register carried by a cold institutional surface, a darkening indigo deep, and ONE warm sodium-amber focal that wins every contrast war. Value spine first, hue is costume.

Palette (built in OKLCH in the script; resolved hexes logged in meta):
- paper / deepest sea (bottom): oklch(0.16, 0.055, 262) ~ deep indigo-navy. Darkest dark.
- water mid: oklch(0.36, 0.075, 258) ~ indigo-blue. Field body.
- surface band (docket): oklch(0.70, 0.035, 232) ~ pale cold steel-cyan. The visible official layer, lighter and desaturated.
- contour / schematic ink: oklch(0.80, 0.075, 214) ~ pale cyan. Bathymetric lines, cable core, dimension ticks.
- focal amber: oklch(0.76, 0.15, 72) ~ warm sodium. Highest chroma, reserved for the gate only.
- hot core: oklch(0.93, 0.09, 88) ~ near-white gold. The gate's lit center.
- type light: oklch(0.95, 0.012, 220) ~ cool white. Headline + wordmark.
Value structure. Lightest light = hot core at the gate (draws the eye down-left). Darkest dark = seabed bottom. Focal wins by a hot hue AND a value gap against the near-black deep around it. Everything above the waterline stays cool and quieter than the gate. Grayscale squint test: gate is the brightest object, headline second, surface markers third.

## Step 4 — Composition map (1080 grid)
Pattern: submerged_section (a horizon/waterline splitting surface from deep), focal on the lower-left third, headline counterweight upper-right.
- Waterline y=298, hand-wobbled, pale-cyan strip. Surface band y in [0,298]; deep water y in [298,1080] darkening downward.
- Polaris (colophon) at (992, 66) r=13, a north star over the sea (surface band).
- Kicker line "THE STACK · REGULATORY · 17 JUL 2026" mono ~17px tracked, at (96, 40) top-left in the surface band.
- Three surface markers (the visible FCC layers) sitting ON the waterline:
  - M1 at x=232, tag "1921 ACT / FCC"
  - M2 at x=486, tag "OI 24-523" (the application entry point; the cable drops from here)
  - M3 at x=742, tag "FCC 25-49"
  Each: a thin stanchion from y=252 to y=298, a cool ring light r=10 at y=250, a faint cool glow, a tiny mono tag above.
- Subsea cable (pale-cyan hand-drawn catenary, dark casing halo): enters at surface M2 (486, 298), dips left in a catenary to the focal gate at (356, 662), passes THROUGH the gate housing, then continues faint and thinner down-right to the landing at (884, 986). Dimension ticks along the upper span (blueprint telemetry).
- Focal gate at (356, 662): schematic sluice housing ~150 wide x 176 tall (x in [281,431], y in [574,750]). Cable enters top center, a CLOSED barrier plate across the throat mid-housing, cable exits bottom. Warm amber glow r~210 centered (356,662), hot core r~46. Mono label in amber "TEAM TELECOM" at (356, 772) and small "CAFP · AG" at (356, 792). This is the one lit object.
- Bathymetric contours: 8 pale-cyan contour lines from a warped field, thresholded, drawn across the deep, curving under and around the gate, denser toward the seabed. Suppressed inside the headline quiet zone and dimmed near the gate so they never fight the focal.
- Seabed ridge silhouette from y~918 rising to ~966 at the landing, darkest navy, with the landing node (small cool square) at (884, 986) and a hairline "AK" shore lip.
- Headline block "THE REAL GATE / IS OFF / THE DOCKET" Fraunces Black, left-aligned, x from 560, three lines, baseline1 y~404, leading ~1.06, sized to fit within x in [560,996]. Sits in the dark deep, upper-right = literally below the docket surface. Cool-white on indigo, contrast > 8:1. A very faint water-tone soft_panel calms any contour behind it.
- Wordmark ALASKA.AI Fraunces ~30px at (96, 1016) bottom-left, cool white in a subtle knock chip.
Eye path: headline (upper right) -> down the cable catenary -> hot gate (lower left) -> faint line to the landing (lower right) -> wordmark.

## Step 5 — Layer build order (back to front)
paper deep indigo -> surface-band gradient (top) -> deep-water gradient (darkening down) -> bathymetric contour lines (masked out of headline zone) -> seabed ridge silhouette -> waterline strip + wobble -> cable casing halo -> cable pale core + dimension ticks -> three surface markers (stanchion, ring, cool glow, tags) -> gate amber glow -> gate housing schematic + closed barrier -> gate hot core + label -> marine-snow stipple/chips (gated below waterline, thinned at focal and headline) -> glints on cable -> grain -> gentle vignette -> soft_panel behind headline -> headline -> kicker -> wordmark -> polaris.

## Step 6 — Technique stack
gradient_v (two bands), field + warp + custom contour tracing via field_mask edges, ridge_pts/ridge_fill (seabed), hand_line + wobble_pts (cable, waterline), glow + gradient_r (gate light), stipple + chips (marine snow), circle/poly (markers, housing), grain, vignette, soft_panel, fraunces/mono/text/chip/polaris. Seed constant in script.

## Step 7 — Risk list + mitigations
1. Contours turning the deep to mud and burying the focal. Mitigation: contours at low alpha (~70/255), suppressed inside the headline box and thinned within ~220px of the gate; keep highest detail-contrast at the gate.
2. Headline colliding with contours/particulate. Mitigation: reserve the headline box as a quiet zone (no contours, no snow there) plus a faint water-tone soft_panel.
3. Gate reading as a vague blob rather than a built barrier. Mitigation: crisp schematic housing with straight blueprint lines and an unmistakable closed barrier plate across the throat; silhouette-test the housing filled dark.
4. Amber focal drifting the dominant hue off indigo. Mitigation: keep amber confined to the gate (~<8% of canvas); dominant remains indigo, logged hue_family indigo.
