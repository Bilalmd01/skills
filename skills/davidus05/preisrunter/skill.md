---
name: Preisrunter Grocery Search
description: Search and compare Austrian and German grocery prices via the Preisrunter API wrapper and CLI.
homepage: https://github.com/preisrunter/preisrunter-cli
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["curl","jq","node"],"env":[]}}}
---

# Preisrunter Skill

Search and compare grocery prices from Preisrunter (Austria + Germany).  
This skill is optimized for bots/agents and supports both **curl** and the **preisrunter-cli**.

## Setup

### Option A: Use the API wrapper (no install)
No authentication required. Uses the public wrapper endpoint:

- Base endpoint: `https://api.preisrunter.net/wrapper/clawdbot-v1/products/`

### Option B: Use the CLI (recommended for agents that run commands)
Requires Node.js 20+.

Install globally:

```bash
npm install -g @preisrunter/preisrunter-cli
```

Or run via npx (no install):

```bash
npx @preisrunter/preisrunter-cli --help
```

## Usage

### Query parameters

- `q` (string, required): search query
- `region` (`at|de`, optional, default: `at`)
- `onlySale` (`true|false`, optional)

### Output fields (returned per product)

- `productName`
- `productSize`
- `productUnit`
- `productMarket`
- `productPrice` (numeric EUR)
- `productSale` (sale text, if applicable)
- `productLink` (Preisrunter product detail page)

---

## API Examples (curl)

### Search products (default region = at)
```bash
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=butter" | jq
```

### Search products in Germany
```bash
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=butter&region=de" | jq
```

### Only show products on sale
```bash
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=bier&onlySale=true" | jq
```

### Return only a compact list for bots
```bash
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=milch&region=at" \
  | jq '.[] | {productName, productMarket, productPrice, productSale, productLink}'
```

### Get the cheapest result (best effort)
```bash
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=chips&region=at" \
  | jq 'sort_by(.productPrice) | .[0]'
```

---

## CLI Examples (preisrunter)

### Basic search
```bash
preisrunter search "butter"
```

### Multiple-word search (quotes required)
```bash
preisrunter search "bio milch"
```

### Region selection
```bash
preisrunter search "chips" --region at
preisrunter search "chips" --region de
```

### Only show products on sale
```bash
preisrunter search "bier" --only-sale
```

### JSON output (recommended for agents)
```bash
preisrunter search "bier" --region at --json | jq
```

### Pipe + transform into compact bot format
```bash
preisrunter search "butter" --region at --json \
  | jq '.[] | {name: .productName, store: .productMarket, price: .productPrice, sale: .productSale, link: .productLink}'
```

---

## Notes

- Queries containing spaces must be wrapped in quotes when using the CLI.
- The API wrapper is rate-limited upstream (returning HTTP 429); agents should avoid high-frequency polling.
- If no products are found, the API may return HTTP 404; the CLI exits with code 4.

## Examples

```bash
# API: Find sale items for "bier" in Austria
curl -s "https://api.preisrunter.net/wrapper/clawdbot-v1/products?q=bier&region=at&onlySale=true" | jq

# CLI: Get raw JSON for automation
preisrunter search "bio milch" --region de --json

# CLI: Cheapest "milk" result in Austria (best effort)
preisrunter search "butter" --region at --json | jq 'sort_by(.productPrice) | .[0]'
```
