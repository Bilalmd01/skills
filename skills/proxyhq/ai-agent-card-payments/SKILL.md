---
name: ai-agent-card-payments
description: Virtual card payments for AI agents. Provision cards on-demand, create payment intents, and let agents make autonomous purchases within policy limits. Supports spending controls, merchant restrictions, and human approval for high-value transactions via MCP.
---

# AI Agent Card Payments

Enable your AI agent to make autonomous payments using virtual cards within policy-defined spending limits.

## What This Enables

- **Autonomous purchasing** - Agents can buy things without human intervention (within limits)
- **Virtual cards on-demand** - Fresh card numbers for each purchase
- **Policy enforcement** - Spending limits, merchant restrictions, approval thresholds
- **Human-in-the-loop** - High-value purchases require approval

## Quick Start

```
1. Check balance    → proxy.balance.get
2. Create intent    → proxy.intents.create
3. Get card         → proxy.cards.get_sensitive
4. Make payment     → Use card at checkout
```

## Available MCP Tools

### Payment Flow
| Tool | Purpose |
|------|---------|
| `proxy.intents.create` | Create payment intent → triggers card provisioning |
| `proxy.intents.list` | List all payment intents |
| `proxy.intents.get` | Get intent details + card info |
| `proxy.cards.get` | Get card details (masked) |
| `proxy.cards.get_sensitive` | Get full PAN, CVV, expiry for payment |

### Account Management
| Tool | Purpose |
|------|---------|
| `proxy.balance.get` | Check available spending power |
| `proxy.funding.get` | Get deposit instructions (ACH/wire/crypto) |
| `proxy.user.get` | Get user profile |
| `proxy.kyc.status` | Check KYC verification status |
| `proxy.kyc.link` | Get link to complete verification |

### Transactions
| Tool | Purpose |
|------|---------|
| `proxy.transactions.list_for_card` | List transactions for a card |
| `proxy.transactions.get` | Get transaction details |

## Payment Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Check     │     │   Create    │     │   Policy    │
│   Balance   │ ──▶ │   Intent    │ ──▶ │   Check     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                         ┌─────────────────────┼─────────────────────┐
                         ▼                     │                     ▼
                  ┌─────────────┐              │              ┌─────────────┐
                  │    Auto     │              │              │   Needs     │
                  │   Approve   │              │              │  Approval   │
                  └──────┬──────┘              │              └──────┬──────┘
                         │                     │                     │
                         ▼                     │                     ▼
                  ┌─────────────┐              │              [Human Reviews]
                  │    Card     │              │                     │
                  │   Issued    │◀─────────────┴─────────────────────┘
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Get Card   │
                  │  Details    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Make      │
                  │  Payment    │
                  └─────────────┘
```

## Intent Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Card ready to use | Get card details, make payment |
| `pending_approval` | Awaiting human approval | Inform user, wait |
| `approved` | Approved, card being issued | Wait for card |
| `card_issued` | Card provisioned | Get card details |
| `matched` | Transaction completed | Done |
| `mismatched` | Transaction didn't match | Review |
| `rejected` | Approval denied | Inform user |
| `expired` | Intent expired | Create new intent |

## Example: Complete Purchase

**User says:** "Buy a $50 Amazon gift card"

```
Step 1: proxy.balance.get
→ { availableBalance: 500.00, currency: "USD" }

Step 2: proxy.intents.create
→ { merchant: "Amazon", amount: 50.00, description: "Gift card purchase" }
→ { id: "int_abc123", status: "pending", cardId: "card_xyz" }

Step 3: proxy.cards.get_sensitive
→ { cardId: "card_xyz" }
→ {
    pan: "4532015112830366",
    cvv: "847",
    expiryMonth: "03",
    expiryYear: "2027",
    billingAddress: { zip: "10001", ... }
  }

Step 4: Use card at Amazon checkout
```

## Error Handling

| Error Code | Cause | Resolution |
|------------|-------|------------|
| `POLICY_REQUIRED` | No policy assigned to agent | Admin assigns policy in dashboard |
| `ONBOARDING_INCOMPLETE` | KYC not completed | Use `proxy.kyc.link` |
| `INSUFFICIENT_BALANCE` | Not enough funds | Use `proxy.funding.get` |
| `FORBIDDEN` | Permission denied | Check agent permissions |

## MCP Server Configuration

Add to your agent's MCP config:

```json
{
  "mcpServers": {
    "proxy": {
      "command": "npx",
      "args": ["-y", "proxy-mcp-server"],
      "env": {
        "PROXY_AGENT_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Setup Requirements

1. **Proxy Pay account** at [useproxy.ai](https://useproxy.ai)
2. **Complete KYC** verification
3. **Fund account** (ACH, wire, or USDC)
4. **Create agent** with spending policy
5. **Generate token** for MCP auth

## Best Practices

1. **Always check balance first** before creating intents
2. **Use descriptive descriptions** for reconciliation
3. **Handle pending_approval** gracefully - inform users
4. **Never log full card numbers** - security risk
5. **Set appropriate policies** - limit blast radius
