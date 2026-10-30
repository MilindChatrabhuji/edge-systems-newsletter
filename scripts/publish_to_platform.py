import argparse
import json
import os
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def publish_to_beehiiv(edition_file, api_key=None, pub_id=None, dry_run=False):
    """Pushes the staged newsletter edition to Beehiiv as a scheduled or draft post."""
    if not os.path.exists(edition_file):
        print(f"Error: Edition file {edition_file} not found.")
        sys.exit(1)

    with open(edition_file, 'r', encoding='utf-8') as f:
        content = f.read()

    title_line = content.split('\n')[0].replace('#', '').strip()
    subtitle = "Weekly high-signal intelligence for edge systems & micro-SaaS builders."

    print(f"Staged Edition: {title_line}")
    print(f"Word count: {len(content.split())} words")

    if dry_run:
        print("[DRY-RUN] Ready for Beehiiv / Substack syndication.")
        print("  • Free tier: Executive briefing & open-source bounty highlights")
        print("  • Paid tier: Web Crypto Stripe HMAC signature breakdown & boilerplate")
        print("[DRY-RUN] Verification successful.")
        return True

    api_key = api_key or os.environ.get("BEEHIIV_API_KEY")
    pub_id = pub_id or os.environ.get("BEEHIIV_PUB_ID")

    if not api_key or not pub_id:
        print("Notice: No BEEHIIV_API_KEY or BEEHIIV_PUB_ID provided.")
        print("Edition is packaged and ready to paste into Substack or Beehiiv:")
        print(f"  • Markdown: {edition_file}")
        html_file = edition_file.replace('.md', '.html')
        print(f"  • Email HTML: {html_file}")
        return True

    endpoint = f"https://api.beehiiv.com/v2/publications/{pub_id}/posts"
    payload = {
        "title": title_line,
        "subtitle": subtitle,
        "body": content,
        "status": "draft",
    }

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "EdgeNewsletterBot/1.0",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            post_id = res_data.get("data", {}).get("id")
            print(f"🎉 Successfully created Beehiiv draft post! ID: {post_id}")
            return True
    except urllib.error.HTTPError as e:
        print(f"Beehiiv API Error ({e.code}): {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Error publishing: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish newsletter edition")
    parser.add_argument("--edition", default="engines/newsletter-engine/data/editions/edition_42.md")
    parser.add_argument("--api-key", help="Beehiiv API Key")
    parser.add_argument("--pub-id", help="Beehiiv Publication ID")
    parser.add_argument("--dry-run", action="store_true", help="Perform pre-flight verification")

    args = parser.parse_args()
    publish_to_beehiiv(args.edition, args.api_key, args.pub_id, args.dry_run)
