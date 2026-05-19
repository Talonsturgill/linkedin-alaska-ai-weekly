# linkedin-alaska-ai-weekly

Source for the **Alaska.Ai Weekly LinkedIn Post** Claude Code Routine. Sister automation to [`alaska-ai-weekly`](https://github.com/Talonsturgill/alaska-ai-weekly), which runs the same desk for the Facebook surface.

This routine is biz-shifted. The Facebook automation frames each story for a civic-reader audience. This one frames the same week for industry leadership, federal contractors, capital allocators, and policy professionals. Every paragraph should land a business consequence.

Every week, a Claude routine cloned from this repo:

1. Spawns five parallel research subagents covering biz-shifted beats (Workforce & jobs, Capital & contracts, Industry deployment, Policy & regulation, Enterprise & infrastructure).
2. Validates every story (URLs resolve, dates in window, sourcing rule, named industry consequence per story).
3. Selects the lead + 2-4 supporting stories.
4. Drafts the post in the analytical, position-taking voice anchored on `examples/post_001.md`, 500-700 words, ending with an engagement question and a 3-5 hashtag line from the whitelist.
5. Runs an editor + scorer loop until the rubric threshold holds and every hard-fail check passes.
6. Renders a 1080x1080 square brand image via the `alaska-ai-brief` skill.
7. Drops a polished HTML draft in your connected Gmail with the post text + image inline.
8. Commits all artifacts to a `claude/linkedin-weekly-{YYYY-MM-DD}` branch.

## Setup

1. Push this repo to GitHub.
2. Open https://claude.ai/code/routines and create a new routine bound to this repo.
3. Configure: model = Opus, network = Trusted, connectors = Gmail, schedule = weekly. Stagger from the Facebook routine to spread the editorial load (e.g. Facebook Saturday 5am AKT, LinkedIn Monday 6am AKT).
4. Paste the prompt from `prompts/routine_instructions.md` into the Instructions field.
5. Set `launch_date` in `config/state.yaml` to the day VOL. 01 ships on LinkedIn.
6. Click **Run now** for a smoke test before the first scheduled run.

## Local smoke test of the image renderer

```bash
pip install -r requirements.txt
mkdir -p out
python .claude/skills/alaska-ai-brief/build_template.py \
  --volume "VOL. 01" \
  --topic  "Defense AI Buy\nLands In Alaska" \
  --date   "12 MAY 2026" \
  --byline "BY TALON" \
  --kicker "WEEKLY BRIEF" \
  --out    out/post_image.png
```

A sidecar `out/post_image.png.meta.json` is written next to the PNG.

## What the routine does NOT do

- Post directly to LinkedIn. The Gmail draft is the human checkpoint, copy/paste from there into LinkedIn after a final read.
- Render the LinkedIn cover banner (separate one-off 1584x396 asset).
- Render the profile picture (static).

## Received Wisdom routine (second, independent column)

A second routine on this repo produces a different post type: a corrective
explainer that takes ONE widely circulating claim about Alaska and AI, states
it fairly at its strongest, then corrects it or fills the load-bearing piece it
leaves out, using primary-source evidence. It is depth-first and not tied to a
news window.

How it differs from the weekly recap:

- **Pure discovery.** Four parallel `claim-scout` agents sweep current
  discourse (Alaska press/op-eds, trade/analyst, policy/official, exec/social)
  for claims that are actually circulating, each quoted verbatim with a named
  asserter. No backlog file.
- **Anti-strawman attribution gate.** One `claim-validator` agent enforces a
  six-point gate (named attribution, independent circulation, load-bearing,
  steelman survives, rebuttable from primary evidence, not a recent repeat).
  If nothing clears the gate, the routine ships an honest "no defensible
  target this cycle" email instead of inventing one.
- **Corrective, not snarky.** Steelman the claim generously, then correct it.
- **Own identity.** Kicker `RECEIVED WISDOM`, issue counter `NO. 0N` derived
  from the count of distinct `claude/linkedin-contrarian-*` branch date stems
  (independent, possibly irregular cadence — no `launch_date` formula).
- **Own branch namespace.** Artifacts land on
  `claude/linkedin-contrarian-{YYYY-MM-DD}`, disjoint from
  `claude/linkedin-weekly-*`, so the two routines never collide.

It reuses the same `writer`, `editor`, and `scorer` agents (each has a gated
Corrective Explainer section that activates only when the orchestrator says so),
the `alaska-ai-brief` image skill unchanged, and the Gmail-draft handoff. The
weekly recap is byte-identical regardless of these additions.

Setup: create a SECOND routine at https://claude.ai/code/routines bound to this
same repo, configure model = Opus, network = Trusted, connectors = Gmail, set
its own schedule (independent of the weekly), and paste the prompt from
`prompts/contrarian_instructions.md` into the Instructions field.

## Differences from the Facebook sister automation

| Surface | Word target | Image | Hashtags | Hook discipline |
|---------|-------------|-------|----------|-----------------|
| Facebook (`alaska-ai-weekly`) | 280-420 | 1080x1350 portrait | None | Standard opening line |
| LinkedIn (this repo) | 500-700 | 1080x1080 square | 3-5 from `brand.yaml` whitelist | First 2 lines stand alone (~210 char "see more" cutoff) |

Both surfaces share the punctuation discipline (no em-dashes, en-dashes, double-hyphens, colons, or semicolons in body), the anti-hallucination rules, the 5-agent subagent pipeline, the Gmail draft handoff, and the locked Alaska.Ai brand tokens.

## Files of note

- `prompts/routine_instructions.md` — the pasted weekly-recap routine prompt.
- `prompts/contrarian_instructions.md` — the pasted Received Wisdom routine prompt.
- `.claude/skills/alaska-ai-brief/` — the 1080x1080 square brand image generator.
- `.claude/agents/*.md` — subagent definitions (`researcher`, `validator`,
  `writer`, `editor`, `scorer`, plus `claim-scout` and `claim-validator` for
  the Received Wisdom routine).
- `config/brand.yaml` — voice anchor, hashtag whitelist, banned phrases.
- `config/sources.yaml` — Alaska news + research orgs + government + business/trade outlets + national.
- `config/scoring_rubric.yaml` — weekly-recap ship threshold + hard-fail checks.
- `config/contrarian_rubric.yaml` — Received Wisdom ship threshold + hard-fail
  checks (adds `claim_is_attributed` and `steelman_present`).
- `examples/post_001.md` — published style baseline (shared voice anchor).
