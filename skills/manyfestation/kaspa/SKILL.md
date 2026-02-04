---
name: Kaspa Wallet
description: Standalone Kaspa wallet CLI. Send KAS, check balances.
---

# Kaspa Wallet CLI

## Install

```bash
node install.js
```

Downloads official WASM SDK from [kaspanet/rusty-kaspa](https://github.com/kaspanet/rusty-kaspa/releases).

**Requires:** Node.js >= 20

## Environment

```bash
export KASPA_MNEMONIC="your 12-24 word seed phrase"
# or
export KASPA_PRIVATE_KEY="hex"
```

Optional: `KASPA_NETWORK=mainnet|testnet-10`

## Commands

```bash
./kaswallet.sh balance [address]            # Check balance
./kaswallet.sh info                         # Network status
./kaswallet.sh send <to> <amount|max> [fee] # Send KAS
./kaswallet.sh uri [address] [amount] [msg] # Payment URI
./kaswallet.sh generate-mnemonic            # New seed phrase
```

## Examples

```bash
# Check any address
./kaswallet.sh balance kaspa:qrc8y...

# Send 0.5 KAS
./kaswallet.sh send kaspa:qrc8y... 0.5

# Send entire balance
./kaswallet.sh send kaspa:qrc8y... max
```

## Storage Mass Error

If you see `Storage mass exceeds maximum` when sending a specific amount:

**Consolidate UTXOs first** by sending `max` to your own address, then retry:

```bash
# Step 1: Get your wallet address
./kaswallet.sh balance
# Returns: {"address": "kaspa:qYOUR_ADDRESS...", ...}

# Step 2: Consolidate by sending max to yourself
./kaswallet.sh send kaspa:qYOUR_ADDRESS... max

# Step 3: Now send the specific amount (will work)
./kaswallet.sh send kaspa:qRECIPIENT... 0.5
```

This merges fragmented UTXOs into one, fixing the issue.

## Output

All commands return JSON:

```json
{"status":"sent","txid":"abc...","from":"kaspa:...","to":"kaspa:...","amount":"0.5","fee":"0.0002"}
```

Errors:
```json
{"error":"Storage mass exceeds maximum"}
```
