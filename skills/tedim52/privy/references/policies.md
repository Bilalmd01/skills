# Policies

Policies define guardrails for agent behavior — what transactions are allowed or denied.

## Create Policy

```bash
POST /v1/policies
```

### Request

```json
{
  "version": "1.0",
  "name": "Agent spending limits",
  "chain_type": "ethereum",
  "rules": [
    {
      "name": "Allow transfers up to 0.1 ETH",
      "method": "eth_sendTransaction",
      "conditions": [
        {
          "field_source": "ethereum_transaction",
          "field": "value",
          "operator": "lte",
          "value": "100000000000000000"
        }
      ],
      "action": "ALLOW"
    }
  ]
}
```

### Response

```json
{
  "id": "tb54eps4z44ed0jepousxi4n",
  "name": "Agent spending limits",
  "chain_type": "ethereum",
  "version": "1.0",
  "rules": [...],
  "created_at": 1741833088894
}
```

## Policy Rules

Each rule has:
- `name` — Human-readable name
- `method` — Transaction method this rule applies to
- `conditions` — Array of conditions that must be true
- `action` — `ALLOW` or `DENY`

### Methods

| Method | Description |
|--------|-------------|
| `eth_sendTransaction` | Send EVM transaction |
| `eth_signTransaction` | Sign EVM transaction |
| `eth_signTypedData_v4` | Sign typed data (EIP-712) |
| `signTransaction` | Sign Solana transaction |
| `signAndSendTransaction` | Sign and send Solana transaction |
| `*` | All methods |

### Conditions

#### Ethereum Transaction Conditions

```json
{
  "field_source": "ethereum_transaction",
  "field": "to",
  "operator": "eq",
  "value": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
}
```

Fields: `to`, `value`, `chain_id`

#### Operators

| Operator | Description |
|----------|-------------|
| `eq` | Equals |
| `gt` | Greater than |
| `gte` | Greater than or equal |
| `lt` | Less than |
| `lte` | Less than or equal |
| `in` | In list |
| `in_condition_set` | In condition set |

## Common Policy Patterns

### Max Transfer Amount

```json
{
  "name": "Max 1 ETH per tx",
  "method": "eth_sendTransaction",
  "conditions": [{
    "field_source": "ethereum_transaction",
    "field": "value",
    "operator": "lte",
    "value": "1000000000000000000"
  }],
  "action": "ALLOW"
}
```

### Allowlist Contracts

```json
{
  "name": "Only USDC on Base",
  "method": "eth_sendTransaction",
  "conditions": [{
    "field_source": "ethereum_transaction",
    "field": "to",
    "operator": "eq",
    "value": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  }],
  "action": "ALLOW"
}
```

### Restrict to Specific Chain

```json
{
  "name": "Base only",
  "method": "eth_sendTransaction",
  "conditions": [{
    "field_source": "ethereum_transaction",
    "field": "chain_id",
    "operator": "eq",
    "value": "8453"
  }],
  "action": "ALLOW"
}
```

### Multiple Conditions (AND)

All conditions must be true:

```json
{
  "name": "Small transfers to specific address",
  "method": "eth_sendTransaction",
  "conditions": [
    {
      "field_source": "ethereum_transaction",
      "field": "to",
      "operator": "eq",
      "value": "0x..."
    },
    {
      "field_source": "ethereum_transaction",
      "field": "value",
      "operator": "lte",
      "value": "100000000000000000"
    }
  ],
  "action": "ALLOW"
}
```

## Get Policy

```bash
GET /v1/policies/{policy_id}
```

## Update Policy

```bash
PATCH /v1/policies/{policy_id}
```

## Delete Policy

```bash
DELETE /v1/policies/{policy_id}
```

## Add Rule to Policy

```bash
POST /v1/policies/{policy_id}/rules
```

## Delete Rule from Policy

```bash
DELETE /v1/policies/{policy_id}/rules/{rule_id}
```
