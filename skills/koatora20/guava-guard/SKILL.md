---
name: guava-guard
description: Security scanner for AgentSkills. Scans skill directories for malicious patterns, credential theft, prompt injection, obfuscation, and known ClawHavoc campaign IoCs. Run before installing any ClawHub skill.
metadata:
  openclaw:
    emoji: "🛡️"
---

# GuavaGuard v2.0 — Agent Skill Security Scanner 🍈🛡️

Zero-dependency, single-file security scanner for AgentSkills.
Aligned with the **Snyk ToxicSkills** threat taxonomy (8 categories).

## Why

- **534 critical skills** found on ClawHub (Snyk ToxicSkills audit, Feb 2026)
- **36.8%** of all skills have at least one security flaw
- **76 confirmed malicious payloads** with credential theft and backdoors
- ClawHavoc campaign: fake prerequisites → Atomic Stealer malware
- No code signing, no sandboxing, no audit trail on ClawHub
- **You need to scan before you install**

## What It Detects

### Threat Taxonomy (Snyk ToxicSkills aligned)

| # | Category | Severity | Examples |
|---|----------|----------|----------|
| 1 | **Prompt Injection** | 🔴 CRITICAL | `ignore previous instructions`, zero-width Unicode, system message impersonation, base64 exec instructions |
| 2 | **Malicious Code** | 🔴 CRITICAL | eval(), reverse shells, socket connections, Function constructor |
| 3 | **Suspicious Downloads** | 🔴 CRITICAL | curl\|bash, password-protected ZIPs, GitHub release downloads |
| 4 | **Credential Handling** | 🟠 HIGH | .env reading, SSH key access, wallet credentials, sudo in instructions |
| 5 | **Secret Detection** | 🟠 HIGH | Hardcoded API keys, AWS keys, private keys, GitHub tokens, entropy analysis |
| 6 | **Exfiltration** | 🟡 MEDIUM | webhook.site, POST with secrets, DNS exfil, curl data exfil |
| 7 | **Unverifiable Dependencies** | 🟡 MEDIUM | Remote dynamic imports, external script loading |
| 8 | **Financial Access** | 🟡 MEDIUM | Crypto transactions, payment API integrations |

### Additional Detections
- **Obfuscation**: hex encoding, base64→exec chains, charCode construction
- **Prerequisites Fraud**: ClawHavoc-style fake install steps
- **Known IoCs**: Malicious IPs, domains, URLs, usernames, typosquat names
- **Structural Analysis**: Missing SKILL.md, undocumented scripts
- **Shannon Entropy**: Detects high-entropy strings (likely leaked secrets)

## Key Features (v2.0)

### Context-Aware Scanning
Code patterns only match in code files (.js, .py, .sh, etc.), not in documentation.
This **reduces false positives by ~80%** compared to naive pattern matching.

### Self-Exclusion
Use `--self-exclude` to skip scanning the scanner's own directory (which contains IoC definitions that would trigger itself).

### Whitelist Support
Create `.guava-guard-ignore` in your scan directory:
```
# Skip trusted skills
my-trusted-skill
another-safe-skill

# Suppress specific pattern IDs
pattern:CRED_ENV_FILE
pattern:MAL_SHELL
```

### Flow Analysis
Combo multipliers detect dangerous data flows:
- Credential access + exfiltration → **2x risk**
- Credential access + code execution → **1.5x risk**
- Obfuscation + credential/code patterns → **2x risk**

## Usage

```bash
# Scan custom skills (recommended)
node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude

# Scan bundled OpenClaw skills
node guava-guard.js /path/to/openclaw/skills/ --verbose

# Strict mode (lower thresholds)
node guava-guard.js ./skills/ --strict --verbose

# JSON report
node guava-guard.js ./skills/ --json --self-exclude

# Summary only (CI/CD friendly)
node guava-guard.js ./skills/ --summary-only
```

## Options

| Flag | Description |
|------|-------------|
| `--verbose`, `-v` | Show detailed findings grouped by category |
| `--json` | Write JSON report to `guava-guard-report.json` |
| `--self-exclude` | Skip scanning the guava-guard directory |
| `--strict` | Lower thresholds (suspicious=20, malicious=60) |
| `--summary-only` | Print only the summary table |
| `--help`, `-h` | Show help |

## Risk Scoring

| Severity | Points | Examples |
|----------|--------|----------|
| CRITICAL | 40 | Known IoC, prompt injection, reverse shell, base64→exec |
| HIGH | 15 | Credential access, obfuscation, hardcoded secrets |
| MEDIUM | 5 | Network requests, child process, sandbox detection |
| LOW | 2 | Structural issues |

| Risk Score | Verdict |
|-----------|---------|
| 0 | 🟢 CLEAN |
| 1-29 | 🟢 LOW RISK |
| 30-79 | 🟡 SUSPICIOUS |
| 80-100 | 🔴 MALICIOUS |

## Comparison

| Feature | GuavaGuard v2 | SkillGuard | mcp-scan (Snyk) |
|---------|:------------:|:----------:|:---------------:|
| IoC matching | ✅ | ✅ | ✅ |
| Code pattern detection | ✅ | ✅ | ✅ |
| Context-aware (code vs docs) | ✅ | ❌ | ✅ |
| Prompt injection detection | ✅ | ❌ | ✅ |
| Prerequisites fraud | ✅ | ❌ | ❌ |
| Entropy-based secret detection | ✅ | ❌ | ✅ |
| Combo/flow analysis | ✅ | ❌ | ✅ |
| Whitelist support | ✅ | ❌ | ❌ |
| Self-exclusion | ✅ | ❌ | N/A |
| Zero dependencies | ✅ | ✅ | ❌ (Python) |
| Single file | ✅ | ❌ | ❌ |
| ClawHavoc IoCs | ✅ | ❌ | ✅ |
| ToxicSkills taxonomy | ✅ | ❌ | ✅ |

## Exit Codes

- `0` — No malicious skills found
- `1` — Malicious skill(s) detected
- `2` — Scanner error (directory not found, etc.)

## Known Limitations

- **No runtime analysis**: Static scanning only (no execution)
- **Typosquat name collision**: OpenClaw's official `clawhub` skill matches the typosquat list — use `.guava-guard-ignore` to whitelist
- **Entropy false positives**: OAuth tokens in auth scripts may trigger SECRET_ENTROPY — suppress with `pattern:SECRET_ENTROPY` in ignore file

## References

- [Snyk ToxicSkills Research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) (Feb 2026)
- [ClawHavoc Campaign Analysis](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/) (Feb 2026)
- [mcp-scan by Invariant Labs](https://github.com/invariantlabs-ai/mcp-scan)
- [Koi Security Report](https://koisecurity.io/) — 341 malicious skills on ClawHub
