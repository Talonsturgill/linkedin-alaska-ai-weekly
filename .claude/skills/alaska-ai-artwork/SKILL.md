---
name: alaska-ai-artwork
description: Create the bespoke 1080x1080 cover artwork for an Alaska.Ai LinkedIn post (any column — Weekly Brief, Cold Take, The Stack, Anchorage Desk). Every issue gets an original, custom piece of editorial art that illustrates THAT story — a different style, palette, and composition every time, deduplicated against all prior issues. Use whenever a column routine reaches its image phase, or whenever Talon asks for post artwork. The alaska-ai-brief template skill is the emergency fallback only.
---

# Alaska.Ai Artwork — the art brain

You are not filling a template. You are the staff artist of a small,
sharp Alaskan publication, and this issue's cover is yours. The mandate,
in the publisher's words: exquisitely genuine custom artwork that
illustrates the story, with flair, where no two pieces ever look
similar. Slow down, plan like a pro, render, then grind it through the
eval loop until it is genuinely world class.

Everything renders procedurally in Python (Pillow + numpy + scipy, with
opensimplex / shapely / coloraide when installed) through
`art_kit.py` in this directory. You write a fresh `out/art_script.py`
for every issue. The kit gives you primitives; the art is yours.

## Non-negotiables (check every piece against these)

1. **Canvas** 1080x1080 PNG at `out/post_image.png`, built through
   `art_kit.Canvas` (supersampled 2x internally).
2. **Brand marks, small and integrated** — these are the ONLY fixed
   elements; place them wherever the composition wants them:
   - `ALASKA.AI` wordmark (Fraunces Black, small — 26-40px design
     units, any corner/edge, may sit in a chip or knock out of a shape).
   - Kicker line `{KICKER} · {MIDDLE} · {DATE}` in JetBrains Mono
     (14-20px, tracked out). MIDDLE is the column's middle slot
     (volume number or category/role label) passed in by the routine.
   - The Polaris star (`art_kit.polaris`), small, somewhere. It is the
     publication's colophon — a signature, not a subject (unless the
     concept genuinely stars it).
   - The headline, integrated INTO the art (see Typography below).
3. **Legibility at thumbnail.** The piece must read at 300px: one
   dominant focal point, headline legible (contrast >= 4.5:1 against
   its local background — use `art_kit.ensure_contrast` or a chip),
   no critical detail thinner than ~2 design px.
4. **Limited palette.** 2-6 inks + paper. Log every hex in the meta.
   Restraint reads as sophistication; a rainbow reads as clip art.
5. **Cultural guardrail (hard).** Never imitate Alaska Native visual
   traditions — no formline, totemic design, beadwork patterns, ulu or
   mask motifs, or "native-style" ornament. Those languages belong to
   their communities. Alaska is expressible through landscape, light,
   wildlife, industry, weather, and geometry. When a story concerns an
   Alaska Native corporation, represent the BUSINESS (buildings,
   contracts-as-diagrams, regions-as-maps, industries), never the
   cultural iconography.
6. **No confabulated specifics.** Text on the artwork beyond
   headline/marks (stray labels, fake dollar figures, invented docket
   numbers) must come from the verified story dossier or not exist.
7. **Reproducibility.** Every random element seeds from an explicit
   `SEED` constant in art_script.py, recorded in the meta.

## The process — seven steps, in order, no skipping

### Step 0 — Absorb the story

Read the final post (or the dossier/anatomy JSON on a no-target cycle).
Write down, in one sentence each: what happened, why it matters to
Alaska, and the emotional register (triumphant, cautionary, tense,
wry, expansive...). The register drives every aesthetic decision.

### Step 1 — Dedup scan (what has already been made)

Fetch and read prior art ledgers across ALL column branches:

```bash
git fetch origin --quiet
for b in $(git branch -r --list 'origin/claude/linkedin-*' | sort -r | head -n 16); do
  echo "=== $b ==="
  git show "$b:out/post_image.png.meta.json" 2>/dev/null | \
    python3 -c "import json,sys
try:
  m=json.load(sys.stdin)
  print(json.dumps({k:m.get(k) for k in ('date','style_family','hue_family','composition','motifs','technique_stack')}))
except Exception: pass"
done
```

Build the forbidden lists and OBEY them:
- `style_family` used in the last **8** issues → forbidden.
- `hue_family` (dominant hue bucket) used in the last **4** → forbidden.
- Primary motif used in the last **10** → forbidden.
- `composition` pattern used in the last **2** → forbidden.
- The aurora-over-starfield look of the old template counts as a
  permanently "recent" style — never recreate it as the main event.

If the scan returns nothing (no prior branches fetched), note that in
the plan and proceed — but never skip the attempt.

### Step 2 — Concept: find the visual metaphor

Editorial art represents the IDEA, not the scene. Generate THREE
distinct concepts before choosing. For each: the metaphor, why it's
true to the story, and what the reader gets in half a second. Prefer:

- **Metaphor** — abstract mechanism → concrete image (a permitting
  stack as literal geological strata; a chokepoint as an ice-narrowed
  channel one ship fits through).
- **Synecdoche** — one charged detail stands for the whole (a single
  interconnection breaker for a grid fight).
- **Scale contrast** — the tiny against the vast (one surveyor's stake
  in an immense tundra; a server rack dwarfed by a mountain wall).
- **Juxtaposition** — two worlds meeting in one frame (fiber-optic
  line drawn as a river through sea ice; caribou watching a data
  center bloom light on the horizon).
- **Diagram-as-art** — for The Stack especially: exploded isometric
  layers, cutaways, schematics that are beautiful, labeled sparsely.

Kill any concept that is generic (lightbulbs, handshakes, brains made
of circuits, hockey-stick charts). If it could run on any tech blog,
it is dead. It must be OF ALASKA and OF THIS STORY.

Pick the strongest. One idea per piece.

### Step 3 — Pre-production blueprint (SLOW DOWN — plan before code)

Write `out/art_plan.md` BEFORE writing any render code. This is the
professional's storyboard pass — the space to think pixel by pixel.
Required sections:

1. **Concept statement** — two sentences: the metaphor and the read.
2. **Register** — the emotional target and how the palette/forms
   carry it.
3. **Style family** — from the atlas below (or a deliberate hybrid),
   plus WHY it fits this story, plus confirmation it clears the
   dedup cooldowns.
4. **Palette** — every ink as hex, with its role (paper, field,
   shadow, focal accent, type). State the value structure: where the
   darkest dark and lightest light sit and why the focal point wins
   the contrast war. Build it in OKLCH (`art_kit.oklch`) so the
   lightness steps are honest.
5. **Composition map** — a coordinate plan on the 1080 grid. Name the
   pattern (thirds / golden spiral / central icon / horizon band /
   diagonal thrust / radial burst / grid modular). Then place EVERY
   element with numbers: "horizon y=690; focal vessel center
   (410, 585) spanning ~300px; headline block x∈[96,984] top at 84;
   wordmark bottom-left (96, 996); kicker under headline at y=214;
   polaris (930, 78) r=14." Trace the intended eye path in one line
   (e.g. headline → focal → diagonal wake → wordmark).
6. **Layer build order** — the exact painting sequence back-to-front
   (e.g. paper → sky gradient → far ridge → mid ridge → water field →
   focal silhouette → texture pass → grain → type → marks).
7. **Technique stack** — which kit calls do the heavy lifting
   (`field`+`warp`, `streamlines`, `riso`, `halftone`, `hatch`,
   `iso_prism`, `reaction_diffusion`...), with the parameter ranges
   you intend.
8. **Risk list** — the 2-3 ways this could look amateur (mud in the
   midtones, headline collision with busy texture, silhouette reading
   as a blob...) and the planned mitigation for each.

A thin plan produces thin art. If you cannot place elements with
coordinates yet, you have not finished thinking.

### Step 4 — Build

Write `out/art_script.py`: a standalone script that imports art_kit
(`sys.path.insert(0, ".claude/skills/alaska-ai-artwork")`), defines
`SEED`, builds the piece in the planned layer order, and finishes with
the full meta dict (schema below). Run it with
`python out/art_script.py`. Keep runtime under ~90 seconds (mind
`reaction_diffusion` steps and `streamlines` counts; supersampling
already doubles pixel work).

Craft rules while building:

- **Three scales of detail, everywhere it belongs.** MACRO: the 3-6
  big shapes that carry the composition. MESO: the structure inside
  each big shape (a pack-ice field is hundreds of `voronoi_polys`
  floes with per-floe shading and dark seams, not one flat fill; a
  hillside is banded stands of trees; a building has floors, windows,
  rooflines). MICRO: the finishing life — `chips` debris, `stipple`,
  cracks, glints, foam rims, tiny tracks, birds. A piece that only
  has macro shapes is a draft, not a cover. No region larger than
  ~15% of the canvas may be a single flat fill (deliberate negative
  space around type is the one exception, and even it should carry
  paper texture).
- Density with hierarchy: micro-detail must ENRICH the big shapes,
  never bury the focal point — detail contrast stays highest at the
  focal, calmer toward the edges.
- Work back-to-front. Establish the value structure early with big
  shapes; details never rescue a bad value plan.
- Silhouettes are made of composed primitives: `blob_pts` for organic
  mass, polygons for built things, `ridge_pts` for terrain,
  `wobble_pts`/`hand_line` to take the digital edge off. Check every
  silhouette in isolation: fill it black — does it read instantly?
- Texture is seasoning, not soup: ONE finishing texture identity per
  piece (grain OR halftone OR hatch OR mottle+grain), applied with
  restraint (`grain` 4-9, `mottle` 0.03-0.08).
- Atmospheric depth: layers get lighter and less saturated with
  distance (`lighten`/`mix` toward the sky color per layer).
- Never place raw text on busy texture — reserve a quiet zone in the
  plan, or use `chip`, or knock a panel out of the art.

### Step 5 — The eval loop (self-healing; world class or it doesn't ship)

Render, then LOOK at the image (Read the PNG — actually study it at
full size, and mentally at thumbnail scale). Score it 0-10 on each
dimension, honestly, as the harshest art director you know:

| Dimension | What a 10 means |
|---|---|
| Concept | The metaphor lands in <1s and is specific to THIS story |
| Focal hierarchy | One unmistakable focal point; eye path flows; reads at 300px |
| Composition | Balanced but alive; negative space works; nothing cramped or orphaned |
| Color & value | Palette feels inevitable; focal wins contrast; grayscale check still reads |
| Detail richness | Rewarding at nose length AND arm's length: three scales of detail everywhere it belongs; no empty acreage |
| Craft & finish | Tactile, print-like, deliberate; zero default-y artifacts (banding, stray aliasing, uncomposed overlaps) |
| Typography | Headline integrated into the art, legible, tracked/sized like a poster, not pasted on |
| Originality | Would stop a designer's scroll; resembles no prior issue (check the dedup list again) |
| Story fidelity | Someone who read the post says "yes, that's it exactly" |

**Ship bar (world class): weighted mean >= 8.5 with no dimension
below 7.** Weights: Concept .18, Focal .13, Composition .13,
Color .13, Detail .12, Craft .10, Typography .09, Originality .08,
Fidelity .04.

**8.5 is the FLOOR, not the target.** Iterations are the normal cost
of quality, not an exception path — a first render that ships
unchanged should be rare. While you have iteration budget left and a
fix would clearly buy quality, take the iteration. Be exhaustive: the
publisher's standard is a piece that could hang as a print and stops
a designer's scroll, every single issue.

Below the bar → diagnose the WEAKEST dimension, write one line on the
targeted fix, edit art_script.py, re-render, re-score. This is a
loop: repeat up to **6 iterations**. Score every pass into
`eval_history` in the meta. If iteration 6 still misses, ship the
highest-scoring render and flag the miss + weakest dimension in the
Editor's note. Self-healing also covers crashes: if the script
errors, read the traceback, fix, re-run — script failures do not
count as eval iterations, but give up after 4 consecutive crashes
and use the fallback (Step 7).

Common fixes by weak dimension: Concept → strengthen or swap the
metaphor, remove decorative noise that dilutes it. Focal → raise
focal contrast, dim competitors, crop tighter. Composition → move
elements onto the planned grid, open negative space. Color → cut an
ink, re-run the grayscale check, push value gaps apart. Detail →
fracture flat fills into structured cells (`voronoi_polys`), add a
meso pass inside each big shape and a micro pass (`chips`,
`stipple`, cracks, glints) at the focal. Craft → one texture
identity, fix edge quality, add `wobble_pts` humanity. Typography →
resize/re-rag, chip it, clear the quiet zone.

### Step 6 — Technical QA + ledger

```bash
python .claude/skills/alaska-ai-artwork/qa_check.py \
  --image out/post_image.png --date "{D MMM YYYY}" --column "{KICKER}"
```

Must PASS. The meta sidecar (written by `Canvas.finish`) is the dedup
ledger entry — required keys:

```json
{
  "date": "26 JUN 2026",  "column": "The Stack",  "kicker": "THE STACK",
  "middle_slot": "FACILITIES",  "headline": "the quotable headline",
  "style_family": "wpa_layered",  "palette": ["#0b2545", "..."],
  "hue_family": "blue-teal",  "composition": "horizon_band",
  "motifs": ["icebreaker", "sea ice"],
  "technique_stack": ["field", "warp", "grain"],
  "seed": 77,  "eval_history": [{"iter": 1, "weighted": 7.9, "weakest": "focal"}],
  "eval_final": {"weighted": 8.8, "scores": {"concept": 9, "...": 0}}
}
```

`hue_family` buckets: red, orange, gold, green, teal, blue-teal, blue,
indigo, violet, magenta, neutral-warm, neutral-cool.

### Step 7 — Fallback (never ship nothing)

If bespoke art is unrecoverable this run (4 consecutive script crashes,
or environment failure), render the legacy template
(`python .claude/skills/alaska-ai-brief/build_template.py ...`) so the
email always carries an image, and say plainly in the Editor's note
that the fallback fired and why. The fallback is a fire exit, not a
door — using it twice in a row is a defect to flag.

## Style atlas (pick against the dedup list; hybridize deliberately)

Each family names its geometry, its kit recipe, and when it fits.
These are starting grammars — vary them hard; the atlas is not a set
of templates.

1. **wpa_layered** — flat layered landscape, <8 inks, big type. Stacked
   `ridge_fill` with a `lighten` ramp, `gradient_v` sky, one focal
   silhouette. Expansive/park-service register.
2. **ukiyo_bokashi** — flat planes + fine outlines + banded sky
   (`gradient_v` smooth), asymmetric composition, unusual viewpoint
   (from above a wave, up a cliff). Contemplative, weather stories.
3. **swiss_grid** — modular grid, huge type as form, 2 inks + paper,
   geometric counters, diagonal energy. Policy/regulatory analysis.
4. **constructivist** — diagonal thrust, `rays`, bold wedges, red/black/
   cream classic (vary hues), photo-less agitprop energy. Power moves,
   contested decisions.
5. **riso_zine** — 2-3 fluorescent-ish inks, `riso` overprint +
   misregistration, `field_mask` shapes, grain. Founder/community
   stories, wry register.
6. **blueprint** — dark paper, single pale ink, `hand_line` schematics,
   dimension ticks, mono labels. Infrastructure anatomy (The Stack).
7. **iso_cutaway** — `iso_prism` exploded diagram, 3-tone face shading,
   tiny mono labels. Mechanism/stack anatomy, layered systems.
8. **flow_field** — `angle_field`+`streamlines` (try `quantize` or
   `curl`, custom distortions — plain smooth Perlin flow is overdone),
   lines colored by a `ramp`. Currents: capital, data, migration.
9. **halftone_pop** — one big photographic-feeling `field` or
   silhouette screened through `halftone`, one accent ink. Bold
   personality/decision stories.
10. **engraving** — `hatch`+`stipple` shading of big silhouettes,
    one ink on paper, dense craft. Historical echo, institutions.
11. **topo_map** — contour lines (threshold a `warp`ed `field` at
    several levels, draw `field_mask` outlines), spot labels, a route
    line. Land, leases, siting fights.
12. **aurora_field** — reserved: too close to the legacy template.
    Only as a faint background accent under another family.
13. **deco_rays** — symmetric `rays`, stepped borders, metallic-feeling
    golds, centered icon. Landmark announcements.
14. **mosaic_voronoi** — scipy Voronoi cells clipped to a silhouette
    (via shapely), 3-4 inks by region, grout lines. Coalitions,
    many-parties stories.
15. **organic_rd** — `reaction_diffusion` texture masked into shapes;
    coral/labyrinth morphologies. Growth, ecosystems, fisheries, AI
    diffusion itself.
16. **paper_collage** — torn shapes (`blob_pts` with high wobble +
    `mottle` per piece), hard shadows, layered scraps. Messy multi-
    stakeholder disputes.
17. **pixel_dither** — coarse posterized `field` + ordered-dither feel
    via `halftone` with tiny cells, limited retro palette. Compute,
    software, satellite stories.
18. **minimal_line** — one continuous `hand_line` drawing + one accent
    fill, vast negative space. Quiet-week essays, contemplative takes.

## Color method (per piece, never a house palette)

1. Pick the emotional temperature from the register; pick a base hue.
2. Build 2-6 inks in OKLCH (`oklch(l, c, h)`), using a `harmony`
   scheme (complementary for tension, analogous for calm, split for
   energy-with-control, mono_accent for austere focus).
3. Enforce a VALUE SPINE first: paper/light (L≈0.85-0.97), field
   (L≈0.55-0.75), shadow (L≈0.25-0.4), ink/dark (L≈0.12-0.25). Hue is
   costume; value is anatomy. Squint-test (grayscale) must still read.
4. The focal accent gets the highest chroma AND a value gap from its
   surroundings. Everything else stays quieter than it.
5. Alaska light is real material: low-angle gold (h≈80-95), long blue
   shadow (h≈250-265), fireweed magenta (h≈340), spruce black-green
   (h≈150, low L), sea-ice cyan (h≈200). Use them when the story is
   outdoors; don't force them elsewhere.

## Typography (Fraunces + JetBrains Mono only — the brand glue)

- Headline: Fraunces variable. Vary the VOICE per piece via axes:
  opsz 144 + wght 900 (poster), wght 500 + SOFT 80 (gentle), WONK 1
  (quirky flair — sparingly, founders/zine pieces), italic (motion,
  editorial aside). Sizes 54-120 design px typical; tighter leading
  (~1.02-1.12); rag on meaning, 2-4 words a line.
- Type IS a design element: it can sit inside the scene (behind a
  ridge line via draw order), stack vertically, run on a diagonal
  (`text(..., angle=...)`), or dominate swiss-style. It must never
  look pasted on top as an afterthought.
- Mono is for telemetry only: kicker, labels, coordinates, tiny data.
  Tracked out 0.15-0.3em, small.
- Max two type moments beyond the marks: headline + optionally one
  small supporting line. Art, not a flyer.

## Composition patterns (name one in the plan)

`horizon_band` (low/high horizon, sky does the work) ·
`central_icon` (symmetry, gravitas) · `thirds_focal` (focal on a
third, counterweight opposite) · `diagonal_thrust` (movement, conflict)
· `golden_spiral` (organic flow into a focal) · `radial_burst`
(announcement energy) · `modular_grid` (system stories) ·
`frame_within` (aperture/porthole/window device) · `scatter_field`
(many small units, one anomaly as focal).

Rules that outrank all patterns: one focal point; generous negative
space somewhere; nothing important within 48px of the edge; the
headline zone planned as part of the composition, never leftover space.

## Meta / environment notes

- Deps: Pillow, numpy, scipy guaranteed; opensimplex, shapely,
  coloraide expected (requirements.txt) — the kit degrades gracefully
  without them, but check `art_kit.HAS_SIMPLEX/HAS_SHAPELY/HAS_COLORAIDE`
  if a technique depends on one.
- Fonts auto-download on first use (shared with the brief skill's
  fonts dir when present).
- The old `alaska-ai-brief` template remains ONLY as the Step 7
  fallback and for legacy reproduction.
