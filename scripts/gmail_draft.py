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
.editor-note{background:#f0f4ff;border-left:3px solid #4a6cf7;padding:10px 12px;border-radius:4px;margin:14px 0;font-size:13px;line-height:1.6;}
.no-target-banner{background:#fff0f0;border-left:4px solid #e53e3e;padding:14px 18px;border-radius:4px;margin:14px 0;font-size:15px;font-weight:bold;}
"""


def render(post_text, image_src, sources, score, date_str, branch,
           label="Weekly LinkedIn Recap", footer_label="Weekly LinkedIn",
           editor_note=None, no_target=False, image_is_url=False):
    src_items = "\n".join(
        f'<li><a href="{s["url"]}">{s["outlet"]}</a> &mdash; '
        f'{s.get("pub_date","")} &mdash; {s.get("story_title","")}</li>'
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
    if image_is_url:
        img_tag = f'<img src="{image_src}" alt="Alaska.Ai weekly image"/>'
    elif image_src:
        img_tag = f'<img src="data:image/png;base64,{image_src}" alt="Alaska.Ai weekly image"/>'
    else:
        img_tag = ""

    no_target_banner = ""
    if no_target:
        no_target_banner = (
            '<div class="no-target-banner">NO TARGET THIS CYCLE &mdash; '
            'all 7 candidates dropped on the anti-confabulation gate. '
            'No post ships this week.</div>'
        )

    post_section = ""
    if post_text:
        post_section = f'<h2>Copy this for LinkedIn</h2><pre class="post">{post_text}</pre>'

    editor_note_html = ""
    if editor_note:
        formatted = editor_note.replace("\n", "<br>")
        editor_note_html = (
            f'<div class="editor-note"><b>Editor note:</b><br>{formatted}</div>'
        )

    sources_heading = "Sources investigated" if no_target else "Sources"

    return f"""<!doctype html><html><head><style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Alaska.Ai &mdash; {label} Draft</h1>
  <div class="sub">{date_str} &middot; branch <code>{branch}</code></div>
  {no_target_banner}
  {post_section}
  <div class="img">{img_tag}</div>
  {ship_flag}
  {editor_note_html}
  <h2>{sources_heading}</h2>
  <ul>{src_items}</ul>
  <h2>Editor's report card</h2>
  <table class="score">
    <tr><th>Criterion</th><th>Score</th><th>Weight</th><th>Notes</th></tr>
    {score_rows}
  </table>
  <p><b>Weighted total:</b> {score.get("weighted_total","?")} / 10 &middot;
     <b>Threshold:</b> {score.get("threshold","?")} &middot;
     <b>Ship:</b> {"yes" if score.get("ship") else "no &mdash; see flag above"}</p>
  <div class="foot">Generated {dt.datetime.utcnow().isoformat()}Z by the Alaska.Ai {footer_label} routine.</div>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-md")
    ap.add_argument("--image")
    ap.add_argument("--image-url")
    ap.add_argument("--no-target", action="store_true")
    ap.add_argument("--editor-note", default="")
    ap.add_argument("--to", default="talon.sturgill@gmail.com")
    ap.add_argument("--sources", required=True)
    ap.add_argument("--score",   required=True)
    ap.add_argument("--date",    required=True)
    ap.add_argument("--branch",  required=True)
    ap.add_argument("--label",        default="Weekly LinkedIn Recap")
    ap.add_argument("--footer-label", default="Weekly LinkedIn")
    args = ap.parse_args()

    post_text = Path(args.post_md).read_text() if args.post_md else ""

    if args.image_url:
        image_src = args.image_url
        image_is_url = True
    elif args.image:
        image_src = base64.b64encode(Path(args.image).read_bytes()).decode("ascii")
        image_is_url = False
    else:
        image_src = ""
        image_is_url = False

    sources = json.loads(Path(args.sources).read_text())
    score = json.loads(Path(args.score).read_text())

    display_label = args.label
    no_target_suffix = " — No Target" if args.no_target else ""
    subject = f"Alaska.Ai — {args.label}{no_target_suffix} — {args.date}"

    payload = {
        "subject": subject,
        "to": args.to,
        "html_body": render(
            post_text, image_src, sources, score, args.date, args.branch,
            display_label, args.footer_label,
            editor_note=args.editor_note,
            no_target=args.no_target,
            image_is_url=image_is_url,
        ),
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
