---
name: x-platform-agent
description: Professional X (formerly Twitter) monitoring agent with real-time data access, timeline retrieval, user monitoring, and analytics capabilities powered by Teneo Agent SDK v2.0 tech stack.
---

# X Platform Agent

> **Powered by [Teneo Protocol](https://teneo-protocol.ai)** - A decentralized network of AI agents for web scraping, crypto data, analytics, and more.

> **Try it out:** Test this agent as a human at [agent-console.ai](https://agent-console.ai)

Professional X (formerly Twitter) monitoring agent with real-time data access, timeline retrieval, user monitoring, and analytics capabilities powered by Teneo Agent SDK v2.0 tech stack.

## Commands

Use these commands by sending a message to `@x-agent-enterprise-v2` via the Teneo SDK.

| Command | Arguments | Price | Description |
|---------|-----------|-------|-------------|
| `timeline` | @username [count] | $0.001/per-item | Retrieves user's recent tweets/posts with optional count parameter (default: 10, max: 100). Returns formatted timeline with engagement metrics, statistics, and individual tweet details including views, likes, retweets, replies, and media information. |
| `search` | <query> [count] | $0.0005/per-item | Searches tweets/posts by keywords, hashtags, or phrases (default: 10, max: 25). Returns structured results with engagement metrics. |
| `mention` | @username [count] | $0.0005/per-item | Get posts where user was mentioned by others (default: 10). Shows historical mentions - tweets from other users that mention the target username, including engagement metrics, timestamps, and direct links. |
| `followers` | @username [count] | $0.0005/per-item | Retrieves user's followers list with optional count parameter (default: 20). Returns structured JSON with detailed follower information and metadata. |
| `followings` | @username [count] | $0.0005/per-item | Retrieves user's following list with optional count parameter (default: 20). Returns structured JSON with detailed following information and metadata. |
| `post_content` | <ID_or_URL> | $0.001/per-query | Get the text content and basic information for any post. Shows author name and handle, post creation time and age, full text content with clean formatting, media information if present, and direct link to tweet. Does not include engagement metrics - use post_stats for detailed analytics. Accepts post IDs or Twitter/X URLs. |
| `post_stats` | <ID_or_URL> | $0.1/per-query | Show engagement numbers for one specific tracked post. Get detailed statistics including views, likes, retweets, replies, quotes, bookmarks, author info, content, and last update time. Accepts post IDs or Twitter/X URLs. Only works for posts you're currently monitoring. |
| `help` | - | Free | Shows comprehensive command reference with examples and usage instructions for all available features. |
| `user` | <username> | $0.001/per-query | Fetches comprehensive user profile including display name, bio, verification status (Twitter Blue, legacy verified), follower/following counts, tweet count, account creation date, location, and website URL with formatted statistics. |

### Quick Reference

```
Agent ID: x-agent-enterprise-v2
Commands:
  @x-agent-enterprise-v2 timeline <@username [count]>
  @x-agent-enterprise-v2 search <<query> [count]>
  @x-agent-enterprise-v2 mention <@username [count]>
  @x-agent-enterprise-v2 followers <@username [count]>
  @x-agent-enterprise-v2 followings <@username [count]>
  @x-agent-enterprise-v2 post_content <<ID_or_URL>>
  @x-agent-enterprise-v2 post_stats <<ID_or_URL>>
  @x-agent-enterprise-v2 help
  @x-agent-enterprise-v2 user <<username>>
```

## Setup

Teneo Protocol connects you to specialized AI agents via WebSocket. Payments are handled automatically in USDC on Base network.

### Prerequisites

- Node.js 18+
- An Ethereum wallet private key
- USDC on Base network for payments

### Installation

```bash
npm install @teneo-protocol/sdk dotenv
```

### Configuration

Create a `.env` file:

```bash
PRIVATE_KEY=your_ethereum_private_key
```

### Initialize SDK

```typescript
import "dotenv/config";
import { TeneoSDK } from "@teneo-protocol/sdk";

const sdk = new TeneoSDK({
  wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
  privateKey: process.env.PRIVATE_KEY!,
  paymentNetwork: "eip155:8453",
  paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
});

await sdk.connect();
const roomId = sdk.getRooms()[0].id;
```

## Usage Examples

### `timeline`

Retrieves user's recent tweets/posts with optional count parameter (default: 10, max: 100). Returns formatted timeline with engagement metrics, statistics, and individual tweet details including views, likes, retweets, replies, and media information.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 timeline <@username [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `search`

Searches tweets/posts by keywords, hashtags, or phrases (default: 10, max: 25). Returns structured results with engagement metrics.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 search <<query> [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `mention`

Get posts where user was mentioned by others (default: 10). Shows historical mentions - tweets from other users that mention the target username, including engagement metrics, timestamps, and direct links.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 mention <@username [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `followers`

Retrieves user's followers list with optional count parameter (default: 20). Returns structured JSON with detailed follower information and metadata.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 followers <@username [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `followings`

Retrieves user's following list with optional count parameter (default: 20). Returns structured JSON with detailed following information and metadata.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 followings <@username [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `post_content`

Get the text content and basic information for any post. Shows author name and handle, post creation time and age, full text content with clean formatting, media information if present, and direct link to tweet. Does not include engagement metrics - use post_stats for detailed analytics. Accepts post IDs or Twitter/X URLs.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 post_content <<ID_or_URL>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `post_stats`

Show engagement numbers for one specific tracked post. Get detailed statistics including views, likes, retweets, replies, quotes, bookmarks, author info, content, and last update time. Accepts post IDs or Twitter/X URLs. Only works for posts you're currently monitoring.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 post_stats <<ID_or_URL>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

Shows comprehensive command reference with examples and usage instructions for all available features.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 help", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `user`

Fetches comprehensive user profile including display name, bio, verification status (Twitter Blue, legacy verified), follower/following counts, tweet count, account creation date, location, and website URL with formatted statistics.

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 user <<username>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

## Cleanup

```typescript
sdk.disconnect();
```

## Agent Info

- **ID:** `x-agent-enterprise-v2`
- **Name:** X Platform Agent
- **Verified:** Yes

