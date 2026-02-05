#!/usr/bin/env python3
"""
Deck Report Generator for MTG Commander

Analyzes a deck file and generates statistics about:
- Mana curve
- Card type distribution
- Color distribution
- Category breakdown
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from collections import defaultdict
from typing import List, Dict, Tuple

SCRYFALL_BASE = "https://api.scryfall.com"
HEADERS = {
    "User-Agent": "MTGDeckBuilder/1.0",
    "Accept": "application/json"
}

def make_request(url: str) -> dict:
    """Make a request to Scryfall API."""
    time.sleep(0.1)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())

def get_card_data(card_name: str) -> dict:
    """Fetch card data from Scryfall."""
    encoded = urllib.parse.quote(card_name)
    url = f"{SCRYFALL_BASE}/cards/named?fuzzy={encoded}"
    try:
        return make_request(url)
    except:
        return {"error": True, "name": card_name}

def get_cards_batch(card_names: List[str]) -> List[dict]:
    """Fetch multiple cards using collection endpoint."""
    # Split into batches of 75
    results = []
    for i in range(0, len(card_names), 75):
        batch = card_names[i:i+75]
        identifiers = [{"name": name} for name in batch]
        
        data = json.dumps({"identifiers": identifiers}).encode()
        req = urllib.request.Request(
            f"{SCRYFALL_BASE}/cards/collection",
            data=data,
            headers={**HEADERS, "Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                results.extend(result.get("data", []))
        except Exception as e:
            print(f"Batch fetch error: {e}", file=sys.stderr)
        
        time.sleep(0.1)
    
    return results

def parse_deck_file(filepath: str) -> List[Tuple[int, str]]:
    """Parse a deck file."""
    deck = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines, comments, and section headers
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # Handle "SIDEBOARD" or "COMMANDER" sections
            if line.upper() in ['SIDEBOARD', 'COMMANDER', 'MAINDECK', 'COMPANION']:
                continue
            
            # Parse "N Card Name" or just "Card Name"
            match = re.match(r'^(\d+)[x\s]+(.+)$', line, re.IGNORECASE)
            if match:
                qty = int(match.group(1))
                name = match.group(2).strip()
            else:
                qty = 1
                name = line
            
            # Clean up card name
            name = re.sub(r'\s*\([^)]+\)\s*$', '', name)  # Remove set codes
            name = re.sub(r'\s*#\d+\s*$', '', name)  # Remove collector numbers
            
            deck.append((qty, name))
    
    return deck

def categorize_card(card: dict) -> str:
    """Categorize a card by its primary function."""
    type_line = card.get("type_line", "").lower()
    oracle_text = card.get("oracle_text", "").lower()
    name = card.get("name", "").lower()
    
    # Check type first
    if "land" in type_line:
        return "Land"
    
    if "creature" in type_line:
        # Sub-categorize creatures
        if any(word in oracle_text for word in ["add {", "mana", "search your library for a basic land"]):
            return "Ramp"
        if "draw" in oracle_text and "card" in oracle_text:
            return "Card Draw"
        return "Creature"
    
    # Check for ramp
    if any(word in oracle_text for word in ["add {c}", "add {w}", "add {u}", "add {b}", "add {r}", "add {g}"]):
        return "Ramp"
    if "search your library for" in oracle_text and "land" in oracle_text:
        return "Ramp"
    
    # Check for removal
    if any(word in oracle_text for word in ["destroy target", "exile target", "deals", "damage to target"]):
        if "creature" in oracle_text or "permanent" in oracle_text:
            return "Removal"
    if "destroy all" in oracle_text or "exile all" in oracle_text:
        return "Board Wipe"
    
    # Check for card draw
    if "draw" in oracle_text and "card" in oracle_text:
        return "Card Draw"
    
    # Check for counterspells
    if "counter target" in oracle_text:
        return "Counterspell"
    
    # Check for protection
    if any(word in oracle_text for word in ["hexproof", "indestructible", "protection from"]):
        return "Protection"
    
    # Default by type
    if "instant" in type_line:
        return "Instant"
    if "sorcery" in type_line:
        return "Sorcery"
    if "artifact" in type_line:
        return "Artifact"
    if "enchantment" in type_line:
        return "Enchantment"
    if "planeswalker" in type_line:
        return "Planeswalker"
    
    return "Other"

def analyze_deck(deck: List[Tuple[int, str]], cards_data: List[dict]) -> dict:
    """Generate deck statistics."""
    
    # Create lookup by name
    card_lookup = {}
    for card in cards_data:
        card_lookup[card.get("name", "").lower()] = card
        # Handle double-faced cards
        if "card_faces" in card:
            for face in card["card_faces"]:
                card_lookup[face.get("name", "").lower()] = card
    
    stats = {
        "total_cards": 0,
        "mana_curve": defaultdict(int),
        "types": defaultdict(int),
        "categories": defaultdict(int),
        "colors": defaultdict(int),
        "color_identity": set(),
        "missing_cards": [],
        "average_cmc": 0,
        "land_count": 0,
        "nonland_count": 0,
        "cards_by_cmc": defaultdict(list)
    }
    
    total_cmc = 0
    nonland_count = 0
    
    for qty, name in deck:
        stats["total_cards"] += qty
        
        card = card_lookup.get(name.lower())
        if not card:
            stats["missing_cards"].append(name)
            continue
        
        type_line = card.get("type_line", "").lower()
        cmc = int(card.get("cmc", 0))
        
        # Get mana cost from front face if needed
        if "card_faces" in card:
            cmc = int(card["card_faces"][0].get("cmc", card.get("cmc", 0)))
        
        # Color identity
        for color in card.get("color_identity", []):
            stats["color_identity"].add(color)
            stats["colors"][color] += qty
        
        # Type distribution
        for card_type in ["creature", "instant", "sorcery", "artifact", "enchantment", "planeswalker", "land"]:
            if card_type in type_line:
                stats["types"][card_type.capitalize()] += qty
                break
        
        # Category
        category = categorize_card(card)
        stats["categories"][category] += qty
        
        # Mana curve (excluding lands)
        if "land" not in type_line:
            stats["mana_curve"][cmc] += qty
            stats["cards_by_cmc"][cmc].append(name)
            total_cmc += cmc * qty
            nonland_count += qty
            stats["nonland_count"] += qty
        else:
            stats["land_count"] += qty
    
    # Calculate average CMC
    if nonland_count > 0:
        stats["average_cmc"] = round(total_cmc / nonland_count, 2)
    
    # Convert sets to lists for JSON serialization
    stats["color_identity"] = sorted(list(stats["color_identity"]))
    stats["mana_curve"] = dict(sorted(stats["mana_curve"].items()))
    stats["types"] = dict(stats["types"])
    stats["categories"] = dict(stats["categories"])
    stats["colors"] = dict(stats["colors"])
    stats["cards_by_cmc"] = {k: v for k, v in sorted(stats["cards_by_cmc"].items())}
    
    return stats

def generate_text_report(stats: dict, format_name: str) -> str:
    """Generate a human-readable report."""
    lines = []
    
    lines.append("=" * 60)
    lines.append(f"DECK ANALYSIS REPORT - {format_name.upper()}")
    lines.append("=" * 60)
    lines.append("")
    
    # Overview
    lines.append("📊 OVERVIEW")
    lines.append("-" * 40)
    lines.append(f"Total Cards: {stats['total_cards']}")
    lines.append(f"Lands: {stats['land_count']}")
    lines.append(f"Nonlands: {stats['nonland_count']}")
    lines.append(f"Average CMC (nonlands): {stats['average_cmc']}")
    lines.append(f"Color Identity: {', '.join(stats['color_identity']) or 'Colorless'}")
    lines.append("")
    
    # Mana Curve
    lines.append("📈 MANA CURVE")
    lines.append("-" * 40)
    max_count = max(stats['mana_curve'].values()) if stats['mana_curve'] else 1
    
    for cmc in range(0, max(stats['mana_curve'].keys(), default=0) + 1):
        count = stats['mana_curve'].get(cmc, 0)
        bar_length = int((count / max_count) * 30)
        bar = "█" * bar_length
        lines.append(f"{cmc}cmc [{count:2d}] {bar}")
    lines.append("")
    
    # Card Types
    lines.append("🃏 CARD TYPES")
    lines.append("-" * 40)
    for card_type, count in sorted(stats['types'].items(), key=lambda x: -x[1]):
        lines.append(f"{card_type}: {count}")
    lines.append("")
    
    # Categories
    lines.append("📁 CATEGORIES")
    lines.append("-" * 40)
    for category, count in sorted(stats['categories'].items(), key=lambda x: -x[1]):
        lines.append(f"{category}: {count}")
    lines.append("")
    
    # Color Distribution
    lines.append("🎨 COLOR DISTRIBUTION")
    lines.append("-" * 40)
    color_names = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green"}
    for color, count in sorted(stats['colors'].items()):
        lines.append(f"{color_names.get(color, color)}: {count}")
    lines.append("")
    
    # Missing cards warning
    if stats['missing_cards']:
        lines.append("⚠️  MISSING CARDS (not found in Scryfall)")
        lines.append("-" * 40)
        for card in stats['missing_cards']:
            lines.append(f"  - {card}")
        lines.append("")
    
    # Recommendations
    lines.append("💡 RECOMMENDATIONS")
    lines.append("-" * 40)
    
    if stats['land_count'] < 33:
        lines.append(f"⚠ Low land count ({stats['land_count']}). Consider adding {35 - stats['land_count']} more lands.")
    elif stats['land_count'] > 40:
        lines.append(f"⚠ High land count ({stats['land_count']}). Consider cutting {stats['land_count'] - 38} lands.")
    
    if stats['average_cmc'] > 3.5:
        lines.append(f"⚠ High average CMC ({stats['average_cmc']}). Consider adding more low-cost cards or ramp.")
    
    ramp_count = stats['categories'].get('Ramp', 0)
    if ramp_count < 8:
        lines.append(f"⚠ Low ramp count ({ramp_count}). Consider adding {10 - ramp_count} more ramp pieces.")
    
    draw_count = stats['categories'].get('Card Draw', 0)
    if draw_count < 8:
        lines.append(f"⚠ Low card draw ({draw_count}). Consider adding {10 - draw_count} more draw effects.")
    
    if not stats.get('categories', {}).get('Board Wipe') and not stats.get('categories', {}).get('Removal'):
        lines.append("⚠ No interaction found. Consider adding removal and board wipes.")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Analyze MTG Commander deck")
    
    parser.add_argument("--deck", "-d", required=True, help="Deck file path")
    parser.add_argument("--format", "-f", choices=["commander", "duel"], default="commander", help="Format")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    print("Parsing deck file...", file=sys.stderr)
    deck = parse_deck_file(args.deck)
    
    print(f"Fetching data for {len(deck)} unique cards...", file=sys.stderr)
    card_names = [name for _, name in deck]
    cards_data = get_cards_batch(card_names)
    
    print("Analyzing deck...", file=sys.stderr)
    stats = analyze_deck(deck, cards_data)
    
    if args.json:
        output = json.dumps(stats, indent=2)
    else:
        output = generate_text_report(stats, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
