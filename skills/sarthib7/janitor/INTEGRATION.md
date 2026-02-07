# Integrating Janitor Skill with ClawHub.ai

This guide shows how to integrate the lightweight Janitor skill into your ClawHub.ai agent.

## Installation

### Option 1: Copy skill directory

```bash
# Copy the skill directory to your ClawHub.ai skills folder
cp -r skill/ /path/to/clawhub/skills/janitor/
```

### Option 2: Clone from repository

```bash
# In your ClawHub.ai skills directory
cd skills/
git clone https://github.com/openclaw/janitor
cd janitor/skill
```

## Basic Integration

### Method 1: Direct Import

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

async function runWithCleanup() {
  const janitor = new Janitor();

  // Your agent code here
  // ...

  // Cleanup after task
  const result = await janitor.cleanup();
  console.log('Cleanup:', result);
}
```

### Method 2: As a Subagent

```javascript
class ClawHubAgent {
  constructor() {
    this.janitor = new (require('./skills/janitor/skill/janitor'))();
  }

  async runTask(task) {
    // Execute task
    const result = await this.executeTask(task);

    // Auto-cleanup
    await this.janitor.cleanup();

    return result;
  }
}
```

### Method 3: Post-Task Hook

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

class ClawHubAgent {
  constructor() {
    this.janitor = new Janitor();
    this.onTaskComplete = this.cleanup.bind(this);
  }

  async cleanup() {
    return await this.janitor.cleanup();
  }
}
```

## Using with Different Agents

### CrewAI Integration

```python
# For CrewAI, you can call via subprocess
import subprocess
import json

def cleanup_after_task():
    result = subprocess.run(
        ['node', 'skills/janitor/skill/index.js', 'clean'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

### LangChain Integration

```javascript
const { Tool } = require('langchain/tools');
const Janitor = require('./skills/janitor/skill/janitor');

class JanitorTool extends Tool {
  constructor() {
    super();
    this.name = 'janitor';
    this.description = 'Clean up cache and temporary files';
    this.janitor = new Janitor();
  }

  async _call(input) {
    const result = await this.janitor.cleanup();
    return JSON.stringify(result);
  }
}
```

## Scheduled Cleanup

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

const janitor = new Janitor();

// Run cleanup every hour
setInterval(async () => {
  console.log('Running scheduled cleanup...');
  await janitor.cleanup();
}, 60 * 60 * 1000);
```

## Monitoring

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

const janitor = new Janitor();

// Get stats periodically
setInterval(() => {
  const stats = janitor.getStats();
  console.log('Janitor Stats:', stats);

  // Send to monitoring system
  sendToMonitoring('janitor.stats', stats);
}, 5 * 60 * 1000); // Every 5 minutes
```

## Configuration

```javascript
const Janitor = require('./skills/janitor/skill/janitor');

const janitor = new Janitor({
  enabled: true,
  unusedFileAgeDays: 14  // Keep files for 2 weeks
});
```

## Advanced Features

For advanced features like:
- Automated GitHub backups
- Cron scheduling
- Session management
- Log rotation

See the full version: **https://github.com/openclaw/janitor**

## Support

- Full repo: https://github.com/openclaw/janitor
- Issues: https://github.com/openclaw/janitor/issues
- Author: Sarthi Borkar

---

**Janitor Lite v1.0.0** - Keep your AI agents clean!
