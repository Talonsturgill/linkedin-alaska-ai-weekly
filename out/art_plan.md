# Art plan — The Stack — 2026-07-07

## Step 0 — Story absorption
- **What happened:** On June 23 Alaska Energy reported the RCA worries Railbelt ratepayers get stuck paying inflated infrastructure costs to build multiple LNG-import facilities for one small market. Every proposed Railbelt AI data center runs through one fuel gate first.
- **Why it matters to Alaska:** Cook Inlet gas depletion has turned Railbelt replacement fuel into a natural-monopoly build. One RCA cost-recovery vote is the switch on whether any AI data center gets firm power.
- **Register:** Tense, structural, cautionary-analytical. A bottleneck. A wide flow throttled to a single gate.

## Step 1 — Dedup scan
Every prior issue across all `claude/linkedin-*` branches used the LEGACY template (meta shows volume/topic/motto/coords, seed 11, no style_family). This is the FIRST bespoke piece in the series, so no style_family / hue_family / motif / composition cooldown is active. Hard rule still obeyed: NOT the aurora-over-starfield legacy look. Chosen style is a diagram-as-art register, which no prior issue used.

## Step 2 — Concept (three, one chosen)
1. **Exploded iso fuel-stack with one throttling gate (CHOSEN).** Five isometric slabs (gas → terminal → utility → RCA gate → AI load) stacked with gaps. A broad bundle of energy conduits rises from the gas base, necks through a single bright amber iris at the RCA gate, and only ONE conduit continues up to feed a small lit data-center block. Metaphor + synecdoche: the stack IS the mechanism, the iris IS the chokepoint. Reads in <1s: many streams in, one gate, one stream out.
2. Single industrial gate-valve wheel as central icon, gas abundant below, AI load starved above. Rejected: too literal-industrial, loses the five-layer "stack" read.
3. Narrowing ice channel where one ship-terminal fits through, data center glowing on far shore. Rejected: drifts to landscape, the column wants diagram-as-art here.

## Step 3 — Blueprint

**Concept statement.** An exploded isometric fuel stack in which a broad bundle of gas conduits necks through a single amber iris (the RCA cost-recovery gate) and only one conduit survives to power a lit data-center block. The read: Alaska AI power is gated by one decision, drawn as one narrow aperture every stream must pass.

**Register.** Tense and structural. Cool technical navy field carries the machinery; a single warm amber focal at the gate carries the tension (the one decision). Restraint reads as engineering, not decoration.

**Style family.** `iso_cutaway` hybridized with `blueprint` linework (dark technical paper, pale cyan schematic lines, dimension ticks, tiny mono labels). Fits because the story is literally a layered mechanism with a chokepoint; the exploded iso stack is the truest possible diagram-as-art. Clears dedup (first bespoke piece; not aurora/starfield).

**Palette (OKLCH value spine; 7 inks incl. paper).**
- `#0b1a2a` deep navy — paper / darkest field (L~0.20)
- `#10263a` navy-2 — gradient field lower structure (L~0.26)
- `#2e6f8e` mid teal — prism left faces / structure (L~0.52)
- `#5f9cb8` teal-light — prism right/top faces mid (L~0.66)
- `#cfe8f2` pale cyan — schematic lines, type, ticks (L~0.90, the light)
- `#ffb703` amber — focal gate iris + glow (highest chroma, focal accent)
- `#ffe3a3` amber-core — gate hotspot / lit data-center windows (L~0.90 warm)
Value spine: darkest dark = navy field; lightest lights = pale cyan lines and amber core. Focal wins because amber is the ONLY warm hue and sits in a pool of cool navy with a glow halo. Grayscale squint test: the amber iris + its glow is the brightest compact mass → focal survives grayscale.

**Composition map (`thirds_focal`, 1080 grid).**
- Iso tower on the right third. `iso` origin (720, 600), scale 58. Footprint centered on model (0,0).
- Slabs (model z, footprint half-width h so x0=y0=-h, dx=dy=2h):
  - GAS reservoir: z 0.00→1.00, h=1.40 (widest base)
  - LNG TERMINAL: z 1.40→2.30, h=1.20
  - UTILITY: z 2.70→3.60, h=1.20
  - RCA GATE: z 4.00→4.85, h=1.32 (focal, amber; iris on top face)
  - AI LOAD: z 5.25→6.05, h=0.62 (small lit block)
- Gate top-face center ≈ (720, 319); tower spans py ≈ 249 (load top) → ≈ 681 (gas base front corner). Focal amber iris centered ≈ (720, 330) with glow r≈150.
- Broad conduit bundle: 9 pale-cyan lines from gas top face (spread x∈[past,700..740] at py≈540) converging to the gate underside (720, ~360). Drawn BEHIND slabs so they show only in the inter-slab gaps.
- Single bright conduit: one amber line from gate top (720, ~300) to AI-load base (720, ~262), drawn in front (in the top gap).
- Headline block: LEFT quiet column x∈[84, 540], two lines centered y≈396–556. Fraunces poster (wght 900, opsz 144). Line 1 "Alaska AI's Power", line 2 "Runs on One Vote". Fit to width ~452.
- Kicker (mono, tracked 0.22): top-left (96, 150) "THE STACK · FACILITIES · 7 JUL 2026".
- Tiny slab labels (mono ~15px, pale cyan) to the right of each slab: "GAS", "TERMINAL", "UTILITY", "RCA GATE", "AI LOAD" (all from dossier layer names). One tiny "AS 42.05.141" tag by the gate (verified statute).
- Wordmark ALASKA.AI: bottom-left (96, 992), Fraunces black ~30px.
- Polaris colophon: top-right (980, 96), r=13.
- Eye path: headline (left) → amber gate iris (center) → up single conduit to lit AI load → down the broad converging bundle to the gas base → wordmark.

**Layer build order (back to front).** paper navy → vertical gradient field → faint blueprint tick-grid confined to right half → amber glow at gate → broad conduit bundle (behind) → GAS slab → TERMINAL slab → UTILITY slab → GATE slab (3-tone) → single amber conduit → AI-LOAD slab (lit windows) → gate iris blades + hotspot (focal, on gate top face) → slab meso detail (edge ticks, face seams) → tiny mono labels → headline + kicker → wordmark + polaris → grain + gentle vignette.

**Technique stack.** `gradient_v` (field), `iso_prism` (5 slabs, 3-tone), `hand_line`/`line` (conduits, seams, ticks), `glow` (gate halo + load), `circle`/`poly` (iris blades, hotspot), `chips` (gas particles in the base gap), `grain` (finishing), `vignette`. Params: grain 5-7 mono; glow alpha 60-90; hand_line wobble amp 1.2-1.8.

**Three scales of detail.**
- MACRO: 5 slabs, the amber iris, the single conduit, the headline.
- MESO: inside each slab — gas reservoir gets horizontal strata seams + chips (particles); terminal gets two small tank cylinders on its top; utility gets a small transformer/grid line motif; gate top face gets the iris; AI-load gets lit window rows. Converging conduit bundle in the lower gaps.
- MICRO: dimension ticks along the front-left prism edges, seam lines on faces, glints on the iris hotspot, tiny mono labels, gas particle chips.

**Risk list + mitigation.**
1. Iso tower muddies in midtones / reads as a blob → strict 3-tone face shading (top lightest teal, left mid teal, right dark navy-teal), clear gaps between slabs, amber focal isolated in cool field.
2. Headline collides with busy flow → left column is a reserved quiet zone; NO conduits or grid ticks drawn left of x=560; add a faint `soft_panel` behind headline only if contrast check needs it.
3. Diagram reads cluttered / clip-arty → labels tiny and few (5 slab tags + 1 statute), limited 7-ink palette, single warm focal, generous navy negative space around the tower.
4. Conduits look like default Perlin flow → straight converging `hand_line`s with light wobble (not smooth noise streamlines); they visibly funnel to one point at the gate.
