# The Edge Systems & Micro-SaaS Report

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Automated Weekly Cron](https://img.shields.io/badge/Cadence-Every%20Monday-brightgreen.svg)]()
[![RSS Feed](https://img.shields.io/badge/RSS-Feed%20Active-orange.svg)](https://raw.githubusercontent.com/MilindChatrabhuji/edge-systems-newsletter/master/data/editions/feed.xml)

A high-signal, programmatic weekly newsletter engineered for indie hackers, systems developers, and micro-SaaS founders building zero-cold-start applications on Cloudflare Workers, Hono, and V8 Isolates.

![NexusPulse Banner](https://raw.githubusercontent.com/MilindChatrabhuji/edgesaas-starter-kit/main/assets/edgesaas-banner-hero.svg)

---

## 📅 What Subscribers Receive

- **⚡ Executive Architecture Briefing**: What shipped in edge runtimes, WASM engines, and V8 isolate benchmarks.
- **💰 Top Funded Open-Source Cash Bounties ($100–$1,000+)**: Direct links to funded issues across Algora, Polar, and GitHub.
- **📊 Infrastructure Cost Benchmarks**: Traditional VPS / Docker container costs vs. $0.00 idle edge isolate execution.
- **🔒 Paid Subscriber Deep-Dive ($7/mo or $60/yr)**: Audited code implementations (Web Crypto HMAC webhooks, distributed KV rate limiting, Stripe edge integration) and commercial boilerplates.

---

## 🚀 Live Editions & RSS Feed

- **Latest Edition (#42)**:
  - [Read Markdown Edition](https://github.com/MilindChatrabhuji/edge-systems-newsletter/blob/master/data/editions/edition_42.md)
  - [View Standalone Responsive HTML](https://htmlpreview.github.io/?https://github.com/MilindChatrabhuji/edge-systems-newsletter/blob/master/data/editions/edition_42.html)
- **Live RSS 2.0 Feed**:  
  `https://raw.githubusercontent.com/MilindChatrabhuji/edge-systems-newsletter/master/data/editions/feed.xml`

---

## 🛠️ Automated Pipeline & Self-Publishing

The entire newsletter is produced via automated Python scripts and scheduled via GitHub Actions:

```bash
# 1. Scrape latest edge intelligence & funded bounties
python scripts/scrape_weekly_intelligence.py

# 2. Build edition Markdown
python scripts/generate_edition.py

# 3. Export responsive email HTML and RSS 2.0 feed
python scripts/export_html_and_rss.py

# 4. Optional: Dispatch directly to Beehiiv API
python scripts/publish_to_platform.py --api-key $BEEHIIV_KEY --pub-id $BEEHIIV_PUB
```

---

## 💳 Monetization & Bank Settlement

Substack and Beehiiv handle global credit card processing natively via Stripe and auto-sweep monthly recurring subscription payouts in INR directly into your verified bank account.

Commercial templates linked within the newsletter direct to the [NexusPulse EdgeSaaS Starter Kit](https://github.com/MilindChatrabhuji/edgesaas-starter-kit).

## License

MIT License. Curated & maintained by [Milind Chatrabhuji](https://github.com/MilindChatrabhuji).
