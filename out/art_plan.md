# Art plan — Anchorage Desk — 24 JUL 2026

## Step 0 — Absorb the story
- **What happened.** John Boyle, Stak Energy's chief strategy officer and Alaska's DNR
  Commissioner until 2025, publicly sorted the public comments opposing his own
  company's North Slope lease into substantive and non-substantive piles while the
  state's review was still open.
- **Why it matters to Alaska.** A $10B+, 1GW+ campus is the largest AI-adjacent
  infrastructure proposal on the state's books, and the applicant's own executive
  grading the opposition hands critics a process argument that could cost the project
  more than the comments ever would.
- **Register.** Wry and cool, with an edge. Not scandalised, not celebratory. The tone
  of a raised eyebrow at a procedural fact. Bureaucratic materials, human stakes.

## Step 1 — Dedup scan (clears)
Six prior bespoke ledgers, all on stack branches. Forbidden this run:
- style: geologic_engraving, bathymetric_blueprint, flow_field, swiss_grid,
  cadastral_ledger, iso_cutaway, aurora_field (permanent).
- hue (last 4): green, indigo, gold, neutral-cool.
- composition (last 2): bilateral_gate, submerged_section.
- motifs (last 10): ore bodies, valves, reticles, strata, conduits, subsea fiber,
  sluice gates, bathymetric contours, funnels, modular grids, transmission towers,
  cadastral plats, seals, survey ticks, north arrows, exploded stacks, gate irises,
  data-center blocks.

**This piece uses `paper_collage` / neutral-warm / `scatter_field`. All three clear.**
No prior desk issue has bespoke art at all, so there is nothing to repeat within the
column either.

## Step 2 — Concept (three generated, one chosen)

1. *Revolving door in a state office lobby.* Rejected. Generic, could run on any
   politics blog, and it illustrates the biography rather than the decision.
2. *Tundra parcel outlined against vast emptiness.* Rejected. It is the Mahoney/DNR
   lease story, which is the permanently blocked prior issue, not this one.
3. **CHOSEN — the red pen through the drift.** A vast drift of torn public-comment
   paper sweeps across the frame like a snowdrift. A single confident red pen stroke
   cuts diagonally through it. On the far side, three scraps sit alone, marked and
   kept. Everything else is set aside.

**Concept statement.** The public's comments become a physical drift of torn paper, and
someone has run a red pen through it, keeping three sheets. The reader gets the whole
argument in half a second, an enormous pile swept aside by a hand that belongs to the
applicant. The medium is the subject: paper about paper.

Why it is true to the story: the decision literally was a sorting of comments into
substantive and non-substantive. The red pen is the grading metaphor the desk position
turns on ("the triage was ordinary, the messenger was wrong"). The drift reading as an
Arctic snowdrift, plus a faint North Slope horizon, keeps it OF ALASKA without a single
generic tech-blog image.

## Step 3 — Blueprint

### Register carried by palette and form
Bureaucratic warmth (bone paper, manila, archive grey) for the drift, so it feels like
documents and not decoration. One hot vermilion for the pen, which is the only
saturated ink in the piece and therefore automatically the focal. Cold would read as
scandal; warm reads as procedure, which is the honest register.

### Palette (neutral-warm + one accent)
| hex | role | notes |
|---|---|---|
| `#ece3d1` | paper (ground) | warm bone, L≈0.90 |
| `#dbd0b8` | scrap light | L≈0.83 |
| `#c3b394` | scrap mid | L≈0.73 |
| `#9d8b6c` | scrap dark / shadow side | L≈0.58 |
| `#6b5c46` | far horizon, atmospheric | L≈0.40 |
| `#332b21` | ink (type, seams, deep shadow) | L≈0.17 |
| `#cf4520` | VERMILION, pen stroke + kept marks | the only high-chroma ink |

Value spine: paper 0.90 → scraps 0.83/0.73/0.58 → horizon 0.40 → ink 0.17. The drift
lives in a deliberately narrow mid band (0.58–0.83) so it groups as ONE mass at
thumbnail instead of fragmenting into noise. The vermilion sits at L≈0.50 but wins on
chroma and on isolation, not on value. Grayscale check: the drift reads as a single
soft mass, the pen stroke reads as a dark diagonal, the three kept scraps read as
isolated lights against clean paper. Still legible.

### Composition map (`scatter_field` with a diagonal divider)
- Headline block `x ∈ [86, 900]`, two lines, top at `y=104`, leading ~1.06.
- Kicker line `ANCHORAGE DESK · OPERATOR · 24 JUL 2026`, mono, at `y=330`.
- Hairline rule under kicker, `x ∈ [86, 300]`, `y=356`.
- Faint North Slope horizon at `y=486`, very low amplitude (amp 14), atmospheric.
- The drift occupies `y ∈ [470, 1080]`, densest at lower-left, thinning up and right.
  ~520 scraps, sizes 7–34px, rotation free.
- **Red pen stroke** from `(150, 1010)` to `(905, 452)`, wobbled, width 10, with a
  short overshoot tail past the end point so it reads as a hand gesture.
- **Focal**: three kept scraps in the clean zone beyond the stroke, centered near
  `(880, 556)`, each ~50px, each carrying a small vermilion tick.
- Polaris `(998, 86)` r=13.
- `ALASKA.AI` wordmark bottom-left `(86, 1012)`, 30px.

Eye path: headline → red stroke (diagonal, brightest chroma) → three kept scraps at its
upper end → back down the drift → wordmark.

### Layer build order
paper ground → paper mottle → far horizon ridge (atmospheric) → drift shadow pass
(offset dark blobs, blurred) → drift scraps back-to-front in three depth bands, each
band lighter and cooler toward the back → seam/tear detail on nearer scraps → micro
pass (chips, stipple flecks) at the drift crest → red pen stroke → three focal scraps
with hard shadows → vermilion ticks → grain → type → brand marks.

### Technique stack
`mottle` (paper tooth), `ridge_pts`/`poly` (horizon), custom torn-quad generator built
on `wobble_pts` for every scrap edge (this is what makes them read as TORN rather than
cut), `poly` for scraps and their hard shadows, `chips` + `stipple` for the micro pass,
`hand_line` for the pen stroke, `grain` (6.0) as the single finishing texture identity,
`soft_panel` only if the headline needs rescuing.

### Three scales of detail
- MACRO: the drift mass, the pen stroke, the three kept scraps, the headline block.
- MESO: every scrap individually torn, shaded on one side, with a cast shadow; the
  drift banded into three depth zones with an atmospheric lightness ramp.
- MICRO: torn-edge wobble on each scrap, paper flecks and dust at the drift crest,
  stipple tooth in the paper ground, tiny ruled lines on the three focal scraps so
  they read as documents rather than confetti.

No flat fill exceeds 15% of canvas: the upper paper zone carries mottle plus grain and
is the deliberate negative space around the type.

### Risk list
1. **The drift reads as noise/mud at 300px.** Mitigation: narrow value band for all
   scraps, strong density gradient (dense lower-left, sparse upper-right), and a
   blurred unified shadow pass under the mass so it groups as one shape.
2. **Headline collides with the drift.** Mitigation: hard rule that no scrap spawns
   above `y=440`, leaving the top 40% as quiet paper. `soft_panel` held in reserve.
3. **The red stroke reads as a decorative slash, not a pen mark.** Mitigation: taper
   and overshoot the stroke, wobble it as a hand gesture, and repeat the same vermilion
   as small ticks on the three kept scraps so the causal relationship reads.
4. **Confetti risk — scraps read as celebration.** Mitigation: rectilinear torn quads
   (document-shaped, not triangular shards), ruled lines on the focal scraps, muted
   archive palette, no rotation beyond ±40°.
