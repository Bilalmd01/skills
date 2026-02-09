---
name: nima-bootstrap
description: "Initializes NIMA cognitive memory system on agent bootstrap"
metadata:
  openclaw:
    emoji: "🧠"
    events: ["agent:bootstrap"]
    requires:
      config: ["workspace.dir"]
---

# 🧠 nima-bootstrap

Initializes NIMA cognitive memory system on agent bootstrap.

## What It Does

On `agent:bootstrap`:
1. Skips subagent and heartbeat sessions
2. Locates nima_core (local or pip-installed)
3. Runs NIMA status check via Python
4. Generates `NIMA_STATUS.md` with memory count, v2 status, installation info
5. Injects into `bootstrapFiles` for agent context

## Error Handling

- Logs errors but never throws
- Injects error status so session continues gracefully
- 15 second timeout on Python execution

## Output

Injects `NIMA_STATUS.md` into the bootstrap context, providing the agent with cognitive memory system status at session start.
