# TRADING.md - Token Trading Skill

**Interact with your token after launch. Buy, sell, and track progress.**

This module enables agents to execute trades on the nad.fun bonding curve autonomously.

## Capabilities

1.  **Price Discovery**: Get current buy/sell quotes.
2.  **Execute Buy**: Purchase tokens on the bonding curve.
3.  **Execute Sell**: Sell tokens back to the curve.
4.  **Monitor Progress**: Track how close a token is to graduating.

## 1. Price Quotes (Lens)

Use the `Lens` contract to get real-time price data.

```typescript
import { lensAbi } from './ABI'; // See ABI.md

// Get amount out for 1 MON buy
const amountOut = await publicClient.readContract({
  address: CONFIG.LENS,
  abi: lensAbi,
  functionName: "getInitialBuyAmountOut",
  args: [parseEther("1")]
});
```

## 2. Execute Buy (Router)

Purchase tokens using `BondingCurveRouter.buy()`.

```typescript
import { bondingCurveRouterAbi } from './ABI';

const hash = await walletClient.writeContract({
  address: CONFIG.BONDING_CURVE_ROUTER,
  abi: bondingCurveRouterAbi,
  functionName: "buy",
  args: [
    tokenAddress,
    0n, // minAmountOut (slippage protection)
    account.address // recipient
  ],
  value: parseEther("1"), // Amount of MON to spend
  gas: 500000n
});
```

## 3. Execute Sell (Router)

Sell tokens back to the curve. Note: Requires token approval first.

```typescript
// 1. Approve Router
await walletClient.writeContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: "approve",
  args: [CONFIG.BONDING_CURVE_ROUTER, amountToSell]
});

// 2. Sell
const hash = await walletClient.writeContract({
  address: CONFIG.BONDING_CURVE_ROUTER,
  abi: bondingCurveRouterAbi,
  functionName: "sell",
  args: [
    tokenAddress,
    amountToSell,
    0n, // minAmountOut
    account.address // recipient
  ]
});
```

## 4. Graduation Progress

Track when a token will graduate to a DEX (e.g., Uniswap).

```typescript
const progress = await publicClient.readContract({
  address: CONFIG.LENS,
  abi: lensAbi,
  functionName: "getProgress",
  args: [tokenAddress]
});
// Progress is returned as a percentage (0-100)
```

## Agent Instructions

When asked to "buy the dip" or "check progress":
1.  **Check Balance**: Ensure wallet has MON.
2.  **Get Quote**: Use `Lens` to show the user the expected return.
3.  **Confirm**: Always ask for user confirmation before sending a trade transaction.
4.  **Report**: Provide the transaction hash and current graduation progress.
