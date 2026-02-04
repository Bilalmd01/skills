---
name: privy
description: Create and manage agentic wallets with Privy. Use for autonomous onchain transactions, wallet creation, policy management, and transaction execution on Ethereum, Solana, and other chains. Triggers on requests involving crypto wallets for AI agents, server-side wallet operations, or autonomous transaction execution.
---

# Privy Agentic Wallets

Create wallets that AI agents can control autonomously with policy-based guardrails.

## Prerequisites

This skill requires Privy API credentials as environment variables:

- **PRIVY_APP_ID** — App identifier from dashboard
- **PRIVY_APP_SECRET** — Secret key for API auth

**Before using this skill:** Check if credentials are configured by running:
```bash
echo $PRIVY_APP_ID
```

If empty or not set, direct the user to [setup.md](references/setup.md) to:
1. Create a Privy app at [dashboard.privy.io](https://dashboard.privy.io)
2. Add credentials to OpenClaw gateway config

## Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| Create wallet | `/v1/wallets` | POST |
| List wallets | `/v1/wallets` | GET |
| Get wallet | `/v1/wallets/{id}` | GET |
| Send transaction | `/v1/wallets/{id}/rpc` | POST |
| Create policy | `/v1/policies` | POST |
| Get policy | `/v1/policies/{id}` | GET |

## Authentication

All requests require:
```
Authorization: Basic base64(APP_ID:APP_SECRET)
privy-app-id: <APP_ID>
Content-Type: application/json
```

## Core Workflow

### 1. Create a Policy (optional but recommended)

Policies constrain what the agent can do. See [policies.md](references/policies.md).

```bash
curl -X POST "https://api.privy.io/v1/policies" \
  --user "$PRIVY_APP_ID:$PRIVY_APP_SECRET" \
  -H "privy-app-id: $PRIVY_APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0",
    "name": "Agent transfer limits",
    "chain_type": "ethereum",
    "rules": [{
      "name": "Max 0.1 ETH per transaction",
      "method": "eth_sendTransaction",
      "conditions": [{
        "field_source": "ethereum_transaction",
        "field": "value",
        "operator": "lte",
        "value": "100000000000000000"
      }],
      "action": "ALLOW"
    }]
  }'
```

### 2. Create an Agent Wallet

```bash
curl -X POST "https://api.privy.io/v1/wallets" \
  --user "$PRIVY_APP_ID:$PRIVY_APP_SECRET" \
  -H "privy-app-id: $PRIVY_APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "chain_type": "ethereum",
    "policy_ids": ["<policy_id>"]
  }'
```

Response includes `id` (wallet ID) and `address`.

### 3. Execute Transactions

See [transactions.md](references/transactions.md) for chain-specific examples.

```bash
curl -X POST "https://api.privy.io/v1/wallets/<wallet_id>/rpc" \
  --user "$PRIVY_APP_ID:$PRIVY_APP_SECRET" \
  -H "privy-app-id: $PRIVY_APP_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "eth_sendTransaction",
    "caip2": "eip155:1",
    "params": {
      "transaction": {
        "to": "0x...",
        "value": "1000000000000000"
      }
    }
  }'
```

## Supported Chains

| Chain | chain_type | CAIP-2 Example |
|-------|------------|----------------|
| Ethereum | `ethereum` | `eip155:1` |
| Base | `ethereum` | `eip155:8453` |
| Polygon | `ethereum` | `eip155:137` |
| Arbitrum | `ethereum` | `eip155:42161` |
| Optimism | `ethereum` | `eip155:10` |
| Solana | `solana` | `solana:mainnet` |

Extended chains: `cosmos`, `stellar`, `sui`, `aptos`, `tron`, `bitcoin-segwit`, `near`, `ton`, `starknet`

## Reference Files

- [setup.md](references/setup.md) — Dashboard setup, getting credentials
- [wallets.md](references/wallets.md) — Wallet creation and management
- [policies.md](references/policies.md) — Policy rules and conditions
- [transactions.md](references/transactions.md) — Transaction execution examples
