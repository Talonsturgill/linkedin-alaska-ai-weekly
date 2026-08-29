# Anchorage Desk cover art — 2026-08-28

## Step 0 — the story
**What happened.** Sydney Scout co-sponsored AO 2026-108, which would bar APD
from adding AI human-feature recognition to the Real-Time Crime Center without
Assembly approval.
**Why it matters to Alaska.** It decides who authorizes algorithmic recognition
on a municipal camera network, before the capability is deployed rather than
after.
**Register.** Watchful, restrained, institutional. Not alarmist, not
triumphant. The feeling of a line drawn deliberately, in advance.

## Step 1 — dedup (scan of all linkedin-* branches)
Forbidden style (last 8): riso_form, hydrographic_claim, engraved_headworks,
voronoi_impoundment, constructivist_scatter, organic_rd_moorage,
wpa_layered_minimal_line, ukiyo_bokashi.
Forbidden hue (last 4): orange, green, neutral-cool, violet.
Forbidden composition (last 2): form_field_grid, offset_parcel_drift.
Forbidden motifs (last 10) include: surveillance camera crowd, ordinance page,
stop-log gate headworks, crest gates, torn paper drift, ore body + valves,
subsea fiber section, permit form, claim quadrilateral, moored land raft.
**Chosen: `landmark_mesh` (new hybrid of blueprint + minimal_line), hue
`indigo`, composition `thirds_focal`.** All clear. Note the previous Anchorage
Desk RTCC pieces used a camera crowd (7 AUG) and a headworks gate (14 AUG), so
this piece deliberately avoids both cameras and gates.

## Step 2 — concept (three considered)
1. *A control gate on a dry channel.* Killed. Gate motifs used 14 AUG and
   24 JUL, and it repeats the desk's own recent visual language.
2. *A wall of camera feeds, most dark.* Killed. "Surveillance camera crowd"
   was the 7 AUG Anchorage Desk motif, and it drifts back to the procurement
   story this post is explicitly not about.
3. **CHOSEN — the half-built face mesh.** Facial-landmark geometry is what
   human-feature recognition actually emits, so it depicts the regulated
   capability itself rather than a stock privacy symbol. Landmark points and
   their connecting edges build a face from the left. At a bright gold
   threshold rule the edges stop. The remaining landmarks, including an entire
   unmeshed eye, sit as loose unconnected points. The capability exists; the
   connections are not authorized. Half-second read: a face assembling out of
   points, cut clean by a line.

## Step 3 — blueprint

**Concept statement.** A facial-landmark mesh builds itself from the left and
halts at a gold rule labeled AO 2026-108. The points beyond the rule are
present but unjoined, so recognition is visibly withheld rather than absent.

**Register carried by form.** Deep indigo night ground for institutional
surveillance. Cool pale blue for the machine's own linework, which keeps it
clinical, not menacing. One warm gold rule as the single human decision in the
frame, and the only warm element on the canvas.

**Style family.** `landmark_mesh` — blueprint linework (thin pale ink on dark
paper, dimension ticks, mono labels) crossed with minimal_line restraint.
Clears the last-8 cooldown.

**Palette (value spine, dark to light).**
- `#0b0f24` ground, deepest dark (L≈0.13)
- `#141a3a` field mottle, near-ground
- `#222d5e` orphan-point ink, low value (L≈0.25)
- `#4a5f9e` mesh edge mid (L≈0.45)
- `#b9c6e8` landmark point light (L≈0.80)
- `#eef1f7` type near-white (L≈0.95)
- `#ffc72c` Alaska flag gold, focal accent, highest chroma, used ONCE
Focal wins on both chroma and value gap: gold against indigo at maximum
separation. Grayscale check still reads because the rule is the lightest
vertical element and the mesh density falls off to its right.

**Composition map (1080 grid), pattern `thirds_focal`.**
- Headline block x∈[86, 900], baseline top y=104, auto-fit to 814px width.
- Kicker line `ANCHORAGE DESK · MUNICIPAL · 28 AUG 2026`, mono 17px tracked,
  y=252.
- Hairline rule under kicker, x∈[86, 300], y=276.
- Face box x∈[250, 840], y∈[300, 900]. Landmark set of ~72 points.
- **Threshold rule x=620**, y∈[248, 942], 3px gold. Sits just right of the
  vertical third, which is where the eye lands after the headline.
- Label `AO 2026-108` in mono 15px, gold, on a knockout chip at (632, 262).
- Label `SEPT 1 HEARING` mono 13px, dim, at (632, 922).
- Wordmark `ALASKA.AI` Fraunces Black 30px, bottom-left (86, 984).
- Polaris r=12 at (988, 118).
- Eye path: headline → gold rule → dense mesh at the left eye → orphan points
  trailing right → wordmark.

**Layer build order.** ground fill → vertical gradient → mottle → faint
canvas-wide micro dot field → orphan landmark points (right of cut) →
dashed pending stubs → mesh edges (Delaunay, length-filtered, left of cut) →
feature loops (jaw, brows, eyes, nose, mouth) brighter → landmark points →
gold threshold rule + tick marks → labels → headline + kicker + hairline →
wordmark + polaris → grain → vignette.

**Technique stack.** hand-authored landmark topology, `scipy.spatial.Delaunay`
with an edge-length filter, `line`/`circle` primitives, `field`+`mottle` for
ground life, `chip` for label legibility, `grain`, `vignette`, `fit_size` for
headline fitting.

**Risk list.**
1. *The mesh reads as random scatter, not a face.* Mitigation: hand-authored
   dlib-style landmark topology with explicit feature loops drawn brighter than
   the Delaunay fill, so jaw/eyes/mouth carry the read even before the mesh
   registers.
2. *The dark ground goes flat and dead across large areas.* Mitigation:
   vertical gradient plus mottle plus a canvas-wide micro dot field at very low
   value, plus grain, so no region is a single flat fill.
3. *Headline collides with the mesh or the rule.* Mitigation: face box starts
   at y=300, headline block ends by y=240, and the rule starts at y=248. A
   clean 60px quiet band separates type from art.
4. *Gold rule reads as decoration rather than a cut.* Mitigation: edges are
   hard-clipped at the rule and orphan points are visibly dimmer, so the rule
   is doing visible work.
