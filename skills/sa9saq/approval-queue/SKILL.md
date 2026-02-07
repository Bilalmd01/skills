---
name: approval-queue
description: Approval queue system for managing pending actions (SNS posts, deployments, etc.) with one-tap approve/reject. REST API + CLI interface. Use when user says "approval queue", "pending approvals", "approve post", or "review queue".
---

# Approval Queue

A lightweight approval queue system for managing pending actions — SNS posts, deployments, content publishing, and more. Approve or reject with a single tap.

## Features

- **REST API + CLI**: Manage queue from terminal or integrate with bots
- **One-tap approval**: Quick approve/reject via API or inline buttons
- **Flexible payloads**: Queue any action type (SNS posts, deploys, emails)
- **SQLite storage**: Persistent queue with history
- **Webhook callbacks**: Trigger actions on approval
- **Status tracking**: Pending → Approved/Rejected with timestamps

## Quick Start

```bash
cd {skill_dir}
npm install
npm run build

# Start API server
node dist/server.js --port 3010

# CLI usage
node dist/cli.js add --type sns_post --payload '{"text":"Hello world","platform":"twitter"}'
node dist/cli.js list --status pending
node dist/cli.js approve <item-id>
node dist/cli.js reject <item-id> --reason "Not appropriate"
```

## API Endpoints

- `GET /api/queue` — List queue items (filter by status, type)
- `POST /api/queue` — Add item to queue
- `POST /api/queue/:id/approve` — Approve an item
- `POST /api/queue/:id/reject` — Reject an item
- `GET /api/queue/:id` — Get item details
- `DELETE /api/queue/:id` — Delete item

## Queue Item Structure

```json
{
  "id": "uuid",
  "type": "sns_post",
  "status": "pending",
  "payload": {
    "text": "Post content",
    "platform": "twitter",
    "media": []
  },
  "created_at": "2025-01-01T00:00:00Z",
  "reviewed_at": null,
  "reviewer_note": null
}
```

## Integration with OpenClaw

Use with inline buttons for Telegram/Discord one-tap approval:
```
Agent receives content → Adds to queue → Sends approval button → User taps → Action executes
```

## Configuration

Environment variables:
- `PORT` — Server port (default: 3010)
- `DB_PATH` — SQLite database path (default: ./data/queue.db)
- `WEBHOOK_URL` — Callback URL on approve/reject (optional)

## Requirements

- Node.js 18+
- No external API keys needed
