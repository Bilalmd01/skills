"""
LiquidBot Agent Handler
Professional liquidity pool management
"""

import json
import os
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class Chain(Enum):
    ETHEREUM = 1
    BASE = 8453
    POLYGON = 137
    ARBITRUM = 42161


class Protocol(Enum):
    UNISWAP_V2 = "uniswap_v2"
    UNISWAP_V3 = "uniswap_v3"
    SUSHISWAP = "sushiswap"
    AERODROME = "aerodrome"
    QUICKSWAP = "quickswap"
    CAMELOT = "camelot"


@dataclass
class LPPosition:
    position_id: str
    protocol: Protocol
    chain: Chain
    token0: str
    token1: str
    amount0: Decimal
    amount1: Decimal
    lp_tokens: Decimal
    price_range: Optional[Tuple[Decimal, Decimal]] = None  # For V3
    fee_tier: int = 3000  # For V3


@dataclass
class AddLiquidityParams:
    token0: str
    token1: str
    amount0: Decimal
    amount1: Decimal
    slippage: float = 0.5
    price_lower: Optional[Decimal] = None  # V3 only
    price_upper: Optional[Decimal] = None  # V3 only
    fee_tier: int = 3000  # V3 only


PAYMENT_WALLET = "0x4A9583c6B09154bD88dEE64F5249df0C5EC99Cf9"


class LiquidBotHandler:
    """Main handler for LiquidBot agent"""
    
    def __init__(self):
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r") as f:
            return json.load(f)
    
    async def check_subscription(self, user_id: str) -> Dict[str, Any]:
        """Check if user has active subscription"""
        return {
            "active": False,
            "plan": None,
            "expires_at": None,
            "payment_required": True,
            "payment_wallet": PAYMENT_WALLET
        }
    
    async def generate_payment_request(self, user_id: str, plan: str, chain: Chain) -> Dict[str, Any]:
        """Generate payment request for subscription"""
        pricing = self.config["pricing"]["plans"].get(plan)
        if not pricing:
            raise ValueError(f"Invalid plan: {plan}")
            
        return {
            "user_id": user_id,
            "plan": plan,
            "amount_usd": pricing["price_usd"],
            "payment_wallet": PAYMENT_WALLET,
            "chain": chain.name.lower(),
            "accepted_tokens": self.config["pricing"]["accepted_tokens"],
            "memo": f"liquidbot_{plan}_{user_id}"
        }
    
    async def add_liquidity_v2(
        self,
        wallet: str,
        params: AddLiquidityParams,
        protocol: Protocol,
        chain: Chain
    ) -> Dict[str, Any]:
        """Add liquidity to V2-style pool"""
        
        # Calculate minimum amounts with slippage
        min_amount0 = params.amount0 * Decimal(1 - params.slippage / 100)
        min_amount1 = params.amount1 * Decimal(1 - params.slippage / 100)
        
        tx_params = {
            "token0": params.token0,
            "token1": params.token1,
            "amount0Desired": str(params.amount0),
            "amount1Desired": str(params.amount1),
            "amount0Min": str(min_amount0),
            "amount1Min": str(min_amount1),
            "to": wallet,
            "deadline": "auto"
        }
        
        return {
            "success": True,
            "stage": "pending_signature",
            "protocol": protocol.value,
            "chain": chain.name,
            "tx_params": tx_params,
            "estimated_lp_tokens": "calculated_at_execution"
        }
    
    async def add_liquidity_v3(
        self,
        wallet: str,
        params: AddLiquidityParams,
        chain: Chain
    ) -> Dict[str, Any]:
        """Add concentrated liquidity to V3 pool"""
        
        if not params.price_lower or not params.price_upper:
            raise ValueError("V3 requires price range (price_lower, price_upper)")
        
        # Convert prices to ticks
        tick_lower = self._price_to_tick(params.price_lower, params.fee_tier)
        tick_upper = self._price_to_tick(params.price_upper, params.fee_tier)
        
        tx_params = {
            "token0": params.token0,
            "token1": params.token1,
            "fee": params.fee_tier,
            "tickLower": tick_lower,
            "tickUpper": tick_upper,
            "amount0Desired": str(params.amount0),
            "amount1Desired": str(params.amount1),
            "amount0Min": str(params.amount0 * Decimal(1 - params.slippage / 100)),
            "amount1Min": str(params.amount1 * Decimal(1 - params.slippage / 100)),
            "recipient": wallet,
            "deadline": "auto"
        }
        
        return {
            "success": True,
            "stage": "pending_signature",
            "protocol": "uniswap_v3",
            "chain": chain.name,
            "tx_params": tx_params,
            "price_range": {
                "lower": str(params.price_lower),
                "upper": str(params.price_upper)
            }
        }
    
    async def remove_liquidity(
        self,
        wallet: str,
        position: LPPosition,
        percentage: float = 100.0,
        slippage: float = 0.5
    ) -> Dict[str, Any]:
        """Remove liquidity from position"""
        
        lp_to_remove = position.lp_tokens * Decimal(percentage / 100)
        
        tx_params = {
            "liquidity": str(lp_to_remove),
            "amount0Min": str(position.amount0 * Decimal(percentage / 100) * Decimal(1 - slippage / 100)),
            "amount1Min": str(position.amount1 * Decimal(percentage / 100) * Decimal(1 - slippage / 100)),
            "deadline": "auto"
        }
        
        return {
            "success": True,
            "stage": "pending_signature",
            "position_id": position.position_id,
            "percentage_removed": percentage,
            "tx_params": tx_params
        }
    
    async def get_positions(self, wallet: str, chain: Optional[Chain] = None) -> List[Dict[str, Any]]:
        """Get all LP positions for wallet"""
        # Integration point for actual position fetching
        return []
    
    async def calculate_impermanent_loss(self, position: LPPosition) -> Dict[str, Any]:
        """Calculate impermanent loss for position"""
        # Integration point for IL calculation
        return {
            "position_id": position.position_id,
            "il_percentage": 0.0,
            "il_usd": 0.0,
            "fees_earned_usd": 0.0,
            "net_pnl_usd": 0.0
        }
    
    def _price_to_tick(self, price: Decimal, fee_tier: int) -> int:
        """Convert price to V3 tick"""
        import math
        tick_spacing = {100: 1, 500: 10, 3000: 60, 10000: 200}[fee_tier]
        tick = int(math.log(float(price)) / math.log(1.0001))
        return tick - (tick % tick_spacing)


async def handle_command(
    command: str,
    args: Dict[str, Any],
    user_id: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Main entry point for bot commands"""
    
    handler = LiquidBotHandler()
    
    # Check subscription first
    subscription = await handler.check_subscription(user_id)
    if subscription["payment_required"]:
        return {
            "action": "payment_required",
            "message": "🔐 LiquidBot requires an active subscription",
            "pricing": handler.config["pricing"]["plans"],
            "payment_wallet": PAYMENT_WALLET
        }
    
    chain = Chain(args.get("chain_id", 8453))
    
    if command == "add_liquidity":
        params = AddLiquidityParams(
            token0=args["token0"],
            token1=args["token1"],
            amount0=Decimal(args["amount0"]),
            amount1=Decimal(args["amount1"]),
            slippage=args.get("slippage", 0.5),
            price_lower=Decimal(args["price_lower"]) if args.get("price_lower") else None,
            price_upper=Decimal(args["price_upper"]) if args.get("price_upper") else None,
            fee_tier=args.get("fee_tier", 3000)
        )
        
        if params.price_lower and params.price_upper:
            return await handler.add_liquidity_v3(args["wallet"], params, chain)
        else:
            protocol = Protocol(args.get("protocol", "uniswap_v2"))
            return await handler.add_liquidity_v2(args["wallet"], params, protocol, chain)
    
    elif command == "remove_liquidity":
        position = LPPosition(
            position_id=args["position_id"],
            protocol=Protocol(args.get("protocol", "uniswap_v2")),
            chain=chain,
            token0=args["token0"],
            token1=args["token1"],
            amount0=Decimal(args.get("amount0", 0)),
            amount1=Decimal(args.get("amount1", 0)),
            lp_tokens=Decimal(args["lp_tokens"])
        )
        return await handler.remove_liquidity(
            args["wallet"],
            position,
            args.get("percentage", 100.0),
            args.get("slippage", 0.5)
        )
    
    elif command == "get_positions":
        return {
            "positions": await handler.get_positions(args["wallet"], chain)
        }
    
    return {"error": f"Unknown command: {command}"}
