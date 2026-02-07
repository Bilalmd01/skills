# METADATA.md - Token Asset Generation

**Turn raw project data into a compelling token identity.**

This module guides the agent in generating creative and compliant metadata for the nad.fun token launch.

## 1. Naming Strategy

When helping a user pick a token name/symbol, use these strategies:

### A. The Ecosystem Token
Directly named after the project. Best for serious utilities.
*   **Source**: "OpenClaw"
*   **Name**: "OpenClaw Token"
*   **Symbol**: `$CLAW`

### B. The Mascot/Meme
A character or concept derived from the project's brand. High engagement potential.
*   **Source**: "TokenBroker" (Lobster emoji used in docs)
*   **Name**: "Broker Lobster"
*   **Symbol**: `$LOBSTER`

### C. The DAO/Governance
For community-led initiatives.
*   **Source**: "Builder Toolkit"
*   **Name**: "Builder DAO"
*   **Symbol**: `$BUILD`

## 2. Description Generation

Descriptions on nad.fun should be punchy (under 280 chars recommended) but informative.

**Template:**
> "The official [Utility/Meme] token for [Project Name]. [Value Prop]. Powered by [Tech Stack] on Monad."

**Example:**
> "The official automation token for TokenBroker. Deploy agents instantly and mine launches on nad.fun. Powered by OpenClaw on Monad. 🦞"

## 3. Metadata Structure

The nad.fun API expects this exact JSON structure:

```json
{
  "name": "My Token",
  "symbol": "MTK",
  "description": "Token description",
  "image_uri": "ipfs://...",
  "website": "https://...", 
  "twitter": "https://x.com/...",
  "telegram": "https://t.me/..."
}
```

*   `image_uri` comes from the Image Upload step (see **LAUNCH.md**).
*   Social links are optional but highly recommended for trust.

## 4. Agent Prompts

**Prompt:** "Suggest 3 token ideas for this project."
**Agent Action:**
1.  Read `PROJECT-SCAN.md` output.
2.  Apply Strategies A, B, and C.
3.  Output a table with Name, Symbol, and Description for each.

## Next Steps

Once metadata is approved by the user:
- Go to **LAUNCH.md** to start the upload and deployment process.
