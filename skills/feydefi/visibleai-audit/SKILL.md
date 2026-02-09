---
name: visibleai-audit
description: Audit brand visibility across AI search engines (ChatGPT, Perplexity, Gemini). Get a GEO score with actionable recommendations.
version: 1.0.0
---

# VisibleAI Audit

Check how visible any brand is across AI search engines. Returns a GEO (Generative Engine Optimization) score with engine-by-engine breakdown and recommendations.

## Usage

Run a GEO audit via the VisibleAI API:

```bash
curl -X POST https://visibleai.space/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"brand": "BRAND_NAME", "website": "https://example.com", "industry": "INDUSTRY"}'
```

Or use the script:

```bash
python3 scripts/audit.py "Brand Name" --website "https://example.com" --industry "SaaS"
```

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand or company name |
| website | string | No | Website URL to analyze |
| industry | string | No | Industry or vertical |
| competitors | string[] | No | Up to 5 competitor names |

## Response

Returns JSON with:
- `overall_score` (0-100) and letter `grade`
- Per-engine scores (Gemini, Perplexity)
- Category breakdown (discovery, branded, comparison)
- Site analysis (schema markup, meta tags)
- Actionable `recommendations`

## Free Tier

1 audit per day at visibleai.space — no signup needed.

## API (Pay-per-query)

$1 per audit via x402 protocol (USDC on Base network). No API keys required.

## Learn More

- Website: https://visibleai.space
- API Docs: https://visibleai.space/api-docs
- Courses: https://visibleai.space/courses
