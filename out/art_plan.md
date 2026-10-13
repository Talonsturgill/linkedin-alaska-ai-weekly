# Art plan — The Stack — 21 SEP 2026
## "The Last Inch"

### Step 0 — Absorb the story
- **What happened.** The Air Force opened a wetlands comment period, closing Sept. 30,
  on the preferred site for a 5-megawatt micro-reactor inside the fence at Eielson AFB.
- **Why it matters to Alaska.** It is the only firm behind-the-fence generation in motion
  for Interior Alaska compute, but the Air Force cannot buy that power until the Secretary
  of Defense approves a 30-year contract that does not yet exist.
- **Register.** Wry, cool, quietly ironic. Tense but completely still. Everyone is working
  at the visible gate down in the muskeg; the decisive one is silent and somewhere else.
  Not cautionary, not triumphant. The emotion is *arrested motion*.

### Step 1 — Dedup confirmation
Ledger scanned across all `claude/linkedin-*` branches, sorted by the date in the branch
name (the skill's `sort -r` snippet sorts by column name and returns stale nulls — noted
for the Editor's note).
- **style_family, last 8 forbidden**: pixel_dither_aerial, woven_fabric, wpa_scaffold,
  exploded_iso_docket, halftone_section, riso_form, landmark_mesh, hydrographic_claim.
  → `machined_plate` is new to the ledger. CLEARS.
- **hue_family, last 4 forbidden**: green, gold, teal, blue. → `violet` last appeared
  14 AUG (position 9). CLEARS.
- **composition, last 2 forbidden**: aerial_plan_view, weave_rupture (+diagonal_thrust).
  → `suspended_gap` is a new pattern. CLEARS.
- **motif, last 10 forbidden**: exploded isometric assemblies, permit forms and stamp
  blocks, survey parcels / stakes / monuments / section lines, dithered aerial raster,
  weaving and thread, spillway crest gates, moorage and mooring pins, bathymetric
  contours, geologic strata, facial-landmark mesh, torn public-comment paper.
  → No coupling, connector, busbar or insulator appears anywhere in 17 issues. CLEARS.
- Deliberately pushing AWAY from the document/diagram/survey register The Stack has used
  for eight consecutive issues. This piece is physical, material and industrial.

### Step 2 — Concepts considered
1. **"The Last Inch"** *(CHOSEN)*. Two halves of a monumental high-voltage coupling, one
   rising out of Alaska muskeg, one descending from off the top of the frame, held apart
   by a narrow pale slot. Energized amber conductors climb the lower half and stop dead at
   the slot. Metaphor: the unsigned approval as a physical air gap in a power connection.
   Half-second read: *power that arrives and does not connect.*
2. **"The Quiet Desk."** A tiny lit government desk on vast tundra, one unsigned page.
   Killed: desks are generic office imagery, and "paper" sits too close to the burned
   torn-public-comment-paper motif from 24 JUL.
3. **"Thirty Winters."** The 30-year contract term as a receding rank of markers across
   ice. Killed: too abstract, no focal point, and marker/stake geometry is burned.

### Step 3 — Blueprint

**Concept statement.** A high-voltage coupling is split in two. Alaska has built and
energized its half; the other half hangs from outside the frame, inert, and the last inch
between them is empty.

**Register carried by form.** Absolute vertical stillness, one hard horizontal void. The
palette is a cold violet winter dusk so the single warm ink reads as the only live thing
in the picture, and it is the thing that stops short.

**Style family.** `machined_plate` — technical catalog illustration (hard stepped tonal
shading on metal, precise specular edges, bolt-and-flange vocabulary) finished like a
printed editorial plate (grain, faint mottle, slightly imperfect hand-drawn organic
edges). Fits because the mechanism itself is an acquisition of hardware, and because a
parts-catalog register is exactly the cold, administrative voice the post is critiquing.

**Palette** (OKLCH-built, 6 inks + paper). Value spine enforced before hue.
| role | hex | L | note |
|---|---|---|---|
| paper / lightest light | `#f4f0f8` | .95 | the GAP is this value — focal wins the contrast war |
| sky deep | `#241a3e` | .22 | top of frame |
| sky mauve | `#7d6590` | .52 | horizon band |
| ink / darkest dark | `#150f28` | .13 | metal shadow, silhouettes |
| metal light face | `#bcaad0` | .74 | lit faces of the coupling |
| amber accent | `#e2883a` | .68 | conductor cores only, capped under 3% of canvas |

Darkest dark `#150f28` sits directly against lightest light `#f4f0f8` at the gap — a
value gap of .82, the largest in the piece, at the focal point. Grayscale squint test:
everything else lives between .22 and .74, so the slot is the only near-white and reads
first at 300px. Amber is the highest chroma but occupies tiny area, so it accents rather
than competes.

**Composition map — `suspended_gap`** (1080 grid, design units)
- Horizon `y = 742`. Sky occupies the top 69%.
- Coupling axis `x = 700`. Column half-width ~150, so the assembly spans `x ∈ [550, 850]`.
- **Upper half**: enters at `y = 0` (cut by the frame, deliberately — it comes from
  elsewhere), descends to its contact face at `y = 452`. Widest flange at `y ∈ [250, 300]`.
- **THE GAP (focal)**: `y ∈ [452, 498]`, 46px tall, `x ∈ [560, 840]`. Pure paper value.
- **Lower half**: contact face at `y = 498`, descends through insulator sheds
  `y ∈ [520, 650]`, into a bolted base plinth `y ∈ [650, 726]`, rooted in the muskeg berm.
- **Headline block**: `x ∈ [96, 520]`, three lines, top at `y = 120`, ~74px Fraunces Black,
  leading 1.06. Sits entirely left of the column — quiet zone is `x < 540, y < 380`.
- **Kicker** `THE STACK · VEHICLES · 21 SEP 2026`: JetBrains Mono 16px, tracked 0.22em,
  at `(96, 392)`.
- **Support label** `EIELSON AFB · 5 MW`: Mono 14px tracked, at `(556, 782)`, directly
  under the plinth. Both facts are in the dossier.
- **Eielson silhouette**: far left on the horizon, `x ∈ [104, 430]`, hangar roofs and the
  1950s plant stack with a thin plume, capped at `y = 700`.
- **Wordmark** `ALASKA.AI`: Fraunces Black 30px, bottom-left `(96, 988)`.
- **Polaris**: `(956, 116)`, r = 13.
- **Eye path**: headline → kicker → down the dark column → arrested at the pale slot →
  down the amber conductors into the muskeg → left along the waterline to the base
  silhouette → wordmark.
- Nothing important within 48px of any edge except the upper half, which is cut by the top
  edge on purpose.

**Layer build order (back to front)**
1. Paper base + faint paper mottle.
2. Sky gradient `#241a3e → #7d6590`, with low-res noise banding.
3. Far ridge (Interior hills), lightened toward the sky for atmosphere.
4. Eielson installation silhouette on the horizon + stack plume.
5. Muskeg ground mass, berm profile with hand-drawn wobble.
6. Water pools (voronoi cells clipped to the ground), dark seams, thin ice sheets.
7. Tussock and sedge meso banding.
8. Lower coupling half: plinth → bolt ring → insulator sheds → conductor bundles → contact
   face. Stepped 3-tone shading.
9. Amber conductor cores + their glow, terminating hard at `y = 498`.
10. Upper coupling half: shaft → flange → bolt ring → contact face. Same shading grammar,
    but NO amber and a colder, greyer light — it is not energized.
11. Micro pass: bolt heads, specular glints on flange corners, rime frost stipple on the
    upper half only, ice chips at the waterline.
12. Grain finish (single texture identity).
13. Type: headline, kicker, support label, wordmark, polaris.

**Technique stack.** `gradient_v` (sky), `field`/`field_mask` at **w=h=300 then upscale**
(mottle + ground masks — full-resolution `field` costs 52s and `warp` 78s, measured; this
is the runtime fix), `ridge_pts`/`ridge_fill` (hills), `voronoi_polys` (water cells,
0.1s), `poly`/`circle` (machined parts), `hatch` (metal shading), `stipple` (rime),
`chips` (ice debris), `wobble_pts`/`hand_line` (organic edges), `glow` (amber cores),
`grain` (finish), `polaris`, `fraunces`/`mono`. **`angle_field` and `streamlines` are
banned from this script** — `angle_field` takes 53s and accepts no resolution parameter.

**Risk list**
1. *The two halves read as one undifferentiated blob at thumbnail.* → Silhouette test in
   isolation; give the halves different profiles (upper = plain shaft + one wide flange,
   lower = stacked insulator sheds + plinth) so the gap is legible as a break, not a seam.
   The near-white slot guarantees separation at 300px.
2. *Mud in the midtones — violet metal against a violet sky.* → Force the value spine:
   sky stays .22–.52, metal goes to .13–.25 in shadow with .74 lit faces only on
   frame-facing planes. No metal tone may fall inside .45–.55, the sky's range.
3. *Headline collides with the column or the busy muskeg.* → Hard quiet zone `x < 540,
   y < 380`, column starts at x=550. Headline gets paper-value knockout, no chip needed.
4. *Amber overwhelms and turns the piece into a power-company ad.* → Cap amber at <3% of
   canvas, confined to conductor cores under 6px wide and three glints. No amber above
   `y = 498`, ever — that is the whole point.
