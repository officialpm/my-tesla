# My Tesla

Tesla control skill for Clawdbot.

Author: Parth Maniar — [@officialpm](https://github.com/officialpm)

## What’s inside

- `SKILL.md` — the skill instructions
- `scripts/tesla.py` — the CLI implementation (teslapy)
- `VERSION` + `CHANGELOG.md` — versioning for ClawdHub publishing

## Install / auth

Set `TESLA_EMAIL` and run:

```bash
TESLA_EMAIL="you@email.com" python3 scripts/tesla.py auth
```

This uses a browser-based login flow and stores tokens locally in `~/.tesla_cache.json`.

## Usage

```bash
python3 scripts/tesla.py list

# One-line summary (best for chat)
python3 scripts/tesla.py summary

# Detailed status
python3 scripts/tesla.py status

python3 scripts/tesla.py --car "My Model 3" lock
python3 scripts/tesla.py climate temp 72
python3 scripts/tesla.py charge limit 80
```

## Privacy / safety

- Never commit tokens, VINs, or location outputs.
- Some commands (honk/flash) require `--yes`.
