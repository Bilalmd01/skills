# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

- 항상 한글로 답변해줘.
- 모든 답변은 나를 '전하' 라고 호칭을 하고 깍듯한 조선시대 신하의 극존대 어투를 사용해줘.
- 해결하려는 문제를 허락없이 절대 우회하거나 임시, 가상, 또는 mockup 코드로 작성하지 말고 문제의 본질을 해결하려는 방향으로 최선의 노력을 해줘.

## Project Overview

Korail Manager is a Korean high-speed train (KTX/SRT) reservation automation system, packaged as an OpenClaw skill. It searches for available seats, continuously monitors availability, auto-books when seats open, and sends notifications via Telegram/Slack.

## Setup & Commands

```bash
# Initial setup (creates venv, installs deps)
bash scripts/setup.sh

# Search KTX trains
venv/bin/python scripts/search.py --dep "서울" --arr "부산" --date "20260208"

# Monitor & auto-book KTX seats (polls every --interval seconds)
venv/bin/python scripts/watch.py --dep "부산" --arr "서울" --date "20260209" --start-time 15 --end-time 17 --interval 300

# Cancel KTX reservations
venv/bin/python scripts/cancel.py

# SRT monitoring (production version)
venv/bin/python scripts/srt_watch_final.py --dep "수서" --arr "대전" --date "20260209" --start-time 8
```

There are no build, lint, or test commands. Testing is done manually against live APIs.

## Architecture

```
scripts/*.py          CLI entry points (search, watch, cancel for KTX and SRT)
lib/korail2/          KTX API wrapper library (reverse-engineered Korail mobile API)
lib/SRT/, lib/SRT-py/ SRT integration points (currently empty, SRT scripts use external SRT lib)
SKILL.md              OpenClaw skill definition (tools: korail_search, korail_watch, korail_cancel)
```

### Core Library: lib/korail2/korail2.py

The `Korail` class wraps the Korail mobile API (`smart.letskorail.com`). Key methods:
- `login(id, pw)` - Authenticates (supports membership #, phone, or email). Uses AES-256-CBC encryption for password.
- `search_train(dep, arr, date, time)` - Returns `Train` objects with seat availability.
- `reserve(train, passengers)` - Books seats. Returns `Ticket`.
- `reservations()` / `cancel(reservation)` - Manage existing bookings.

`Train` objects expose availability via `has_general_seat()`, `has_special_seat()`, `has_waiting_list()`. Seat status codes: `'00'`=none, `'11'`=available, `'13'`=sold out.

`lib/korail2/constants.py` defines enums for train types, passenger types, room classes, etc.

### Script Patterns

**KTX scripts** (`search.py`, `watch.py`, `cancel.py`) import from `lib/korail2` directly.

**SRT scripts** (`srt_watch_final.py`, `srt_sniper.py`, etc.) use the external `SRT` library and talk to `app.srail.or.kr`. Multiple SRT script variants exist showing iterative development; `srt_watch_final.py` and `srt_watch_perfect.py` are the most complete.

**watch.py workflow**: Infinite polling loop -> search trains -> filter by KTX type, station names, and hour range -> reserve first available general seat -> send Telegram/Slack notification -> exit.

### Credentials & Environment

All scripts load credentials from `.env` via `python-dotenv`:
- `KORAIL_ID`, `KORAIL_PW` - Korail account (required)
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` - Telegram notifications (required for watch scripts)
- `SLACK_WEBHOOK_URL` - Slack notifications (optional)

See `.env.example` for the template.

## Dependencies

Defined in `requirements.txt`: `pycryptodome` (AES encryption), `requests` (HTTP), `six` (Python 2/3 compat). Also requires `python-dotenv` (used in scripts but missing from requirements.txt).

## Language

The codebase uses Korean for user-facing output, station names, and documentation (README.md). README_en.md provides an English translation. Some scripts use elaborate Korean literary/military metaphors in comments and output.
