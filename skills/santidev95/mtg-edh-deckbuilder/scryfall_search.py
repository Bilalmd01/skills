#!/usr/bin/env python3
"""
Scryfall API Search Tool for MTG Commander Deck Building
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://api.scryfall.com"
HEADERS = {
    "User-Agent": "MTGDeckBuilder/1.0",
    "Accept": "application/json"
}

def make_request(url: str) -> dict:
    """Make a request to Scryfall API with rate limiting."""
    time.sleep(0.1)  # 100ms delay between requests
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": "not_found", "details": "Card not found"}
        raise

def search_cards(query: str, limit: int = 50, unique: str = "cards") -> list:
    """
    Search for cards using Scryfall syntax.
    
    Args:
        query: Scryfall search query
        limit: Maximum cards to return
        unique: 'cards', 'art', or 'prints'
    
    Returns:
        List of card objects
    """
    encoded_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/cards/search?q={encoded_query}&unique={unique}"
    
    cards = []
    while url and len(cards) < limit:
        data = make_request(url)
        
        if "error" in data:
            if data.get("code") == "not_found":
                return []
            print(f"Error: {data.get('details', 'Unknown error')}", file=sys.stderr)
            return cards
        
        cards.extend(data.get("data", []))
        url = data.get("next_page") if data.get("has_more") else None
    
    return cards[:limit]

def get_card_by_name(name: str, fuzzy: bool = True) -> dict:
    """
    Get a specific card by name.
    
    Args:
        name: Card name
        fuzzy: Use fuzzy matching (default) or exact
    
    Returns:
        Card object or error dict
    """
    encoded_name = urllib.parse.quote(name)
    match_type = "fuzzy" if fuzzy else "exact"
    url = f"{BASE_URL}/cards/named?{match_type}={encoded_name}"
    
    return make_request(url)

def format_card(card: dict, verbose: bool = False) -> str:
    """Format a card for display."""
    name = card.get("name", "Unknown")
    mana_cost = card.get("mana_cost", "")
    type_line = card.get("type_line", "")
    
    # Handle double-faced cards
    if "card_faces" in card and not mana_cost:
        mana_cost = card["card_faces"][0].get("mana_cost", "")
    
    cmc = card.get("cmc", 0)
    
    line = f"{name} {mana_cost} ({int(cmc)}) - {type_line}"
    
    if verbose:
        oracle = card.get("oracle_text", "")
        if "card_faces" in card:
            oracle = " // ".join(f.get("oracle_text", "") for f in card["card_faces"])
        
        prices = card.get("prices", {})
        usd = prices.get("usd") or prices.get("usd_foil") or "N/A"
        
        legalities = card.get("legalities", {})
        commander_legal = legalities.get("commander", "unknown")
        duel_legal = legalities.get("duel", "unknown")
        
        line += f"\n  Oracle: {oracle[:200]}..."
        line += f"\n  USD: ${usd} | Commander: {commander_legal} | Duel: {duel_legal}"
    
    return line

def check_commander_legal(card: dict, format_name: str = "commander") -> dict:
    """
    Check if a card can be a commander.
    
    Returns dict with:
        - is_legendary: bool
        - can_be_commander: bool  
        - is_legal: bool (not banned)
        - color_identity: list
    """
    type_line = card.get("type_line", "").lower()
    oracle_text = card.get("oracle_text", "").lower()
    
    is_legendary = "legendary" in type_line
    is_creature = "creature" in type_line
    
    # Check for "can be your commander" text
    can_be_commander_text = "can be your commander" in oracle_text
    
    can_be_commander = (is_legendary and is_creature) or can_be_commander_text
    
    # Check legality
    legalities = card.get("legalities", {})
    format_key = "duel" if format_name == "duel" else "commander"
    is_legal = legalities.get(format_key) == "legal"
    
    return {
        "name": card.get("name"),
        "is_legendary": is_legendary,
        "can_be_commander": can_be_commander,
        "is_legal": is_legal,
        "color_identity": card.get("color_identity", []),
        "format": format_name
    }

def get_cards_in_color_identity(colors: str, card_type: str = None, limit: int = 50) -> list:
    """
    Get cards within a color identity.
    
    Args:
        colors: Color identity string (e.g., "wubrg", "rg", "u")
        card_type: Optional type filter (e.g., "creature", "instant")
        limit: Max results
    """
    query = f"ci<={colors} f:commander"
    if card_type:
        query += f" t:{card_type}"
    
    return search_cards(query, limit)

def main():
    parser = argparse.ArgumentParser(description="Search Scryfall for MTG cards")
    
    parser.add_argument("--query", "-q", help="Scryfall search query")
    parser.add_argument("--name", "-n", help="Get card by name")
    parser.add_argument("--exact", action="store_true", help="Use exact name matching")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Max results (default: 50)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed card info")
    parser.add_argument("--check-commander", action="store_true", help="Check if card can be commander")
    parser.add_argument("--format", "-f", choices=["commander", "duel"], default="commander", help="Format to check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--color-identity", "-ci", help="Get cards in color identity (e.g., 'ug' for Simic)")
    parser.add_argument("--type", "-t", help="Card type filter (used with --color-identity)")
    
    args = parser.parse_args()
    
    if args.name:
        card = get_card_by_name(args.name, fuzzy=not args.exact)
        
        if "error" in card:
            print(f"Error: {card.get('details', 'Card not found')}", file=sys.stderr)
            sys.exit(1)
        
        if args.check_commander:
            result = check_commander_legal(card, args.format)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Commander Check for: {result['name']}")
                print(f"  Format: {result['format']}")
                print(f"  Is Legendary: {result['is_legendary']}")
                print(f"  Can be Commander: {result['can_be_commander']}")
                print(f"  Is Legal: {result['is_legal']}")
                print(f"  Color Identity: {', '.join(result['color_identity']) or 'Colorless'}")
        else:
            if args.json:
                print(json.dumps(card, indent=2))
            else:
                print(format_card(card, args.verbose))
    
    elif args.color_identity:
        cards = get_cards_in_color_identity(args.color_identity, args.type, args.limit)
        
        if args.json:
            print(json.dumps(cards, indent=2))
        else:
            print(f"Found {len(cards)} cards in color identity '{args.color_identity}':")
            for card in cards:
                print(f"  {format_card(card, args.verbose)}")
    
    elif args.query:
        cards = search_cards(args.query, args.limit)
        
        if args.json:
            print(json.dumps(cards, indent=2))
        else:
            print(f"Found {len(cards)} cards:")
            for card in cards:
                print(f"  {format_card(card, args.verbose)}")
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
