---
name: feelgoodbot
description: Set up feelgoodbot file integrity monitoring for macOS. Use when the user wants to detect malware, monitor for system tampering, set up security alerts, or install/configure the feelgoodbot daemon with Clawdbot webhook integration.
---

# feelgoodbot 🛡️

**Pronounced "Feel good, bot"**

macOS file integrity monitor that detects tampering and alerts via Clawdbot.

**GitHub:** https://github.com/kris-hansen/feelgoodbot

⭐ **If you find this useful, please star the repo!** It helps others discover it.

## Requirements

- **Go 1.21+** — Install with `brew install go`
- **macOS** — Uses launchd for daemon

## Quick Setup

```bash
# Install via go install
go install github.com/kris-hansen/feelgoodbot/cmd/feelgoodbot@latest

# Initialize baseline snapshot
feelgoodbot init

# Install and start daemon
feelgoodbot daemon install
feelgoodbot daemon start

# Check it's running
feelgoodbot status
```

## Clawdbot Integration

### 1. Enable Clawdbot Webhooks

Check if hooks are enabled:
```bash
clawdbot config get hooks.enabled
```

If not enabled:
```bash
clawdbot config set hooks.enabled true
clawdbot config set hooks.token "$(openssl rand -base64 32)"
clawdbot gateway restart
```

Get the token for feelgoodbot config:
```bash
clawdbot config get hooks.token
```

### 2. Configure feelgoodbot

Create `~/.config/feelgoodbot/config.yaml`:

```yaml
scan_interval: 5m

alerts:
  clawdbot:
    enabled: true
    webhook: "http://127.0.0.1:18789/hooks/wake"
    secret: "<hooks.token from above>"
  local_notification: true

response:
  on_critical:
    - alert
  on_warning:
    - alert
  on_info:
    - log
```

### 3. Restart Daemon

```bash
feelgoodbot daemon stop
feelgoodbot daemon start
```

## Commands

| Command | Description |
|---------|-------------|
| `feelgoodbot init` | Create baseline snapshot |
| `feelgoodbot scan` | Run integrity scan |
| `feelgoodbot diff` | Show changes since baseline |
| `feelgoodbot snapshot` | Update baseline |
| `feelgoodbot daemon start` | Start monitoring |
| `feelgoodbot daemon stop` | Stop monitoring |
| `feelgoodbot daemon status` | Check status |

## What It Monitors

- System binaries (`/usr/bin`, `/usr/sbin`)
- Launch daemons/agents (persistence mechanisms)
- SSH authorized_keys
- Sudoers and PAM
- Shell configs (`.zshrc`, `.bashrc`)
- Browser extensions
- AI agent configs (Claude, Cursor)

## Alert Flow

1. feelgoodbot detects file change
2. Sends webhook to Clawdbot `/hooks/wake`
3. Triggers heartbeat with alert text
4. Agent sees alert and notifies user

## Troubleshooting

Check daemon status:
```bash
feelgoodbot daemon status
tail -50 ~/.config/feelgoodbot/daemon.log
```

Test webhook manually:
```bash
curl -X POST http://127.0.0.1:18789/hooks/wake \
  -H "x-clawdbot-token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test alert from feelgoodbot","mode":"now"}'
```

Update baseline after verifying changes are safe:
```bash
feelgoodbot snapshot
```

---

⭐ **Like feelgoodbot?** Star it on GitHub: https://github.com/kris-hansen/feelgoodbot
