---
name: control-ikea-lightbulb
description: Control IKEA/TP-Link Kasa smart bulbs (set on/off, brightness, and color). Use when you want to programmatically control a local smart bulb by IP on the LAN.
---

# control-ikea-lightbulb

This skill provides a lightweight Python script to control a local smart bulb (supports TP-Link Kasa-compatible bulbs via python-kasa). It is intended for local LAN devices that do not require cloud credentials; control is by IP address.

When to use this skill
- When you want to turn a bulb on or off
- When you want to set brightness (0-100)
- When you want to set color (HSV)
- When you have the bulb's local IP and it's accessible from this machine

Contents
- scripts/control_kasa_light.py — main runnable script (Python 3.9+)
- scripts/light_show.py — small light-show controller for sequences (uses python-kasa). Changes include:
  - Default white uses a high color temperature (9000K) to make white appear "whiter"; pass --white-temp to override.
  - Bug fixes: the off-flash between blue→red now ignores transitions to white (saturation==0) to avoid white<->blue ping-pong, and white-temp is only applied to white steps (fixes red being skipped during off-flash). White steps also set brightness even without --double-write.
- scripts/run_test_light_show.sh — helper to run light_show in the included .venv_kasa virtualenv (or created via bootstrap)

Notes
- This repo provides a bootstrap script at scripts/bootstrap_venv.sh that creates a local .venv_kasa and installs python-kasa on first use. We avoid committing a full virtualenv to keep the repo small and portable. The wrapper (scripts/run_control_kasa.sh) will auto-run the bootstrap on first use if .venv_kasa is missing.
  Example (first-run or when venv exists):
  ./skills/control-ikea-lightbulb/scripts/run_control_kasa.sh --ip 192.168.4.69 --on --hsv 0 100 80 --brightness 80
- You can also run the bootstrap manually:
  ./skills/control-ikea-lightbulb/scripts/bootstrap_venv.sh
- The existing test helper remains available and will use the venv if present:
  ./skills/control-ikea-lightbulb/scripts/run_test_light_show.sh --ip 192.168.4.69 --duration 6 --transition 1 --off-flash --verbose
- If your device is actually an IKEA TRADFRI device (not Kasa), this script is a starting point; tell me and I will add TRADFRI support.
- No cloud credentials are required; control happens over LAN to the device's IP.

Git note
- Add .venv_kasa to your .gitignore if you plan to create the venv locally. The bootstrap script will recreate the environment when needed.
