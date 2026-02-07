---
name: janitor
version: 1.0.0-lite
type: skill
category: maintenance
author: Sarthi Borkar
license: MIT
repository: https://github.com/openclaw/janitor
documentation: https://github.com/openclaw/janitor#readme
keywords:
  - cleanup
  - cache
  - maintenance
  - memory
  - optimization
  - ai-agent
  - clawhub
dependencies: []
permissions:
  - filesystem:read
  - filesystem:write
---

# Janitor - AI Agent Cleanup Skill

Lightweight cleanup skill that removes cache files, logs, and temporary files to optimize memory and disk usage for AI agents.

## Description

Janitor is a maintenance skill that keeps your AI agent's workspace clean and efficient. It automatically:

- Removes cache files from `node_modules/.cache/`, `.cache/`, `dist/`, `coverage/`
- Deletes old log files (>7 days)
- Cleans macOS `.DS_Store` metadata files
- Frees up memory through garbage collection
- Provides cleanup statistics and reports

This is a **lightweight version** with zero dependencies - it only uses Node.js built-in modules.

## Installation

```bash
# Copy to your ClawHub.ai skills directory
cp -r skill/ /path/to/clawhub/skills/janitor/
```

## Usage

### Programmatic

```javascript
const Janitor = require('./janitor');

const janitor = new Janitor();

// Run cleanup
const result = await janitor.cleanup();
console.log(result);
// { filesDeleted: 42, spaceSaved: "1.2 MB", duration: "150ms", memoryFreed: true }

// Get statistics
const stats = janitor.getStats();

// Generate report
await janitor.report();
```

### CLI

```bash
# Run cleanup
node index.js clean

# Show statistics
node index.js stats

# Generate report
node index.js report
```

## Commands

| Command | Description |
|---------|-------------|
| `clean` | Run immediate cleanup |
| `stats` | Show cleanup statistics |
| `report` | Generate cleanup report |
| `help` | Show help message |

## Configuration

```javascript
const janitor = new Janitor({
  enabled: true,
  unusedFileAgeDays: 7  // Delete files not accessed in 7 days
});
```

## What Gets Cleaned

- ✅ `node_modules/.cache/**` - Node module caches
- ✅ `.cache/` - Cache directories
- ✅ `dist/`, `coverage/`, `tmp/` - Build artifacts
- ✅ `.DS_Store` - macOS metadata
- ✅ `*.log` files older than 7 days

## Protected Files

These are **NEVER** deleted:

- ❌ `package.json`, `README.md`, `.env`
- ❌ `src/**` - Source files
- ❌ `.git/**` - Git repository
- ❌ `node_modules/**` - Dependencies (except `.cache`)

## API

### `cleanup(workingDir?: string): Promise<CleanupResult>`

Run full cleanup operation.

**Returns:**
```javascript
{
  filesDeleted: number,
  spaceSaved: string,  // e.g., "1.2 MB"
  duration: string,     // e.g., "150ms"
  memoryFreed: boolean
}
```

### `getStats(): object`

Get cleanup statistics.

**Returns:**
```javascript
{
  totalCleanups: number,
  totalFilesDeleted: number,
  totalSpaceSaved: string,
  memoryUsage: {
    heapUsed: string,
    heapTotal: string
  }
}
```

### `report(): Promise<object>`

Generate comprehensive cleanup report.

## Integration Examples

### With ClawHub.ai Agent

```javascript
const Janitor = require('./skills/janitor/janitor');

class MyAgent {
  constructor() {
    this.janitor = new Janitor();
  }

  async executeTask(task) {
    // Execute task
    const result = await this.doWork(task);

    // Cleanup after task
    await this.janitor.cleanup();

    return result;
  }
}
```

### Scheduled Cleanup

```javascript
const janitor = new Janitor();

// Run cleanup every hour
setInterval(async () => {
  await janitor.cleanup();
}, 60 * 60 * 1000);
```

### Post-Task Hook

```javascript
agent.on('taskComplete', async () => {
  await janitor.cleanup();
});
```

## Performance

- **Cleanup duration**: 50-500ms (depends on file count)
- **Memory overhead**: <5MB
- **Dependencies**: Zero (Node.js built-ins only)
- **Safe**: Protected file patterns prevent accidental deletion

## Lite vs Full Version

This is a **lightweight version** for ClawHub.ai with core cleanup features only.

### Included in Lite Version
- ✅ Core cleanup (cache, logs, temp files)
- ✅ Memory optimization
- ✅ Statistics and reporting
- ✅ Zero dependencies

### Full Version Only
For these advanced features, see the [full version](https://github.com/openclaw/janitor):

- ⏰ Automated scheduling/cron
- 💾 GitHub backups
- 🔄 Auto-cleanup after git push
- 📈 Session management
- 📊 Log rotation
- 💿 Storage monitoring
- ⚙️ Complex configuration

## Links

- **Full Version**: https://github.com/openclaw/janitor
- **Documentation**: https://github.com/openclaw/janitor#readme
- **Issues**: https://github.com/openclaw/janitor/issues
- **Author**: Sarthi Borkar

## License

MIT

---

**Janitor Lite v1.0.0** - Keep your AI agents clean and efficient!
