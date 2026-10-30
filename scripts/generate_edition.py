import os
import sys
import json
from scrape_weekly_intelligence import scrape_weekly_intelligence

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def generate_newsletter_markdown(intel=None):
    if intel is None:
        intel = scrape_weekly_intelligence()

    md = []
    md.append(f"# The Edge Systems & Micro-SaaS Report — Edition #{intel['edition_number']}")
    md.append(f"**Date**: {intel['date']} | **Author**: Milind Chatrabhuji\n")
    md.append(f"### This Week's Focus: *{intel['theme']}*\n")
    md.append("Welcome back to the weekly intelligence report for engineers, indie founders, and edge architects. Today we break down how zero-idle-cost edge architecture is reshaping the unit economics of SaaS development.\n")

    md.append("## ⚡ Executive Briefing (Key Developments)\n")
    for item in intel["key_developments"]:
        md.append(f"### [{item['tag']}] {item['headline']}")
        md.append(f"{item['summary']}\n")

    md.append("## 💰 Top Funded Cash Bounties of the Week ($100–$1,000+)\n")
    md.append("| Repository | Task / Feature | Bounty Value |")
    md.append("| :--- | :--- | :--- |")
    for b in intel["top_bounties"]:
        md.append(f"| `{b['repo']}` | {b['title']} | **{b['reward']}** |")
    md.append("")

    md.append("## 📊 Architecture Benchmark: Traditional VPS vs. V8 Edge\n")
    md.append("| Metric | Traditional VPS / Docker | Edge Micro-SaaS (Cloudflare Workers) |")
    md.append("| :--- | :--- | :--- |")
    dims = intel["benchmark_comparison"]["dimensions"]
    vps = intel["benchmark_comparison"]["vps"]
    edge = intel["benchmark_comparison"]["edge"]
    for i in range(len(dims)):
        md.append(f"| **{dims[i]}** | {vps[i]} | **{edge[i]}** |")
    md.append("")

    # Paid Subscriber Divider
    md.append("---\n")
    md.append("<!-- PAID_SUBSCRIBERS_ONLY -->")
    md.append("## 🔒 Paid Subscriber Deep-Dive: Zero-Cold-Start Stripe Webhooks with Web Crypto\n")
    md.append("> *This section, along with complete production boilerplate repositories and raw benchmark CSV files, is available to paid subscribers ($7/month or $60/year).*\n")
    md.append("Traditional Node.js Stripe webhooks rely on `stripe-node` and Node `crypto.createHmac`. On V8 Isolates, importing Node crypto polyfills adds 300KB+ to the worker bundle.\n")
    md.append("Here is the audited, zero-dependency Web Crypto implementation using `crypto.subtle`:\n")
    md.append("```typescript")
    md.append("export async function verifyStripeSignature(payload: string, header: string, secret: string): Promise<boolean> {")
    md.append("  const parts = header.split(',');")
    md.append("  let t = '', v1 = '';")
    md.append("  for (const p of parts) {")
    md.append("    const [k, v] = p.split('=');")
    md.append("    if (k.trim() === 't') t = v.trim();")
    md.append("    if (k.trim() === 'v1') v1 = v.trim();")
    md.append("  }")
    md.append("  if (!t || !v1) return false;")
    md.append("  const encoder = new TextEncoder();")
    md.append("  const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);")
    md.append("  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(`${t}.${payload}`));")
    md.append("  const hex = Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');")
    md.append("  return hex === v1;")
    md.append("}")
    md.append("```\n")
    md.append("👉 **[Clone & Deploy Complete Production Starter Kit](https://github.com/MilindChatrabhuji/edgesaas-starter-kit)**\n")

    return "\n".join(md)

def build_edition_file(output_dir="engines/newsletter-engine/data/editions"):
    os.makedirs(output_dir, exist_ok=True)
    intel = scrape_weekly_intelligence()
    content = generate_newsletter_markdown(intel)
    filename = os.path.join(output_dir, f"edition_{intel['edition_number']}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated newsletter edition -> {filename}")
    return filename

if __name__ == "__main__":
    build_edition_file()
