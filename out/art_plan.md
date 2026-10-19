# Art plan — The Stack, 7 AUG 2026
## "One Signature Moves 19,950 Acres"

---

## Step 0 — Absorb the story

**What happened.** Alaska DNR is deciding whether to convey roughly 19,950 acres near
Houston to AIDEA under a statute titled "public and charitable use," noncompetitively,
before any tenant, power source, water plan or schedule exists.

**Why it matters to Alaska.** Sovereign land is being pre-positioned into a bondable
financing vehicle ahead of AI and data-center demand, on one officer's discretion with no
competitive test, and the reversionary interest that would claw it back is waivable by
that same officer.

**Emotional register.** Cool, watchful, quietly unnerving. Not outrage, not alarm. The
specific unease of an enormous thing resting on a very small fastening that somebody is
allowed to untie. Restraint is the whole tone. The piece should feel patient and cold.

---

## Step 1 — Dedup scan (obeyed, not skipped)

Ledgers read across all `claude/linkedin-*` branches, sorted by issue date.

**style_family forbidden (last 8 issues):** ukiyo_bokashi, wpa_layered_minimal_line,
geologic_engraving, paper_collage, bathymetric_blueprint, flow_field, swiss_grid,
cadastral_ledger, iso_cutaway.
**hue_family forbidden (last 4 dates):** magenta, orange, green, neutral-warm, indigo, gold.
**composition forbidden (last 2 dates):** diagonal_thrust, horizon_band, bilateral_gate,
scatter_field.
**motifs forbidden (last 10):** gate iris, valve, sluice, funnel throat, geologic strata
section, cadastral plat, consent seal, survey ticks, north arrow, modular cell grid, torn
paper drift, catwalk, converging conduits, transmission-tower glyph, targeting reticle.

**SPECIAL HAZARD.** Issue 2026-07-07-02 was the desk's *other* DNR land-disposal story and
used `cadastral_ledger` + `central_icon` + cadastral plat + consent seal + survey ticks +
north arrow. This piece is the second DNR land mechanism in five weeks. It must therefore
share **none** of that visual vocabulary. Hard rule for this render: no straight parcel
boundaries, no seal, no ticks, no north arrow, no surveyed rectangles, no map register.
The land is organic geometry only.

**Chosen and clear:** style `organic_rd_moorage` (reaction-diffusion muskeg hybridised with
fine schematic hand-line), hue `teal`, composition `thirds_focal`. None are cooling down.

---

## Step 2 — Concepting (three, then one)

**A. The single fastening.** A vast muskeg landmass floating as a moored raft on cold
water, held by one hairline filament to a small mooring pin. The filament frays near the
pin. Metaphor is exact — the reversionary interest is the only thing tying that land to
its restricted use, and the officer who applies the restriction may untie it. Scale
contrast plus synecdoche. Reader gets it in half a second: *enormous thing, one thin
thread, and the thread is failing.*

**B. Ink becomes coastline.** A pen stroke magnified until its edge is the property
boundary. **Killed** — lands squarely in plat/cadastral territory, which is the one thing
this piece cannot resemble.

**C. The charitable-use garment.** A heavy industrial form draped in thin charitable
cloth. **Killed** — reads as editorial cartoon, not editorial art, and renders poorly
procedurally.

**Chosen: A.** It is of Alaska (moorage, tidewater, muskeg from altitude), of this story
(the waivable tether), and it is not a diagram of a process, which is what the last two
Stack covers already were.

---

## Step 3 — Pre-production blueprint

### 1. Concept statement
Nineteen thousand nine hundred fifty acres rendered as an immense raft of muskeg on cold
water, cropped by the frame because it is larger than the canvas can hold, moored by a
single ember-bright filament to one small pin. The filament is fraying at the pin.

### 2. Register carried by form
Cold, patient, unnerving. Carried by a near-monochrome cold-teal field at low internal
contrast, an enormous low-energy mass, and exactly one warm high-chroma element the size
of a fingernail. The warmth is the human decision inside a cold system, and it is the only
thing in the frame that is small enough to move.

### 3. Style family
`organic_rd_moorage` — reaction-diffusion labyrinth morphology masked into an organic
landform (this is genuinely what Mat-Su wetland reads like from altitude), finished with
sparse hand-line for the filament and pin. Fits because the subject is *land that has not
been surveyed into anything yet* — pre-development, undifferentiated, organic. A schematic
style would falsely imply a plan exists, which is precisely what the trigger quote denies.
Clears all cooldowns.

### 4. Palette (OKLCH-built, value spine first)

| role | hex | L | note |
|---|---|---|---|
| paper / ice light | `#dbe8ec` | 0.92 | type, shoreline rim, water sheen |
| field teal | `#2f7f8c` | 0.58 | open-water mid, RD channel highlights |
| shadow | `#123640` | 0.28 | mass body, water depth |
| ink | `#07161b` | 0.13 | darkest mass interior, bottom-right falloff |
| ember (focal) | `#e4573f` | 0.62 | filament + pin ONLY, ~1% of canvas |
| polaris gold | `#f0c987` | 0.85 | colophon star only |

**Value structure.** Darkest dark is the mass interior and the lower-right corner (L 0.13).
Lightest light is the headline and the upper-left water sheen (L 0.92). The focal wins the
contrast war not on value but on **chroma and hue isolation** — it is the only warm hue in
a fully cold frame, set against a mid-value sheen so it also carries a real value gap.
Grayscale check: mass reads as a dark shape against mid water, headline reads white, pin
reads as a small mid-light node. Passes.

### 5. Composition map — `thirds_focal` on the 1080 grid

- Headline block left edge `x=96`. `ONE SIGNATURE` baseline `y=200` at ~96px.
  `MOVES 19,950 ACRES` baseline `y=278` at ~58px.
- Kicker `THE STACK · SOVEREIGNTY · 7 AUG 2026`, JetBrains Mono 17px, tracking 0.22em,
  at `(96, 322)`.
- **Mooring pin (FOCAL)** centre `(206, 512)`, post height ~34px, eyelet ring r≈9.
- **Filament** catenary from `(206, 505)` to the mass bow at `(585, 780)`, sagging ~42px
  below the chord. Fraying strands splay between `t=0.06` and `t=0.22` (near the pin).
- **Land mass** silhouette spans `x∈[430, 1150]` (bleeds off right edge),
  `y∈[700, 1170]` (bleeds off bottom edge). Bow tip `(585, 780)`.
- Polaris `(960, 150)`, r=13.
- `ALASKA.AI` wordmark bottom-left `(96, 996)`, Fraunces Black 30px, on open water.
- Negative space held open: the upper-right quadrant and the left margin band below the
  kicker down to y≈960 are open water carrying only gradient and micro-texture.

**Eye path:** headline → kicker → down-left to the ember pin → along the fraying filament
→ out into the vast mass filling the lower-right.

Nothing important sits within 48px of any edge except the deliberate bleed of the mass,
which is the point.

### 6. Layer build order (back to front)
1. Base vertical gradient, `#16404a` top to `#061419` bottom.
2. Cold sheen glow upper-left at `(250, 300)`, pale cyan, low alpha.
3. Water field — warped noise, very low contrast, plus sparse `streamlines` for slow
   current, all within 0.06 value of the base.
4. Mass silhouette — union of three overlapping `blob_pts` with differing wobble and
   harmonics, then `wobble_pts` on the union; inlets and bays cut along the upper edge so
   the outline has structure rather than reading as one lozenge.
5. RD texture masked into the mass — peat hummocks dark, water channels punching pale.
6. Atmospheric ramp — mass lightens and desaturates slightly toward the far right edge.
7. Shoreline rim — pale ice hairline along the upper-left edge of the mass only.
8. Micro pass — `chips` (pale gravel/ice), `stipple`, a few glints in the channels,
   concentrated near the bow and thinning toward the edges.
9. Filament glow, then filament, then fraying strands, then the pin.
10. Grain, light vignette.
11. Type — headline, kicker, wordmark, polaris.

### 7. Technique stack
`gradient_v`, `glow`, `field` + `warp`, `streamlines` (sparse, low alpha),
`reaction_diffusion` (masked), `blob_pts` + `wobble_pts`, `voronoi_polys` (hummock cells
along the mass edge), `chips`, `stipple`, `hand_line` (fray), `grain`, `vignette`,
`polaris`, `fraunces` / `mono`.

RD parameters: `steps≈2600, f=0.037, k=0.061, res=216` for coral-labyrinth morphology.
Streamlines kept under 140 at low alpha so they never compete.

### 8. Risk list and mitigation

1. **Mud in the midtones.** RD across a big mass can turn to grey sludge.
   *Mitigation:* keep the mass body in the L 0.13–0.35 band, let channels punch to L≈0.72
   only in thin veins, and keep open water at a distinct L≈0.45 so mass and water never
   converge. Grayscale check every iteration.
2. **Headline collides with texture.** *Mitigation:* the mass top edge is held below
   y=700 and the headline zone above y=340 is open water carrying gradient only. If any
   streamline strays up, clip the streamline region to y>380.
3. **Filament illegible at 300px thumbnail.** *Mitigation:* 3.2px design width (well above
   the 2px floor), a soft ember glow beneath it, and the pin as a bright terminal node so
   there is a point of entry even when the line itself dissolves.
4. **Mass reads as an undifferentiated blob.** *Mitigation:* build from three unioned
   blobs, cut real inlets along the upper edge, add the pale shoreline rim so the
   silhouette has articulation. Silhouette test in isolation before shipping.
5. **Fray reads as a rendering bug.** *Mitigation:* fraying strands must be clean, tapered,
   deliberate hairlines that splay in a consistent direction, never a broken or dashed main
   line. The main filament stays continuous end to end.
6. **Resembling the 2026-07-07-02 cadastral piece.** *Mitigation:* the hard rule in Step 1.
   Organic geometry only, no map register anywhere in the frame.

---

## Ledger targets
`style_family` organic_rd_moorage · `hue_family` teal · `composition` thirds_focal ·
`motifs` [moored land raft, single fraying filament, mooring pin, muskeg labyrinth,
cold open water] · `seed` 819 · kicker `THE STACK` · middle slot `SOVEREIGNTY` ·
byline `""` (not drawn for this column).
