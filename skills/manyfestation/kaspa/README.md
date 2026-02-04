# Kaspa Wallet CLI

Standalone wallet using the **official Kaspa WASM SDK** from [rusty-kaspa releases](https://github.com/kaspanet/rusty-kaspa/releases).

## Install

```bash
node install.js
```

## Usage

```bash
./kaswallet.sh info                              # Network status
./kaswallet.sh balance <address>                 # Check balance
./kaswallet.sh send <to> <amount> [fee]          # Send KAS
./kaswallet.sh generate-mnemonic                 # New seed phrase
```

## Environment

```bash
export KASPA_MNEMONIC="your 24 words..."    # Wallet seed
export KASPA_PRIVATE_KEY="hex..."           # Or private key
export KASPA_NETWORK="mainnet"              # mainnet | testnet-10
```
