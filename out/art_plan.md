# Anchorage Desk — Art Plan — 2026-07-31

## Step 0 — Absorb the story

- **What happened.** On 11 June 2026 Billy Wailand committed GCI to Starlink bonded
  gateways as the outage backup for the fiber and microwave serving Bethel, Sitka,
  Kotzebue and Dillingham, choosing to buy orbital redundancy rather than build more
  GCI-owned iron.
- **Why it matters to Alaska.** Four hub communities now route their outage recovery,
  and the health, education and public-safety traffic riding it, through one external
  vendor on commercial terms nobody outside the two companies can see.
- **Register.** Measured and quietly precarious. Not alarmed, not triumphant. The call
  is defensible; the picture should carry the dependency without shouting about it.

## Step 1 — Dedup scan (performed, see scratch/art_dedup.md)

Scanned 20 prior `claude/linkedin-*` branches with meta ledgers.

- **Forbidden style_family (last 8):** ukiyo_bokashi, geologic_engraving,
  bathymetric_blueprint, flow_field, swiss_grid, cadastral_ledger, iso_cutaway.
  Plus aurora_field permanently.
- **Forbidden hue_family (last 4):** magenta, green, indigo, gold.
- **Forbidden composition (last 2):** diagonal_thrust, bilateral_gate.
- **Forbidden motifs (last 10):** converging funnel throat, capital current, single desk
  gate, gate iris, exploded fuel stack, subsea fiber section, submerged sluice gate,
  bathymetric contours, cadastral plat, consent seal, modular offer grid,
  transmission-tower glyph, geologic strata, ore body, series valves, and the rest of
  the ledger list.

This piece clears all four cooldowns. Style is a **wpa_layered / minimal_line hybrid**
(neither used recently), hue family is **orange** (not in the last four), composition is
**horizon_band** (not in the last two), and the primary motif, a fan of taut threads from
four settlements to one satellite, appears nowhere in the ledger. The nearest ledger
neighbour is "converging funnel throat" (10 Jul); this is deliberately NOT a funnel. There
is no throat, no narrowing channel, no fan of losers. Four equal peers each hold one line
to one node, which is a different geometry and a different argument.

## Step 2 — Concept (three generated, one chosen)

**A. Two lifelines to a hub.** One village, a heavy ground line running off-frame and a
thin line rising to a point of light. Reads the build-or-buy binary cleanly but only
carries one community, so it loses the concentration argument entirely. Rejected.

**B. Four fires, one sky-anchor. CHOSEN.** Four small lit settlements spaced along a low
winter horizon. From each, a single fine taut thread rises into the sky, and all four
threads terminate on ONE satellite node in the upper right. Along the ground between
them runs the terrestrial path, drawn as a heavier stitched line that is visibly BROKEN
in three places. The reader gets it in half a second. The ground is cut; everything now
hangs from one point. It is the post's actual thesis rendered as geometry rather than
illustrated as a scene.

**C. The unbuilt tower.** A half-built relay tower in blueprint ghost beside a solid
orbital node, the iron not built against the orbit bought. True to the binary but static,
and it argues about GCI's capex rather than about the four communities. Rejected.

**Chosen: B.** Metaphor is scale contrast plus synecdoche. Four tiny lit places against a
vast cold sky, and the one small object everything depends on.

## Step 3 — Blueprint

### 1. Concept statement
Four hub communities each hold a single thread to one satellite while the ground link
between them lies broken. The picture argues that redundancy bought from one vendor is
still a single point.

### 2. Register
Measured, cold, quietly precarious. Deep blue-black land and upper sky carry the weight;
a narrow band of low-angle orange winter light at the horizon keeps it Alaskan and warm
enough to avoid reading as doom. The satellite is the brightest thing in the frame,
which is exactly the uncomfortable point.

### 3. Style family
**wpa_layered** base (flat stacked landscape bands, big type, restrained ink count)
hybridised with **minimal_line** thread work (fine hand-drawn lines, generous negative
sky). Fits because the story is a landscape-scale infrastructure decision, and the
layered-band grammar gives a value spine that reads at thumbnail. Clears all dedup
cooldowns as noted above.

### 4. Palette (OKLCH-built, 5 inks + paper)

| hex | role | approx L |
|---|---|---|
| `#f6e6d2` | paper / type light, horizon high-light | 0.93 |
| `#e07a3c` | horizon glow, dominant hue (orange) | 0.68 |
| `#a8492c` | mid sky warm shadow, thread ink | 0.48 |
| `#3a2c3a` | far land band, upper sky mid | 0.30 |
| `#171320` | near land, ink, silhouettes | 0.16 |
| `#ffeede` | focal accent, satellite body + settlement lights | 0.96 |

**Value spine.** Darkest dark is the near land at L 0.16, occupying the bottom third.
Lightest light is the satellite accent at L 0.96, a small object in the upper right. The
horizon band at L 0.68-0.93 is a thin bright seam, so the focal still wins because it
sits against the DARKEST part of the sky (L 0.30 at that altitude) rather than against
the bright seam. Value gap at the focal is roughly 0.66, the largest in the piece.
Grayscale check: four bright pinpricks on a dark ridge, one bright node above, one bright
seam across the middle. Still reads.

### 5. Composition map — `horizon_band`

- Canvas 1080x1080. Horizon seam at **y = 726**.
- Upper sky gradient box `(0, 0, 1080, 726)`, `#241d2c` at top to `#e07a3c` at horizon,
  ease 1.7 so the warm seam stays narrow.
- Far land band: `ridge_fill` y_base **714**, amp 26, fill `#3a2c3a`.
- Mid land band: `ridge_fill` y_base **762**, amp 34, fill `#241d28`.
- Near land band: `ridge_fill` y_base **846**, amp 44, fill `#171320`, down to 1080.
- **Four settlements** on the far ridge at x = **150, 372, 606, 918**, y ≈ **706**.
  Each is a cluster of 5-9 lit windows, 3-7px, plus a `glow` r 34 at alpha 52.
  Spacing is deliberately uneven so it reads as geography, not as a chart.
- **Satellite node** centre **(806, 322)**. Body 46x28 rounded, two wings 48x13 either
  side, total span ~152px. `glow` r 96 alpha 66 behind it. Highest contrast in frame.
- **Four threads**: `hand_line` from each settlement top to the node, width 2.0,
  amp 1.1, colour `#a8492c` lifting to `#e07a3c` near the node.
- **Broken ground stitch** along y ≈ 742 through all four settlements in `#4a3a44`,
  drawn as dashes with three deliberate GAPS at x∈[248,318], x∈[470,540], x∈[712,782].
  Three tiny relay towers at x = 262, 508, 760 sitting just above it.
- **Headline block** x∈[96, 660], line 1 baseline top **y = 118**, line 2 top **y = 200**.
  Fraunces 900, opsz 144, size fitted to 564px max width, leading ~1.06.
- **Kicker** mono, x = 96, y = 300, tracked 0.22em, colour `#e0b9a0`.
- **Wordmark** ALASKA.AI, Fraunces 900, size 30, bottom-left **(96, 986)**.
- **Polaris** small r 11 at **(984, 988)**, bottom-right, far from the satellite so the
  colophon never competes with the focal.

**Eye path.** Headline (top left) → satellite node (upper right, brightest) → down the
thread fan → four settlement lights along the horizon → broken ground stitch → wordmark.

**Negative space.** The sky between the headline block and the node, roughly
x∈[660,1080] y∈[0,240] and x∈[96,660] y∈[330,600], stays open. Threads cross it thinly.

### 6. Layer build order
paper → sky gradient → sky field banding (subtle cloud strata) → sparse star stipple →
satellite glow → far land band → mid land band → near land band → land hatch + chips
texture → broken ground stitch + relay towers → settlement glows → settlement windows →
thread fan → satellite body and wings → headline type → kicker → wordmark → polaris →
mottle → grain → vignette.

### 7. Technique stack
`gradient_v` (sky, ease 1.7), `field` + `field_mask` (cloud strata bands in the mid sky),
`stipple` (sparse stars, upper sky only, density 0.05), `ridge_pts`/`ridge_fill` (three
land bands), `hatch` (near-land texture, spacing 14, angle 62, very low contrast),
`chips` (snow/scree micro on the near band, n 260, size 2-6), `hand_line` (thread fan,
amp 1.1), `glow` (satellite halo, settlement lamps), `circle`/`poly` (satellite body,
wings, windows, towers), `polaris`, `mottle` (0.05), `grain` (6.0), `vignette` (0.16).
ONE texture identity: mottle + grain. No halftone, no riso.

### 8. Risk list

1. **The satellite reads as a generic star or a UFO blob.** Mitigation: give it a
   rectangular body with two flat wings and a visible stand-off gap, so the silhouette is
   unmistakably built hardware, not celestial. Fill-black test the silhouette. Keep
   Polaris tiny and far away in the opposite corner.
2. **The thread fan reads as a converging funnel and collides with the 10 Jul ledger
   entry.** Mitigation: four discrete lines with visible air between them, no envelope,
   no narrowing channel walls, no mass of losers. The lines arrive at the node from four
   clearly different angles including one from the right, which a funnel never does.
3. **Mud in the mid-sky.** The orange seam meeting the violet-dark upper sky can turn
   muddy brown across the middle third. Mitigation: ease 1.7 on the gradient keeps the
   transition compressed near the horizon, and the cloud strata are drawn in a slightly
   desaturated version of the sky colour rather than a third hue.
4. **Headline collides with a thread.** The thread from the leftmost settlement (x 150)
   rises steeply right toward (806, 322) and could cut the headline block. Mitigation:
   headline bottom is y 268, and that thread passes below y 500 until x > 400. Verified in
   the coordinate plan; re-check on render.
