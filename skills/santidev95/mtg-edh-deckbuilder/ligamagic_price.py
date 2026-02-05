#!/usr/bin/env python3
"""
LigaMagic Price Scraper for MTG Cards

Note: LigaMagic does not have a public API, so this uses web scraping.
Always respect rate limits and the site's terms of service.

REQUIREMENTS:
    pip install cloudscraper

The cloudscraper library is required to bypass Cloudflare protection.
Without it, the script will fail when accessing LigaMagic.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
from html.parser import HTMLParser
from typing import Optional

try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False
    import urllib.request
    import urllib.error

BASE_URL = "https://www.ligamagic.com.br"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

class LigaMagicPriceParser(HTMLParser):
    """Parser to extract price information from LigaMagic card pages."""
    
    def __init__(self):
        super().__init__()
        self.prices = []
        self.current_price = None
        self.in_price_div = False
        self.in_price_value = False
        self.current_condition = None
        self.current_edition = None
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Look for price containers
        if tag == "div" and "class" in attrs_dict:
            classes = attrs_dict["class"]
            if "card-price" in classes or "menor-preco" in classes:
                self.in_price_div = True
                self.current_price = {}
        
        # Look for price value spans
        if tag == "span" and self.in_price_div:
            if "class" in attrs_dict and "preco" in attrs_dict["class"]:
                self.in_price_value = True
    
    def handle_data(self, data):
        if self.in_price_value:
            # Extract price value (format: R$ XX,XX)
            price_match = re.search(r'R\$\s*([\d.,]+)', data)
            if price_match:
                price_str = price_match.group(1).replace('.', '').replace(',', '.')
                try:
                    self.current_price["value"] = float(price_str)
                    self.current_price["formatted"] = f"R$ {price_match.group(1)}"
                except ValueError:
                    pass
    
    def handle_endtag(self, tag):
        if tag == "span" and self.in_price_value:
            self.in_price_value = False
        
        if tag == "div" and self.in_price_div:
            if self.current_price and "value" in self.current_price:
                self.prices.append(self.current_price)
            self.current_price = None
            self.in_price_div = False

def search_card_url(card_name: str) -> Optional[str]:
    """
    Get the LigaMagic URL for a card.
    
    Args:
        card_name: English card name
    
    Returns:
        URL string or None if not found
    """
    encoded_name = urllib.parse.quote(card_name.replace(" ", "+"))
    search_url = f"{BASE_URL}/?view=cards/search&card={encoded_name}"
    return search_url

def get_card_prices(card_name: str, edition: str = None) -> dict:
    """
    Get prices for a card from LigaMagic.
    
    Args:
        card_name: Card name (English or Portuguese)
        edition: Optional edition filter
    
    Returns:
        Dict with price information
    """
    time.sleep(0.5)  # Rate limiting
    
    url = search_card_url(card_name)
    
    try:
        if HAS_CLOUDSCRAPER:
            # Use cloudscraper to bypass Cloudflare
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                }
            )
            response = scraper.get(url, headers=HEADERS, timeout=30)
            html = response.text
        else:
            # Fallback to urllib (may not work with Cloudflare)
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        error_msg = str(e)
        # Check for Cloudflare-related errors
        if not HAS_CLOUDSCRAPER:
            return {
                "error": "cloudscraper não está instalado. LigaMagic é protegido por Cloudflare. Instale com: pip install cloudscraper",
                "card": card_name,
                "url": url
            }
        if "cloudflare" in error_msg.lower() or "403" in error_msg or "challenge" in error_msg.lower() or "cf-ray" in error_msg.lower():
            return {
                "error": f"Cloudflare bloqueou o acesso: {error_msg}. Tente novamente em alguns segundos.",
                "card": card_name,
                "url": url
            }
        return {"error": error_msg, "card": card_name, "url": url}
    
    # Try to extract prices using regex (more reliable than HTML parsing)
    result = {
        "card": card_name,
        "url": url,
        "prices": []
    }
    
    # Pattern for minimum price
    min_price_match = re.search(r'menor[^>]*>.*?R\$\s*([\d.,]+)', html, re.IGNORECASE | re.DOTALL)
    if min_price_match:
        price_str = min_price_match.group(1).replace('.', '').replace(',', '.')
        try:
            result["min_price"] = float(price_str)
            result["min_price_formatted"] = f"R$ {min_price_match.group(1)}"
        except ValueError:
            pass
    
    # Pattern for average price
    avg_price_match = re.search(r'm[ée]dio[^>]*>.*?R\$\s*([\d.,]+)', html, re.IGNORECASE | re.DOTALL)
    if avg_price_match:
        price_str = avg_price_match.group(1).replace('.', '').replace(',', '.')
        try:
            result["avg_price"] = float(price_str)
            result["avg_price_formatted"] = f"R$ {avg_price_match.group(1)}"
        except ValueError:
            pass
    
    # Extract individual store prices
    price_pattern = re.compile(r'R\$\s*([\d]+[.,][\d]{2})', re.MULTILINE)
    all_prices = price_pattern.findall(html)
    
    if all_prices:
        numeric_prices = []
        for p in all_prices:
            try:
                numeric_prices.append(float(p.replace('.', '').replace(',', '.')))
            except ValueError:
                continue
        
        if numeric_prices:
            numeric_prices.sort()
            # Filter out unreasonably low/high prices
            filtered = [p for p in numeric_prices if 0.5 < p < 50000]
            
            if filtered:
                if "min_price" not in result:
                    result["min_price"] = min(filtered)
                    result["min_price_formatted"] = f"R$ {min(filtered):.2f}".replace('.', ',')
                
                result["price_range"] = {
                    "min": min(filtered),
                    "max": max(filtered),
                    "count": len(filtered)
                }
    
    return result

def get_deck_prices(deck_list: list) -> dict:
    """
    Get prices for an entire deck.
    
    Args:
        deck_list: List of tuples (quantity, card_name)
    
    Returns:
        Dict with total and per-card prices
    """
    result = {
        "cards": [],
        "total_min": 0,
        "total_avg": 0,
        "not_found": []
    }
    
    for qty, card_name in deck_list:
        print(f"Fetching price for: {card_name}...", file=sys.stderr)
        price_data = get_card_prices(card_name)
        
        if "error" in price_data or "min_price" not in price_data:
            result["not_found"].append(card_name)
            continue
        
        card_result = {
            "name": card_name,
            "quantity": qty,
            "unit_price": price_data.get("min_price", 0),
            "total": price_data.get("min_price", 0) * qty
        }
        
        result["cards"].append(card_result)
        result["total_min"] += card_result["total"]
        
        if "avg_price" in price_data:
            result["total_avg"] += price_data["avg_price"] * qty
    
    return result

def parse_deck_file(filepath: str) -> list:
    """
    Parse a deck file in standard format.
    
    Expected format:
    1 Card Name
    4 Another Card
    
    Returns:
        List of (quantity, card_name) tuples
    """
    deck = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # Try to parse "N Card Name" format
            match = re.match(r'^(\d+)\s+(.+)$', line)
            if match:
                qty = int(match.group(1))
                name = match.group(2).strip()
                deck.append((qty, name))
            else:
                # Assume single card
                deck.append((1, line))
    
    return deck

def main():
    parser = argparse.ArgumentParser(description="Get MTG card prices from LigaMagic")
    
    parser.add_argument("--card", "-c", help="Single card name to price")
    parser.add_argument("--deck", "-d", help="Deck file path to price")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--budget", "-b", type=float, help="Budget limit in BRL (filters suggestions)")
    
    args = parser.parse_args()
    
    if args.card:
        result = get_card_prices(args.card)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nCard: {result['card']}")
            print(f"URL: {result['url']}")
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                if "min_price_formatted" in result:
                    print(f"Minimum Price: {result['min_price_formatted']}")
                if "avg_price_formatted" in result:
                    print(f"Average Price: {result['avg_price_formatted']}")
                if "price_range" in result:
                    pr = result["price_range"]
                    print(f"Price Range: R$ {pr['min']:.2f} - R$ {pr['max']:.2f} ({pr['count']} offers)")
    
    elif args.deck:
        deck = parse_deck_file(args.deck)
        result = get_deck_prices(deck)
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n{'='*60}")
            print("DECK PRICE BREAKDOWN")
            print(f"{'='*60}\n")
            
            # Sort by total price descending
            sorted_cards = sorted(result["cards"], key=lambda x: x["total"], reverse=True)
            
            for card in sorted_cards:
                print(f"{card['quantity']}x {card['name']}: R$ {card['total']:.2f} (R$ {card['unit_price']:.2f} each)")
            
            print(f"\n{'-'*60}")
            print(f"TOTAL (Min Prices): R$ {result['total_min']:.2f}")
            if result["total_avg"] > 0:
                print(f"TOTAL (Avg Prices): R$ {result['total_avg']:.2f}")
            
            if result["not_found"]:
                print(f"\nCards not found ({len(result['not_found'])}):")
                for card in result["not_found"]:
                    print(f"  - {card}")
            
            if args.budget:
                diff = args.budget - result["total_min"]
                if diff >= 0:
                    print(f"\n✓ Under budget by R$ {diff:.2f}")
                else:
                    print(f"\n✗ Over budget by R$ {abs(diff):.2f}")
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
