import argparse
import base64
import datetime as dt
import json
from pathlib import Path

CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1a1a1a;background:#fafafa;margin:0;padding:24px;}
.wrap{max-width:720px;margin:0 auto;background:#fff;border:1px solid #e5e5e5;border-radius:12px;padding:28px;}
h1{font-size:22px;margin:0 0 4px;}
.sub{color:#666;font-size:13px;margin-bottom:24px;}
h2{font-size:16px;margin-top:28px;border-bottom:1px solid #eee;padding-bottom:6px;}
pre.post{white-space:pre-wrap;background:#f6f6f6;padding:16px;border-radius:8px;font-family:ui-monospace,Menlo,monospace;font-size:14px;line-height:1.5;}
.img{text-align:center;margin:18px 0;}
.img img{max-width:100%;height:auto;border-radius:8px;border:1px solid #e5e5e5;}
ul{padding-left:22px;} li{margin:4px 0;font-size:14px;}
table.score{width:100%;border-collapse:collapse;font-size:13px;}
table.score th,table.score td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;}
.foot{color:#888;font-size:11px;margin-top:22px;}
.flag{background:#fff4e5;border-left:3px solid #f0a500;padding:10px 12px;border-radius:4px;margin:14px 0;}
.notes{background:#f0f7ff;border-left:3px solid #3b82f6;padding:10px 12px;border-radius:4px;margin:14px 0;font-size:13px;}
"""


def render(post_text, image_b64, sources, score, date_str, branch, label, footer_label, editor_notes):
    src_items = "\n".join(
        f'<li><a href="{s["url"]}">{s.get("outlet", s["url"])}</a>'
        + (f' &mdash; {s["pub_date"]}' if s.get("pub_date") else "")
        + (f' &mdash; {s["story_title"]}' if s.get("story_title") else "")
        + "</li>"
        for s in sources.get("sources", [])
    )
    score_rows = "\n".join(
        f'<tr><td>{c["name"]}</td><td>{c["score"]}</td>'
        f'<td>{c["weight"]}</td><td>{c.get("notes","")}</td></tr>'
        for c in score.get("criteria", [])
    )
    ship_flag = "" if score.get("ship") else (
        f'<div class="flag"><b>Below threshold.</b> Weakest: '
        f'{score.get("weakest_criterion","?")}. '
        f'Fix: {score.get("one_sentence_fix","?")}</div>'
    )
    notes_block = (
        f'<h2>Editor\'s note</h2><div class="notes">{editor_notes}</div>'
        if editor_notes else ""
    )
    image_block = (
        f'<div class="img"><img src="{image_b64}" alt="Alaska.Ai post image"/></div>'
        if image_b64 else ""
    )
    return f"""<!doctype html><html><head><style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Alaska.Ai &mdash; {label} Draft</h1>
  <div class="sub">{date_str} &middot; branch <code>{branch}</code></div>
  <h2>Copy this for LinkedIn</h2>
  <pre class="post">{post_text}</pre>
  {image_block}
  {ship_flag}
  <h2>Sources</h2>
  <ul>{src_items}</ul>
  <h2>Score report</h2>
  <table class="score">
    <tr><th>Criterion</th><th>Score</th><th>Weight</th><th>Notes</th></tr>
    {score_rows}
  </table>
  <p><b>Weighted total:</b> {score.get("weighted_total","?")} / 10 &middot;
     <b>Threshold:</b> {score.get("threshold","?")} &middot;
     <b>Ship:</b> {"yes" if score.get("ship") else "no &mdash; see flag above"}</p>
  {notes_block}
  <div class="foot">Generated {dt.datetime.utcnow().isoformat()}Z &mdash; {footer_label} &mdash; branch <code>{branch}</code></div>
</div></body></html>"""


def render_no_target(validation_note, dropped_claims, date_str, branch, label, footer_label, editor_notes):
    dropped_items = "\n".join(
        f'<li><b>{c.get("claim_verbatim","(unknown)")}</b> &mdash; '
        f'Dropped: {c.get("drop_reason","unspecified")}</li>'
        for c in (dropped_claims or [])
    )
    notes_block = (
        f'<h2>Editor\'s note</h2><div class="notes">{editor_notes}</div>'
        if editor_notes else ""
    )
    return f"""<!doctype html><html><head><style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Alaska.Ai &mdash; {label} Draft</h1>
  <div class="sub">{date_str} &middot; branch <code>{branch}</code></div>
  <div class="flag"><b>No defensible target this cycle.</b><br>{validation_note}</div>
  <h2>Dropped claims</h2>
  <ul>{dropped_items}</ul>
  {notes_block}
  <div class="foot">Generated {dt.datetime.utcnow().isoformat()}Z &mdash; {footer_label} &mdash; branch <code>{branch}</code></div>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-md",       required=False, default=None)
    ap.add_argument("--image",         required=False, default=None)
    ap.add_argument("--sources",       required=True)
    ap.add_argument("--score",         required=False, default=None)
    ap.add_argument("--date",          required=True)
    ap.add_argument("--branch",        required=True)
    ap.add_argument("--label",         default="Weekly LinkedIn Recap")
    ap.add_argument("--footer-label",  default="Weekly Brief")
    ap.add_argument("--editor-notes",  default=None,
                    help="Path to a plain-text file with editor/process notes, or inline text.")
    ap.add_argument("--no-target",     action="store_true",
                    help="Build a no-target email from sources JSON (requires no-target fields in sources JSON).")
    args = ap.parse_args()

    sources = json.loads(Path(args.sources).read_text())
    editor_notes = ""
    if args.editor_notes:
        p = Path(args.editor_notes)
        editor_notes = p.read_text() if p.exists() else args.editor_notes

    subject = f"Alaska.Ai — {args.label} Draft — {args.date}"

    if args.no_target or sources.get("no_target_this_cycle"):
        html_body = render_no_target(
            validation_note=sources.get("_validation_note", "Validator returned no defensible target."),
            dropped_claims=sources.get("dropped_claims", []),
            date_str=args.date,
            branch=args.branch,
            label=args.label,
            footer_label=args.footer_label,
            editor_notes=editor_notes,
        )
    else:
        post_text = Path(args.post_md).read_text() if args.post_md else ""
        image_b64 = ""
        if args.image:
            img_path = Path(args.image)
            if img_path.exists():
                raw = base64.b64encode(img_path.read_bytes()).decode("ascii")
                image_b64 = f"data:image/png;base64,{raw}"
            else:
                image_b64 = args.image  # treat as already-resolved URL
        score = json.loads(Path(args.score).read_text()) if args.score else {}
        html_body = render(
            post_text=post_text,
            image_b64=image_b64,
            sources=sources,
            score=score,
            date_str=args.date,
            branch=args.branch,
            label=args.label,
            footer_label=args.footer_label,
            editor_notes=editor_notes,
        )

    payload = {
        "subject": subject,
        "to": "",
        "html_body": html_body,
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
