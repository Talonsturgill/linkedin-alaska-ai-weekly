# The Stack — Art Plan — 7 JUL 2026

Mechanism: ADNR State-Land Disposal Gate for the Stak Energy North Slope AI Data-Center Lease.
Headline: ONE SIGNATURE / FIFTY-YEAR GATE.
Kicker on art: THE STACK · FACILITIES · 7 JUL 2026. Byline: "" (not drawn).

## 1. Concept statement
The entire North Slope state-land tract Stak Energy wants reduces to a single official consent stamp. The frame is a cadastral land-disposal document, a surveyed parcel drawn as a plat, and the Commissioner's vermilion consent seal is stamped across it as the one focal, while hundreds of tiny public-comment marks drift and pile against a single closed gate in the parcel boundary but none pass through. The read in half a second: one red stamp decides all this land, and the comments are not the gate.

## 2. Register
Cool-institutional, quietly tense, weighty. The gravity of one signature over a vast tract. No snark, no triumph. Restraint carries it. Warm ledger paper + survey ink + one decisive red says "legal instrument," and the lone red seal against a field of stopped comment-marks says where the leverage actually sits.

## 3. Style family
`cadastral_ledger` (a deliberate hybrid): engraving/blueprint linework discipline (hatch + stipple + hand-drawn survey lines) on warm ledger paper, with topo/cartographic elements (irregular parcel polygon, section grid, metes-and-bounds ticks, contour hints, north arrow, a river line) and swiss-grid type discipline for the headline. WHY it fits: this is a state-land DISPOSAL story, a legal document and a survey plat, not an infrastructure cutaway. Dedup clearance: yesterday's stack (7 JUL) was `iso_cutaway` / `blue-teal` / `thirds_focal` / motifs {exploded fuel stack, gate iris, converging conduits, data-center block}. This piece is a different style family (cadastral document, not exploded isometric), a different hue (warm cream + red, not blue-teal), a different composition (central_icon, not thirds_focal), and different motifs (cadastral plat, consent seal, comment-mark drift, survey ticks, north arrow). No aurora/starfield.

## 4. Palette (value spine, cream + ink + one red)
- paper (ledger cream) `#ece3cf` — L high (~0.90), the document ground.
- parcel fill (warm parchment) `#d8c9a3` — L ~0.78, a clear value step below paper so the tract reads.
- survey ink (warm near-black) `#241f18` — darkest, L ~0.16, headline + primary linework.
- graphite (mid) `#7a6f57` — L ~0.48, section grid, secondary ticks, contours.
- consent vermilion (focal accent) `#c0341d` — highest chroma, mid-dark value, the seal + the gate latch + process stage 03. Wins the contrast war on cream.
- slate (cold restraint) `#4d6473` — muted, tiny area only (river line + a few comment marks), so the dominant hue stays warm/red.
- polaris gold `#ffc72c` — colophon star only, tiny.
Value structure: darkest dark = survey ink headline; lightest light = paper; the focal (vermilion seal) owns the only high-chroma mass and sits on the light paper/parchment so it pops. Everything else stays lower chroma than the seal. Grayscale squint test still reads: big red disc becomes the darkest round mass over a light field.

## 5. Composition map (central_icon on the 1080 grid)
Safe area 48..1032. Eye path: HEADLINE (top-left) -> RED SEAL (center focal) -> COMMENT DRIFT piling at the gate (lower-left) -> WORDMARK (bottom-left); NORTH ARROW + Polaris (top-right) counterweight.
- Kicker line: mono ~17px, tracked 0.22, survey ink, top-left baseline (72, 78). Text "THE STACK · FACILITIES · 7 JUL 2026".
- Headline: Fraunces poster (wght 900, opsz 144), survey ink, left rag x0=72. Line 1 "ONE SIGNATURE," top ~152; Line 2 "FIFTY-YEAR GATE" top ~292. Sizes fit to width <=940, same size both lines, leading ~1.06. Quiet zone reserved: the upper ~40% (y<430) stays calm paper (grain + faint contours only), no busy texture behind the type.
- Parcel polygon (irregular 7-vertex tract), lower-center, approx vertices: (168,560),(470,486),(742,470),(930,604),(886,872),(560,900),(250,860). Center ~ (560,690). Filled parchment, dark boundary, section grid + contours + ticks inside.
- Single GATE: a gap with two posts on the left boundary near (206,704), facing the comment drift, with a short vermilion latch line.
- CONSENT SEAL (focal): center (632,606), outer r=148 (top ~458, clears headline). Vermilion inked disc + faint emboss shadow, two cream rings (r=126, r=112) with 48 short cream border ticks between them, inner cream text stack "COMMISSIONER" (mono ~15) / "CONSENT" (Fraunces ~40 tracked) / "AS 38.05.035(e)" (mono ~16). All three strings are dossier-grounded (chokepoint actor, binary decision, statute).
- COMMENT DRIFT: ~360 tiny rotated ticks in region (60..250, 520..885), biased dense toward the gate at (206,704); mostly graphite, a few slate. A knockout chip "500+ COMMENTS" (mono ~16) at ~(96,908). ("More than 500 public comments" is the verbatim news trigger.)
- PROCESS LADDER (the 4 dossier layers): right margin x~972, four 26px squares at y=496,586,676,766 with mono numerals 01..04 to their left; stage 03 (Commissioner consent) filled vermilion, 01/02/04 graphite outline. Tiny.
- Data-center FOOTPRINT: small graphite rectangle ~ (612,772)-(704,828) inside parcel, faint hatch, no size label (unverified, so unlabeled).
- River line: a slate hand-line across the lower-left parcel corner, unlabeled.
- North arrow: top-right, shaft (966,180)->(966,110), head at top; Polaris star as its tip at (966,96) r=13; mono "N" at (966,196).
- Wordmark "ALASKA.AI": Fraunces Black ~30, survey ink, bottom-left baseline (72,1014).

## 6. Layer build order (back to front)
paper cream -> paper mottle + faint large-scale tone field -> faint topo contour lines (denser lower half) -> parcel fill + boundary -> section grid clipped to parcel -> contour hints + river line clipped to parcel -> footprint rectangle -> metes-and-bounds ticks + bearings + the single gate -> comment-drift ticks -> hatch/stipple shading (parcel corners + under-seal) -> consent seal (emboss shadow, disc, rings, border ticks, inner type) -> process ladder -> north arrow + Polaris -> type (kicker, headline, wordmark, 500+ chip) -> grain + light vignette.

## 7. Technique stack
`field`+`warp` (tone + contour source), manual section grid clipped via a parcel L-mask (Image.composite two-mask trick like `hatch`), `hand_line`/`wobble_pts` (survey-line humanity), `hatch` + `stipple` (parcel-corner + under-seal shading, engraving read), `chips` and manual tick scatter (comment drift + dust), `circle`/`poly` (seal + rings + gate posts), `text`/`fraunces`/`mono`/`chip` (type), `grain` (4-8) + `mottle` (0.03-0.06) + light `vignette` (single finishing texture identity = grain).

## 8. Risk list + mitigation
1. Seal micro-text unreadable or messy -> keep to three short high-contrast cream strings, large, centered, verified at full size; no circular per-char text.
2. Headline colliding with busy plat texture -> reserve the calm upper 40% for type; parcel and seal live in the lower/center; add a faint `soft_panel` behind the headline only if contrast dips.
3. Mud in midtones / parcel fill too near paper -> distinct value step (parchment vs cream) + a firm dark boundary line; hatch/stipple only in corners so the tract never grays out.
4. Comment drift reading as random noise -> give the ticks a shared drift direction toward the gate and cap with the labeled chip; keep them smaller and quieter than the seal.
5. Ink count creep -> hold to 6 working inks + tiny polaris gold (<=7 logged); no extra hues.

SEED = 738.
