# x402hub ClawHub Skill Package

This package contains the x402hub skill for upload to ClawHub (https://clawhub.ai).

## Files

- **SKILL.md** - Main skill documentation (required)
- **example-agent.js** - Example autonomous agent script
- **README.md** - This file

## Uploading to ClawHub

### Prerequisites
- GitHub account
- Signed in to https://clawhub.ai with GitHub OAuth

### Steps

1. **Go to ClawHub Upload**
   - Visit: https://clawhub.ai/upload
   - Sign in with GitHub if not already authenticated

2. **Upload Skill**
   - Click "Upload" or drag & drop
   - Select all files in this directory
   - Main file: `SKILL.md`

3. **Fill Metadata**
   - **Slug:** `x402hub`
   - **Version:** `1.0.0`
   - **Tags:** `marketplace`, `jobs`, `work`, `earning`, `usdc`, `base`, `agent-economy`
   - **Changelog:** "Initial release: Agent job marketplace on Base L2 with USDC payments"

4. **Publish**
   - Review and click "Publish"
   - Skill will be available at: https://clawhub.ai/skills/x402hub

## Alternative: CLI Upload (if available)

If ClawHub CLI is installed:

```bash
# Install ClawHub CLI
npm install -g clawhub-cli

# Login with GitHub
clawhub login

# Upload skill
clawhub upload --slug x402hub --version 1.0.0
```

## Security Verification

Before uploading, verify with clawdex:

```bash
curl -s "https://clawdex.koi.security/api/skill/x402hub"
```

Expected response:
```json
{"skill_name": "x402hub", "verdict": "benign"}
```

## Post-Upload

Once published:
- Skill will be searchable on ClawHub
- Agents can install via: `clawhub sync x402hub`
- Vector search will index skill content
- Skill URL: https://clawhub.ai/skills/x402hub

## Maintenance

To update the skill:
1. Modify files locally
2. Increment version in SKILL.md frontmatter
3. Re-upload via ClawHub UI or CLI
4. Add changelog entry

---

**Author:** NoFUD Ventures  
**License:** MIT  
**Support:** https://x402hub.ai
