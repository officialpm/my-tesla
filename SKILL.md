---
name: my-tesla
description: Control Tesla vehicles from macOS via the Tesla Owner API using teslapy (auth, list cars, status, lock/unlock, climate, charging, location, and extras). Use when you want to check your car state or run safe remote commands. Designed for Parth Maniar (@officialpm) with local-only auth caching, confirmation gates for disruptive actions, and chat-friendly status output.
---

# My Tesla

**Author:** Parth Maniar — [@officialpm](https://github.com/officialpm)

A practical Tesla control skill for Clawdbot built on `teslapy`.

## Setup

### Requirements

- `TESLA_EMAIL` env var set (your Tesla account email)
- Python 3.10+
- Python dependency: `teslapy` (install: `python3 -m pip install teslapy`)
- Repo hygiene: the CLI auto-cleans `__pycache__` / `*.pyc` under `{baseDir}` to keep `git status` clean

### First-time authentication

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

This opens a Tesla login URL. Log in, then paste the callback URL back into the CLI.

- Token cache: `~/.tesla_cache.json` (local only; best-effort chmod `0600`)
- Optional: set `MY_TESLA_DEFAULT_CAR` to a vehicle display name to pick a default car via env var
- Or persist a local default with: `python3 {baseDir}/scripts/tesla.py default-car "Name"` (writes `~/.my_tesla.json`; best-effort chmod `0600`). By default it validates the name against your account; use `--force` to skip validation.

## Commands

```bash
# List vehicles
python3 {baseDir}/scripts/tesla.py list
python3 {baseDir}/scripts/tesla.py list --json   # machine-readable, privacy-safe

# Version
python3 {baseDir}/scripts/tesla.py version
python3 {baseDir}/scripts/tesla.py --version

# Debugging
# If something fails unexpectedly, add --debug for a full traceback
# (or set MY_TESLA_DEBUG=1)
python3 {baseDir}/scripts/tesla.py --debug status --no-wake

# Reliability (transient API failures)
# Many read-only commands fetch vehicle_data and will retry a couple times by default.
# Tune/disable retries with:
python3 {baseDir}/scripts/tesla.py --retries 0 status
python3 {baseDir}/scripts/tesla.py --retries 5 --retry-delay 0.25 report

# Pick a car (optional)
# --car accepts: exact name, partial name (substring match), or a 1-based index from `list`
python3 {baseDir}/scripts/tesla.py --car "Model" status
python3 {baseDir}/scripts/tesla.py --car 1 report

# Set a default car (used when --car is not passed)
# Accepts exact name / partial name / 1-based index from `list`.
# Use --force to set without validating against the Tesla API.
python3 {baseDir}/scripts/tesla.py default-car "My Model 3"
python3 {baseDir}/scripts/tesla.py default-car 1
python3 {baseDir}/scripts/tesla.py default-car "My Model 3" --force

# One-line summary (best for chat)
python3 {baseDir}/scripts/tesla.py summary
python3 {baseDir}/scripts/tesla.py summary --no-wake   # don't wake a sleeping car
python3 {baseDir}/scripts/tesla.py --metric summary    # show km instead of miles

# Summary as JSON (privacy-safe)
# Unlike `status --json`, this emits a small sanitized object (no location).
# Includes `usable_level_percent` when the vehicle reports it.
python3 {baseDir}/scripts/tesla.py summary --json
python3 {baseDir}/scripts/tesla.py summary --json --raw-json   # raw vehicle_data (may include location)

# One-screen report (chat friendly, more detail)
# Includes battery/charging/climate + (when available) TPMS tire pressures.
# Includes "Usable battery" when the vehicle reports it (helpful for health/degradation).
# Also includes a quick openings summary (doors/trunk/frunk/windows) when available.
# When available, includes a compact seat heater summary line.
# When actively charging, also shows charging power details when available (kW / V / A).
# When available, also shows the requested charging current (A) and the max allowed.
# When Tesla provides it, also shows an estimated finish time ("full at HH:MM").
# When the vehicle reports it, includes fast-charger info (e.g., Supercharger/CCS).
# When the vehicle reports it, includes scheduled departure / preconditioning / off-peak charging status.
# When the vehicle reports it, includes software version + last-updated timestamp.
python3 {baseDir}/scripts/tesla.py report
python3 {baseDir}/scripts/tesla.py report --compact    # core lines only (also makes `--json` output compact)
python3 {baseDir}/scripts/tesla.py report --json --compact   # small sanitized JSON payload
python3 {baseDir}/scripts/tesla.py report --no-wake
python3 {baseDir}/scripts/tesla.py --metric report    # show km instead of miles (and km/h instead of mph where applicable)

# Detailed status
python3 {baseDir}/scripts/tesla.py status
python3 {baseDir}/scripts/tesla.py status --no-wake
python3 {baseDir}/scripts/tesla.py --metric status   # show km instead of miles
python3 {baseDir}/scripts/tesla.py status --summary   # include one-line summary + detailed output
python3 {baseDir}/scripts/tesla.py --car "My Model 3" status

# JSON output (prints ONLY JSON; good for piping/parsing)
# NOTE: `status --json` outputs *raw* `vehicle_data`, which may include location/drive_state.
# Prefer `summary --json` (sanitized) or `report --json` (sanitized) unless you explicitly need the raw payload.
python3 {baseDir}/scripts/tesla.py summary --json              # sanitized summary object (no location)
python3 {baseDir}/scripts/tesla.py report --json               # sanitized report object (no location; includes scheduled charging + charge port state)
python3 {baseDir}/scripts/tesla.py status --json               # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py status --json --safe-json    # sanitized summary object (no location)
python3 {baseDir}/scripts/tesla.py report --json --raw-json     # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py summary --json --raw-json    # raw vehicle_data (may include location)
python3 {baseDir}/scripts/tesla.py charge status --json   # includes usable battery + scheduled charging + (when charging) power details (kW/V/A)
# Sanitized JSON outputs include both miles + kilometers (e.g., range_mi + range_km).

# Lock / unlock
python3 {baseDir}/scripts/tesla.py lock
python3 {baseDir}/scripts/tesla.py lock --no-wake    # refuse waking (exits 3 if asleep/offline)
python3 {baseDir}/scripts/tesla.py unlock --yes
python3 {baseDir}/scripts/tesla.py unlock --yes --no-wake

# Climate (status is read-only)
# Output includes defrost/preconditioning flags when the vehicle reports them.
python3 {baseDir}/scripts/tesla.py climate status
python3 {baseDir}/scripts/tesla.py climate status --no-wake
python3 {baseDir}/scripts/tesla.py climate on
python3 {baseDir}/scripts/tesla.py climate off
python3 {baseDir}/scripts/tesla.py climate defrost on
python3 {baseDir}/scripts/tesla.py climate defrost off
python3 {baseDir}/scripts/tesla.py climate temp 72      # default: °F
python3 {baseDir}/scripts/tesla.py climate temp 22 --celsius

# Charging
python3 {baseDir}/scripts/tesla.py charge status
python3 {baseDir}/scripts/tesla.py charge status --no-wake
python3 {baseDir}/scripts/tesla.py charge start --yes
python3 {baseDir}/scripts/tesla.py charge stop  --yes
python3 {baseDir}/scripts/tesla.py charge limit 80 --yes   # 50–100
python3 {baseDir}/scripts/tesla.py charge amps 16 --yes    # 1–48 (conservative guardrail)

# Scheduled charging (set/off are safety gated)
python3 {baseDir}/scripts/tesla.py scheduled-charging status
python3 {baseDir}/scripts/tesla.py scheduled-charging status --no-wake
python3 {baseDir}/scripts/tesla.py scheduled-charging set 23:30 --yes
python3 {baseDir}/scripts/tesla.py scheduled-charging set 2330  --yes   # compact HHMM
python3 {baseDir}/scripts/tesla.py scheduled-charging set 7     --yes   # hour-only (07:00)
python3 {baseDir}/scripts/tesla.py scheduled-charging set 7:30pm --yes  # 12-hour time
python3 {baseDir}/scripts/tesla.py scheduled-charging off --yes

# Scheduled departure (read-only)
# Shows scheduled departure, preconditioning, and off-peak charging flags (when the vehicle reports them).
python3 {baseDir}/scripts/tesla.py scheduled-departure status
python3 {baseDir}/scripts/tesla.py scheduled-departure status --no-wake
python3 {baseDir}/scripts/tesla.py --json scheduled-departure status

# Set/disable scheduled departure (requires --yes)
python3 {baseDir}/scripts/tesla.py scheduled-departure set 07:30 --yes
python3 {baseDir}/scripts/tesla.py scheduled-departure off --yes

# Location (approx by default; use --yes for precise coordinates)
python3 {baseDir}/scripts/tesla.py location
python3 {baseDir}/scripts/tesla.py location --no-wake
python3 {baseDir}/scripts/tesla.py location --digits 1   # coarser rounding
python3 {baseDir}/scripts/tesla.py location --digits 3   # a bit more precise (still approximate)
python3 {baseDir}/scripts/tesla.py location --yes

# Wake (safety gated)
python3 {baseDir}/scripts/tesla.py wake --yes

# Tire pressures (TPMS)
python3 {baseDir}/scripts/tesla.py tires
python3 {baseDir}/scripts/tesla.py tires --no-wake

# Openings (doors/trunks/windows)
python3 {baseDir}/scripts/tesla.py openings
python3 {baseDir}/scripts/tesla.py openings --no-wake
python3 {baseDir}/scripts/tesla.py openings --json

# Trunk / frunk
python3 {baseDir}/scripts/tesla.py trunk status trunk
python3 {baseDir}/scripts/tesla.py trunk status frunk --no-wake
python3 {baseDir}/scripts/tesla.py trunk open trunk  --yes
python3 {baseDir}/scripts/tesla.py trunk close trunk --yes
python3 {baseDir}/scripts/tesla.py trunk toggle frunk --yes
# Note: open/close use a toggle endpoint under the hood; if state can't be determined,
# the command refuses unless you add --force (to avoid accidental toggles).

# Windows
python3 {baseDir}/scripts/tesla.py windows status
python3 {baseDir}/scripts/tesla.py windows status --no-wake
python3 {baseDir}/scripts/tesla.py windows status --json

# Windows (safety gated)
python3 {baseDir}/scripts/tesla.py windows vent  --yes
python3 {baseDir}/scripts/tesla.py windows close --yes

# Seat heaters
python3 {baseDir}/scripts/tesla.py seats status
python3 {baseDir}/scripts/tesla.py seats status --no-wake
python3 {baseDir}/scripts/tesla.py seats status --json

# Seat heaters (safety gated)
# seat: driver|passenger|rear-left|rear-center|rear-right|3rd-left|3rd-right (or 0–6)
# level: 0–3 (0=off)
python3 {baseDir}/scripts/tesla.py seats set driver 3 --yes

# Set ALL seat heaters to a level (safety gated)
python3 {baseDir}/scripts/tesla.py seats all 1 --yes

# Turn ALL seat heaters off (safety gated)
python3 {baseDir}/scripts/tesla.py seats off --yes

# Sentry Mode (status is read-only; on/off safety gated)
python3 {baseDir}/scripts/tesla.py sentry status
python3 {baseDir}/scripts/tesla.py sentry status --no-wake
python3 {baseDir}/scripts/tesla.py sentry on  --yes
python3 {baseDir}/scripts/tesla.py sentry off --yes

# Valet mode (status is read-only; on/off/reset-pin safety gated)
# Note: enabling valet mode usually requires a PIN/password
python3 {baseDir}/scripts/tesla.py valet status
python3 {baseDir}/scripts/tesla.py valet status --no-wake
python3 {baseDir}/scripts/tesla.py valet status --json
python3 {baseDir}/scripts/tesla.py valet on --pin 1234 --yes
python3 {baseDir}/scripts/tesla.py valet off --yes
python3 {baseDir}/scripts/tesla.py valet reset-pin --yes

# Charge port door
python3 {baseDir}/scripts/tesla.py charge-port status
python3 {baseDir}/scripts/tesla.py charge-port status --no-wake
python3 {baseDir}/scripts/tesla.py charge-port status --json

# Mileage tracking (odometer) — local SQLite
python3 {baseDir}/scripts/tesla.py mileage init
python3 {baseDir}/scripts/tesla.py mileage record --no-wake --auto-wake-after-hours 24
python3 {baseDir}/scripts/tesla.py mileage status
python3 {baseDir}/scripts/tesla.py mileage export --format csv
python3 {baseDir}/scripts/tesla.py mileage export --format csv --since-days 7
python3 {baseDir}/scripts/tesla.py mileage export --format json
python3 {baseDir}/scripts/tesla.py mileage export --format json --since-ts 1738195200

# Charge port door open/close (safety gated)
python3 {baseDir}/scripts/tesla.py charge-port open  --yes
python3 {baseDir}/scripts/tesla.py charge-port close --yes

# Fun / attention-grabbing
python3 {baseDir}/scripts/tesla.py honk   --yes
python3 {baseDir}/scripts/tesla.py flash  --yes
```

## Safety defaults

Some actions require an explicit confirmation flag:
- `unlock`, `charge start|stop|limit|amps`, `trunk`, `windows`, `seats set|all|off`, `sentry on|off`, `valet on|off|reset-pin`, `honk`, `flash`, `charge-port open|close`, and `scheduled-charging set|off` require `--yes`
- `location` is *approximate* by default; add `--yes` for precise coordinates (or `--digits N` to control rounding)

## Privacy

- Credentials are cached locally only (`~/.tesla_cache.json`).
- Do not commit tokens, logs, VINs, or location outputs.

## Exit codes (automation)

- `0` — success
- `2` — bad/missing arguments (e.g., missing `TESLA_EMAIL`)
- `3` — car is asleep/offline and `--no-wake` was set (refused to wake)
  - For UX, `summary --no-wake`, `report --no-wake`, and `status --no-wake` still print a minimal payload before exiting 3.
