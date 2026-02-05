#!/usr/bin/env python3
"""
Metagame Data Fetcher for MTG Commander Formats

Fetches current metagame data from multiple sources:
- MTGGoldfish (Duel Commander, Commander)
- MTGTop8 (tournament results)
- EDHREC (card recommendations)
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from typing import Dict, List, Optional

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

# =============================================================================
# MTGGoldfish Parser
# =============================================================================

class MTGGoldfishMetaParser(HTMLParser):
    """Parse metagame data from MTGGoldfish."""
    
    def __init__(self):
        super().__init__()
        self.decks = []
        self.current_deck = {}
        self.in_deck_tile = False
        self.in_deck_name = False
        self.in_meta_percent = False
        self.in_price = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get("class", "")
        
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if "/archetype/" in href and "duel_commander" in href:
                self.in_deck_tile = True
                self.current_deck = {"url": href}
                
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.in_deck_tile:
            # Try to extract commander name
            if not self.current_deck.get("name") and len(data) > 3:
                if not data.startswith("$") and not data.endswith("%") and not data.endswith("tix"):
                    self.current_deck["name"] = data
            
            # Extract meta percentage
            if "%" in data and len(data) < 10:
                match = re.search(r'([\d.]+)%', data)
                if match:
                    self.current_deck["meta_percent"] = float(match.group(1))
            
            # Extract price
            if data.startswith("$"):
                match = re.search(r'\$([\d,]+)', data)
                if match:
                    self.current_deck["price_usd"] = int(match.group(1).replace(",", ""))
                    
    def handle_endtag(self, tag):
        if tag == "a" and self.in_deck_tile:
            if self.current_deck.get("name"):
                self.decks.append(self.current_deck)
            self.in_deck_tile = False
            self.current_deck = {}


def fetch_mtggoldfish_meta(format_name: str = "duel_commander") -> Dict:
    """
    Fetch metagame data from MTGGoldfish.
    
    Args:
        format_name: 'duel_commander' or 'commander'
    
    Returns:
        Dict with metagame breakdown
    """
    url = f"https://www.mtggoldfish.com/metagame/{format_name}"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {"error": str(e), "source": "mtggoldfish"}
    
    # Parse the HTML
    parser = MTGGoldfishMetaParser()
    parser.feed(html)
    
    # Also try regex extraction for more reliable results
    decks = []
    
    # Pattern for deck entries
    deck_pattern = re.compile(
        r'archetype/[^"]+' + format_name + r'-([^"#]+)',
        re.IGNORECASE
    )
    
    meta_pattern = re.compile(r'(\d+\.?\d*)%\s*\((\d+)\)')
    
    for match in deck_pattern.finditer(html):
        commander = match.group(1).replace("-", " ").title()
        decks.append({"name": commander})
    
    # Deduplicate
    seen = set()
    unique_decks = []
    for d in parser.decks + decks:
        name = d.get("name", "").lower()
        if name and name not in seen:
            seen.add(name)
            unique_decks.append(d)
    
    return {
        "source": "mtggoldfish",
        "format": format_name,
        "url": url,
        "decks": unique_decks[:20],  # Top 20
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# =============================================================================
# MTGTop8 Parser
# =============================================================================

def fetch_mtgtop8_events(format_code: str = "EDH", limit: int = 10) -> Dict:
    """
    Fetch recent tournament results from MTGTop8.
    
    Args:
        format_code: 'EDH' for Duel Commander
        limit: Max events to return
    
    Returns:
        Dict with tournament data
    """
    url = f"https://mtgtop8.com/format?f={format_code}"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('latin-1', errors='ignore')
    except Exception as e:
        return {"error": str(e), "source": "mtgtop8"}
    
    events = []
    
    # Extract event links
    event_pattern = re.compile(r'event\?e=(\d+)&f=' + format_code + r'[^"]*"[^>]*>([^<]+)')
    
    for match in event_pattern.finditer(html):
        event_id = match.group(1)
        event_name = match.group(2).strip()
        if event_name and len(event_name) > 3:
            events.append({
                "id": event_id,
                "name": event_name,
                "url": f"https://mtgtop8.com/event?e={event_id}&f={format_code}"
            })
    
    # Extract most played cards
    cards = []
    card_pattern = re.compile(r'(\d+)\s*%.*?card\?ref=([a-z0-9]+)', re.IGNORECASE | re.DOTALL)
    
    for match in card_pattern.finditer(html):
        percent = match.group(1)
        card_ref = match.group(2)
        cards.append({"percent": int(percent), "ref": card_ref})
    
    return {
        "source": "mtgtop8",
        "format": format_code,
        "url": url,
        "recent_events": events[:limit],
        "most_played_cards": cards[:10],
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# =============================================================================
# EDHREC Helper
# =============================================================================

def fetch_edhrec_commander(commander_name: str) -> Dict:
    """
    Fetch commander data from EDHREC.
    
    Args:
        commander_name: Name of the commander
    
    Returns:
        Dict with commander recommendations
    """
    # Format commander name for URL
    slug = commander_name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    
    url = f"https://edhrec.com/commanders/{slug}"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {"error": str(e), "source": "edhrec", "commander": commander_name}
    
    # Extract deck count
    deck_count = None
    count_match = re.search(r'([\d,]+)\s*decks?', html, re.IGNORECASE)
    if count_match:
        deck_count = int(count_match.group(1).replace(",", ""))
    
    # Extract card recommendations (simplified)
    cards = []
    card_pattern = re.compile(r'"cardname":\s*"([^"]+)".*?"synergy":\s*([\d.-]+)', re.DOTALL)
    
    for match in card_pattern.finditer(html[:50000]):  # Limit search
        cards.append({
            "name": match.group(1),
            "synergy": float(match.group(2))
        })
    
    return {
        "source": "edhrec",
        "commander": commander_name,
        "url": url,
        "deck_count": deck_count,
        "recommended_cards": sorted(cards, key=lambda x: -x["synergy"])[:20],
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Fetch MTG metagame data")
    
    parser.add_argument("--source", "-s", 
                        choices=["mtggoldfish", "mtgtop8", "edhrec", "all"],
                        default="mtggoldfish",
                        help="Data source to fetch from")
    parser.add_argument("--format", "-f",
                        choices=["duel_commander", "commander"],
                        default="duel_commander",
                        help="MTG format")
    parser.add_argument("--commander", "-c",
                        help="Commander name (for EDHREC)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--limit", "-l", type=int, default=10,
                        help="Limit results")
    
    args = parser.parse_args()
    
    results = {}
    
    if args.source in ["mtggoldfish", "all"]:
        print("Fetching MTGGoldfish data...", file=sys.stderr)
        results["mtggoldfish"] = fetch_mtggoldfish_meta(args.format)
    
    if args.source in ["mtgtop8", "all"]:
        print("Fetching MTGTop8 data...", file=sys.stderr)
        format_code = "EDH" if args.format == "duel_commander" else "cEDH"
        results["mtgtop8"] = fetch_mtgtop8_events(format_code, args.limit)
    
    if args.source == "edhrec" or (args.source == "all" and args.commander):
        if not args.commander:
            print("Error: --commander required for EDHREC", file=sys.stderr)
            sys.exit(1)
        print(f"Fetching EDHREC data for {args.commander}...", file=sys.stderr)
        results["edhrec"] = fetch_edhrec_commander(args.commander)
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for source, data in results.items():
            print(f"\n{'='*60}")
            print(f"SOURCE: {source.upper()}")
            print(f"{'='*60}")
            
            if "error" in data:
                print(f"Error: {data['error']}")
                continue
            
            if source == "mtggoldfish":
                print(f"Format: {data.get('format')}")
                print(f"URL: {data.get('url')}")
                print(f"\nTop Decks:")
                for i, deck in enumerate(data.get("decks", [])[:10], 1):
                    name = deck.get("name", "Unknown")
                    meta = deck.get("meta_percent", "?")
                    price = deck.get("price_usd", "?")
                    print(f"  {i}. {name} ({meta}% meta, ${price})")
            
            elif source == "mtgtop8":
                print(f"\nRecent Events:")
                for event in data.get("recent_events", [])[:5]:
                    print(f"  - {event['name']}")
                print(f"\nMost Played Cards:")
                for card in data.get("most_played_cards", [])[:5]:
                    print(f"  - {card['percent']}%: {card['ref']}")
            
            elif source == "edhrec":
                print(f"Commander: {data.get('commander')}")
                print(f"Deck Count: {data.get('deck_count', 'Unknown')}")
                print(f"\nTop Synergy Cards:")
                for card in data.get("recommended_cards", [])[:10]:
                    print(f"  +{card['synergy']}% {card['name']}")

if __name__ == "__main__":
    main()
