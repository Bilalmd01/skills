---
name: mtg-deck-builder
description: |
  Builds Magic: The Gathering Commander/EDH and Duel Commander decks from scratch. Use when the user asks to create or build a deck, suggest cards for a commander or strategy, work with budget (LigaMagic), analyze mana curve or card types, or check card legality. Keywords: MTG, Magic, Commander, EDH, Duel Commander, deck building, Scryfall, LigaMagic.
---

# MTG Deck Builder

Build Commander/EDH and Duel Commander decks using Scryfall API for card data and LigaMagic for Brazilian market prices.

## Quick Start

1. Identify format: Commander (multiplayer) or Duel Commander (1v1)
2. Get commander from user or help them choose one
3. Use `scryfall_search.py` to find cards
4. Check banlist using `banlists.md`
5. Build deck respecting color identity and deck rules
6. Generate report with `deck_report.py`

## Supported Formats

| Format | Life | Deck Size | Commander | Banlist |
|--------|------|-----------|-----------|---------|
| Commander/EDH | 40 | 100 (including commander) | 1 or 2 (partner); Companion only if legal | See `banlists.md` |
| Duel Commander | 20 | 100 (including commander) | Exactly 1 legendary creature | See `banlists.md`; check "banned as commander" |

**Duel Commander:** As of March 2026 the format transitions to a new system; check `banlists.md` and mtgdc.info for current rules.

## Regra Singleton (IMPORTANTE!)

Decks de Commander são singleton: cada carta pode aparecer apenas UMA vez 
no deck, com exceção de terrenos básicos (Plains, Island, Swamp, Mountain, 
Forest, Wastes).

Regra:
NENHUMA CARTA A NÃO SER Plains, Island, Swamp, Mountain, 
Forest, Wastes PODEM APARECER MAIS DE UMA VEZ

- ✅ 1x Sol Ring
- ✅ 1x Counterspell  
- ✅ 15x Island (terreno básico - pode repetir)
- ❌ 2x Lightning Bolt (não permitido)
- ❌ 4x Reliquary Tower (não permitido)
- ❌ 2x Counterspell 

## Workflow

### 1. Understand Request
Extract from user message:
- Format (Commander or Duel Commander)
- Commander choice or strategy theme
- Budget constraint (if any, in BRL using LigaMagic)
- Power level preference (casual/competitive)

### 2. Validate Commander
- **Commander/EDH:** 1 commander, or 2 with partner; Companion only if allowed by banlist.
- **Duel Commander:** Exactly 1 legendary creature; confirm not in "banned as commander" in `banlists.md`.
```bash
python scryfall_search.py --name "Commander Name" --check-commander --format commander
```

### 3. Search Cards
Use Scryfall syntax for powerful searches:
```bash
python scryfall_search.py --query "ci:wubrg t:creature" --limit 50
python scryfall_search.py --query "o:counter ci:ug t:creature"
```

### 4. Check Prices (Optional)
```bash
python ligamagic_price.py --card "Sol Ring"
```

### 5. Build Deck Structure
Standard Commander deck template:
- 1 Commander
- 35-38 Lands
- 10-12 Ramp/Mana acceleration
- 10 Card draw
- 8-10 Removal (single target + board wipes)
- 30-35 Cards supporting strategy

### 6. Generate Report
```bash
python deck_report.py --deck deck.txt --format commander
```

## Key References

- **Scryfall API**: See `scryfall_api.md` for search syntax
- **Banlists**: See `banlists.md` for Commander and Duel Commander
- **Deck Templates**: See `deck_templates.md` for archetypes
- **Metagame Sources**: See `metagame_sources.md` for live data URLs
- **Color Identity**: A card's color identity includes mana symbols in cost and rules text

## Fetching Live Metagame Data

**IMPORTANT:** Always fetch current metagame data before building competitive decks!

### For Duel Commander:
1. Search: `mtggoldfish duel commander metagame`
2. Fetch: `https://www.mtggoldfish.com/metagame/duel_commander`
3. Extract top commanders, meta %, prices

### For Commander/EDH:
1. Search: `site:edhrec.com [commander name]`
2. Get recommended cards with synergy scores
3. Check `https://edhrec.com/commanders` for popular choices

### For cEDH:
1. Check: `https://cedh-decklist-database.com/`
2. Find optimized lists by tier

## Budget Building with LigaMagic

When user specifies budget:
1. Search cards normally via Scryfall
2. Get prices via `ligamagic_price.py`
3. Optimize deck to fit budget
4. Report total cost and suggest upgrades

## Output Format

Always provide:
1. Decklist in standard format (quantity + card name)
2. Mana curve visualization
3. Card type distribution
4. Total price (if budget was considered)
5. Key synergies explanation

**Example decklist section:**
```text
COMMANDER
1 Atraxa, Praetors' Voice

MAINDECK
1 Sol Ring
1 Command Tower
1 Arcane Signet
...
38 Forest
```

**Example report summary:** Mana curve (e.g. 0: 5, 1: 8, 2: 12, …), card types (Creatures: 35, Instants: 12, …), total LigaMagic (BRL) if applicable, and 2–3 key synergies with the commander.
