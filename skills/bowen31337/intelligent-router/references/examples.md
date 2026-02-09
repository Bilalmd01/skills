# Real-World Routing Examples

Practical examples of intelligent routing decisions for common agent tasks.

## Monitoring & Status Checks (SIMPLE Tier)

### Example 1: Heartbeat Checks
**Task**: "Check system status and report any anomalies"
**Classification**: SIMPLE (monitoring, status check)
**Model**: `anthropic-proxy-6/glm-4.5-air`
**Reasoning**: Heartbeats are routine, low-complexity checks that don't require advanced reasoning. GLM-4.5-Air is the cheapest cloud option.
**Code**:
```python
sessions_spawn(
    task="Run system heartbeat: check disk space, memory usage, and process status",
    model="anthropic-proxy-6/glm-4.5-air",
    label="heartbeat-check"
)
```

### Example 2: GitHub Notification Check
**Task**: "Check GitHub for new notifications and summarize"
**Classification**: SIMPLE (API call, summarization)
**Model**: `anthropic-proxy-6/glm-4.5-air`
**Reasoning**: Fetching and summarizing notifications is straightforward. No complex reasoning required.
**Code**:
```python
sessions_spawn(
    task="Fetch GitHub notifications, categorize by type (PRs, issues, comments), and summarize urgent items",
    model="anthropic-proxy-6/glm-4.5-air",
    label="github-notifications"
)
```

## Development Tasks (MEDIUM Tier)

### Example 3: CI Lint Fix
**Task**: "Fix ESLint errors in the utils.js file"
**Classification**: MEDIUM (code fix < 50 lines)
**Model**: `nvidia-nim/meta/llama-3.3-70b-instruct`
**Reasoning**: Lint fixes are algorithmic and well-defined. Llama 3.3 70B is cost-effective for code tasks.
**Code**:
```python
sessions_spawn(
    task="Fix all ESLint errors in utils.js: 15 errors involving arrow functions, variable declarations, and missing semicolons",
    model="nvidia-nim/meta/llama-3.3-70b-instruct",
    label="eslint-fix"
)
```

### Example 4: Research Summary
**Task**: "Research latest React best practices and summarize"
**Classification**: MEDIUM (research, analysis)
**Model**: `anthropic-proxy-6/glm-4.7`
**Reasoning**: Research requires good comprehension and synthesis. GLM-4.7 provides better quality than GLM-4.5-Air but isn't premium.
**Code**:
```python
sessions_spawn(
    task="Research React 19 best practices, compare with React 18 patterns, and create a summary document",
    model="anthropic-proxy-6/glm-4.7",
    label="react-research"
)
```

## Complex Development (COMPLEX Tier)

### Example 5: Feature Build
**Task**: "Build new authentication feature with JWT, middleware, and tests"
**Classification**: COMPLEX (multi-file feature build)
**Model**: `nvidia-nim/deepseek-ai/deepseek-v3.2`
**Reasoning**: Multi-file architecture requires excellent code understanding. DeepSeek V3.2 is specifically good at code generation.
**Code**:
```python
sessions_spawn(
    task="Build authentication system: JWT token generation/validation, auth middleware, user schema, unit tests. Create 5+ files with proper architecture.",
    model="nvidia-nim/deepseek-ai/deepseek-v3.2",
    label="auth-system"
)
```

### Example 6: Debugging Complex Issue
**Task**: "Debug race condition in concurrent file processing"
**Classification**: COMPLEX (debugging, complex logic)
**Model**: `nvidia-nim/deepseek-ai/deepseek-v3.2`
**Reasoning**: Debugging race conditions requires deep reasoning about concurrency. DeepSeek's strong reasoning capabilities help.
**Code**:
```python
sessions_spawn(
    task="Debug race condition: file processing workers sometimes skip files when running concurrently. Analyze code and propose fix.",
    model="nvidia-nim/deepseek-ai/deepseek-v3.2",
    label="race-condition-debug"
)
```

## Critical Operations (CRITICAL Tier)

### Example 7: Security Audit
**Task**: "Audit authentication code for security vulnerabilities"
**Classification**: CRITICAL (security-sensitive)
**Model**: `anthropic/claude-opus-4-6`
**Reasoning**: Security flaws can have severe consequences. Opus provides the highest quality analysis.
**Code**:
```python
sessions_spawn(
    task="Security audit of authentication system: check for SQL injection, JWT implementation flaws, session management issues, and password handling vulnerabilities",
    model="anthropic/claude-opus-4-6",
    label="security-audit"
)
```

### Example 8: Production Database Migration
**Task**: "Plan and execute production database schema migration"
**Classification**: CRITICAL (production deployment)
**Model**: `anthropic/claude-opus-4-6`
**Reasoning**: Production migrations carry high risk. Opus's careful reasoning minimizes mistakes.
**Code**:
```python
sessions_spawn(
    task="Plan zero-downtime migration: add new columns to users table, create migration script with rollback, test thoroughly",
    model="anthropic/claude-opus-4-6",
    label="db-migration"
)
```

## Market & Financial (Variable Tier)

### Example 9: Market Monitoring
**Task**: "Monitor cryptocurrency markets and flag significant movements"
**Classification**: MEDIUM (data analysis, monitoring)
**Model**: `anthropic-proxy-6/glm-4.7`
**Reasoning**: Pattern recognition in market data requires decent analysis but not frontier-model level.
**Code**:
```python
sessions_spawn(
    task="Monitor top 10 cryptocurrencies for >5% price movements in past hour, summarize trends",
    model="anthropic-proxy-6/glm-4.7",
    label="crypto-monitor"
)
```

### Example 10: Financial Analysis
**Task**: "Analyze quarterly financial statements for investment recommendations"
**Classification**: CRITICAL (financial operations)
**Model**: `anthropic/claude-opus-4-6`
**Reasoning**: Financial decisions require careful, accurate analysis. Opus reduces risk of misinterpretation.
**Code**:
```python
sessions_spawn(
    task="Analyze Q3 financial statements: calculate key ratios, identify trends, provide investment recommendation with risk assessment",
    model="anthropic/claude-opus-4-6",
    label="financial-analysis"
)
```

## Cost-Saving Patterns

### Pattern 1: Two-Phase Processing
**Scenario**: Processing a large document
**Phase 1 (SIMPLE)**: Extract key sections with GLM-4.5-Air
**Phase 2 (MEDIUM/COMPLEX)**: Analyze extracted content with better model
**Savings**: Process 90% of tokens with cheap model, only 10% with expensive model

### Pattern 2: Tiered Escalation
**Scenario**: Uncertain task complexity
**Approach**: Start with MEDIUM tier, escalate to COMPLEX if results inadequate
**Example**: Start with Llama 3.3 for code fix, escalate to DeepSeek if stuck
**Savings**: Avoid overpaying for simple tasks

### Pattern 3: Batch Processing
**Scenario**: Multiple similar tasks
**Approach**: Group SIMPLE tasks, process with cheap model
**Example**: Batch 10 monitoring checks together with GLM-4.5-Air
**Savings**: Reduced overhead per task

## Common Mistakes to Avoid

### Mistake 1: Over-Engineering Simple Tasks
**Wrong**: Using Claude Opus for heartbeat checks
**Cost impact**: 150x more expensive than necessary
**Fix**: Always classify task before selecting model

### Mistake 2: Under-Engineering Critical Tasks
**Wrong**: Using GLM-4.5-Air for security audit
**Risk impact**: May miss critical vulnerabilities
**Fix**: When in doubt for critical tasks, go one tier up

### Mistake 3: Ignoring Retry Costs
**Wrong**: Choosing cheapest model, needing 3 retries
**Actual cost**: 3 × cheap model + time delay
**Fix**: Consider likelihood of success, not just per-token cost

## Decision Flowchart

```
Start → Classify Task Complexity
    │
    ├── SIMPLE (monitoring, checks) → GLM-4.5-Air
    │
    ├── MEDIUM (small code, research) → Llama 3.3 70B or GLM-4.7
    │
    ├── COMPLEX (multi-file, debugging) → DeepSeek V3.2
    │
    └── CRITICAL (security, production) → Claude Opus
        │
        └── If cost prohibitive → DeepSeek V3.2
```
