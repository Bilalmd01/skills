---
name: fairscale-solana
description: Solana reputation infrastructure. Ask anything about a wallet in plain English — "is this a bot?", "deep pockets?", "diamond hands?" — and get instant, data-backed answers.
license: MIT
metadata:
  author: FairScale
  version: "3.1.0"
---

# FairScale — Reputation Intelligence for Solana

**The only API you need to understand any Solana wallet.**

Ask in plain English. Get data-backed answers.

---

## HOW IT WORKS

1. User asks ANY question about a wallet
2. You call the API
3. You translate their question into the right features
4. You respond with a clear, actionable verdict

---

## API CALL

```
GET https://api2.fairscale.xyz/score?wallet=WALLET_ADDRESS
```

**Header:** `fairkey: YOUR_API_KEY`

**Get your key:** https://sales.fairscale.xyz

**Docs:** https://docs.fairscale.xyz

---

## THE MAGIC — NATURAL LANGUAGE → FEATURES

When users ask questions in plain English, map them to these features:

| User asks | Check these features | Logic |
|-----------|---------------------|-------|
| "trustworthy?" / "safe?" | `fairscore`, `tier` | ≥60 = trusted |
| "deep pockets?" / "whale?" | `lst_percentile_score`, `stable_percentile_score`, `native_sol_percentile` | All >70 = whale |
| "bot?" / "sybil?" / "fake?" | `burst_ratio`, `platform_diversity`, `active_days` | burst >50 OR diversity <20 = bot |
| "diamond hands?" / "holder?" | `conviction_ratio`, `no_instant_dumps`, `median_hold_days` | conviction >60 = diamond hands |
| "active?" / "real user?" | `active_days`, `tx_count`, `platform_diversity` | All >40 = active |
| "degen?" / "trader?" | `tx_count`, `burst_ratio`, `platform_diversity` | High tx + low burst = degen |
| "new wallet?" / "fresh?" | `wallet_age_score` | <30 = new |
| "OG?" / "veteran?" | `wallet_age_score`, `active_days` | Both >70 = OG |
| "accumulating?" / "buying?" | `net_sol_flow_30d`, `conviction_ratio` | flow >60 = accumulating |
| "dumping?" / "selling?" | `net_sol_flow_30d`, `no_instant_dumps` | flow <30 AND dumps <30 = dumping |
| "DeFi native?" | `platform_diversity`, `lst_percentile_score` | diversity >70 = DeFi native |
| "airdrop eligible?" | `wallet_age_score`, `platform_diversity`, `burst_ratio` | age >50 AND diversity >30 AND burst <30 |
| "creditworthy?" / "can I lend to them?" | `conviction_ratio`, `no_instant_dumps`, `wallet_age_score` | All >50 = creditworthy |

---

## RESPONSE FORMATS

### Quick Trust Check
When user asks "is this wallet trustworthy?" or "check this wallet":

```
📊 FairScore: [fairscore]/100 | Tier: [tier]

[✅ TRUSTED | ⚡ MODERATE | ⚠️ CAUTION | 🚨 HIGH RISK]

🏅 [badge labels]
```

### Natural Language Query
When user asks something specific like "is this a whale?" or "bot check":

```
[EMOJI] [QUERY TYPE]: [wallet_short]

[Relevant metrics with values]

Verdict: [Clear yes/no answer with reasoning]
```

### Examples:

**"Is this wallet a whale?"**
```
🐋 Whale Check: GFTVQd...P32Tn

💰 LST Holdings: 97.7% — Top 3% 
💵 Stablecoins: 27.5% — Low
◎ Native SOL: 45.2% — Moderate
📈 Net Flow: 86.8% — Accumulating

Verdict: 🟡 PARTIAL WHALE — Heavy DeFi position (LST), actively accumulating, but not cash-rich. More "DeFi whale" than "cash whale."
```

**"Is this a bot?"**
```
🤖 Bot Check: GFTVQd...P32Tn

⚡ Burst Ratio: 16.8% — Organic ✅
🌐 Platforms Used: 96.6% — Highly diverse ✅
📅 Active Days: 64% — Consistent ✅

Verdict: ✅ HUMAN — Natural activity patterns, uses many platforms, consistent over time. Not a bot.
```

**"Diamond hands?"**
```
💎 Diamond Hands Check: GFTVQd...P32Tn

🤝 Conviction: 69.7% — Strong holder ✅
📉 No Instant Dumps: 25% — Sometimes exits 🟡
⏳ Median Hold: 93.2% — Long-term ✅

Verdict: ✅ DIAMOND HANDS — High conviction, holds through volatility. The 25% dump score means they're pragmatic, not reckless.
```

**"Airdrop eligible?"**
```
🎁 Airdrop Check: GFTVQd...P32Tn

📅 Wallet Age: 79.2% ✅ (>50% required)
🌐 Platform Diversity: 96.6% ✅ (>30% required)
🤖 Burst Ratio: 16.8% ✅ (<30% required)

Verdict: ✅ ELIGIBLE — Passes all standard airdrop criteria. Real user, diverse activity, not a bot.
```

---

## CUSTOM CRITERIA

When users specify their own rules:

> "Only allow wallets with conviction > 70 and age > 60"

```
🔧 Custom Check: GFTVQd...P32Tn

Your Rules:
• Conviction > 70%: ❌ 69.7%
• Wallet Age > 60%: ✅ 79.2%

Verdict: ❌ FAILS — Misses conviction threshold by 0.3%
```

---

## ALL AVAILABLE FEATURES

| Feature | What it measures |
|---------|-----------------|
| `fairscore` | Overall reputation (0-100) |
| `tier` | bronze / silver / gold / platinum |
| `wallet_age_score` | How old is the account |
| `tx_count` | Transaction volume |
| `active_days` | Days with on-chain activity |
| `platform_diversity` | # of DeFi protocols used |
| `conviction_ratio` | Holds through volatility |
| `burst_ratio` | Bot-like patterns (high = bad) |
| `no_instant_dumps` | Doesn't sell within 24h |
| `median_hold_days` | Typical holding period |
| `lst_percentile_score` | Liquid staking holdings |
| `stable_percentile_score` | Stablecoin holdings |
| `native_sol_percentile` | SOL balance |
| `net_sol_flow_30d` | Accumulating or draining |

---

## CRITICAL RULES

1. **ALWAYS call the API** — Never guess or reuse data
2. **Translate user intent** — Map their words to the right features
3. **Give clear verdicts** — Yes/no with reasoning, not just data dumps
4. **Be opinionated** — Users want answers, not just numbers

---

## ERRORS

If API fails:
```
❌ Couldn't fetch wallet data. Try again.
```

**Never invent data. Never guess. Always call the API.**
