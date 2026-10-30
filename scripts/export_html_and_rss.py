import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def markdown_to_html(md_text):
    """Converts the structured newsletter markdown into a responsive, clean HTML document."""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_table = False
    table_header = True

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                lang = stripped[3:].strip() or 'text'
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code_block = True
            continue

        if in_code_block:
            escaped = (
                line.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
            )
            html_lines.append(escaped)
            continue

        # Tables
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                # Separator line
                continue
            if not in_table:
                html_lines.append('<div class="table-container"><table>')
                in_table = True
                table_header = True

            tag = 'th' if table_header else 'td'
            row_html = '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
            html_lines.append(row_html)
            table_header = False
            continue
        elif in_table:
            html_lines.append('</table></div>')
            in_table = False

        # Dividers
        if stripped in ['---', '***']:
            html_lines.append('<hr />')
            continue

        # Paid subscriber badge
        if '<!-- PAID_SUBSCRIBERS_ONLY -->' in stripped:
            html_lines.append(
                '<div class="paid-divider">⭐ <strong>PAID SUBSCRIBERS ONLY DEEP-DIVE</strong></div>'
            )
            continue

        # Headings
        if stripped.startswith('# '):
            html_lines.append(f'<h1>{stripped[2:]}</h1>')
            continue
        if stripped.startswith('## '):
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
            continue
        if stripped.startswith('### '):
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
            continue

        # Blockquote
        if stripped.startswith('> '):
            html_lines.append(f'<blockquote>{stripped[2:]}</blockquote>')
            continue

        # Empty lines
        if not stripped:
            continue

        # Inline formatting: bold, italic, code, links
        formatted = stripped
        formatted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = re.sub(r'\*(.+?)\*', r'<em>\1</em>', formatted)
        formatted = re.sub(r'`(.+?)`', r'<code>\1</code>', formatted)
        formatted = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', formatted)

        html_lines.append(f'<p>{formatted}</p>')

    if in_table:
        html_lines.append('</table></div>')
    if in_code_block:
        html_lines.append('</code></pre>')

    body_content = '\n'.join(html_lines)

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Edge Systems & Micro-SaaS Report</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.65;
      color: #24292f;
      background: #f6f8fa;
      padding: 30px 15px;
      margin: 0;
    }}
    .email-wrapper {{
      max-width: 680px;
      margin: 0 auto;
      background: #ffffff;
      padding: 36px 32px;
      border-radius: 10px;
      border: 1px solid #d0d7de;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    h1 {{ color: #0969da; font-size: 26px; border-bottom: 2px solid #eaeef2; padding-bottom: 12px; margin-top: 0; }}
    h2 {{ color: #1f2328; font-size: 20px; margin-top: 28px; border-bottom: 1px solid #eaeef2; padding-bottom: 6px; }}
    h3 {{ color: #24292f; font-size: 16px; margin-top: 20px; }}
    p {{ margin: 14px 0; font-size: 15px; }}
    a {{ color: #0969da; text-decoration: none; font-weight: 500; }}
    a:hover {{ text-decoration: underline; }}
    code {{ background: #f6f8fa; color: #cf222e; padding: 2px 6px; border-radius: 4px; font-size: 85%; font-family: ui-monospace, SFMono-Regular, monospace; }}
    pre {{ background: #161b22; color: #e6edf3; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.45; }}
    pre code {{ color: inherit; background: transparent; padding: 0; }}
    blockquote {{ border-left: 4px solid #0969da; margin: 16px 0; padding: 8px 16px; color: #57606a; background: #f6f8fa; border-radius: 0 6px 6px 0; }}
    .table-container {{ overflow-x: auto; margin: 20px 0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ padding: 10px 12px; border: 1px solid #d0d7de; text-align: left; }}
    th {{ background: #f6f8fa; font-weight: 600; }}
    .paid-divider {{ background: #ddf4ff; color: #0969da; border: 1px solid #54aeff; padding: 12px; border-radius: 6px; text-align: center; font-size: 14px; margin: 28px 0; }}
    .footer {{ margin-top: 36px; padding-top: 20px; border-top: 1px solid #eaeef2; font-size: 13px; color: #57606a; text-align: center; }}
  </style>
</head>
<body>
  <div class="email-wrapper">
    {body_content}
    <div class="footer">
      <p>The Edge Systems & Micro-SaaS Report · Published weekly by Milind Chatrabhuji</p>
      <p><a href="https://github.com/MilindChatrabhuji/edgesaas-starter-kit">NexusPulse Edge Architecture</a> · <a href="https://github.com/MilindChatrabhuji/edge-systems-newsletter">Open Source Edition Feed</a></p>
    </div>
  </div>
</body>
</html>"""
    return template

def generate_rss_feed(editions, output_file="engines/newsletter-engine/data/editions/feed.xml"):
    """Generates standard RSS 2.0 feed for automated ingestion into Substack or RSS readers."""
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    title = ET.SubElement(channel, 'title')
    title.text = 'The Edge Systems & Micro-SaaS Report'

    link = ET.SubElement(channel, 'link')
    link.text = 'https://github.com/MilindChatrabhuji/edge-systems-newsletter'

    desc = ET.SubElement(channel, 'description')
    desc.text = 'Weekly high-signal intelligence for edge architecture, Cloudflare Workers, and open-source bounties.'

    for ed in editions:
        item = ET.SubElement(channel, 'item')
        item_title = ET.SubElement(item, 'title')
        item_title.text = ed.get('title', 'Weekly Edition')

        item_link = ET.SubElement(item, 'link')
        item_link.text = ed.get('url', 'https://github.com/MilindChatrabhuji/edge-systems-newsletter')

        item_desc = ET.SubElement(item, 'description')
        item_desc.text = ed.get('summary', '')

        pubDate = ET.SubElement(item, 'pubDate')
        pubDate.text = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

    tree = ET.ElementTree(rss)
    ET.indent(tree, space='  ')
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Generated RSS 2.0 Feed -> {output_file}")
    return output_file

def export_all():
    editions_dir = "engines/newsletter-engine/data/editions"
    md_file = os.path.join(editions_dir, "edition_42.md")
    html_file = os.path.join(editions_dir, "edition_42.html")

    if os.path.exists(md_file):
        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()
        html = markdown_to_html(md_text)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated Responsive HTML Edition -> {html_file}")

    # Generate RSS feed
    editions = [
        {
            "title": "Edition #42: Zero-Cold-Start Micro-SaaS & V8 Isolate Unit Economics",
            "url": "https://github.com/MilindChatrabhuji/edge-systems-newsletter",
            "summary": "Benchmarking Cloudflare Workers KV sliding window rate limiting, Web Crypto HMAC-SHA256 signatures, and $150k in open AI/Web3 developer bounties."
        }
    ]
    generate_rss_feed(editions)

if __name__ == "__main__":
    export_all()
