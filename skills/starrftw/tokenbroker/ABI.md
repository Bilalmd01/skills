# ABI.md - Smart Contract Interfaces

Reference ABIs for TokenBroker / nad.fun integration.

## BondingCurveRouter

Used for **Creating**, **Buying**, and **Selling**.

```typescript
export const bondingCurveRouterAbi = [
  {
    type: "function",
    name: "create",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "name", type: "string" },
          { name: "symbol", type: "string" },
          { name: "tokenURI", type: "string" },
          { name: "amountOut", type: "uint256" },
          { name: "salt", type: "bytes32" },
          { name: "actionId", type: "uint8" }
        ]
      }
    ],
    outputs: [
      { name: "token", type: "address" },
      { name: "pool", type: "address" }
    ],
    stateMutability: "payable"
  }
  // ... (buy/sell functions omitted for brevity, see nad.fun/abi.md)
] as const;
```

## Lens

Used for **Price Quotes** and **Progress**.

```typescript
export const lensAbi = [
  {
    type: "function",
    name: "getInitialBuyAmountOut",
    inputs: [{ name: "amountIn", type: "uint256" }],
    outputs: [{ type: "uint256" }],
    stateMutability: "view"
  },
  {
    type: "function",
    name: "getProgress",
    inputs: [{ name: "_token", type: "address" }],
    outputs: [{ name: "progress", type: "uint256" }],
    stateMutability: "view"
  }
] as const;
```

## Curve

Used for **Fees** and **State**.

```typescript
export const curveAbi = [
  {
    type: "function",
    name: "feeConfig",
    inputs: [],
    outputs: [
      { name: "deployFeeAmount", type: "uint256" },
      { name: "graduateFeeAmount", type: "uint256" },
      { name: "protocolFee", type: "uint24" }
    ],
    stateMutability: "view"
  },
  {
    type: "event",
    name: "CurveCreate",
    inputs: [
      { name: "token", type: "address", indexed: true },
      { name: "pool", type: "address", indexed: true }
    ],
    anonymous: false
  }
] as const;
```
