---
name: alaska-ai-brief
description: EMERGENCY FALLBACK image path — the locked aurora/starfield Alaska.Ai template (1080x1080 PNG). The primary image path for every column is the alaska-ai-artwork skill (bespoke editorial art per issue); use this template ONLY when the artwork pipeline is unrecoverable this run (4 consecutive render-script crashes or environment failure), and flag the fallback in the Editor's note.
---

# Alaska.Ai Weekly Brief Template — LinkedIn Square

> **STATUS: EMERGENCY FALLBACK ONLY.** The primary image path for every
> column is now the `alaska-ai-artwork` skill (bespoke editorial art per
> issue). Use this locked template only when the artwork pipeline is
> unrecoverable this run (see that skill's Step 7), and flag the
> fallback in the Editor's note.

Generate the Alaska.Ai weekly brief post graphic for the LinkedIn surface.
Use when creating the visual header for a new weekly Alaska AI news brief
that will be posted to the Alaska.Ai LinkedIn page. Outputs a 1080x1080
square PNG using the locked Alaska.Ai brand design tokens. Parameterized
for volume number, topic title, date, and byline.

## When to use

Trigger this skill whenever Talon writes "weekly brief", "Alaska.Ai post
graphic", "brief header", "next issue", or similar language indicating a
new entry in the weekly brief series for the LinkedIn page. Also triggers
on any request to generate a LinkedIn-feed post header for the Alaska.Ai
brand specifically.

Do NOT use for:
- The Facebook portrait variant (1080x1350 lives in the sister repo
  `alaska-ai-weekly`).
- The LinkedIn cover photo / banner (separate one-off asset).
- The profile picture (separate asset).
- Generic post graphics for other Talon brands or projects.

## Inputs (CLI args, all optional, sensible defaults)

- `--volume` Volume number string. Default `VOL. 01`. Examples `VOL. 02`,
  `VOL. 14`.
- `--topic` Topic title / quotable headline. Use `\n` for line break.
  Default `Defense AI Buy\nLands In Alaska`. Keep to 1-2 lines, max ~28
  chars per line for legibility at the locked 88pt display size.
- `--date` Date stamp. Default `12 MAY 2026`. Format day-month-year all
  caps.
- `--byline` Byline credit. Default `BY TALON`.
- `--kicker` Kicker label above the headline. Default `WEEKLY BRIEF`. Can
  be swapped for `DEEP DIVE`, `FIELD NOTES`, `SPECIAL ISSUE`, etc.
- `--motto` Italic gold motto under the headline. Default `what's moving
  in alaska ai, this week`.
- `--coords` Footer coordinates stamp. Default `61°13′N  ·  149°54′W`
  (Anchorage).
- `--seed` Random seed for aurora + starfield. Default `11`. Same seed
  produces the same render.
- `--out` Output PNG path. Default
  `./alaska-ai-brief-{vol_slug}.png` derived from volume number.

## Locked design tokens (do not alter without rebrand approval)

```
SKY_TOP        rgb(2, 6, 20)     deep night sky
SKY_HORIZ      rgb(8, 20, 44)    flag-blue at horizon
FLAG_GOLD      rgb(255, 199, 44) Pantone 1235, Alaska state flag gold
FLAG_GOLD_HALO rgb(255, 218, 110) gold halo for stars and glows
FORGETMENOT    rgb(110, 165, 255) state flower blue, accent only

AURORA cyan-green   rgb(60, 230, 180)
AURORA cyan-blue    rgb(90, 200, 240)
AURORA violet       rgb(150, 100, 230)

DISPLAY FONT  Fraunces variable, opsz=144 wght=900 (Black) for headlines
ITALIC FONT   Fraunces Italic variable, opsz=12 wght=400 SOFT=50
MONO FONT     JetBrains Mono Regular for telemetry stamps
```

## Composition spec (1080x1080 square)

- Canvas 1080x1080 (1:1, modern LinkedIn feed standard, balanced for
  desktop + mobile)
- Polaris gold star at top center, y=140, radius=34
- ALASKA.AI wordmark in Fraunces Black 64pt, white, top, y~210
- Kicker line in JetBrains Mono Medium 18pt, gold @ 80%, format
  `KICKER · VOL · DATE`, y~300
- Thin 120px gold rule beneath kicker, y~345
- Topic headline in Fraunces Black, **auto-shrink from 88pt → 56pt** to
  fit canvas width and the tighter square vertical
- Italic gold motto beneath headline
- Footer band at y=H-90 with coordinates centered. Byline argument is
  accepted and stored in the sidecar meta JSON but is not drawn on the
  canvas
- Coordinates stamp `61°13′N · 149°54′W` (Anchorage default, overridable),
  horizontally centered above the hairline
- Thin gold hairline above footer

## Soft aurora wash + starfield

- 3 aurora layers (cyan-green, cyan-blue, violet) with vertical bell +
  horizontal noise + heavy gaussian blur
- Intensity max 105 per layer (softer than cover, doesn't fight headline
  legibility)
- 130 stars in upper 50% of canvas (less area than the portrait variant,
  so a lower count prevents visual clutter), varying brightness, brightest
  get 4-pixel halos
- `--seed` controls aurora + star placement deterministically

## Dependencies

- Python 3.11+
- pillow, numpy, scipy
- Fraunces variable font (TTF), Fraunces Italic variable (TTF)
- JetBrains Mono Regular + Medium (TTF)

The build script auto-downloads fonts to `./fonts/` (relative to the
script) on first run if missing. Cached after that by the environment
snapshot.

## How to invoke from a Claude Code routine

```bash
python .claude/skills/alaska-ai-brief/build_template.py \
  --volume "VOL. 02" \
  --topic "Cook Inlet Power Math\nBreaks The Deal" \
  --date "19 MAY 2026" \
  --byline "BY TALON" \
  --kicker "WEEKLY BRIEF" \
  --out "out/post_image.png"
```

A sidecar `out/post_image.png.meta.json` is written next to the PNG with
the render parameters and timestamp.

## Output

A 1080x1080 PNG. Roughly 160-200 KB. Sharp on retina. Drops cleanly into
LinkedIn feed (1:1 square, best for native upload).

## Cross-platform notes

- LinkedIn native upload only. Do not attach as a link preview.
- For the Facebook portrait variant (1080x1350), see the sister repo
  `alaska-ai-weekly`.
- For Instagram cross-post, this 1080x1080 works directly.
- For LinkedIn cover banner use, generate a 1584x396 horizontal variant
  separately (not this skill).

## When the brand evolves

If brand tokens change (new accent color, new font, new motto), update
this SKILL.md AND the `build_template.py` constants in lockstep. Also
update the sister Facebook repo so the two surfaces stay visually
synchronized. Don't let token drift between Facebook portrait, LinkedIn
square, the cover, and the profile.
