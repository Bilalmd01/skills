# ClawSkill — Mine RTC Tokens With Your AI Agent

Mine **RTC (RustChain Tokens)** by proving your agent runs on real hardware. One command to install, automatic attestation, built-in wallet.

## Install

```bash
# Python (recommended)
pip install clawskill

# Node.js
npm install -g clawskill
```

## Setup

```bash
# Install miner + configure wallet
clawskill install --wallet my-agent-miner

# Start mining in background
clawskill start
```

Your agent is now mining RTC. That's it.

## How It Works

1. **Hardware Fingerprinting** — 6 cryptographic checks prove your machine is real:
   - Clock-skew & oscillator drift
   - Cache timing fingerprint (L1/L2/L3 latency)
   - SIMD unit identity (SSE/AVX/AltiVec/NEON bias)
   - Thermal drift entropy
   - Instruction path jitter (microarchitectural)
   - Anti-emulation behavioral checks

2. **Automatic Attestation** — Your agent attests to the RustChain network every few minutes

3. **Per-Epoch Rewards** — RTC tokens accumulate in your wallet each epoch (~10 minutes)

4. **VM Detection** — Virtual machines are detected and receive effectively zero rewards. Real iron only.

## Multipliers

| Hardware | Multiplier | Notes |
|----------|-----------|-------|
| Modern x86/ARM | **1.0x** | Standard rate — this is you |
| Apple Silicon (M1/M2/M3) | **1.2x** | Slight bonus |
| IBM POWER8 | **1.5x** | Server-class vintage |
| PowerPC G5 | **2.0x** | Vintage bonus |
| PowerPC G4 | **2.5x** | Maximum vintage bonus |
| **VM/Emulator** | **~0x** | **Detected and penalized** |

## Commands

| Command | Description |
|---------|-------------|
| `clawskill install` | Download miner, create wallet, set up service |
| `clawskill start` | Start mining in background |
| `clawskill stop` | Stop mining |
| `clawskill status` | Check miner + network status |
| `clawskill logs` | View miner output |
| `clawskill uninstall` | Remove everything |

## Why VMs Are Penalized

RustChain uses **Proof-of-Antiquity (PoA)** consensus. The network rewards machines that bring **real compute** — physical CPUs with genuine timing characteristics, thermal profiles, and instruction path jitter. VMs flatten all of these signals, making them trivially detectable via the 6 fingerprint checks.

This prevents "VM farms" from gaming rewards. If you want to earn RTC, run on bare metal.

## What Gets Installed

- Miner scripts from the [RustChain GitHub repo](https://github.com/Scottcjn/Rustchain)
- Python virtual environment with dependencies
- Systemd user service (Linux) or LaunchAgent (macOS)
- All files stored in `~/.clawskill/`

## Requirements

- Python 3.8+ (installed on most systems)
- Linux or macOS
- Real hardware (not a VM)

## Links

- **PyPI**: https://pypi.org/project/clawskill/
- **npm**: https://www.npmjs.com/package/clawskill
- **GitHub**: https://github.com/Scottcjn/Rustchain
- **BoTTube**: https://bottube.ai
- **Block Explorer**: https://50.28.86.131/explorer

## License

MIT — [Elyan Labs](https://bottube.ai)
