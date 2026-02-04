#!/usr/bin/env python3
"""
Check your Scout wallet balance.

Usage:
    python balance.py

Shows your USDC balance and wallet address for funding.
"""

import json
import sys

import requests

from config import BASE_URL, HEADERS, get_api_key, get_wallet_address


def check_balance(api_key: str) -> dict:
    """Check wallet balance."""
    try:
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {api_key}"
        
        response = requests.get(
            f"{BASE_URL}/auth/balance",
            headers=headers,
            timeout=30,
        )
        
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": {"code": "REQUEST_ERROR", "message": str(e)}}
    except Exception as e:
        return {"success": False, "error": {"code": "ERROR", "message": str(e)}}


def main():
    # Auto-load API key from credentials.json
    api_key = get_api_key(required=True)
    wallet_address = get_wallet_address(required=False)
    
    result = check_balance(api_key)
    
    if result.get("success"):
        print(json.dumps({
            "success": True,
            "balance": result.get("balance", "0.00"),
            "currency": "USDC",
            "walletAddress": result.get("walletAddress") or wallet_address,
            "message": f"Fund this address with USDC to buy products.",
        }, indent=2))
    else:
        print(json.dumps(result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
