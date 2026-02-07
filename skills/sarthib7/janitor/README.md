# Janitor Skill (Lite) - ClawHub.ai

Lightweight cleanup skill for AI agents. Removes cache files, logs, and temporary files to optimize memory and disk usage.

## Quick Start

```javascript
const Janitor = require('./janitor');

const janitor = new Janitor();

// Run cleanup
const result = await janitor.cleanup();
console.log(result);
// { filesDeleted: 42, spaceSaved: "1.2 MB", duration: "150ms", memoryFreed: true }

// Get stats
const stats = janitor.getStats();
console.log(stats);

// Get report
await janitor.report();
```

## What Gets Cleaned?

- `node_modules/.cache/**` - Node module caches
- `.cache/` - Cache directories
- `dist/`, `coverage/`, `tmp/` - Build artifacts and temp files
- `.DS_Store` - macOS metadata files
- `*.log` files older than 7 days

## Protected Files

These are NEVER deleted:
- `package.json`, `README.md`, `.env`
- `src/**` - Source files
- `.git/**` - Git repository
- `node_modules/**` - Dependencies (except `.cache`)

## Features

- 🧹 **Core Cleanup** - Cache, logs, temp files
- 🗑️ **Memory Optimization** - Garbage collection
- 📊 **Statistics** - Track cleanups and space saved
- 🛡️ **Safe** - Protected file patterns
- 🚀 **Zero Dependencies** - Only uses Node.js built-ins

## Differences from Full Version

This is a **lightweight version** for ClawHub.ai with only core cleanup features.

**Missing features** (available in full version):
- ⏰ Automated scheduling/cron
- 💾 GitHub backups
- 🔄 Auto-cleanup after git push
- 📈 Advanced reporting
- ⚙️ Complex configuration

## Full Version

For advanced features, visit the main repository:

**https://github.com/openclaw/janitor**

The full version includes:
- Automated backup to GitHub
- Cron scheduling
- Session management
- Log rotation
- Storage monitoring
- And more...

## Usage in ClawHub.ai

Install as a skill:

```bash
# In your ClawHub.ai skills directory
cd skills/
git clone https://github.com/openclaw/janitor
cd janitor/skill
```

Use in your agent:

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

const janitor = new Janitor();
await janitor.cleanup();
```

## API

### `cleanup(workingDir?: string): Promise<object>`

Run full cleanup operation.

Returns:
```javascript
{
  filesDeleted: number,
  spaceSaved: string,
  duration: string,
  memoryFreed: boolean
}
```

### `getStats(): object`

Get cleanup statistics.

### `report(): Promise<object>`

Generate cleanup report.

## License

MIT

---

**Janitor Lite v1.0.0** - Part of OpenClaw AI Agent Framework
