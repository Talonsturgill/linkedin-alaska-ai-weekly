# Art plan — The Stack — 11 SEP 2026 — "The Fabric"

## Step 0 — Absorb the story
- **What happened.** On 3 September 2026 NTIA reopened BEAD with a supplemental
  deployment policy notice, letting states redeploy unspent "Benefit of the
  Bargain" savings toward locations the first round missed; Sen. Dan Sullivan
  says it could make over 5,000 Alaska locations eligible.
- **Why it matters to Alaska.** Roughly $370 million of Alaska's already-won
  broadband money, and the last- and middle-mile that every AI workload outside
  the Railbelt depends on, now hangs on one federal officer's approve, reject,
  or reallocate decision under 47 U.S.C. 1702.
- **Emotional register.** Suspended. Tense but quiet. Not triumphant, not
  catastrophic. The feeling of work stopped mid-motion with everything needed to
  finish it already present, waiting on one hand. Patience under a held breath.

## Step 1 — Dedup scan (obeyed; full ledger in scratch)
Scanned all `origin/claude/linkedin-*` branches sorted by ISSUE DATE (not
alphabetically, which surfaces only the pre-bespoke legacy weeklies). 18 real
ledger entries recovered.
- **style_family forbidden (last 8):** halftone_section, exploded_iso_docket,
  landmark_mesh, riso_form, hydrographic_claim, engraved_headworks,
  voronoi_impoundment, constructivist_scatter. `woven_fabric` is unused. CLEAR.
- **hue_family forbidden (last 4):** red, blue, indigo, orange. Chosen **gold**,
  last used 9 issues back (stack 07-10). CLEAR.
- **composition forbidden (last 2):** horizon_band, exploded_iso_stack. Also
  avoided thirds_focal (3x in 18) and scatter_field. Chosen `weave_rupture`,
  unused. CLEAR.
- **motif check.** Gate / valve / sluice / iris imagery is EXHAUSTED (7 of the
  last 18 pieces). This piece deliberately refuses a literal gate as the
  chokepoint device. Woven cloth, loose warp, selvedge and shuttle appear
  nowhere in the ledger. CLEAR.
- The isometric-exploded-diagram register, The Stack's usual default, was LAST
  WEEK's piece. Deliberately not repeated.

## Step 2 — Concept (three generated, one chosen)
1. **The Fabric (CHOSEN).** The FCC's actual statutory artifact is the
   "Broadband Serviceable Location Fabric." Render it literally as woven cloth.
   Each thread crossing is a serviceable location. Across the lower third the
   weave simply stops: weft runs out, warp threads hang loose over a dark void.
   One small shuttle rests on the exact line where weaving halted, loaded and
   motionless. **Why it's true:** "fabric" is the agency's own word, unwoven is
   literally unserved, and a loom advances only one pick at a time and only if
   the shuttle is thrown, which is exactly a single-officer approve/reject
   binary. **Half-second read:** cloth that stops, and the one small object that
   would continue it, doing nothing.
2. *A ledger of 5,000 tally marks, most struck through.* Rejected: cadastral /
   ledger register already used (stack 07-07-02), and counting is a weaker idea
   than making.
3. *A vast dot-field of locations with one lit path.* Rejected: too close to the
   07-31 desk piece (lit hub settlements, thread fan to one point, relay towers)
   and to flow_field 07-10. Connectivity-as-network-diagram is burned.

## Step 3 — Blueprint

### Style family
`woven_fabric` — a textile-object still life rendered as editorial print.
Closest atlas relatives are `engraving` (dense hand craft) and `minimal_line`
(one honest object, generous rest), deliberately hybridized into something the
ledger has never carried. Fits because the mechanism's own name is a weaving
word and because cloth carries "unfinished" better than any diagram can.

### Register carried by palette and form
Low-angle September gold on the finished cloth (Alaska light at h≈85), falling
to a cold spruce-dark void below the rupture. Warmth above, absence below. The
shuttle is the only object with a hard edge and the highest chroma, so the eye
treats it as an actor rather than scenery.

### Palette (OKLCH-built, 6 inks + paper)
| role | hex | OKLCH intent | note |
|---|---|---|---|
| paper / linen ground | `#efe4cc` | L .91 C .045 h 85 | warm bone, carries grain |
| cloth field (lit gold) | `#d9a441` | L .74 C .13 h 82 | the woven acreage |
| cloth shadow / weft dark | `#8a5f28` | L .48 C .09 h 72 | weave seams, depth |
| deep umber ink | `#3a2614` | L .27 C .05 h 62 | type, selvedge, outlines |
| void (unwoven) | `#14180f` | L .13 C .015 h 130 | spruce-black, the absence |
| focal accent (shuttle brass) | `#ffcf5c` | L .87 C .15 h 88 | highest chroma, focal only |

**Value spine:** paper .91 > cloth .74 > shadow .48 > ink .27 > void .13. The
darkest dark (void) sits directly beneath the lightest, most saturated element
(brass shuttle) so the focal wins the contrast war by a full value gap of ~.74.
Grayscale squint test: the piece still reads as bright band / dark band / bright
chip. Nothing else in the frame is allowed above L .80.

### Composition map — pattern `weave_rupture` (1080 grid)
- Headline block: x ∈ [86, 700], two lines, cap-height top at y=132, second
  baseline ~y=246. Sits ON the cloth in its calmest region (upper-left, where
  weft density is dialed down 35% and a soft panel lifts it).
- Kicker line `THE STACK · VEHICLES · 11 SEP 2026`: mono 15px, tracked 0.26em,
  left-aligned x=88, y=292, directly under the headline.
- Cloth field: full-bleed, x ∈ [0, 1080], from y=0 down to the rupture line.
  (Build note: the blueprint first said y=330, but the headline is specified to
  sit ON the cloth at y=132-246, so the bolt runs to the top edge. Corrected
  during Step 4 so plan and code agree.)
- Rupture line: ragged, non-horizontal. Mean y≈706, amplitude ±34, drifting
  lower toward the right so the shuttle sits on a slight rise.
- Selvedge (finished left edge of cloth): x ∈ [44, 62], runs the full cloth
  height, denser and darker — proves the cloth is real and made.
- Void: from the rupture line to y=1080, full width.
- Hanging warp threads: ~180 threads dropping from the rupture into the void,
  lengths 40–330px, lengthening toward the right-centre, a few reaching y≈1040.
- **Shuttle (FOCAL):** centred (742, 694), length ~196px, height ~40px, tapered
  boat spindle with a visible thread eye and a wound bobbin, resting on the
  rupture line at a slight 6° tilt, its brass catching the light.
- Tiny mono label `47 U.S.C. 1702`, 13px tracked 0.18em, at (742, 752),
  centre-anchored, just below the shuttle in the void. This is the chokepoint
  statute and comes straight from the dossier.
- `ALASKA.AI` wordmark: Fraunces Black 30px, bottom-left (86, 1002), knocked
  out light against the void.
- Polaris: (986, 96), r=13, upper-right in the quiet cloth corner.
- **Eye path:** headline (upper-left) → down the warp grain → brass shuttle
  (focal, lit against black) → hanging threads falling away right and down →
  wordmark bottom-left → out.
- Edge discipline: nothing important within 48px of any edge. Negative space is
  the calm upper-right cloth and the lower-left void.

### Layer build order (back to front)
1. Paper ground + `mottle` for linen tone.
2. Void block painted from rupture line to bottom (flat-ish, gets texture later).
3. Cloth base field: `field` + `warp` mapped through gold ramp, so the cloth
   undulates like real fabric rather than sitting flat.
4. **Warp pass** (vertical threads): ~200 threads, slight `wobble_pts`, width
   jittered 1.6–3.0, value jittered against the undulation field.
5. **Weft pass** (horizontal threads): ~230 picks drawn over the warp with
   per-crossing alternation so the over/under actually reads as a weave.
6. Weft density falloff in the headline zone (upper-left) to keep type legible.
7. Selvedge band at the left edge, denser and darker.
8. Rupture edge: fraying — short broken weft stubs, `chips` lint at the tear.
9. Hanging warp threads into the void, with a slight catenary droop and
   `wobble_pts` for gravity and hand.
10. Void texture: `stipple` at very low density so it isn't a flat fill.
11. Shuttle: composed polygons (tapered body, bobbin, thread eye), `hatch`
    shading on its underside, `glow` behind it, specular glints.
12. A single live thread running from the shuttle eye back into the last woven
    pick — the connection that still exists.
13. Finishing: one texture identity only — `grain` at 6.
14. `vignette` 0.14.
15. Type: soft panel, headline, kicker, mono label, wordmark, polaris.

### Technique stack
`field` + `warp` (cloth undulation, scale 3.2), `ramp` (gold value mapping),
`wobble_pts` / `hand_line` (thread humanity), `poly` (shuttle), `hatch`
(shuttle shading, spacing 5), `stipple` (void tooth, density 0.03), `chips`
(lint/fibre at the tear), `glow` (brass), `soft_panel` (headline legibility),
`mottle` (0.05), `grain` (6), `vignette` (0.14), `polaris`.
Explicitly NOT used: halftone, riso, voronoi, iso_prism, reaction_diffusion,
streamlines — all recently burned as primary identities.

### Three scales of detail
- **MACRO:** lit cloth band / dark void / brass shuttle. Reads at 300px.
- **MESO:** the weave itself — warp and weft crossings, the selvedge, the
  fraying rupture edge, the bundle structure of the hanging threads.
- **MICRO:** individual fibre strands off the frayed edge, lint chips, the
  bobbin winding, glints on the brass, paper grain.
No region larger than 15% of the canvas is a flat fill: the cloth is threads,
the void gets stipple tooth and hanging warp.

### Risk list and mitigations
1. **Thread moiré / aliasing** at 2x supersample from near-regular spacing.
   → Jitter every thread's spacing, width and value; apply `wobble_pts`; never
   use a constant pitch.
2. **Weave turning to mud in the midtones**, killing the value spine.
   → Keep warp and weft within a narrow value band and let the underlying
   `field` undulation carry the large-scale light, not the individual threads.
   Re-check grayscale before scoring.
3. **Headline colliding with busy weave.**
   → Dial weft density down 35% in the upper-left zone AND lay a `soft_panel`
   under the type. Two mitigations, because this is the most likely failure.
4. **Shuttle reading as an undifferentiated blob at thumbnail.**
   → Tapered silhouette with a notched thread eye, a value gap against pure
   void, and a `glow` halo. Silhouette-test it filled black before shipping.
5. **Runtime blowout** from ~430 thread draws at 2160px.
   → Cap warp at 200 and weft at 230, draw as simple polylines, no per-thread
   compositing. Target well under 90s.


## Build log (Step 5 eval loop, actual)
Six eval iterations used, plus two script crashes fixed and re-run (numpy 2.x
removed `ndarray.ptp`; `circle` missing from the import list). Per the skill,
crashes do not count as eval iterations.

| iter | weighted | weakest | targeted fix |
|---|---|---|---|
| 1 | 6.73 | craft 5 | `soft_panel` left a visible smudge halo. Weave read as corduroy stripes, not cloth. The 196px shuttle read as a FISH, which fought the concept. |
| 2 | 7.36 | craft 5.5 | True plain-weave checkerboard killed the stripes but went mechanical/carbon-fibre, and the headline quiet zone left a HARD-EDGED rectangle, worse than the halo it replaced. |
| 3 | 7.95 | focal 7 | Smooth elliptical calm zone, per-thread slub tone, low-frequency twill drift and faint continuous warp grain. Cloth now reads as real textile. Shuttle's oval cavity still read as an eye. |
| 4 | 8.24 | focal 7.5 | Rebuilt the shuttle as the actual object: flat-bottomed boat, long rectangular pirn well with a tapered cop on a spindle, steel tips. Eye/fish read gone. Still gold-on-gold with no value gap. |
| 5 | 8.70 | craft 8 | Seated the shuttle mostly over the void, darkened the body to bronze so pirn/tips/glints carry contrast, added a drawn torn edge. Cleared the 8.5 floor. |
| 6 | **8.76** | craft 8.5 | 8.5 is the floor, not the target. Drape folds added meso structure to the upper ~45% of the canvas, which was still flat cloth acreage, and broke the monochrome. |

**Final:** weighted 8.76. Concept 9, Focal 8.5, Composition 8.5, Color 8.5,
Detail 9, Craft 8.5, Typography 9, Originality 9, Fidelity 9. No dimension
below 7. `qa_check.py` PASS (1080x1080 PNG, 1674 KB, stddev 66, 3953
colors@128, meta complete, date and kicker consistent).

**Performance note.** `field()` and `warp()` at native 1080 cost ~112s combined
(45s + 67s), which would have consumed the entire iteration budget on a single
render. The undulation is a large-scale soft gradient, so it is built at 360 and
zoomed 3x with no visible difference. Full render is ~30s.
