# Art plan — Anchorage Desk, 24 SEP 2026 (Ben Shier / UA draft AI policy)

Story: UA's CITO put a draft system-wide AI policy before the regents; if adopted in November, UAA, UAF and UAS must each write an AI plan. Register: measured, constructive, slightly cautionary ("use is already ahead of policy", guardrails before scale).

## 1. Concept statement
Three wooden trail-marker tripods are being staked across a winter snowfield, but a deep, busy trail of footprints already runs past them toward the mountains. The policy is the marker line; the use is the trail that got there first.

Concepts considered: (a) three blank ruled plan pages pinned to a campus board (generic, killed); (b) a surveyor's level sighting across three campus lights (too close to recent siting/land pieces); (c) trail markers behind the tracks (chosen: Alaskan, specific, reads in half a second).

## 2. Register
Calm winter light, cool indigo ink on warm paper, one fireweed-red flagging-tape accent on the markers. Not alarm; order arriving slightly late.

## 3. Style family
`engraving_trail` (engraving family: hatch + stipple, one dominant ink on paper). Clears cooldown: not in last 8 (machined_plate, pixel_dither_aerial, woven_fabric, wpa_scaffold, exploded_iso_docket, halftone_section, riso_form, landmark_mesh).

## 4. Palette (OKLCH-built)
- paper  #efe8d8 (L≈.93) lightest light, the snow
- ink    #1f2a4d (L≈.28) indigo, darkest dark: poles, headline, hatch
- shade  #6f7fa6 (L≈.60) long blue shadow / trough hatch
- mist   #b9c2d6 (L≈.80) far ridge hatch, sky lines
- accent #d0452f (L≈.58, high chroma) flagging tape — focal
- star   #e0a526 polaris only
hue_family: blue. Value spine: markers (ink) against snow (paper) is the max contrast; tape accent wins chroma.

## 5. Composition map (diagonal_thrust)
- Headline block top-left x∈[72,760], baselines y≈150, 240; Fraunces 900 opsz144 ~78px.
- Kicker mono 17px tracked .2em at (74, 288).
- Polaris (990, 92) r=15.
- Horizon/ridge band y≈400–520; far ridge mist hatch, near ridge ink hatch with snow patches.
- Snowfield y 500–1080.
- Trail: cubic from (120,1080) → (430,860) → (640,690) → (860,540); footprints scale 1.0→0.18 with distance, three interleaved tracks.
- Markers left of trail: M1 foot (250,960) h=230; M2 foot (455,800) h=150; M3 foot (600,700) h=100. Red tape on each. Long shadows to lower-right.
- Tracks continue beyond M3 up to the ridge at ~(860,540): the "ahead of policy" read.
- Wordmark ALASKA.AI bottom-right anchor (1008, 1016).
Eye path: headline → M1 red tape → marker line → tracks running past → ridge → star.

## 6. Layer order
paper → sky engraved lines (gradient mask) → far ridge (mist hatch) → near ridge (ink hatch masked by rock-noise; snow faces left paper) → snowfield drift contours + stipple in hollows → trail trough (shade) → footprints → marker shadows (shade hatch) → markers (poles, lashing, tape) → snow chips micro → grain → type → marks.

## 7. Technique stack
hatch (sky 0°, ridges 45°/−35°, shadows −12°), stipple (drift hollows, density .10), field + field_mask (rock patches), ridge_pts, hand_line (poles, contours), chips, grain 5.

## 8. Risks
- Footprints read as dots/noise → make them paired, elongated, oriented along path, with trough underlay.
- Headline colliding with sky hatch → sky hatch only below y=320.
- Markers read as tepees → thin poles, lashing wrap, tape flutter, small scale vs. trail.
