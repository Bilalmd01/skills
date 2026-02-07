---
name: deepseek-trader
description: Hybrid cryptocurrency analysis using DeepSeek API. Combines technical indicators (RSI, MACD, SMA, Bollinger Bands) with AI-powered market analysis. Use when user says "crypto analysis", "DeepSeek trader", "AI trading signal", or "market analysis".
---

# DeepSeek Trader

Hybrid cryptocurrency analysis combining technical indicators with DeepSeek AI reasoning. Get buy/sell/hold signals backed by both quantitative data and AI interpretation.

## Features

- **Technical Indicators**: RSI, MACD, SMA (20/50), Bollinger Bands, price change %
- **AI Analysis**: DeepSeek API interprets indicators and market context
- **Multi-coin support**: BTC, ETH, SOL, and more via CoinGecko
- **Risk assessment**: AI provides confidence levels and risk warnings
- **Japanese language support**: Analysis output in Japanese
- **Cost-effective**: DeepSeek API is significantly cheaper than GPT-4

## Quick Start

```bash
cd {skill_dir}
npm install
npm run build

# Analyze a single coin
DEEPSEEK_API_KEY=your_key node dist/cli.js analyze --coin bitcoin

# Analyze multiple coins
DEEPSEEK_API_KEY=your_key node dist/cli.js analyze --coins bitcoin,ethereum,solana

# Get trading signals only
DEEPSEEK_API_KEY=your_key node dist/cli.js signals --coin bitcoin
```

## Analysis Output

```json
{
  "coin": "bitcoin",
  "current_price_jpy": 15234567,
  "technical_indicators": {
    "rsi": 45.2,
    "macd": { "macd_line": 120, "signal_line": 95, "histogram": 25 },
    "sma_20": 15100000,
    "sma_50": 14800000,
    "price_change_24h_pct": 2.3,
    "price_change_7d_pct": -1.5
  },
  "ai_analysis": {
    "signal": "HOLD",
    "confidence": 0.72,
    "reasoning": "RSI is neutral, MACD shows mild bullish momentum...",
    "risk_level": "medium",
    "suggested_action": "Wait for RSI to drop below 35 for entry"
  }
}
```

## Architecture

```
CoinGecko API → Price Data → Technical Indicators
                                    ↓
                              DeepSeek API → AI Analysis → Signal
```

## Configuration

Environment variables:
- `DEEPSEEK_API_KEY` — DeepSeek API key (required)
- `COINGECKO_API` — CoinGecko base URL (default: free tier)

## Requirements

- Node.js 18+
- DeepSeek API key
- Internet connection
