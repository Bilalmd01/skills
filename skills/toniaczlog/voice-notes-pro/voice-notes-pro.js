// voice-notes-pro.js - Voice Notes with Whisper & Smart Categorization
const fs = require('fs').promises;
const path = require('path');

class VoiceNotesPro {
  constructor(config, whatsapp) {
    this.config = config;
    this.whatsapp = whatsapp;
    this.dirs = config.directories;
    this.init();
  }

  async init() {
    const dirs = [
      this.dirs.songs,
      this.dirs.tasks,
      this.dirs.shopping,
      this.dirs.ideas,
      this.dirs.people,
      this.dirs.watchlist,
    ];

    for (const dir of dirs) {
      await fs.mkdir(dir, { recursive: true });
    }

    await this.ensureFile(path.join(this.dirs.songs, 'brudnopis.md'), '# Brudnopis - Teksty Piosenek\n\n');
    await this.ensureFile(path.join(this.dirs.tasks, 'inbox.md'), '# Inbox - Zadania\n\n');
    await this.ensureFile(path.join(this.dirs.shopping, 'shopping.md'), '# Lista Zakupów\n\n');
    await this.ensureFile(path.join(this.dirs.people, 'database.md'), '# Baza Ludzi\n\n');
    await this.ensureFile(path.join(this.dirs.watchlist, 'watchlist.md'), '# Watchlist\n\n');

    console.log('? Voice Notes Pro initialized');
  }

  async ensureFile(filepath, defaultContent = '') {
    try {
      await fs.access(filepath);
    } catch {
      await fs.writeFile(filepath, defaultContent);
    }
  }

  async handleVoiceNote(transcription) {
    console.log(`?? "${transcription}"`);
    try {
      const noteType = this.detectNoteType(transcription);
      console.log(`???  ${noteType}`);
      const result = await this.processNote(transcription, noteType);
      return this.formatResponse(result);
    } catch (error) {
      console.error('?', error);
      return { success: false, message: `B³¹d: ${error.message}` };
    }
  }

  detectNoteType(text) {
    const lower = text.toLowerCase();
    if (this.matchKeywords(lower, ['dyktujê', 'tekst utworu', 'piosenka', 'zwrotka', 'refren', 'wers', 'rap'])) return 'song';
    if (this.matchKeywords(lower, ['dodaj osobê', 'osoba:', 'celebryta:', 'urodzony', 'urodzona', 'zmar³', 'zmar³a'])) return 'person';
    if (this.matchKeywords(lower, ['sprawdŸ osobê', 'kto to', 'czy mam', 'szukaj osoby'])) return 'person-check';
    if (this.matchKeywords(lower, ['zapisz film', 'zapisz serial', 'zapisz ksi¹¿kê', 'do obejrzenia', 'do przeczytania', 'watchlist'])) return 'watchlist';
    if (this.matchKeywords(lower, ['zadanie', 'todo', 'zrób', 'pamiêtaj', 'przypomnienie'])) return 'task';
    if (this.matchKeywords(lower, ['zakupy', 'kup', 'lista zakupów', 'sklep'])) return 'shopping';
    if (this.matchKeywords(lower, ['pomys³', 'projekt', 'apka', 'aplikacja', 'strona', 'saas'])) return 'idea';
    if (this.looksLikeShopping(text)) return 'shopping';
    if (this.looksLikeIdea(text)) return 'idea';
    return 'task';
  }

  matchKeywords(text, keywords) {
    return keywords.some(kw => text.includes(kw));
  }

  looksLikeShopping(text) {
    const items = text.split(',');
    if (items.length >= 3) {
      const avgLength = items.reduce((sum, item) => sum + item.trim().length, 0) / items.length;
      return avgLength < 20;
    }
    return false;
  }

  looksLikeIdea(text) {
    const ideaKeywords = ['aplikacja', 'apka', 'strona', 'narzêdzie'];
    return ideaKeywords.some(kw => text.toLowerCase().includes(kw)) && text.length > 50;
  }

  async processNote(text, type) {
    const now = new Date();
    const date = now.toISOString().split('T')[0];
    const time = now.toTimeString().split(' ')[0].substring(0, 5);

    switch (type) {
      case 'song': return await this.processSong(text, date, time);
      case 'task': return await this.processTask(text, date, time);
      case 'shopping': return await this.processShopping(text, date, time);
      case 'idea': return await this.processIdea(text, date, time);
      case 'person': return await this.processPerson(text, date, time);
      case 'person-check': return await this.checkPerson(text);
      case 'watchlist': return await this.processWatchlist(text, date, time);
      default: throw new Error(`Unknown type: ${type}`);
    }
  }

  async processSong(text, date, time) {
    const filepath = path.join(this.dirs.songs, 'brudnopis.md');
    const cleanText = text.replace(/^(dyktujê|tekst utworu|piosenka|zwrotka|refren)[:\s]*/i, '').trim();
    const entry = `\n## ${date} ${time}\n\n${cleanText}\n\n---\n`;
    await fs.appendFile(filepath, entry);
    return { type: 'song', content: cleanText, message: '? Zapisano tekst piosenki' };
  }

  async processTask(text, date, time) {
    const filepath = path.join(this.dirs.tasks, 'inbox.md');
    const cleanText = text.replace(/^(dodaj zadanie|zadanie|todo|zrób|pamiêtaj)[:\s]*/i, '').trim();
    const entry = `- [ ] ${cleanText} _(${date} ${time})_\n`;
    await fs.appendFile(filepath, entry);
    return { type: 'task', content: cleanText, message: '? Dodano zadanie' };
  }

  async processShopping(text, date, time) {
    const filepath = path.join(this.dirs.shopping, 'shopping.md');
    const cleanText = text.replace(/^(dodaj na zakupy|zakupy|kup|lista zakupów)[:\s]*/i, '').trim();
    const items = cleanText.split(/,|i(?=\s)/).map(item => item.trim()).filter(item => item.length > 0);
    const entries = items.map(item => `- [ ] ${item}`).join('\n');
    const entry = `\n### ${date} ${time}\n${entries}\n`;
    await fs.appendFile(filepath, entry);
    return { type: 'shopping', content: items, count: items.length, message: `? Dodano ${items.length} produktów` };
  }

  async processIdea(text, date, time) {
    const cleanText = text.replace(/^(pomys³|projekt|apka|aplikacja)[:\s]*/i, '').trim();
    const slug = cleanText.toLowerCase().split(' ').slice(0, 4).join('-').replace(/[^a-z0-9-]/g, '').substring(0, 30);
    const projectDir = path.join(this.dirs.ideas, `${date}-${slug}`);
    await fs.mkdir(projectDir, { recursive: true });
    const readme = `# ${this.titleCase(slug.replace(/-/g, ' '))}\n\n**Data:** ${date} ${time}\n\n## ?? Pomys³\n\n${cleanText}\n\n## ?? Next Steps\n\n- [ ] Walidacja\n- [ ] Mockupy\n- [ ] Tech stack\n- [ ] MVP\n`;
    await fs.writeFile(path.join(projectDir, 'README.md'), readme);
    return { type: 'idea', content: cleanText, slug, message: `? Projekt: ${slug}` };
  }

  async processPerson(text, date, time) {
    const filepath = path.join(this.dirs.people, 'database.md');
    const parsed = this.parsePerson(text);
    const existing = await this.findPerson(parsed.name);
    if (existing) {
      return { type: 'person', duplicate: true, existing, message: `?? ${parsed.name} - ju¿ w bazie!\n?? Dodano: ${existing.addedAt}` };
    }
    const entry = `\n## ${parsed.name}\n- **Urodziny:** ${parsed.birth || 'nieznane'}\n- **Œmieræ:** ${parsed.death || '¿yje'}\n- **Kategoria:** ${parsed.category || 'brak'}\n- **Dodano:** ${date} ${time}\n${parsed.notes ? `- **Notatki:** ${parsed.notes}\n` : ''}\n---\n`;
    await fs.appendFile(filepath, entry);
    return { type: 'person', name: parsed.name, birth: parsed.birth, death: parsed.death, message: `? Dodano: ${parsed.name}\n?? ${parsed.birth || '?'} - ${parsed.death || '?'}\n?? ${date} ${time}` };
  }

  parsePerson(text) {
    let clean = text.replace(/^(dodaj osobê|osoba)[:\s]*/i, '').trim();
    const name = clean.split(',')[0].trim();
    const birthMatch = clean.match(/urodzony|urodzona|ur\.?\s*(\d{4})/i);
    const deathMatch = clean.match(/zmar³|zmar³a|zm\.?\s*(\d{4})/i);
    return { name, birth: birthMatch ? birthMatch[1] : null, death: deathMatch ? deathMatch[1] : null, category: 'Nieznana', notes: '' };
  }

  async findPerson(name) {
    const filepath = path.join(this.dirs.people, 'database.md');
    try {
      const content = await fs.readFile(filepath, 'utf8');
      const regex = new RegExp(`## ${name}[\\s\\S]*?Dodano:\\*\\* ([^\\n]+)`, 'i');
      const match = content.match(regex);
      if (match) return { name, addedAt: match[1] };
    } catch {}
    return null;
  }

  async checkPerson(text) {
    const name = text.replace(/^(sprawdŸ osobê|kto to|czy mam|szukaj osoby)[:\s]*/i, '').trim();
    const person = await this.findPerson(name);
    if (person) return { type: 'person-check', found: true, person, message: `?? ${name} - w bazie!\n?? Dodano: ${person.addedAt}` };
    return { type: 'person-check', found: false, message: `? ${name} - nie znaleziono` };
  }

  async processWatchlist(text, date, time) {
    const filepath = path.join(this.dirs.watchlist, 'watchlist.md');
    const parsed = this.parseWatchlist(text);
    const entry = `\n## ${parsed.title}\n- **Typ:** ${parsed.type}\n- **Autor/Re¿yser:** ${parsed.author || 'nieznany'}\n- **Dodano:** ${date} ${time}\n- **Status:** Do obejrzenia\n\n---\n`;
    await fs.appendFile(filepath, entry);
    return { type: 'watchlist', title: parsed.title, itemType: parsed.type, message: `${parsed.icon} Dodano: ${parsed.title}` };
  }

  parseWatchlist(text) {
    let clean = text.replace(/^(zapisz|dodaj|watchlist)[:\s]*/i, '').trim();
    let type = 'Film', icon = '??';
    if (clean.match(/^(film|movie)/i)) {
      type = 'Film'; icon = '??'; clean = clean.replace(/^(film|movie)[:\s]*/i, '');
    } else if (clean.match(/^(serial|series)/i)) {
      type = 'Serial'; icon = '??'; clean = clean.replace(/^(serial|series)[:\s]*/i, '');
    } else if (clean.match(/^(ksi¹¿k|book)/i)) {
      type = 'Ksi¹¿ka'; icon = '??'; clean = clean.replace(/^(ksi¹¿k\w*|book)[:\s]*/i, '');
    }
    const parts = clean.split(/,|autor:/i);
    const title = parts[0].trim();
    const author = parts[1] ? parts[1].trim() : null;
    return { title, type, author, icon };
  }

  titleCase(str) {
    return str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
  }

  formatResponse(result) {
    if (!result.success && result.success !== undefined) return result;
    return { success: true, message: result.message, data: result };
  }
}

module.exports = {
  name: 'voice-notes-pro',
  version: '2.0.0',
  description: 'Voice notes with 6 categories',
  
  async init(context) {
    const config = context.config.skills.entries['voice-notes-pro'];
    if (!config?.enabled) return;
    this.handler = new VoiceNotesPro(config, context.whatsapp);
    console.log('? Voice Notes Pro ready (6 categories)');
  },

  async onVoiceMessage(message, context) {
    let transcription = message.body || await context.transcribe(message);
    const result = await this.handler.handleVoiceNote(transcription);
    await context.reply(result.message);
    return result;
  },

  async onMessage(message, context) {
    const text = message.body;
    if (text.toLowerCase().startsWith('sprawdŸ osobê:')) {
      const result = await this.handler.checkPerson(text);
      await context.reply(result.message);
    }
  },
};