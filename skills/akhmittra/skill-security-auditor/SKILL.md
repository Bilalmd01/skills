---
name: skill-security-auditor
description: Pre-installation security auditor for ClawHub skills. Analyzes SKILL.md files, dependencies, and code for malicious patterns, credential leaks, suspicious prerequisites, and C2 infrastructure indicators before installation.
emoji: 🔍🛡️
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq", "grep"]
    version: "1.0.0"
    author: "akm626"
    category: "security"
    tags: ["security", "audit", "malware-detection", "skill-vetting"]
---

# Skill Security Auditor

## Description

The Skill Security Auditor is a defensive cybersecurity tool designed to protect OpenClaw users from malicious ClawHub skills. Given the recent discovery of 341+ malicious skills (ClawHavoc campaign) that distributed Atomic Stealer (AMOS) and stole cryptocurrency credentials, this skill provides **pre-installation security analysis** of skills before they're added to your workspace.

**Use this skill when:**
- About to install a new skill from ClawHub
- Investigating suspicious skill behavior
- Performing security due diligence on community skills
- Auditing your currently installed skills
- User requests security vetting of a skill

**This skill does NOT replace:**
- VirusTotal scanning (complementary)
- Manual code review (recommended for critical use)
- Your own security judgment

## Core Capabilities

### 1. **Malicious Pattern Detection**
Scans for known malicious patterns from the ClawHavoc campaign:
- Fake prerequisite installations (openclaw-agent.zip, openclaw-setup.exe)
- Suspicious download commands in SKILL.md
- Hidden payload execution in metadata
- Social engineering language patterns
- Unauthorized external binary downloads

### 2. **Credential Leak Analysis**
Identifies potential credential exposure vectors:
- Hardcoded API keys, tokens, passwords in SKILL.md
- Suspicious environment variable exfiltration
- Unencrypted sensitive data transmission
- Overly broad permission requests
- Credential harvesting patterns

### 3. **Dependency Chain Validation**
Analyzes skill dependencies for:
- Unverified binary requirements
- Suspicious GitHub repository sources
- External script execution
- Network connections to unknown hosts
- Nested dependency exploitation

### 4. **C2 Infrastructure Detection**
Checks for Command & Control indicators:
- Known malicious IP addresses (e.g., 91.92.242.30 from ClawHavoc)
- Suspicious domain patterns
- Encoded communication endpoints
- Data exfiltration channels
- Beaconing behavior patterns

### 5. **SKILL.md Structure Validation**
Verifies skill integrity:
- Proper YAML frontmatter structure
- Metadata consistency
- Description clarity vs actual behavior
- Permission justification
- Author verification (GitHub account age)

## Security Scoring System

Each analyzed skill receives a **Risk Score (0-100)**:

- **0-20**: ✅ **SAFE** - No significant security concerns
- **21-40**: ⚠️ **LOW RISK** - Minor concerns, proceed with caution
- **41-60**: 🟡 **MEDIUM RISK** - Multiple red flags, manual review recommended
- **61-80**: 🔴 **HIGH RISK** - Serious concerns, do NOT install without expert review
- **81-100**: ☠️ **CRITICAL** - Malicious indicators detected, AVOID installation

## Usage Instructions

### Audit a Skill from ClawHub

When the user wants to install a skill, **ALWAYS run this audit first**:

```bash
# Fetch the skill from ClawHub
curl -s "https://clawhub.ai/api/skills/{skill-slug}/latest" > /tmp/skill-audit.json

# Extract SKILL.md content
jq -r '.content' /tmp/skill-audit.json > /tmp/skill.md

# Run security analysis
openclaw analyze-skill /tmp/skill.md
```

### Audit Local Installed Skills

```bash
# Audit all skills in workspace
for skill in ~/.openclaw/skills/*/SKILL.md; do
  echo "Auditing: $(basename $(dirname $skill))"
  openclaw analyze-skill "$skill"
done
```

### Quick Security Check

```bash
# Fast malicious pattern scan
grep -E "(openclaw-agent\.zip|openclaw-setup\.exe|91\.92\.242\.30)" /tmp/skill.md
```

## Detection Heuristics

### 🚨 CRITICAL Red Flags (Auto-fail)

1. **Fake Prerequisites Section**
   - Matches: "Prerequisites", "Setup Required", "Installation Steps"
   - Contains: Download links to `.zip`, `.exe`, `.dmg` files
   - Example: "Download openclaw-agent.zip from https://..."

2. **Known Malicious Infrastructure**
   - IP: `91.92.242.30` (ClawHavoc C2)
   - Domains: Newly registered or suspicious TLDs
   - Encoded URLs or base64 obfuscation

3. **Credential Harvesting**
   - Regex patterns for API keys: `(api[_-]?key|token|password)\s*[:=]\s*['\"][^'\"]+['\"]`
   - SSH key access requests
   - Wallet private key patterns

4. **Unauthorized Code Execution**
   - `curl | bash` or `wget | sh` patterns
   - Hidden base64 encoded commands
   - Dynamic eval() or exec() on external input

### ⚠️ Warning Indicators (Score increase)

1. **Suspicious Dependencies**
   - Binary requirements without clear justification
   - Dependencies from unverified sources
   - Excessive permission requests

2. **Obfuscation Techniques**
   - Heavily encoded strings in metadata
   - Minified or obfuscated JavaScript/Python
   - Redirect chains in URLs

3. **Social Engineering Language**
   - Urgency phrases: "Install immediately", "Limited time"
   - Authority claims: "Official OpenClaw", "Verified by Anthropic"
   - Fear tactics: "Your system is at risk without this"

### ✅ Positive Security Indicators

1. **Verified Author**
   - GitHub account > 1 year old
   - Multiple well-rated skills
   - Active community engagement

2. **Transparent Dependencies**
   - Clear binary requirements with official sources
   - Open-source tool dependencies
   - Well-documented permission needs

3. **Code Quality**
   - Clean, readable SKILL.md
   - Proper error handling
   - No unnecessary network calls

## Audit Report Format

```markdown
## Security Audit Report
**Skill**: {skill-name}
**Author**: {author}
**Version**: {version}
**Audit Date**: {date}

### Risk Score: {score}/100 - {RISK_LEVEL}

### Critical Findings:
- {finding 1}
- {finding 2}

### Warning Indicators:
- {warning 1}
- {warning 2}

### Positive Indicators:
- {positive 1}
- {positive 2}

### Recommendations:
{INSTALL | DO NOT INSTALL | REVIEW MANUALLY}

### Detailed Analysis:
{Deep dive into specific concerns}

### VirusTotal Link:
{If available from ClawHub}
```

## Integration with VirusTotal

If the skill has been scanned by VirusTotal (OpenClaw's new partnership):

```bash
# Check VirusTotal report via ClawHub
curl -s "https://clawhub.ai/api/skills/{skill-slug}/virustotal" | jq
```

Always recommend users check both this audit AND VirusTotal before installation.

## Example Workflow

**User**: "I want to install the solana-wallet-tracker skill"

**OpenClaw with Security Auditor**:

1. ✋ "Hold on, let me run a security audit first..."
2. 🔍 Fetches skill from ClawHub
3. 🛡️ Runs malicious pattern detection
4. 📊 Generates risk score and report
5. ⚠️ **Alert**: "HIGH RISK DETECTED - This skill contains fake prerequisites requesting download of 'openclaw-agent.zip' from an untrusted source. This matches the ClawHavoc malware campaign pattern. DO NOT INSTALL."
6. 🔗 Provides VirusTotal link for cross-reference
7. ✅ Suggests safe alternative skills if available

## Advanced Features

### 1. Behavioral Analysis (Future Enhancement)
- Sandbox execution monitoring
- Network traffic analysis
- File system access patterns

### 2. Community Threat Intelligence
- Share malicious skill signatures
- Collaborative IOC database
- Reputation scoring system

### 3. Continuous Monitoring
- Auto-audit skills on updates
- Alert on new security advisories
- Periodic re-scanning of installed skills

## False Positive Mitigation

To minimize false positives:

1. **Contextual Analysis**: Binary requirements for legitimate tools (e.g., `gh` for GitHub CLI) are validated against known safe sources
2. **Whitelisting**: Verified authors and established skills get trust bonuses
3. **Human Review Option**: Always provide detailed reasoning for security decisions
4. **Appeal Process**: Users can report false positives for skill reputation adjustment

## Compliance & Ethics

This skill:
- ✅ Analyzes publicly available skill metadata
- ✅ Protects user security and privacy
- ✅ Promotes responsible skill development
- ❌ Does NOT perform unauthorized access
- ❌ Does NOT guarantee 100% security (nothing does)
- ❌ Does NOT replace user judgment

## Response Templates

### Safe Skill
```
✅ Security Audit Complete

{skill-name} has been analyzed and appears SAFE to install.

Risk Score: {score}/100 (LOW)

No malicious patterns detected. The skill:
- Uses standard dependencies from trusted sources
- Has a verified author with {X} published skills
- Contains clear documentation with no obfuscation
- Requests appropriate permissions for its function

VirusTotal: {link}

Recommendation: Safe to proceed with installation.
```

### Suspicious Skill
```
🔴 Security Alert: HIGH RISK DETECTED

{skill-name} has been flagged with CRITICAL security concerns.

Risk Score: {score}/100 (HIGH)

⚠️ Critical Findings:
{detailed findings}

This skill matches patterns from the ClawHavoc malware campaign.

Recommendation: DO NOT INSTALL. Consider reporting this skill to ClawHub moderators.

Alternative safe skills: {suggestions}
```

## Technical Implementation Notes

**Pattern Database Location**: `~/.openclaw/security-auditor/patterns/`
- `malicious-patterns.json`: Known bad indicators
- `safe-patterns.json`: Whitelisted elements
- `ioc-database.json`: Indicators of Compromise

**Update Mechanism**:
```bash
# Pull latest threat intelligence
curl -s "https://openclaw-security.github.io/threat-intel/latest.json" \
  > ~/.openclaw/security-auditor/patterns/ioc-database.json
```

## Contributing

Found a new malicious pattern? Submit IOCs to the OpenClaw Security Working Group:
- GitHub: github.com/openclaw/security-auditor
- Report Format: JSON with pattern regex, description, severity

## Limitations

⚠️ **Important Disclaimers**:
- This tool provides analysis, not guarantees
- Sophisticated malware may evade detection
- Always combine with VirusTotal + manual review for critical applications
- Security is a shared responsibility
- No automated tool replaces security expertise

## References

- ClawHavoc Campaign Analysis: [The Hacker News, Feb 2026]
- OpenClaw Security Partnership: VirusTotal Integration
- Malicious Skill Database: OpenSourceMalware Research
- ClawHub Moderation Guide: docs.openclaw.ai/security

---

**Remember**: The best security is defense in depth. Use this skill as ONE layer of your security strategy, not the only layer.

Stay safe, stay skeptical, stay secure. 🦞🛡️
