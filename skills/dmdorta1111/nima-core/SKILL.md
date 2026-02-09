---
name: nima-core
description: Biologically-inspired cognitive memory for AI agents. Panksepp affects, Free Energy consolidation, VSA binding, sparse retrieval, temporal prediction, metacognition.
version: 1.0.0
---

# NIMA Core

Plug-and-play cognitive memory architecture for AI agents.

## Install

```bash
pip install torch numpy sentence-transformers
# Copy nima_core/ to your project
```

## Quick Start

```python
from nima_core import NimaCore

nima = NimaCore(
    name="MyBot",
    important_people={"Alice": 1.5, "Bob": 1.3},  # These people's memories get priority
)
nima.experience("Alice asked about the project", who="Alice", importance=0.7)
results = nima.recall("project")
```

## Smart Consolidation

Configure which people, emotions, and topics matter most:

```python
from nima_core.services.heartbeat import NimaHeartbeat, SmartConsolidation

smart = SmartConsolidation(
    important_people={"Alice": 1.5, "Bob": 1.3},  # Weight multipliers
    emotion_words={"love", "excited", "proud", "worried"},  # Force-consolidate
    importance_markers={"family", "milestone", "decision"},  # Force-consolidate
    noise_patterns=["system exec", "heartbeat_ok"],  # Skip these
)

heartbeat = NimaHeartbeat(nima, message_source=my_source, smart_consolidation=smart)
heartbeat.start_background()
```

Memories from important people get boosted. Emotional content is always kept. Noise is filtered out.

## Enable Components

```bash
export NIMA_V2_ALL=true  # Enable full cognitive stack
```

## API

- `nima.experience(content, who, importance)` — Process through affect → binding → FE pipeline
- `nima.recall(query, top_k)` — Semantic memory search
- `nima.capture(who, what, importance)` — Explicit memory capture (bypasses FE gate)
- `nima.dream(hours)` — Run consolidation (schema extraction)
- `nima.status()` — System status
- `nima.introspect()` — Metacognitive self-reflection

## Architecture

```
METACOGNITIVE  — Self-model, 4-chunk WM, strange loops
SEMANTIC       — Hyperbolic embeddings, concept hierarchies
EPISODIC       — VSA + Holographic storage, sparse retrieval
CONSOLIDATION  — Free Energy decisions, schema extraction
BINDING        — VSA circular convolution, role-filler composition
AFFECTIVE CORE — Panksepp's 7 affects (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `./nima_data` | Memory storage path |
| `NIMA_MODELS_DIR` | `./models` | Model files path |
| `NIMA_V2_ALL` | `false` | Enable all components |
| `NIMA_SPARSE_RETRIEVAL` | `true` | Two-stage sparse index |
| `NIMA_PROJECTION` | `true` | 384D → 50KD projection |

## References

- `README.md` — Full documentation with all settings
- `nima_core/config/nima_config.py` — All feature flags
- `.env.example` — Environment variable template
