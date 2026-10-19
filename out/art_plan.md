# Art plan — The Stack, 28 AUG 2026
## "The Complete Application"

Kicker: `THE STACK · FACILITIES · 28 AUG 2026`
Headline on art: **NO STATEMENT, / NO HEARING.**  (tightened by the artist from the writer's
"One letter from the utility gates every data center"; the phrase is lifted verbatim from the post body,
"No statement, no complete application, no hearing.")
Byline: `""` (not drawn for this column)

---

### 1. Concept statement

A municipal permit application seen close, every field satisfied and stamped, except one large open
box near the bottom marked for the electrical utility's statement of system capacity. Inside that
single empty box stand two utility poles with no span between them. The read in half a second is that
the whole apparatus is complete and it still cannot move, because the one field nobody at City Hall
can fill is blank.

Metaphor plus synecdoche. The mechanism is literally a piece of paper that must be handed over by a
party outside the process, so the artwork is that piece of paper, and the missing line is the story.
The unbuilt span inside the empty box says what the missing letter actually means, which is
interconnection.

### 2. Register

Wry, cool, procedural, faintly ironic. Not alarmed and not triumphant. The tone of a well-made form
with a hole in it. Anchorage built this gate before any applicant arrived, so the piece should feel
immaculate and idle at the same time. Warm paper and stamp-orange carry the bureaucratic warmth; the
empty void carries the irony. Nothing is on fire here, and that is the point.

### 3. Style family

`riso_form` — a deliberate `riso_zine` hybrid applied to a bureaucratic document plane: limited inks,
overprint with slight misregistration, halftone stamp blocks, heavy paper grain.

Dedup clearance (ledger read across all `claude/linkedin-*` branches, sorted by commit date):
- Last 8 style families were `hydrographic_claim`, `engraved_headworks`, `voronoi_impoundment`,
  `constructivist_scatter`, `organic_rd_moorage`, `wpa_layered_minimal_line`, `ukiyo_bokashi`,
  `geologic_engraving`. `riso_form` collides with none of them. Riso has not been used at all in the
  visible ledger.
- Hue cooldown (last 4): green, neutral-cool, violet, blue are all forbidden. **Orange** was last used
  31 JUL on the Desk column, six issues back, so it is clear.
- Composition cooldown (last 2): `offset_parcel_drift`, `frame_within`, `central_icon` forbidden.
  This piece is `form_field_grid`, used never.
- Motif check: the obvious metaphor for a chokepoint is a gate or a valve, and the ledger shows
  gate/valve motifs in four of the last ten issues (stop-log headworks, crest gates, series valves,
  gate iris). **Literal gates are therefore banned to me here.** A form field and an unbuilt span are
  the fresh route to the same idea.

### 4. Palette (OKLCH-built, 4 inks + paper)

| role | hex | approx L | use |
|---|---|---|---|
| paper | `#f0e6d2` | 0.92 | sheet, and the focal void |
| ink_dark | `#23190f` | 0.16 | headline, rules, poles, labels |
| ink_orange | `#e8501e` | 0.62 | stamp blocks, the accent, required-field tick |
| ink_gold | `#c8912f` | 0.68 | secondary ticks, punch rings, overprint |
| ink_mid | `#8a7355` | 0.55 | hairline rules, faint interior grid |

**Value structure.** The darkest dark is `ink_dark` in the poles and headline; the lightest light is
bare paper inside the empty box. The focal wins the contrast war by *inversion*: every other row on
the sheet is dense with dark type and saturated orange stamp mass, so the one region that is simply
clean paper becomes the brightest, quietest hole in a busy field. Grayscale squint test still reads,
because the separation is value-driven (0.92 void against 0.16/0.62 rows), not hue-driven.
Chroma discipline: orange is the only high-chroma ink and appears only in stamp blocks and one tick,
so it never competes with the void.

### 5. Composition map — `form_field_grid` (1080 grid)

Full-bleed document plane, axis aligned, sheet running off top and bottom so it reads as an extreme
close-up rather than a floating page.

- Kicker line: mono 15px, tracking 0.22em, left at **(96, 62)**.
- Polaris: **(984, 62)**, r = 13, gold. Balances the kicker across the top margin.
- Headline block: x ∈ [96, 984], two lines, Fraunces wght 900 / opsz 144, size ~118, leading 1.06.
  Line 1 "NO STATEMENT," baseline top at **y = 118**; line 2 "NO HEARING." top at **y = 243**.
  Block bottom ≈ **y = 368**.
- Zone rule: `hand_line` across **y = 400**, x from 96 to 984, dark, width 3, slight wobble.
- Punch perforations: five gold rings down the left margin at x = 52, y = 470, 590, 710, 830, 950.
- **Filled field rows** (thin bars, pitch 56), label left at x = 128, stamp block right x ∈ [700, 968]:
  - r0 **y = 448** ZONING DISTRICT I-1 / I-2 / I-3
  - r1 **y = 504** PEAK DEMAND 20 MW
  - r2 **y = 560** SETBACK 200 FT
  - r3 **y = 616** NOISE MITIGATION STUDY
  - r4 **y = 672** FIRE SUPPRESSION
- **THE FOCAL — empty field box**: x ∈ [96, 984], y ∈ **[716, 902]** (186 tall, ~3.3x a normal row).
  Deliberate rhythm break. Border dark width 4 with corner ticks; interior bare paper with a very
  faint `ink_mid` grid; label "ELECTRICAL UTILITY STATEMENT" mono 19px at (128, 740); a small orange
  "REQUIRED" tick at (952, 740) anchored right; an empty signature hairline at y = 878, x ∈ [128, 700].
  - Inside it, the unbuilt span: pole A at **x = 372**, pole B at **x = 708**, both footed at
    **y = 862**, crossarms at **y = 792**, pole tops **y = 776**. Conductor stubs run inward from each
    crossarm and stop, leaving a **~150px gap centred on x = 540** at y = 800. Two tiny insulator
    nubs per crossarm.
- **Filled field rows below** (so the void is bracketed, not bottom-orphaned):
  - r5 **y = 934** WATER UTILITY STATEMENT
  - r6 **y = 990** WASTEWATER UTILITY STATEMENT
- Wordmark `ALASKA.AI`: Fraunces Black 30px, bottom-left at **(96, 1042)**.

Eye path: headline (top-left mass) → down the stamped row rhythm → hard stop at the bright void →
the gap between the poles → out along the bottom rows → wordmark.

Nothing important sits within 48px of an edge except the punch rings at x = 52, which are deliberate
margin furniture, and the sheet bleed itself.

**Every label is dossier-grounded.** Zoning districts I-1/I-2/I-3, 20 MW peak demand, 200-foot
setback, noise mitigation study, fire detection and suppression, and the water / wastewater /
electrical utility statements are all provisions verified in `stack_anatomy.json`. No invented
docket numbers, dollar figures or agency names appear anywhere on the art.

### 6. Layer build order (back to front)

1. Paper base `#f0e6d2` + `mottle` (0.045) + faint raking `gradient_v` warm-to-cool across the sheet.
2. Punch perforation rings (gold, with dark inner shadow arc).
3. Filled row substrate: hairline `ink_mid` rules under every row.
4. Stamp blocks on the five upper + two lower rows: orange `poly` blocks, each screened with
   `halftone` and given `hatch` at 38° so no block is a flat fill; slight per-block rotation.
5. Row labels in mono `ink_dark`, small.
6. Focal box border (dark, `wobble_pts` for hand-drawn edge) + corner ticks + faint interior grid.
7. The two poles and the broken span, `ink_dark`, `hand_line` for the humanised edge; insulator nubs.
8. Zone rule at y = 400.
9. Headline (Fraunces 900) + kicker + wordmark + polaris.
10. Riso overprint pass: re-print the orange layer at ~2.2px misregistration, low opacity.
11. Micro finishing: `stipple` inside stamp blocks, `chips` paper-fibre dust across the sheet,
    tick marks along rules, `grain` (6.5), soft `vignette` (0.14).

### 7. Technique stack

`gradient_v` (raking light, ease 1.2) · `mottle` (0.045, scale 3.2) · `poly` + `wobble_pts` (stamp
blocks, focal border) · `halftone` (cell 7.5, max_r 0.55, clipped by region to each stamp block) ·
`hatch` (spacing 7, angle 38°, clipped to stamp masks) · `stipple` (density 0.10 inside blocks) ·
`hand_line` (zone rule, poles, box border, amp 1.4) · `circle` (punch rings, insulators) ·
`chips` (n≈260, size 2-5, paper dust) · `grain` (6.5) · `vignette` (0.14) · `polaris` · `fraunces` /
`mono` / `chip` for type. Seed constant `SEED = 828`.

### 8. Risk list

1. **Reads as a flyer, not as art.** A document full of type can collapse into a form. Mitigation:
   mono labels are kept small (17-19px) and function as *texture and rhythm* rather than as content
   to be read; only the headline is a real type moment; the poles supply a pictorial anchor so the
   piece has a drawn subject, not just typesetting.
2. **The empty box reads as an unfinished render.** A blank rectangle can look like a bug. Mitigation:
   heavy deliberate framing — width-4 wobbled border, corner ticks, faint interior grid, a labelled
   header, an orange REQUIRED tick, and an empty signature hairline. The poles inside confirm intent.
3. **Muddy midtones from riso overprint.** Orange over dark goes to sludge. Mitigation: the overprint
   pass touches only the orange stamp layer and never crosses the headline or the poles; orange and
   dark are held ~0.46 apart in lightness.
4. **Headline colliding with the row rhythm.** Mitigation: the y = 400 zone rule is a hard divider and
   the headline zone above it is reserved negative space carrying paper texture only.
