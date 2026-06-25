import datetime as dt
import html
import json
from pathlib import Path

DATE = "2026-06-25"
BRANCH = "claude/linkedin-desk-2026-06-25"
SUBJECT = f"Alaska.Ai — Anchorage Desk Draft — {DATE}"

dossier = json.loads(Path("out/desk_dossier.json").read_text())

CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1a1a1a;background:#fafafa;margin:0;padding:24px;}
.wrap{max-width:720px;margin:0 auto;background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:28px;}
h1{font-size:22px;margin:0 0 4px;}
.sub{color:#666;font-size:13px;margin-bottom:24px;}
h2{font-size:16px;margin-top:28px;border-bottom:1px solid #eee;padding-bottom:6px;}
.banner{background:#eef4ff;border-left:4px solid #2b6cff;padding:14px 16px;border-radius:6px;margin:18px 0;font-size:15px;}
.note{background:#f6f6f6;padding:14px 16px;border-radius:8px;font-size:13.5px;line-height:1.55;}
ul{padding-left:20px;} li{margin:10px 0;font-size:13.5px;line-height:1.5;}
.cand{font-weight:600;}
.tag{display:inline-block;background:#fff4e5;border:1px solid #f0a500;color:#8a5a00;font-size:11px;padding:1px 7px;border-radius:10px;margin-left:6px;}
.foot{color:#888;font-size:11px;margin-top:26px;}
"""

note = dossier.get("_validation_note", "")
window = dossier.get("window_used", "n/a")
dropped = dossier.get("dropped_candidates", [])

drop_items = "\n".join(
    f'<li><span class="cand">{html.escape(c.get("subject_name",""))}</span>'
    f'<span class="tag">{html.escape(c.get("drop_reason",""))}</span><br>'
    f'<i>{html.escape(c.get("decision_summary",""))}</i><br>'
    f'{html.escape(c.get("_drop_detail",""))}</li>'
    for c in dropped
)

editor_note = (
    "Four role-slice scouts (founders, operators, municipal, research) ran in parallel; "
    "all four returned. The validator ran the seven-point anti-puff gate at the 30-day "
    "window, returned zero survivors, then re-ran at the broadened 45-day window per "
    "protocol and again returned zero. No subagent stalled. No image, post, score, or "
    "source ledger was generated because no profile shipped. This is the sixth consecutive "
    "no-target cycle for the desk; the Anchorage AI primary-source decision pool is "
    "genuinely thin and the bar was held, not lowered."
)

body = f"""<!doctype html><html><head><style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Alaska.Ai &mdash; Anchorage Desk Draft</h1>
  <div class="sub">{DATE} &middot; branch <code>{BRANCH}</code></div>

  <div class="banner"><b>No defensible target this cycle.</b> No Anchorage AI founder,
  operator, municipal decision-maker, or research lead cleared the anti-puff gate for a
  specific decision made or owned in the last 30 days (window broadened to 45 days with the
  same result). Nothing shipped to LinkedIn this run.</div>

  <h2>Why nothing shipped</h2>
  <div class="note">{html.escape(note)}</div>
  <p style="font-size:12.5px;color:#666;">Decision window used: <b>{html.escape(window)}</b>
  (2026-05-11 through 2026-06-25 after broadening).</p>

  <h2>Candidates evaluated and dropped</h2>
  <ul>{drop_items}</ul>

  <h2>Editor's note</h2>
  <div class="note">{html.escape(editor_note)}</div>

  <div class="foot">Generated {dt.datetime.utcnow().isoformat()}Z by the Alaska.Ai Anchorage Desk routine.</div>
</div></body></html>"""

payload = {"subject": SUBJECT, "to": "me", "html_body": body}
Path("out/gmail_payload.json").write_text(json.dumps(payload))
print("subject:", SUBJECT)
print("html_body bytes:", len(body))
print("dropped count:", len(dropped))
