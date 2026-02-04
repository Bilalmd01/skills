# Workspace Review Checklist

Quick-reference for periodic audits.

## Structure (Required Files)

- [ ] `AGENTS.md` exists
- [ ] `SOUL.md` exists
- [ ] `USER.md` exists
- [ ] `IDENTITY.md` exists
- [ ] `TOOLS.md` exists
- [ ] `memory/` directory exists

## Structure (Optional Files)

- [ ] `HEARTBEAT.md` — if using heartbeats
- [ ] `MEMORY.md` — if maintaining long-term memory
- [ ] `BOOT.md` — if using boot hooks
- [ ] `skills/` — if using workspace skills
- [ ] `docs/` — if maintaining documentation

## File Purpose (No Scope Creep)

- [ ] AGENTS.md: Only operating instructions, no memories
- [ ] SOUL.md: Only persona/tone, no tasks or tech details
- [ ] USER.md: Only user info, no agent memories
- [ ] IDENTITY.md: Only identity facts, no philosophy
- [ ] TOOLS.md: Only environment notes, no procedures
- [ ] HEARTBEAT.md: Short checklist only, no full docs
- [ ] MEMORY.md: Curated insights only, no raw logs

## File Sizes

- [ ] AGENTS.md < 1000 lines
- [ ] SOUL.md < 200 lines
- [ ] USER.md < 100 lines
- [ ] IDENTITY.md < 50 lines
- [ ] HEARTBEAT.md < 100 lines

## Memory Hygiene

- [ ] Daily files use `YYYY-MM-DD.md` naming
- [ ] Reference docs in `memory/` use descriptive names (not dates)
- [ ] No duplicate content between MEMORY.md and daily files
- [ ] Recent daily files reviewed and distilled
- [ ] No API keys or passwords in memory files

## Vector Search Alignment

- [ ] Reference docs are in `memory/`, not `docs/`
- [ ] No important material stranded in `docs/`

## Git Status

**⚠️ Workspace is PRIVATE — never push to GitHub**

- [ ] No public remote configured
- [ ] Working tree clean (or intentionally dirty)
- [ ] No untracked files that should be tracked
- [ ] .gitignore excludes secrets
- [ ] No secrets committed

## No Rogue Files

- [ ] No README.md duplicating AGENTS.md purpose
- [ ] No NOTES.md or similar duplicates
- [ ] No credentials stored in workspace
- [ ] No files that belong in ~/.openclaw/

## Skills (if present)

- [ ] Each skill has SKILL.md
- [ ] Each SKILL.md has name + description frontmatter
- [ ] SKILL.md files are lean (< 500 lines)
- [ ] No duplicate skills vs managed/bundled
