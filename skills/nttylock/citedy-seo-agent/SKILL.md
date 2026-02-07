---
name: Citedy SEO Agent
description: Connect your AI agent to Citedy's SEO content platform — scout trending topics on X/Reddit, find content gaps, analyze competitors, and generate SEO-optimized articles automatically.
---

# Citedy AI Agent Integration

Connect your AI agent to [Citedy](https://www.citedy.com) — an AI-powered SEO content platform.

## What You Can Do

- **Scout X/Twitter** — Find trending topics in any niche (fast/ultimate modes)
- **Scout Reddit** — Discover discussions in relevant subreddits
- **Content Gaps** — Analyze competitors to find content opportunities
- **Competitor Analysis** — Deep-dive into competitor strategies
- **Autopilot** — Generate full SEO-optimized articles (500–2500 words)

## Getting Started

### Step 1: Register Your Agent

```bash
curl -X POST https://citedy.com/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "YourAgentName"}'
```

**Response:**

```json
{
  "pending_id": "abc123def456",
  "approval_url": "https://citedy.com/approve-agent/abc123def456",
  "expires_in": 3600,
  "status": "awaiting_approval"
}
```

**IMPORTANT:** You will NOT receive an API key in this response!

### Step 2: Human Approval

Ask the human to:

1. Open the `approval_url` in their browser
2. Log in to Citedy (if not already logged in)
3. Click [Approve] to authorize your agent
4. Copy the API key that appears
5. Send the API key back to you

### Step 3: Start Using the API

Include the API key in all requests:

```bash
curl https://citedy.com/api/agent/me \
  -H "Authorization: Bearer citedy_agent_xxxxx..."
```

## Available Actions

### Scout Topics on X (Twitter)

```bash
curl -X POST https://citedy.com/api/agent/scout/x \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI content marketing challenges",
    "mode": "fast",
    "limit": 20
  }'
```

**Modes:** `fast` (35 credits), `ultimate` (70 credits)

### Scout Topics on Reddit

```bash
curl -X POST https://citedy.com/api/agent/scout/reddit \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "subreddits": ["marketing", "SEO", "content_marketing"],
    "query": "content strategy problems",
    "limit": 20
  }'
```

**Cost:** 30 credits

### Get Content Gaps

```bash
curl https://citedy.com/api/agent/gaps \
  -H "Authorization: Bearer {your_api_key}"
```

**Cost:** 0 credits (free read)

### Generate Content Gaps

```bash
curl -X POST https://citedy.com/api/agent/gaps/generate \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "competitor_urls": [
      "https://competitor1.com",
      "https://competitor2.com"
    ]
  }'
```

**Cost:** 40 credits. Async — poll `/api/agent/gaps-status/{id}` for completion.

### Discover Competitors

```bash
curl -X POST https://citedy.com/api/agent/competitors/discover \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["ai content marketing", "automated blogging"]
  }'
```

**Cost:** 20 credits

### Analyze Competitor

```bash
curl -X POST https://citedy.com/api/agent/competitors/scout \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "https://competitor.com",
    "mode": "fast"
  }'
```

**Modes:** `fast` (25 credits), `ultimate` (50 credits)

### Generate Article (Autopilot)

```bash
curl -X POST https://citedy.com/api/agent/autopilot \
  -H "Authorization: Bearer {your_api_key}" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How to Use AI for Content Marketing in 2026",
    "language": "en",
    "size": "standard"
  }'
```

**Sizes:** `mini` (15 cr, ~500w), `standard` (20 cr, ~1000w), `full` (33 cr, ~1500w), `pillar` (48 cr, ~2500w)

Async — poll `/api/agent/autopilot/{id}` for completion.

### List Generated Articles

```bash
curl https://citedy.com/api/agent/articles \
  -H "Authorization: Bearer {your_api_key}"
```

**Cost:** 0 credits (free read)

### Check Your Status

```bash
curl https://citedy.com/api/agent/me \
  -H "Authorization: Bearer {your_api_key}"
```

**Tip:** Call this every 4+ hours as a heartbeat to keep your agent active.

## Rate Limits

| Limit Type   | Rate               | Scope                   |
| ------------ | ------------------ | ----------------------- |
| General      | 60 requests/minute | Per agent               |
| Scout        | 10 requests/hour   | X + Reddit combined     |
| Gaps         | 10 requests/hour   | Get + Generate combined |
| Registration | 10 requests/hour   | Per IP                  |

429 responses include `retry_after`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers.

## Credits

All actions consume credits from the account owner's balance. **1 credit = $0.01 USD.**

| Action                        | Cost       |
| ----------------------------- | ---------- |
| X-Scout Fast                  | 35 credits |
| X-Scout Ultimate              | 70 credits |
| Reddit Scout                  | 30 credits |
| Content Gaps (read)           | 0 credits  |
| Content Gaps (generate)       | 40 credits |
| Discover Competitors          | 20 credits |
| Analyze Competitor (fast)     | 25 credits |
| Analyze Competitor (ultimate) | 50 credits |
| Autopilot Mini                | 15 credits |
| Autopilot Standard            | 20 credits |
| Autopilot Full                | 33 credits |
| Autopilot Pillar              | 48 credits |

Check balance: `GET /api/agent/me`

## Error Codes

| Status | Meaning                    |
| ------ | -------------------------- |
| 401    | Invalid or missing API key |
| 402    | Insufficient credits       |
| 403    | Agent paused/revoked       |
| 429    | Rate limit exceeded        |
| 500    | Server error               |

## Best Practices

1. **Heartbeat**: Call `/api/agent/me` every 4-6 hours to stay active
2. **Check Balance**: Verify credits before expensive operations
3. **Handle Rate Limits**: Respect `Retry-After` headers
4. **Async Operations**: Poll status endpoints for long-running tasks
5. **Error Handling**: Gracefully handle 4xx/5xx responses

## Support

- Full docs: https://citedy.com/skill.md
- Website: https://www.citedy.com
- Help: https://citedy.com/help

---

_Citedy SEO/GEO Agent Platform v1.0_
