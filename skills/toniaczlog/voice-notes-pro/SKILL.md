# Voice Notes Pro v2.0

**Notatki g³osowe z 6 kategoriami + baza ludzi.**

## ?? Kategorie

1. ?? **Teksty piosenek** › `~/notes/songs/brudnopis.md`
2. ? **Zadania** › `~/notes/tasks/inbox.md`
3. ?? **Zakupy** › `~/notes/lists/shopping.md`
4. ?? **Pomys³y** › `~/notes/ideas/[projekt]/`
5. ?? **Baza ludzi** › `~/notes/people/database.md`
6. ?? **Watchlist** › `~/notes/watchlist/watchlist.md`

## ?? Przyk³ady

### Piosenka:
```
?? "Dyktujê tekst utworu: jestem te o eN aka Œcinacz G³ów..."
› ?? Zapisano tekst piosenki
```

### Zadanie:
```
?? "Zadanie: zadzwoniæ do klienta jutro"
› ? Dodano zadanie
```

### Zakupy:
```
?? "Zakupy: mleko, chleb, jajka"
› ?? Dodano 3 produkty
```

### Baza ludzi:
```
?? "Dodaj osobê: Michael Jackson, urodzony 1958, zmar³ 2009"
› ? Dodano: Michael Jackson
?? 1958 - 2009
?? 2026-02-07 18:00
```
```
?? "SprawdŸ osobê: Michael Jackson"
› ?? Michael Jackson - ju¿ w bazie!
?? Dodano: 2026-02-07 18:00
```

### Watchlist:
```
?? "Zapisz film: Oppenheimer Christopher Nolan"
› ?? Dodano: Oppenheimer
```

## ?? Konfiguracja

W `openclaw.json`:
```json
"voice-notes-pro": {
  "enabled": true,
  "whatsapp": {
    "enabled": true,
    "phoneNumber": "+48TWOJ_NUMER"
  },
  "directories": {
    "songs": "/root/notes/songs",
    "tasks": "/root/notes/tasks",
    "shopping": "/root/notes/lists",
    "ideas": "/root/notes/ideas",
    "people": "/root/notes/people",
    "watchlist": "/root/notes/watchlist"
  }
}
```

## ?? Whisper (Blew)

Skill u¿ywa Whisper przez Blew do transkrypcji.
Upewnij siê ¿e Whisper jest skonfigurowany w Blew.

## ?? Licencja

MIT