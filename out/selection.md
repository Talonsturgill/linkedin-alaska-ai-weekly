# The Stack — selection — 2026-09-11

**CATEGORY = VEHICLES**  (kicker line renders `THE STACK · VEHICLES · 11 SEP 2026`)

## Mechanism
NTIA BEAD Supplemental Deployment Policy Notice (savings "true-up" redeployment)

## News trigger
Roll Call, 2026-09-04 — the Commerce Department announced it would "accept new
proposals from states under the Broadband Equity, Access and Deployment program"
targeting "newly identified unserved locations" that became eligible due to FCC
map changes or program defaults. NTIA Administrator Roth "visited Alaska and
attended a roundtable with broadband providers," and Sen. Dan Sullivan stated
"the new round could make 'over 5,000' new locations eligible for broadband
deployment funding in his state." Policy notice issued 2026-09-03.
Corroborated in-window by Telecompetitor (2026-09-03).

## Layer count
3 layers (reduced from 6 provisional). The mapper dropped the Alaska Broadband
Office layer and the NIST grant-agreement layer because neither had a fetchable
primary source this run (commerce.alaska.gov returned 403; the NIST step was
carried only by a trade summary). Dropping them does not break the
FCC -> NTIA -> GCI spine or the chokepoint, so the mechanism survives.

1. FCC Broadband Serviceable Location Fabric / National Broadband Map —
   creates "newly identified unserved locations." Controlling actor: the
   Commission. Primary source: 47 U.S.C. 642.
2. NTIA BEAD approval and reallocation authority — issues the notice, approves
   or disapproves each state's supplemental final proposal, can reallocate or
   deobligate unspent savings. Controlling actor: Assistant Secretary of
   Commerce for Communications and Information / NTIA Administrator.
   Primary source: 47 U.S.C. 1702.
3. Subgrantee deployment in rural Alaska — builds the last and middle mile,
   explicitly conditioned on BEAD/IIJA subsidy availability. Controlling actor:
   GCI Holdings (subsidiary of GCI Liberty). Primary source: GCI Liberty
   Form 10-K FY2025, filed 2026-02-11.

## Chokepoint
Layer 2. The NTIA Administrator unilaterally approves or disapproves Alaska's
supplemental final proposal and can reallocate or deobligate roughly $370M+ of
Alaska's unspent BEAD savings under 47 U.S.C. 1702(c)(5)(C) and (g)(3). One
statutory officer owns the approve / reject / reallocate binary. Not a committee.

## Structural read
A funding-deployment vehicle whose entire flow narrows to one statutory officer.
The FCC decides who counts as unserved; the NTIA Administrator decides whether
Alaska's leftover savings may chase those locations at all. AI nexus: last- and
middle-mile connectivity to newly-unserved rural Alaska is the physical
substrate for any AI workload outside the Railbelt. Edge compute, satellite and
remote-sensing pipelines, and telehealth or resource-monitoring inference all
stop where fiber and fixed wireless stop. Redeploying the savings to 5,000+
Bush locations is structurally a decision about where Alaska AI can be deployed
at all.

## Forward implication
Treat the NTIA Administrator's approval of Alaska's supplemental final proposal
(submissions triggered by the 2026-09-03 notice, decision expected this fall) as
the binary gating roughly $370M of deployable capital. Confirm which locations
the state expects to put in the supplemental proposal before the submission
window closes, rather than assuming the first-round awards define the footprint.

## Why this one won
- Only high-confidence, clearly in-window mechanism in the field. Notice issued
  8 days before this run; trigger reporting 7 days before.
- Surfaced INDEPENDENTLY by two scouts (vehicles and regulatory). Overlap rule
  applied: the vehicles framing won because leverage sits at the NTIA approval
  desk, not at the state office's upstream selection.
- Not a recent repeat. BEAD has never been anatomized by this column. Distinct
  from the 07-31 FCC Rural Health Care chain and the 07-17 cable-landing chain.
- Non-FERC. The FCC appears only as an upstream map custodian, not as the
  chokepoint, so this clears the "no third FERC chain" and FCC-caution rules.
- VEHICLES is the most under-covered category (absent from the last 6 issues).

## Field dropped (7)
SBA 8(a) ANC entity-owned carve-out (missing per-layer primary source);
FY2027 CR new-start prohibition (diffuse chokepoint — OMB/Congress);
OMB M-25-22 / GSA OneGov AI acquisition (no AK consequence);
ISDEAA Title V / ANMC transfer to ANTHC (missing per-layer primary source);
DAF Enhanced-Use Lease data centers 10 U.S.C. 2667 (no news tie, trigger ~13
weeks stale); STAK Energy ADL 422741 (no news tie, FFD not yet issued);
APFC POMV draw (diffuse chokepoint — Legislature is a body, Board a committee).

## Deviations to surface in the Editor's note
The NTIA Supplemental Deployment Policy Notice PDF itself was never fetchable
(persistent HTTP 503 across every ntia.gov and broadbandusa.ntia.gov path, for
both scouts and the mapper). fcc.gov, broadbandmap.fcc.gov and
commerce.alaska.gov returned 403. The mapper re-anchored every surviving layer
to a fetched statute or filing rather than cite an unfetched page, and declined
to ship the unverified Alaska Broadband Office director name. Window was NOT
broadened; selection made at 14 days.
