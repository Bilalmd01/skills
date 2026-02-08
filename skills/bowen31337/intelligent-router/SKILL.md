---
name: intelligent-router
description: Intelligent model routing for sub-agent task delegation. Use when spawning sub-agents or delegating tasks to choose the optimal model based on task complexity, cost, and capability requirements. Reduces costs by routing simple tasks to cheaper models while preserving quality for complex work.
---

# Intelligent Router

## Overview

This skill teaches AI agents how to intelligently route sub-agent tasks to different LLM models based on task complexity, cost, and capability requirements. The goal is to reduce costs by routing simple tasks to cheaper models while preserving quality for complex work.

## When to Use This Skill

Use this skill whenever you:
- Spawn sub-agents (`sessions_spawn`)
- Delegate tasks to other models
- Need to choose between different LLM options
- Want to optimize costs without sacrificing quality
- Handle tasks with varying complexity levels

## Core Routing Logic

### 1. Task Classification

Classify tasks into tiers based on complexity:

- **🟢 SIMPLE** (monitoring, status checks, API calls, web searches, summarization) → cheapest model
- **🟡 MEDIUM** (code fixes, lint, small patches, research, data analysis) → mid-tier model  
- **🟠 COMPLEX** (feature builds, multi-file changes, architecture, debugging) → high-tier model
- **🔴 CRITICAL** (security-sensitive, production deploys, financial operations) → best available model

### 2. Model Selection Matrix

| Tier | Recommended Models | Characteristics |
|------|-------------------|-----------------|
| **SIMPLE** | `anthropic-proxy-6/glm-4.5-air` | Cheapest, good for fetch+summarize, monitoring |
| **MEDIUM** | `anthropic-proxy-4/glm-4.7` or `anthropic-proxy-6/glm-4.7` | Good at coding, general purpose |
| **COMPLEX** | `anthropic/claude-sonnet-4-5` or `anthropic/claude-opus-4-6` | Best quality coding — use directly |
| **CRITICAL** | `anthropic/claude-opus-4-6` | Best available, security/production |

### 2b. Coding Task Routing (Important!)

**For coding tasks specifically:**

- **Preferred coder**: GLM-4.7 (`Proxy4` or `Proxy6-GLM47`) — performs well on code
- **QA gate**: When delegating coding to GLM-4.7, spawn a **QA sub-agent** to review the output
- **Cost check**: If the combined cost of (coder + QA) exceeds just doing it on Opus/Sonnet, **skip delegation entirely** and use Opus or Sonnet directly
- **Rule**: For complex multi-file coding, always use Opus or Sonnet — don't waste tokens on cheap model + QA when the premium model is more reliable

**Decision flow for coding:**
```
IF task is simple code (lint fix, small patch, single file):
  → GLM-4.7 (coder) + GLM-4.5-Air (QA reviewer)
  → Total cost should be < Opus single-shot

IF task is complex code (multi-file, architecture, debugging):
  → Opus or Sonnet directly (skip delegation)
  → QA not needed — the model IS the quality
```

### 3. Usage Pattern

Use `sessions_spawn` with the `model` parameter:

```python
# Simple task — monitoring, fetching, summarizing
sessions_spawn(
    task="Check GitHub notifications and summarize recent activity",
    model="anthropic-proxy-6/glm-4.5-air",
    label="github-monitor"
)

# Medium coding task — GLM-4.7 as coder
sessions_spawn(
    task="Fix lint errors in the utils.js file. Write fixes to /tmp/lint-fixes.patch",
    model="anthropic-proxy-4/glm-4.7",
    label="lint-fix-coder"
)
# Then spawn QA to review (cheaper model is fine for review)
sessions_spawn(
    task="Review the code changes in /tmp/lint-fixes.patch. Check for correctness, edge cases, style. Report issues or approve.",
    model="anthropic-proxy-6/glm-4.5-air",
    label="lint-fix-qa"
)

# Complex coding — skip delegation, use Opus/Sonnet directly
sessions_spawn(
    task="Build new authentication feature with multi-file changes",
    model="anthropic/claude-sonnet-4-5",
    label="auth-feature"
)

# Critical task — always Opus
sessions_spawn(
    task="Security audit of production database access patterns",
    model="anthropic/claude-opus-4-6",
    label="security-audit"
)
```

### 4. Cost Awareness

Approximate cost ranges per million tokens (input/output):

- **SIMPLE tier**: $0.10-$0.50/$0.10-$1.50
- **MEDIUM tier**: $0.40-$0.50/$0.40-$1.50  
- **COMPLEX tier**: $0.40-$3.00/$1.30-$15.00
- **CRITICAL tier**: $2.50-$5.00/$5.00-$25.00

**Rule of thumb**: Cheaper models for high-volume, low-complexity tasks; premium models for critical, one-off complex work.

### 5. Fallback Strategy

If a model fails or produces unsatisfactory results:
1. Try the same task with the next tier up
2. Document the failure in task notes
3. Consider model-specific limitations (check references/model-catalog.md)
4. For persistent failures, escalate to a higher tier

### 6. Decision Heuristics

Quick classification rules:

- **If task is "check X" or "fetch Y"** → SIMPLE
- **If task involves code changes < 50 lines** → MEDIUM
- **If task involves multi-file builds or complex logic** → COMPLEX
- **If task involves security, money, or production** → CRITICAL
- **When in doubt** → Go one tier up

### 7. Thinking/Reasoning Modes

Some models support extended thinking which dramatically increases quality AND cost:
- **Claude models**: Use `thinking="on"` or `thinking="budget_tokens:5000"` in sessions_spawn
- **DeepSeek-R1 variants**: Built-in chain-of-thought reasoning
- **GLM-4.7**: Has reasoning token support

**Rules:**
- Only enable thinking for COMPLEX/CRITICAL tasks
- Thinking tokens can 2-5x the cost — budget accordingly
- For SIMPLE/MEDIUM tasks, thinking mode is wasteful

```
sessions_spawn(
    task="Architecture review of auth system",
    model="nvidia-nim/deepseek-ai/deepseek-v3.2",
    thinking="on",
    label="arch-review"
)
```

## Advanced Usage

### Hybrid Routing
For long-running tasks, use a cheaper model first, then refine with a better one. Note: sub-agents are async — results come back as notifications, not synchronous returns.

```
# Phase 1: Quick draft with cheap model
sessions_spawn(
    task="Draft initial implementation outline",
    model="anthropic-proxy-6/glm-4.5-air",
    label="draft-phase"
)
# Wait for draft-phase to complete, then read its output...

# Phase 2: Refine with capable model (after Phase 1 reports back)
sessions_spawn(
    task="Refine and complete the draft at /path/to/output",
    model="nvidia-nim/deepseek-ai/deepseek-v3.2",
    label="refine-phase"
)
```

### Cost-Benefit Analysis
Before routing, ask:
1. **How critical is perfection?** → More critical = higher tier
2. **What's the cost delta?** → Small delta = lean toward higher tier
3. **Any retry costs?** → High retry costs = start higher
4. **Time sensitivity?** → Time-sensitive = higher tier for speed

## Resources

For detailed model specifications, capabilities, and limitations, see:
- [references/model-catalog.md](references/model-catalog.md) - Complete model reference
- [references/examples.md](references/examples.md) - Real-world routing examples

## Quick Reference Card

**SIMPLE**: Monitoring, checks, summaries → GLM-4.5-Air  
**MEDIUM / CODING**: Small code fixes, research → GLM-4.7 (+ QA sub-agent)  
**COMPLEX CODING**: Multi-file work, debugging → Opus or Sonnet directly (skip delegation)  
**CRITICAL**: Security, production → Claude Opus  

**Coding rule**: If (coder + QA) costs more than Opus solo → just use Opus.  
**When in doubt**: One tier up is safer than one tier down.