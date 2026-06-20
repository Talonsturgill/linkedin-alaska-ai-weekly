#!/usr/bin/env python3
"""Build the no-target Received Wisdom Gmail HTML body from claim_dossier.json."""
import json, html, datetime, sys

DOSSIER = "out/claim_dossier.json"
RUN_DATE = "2026-06-19"
BRANCH = "claude/linkedin-contrarian-2026-06-19"
ISSUE = "NO. 20"
LABEL = "Received Wisdom"

d = json.load(open(DOSSIER))
note = d.get("_validation_note", "")
dropped = d.get("dropped_claims", [])

reason_labels = {
    "no_primary_counter": "No re-fetchable primary counter-evidence",
    "not_load_bearing": "Not load-bearing (too generic)",
    "true_as_stated": "Steelman is true as stated (nothing to correct)",
    "single_non_primary": "Single-sourced, counter not verifiable",
    "recent_repeat": "Recently corrected (last 6 issues)",
    "strawman_unverified": "Verbatim not confirmable on a live page",
}

rows = []
for c in dropped:
    cid = html.escape(c.get("id", ""))
    cv = html.escape((c.get("claim_verbatim") or "")[:240])
    ass = html.escape(c.get("asserter", ""))
    rl = reason_labels.get(c.get("drop_reason", ""), html.escape(c.get("drop_reason", "")))
    detail = html.escape(c.get("detail", ""))
    rows.append(f"""
      <tr>
        <td style="padding:10px 12px;border-bottom:1px solid #e6e6e6;vertical-align:top;font-family:Georgia,serif;">
          <div style="font-style:italic;color:#222;">&ldquo;{cv}&rdquo;</div>
          <div style="font-size:12px;color:#666;margin-top:4px;">{ass}</div>
        </td>
        <td style="padding:10px 12px;border-bottom:1px solid #e6e6e6;vertical-align:top;font-family:Arial,sans-serif;font-size:13px;white-space:nowrap;color:#8a1c1c;font-weight:bold;">{rl}</td>
      </tr>
      <tr>
        <td colspan="2" style="padding:0 12px 12px 12px;border-bottom:1px solid #e6e6e6;font-family:Arial,sans-serif;font-size:12px;color:#555;line-height:1.5;">{detail}</td>
      </tr>""")

rows_html = "".join(rows)
ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

editor_note = (
    "A clean no-target cycle. The scouts surfaced eight live, named, circulating claims across all four "
    "discourse slices, and the validator put each through the six-point gate. None cleared. Worth flagging for "
    "the next run: three of the seven drops were driven at least partly by HTTP 403 access blocks on otherwise "
    "credible Alaska sources during re-verification (Alaska Beacon, Wrangell Sentinel) and on a manufacturer site "
    "(Quantum Systems), not by the claims being demonstrably false. Candidate H (Painter, &lsquo;data centers "
    "require massive energy and few jobs&rsquo;) was the structurally strongest target and is rebuttable from "
    "ADN primary sources on fiscal-yield-per-megawatt; if a future scout supplies an independently fetchable "
    "syndicated URL whose verbatim resolves on the live page, it is revisable. Candidate A (Arctic drones fail "
    "in the cold, 11th Airborne via Breaking Defense) was the second-strongest and had a clean claim, but its "
    "counter-evidence could not clear the primary / two-independent-outlet bar. No subagent stalled; no image "
    "fallback or hosting swap was needed (no image was rendered this cycle). The honest outcome is no post."
)

body = f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;background:#f4f4f2;">
<div style="max-width:680px;margin:0 auto;background:#ffffff;">
  <div style="background:#0b1430;padding:22px 28px;">
    <div style="font-family:Georgia,serif;font-size:24px;color:#ffffff;font-weight:bold;letter-spacing:0.5px;">Alaska.Ai &mdash; {LABEL}</div>
    <div style="font-family:'Courier New',monospace;font-size:12px;color:#ffc72c;margin-top:6px;letter-spacing:1px;">COLD TAKE &middot; {ISSUE} &middot; {RUN_DATE}</div>
  </div>

  <div style="padding:24px 28px;">
    <div style="background:#fbeaea;border:1px solid #e3b3b3;border-radius:6px;padding:16px 18px;margin-bottom:20px;">
      <div style="font-family:Arial,sans-serif;font-size:16px;color:#8a1c1c;font-weight:bold;">No defensible target this cycle</div>
      <div style="font-family:Arial,sans-serif;font-size:13px;color:#5a2222;margin-top:6px;line-height:1.5;">
        The discovery sweep ran in full and the attribution gate ran in full. No claim cleared all six checks,
        so nothing shipped. This is a correct outcome for the column, not a failure of the run. No LinkedIn post
        and no image were produced.
      </div>
    </div>

    <div style="font-family:Arial,sans-serif;font-size:14px;color:#222;font-weight:bold;margin:0 0 8px 0;">Validator&rsquo;s note</div>
    <div style="font-family:Arial,sans-serif;font-size:13px;color:#444;line-height:1.6;margin-bottom:24px;">{html.escape(note)}</div>

    <div style="font-family:Arial,sans-serif;font-size:14px;color:#222;font-weight:bold;margin:0 0 8px 0;">Claims considered and why each was dropped</div>
    <table style="width:100%;border-collapse:collapse;border:1px solid #e6e6e6;margin-bottom:24px;">
      <tr style="background:#f0f0ee;">
        <td style="padding:8px 12px;font-family:Arial,sans-serif;font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.5px;">Claim &amp; asserter</td>
        <td style="padding:8px 12px;font-family:Arial,sans-serif;font-size:12px;color:#666;text-transform:uppercase;letter-spacing:0.5px;">Gate failure</td>
      </tr>{rows_html}
    </table>

    <div style="font-family:Arial,sans-serif;font-size:14px;color:#222;font-weight:bold;margin:0 0 8px 0;">Editor&rsquo;s note</div>
    <div style="font-family:Arial,sans-serif;font-size:13px;color:#444;line-height:1.6;margin-bottom:8px;">{editor_note}</div>
  </div>

  <div style="background:#0b1430;padding:16px 28px;">
    <div style="font-family:'Courier New',monospace;font-size:11px;color:#9fb0d8;line-height:1.6;">
      {LABEL} &middot; run {ts}<br>
      branch {BRANCH}
    </div>
  </div>
</div>
</body></html>"""

payload = {
    "subject": f"Alaska.Ai — Received Wisdom Draft — {RUN_DATE}",
    "to": "talon.sturgill@gmail.com",
    "html_body": body,
}
json.dump(payload, open("out/gmail_payload.json", "w"), indent=2)
print("WROTE out/gmail_payload.json")
print("html_body bytes:", len(body))
