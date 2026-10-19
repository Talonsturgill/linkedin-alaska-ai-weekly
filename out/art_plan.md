# Art plan — The Stack, 21 August 2026

Column marks: kicker `THE STACK`, middle slot `REGULATORY`, date `21 AUG 2026`.
Byline: `""` (not drawn for this column).

---

## 1. Concept statement

A hard-edged surveyed claim boundary is drawn across open tidewater, and the Cook
Inlet current pours straight through it as though it were not there. Physically it
is not there. Legally it is, and it is the only thing in the frame that does not
move.

The read in half a second: **you cannot fence moving water, but paper can.**

## 2. Register

Quiet alarm. Cold, still, faintly unsettling. Not triumphant, not snarky, not
alarmist. The emotional target is the irony of dry bureaucratic precision laid over
something vast and in motion. Palette carries it by keeping the water desaturated
and heavy while the claim linework is the single saturated, man-made thing on the
canvas. Forms carry it by contrast of grammar, organic streamline versus straight
ruled edge with monuments and ticks.

## 3. Style family

`hydrographic_claim` — a deliberate hybrid of a tidal streamline field with survey
/ cadastral linework, read near-plan like a hydrographic chart that someone has
platted a parcel onto.

Why it fits: the mechanism IS a paper boundary over water, so the piece should be
built from exactly those two visual languages in collision. The Stack's
diagram-as-art register earns its place here because the story is literally about
an instrument, not a landscape.

**Dedup clearance** (checked against the 16 most recent `claude/linkedin-*` ledgers):
- style_family: not in the last 8 (`engraved_headworks`, `voronoi_impoundment`,
  `constructivist_scatter`, `organic_rd_moorage`, `wpa_layered_minimal_line`,
  `ukiyo_bokashi`, `geologic_engraving`, `paper_collage`). Deliberately distanced
  from both `flow_field` (stack-07-10) and `cadastral_ledger` (stack-07-07-02),
  which sit outside the cooldown but are the two nearest relatives. Distance is
  enforced by combining them rather than repeating either, and by avoiding both of
  their signature motifs.
- hue_family `green`: last 4 are neutral-cool, violet, blue, teal. Clear.
- composition: last 2 are `frame_within` and `central_icon`. Clear (see the
  anti-frame mitigation in §8).
- motifs: avoids every gate/valve/sluice figure (badly overused by this desk),
  the converging funnel (stack-07-10), bathymetric contours (stack-07-17), the
  cadastral plat (stack-07-07-02), and the exploded iso stack (stack-07-07).
- aurora over starfield: absent.

## 4. Palette (built in OKLCH, value spine first)

| Role | OKLCH | Hex target | Notes |
|---|---|---|---|
| paper / light | L .94 C .012 H 95 | `#f0eade` | cold sand, type zone + brightest rip crests |
| water field | L .58 C .045 H 168 | `#7d9187` | slate green, dominant mass |
| water deep | L .30 C .040 H 172 | `#374b43` | troughs, current shadow |
| ink / land | L .17 C .030 H 160 | `#1b2622` | shoreline wedge, wordmark |
| focal accent | L .56 C .175 H 32 | `#c8552c` | vermilion, claim linework + monuments |
| accent halo | L .22 C .060 H 30 | `#3d1d12` | dark stroke under accent, see §8 risk 2 |

Value structure: darkest dark is the shoreline wedge (L .17) at bottom-left;
lightest light is the paper-toned quiet zone at upper-left where the headline sits.
The focal wins the contrast war not on lightness but on **chroma isolation** — the
vermilion is the only saturated element in an otherwise desaturated field, and it
is backed by the dark halo so it also holds a value gap. Everything else stays
between L .30 and L .58.

## 5. Composition map — `offset_parcel_drift`

Diagonal current thrust running upper-right to lower-left, against a static
off-axis quadrilateral. NOT a centred frame.

Coordinates on the 1080 grid:

- **Current flow direction**: base angle ≈ 208°, i.e. down-and-left. Streamlines
  seeded across the full canvas, density ramping from sparse at upper-left to dense
  at lower-right.
- **Claim quad**: centre `(628, 646)`, nominal 430 × 330, rotated **−14°**.
  Deliberately off-centre (canvas centre is 540,540) and allowed to run out of the
  frame at the right edge so it reads as a surveyed parcel, not a border.
- **Corner monuments**: filled 10px squares with a tick cross at each rotated
  corner, the upper-left monument at approximately `(432, 512)` is the FOCAL POINT.
- **Dimension ticks**: 7px perpendicular ticks every 42px along all four edges.
- **Edge labels** (mono, tiny, tracked): `≈1,650 ACRES` along the lower edge;
  `PRIORITY ONLY · NO CONSTRUCTION RIGHT` along the upper edge. Both are
  dossier-true, see §9.
- **Shoreline wedge**: bottom-left, `x ∈ [0, 320]`, `y ∈ [past 826, 1080]`,
  irregular coast built from `ridge_pts`.
- **Substation glyph** (Bernice Lake landfall): micro detail at `(158, 902)`,
  ~34px wide.
- **Headline block**: `x ∈ [88, 604]`, top at `y = 104`. `COOK INLET,` / `BANKED`,
  Fraunces Black, two lines, tight leading.
- **Supporting line**: `BEFORE ALASKA CAN OBJECT`, small, at `y ≈ 322`.
- **Kicker**: `THE STACK · REGULATORY · 21 AUG 2026`, JetBrains Mono, tracked
  0.22em, at `y ≈ 366`.
- **Wordmark** `ALASKA.AI`: bottom-left `(88, 1004)`, Fraunces Black ~30px.
- **Polaris**: `(978, 96)`, r = 13.

Eye path: headline (upper-left, quiet) → down the diagonal current → collision at
the upper-left corner monument (focal) → along the ruled edge into the parcel →
out to the shoreline wedge and wordmark at bottom-left.

Negative space: the upper-left third is deliberately calm and paper-toned. That is
the planned headline zone, not leftover space.

## 6. Layer build order (back to front)

1. Paper base fill
2. Water tonal field (`field` + `warp`, mapped paper→water deep)
3. Broad current bands (thick, low-contrast streamlines, meso structure)
4. Mid streamlines (the main tidal texture, density ramp applied)
5. Tide-rip shear lines (2 or 3 converging light crests, high value)
6. Fine hairline eddies (micro)
7. Silt `chips` + `stipple` foam, concentrated mid-field
8. Shoreline wedge (`ridge_pts` coast, flat dark fill)
9. Substation glyph (micro built detail)
10. Claim quad dark halo stroke
11. Claim quad accent linework, ticks, monuments
12. Monument glow (very subtle)
13. Mono edge labels
14. Grain (single finishing texture identity)
15. Vignette (light)
16. Type: headline, supporting line, kicker, wordmark, polaris

## 7. Technique stack

`field` + `warp` (water tone), `angle_field` + `streamlines` with a quantised /
curl-distorted angle source rather than plain smooth Perlin (tidal current at three
scales), `ridge_pts` (coastline), `hand_line` + light `wobble_pts` (claim edges,
just enough humanity to avoid a vector look while staying ruled), `chips` +
`stipple` (silt and foam), `glow` (monuments, subtle), `grain` 5–7 (single texture
identity), `vignette` 0.14, `polaris`, `fraunces` / `mono` / `chip` for type.

## 8. Risk list

1. **Streamlines become decorative noise and dilute the boundary.**
   Mitigation: hard density ramp (sparse upper-left → dense lower-right) so detail
   contrast peaks exactly at the focal corner monument, and cap the fine-eddy pass
   to the mid-field band only. Edges of the canvas stay calm.

2. **Vermilion on slate-green vanishes in the grayscale check** — both land near
   L .56. This is the single biggest craft risk in the plan.
   Mitigation: every accent line gets a 2px dark halo stroke (`accent halo`,
   L .22) drawn underneath and offset, so the linework holds a real value gap
   independent of hue. Run an explicit grayscale check in the eval loop.

3. **The quad reads as a picture frame**, which would both look amateur and trip the
   forbidden `frame_within` composition.
   Mitigation: rotate −14°, place off-centre, crop it at the right canvas edge, and
   load the edges with monuments, ticks and mono labels so it reads unmistakably as
   a surveyed parcel rather than a border device.

4. **Headline collides with busy current texture.**
   Mitigation: the density ramp already reserves the upper-left as the quiet zone.
   If the eval still shows collision, add a soft paper panel behind the type rather
   than shrinking the headline.

## 9. Text on the artwork — provenance

Only these strings appear beyond the fixed marks, and each traces to the verified
dossier at `out/stack_anatomy.json`:

- `COOK INLET, BANKED` / `BEFORE ALASKA CAN OBJECT` — the writer's quotable
  headline, tightened typographically as the skill permits.
- `≈1,650 ACRES` — the corridor size, per `ak_consequence` and Layer 1.
- `PRIORITY ONLY · NO CONSTRUCTION RIGHT` — paraphrases Layer 3 and the Layer 4
  FERC notice quote, "The sole purpose of a preliminary permit is to grant the
  permit holder priority to file a license application... does not authorize the
  permit holder to perform any land-disturbing activities."

No docket number appears anywhere on the artwork. No dollar figure, no signatory
name, no beluga or habitat reference, per the dossier's `do_not_assert` list.
No Alaska Native visual traditions are referenced or imitated anywhere in the piece.
