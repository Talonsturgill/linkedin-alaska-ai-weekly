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
.imgurl{text-align:center;font-size:11px;color:#888;margin:-8px 0 18px;word-break:break-all;}
.imgurl a{color:#0a66c2;}
ul{padding-left:22px;} li{margin:4px 0;font-size:14px;}
table.score{width:100%;border-collapse:collapse;font-size:13px;}
table.score th,table.score td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;}
.foot{color:#888;font-size:11px;margin-top:22px;}
.flag{background:#fff4e5;border-left:3px solid #f0a500;padding:10px 12px;border-radius:4px;margin:14px 0;}
.no-target{background:#fef2f2;border-left:4px solid #ef4444;padding:14px 16px;border-radius:6px;margin:20px 0;font-size:15px;}
"""


def render(post_text, image_src, sources, score, date_str, branch,
           label="Weekly LinkedIn Recap", footer_label="Weekly LinkedIn",
           no_target=False, editor_note=""):
    # image_src: either "data:image/png;base64,..." or "https://..." or "" (no image)
    if image_src:
        # When the image is a hosted URL, surface it as visible, clickable text
        # below the embed so it is always accessible even if the client blocks
        # remote images. Base64 data URIs have no shareable URL, so skip the link.
        if image_src.startswith("http"):
            url_line = (
                f'<div class="imgurl">Image URL '
                f'<a href="{image_src}">{image_src}</a></div>'
            )
        else:
            url_line = ""
        img_block = (
            f'<div class="img"><img src="{image_src}" '
            f'alt="Alaska.Ai {label} image"/></div>{url_line}'
        )
    else:
        img_block = ""

    if no_target:
        post_block = """
  <div class="no-target">
    <b>No defensible target this cycle.</b> The mechanism-discovery scouts ran
    and the accuracy gate found no mechanism that cleared all seven gates.
    See the dropped mechanisms list below and the Editor&rsquo;s note for details.
  </div>"""
    else:
        post_block = f"""
  <h2>Copy this for LinkedIn</h2>
  <pre class="post">{post_text}</pre>"""

    src_items = "\n".join(
        f'<li><a href="{s["url"]}">{s.get("outlet", s["url"])}</a>'
        + (f' &mdash; {s.get("pub_date","")}' if s.get("pub_date") else "")
        + (f' &mdash; {s.get("story_title","")}' if s.get("story_title") else "")
        + "</li>"
        for s in sources.get("sources", [])
    ) if sources.get("sources") else "<li>No sources recorded.</li>"

    score_rows = "\n".join(
        f'<tr><td>{c["name"]}</td><td>{c["score"]}</td>'
        f'<td>{c["weight"]}</td><td>{c.get("notes","")}</td></tr>'
        for c in score.get("criteria", [])
    ) if score.get("criteria") else ""

    ship_flag = "" if score.get("ship") else (
        f'<div class="flag"><b>Below threshold.</b> Weakest: '
        f'{score.get("weakest_criterion","?")}. '
        f'Fix: {score.get("one_sentence_fix","?")}</div>'
    )

    score_section = f"""
  <h2>Editor&rsquo;s report card</h2>
  <table class="score">
    <tr><th>Criterion</th><th>Score</th><th>Weight</th><th>Notes</th></tr>
    {score_rows}
  </table>
  <p><b>Weighted total:</b> {score.get("weighted_total","N/A")} / 10 &middot;
     <b>Threshold:</b> {score.get("threshold","8.0")} &middot;
     <b>Ship:</b> {"yes" if score.get("ship") else "no &mdash; see flag above"}</p>
""" if score_rows else ""

    editor_section = f"""
  <h2>Editor&rsquo;s note</h2>
  <div class="flag">{editor_note}</div>
""" if editor_note else ""

    return f"""<!doctype html><html><head><style>{CSS}</style></head><body>
<div class="wrap">
  <h1>Alaska.Ai &mdash; {label} Draft</h1>
  <div class="sub">{date_str} &middot; branch <code>{branch}</code></div>
  {post_block}
  {img_block}
  {ship_flag}
  <h2>Sources</h2>
  <ul>{src_items}</ul>
  {score_section}
  {editor_section}
  <div class="foot">Generated {dt.datetime.utcnow().isoformat()}Z by the Alaska.Ai {footer_label} routine.</div>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--post-md",    default=None,   help="Path to final post markdown (omit for no-target)")
    ap.add_argument("--image",      default=None,   help="Path to PNG image file (base64 inline)")
    ap.add_argument("--image-url",  default=None,   help="Hosted image URL (takes precedence over --image)")
    ap.add_argument("--sources",    required=True)
    ap.add_argument("--score",      required=True)
    ap.add_argument("--date",       required=True)
    ap.add_argument("--branch",     required=True)
    ap.add_argument("--label",        default="Weekly LinkedIn Recap")
    ap.add_argument("--footer-label", default="Weekly LinkedIn")
    ap.add_argument("--no-target",  action="store_true", help="No mechanism shipped this cycle")
    ap.add_argument("--editor-note", default="",    help="Free-text editor's note for deviations")
    args = ap.parse_args()

    # Post text
    post_text = Path(args.post_md).read_text() if args.post_md else ""

    # Image source: hosted URL takes precedence; else base64 inline; else empty
    if args.image_url:
        image_src = args.image_url
    elif args.image:
        image_b64 = base64.b64encode(Path(args.image).read_bytes()).decode("ascii")
        image_src = f"data:image/png;base64,{image_b64}"
    else:
        image_src = ""

    sources = json.loads(Path(args.sources).read_text())
    score   = json.loads(Path(args.score).read_text())

    html_body = render(
        post_text, image_src, sources, score,
        args.date, args.branch, args.label, args.footer_label,
        no_target=args.no_target,
        editor_note=args.editor_note,
    )

    payload = {
        "subject": f"Alaska.Ai — {args.label} Draft — {args.date}",
        "to": "me",
        "html_body": html_body,
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
