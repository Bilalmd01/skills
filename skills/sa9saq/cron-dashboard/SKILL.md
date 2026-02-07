---
description: View and manage OpenClaw cron jobs with status overview and debugging.
---

# cron-dashboard

View and manage OpenClaw cron jobs at a glance.

**Use when** checking cron job status, viewing scheduled tasks, or debugging cron issues.

## Instructions

1. **List all cron jobs** — Run `openclaw cron list` to get all scheduled jobs. Parse and display as a formatted table: name, schedule, model, status, last run, next run.
2. **Show job details** — For a specific job, run `openclaw cron show {id}` to display full config, recent execution history, and output logs.
3. **Check health** — Flag jobs that: haven't run when expected, have repeated failures, or have stale schedules.
4. **Execution history** — Show last 5-10 runs per job with: timestamp, duration, exit status, and truncated output.
5. **Quick actions** — Help user create, pause, resume, or delete cron jobs using `openclaw cron` subcommands.
6. **Summary view** — When asked for "dashboard" or "overview", show a compact summary of all jobs grouped by status (active/paused/failed).

## Notes

- Use `openclaw cron --help` to discover available subcommands if needed.
- Cron expressions: help users understand and write them (e.g., "every 30 minutes" → `*/30 * * * *`).
- Suggest heartbeat-based alternatives for checks that don't need exact timing.
