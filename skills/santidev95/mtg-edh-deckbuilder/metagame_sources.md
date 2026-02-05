# Metagame Data Sources

Este arquivo contém URLs e instruções para o agente buscar dados atualizados de metagame.

## Fontes Primárias de Dados

### 1. MTGGoldfish (Recomendado)
**URL:** `https://www.mtggoldfish.com/metagame/duel_commander`

**Dados disponíveis:**
- Meta % por comandante
- Preços de decks (USD e MTGO tix)
- Decklists completas
- Torneios recentes

**Como usar:**
```
Buscar a página e extrair:
- Lista de comandantes com % de meta
- Cartas-chave de cada deck
- Preços médios
- Links para decklists
```

### 2. MTGTop8
**URL:** `https://mtgtop8.com/format?f=EDH`

**Dados disponíveis:**
- Eventos recentes (papel e MTGO)
- Breakdown de metagame por período
- Cartas mais jogadas
- Top 8 de torneios

**Filtros úteis:**
- `?meta=115` - Últimas 2 semanas
- `?meta=121` - Últimos 2 meses
- `?meta=306` - MTGO últimos 2 meses
- `?meta=308` - Paper últimos 2 meses

### 3. MTGDecks.net
**URL:** `https://mtgdecks.net/Duel-Commander`

**Dados disponíveis:**
- Agregador de múltiplas fontes
- Decks por data
- Filtros por arquétipo

### 4. Duel Commander Meta (Novo!)
**URL:** `https://duel-commander-meta.com/`

**Dados disponíveis:**
- Análise diária do metagame
- Estatísticas em tempo real
- Feedback da comunidade

---

## Para Commander/EDH Multiplayer

### 5. EDHREC (Melhor para Commander casual/multiplayer)
**URL Base:** `https://edhrec.com`

**Endpoints úteis:**
- `/commanders` - Top comandantes (2 anos)
- `/commanders/month` - Top comandantes (último mês)
- `/commanders/week` - Top comandantes (última semana)
- `/top` - Cartas mais jogadas
- `/top/month` - Cartas populares recentes

**Dados disponíveis:**
- Decks por comandante
- Cartas recomendadas com % de inclusão
- Synergy scores
- Average decklists
- Combos populares

**Biblioteca Python:** `pip install pyedhrec`
```python
from pyedhrec import EDHRec
edhrec = EDHRec()
data = edhrec.get_commander_data("Atraxa, Praetors' Voice")
cards = edhrec.get_commander_cards("Atraxa, Praetors' Voice")
avg_deck = edhrec.get_commanders_average_deck("Atraxa, Praetors' Voice")
```

### 6. cEDH Decklist Database (Para Commander competitivo)
**URL:** `https://cedh-decklist-database.com/`

**Dados disponíveis:**
- Decklists otimizadas para cEDH
- Tiers de comandantes
- Descrições de estratégias
- Combos e linhas de jogo

---

## Fontes de Preços

### 7. LigaMagic (Brasil - BRL)
**URL:** `https://www.ligamagic.com.br/?view=cards/search&card={CARD_NAME}`

**Dados disponíveis:**
- Menor preço
- Preço médio
- Ofertas por loja
- Condição das cartas

### 8. TCGPlayer (USD)
**Via Scryfall API:** Preços incluídos no objeto da carta
```json
{
  "prices": {
    "usd": "1.50",
    "usd_foil": "4.00"
  }
}
```

---

## Workflow para Atualizar Metagame

1. **Buscar MTGGoldfish** para ver % de meta atual
2. **Cruzar com MTGTop8** para ver resultados de torneios
3. **Consultar EDHREC** para cartas populares por comandante
4. **Verificar preços** no Scryfall (USD) ou LigaMagic (BRL)

---

## Regras e Banlists (Fontes Oficiais)

### Commander/EDH
- **Oficial:** `https://mtgcommander.net/index.php/banned-list/`
- **WotC:** `https://magic.wizards.com/en/banned-restricted-list`

### Duel Commander
- **Oficial:** `https://www.mtgdc.info/banned-restricted`
- **Regras:** `https://www.mtgdc.info/comprehensive-rules`

**IMPORTANTE:** Em 3 de Março de 2026, Duel Commander será substituído por um novo sistema!

---

## Exemplo de Query para Agente

Quando o usuário pedir informações de metagame:

```
1. Faça web_search: "mtggoldfish duel commander metagame [MÊS] [ANO]"
2. Faça web_fetch na URL do MTGGoldfish
3. Extraia:
   - Top 10 comandantes com % de meta
   - Preços médios
   - Cartas-chave
4. Para mais detalhes de um deck específico, busque a página do arquétipo
```

Para sugestões de cartas para um comandante específico:
```
1. Busque no EDHREC: "site:edhrec.com [NOME DO COMANDANTE]"
2. Extraia cartas com maior synergy score
3. Cruze com orçamento do usuário via LigaMagic
```
