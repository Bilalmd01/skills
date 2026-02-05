---
name: google-search-console
description: |
  Google Search Console API integration with managed OAuth. Query search analytics, manage sitemaps, and monitor site performance. Use this skill when users want to access Search Console data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
---

# Google Search Console

Access the Google Search Console API with managed OAuth authentication. Query search analytics, manage sitemaps, and monitor site performance in Google Search.

## Quick Start

```bash
# List sites
curl -s -X GET "https://gateway.maton.ai/google-search-console/webmasters/v3/sites" -H "Authorization: Bearer $MATON_API_KEY"
```

## Base URL

```
https://gateway.maton.ai/google-search-console/{native-api-path}
```

Replace `{native-api-path}` with the actual Google Search Console API endpoint path. The gateway proxies requests to `www.googleapis.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Google OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
curl -s -X GET "https://ctrl.maton.ai/connections?app=google-search-console&status=ACTIVE" -H "Authorization: Bearer $MATON_API_KEY"
```

### Create Connection

```bash
curl -s -X POST "https://ctrl.maton.ai/connections" -H "Content-Type: application/json" -H "Authorization: Bearer $MATON_API_KEY" -d '{"app": "google-search-console"}'
```

### Get Connection

```bash
curl -s -X GET "https://ctrl.maton.ai/connections/{connection_id}" -H "Authorization: Bearer $MATON_API_KEY"
```

**Response:**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-search-console",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE "https://ctrl.maton.ai/connections/{connection_id}" -H "Authorization: Bearer $MATON_API_KEY"
```

### Specifying Connection

If you have multiple Google Search Console connections, specify which one to use with the `Maton-Connection` header:

```bash
curl -s -X GET "https://gateway.maton.ai/google-search-console/webmasters/v3/sites" -H "Authorization: Bearer $MATON_API_KEY" -H "Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80"
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Sites

```bash
GET /google-search-console/webmasters/v3/sites
GET /google-search-console/webmasters/v3/sites/{siteUrl}
```

Note: Site URL must be URL-encoded (e.g., `https%3A%2F%2Fexample.com%2F`)

### Search Analytics

```bash
POST /google-search-console/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
Content-Type: application/json

{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "rowLimit": 100
}
```

### Sitemaps

```bash
GET /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps
PUT /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
DELETE /google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
```

## Search Analytics Examples

### Top Queries

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "rowLimit": 25
}
```

### Top Pages

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["page"],
  "rowLimit": 25
}
```

### Device Breakdown

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["device"],
  "rowLimit": 10
}
```

### Daily Performance

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["date"],
  "rowLimit": 31
}
```

### Filtered Query

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "query",
      "operator": "contains",
      "expression": "keyword"
    }]
  }],
  "rowLimit": 100
}
```

## Dimensions

- `query` - Search query
- `page` - Page URL
- `country` - Country code
- `device` - DESKTOP, MOBILE, TABLET
- `date` - Date

## Metrics (returned automatically)

- `clicks` - Number of clicks
- `impressions` - Number of impressions
- `ctr` - Click-through rate
- `position` - Average position

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-search-console/webmasters/v3/sites/https%3A%2F%2Fexample.com/searchAnalytics/query',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      startDate: '2024-01-01',
      endDate: '2024-01-31',
      dimensions: ['query'],
      rowLimit: 25
    })
  }
);
```

### Python

```python
import os
import requests
from urllib.parse import quote

site_url = quote('https://example.com', safe='')
response = requests.post(
    f'https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{site_url}/searchAnalytics/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'startDate': '2024-01-01',
        'endDate': '2024-01-31',
        'dimensions': ['query'],
        'rowLimit': 25
    }
)
```

## Notes

- Site URLs must be URL-encoded in the path
- Date range limited to 16 months
- Maximum 25,000 rows per request
- Use `startRow` for pagination
- Data has 2-3 day delay
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Search Console connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Search Console API |

## Resources

- [Search Console API Reference](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [List Sites](https://developers.google.com/webmaster-tools/v1/sites/list)
- [Search Analytics](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Sitemaps](https://developers.google.com/webmaster-tools/v1/sitemaps)
