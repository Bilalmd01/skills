# VERIFY.md - Ecosystem Verification Skill

**Get funded and verified. Follow official ecosystem guidelines.**

This module guides agents through the automated verification and funding processes provided by the Monad and Nad.fun ecosystem.

## 1. Testnet Faucet

Agents can request testnet MON to cover fees and initial buys.

**Endpoint**: `POST https://agents.devnads.com/v1/faucet`

```typescript
const faucetRes = await fetch("https://agents.devnads.com/v1/faucet", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    address: walletAddress
  })
});
const result = await faucetRes.json();
```

## 2. Submission Verification

Verify your agent and token deployment.

**Endpoint**: `POST https://agents.devnads.com/v1/verify`

```typescript
const verifyRes = await fetch("https://agents.devnads.com/v1/verify", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    agent_id: "tokenbroker",
    token_address: tokenAddress,
    github_repo: "https://github.com/starrftw/tokenbroker"
  })
});
const { status, message } = await verifyRes.json();
```

## Agent Instructions

- **Funding**: If the wallet balance is low (< 5 MON), proactively suggest calling the faucet.
- **Verification**: Once a token is launched successfully via `LAUNCH.md`, prompt the user to run the verification process.
- **Reporting**: Display the verification status clearly to ensure the deployment is correctly indexed.
