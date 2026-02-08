---
name: nima-recall
description: "Auto-queries NIMA memory and injects relevant memories into session context"
metadata:
  openclaw:
    emoji: "🧠"
    events: ["agent:bootstrap"]
    requires:
      config: ["workspace.dir"]
---

# 🧠 nima-recall

Auto-queries NIMA memory and injects relevant memories into session context.

## What It Does

On `agent:bootstrap`:
1. Skips subagent and heartbeat sessions
2. Extracts last 10 messages from session file
3. Queries NIMA with semantic search
4. Injects `NIMA_RECALL.md` with relevant memories into bootstrapFiles

## Configuration

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "nima-recall": {
          "enabled": true,
          "limit": 3,
          "minScore": 0.0,
          "timeout": 15000
        }
      }
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `limit` | number | `3` | Max memories to retrieve |
| `minScore` | number | `0.0` | Minimum similarity score |
| `timeout` | number | `15000` | Query timeout in ms |

## Output

Injects `NIMA_RECALL.md`:

```markdown
# 🧠 NIMA Recall

Relevant memories from NIMA:

**[1]** user: Asked about project configuration
**[2]** assistant: Explained the hook system

---
*Retrieved 2 memories*
```

## Error Handling

- Logs errors but never throws
- Session continues if NIMA query fails or times out
- Skips if insufficient context (<20 chars)

## Requirements

- `nima-core` installed in workspace
- Python 3 with `nima_core` package
- Session file at `event.context.sessionFile`
