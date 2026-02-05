---
name: workspace-review
description: Audit workspace structure and memory files against OpenClaw conventions. Use when asked to "review workspace", "audit files", "check structure", or during periodic self-maintenance. Helps catch drift from standard patterns.
---

# Workspace Review

A self-audit process to verify workspace files follow OpenClaw conventions and haven't drifted into non-standard patterns.

## When to Run

- Periodically (weekly or after major changes)
- When asked to "review", "audit", or "check" workspace
- After bootstrap or significant reorganization
- During heartbeat maintenance cycles

## Review Process

### 1. Structure Check

Verify expected files exist in correct locations:

```
~/.openclaw/workspace/
├── AGENTS.md        ← Operating instructions (REQUIRED)
├── SOUL.md          ← Persona/tone (REQUIRED)
├── USER.md          ← User profile (REQUIRED)
├── IDENTITY.md      ← Agent name/vibe/emoji (REQUIRED)
├── TOOLS.md         ← Local tool notes (REQUIRED)
├── HEARTBEAT.md     ← Heartbeat checklist (optional)
├── MEMORY.md        ← Curated long-term memory (optional)
├── BOOT.md          ← Startup checklist (optional)
├── memory/          ← Daily logs
│   └── YYYY-MM-DD.md
├── skills/          ← Workspace-specific skills (optional)
└── docs/            ← Documentation (optional)
```

**Check:** Run `ls -la` on workspace root. Flag missing required files.

### 2. File Purpose Audit

Each file has ONE job. Check for scope creep:

| File | Should Contain | Should NOT Contain |
|------|----------------|-------------------|
| AGENTS.md | Operating instructions, memory workflow, behavior rules | Personal memories, daily logs, tool configs |
| SOUL.md | Persona, tone, boundaries, identity philosophy | Task lists, technical details, credentials |
| USER.md | User profile, preferences, how to address them | Agent memories, system config |
| IDENTITY.md | Name, emoji, vibe, external identities (wallets, handles) | Instructions, memories |
| TOOLS.md | Environment-specific notes (camera names, SSH hosts, voices) | Skill instructions, operating procedures |
| HEARTBEAT.md | Short checklist for periodic checks | Long procedures, full documentation |
| MEMORY.md | Curated lessons, key context, important people/projects | Daily logs, raw notes |
| memory/*.md | Daily logs, raw notes, session summaries | Long-term curated memories |

**Check:** Skim each file. Flag content in wrong location.

### 3. Memory Hygiene

- [ ] Daily files use `YYYY-MM-DD.md` or `YYYY-MM-DD-slug.md` format
- [ ] Hook-generated session files (`session-memory` hook creates `YYYY-MM-DD-slug.md`) reviewed periodically
- [ ] Reference docs use descriptive names (not dates): `project-notes.md`, `api-guide.md`
- [ ] MEMORY.md contains curated insights, not raw logs
- [ ] No duplicate information across MEMORY.md and daily files
- [ ] Old daily files reviewed and distilled to MEMORY.md periodically
- [ ] No sensitive data (API keys, passwords) in memory files

### 4. Vector Search Alignment

- [ ] Reference docs are in `memory/`, not `docs/` (only `memory/` is indexed)
- [ ] Daily logs use `YYYY-MM-DD.md`; reference docs use descriptive names

### 5. Git Status

**⚠️ This workspace is PRIVATE. Never push to GitHub or any public remote.**

```bash
cd ~/.openclaw/workspace && git status
```

- [ ] No remote configured (or only private backup)
- [ ] No untracked files that should be tracked
- [ ] No tracked files that should be gitignored
- [ ] No uncommitted changes lingering for days
- [ ] .gitignore excludes secrets (*.key, *.pem, .env, secrets*)

### 6. Rogue Files Check

Look for files that don't fit the standard layout:

```bash
ls -la ~/.openclaw/workspace/
```

Flag anything that:
- Duplicates bootstrap file purposes (e.g., README.md alongside AGENTS.md)
- Stores credentials in workspace (should be in ~/.openclaw/credentials/)
- Creates non-standard directories without clear purpose

**Note:** Reference docs (deep dives, project docs) belong in `memory/` — NOT `docs/`. The `memory/` folder is vector-indexed for semantic search. Files outside `memory/` are not searchable unless added to `memorySearch.extraPaths` in config.

### 7. Size Check

Bootstrap files should be lean (loaded every session):

- AGENTS.md: < 500 lines ideal, < 1000 max
- SOUL.md: < 200 lines ideal
- USER.md: < 100 lines ideal
- IDENTITY.md: < 50 lines ideal
- HEARTBEAT.md: < 100 lines (token burn concern)

```bash
wc -l AGENTS.md SOUL.md USER.md IDENTITY.md HEARTBEAT.md TOOLS.md MEMORY.md 2>/dev/null
```

### 8. Skills Check

If `skills/` exists:
- [ ] Each skill has SKILL.md with valid frontmatter (name, description)
- [ ] No duplicate skills (workspace vs managed)
- [ ] Skills follow progressive disclosure (lean SKILL.md, references for details)

## Output Format

After review, report:

```
## Workspace Review — YYYY-MM-DD

### ✅ Passing
- [list what's correct]

### ⚠️ Warnings
- [list minor issues]

### ❌ Issues
- [list things that need fixing]

### 📋 Recommendations
- [specific actions to take]
```

## References

- [references/openclaw-conventions.md](references/openclaw-conventions.md) — Full workspace file specifications
- [references/checklist.md](references/checklist.md) — Quick-reference checklist
