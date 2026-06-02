# Received Wisdom — NO. 06 — Selection

**Run date:** 2026-06-02
**Discourse slice:** policy_official
**Branch:** claude/linkedin-contrarian-2026-06-02

## The claim (verbatim)

> "Our goal was to basically try to replicate the services with the chatbot that we would provide with a human facilitator"

**Asserter:** Stacey Marz, Administrative Director, Alaska Court System
**Source:** NBC News (syndicated via AOL), 2026-01-03 — https://www.aol.com/articles/alaskas-court-system-built-ai-110000726.html

## Steelman (stated before any correction)

Alaska has roughly 7,000 self-represented litigants seeking court help each year, across a state larger than Texas, with no law school and severe legal-aid scarcity. A 24/7 chatbot that reliably answers routine procedural questions (hours, forms, deadlines) would genuinely extend access and ease staff load. Other jurisdictions have shipped narrower court AI tools that work. In a state where the alternative is often no help at all, aiming to replicate facilitator coverage is a defensible north star, not naive techno-optimism.

## Corrective thesis (one sentence)

The right design target for Alaska's access-to-justice AI is reliable augmentation of human facilitators on bounded, high-confidence questions, not replication of their open-ended judgment, because the AVA deployment showed that a general-purpose model asked to stand in for a facilitator fails precisely on the high-stakes questions, and those failures land hardest on the most legally vulnerable Alaskans.

## Evidence spine (all in claim_dossier.json)

1. **Primary, same article:** AVA hallucinated a non-existent Alaska law school when asked where to find legal help. Marz: "We're not confident that the bots can work in that fashion, because of the issues with some inaccuracies and some incompleteness." Validated test-question set cut from 91 to 16. A three-month project ran more than 18 months past target. (NBC News / AOL, 2026-01-03)
2. **Primary, peer-reviewed:** Rice et al., Frontiers in Artificial Intelligence (April 2025) — Stanford, ANTHC, UAF, Southcentral Foundation, Maniilaq — high-stakes AI deployment in Alaska requires community-engaged methodology, multi-year data integration, and explicit ELSI frameworks; only 0.2% of 1,000+ AI healthcare papers even mention community involvement. (https://pmc.ncbi.nlm.nih.gov/articles/PMC12009764/)

## Business consequence (the desk frame)

Court procurement officers, govtech vendors, and legal-aid organizations pursuing AI deployments in Alaska's rural and remote courts are buying against a "facilitator replacement" pitch. The frame that survives the evidence is augmentation with a hard accuracy floor on consequential questions. Anyone underwriting an Alaska justice, health, or social-services AI deployment on a replacement assumption should re-price the reliability gap AVA exposed.

## Tone guardrail for the writer

Corrective and generous, NOT a dunk. Marz and the court already acknowledged the limits publicly; do not mock them. The post credits the ambition, names the structural reason replication fails, and points to the frame that actually works.
