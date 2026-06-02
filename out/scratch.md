# Received Wisdom run scratch — 2026-05-29

## Resolved config
- BRANCH: claude/linkedin-contrarian-2026-05-29 (FREE)
- ISSUE_LABEL: NO. 03 (prior date stems: 2026-05-20, 2026-05-26 = 2 distinct; +1 = 3)
- Anchorage date: 2026-05-29 ; image date stamp: 29 MAY 2026
- contrarian_kicker (state.yaml authoritative): "COLD TAKE"
- contrarian_motto (state.yaml authoritative): "the claim, and the part it leaves out"
- byline: BY TALON
- Gmail label / footer-label: "Received Wisdom"
- Gmail subject: Alaska.Ai — Received Wisdom Draft — 2026-05-29
- DEVIATION NOTE for editor: prompt parenthetical said kicker "RECEIVED WISDOM" but state.yaml authoritative value is "COLD TAKE"; used the file value for the image. Email branding label stays "Received Wisdom" per Phase 9 literal flags.

## Claims already corrected (last 6 issues) — DO NOT RE-SELECT
1. NO. 02 (2026-05-26): Gov. Mike Dunleavy — "we are 30 degrees cooler than Texas ... could save a one-gigawatt plant upwards of $150 million a year" (cold-climate cooling savings). Corrected: cooling is ~5% of data-center O&M (UAF ACEP); AK power is among the highest in US.
2. NO. 02 (2026-05-20-02): Gov. Mike Dunleavy — "you might be looking at four or five cents a kilowatt hour for decades and decades to come" (cheap AK power for data centers). Corrected: Chugach has no gas to serve a large DC; large users pay 14-17 cents/kWh; Alaska LNG no FID, $44B+, gas would cost more.

RULE: Avoid re-litigating the Alaska-data-center energy-cost claim and Dunleavy's data-center power-price pitch. A genuinely NEW angle/topic is fine. Prefer a different sector entirely (defense AI, fisheries AI, rural healthcare/telehealth AI, broadband/BEAD, workforce, Indigenous data, public-sector AI adoption).

## Seasonal / industry context for scouts
- Alaska 2nd session of 34th Legislature wrapping (budget, PFD, energy bills).
- Salmon season ramping (Copper River open; Bristol Bay sockeye approaching).
- Federal FY-end Sept 30 (not imminent).
- Live national threads: AI data-center power demand, Arctic/defense posture, federal AI procurement, rural broadband (BEAD), Alaska LNG / energy.

## Cached Gmail address
- TBD (discover once)

## Phase 3 validation status (IMPORTANT recovery log)
- STALE-FILE INCIDENT: out/ contained prior-run artifacts (desk_dossier.json, stack_anatomy.json, and a same-named merged_candidates.json with desk content). My first Write silently failed; 4 validators (round 1) read STALE desk candidates. Cleaned out/ and rewrote merged_candidates.json correctly, then spawned ONE clean validator (a8b13d3) with arctic candidates fully INLINE.
- ARCTIC LEAD FAILS GATE 1: two independent validators report Defense News (Davis, 2026-01-26) + CEPA URLs return HTTP 404; Davis verbatim NOT verifiable on a live page. Breaking Defense counter-evidence (11th Airborne, Gen. Cogbill "everything breaks at -40") DOES verify, but asserter does not. Per anti-hallucination rules, arctic claim is DROPPED unless clean validator finds a live asserter URL (unlikely).
- BRAWLEY (from stale desk file) NOT selected: corrective thesis re-centers Chugach "no gas" energy-supply story already corrected in both NO. 02 issues -> dedupe-spirit violation (3rd straight energy piece).
- Round-1 validators are tainted by stale read -> DISCARD their verdicts.
- DECISION RULE: take clean validator a8b13d3's verdict on the real candidates. Best fresh dedupe-clean fallback if arctic fails = no_ai_strategy (ADN editorial + Kaye; counter = HB 488 passed, OIT AI features, DOE district AI guidelines). Do NOT manually promote past gate.
- EDITOR'S NOTE items so far: (1) state.yaml kicker is "COLD TAKE" not "RECEIVED WISDOM" (used file value for image; email branding label = "Received Wisdom" per Phase 9). (2) Stale prior-run artifacts found in out/ and removed; one round of validators wasted on stale data; re-run clean. (3) Arctic-defense lead dropped at attribution gate (source URLs 404). (4) SendMessage unavailable, could not hot-patch running scouts; dedupe enforced at gate instead.
