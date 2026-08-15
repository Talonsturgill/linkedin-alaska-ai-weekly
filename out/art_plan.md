# Art plan — Anchorage Desk — 14 AUG 2026

**Headline:** Anchorage Code Can’t Answer / What The Cameras Collect
**Kicker:** ANCHORAGE DESK · MUNICIPAL · 14 AUG 2026
**Output:** out/post_image.png (1080×1080) · SEED 818

---

## Step 0 — the story in three lines

- **What happened.** On 4 Aug 2026 Assembly member Keith McCormick led the objection
  that stopped APD's ~$600,000 three-year Thundercat contract to upgrade the Real-Time
  Crime Center; the Assembly postponed the binding vote to 18 Aug.
- **Why it matters to Alaska.** The contract buys the camera/ALPR/drone/analytics
  infrastructure surveillance AI actually runs on (up to 750 feeds), and Anchorage has
  no binding municipal code on what is collected, who may see it, or how long it is
  kept — it barred facial recognition in 2023 and never wrote the rest.
- **Register.** Tense, watchful restraint. A hold placed on something already
  half-built. Not alarmist, not triumphant. The desk's verdict: withholding was right.

## Step 1 — dedup scan (attempted; parent's table is authoritative)

`git fetch` + ledger read across `origin/claude/linkedin-*` was run. The 16 reachable
branches are older legacy-template issues whose sidecars carry no `style_family` /
`hue_family` / `composition` keys, so they contribute nothing. The parent agent's scan
of the newer column branches supplies the binding list, reproduced and obeyed:

FORBIDDEN style_family — voronoi_impoundment, organic_rd_moorage, constructivist_scatter,
ukiyo_bokashi, wpa_layered_minimal_line, geologic_engraving, paper_collage,
bathymetric_blueprint; flow_field cooling; aurora_field permanent.
FORBIDDEN hue_family — violet, teal, blue, magenta.
FORBIDDEN composition — central_icon, thirds_focal, scatter_field.
FORBIDDEN motifs (2026-08-07 desk, same contract) — surveillance camera crowd, blank
ruled ordinance page, single red record light, street grid substrate.

---

## Step 2 — three concepts

**A. The suspended stop-log gate. (CHOSEN)**
A water-control headworks stands across a braided glacial inflow. Its four bays are the
municipality's rulemaking: three slots stand *empty* under engraved deck plates reading
COLLECTION / ACCESS / RETENTION, and only one bay has a beam actually dropped in —
weathered, stamped `2023`, the facial-recognition ban. The flow pours straight through
the three open bays. Above the deck, a gantry has craned in the upgrade: a bright amber
equipment module tagged `$600,000`, hanging on its sling, **not lowered**, a hold tag
reading `HELD · AUG 18` swinging beneath it. Read in half a second: a heavy thing stopped
in mid-air over a gate that is mostly open.
*Why it's true:* "retention" is literally a water word; the structure is the code, the
beams are rules, the load is the money. The half-built asymmetry (one rule written, three
not; the money bought but not released) is exactly McCormick's binary. Alaska without
cliché: braided glacial channel and the Chugach behind the Anchorage bowl — and Eagle
River, McCormick's district, is itself a braided glacial river.
*Clears the motif ban:* no camera, no page, no record light, no street grid.

**B. The termination frame / patchbay** (the direction offered by the editor).
Hundreds of ports in a dense modular field are where the 750 feeds land; every label
strip beneath them is blank; a hold lever sits locked in the withheld position.
*Rejected because:* the blank label strips are conceptually one step from the 2026-08-07
piece's *blank ruled ordinance page* — same "the form was never filled in" gag in
different hardware — and a wall of identical ports repeats that piece's *crowd of
identical objects* rhythm. It is also the least Alaskan of the three; a patchbay is a
patchbay in Anchorage or Atlanta.

**C. The empty conduit in the ductbank.**
A trench cross-section under Anchorage: the ductbank is poured, every conduit pulled with
cable except one, labelled for code, which holds only a limp pull-string.
*Rejected because:* it is a good idea one size too quiet. A cross-section of buried pipe
has no focal drama and no vertical event; at 300px it reads as an abstract of circles.
It also leans on the iso-cutaway grammar used on 2026-07-07.

**Chosen: A.** It carries the story's exact asymmetry, it has one unmistakable focal
(the hanging amber load), it is unmistakably Alaskan, and it sits nowhere near the
forbidden motifs.

## Step 3 — register

Tense, watchful restraint. Carried by: a cold, low-chroma slate/silt palette (the
watchfulness) broken by exactly one warm high-chroma object (the withheld money);
by frontal, orthographic, unmoving architecture — nothing in the frame is *doing*
anything, everything is *waiting*; by engraved line work, which reads institutional and
deliberate rather than agitated. The only motion cue in the piece is water pouring
through gaps that should be closed.

## Step 4 — style family

**`engraved_headworks`** — an engraving-grammar hybrid: hatch + stipple tonal shading and
fine hand-drawn line work applied to an industrial elevation drawing, with posterized
print-flat water planes and sparse mono dimension labels.

*Why it fits:* engraving is the language of institutions and permanence — exactly the
register for "we have policy, we do not have code." The dimension ticks and stamped plates
make the piece read as a *record of a structure*, which is what a municipal code is.

*Clears cooldowns:* `engraving` is on the available list. Deliberately differentiated from
2026-07-24's `geologic_engraving`, which was a green subsurface strata cross-section in a
bilateral_gate composition; this is a cool frontal architectural elevation over water in
frame_within, with a posterized-plane water treatment that piece did not use.

## Step 5 — palette (OKLCH, value spine first)

| role | OKLCH | hex (approx) | note |
|---|---|---|---|
| paper / high sky | `oklch(0.945, 0.012, 238)` | pale cold white | lightest light |
| haze / low sky | `oklch(0.862, 0.022, 232)` | cold grey-blue | |
| ridge far | `oklch(0.780, 0.020, 236)` | atmospheric | |
| concrete | `oklch(0.735, 0.012, 246)` | structure | |
| water mid | `oklch(0.620, 0.032, 228)` | silt field | |
| water deep | `oklch(0.430, 0.034, 232)` | channel shadow | |
| ink | `oklch(0.190, 0.028, 236)` | darkest dark, all line work | |
| **amber (focal)** | `oklch(0.765, 0.155, 72)` | the withheld load | highest chroma in the piece |
| amber deep | `oklch(0.545, 0.140, 58)` | crate shadow side / tag | |
| amber high | `oklch(0.900, 0.095, 84)` | crate top cap / polaris core | |

**Value structure.** Lightest light is the sky above the headline (0.945); darkest dark is
the ink of the pier faces and under-deck shadow (0.190) — they sit at opposite ends of the
canvas, so the composition has a full value swing top-to-bottom. The focal wins because it
is the ONLY chromatic object in a 0.03-chroma world *and* because it is set against a
locally darkened water plane with an ink outline and ink strap bands: highest local value
contrast and highest chroma in the same 214×116px region. Grayscale check: amber 0.765 on
water-mid 0.620 with ink 0.190 straps inside it — still the busiest, brightest patch in a
squint. `hue_family: neutral-cool` (the dominant field is cold low-chroma slate; the amber
is a single accent, not the field).

## Step 6 — composition map (`frame_within`)

The headworks is the frame; its four bays are the apertures.

```
y=  0        top margin
y= 58   kicker  ANCHORAGE DESK · MUNICIPAL · 14 AUG 2026   x=80, mono 17, track .22
y= 64   polaris (996, 64) r=13 amber            <- balances kicker across the masthead
y= 86   hairline rule x∈[80,1000]
y=110   HEADLINE line 1  x=80, Fraunces 900/opsz144, fit to max_w 920 (≈58-62px)
y=110+1.06S  HEADLINE line 2 (same size, left rag)
y≈228   far ridge PEAKS bite the baseline of line 2 (no descenders there -> zero
        legibility cost, full "type behind the mountains" integration)
y=302   far ridge base (amp 74, jagged, scale 2.6/oct 5, tone 0.780)
y=336   near ridge base (amp 44, tone 0.700), bottom 352
y=330-600  BRAIDED INFLOW BAND, converging 16% toward center as it descends
y=364   dimension bracket x∈[72,404] + label `750 FEEDS` at (238, 380) anchor ma
y=380-400  gantry headbeam  x∈[512,808]
y=374-396  trolley at x=660
y=392-600  gantry legs at x=540 and x=780 (26 wide), X-brace between
y=432-548  **FOCAL: amber load** x∈[553,767] (214×116), sling to (578,432)/(742,432),
           chip `$600,000` at (660,502) anchor mm
y=566-596  hold tag `HELD · AUG 18` on a wire from the load's lower-left, x∈[540,690]
y=548-600  the AIR GAP — the whole point; dashed plumb line 660,548 -> 660,600 + target
y=600-664  DECK slab; bolt rows y=616 / y=650; recessed plate band y=624-646
           plates centered on bay centers x = 180 / 420 / 660 / 900:
           COLLECTION | FACIAL REC. | ACCESS | RETENTION
           (bay-2 plate is INK-FILLED with knocked-out type — the one rule executed;
            the other three are engraved outlines only)
y=664-946  PIERS at x-centers 60/300/540/780/1020 (54 wide) and four BAYS:
           [87,273] [327,513] [567,753] [807,993]  — each 186 wide, 282 tall
           slot grooves: dark vertical bars 5 wide at bay edge +4 and +12, both faces
           bays 1,3,4: OPEN — flow curtains pour full height
           bay 2: beam x∈[313,527] y∈[876,912], stamped `2023`
y=946-1080 tailwater apron: standing waves, foam chips, stipple
y=1012  wordmark chip `ALASKA.AI` at (86,1012) anchor ls, Fraunces 28/900, ink chip
```

**Eye path:** headline (top-left) → ridge shoulder sweeps down-right → the amber load
(focal, unmissable) → plumb line drops → deck plates read left-to-right →
the three empty bays and the one closed one → tailwater → wordmark, bottom-left.

**Balance:** headline mass top-left is counterweighted by the focal mid-right; the
wordmark bottom-left closes the diagonal. Negative space: the sky above the ridge (with
texture, not flat) and the deliberate 52px air gap under the load.

## Step 7 — layer build order (back to front)

1. paper base + `gradient_v` sky 0→352 (paper→haze), sky stipple gradient, survey ticks
2. kicker + hairline + **headline** (drawn early so terrain can overlap it)
3. far ridge (`ridge_pts` amp 74) over the headline baseline, snowfield patches, hatch
4. near ridge, darker, own hatch pass
5. braid band base plane
6. braid channels: vertically-stretched `field` → `warp` → convergence remap → posterize
   to 4 print-flat tones, masked to the band (MESO)
7. `streamlines` threads over the band, alpha-clipped to the band mask (MICRO — this is
   what makes the water read as *feeds*)
8. gravel-bar `stipple` + `chips` on the high-field bars
9. dimension bracket + `750 FEEDS`
10. bay interiors (dark), flow curtains in bays 1/3/4, checked flow in bay 2
11. the `2023` beam + stamp + hatch
12. piers: concrete, hatch shading, chamfers, waterline stain, slot grooves, bolts
13. tailwater apron: waves, foam chips, stipple
14. deck slab: cap, body, under-shadow, bolt rows, recessed plate band
15. deck plates + four labels; rails on the outer thirds only (center left clear)
16. gantry legs, X-brace, headbeam, trolley, hook block (BEHIND the load)
17. dark under-shadow `glow` + warm halo `glow` on the water behind the load
18. the load: body, top cap, straps, corner castings, outline, sling cables
19. `$600,000` chip, hold tag + wire, dashed plumb + target mark
20. `grain` (5.5) — single finishing texture identity alongside the hatch/stipple engraving
21. wordmark chip + polaris

## Step 8 — technique stack

`gradient_v` (sky) · `field` + vertical `zoom` stretch + `warp` + numpy convergence remap
+ posterize (braid channels) · `angle_field`-style hand-built angle array + `streamlines`
(feed threads, n≈420, step 3, len 120-300) · `hatch` (spacing 9-17, ridges/piers/beam) ·
`stipple` (sky gradient, gravel bars, tailwater) · `chips` (foam, brash) · `ridge_pts` /
`ridge_fill` · `glow` (load shadow + halo) · `hand_line`/`wobble_pts` (chains, tag wire,
stain edges) · `chip` (money, wordmark) · `grain` 5.5 · `polaris`.

## Step 9 — risk list

1. **The load reads as a generic yellow box.** Mitigation: internal structure — ink strap
   bands, corner castings, a lighter top cap, a chip-mounted `$600,000` plate, a sling
   whose two cables converge on a hook block, and a tag hanging on a wire. Silhouette test:
   filled black it must read as *slung freight*, not a rectangle. If it still reads flat,
   add a chamfered 3/4 top face and a cast shadow on the deck.
2. **Diagram clutter — eight mono labels is a lot.** Mitigation: strict tonal hierarchy —
   only the two crate labels get full contrast; the deck plates and `750 FEEDS` sit at
   ~55-65% contrast so they are legible at arm's length and recede at thumbnail. If the
   eval says cluttered, `750 FEEDS` is the first thing cut.
3. **The sky is 30% of the canvas and could go flat.** Mitigation: it is never a flat fill
   — vertical gradient + density-graded stipple + faint survey ticks + grain, and the
   jagged far ridge eats its bottom third. The only truly quiet acreage is the immediate
   halo around the headline, which is the sanctioned exception.
4. **Mud in the midtones** — concrete 0.735, ridge-far 0.780 and water-mid 0.620 are close.
   Mitigation: every structural edge carries an ink line at width ≥2.5, and the under-deck
   band is pushed to near-ink so the deck's silhouette separates from the water absolutely.

---

## As-built — deviations from the plan (recorded after the eval loop)

Six eval iterations ran; final weighted 8.58, no dimension below 8. Four planned
decisions were overturned by what the renders actually showed:

1. **The "type behind the mountains" overlap was abandoned** (iteration 2). At the
   headline size fit_size actually returned, the far ridge peaks cut line 2 in half
   rather than kissing its baseline. The ridge was dropped to base 312 / amp 68 and the
   headline capped at 74px, giving a clean 16px gap. Legibility beat the effect. This is
   the piece's weakest dimension in the final eval (typography 8): the headline sits on
   the sky rather than interlocking with the terrain.
2. **The posterized braid was cut back to a narrow inflow strip** (iteration 3). Painting
   the whole pool from a stretched noise field produced camouflage blobs — the planned
   vertical stretch cancelled itself out arithmetically (`field()` uses one frequency for
   both axes, so the zoom exactly undid the anisotropy). Fixed by slicing 108 rows off an
   isotropic field and stretching those 10x, then confining the result to y 357-452 over
   a graded slack pool. The pool below is a gradient + a 78-line ripple system, which
   also opened the negative space the focal needed.
3. **The spreader bar was tried and rejected** (iterations 5-6). Added to kill a
   suitcase read, it created a worse one — a bar spanning the load with vertical legs
   reads as a canopy. Replaced with a wide angled sling to two shackles, plus an
   asymmetric equipment face (stencil plate left of a divider, louvred bay right), which
   reads as slung freight mid-lift.
4. **The dashed plumb line and target mark were cut** (iteration 4) — they collided with
   the hold tag, and risk #2 in the plan (diagram clutter) said to cut before crowding.
   Suspension already reads from the sling, the air gap and the cast shadow.

Also cut: the planned draw-down current lines fanning across the pool read as scratches
and were shortened to short dips at the sill only. The flow curtains and tailwater were
pulled down out of the highlight range in iteration 5 after a grayscale check showed the
white water out-punching the amber focal.
