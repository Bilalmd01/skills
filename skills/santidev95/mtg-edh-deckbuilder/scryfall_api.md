# Scryfall API Reference

Base URL: `https://api.scryfall.com`

## Rate Limits
- 10 requests per second max
- Use 50-100ms delay between requests
- Cache results for 24 hours (prices update daily)

## Key Endpoints

### Search Cards
```
GET /cards/search?q={query}
```
Returns paginated results (175 cards per page).

### Get Card by Name
```
GET /cards/named?fuzzy={name}
GET /cards/named?exact={name}
```

### Autocomplete
```
GET /cards/autocomplete?q={partial_name}
```
Returns up to 20 suggestions.

### Get Card Collection
```
POST /cards/collection
Content-Type: application/json

{
  "identifiers": [
    {"name": "Sol Ring"},
    {"name": "Command Tower"}
  ]
}
```
Max 75 cards per request.

---

## Search Syntax

### Colors and Color Identity
| Syntax | Meaning |
|--------|---------|
| `c:w` | Cards that ARE white |
| `c:wu` | Cards that are white AND blue |
| `c>=uw` | Cards with at least white and blue |
| `ci:wubrg` | Color identity includes (for Commander) |
| `ci<=rug` | Color identity within Temur |

### Card Types
| Syntax | Meaning |
|--------|---------|
| `t:creature` | Type is creature |
| `t:legendary` | Type includes legendary |
| `t:"legendary creature"` | Legendary creatures |

### Oracle Text
| Syntax | Meaning |
|--------|---------|
| `o:flying` | Has "flying" in text |
| `o:"enters the battlefield"` | ETB triggers |
| `o:counter` | Counter-related |
| `kw:flying` | Has flying keyword |

### Mana Cost and CMC
| Syntax | Meaning |
|--------|---------|
| `cmc=3` | Converted mana cost is 3 |
| `cmc<=2` | CMC is 2 or less |
| `mv>=5` | Mana value 5+ |
| `m:{2}{U}` | Mana cost includes 2U |

### Power/Toughness
| Syntax | Meaning |
|--------|---------|
| `pow=3` | Power is 3 |
| `pow>=5` | Power is 5+ |
| `tou<=2` | Toughness 2 or less |

### Rarity and Sets
| Syntax | Meaning |
|--------|---------|
| `r:mythic` | Mythic rare |
| `r:common` | Common |
| `e:cmr` | From Commander Legends |
| `is:commander` | Can be commander |

### Format Legality
| Syntax | Meaning |
|--------|---------|
| `f:commander` | Legal in Commander |
| `f:vintage` | Legal in Vintage |
| `banned:commander` | Banned in Commander |

### Prices (USD)
| Syntax | Meaning |
|--------|---------|
| `usd<1` | Under $1 |
| `usd<=5` | $5 or less |
| `usd>=50` | $50+ |

### Combining Queries
| Operator | Meaning |
|----------|---------|
| `a b` (space) | AND |
| `a or b` | OR |
| `-a` | NOT |
| `(a or b) c` | Grouping |

---

## Common Commander Searches

### Find Potential Commanders
```
is:commander ci<=wubrg
```

### Cards in Color Identity (e.g., Simic)
```
ci<=ug -t:land f:commander
```

### Ramp Cards
```
ci<=g (o:search o:"add {" o:land) t:creature cmc<=3
```

### Board Wipes
```
ci<=w o:destroy o:"all creatures" t:sorcery
```

### Card Draw in Blue
```
ci<=u o:draw t:instant cmc<=3
```

### Creatures with ETB Effects
```
ci<=wubrg t:creature o:"enters the battlefield"
```

### Counterspells
```
ci<=u o:counter t:instant cmc<=3
```

---

## Response Structure

```json
{
  "object": "card",
  "name": "Sol Ring",
  "mana_cost": "{1}",
  "cmc": 1.0,
  "type_line": "Artifact",
  "oracle_text": "{T}: Add {C}{C}.",
  "colors": [],
  "color_identity": [],
  "legalities": {
    "commander": "banned",
    "duel": "banned"
  },
  "prices": {
    "usd": "1.50",
    "usd_foil": "4.00"
  }
}
```

## Card Face Structure (Double-faced cards)
```json
{
  "card_faces": [
    {
      "name": "Front Face",
      "mana_cost": "{1}{G}",
      "oracle_text": "..."
    },
    {
      "name": "Back Face",
      "oracle_text": "..."
    }
  ]
}
```
