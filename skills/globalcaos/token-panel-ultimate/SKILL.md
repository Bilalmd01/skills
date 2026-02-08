---
name: token-panel-ultimate
version: 1.0.4
description: Multi-provider usage tracking for AI agents. Claude Max, Gemini, and Manus in one dashboard.
homepage: https://clawhub.com/skills/token-panel-ultimate
metadata:
  openclaw:
    emoji: "🎛️"
    requires:
      bins: ["python3"]
---

# Token Panel ULTIMATE

> 🎛️ Know your limits. Stay within them. Maximize your capacity.

Real-time usage tracking for **Claude Max**, **Gemini**, and **Manus** — all in one place.

---

## Features

| Provider | What It Tracks |
|----------|----------------|
| **Claude Max** | 5-hour window, 7-day window, reset times |
| **Gemini** | RPD/RPM/TPM per model, bottleneck detection |
| **Manus** | Daily refresh, monthly credits, addon balance |

Plus a **webchat widget** that shows it all at a glance.

---

## Claude Max Usage

Track your Claude Max subscription usage in real-time.

### What It Shows

- **5-hour window:** Rolling usage percentage and reset time
- **7-day window:** Weekly usage percentage and reset time
- **Model-specific limits:** Sonnet and Opus allocations

### Usage

```bash
# Pretty print current usage
python3 {baseDir}/scripts/claude-usage-fetch.py

# Update JSON file for the widget
python3 {baseDir}/scripts/claude-usage-fetch.py --update

# Raw JSON output
python3 {baseDir}/scripts/claude-usage-fetch.py --json
```

### Requirements

- Claude Code CLI installed and authenticated (`claude /login`)

### Auto-Update (Optional)

```bash
# Add to crontab for automatic updates every 5 minutes
*/5 * * * * python3 {baseDir}/scripts/claude-usage-fetch.py --update
```

---

## Gemini Multi-Model Tracking

Track the **bottleneck metric** (highest % among RPD, RPM, TPM) for each model.

### Model Limits (Tier 1)

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| gemini-3-pro | 25 | 1M | 250 |
| gemini-2.5-pro | 25 | 1M | 250 |
| gemini-2.5-flash | 2000 | 4M | **∞** |
| gemini-3-flash | 1000 | 1M | 10K |
| gemini-2.0-flash | 2000 | 4M | **∞** |

### Fallback Strategy

```
gemini-3-pro → gemini-2.5-pro → gemini-2.5-flash(∞) → gemini-3-flash → gemini-2.0-flash(∞)
```

Most capable first, unlimited RPD models as safety nets.

### JSON Format

Store in `memory/gemini-usage.json`:

```json
{
  "models": {
    "gemini-3-pro": {
      "limits": { "rpm": 25, "tpm": 1000000, "rpd": 250 },
      "usage": { "rpm": 17, "tpm": 1380000, "rpd": 251 },
      "status": "exceeded"
    }
  }
}
```

---

## Manus Credit Monitoring

### Credit Structure

- **Monthly:** 4,000 credits (resets on renewal)
- **Daily refresh:** 300 credits (resets 01:00)
- **Addon:** Purchased credits (never expire)

### JSON Format

Store in `memory/manus-usage.json`:

```json
{
  "credits": {
    "breakdown": {
      "monthly": { "used": 62, "limit": 4000 },
      "addon": 7296
    },
    "daily_refresh": { "current": 0, "limit": 300 }
  }
}
```

---

## Budget-Aware Behavior

Add to your SOUL.md:

```markdown
## Resource Awareness

**Behavior by budget level:**
| Budget | Behavior |
|--------|----------|
| 🟢 >50% | Normal operations |
| 🟡 30-50% | Be concise |
| 🟠 10-30% | Defer non-essential tasks |
| 🔴 <10% | Minimal responses only |
```

### Agent Self-Check

```python
import json
from pathlib import Path

def get_claude_usage():
    path = Path.home() / ".openclaw/workspace/memory/claude-usage.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("limits", {}).get("five_hour", {}).get("utilization", 0)
    return 0
```

---

## Webchat Widget

A Tampermonkey userscript that displays real-time usage in OpenClaw webchat.

### Installation

#### 1. Install Tampermonkey

| Browser | Link |
|---------|------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/) |
| Edge | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd) |
| Safari | [Mac App Store](https://apps.apple.com/app/tampermonkey/id1482490089) |

#### 2. Create New Script

1. Click Tampermonkey icon → **"Create a new script..."**
2. Delete all default content
3. Copy entire contents of `{baseDir}/scripts/budget-panel-widget.user.js`
4. Paste into Tampermonkey
5. **Ctrl+S** to save

#### 3. Refresh Webchat

Go to `http://localhost:18789` and refresh. Panel appears bottom-left.

### Troubleshooting

- **Panel not appearing?** Check Tampermonkey is enabled
- **Shows 0%?** Run `claude-usage-fetch.py --update` first
- **MIME error?** Full restart: `openclaw gateway stop && openclaw gateway start`

---

## Files

```
token-panel-ultimate/
├── SKILL.md
├── package.json
└── scripts/
    ├── claude-usage-fetch.py       # Claude Max usage fetcher
    └── budget-panel-widget.user.js # Webchat widget
```

---

## Gateway Plugin

For full integration, the **budget-panel** gateway plugin is available in our OpenClaw fork:

**Repository:** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

The plugin provides:
- `budget.usage` gateway method for real-time data
- Automatic JSON file reading
- Multi-provider aggregation

Install the plugin at `extensions/budget-panel/` in your OpenClaw installation.

---

## Related Skills

- **shell-security-ultimate** - Command security enforcement
- **agent-memory-ultimate** - Memory system with usage logs

---

## Credits

Created by **Oscar Serra** with the help of **Claude** (Anthropic).

*Built during a late-night hacking session, February 2026.*
