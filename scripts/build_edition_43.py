import os
import sys

sys.path.insert(0, os.path.abspath("engines/newsletter-engine/scripts"))
from scrape_edition_43 import scrape_edition_43
from generate_edition import generate_newsletter_markdown
from export_html_and_rss import markdown_to_html, generate_rss_feed

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def build_edition_43():
    intel = scrape_edition_43()
    md_content = generate_newsletter_markdown(intel)
    
    editions_dir = "engines/newsletter-engine/data/editions"
    os.makedirs(editions_dir, exist_ok=True)
    
    md_file = os.path.join(editions_dir, "edition_43.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Generated Edition #43 Markdown -> {md_file}")

    # Generate HTML
    html_content = markdown_to_html(md_content)
    html_file = os.path.join(editions_dir, "edition_43.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Edition #43 Responsive HTML -> {html_file}")

    # Update RSS feed with both editions
    editions = [
        {
            "title": "Edition #43: WASM on V8 Isolates vs. Traditional Microservices & API Governance",
            "url": "https://github.com/MilindChatrabhuji/edge-systems-newsletter/blob/master/data/editions/edition_43.md",
            "summary": "Zero-dependency OpenAPI AST diffing, Telegram Stars (XTR) in-app checkout, and Hugging Face fine-tuning dataset benchmarks."
        },
        {
            "title": "Edition #42: Zero-Cold-Start Micro-SaaS & V8 Isolate Unit Economics",
            "url": "https://github.com/MilindChatrabhuji/edge-systems-newsletter/blob/master/data/editions/edition_42.md",
            "summary": "Benchmarking Cloudflare Workers KV sliding window rate limiting, Web Crypto HMAC-SHA256 signatures, and $150k in open AI/Web3 developer bounties."
        }
    ]
    rss_file = os.path.join(editions_dir, "feed.xml")
    generate_rss_feed(editions, output_file=rss_file)
    print("Updated multi-edition RSS 2.0 Feed successfully!")

if __name__ == "__main__":
    build_edition_43()
