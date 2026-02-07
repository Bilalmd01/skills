---
name: tokenbroker
description: Autonomous agent skill for launching tokens on nad.fun. Scans GitHub projects and executes 4-step token deployment.
metadata:
  tags: monad, nadfun, token, launch, trading, autonomous
---

# SKILL.md - TokenBroker Skillset

**The all-in-one token launch toolkit for OpenClaw agents.** Scan projects, generate assets, and launch tokens on nad.fun with zero friction.

## When to Use This Skill

Use this skill when you need to:
- Analyze a GitHub repository for token launch readiness
- Generate metadata (name, symbol, description) for a new token
- Execute the 4-step nad.fun bonding curve deployment
- Monitor trading progress and graduation
- Coordinate with other agents for launch campaigns

**Never use this skill for:**
- Personal wallet management unrelated to launches
- Non-Monad/nad.fun token operations

## What is TokenBroker?

TokenBroker is a modular skillset that gives AI agents the ability to:
1.  **Understand** a project's codebase and purpose.
2.  **Generate** relevant token metadata (names, symbols, descriptions) and assets.
3.  **Launch** tokens on the Monad blockchain via nad.fun bonding curves.
4.  **Promote** the launch with generated marketing content.

## TokenBroker - The Agent Launch Skill

**TokenBroker** is a specialized capability for AI agents (OpenClaw/ELIZA) that allows them to track builder activity on GitHub and orchestrate token launches on **nad.fun**.

## Core Concept
1. **Track**: Agent monitors specified GitHub repositories for significant activity (commits, releases, tags).
2. **Prompt**: Upon identifying a "launchable" state, the agent prompts the builder to deploy a token.
3. **Launch**: Agent executes the 4-step NadFun flow to deploy the token with a "7777" vanity address.

## Module Structure (tokenbroker/)
- `SKILL.md`: Root configuration and integration guide.
- `GITHUB.md`: Instructions for monitoring repository activity.
- `LAUNCH.md`: High-level orchestration for token deployment.
- `ABI.md`: Smart contract interfaces for nad.fun.
- `STATS.md`: Reputation tracking logic.
- `PROMO.md`: Social media orchestration for new launches.

## Quick Start for Agents
1. Read `GITHUB.md` to begin monitoring local or remote repos.
2. When a trigger is hit, use `METADATA.md` to propose token details.
3. Follow `LAUNCH.md` to execute the transaction flow.

**"Launch this token on nad.fun."**
> 1. Read **LAUNCH.md** for the 4-step flow.
> 2. Ensure `PRIVATE_KEY` is set in the environment.
> 3. Execute the launch sequence.

**"Create a launch post for Twitter."**
> 1. Read **PROMO.md** for templates.
> 2. Generate content using the token address and project info.

## Installation

```bash
# Clone into your project's skill directory
git clone https://github.com/starrftw/tokenbroker.git .tokenbroker
```

## Install Wizard Flow

The Install Wizard is an interactive CLI tool that guides you through setting up TokenBroker. Follow these steps in order:

### Step 1: Project Validation (Local Scan)
The wizard begins by scanning the current directory to identify the project structure. It validates the presence of essential files and checks system dependencies:
- Verifies Node.js/Python project structure
- Checks Git installation and connectivity
- Validates file system permissions for writing

**This step happens BEFORE any GitHub connection is required.**

### Step 2: Wallet Setup (.env Generation)
Configure your cryptographic credentials for on-chain operations:
- Import existing private key (hex or mnemonic)
- Generate new key pair with secure random generation
- The wizard creates `.env` with `PRIVATE_KEY` and applies secure file permissions (0600)

### Step 3: Network Selection
Choose your blockchain network environment:
- **Testnet**: Monad testnet with faucet access (recommended for development)
- **Mainnet**: Production Monad network (requires explicit risk confirmation)

### Step 4: GitHub OAuth (Optional)
Establish GitHub connection for repository monitoring:
- OAuth 2.0 flow opens browser for authorization
- Device code fallback for CLI-only environments
- Pre-existing Personal Access Tokens (PATs) also supported

### Step 5: Post-Setup Launch Suggestions
After wizard completion, the agent:
- Scans your project for launch readiness
- Analyzes codebase for token potential
- Suggests token metadata (name, symbol, description)
- Recommends optimal launch timing

## Configuration

Ensure your environment is set up for Monad:

```bash
NETWORK=testnet # or mainnet
PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
# NAD_API_KEY=... # Optional: for higher rate limits
```

## Network Constants

### Testnet
- **RPC**: `https://monad-testnet.drpc.org`
- **Chain ID**: `10143`
- **API**: `https://dev-api.nad.fun`

### Mainnet
- **RPC**: `https://monad-mainnet.drpc.org`
- **Chain ID**: `143`
- **API**: `https://api.nadapp.net`

---
*Built for the agentic future.* 🦞
