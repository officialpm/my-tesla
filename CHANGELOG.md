# Changelog

## 0.1.100 — 2026-01-30
- New capability (safety gated): `scheduled-departure set <time>` and `scheduled-departure off` (requires `--yes`).

## 0.1.99 — 2026-01-30
- Better UX/safety: expand `trunk` into `trunk status|open|close|toggle` with a state check for open/close; adds `--force` to override when state is unknown.
- Reliability: add unit tests for the new `trunk` behaviors.

## 0.1.98 — 2026-01-30
- Better UX: add `seats all <level> --yes` to set ALL seat heaters to a given level (0–3) in one shot.
- Reliability: add unit tests for the new `seats all` behavior.

## 0.1.97 — 2026-01-30
- Reliability: add unit tests to lock in `--metric` distance formatting (km vs mi) in summary/report helpers.

## 0.1.96 — 2026-01-30
- Better UX: `report --json --compact` now emits a smaller sanitized JSON payload (using the existing `--compact` flag).

## 0.1.95 — 2026-01-30
- DevX/reliability: add a repo `.gitignore` to prevent accidental commits of bytecode (`__pycache__`, `*.pyc`) and local cache/data files.

## 0.1.94 — 2026-01-30
- Better UX: add `*_km` fields to sanitized JSON outputs (e.g., `battery.range_km`, `odometer_km`, `battery_range_km`) alongside existing miles.

## 0.1.93 — 2026-01-30
- Better UX: `charge status` now shows scheduled charging state/time (when the vehicle reports it).
- Reliability: add unit test coverage for the new human output.

## 0.1.92 — 2026-01-30
- Better UX: `climate status` now shows defrost/preconditioning flags (front/rear defroster, defrost mode, preconditioning) when the vehicle reports them.
- Reliability: add unit tests for the new climate-status fields.

## 0.1.91 — 2026-01-30
- Better UX/privacy: add `status --json --safe-json` to emit a sanitized summary object (no location/drive_state) instead of raw `vehicle_data`.
- Reliability: add unit test coverage for the new `--safe-json` path.

## 0.1.90 — 2026-01-30
- Better UX: add `report --compact` to print a shorter one-screen report (core lines only).
- Reliability: add a unit test to lock in the compact report behavior.

## 0.1.89 — 2026-01-30
- Better UX: `scheduled-charging set` now accepts hour-only and 12-hour am/pm times (e.g., `7`, `7:30pm`) in addition to `HH:MM` / `HHMM`.
- Reliability: add unit tests to lock in the new time parsing behavior.

## 0.1.88 — 2026-01-30
- Better UX: when `status` is run with `--no-wake` and the car is asleep/offline, print a minimal payload (then exit 3) instead of only an error.
- Reliability/docs: add unit tests + update docs to reflect the behavior.

## 0.1.87 — 2026-01-30
- Better UX: when `summary`/`report` are run with `--no-wake` and the car is asleep/offline, print a minimal payload (then exit 3) instead of only an error.
- Reliability: add unit tests for the new `--no-wake` minimal payload behavior.

## 0.1.86 — 2026-01-30
- Better UX: when Tesla omits `charger_power`, derive a best-effort charging kW estimate from voltage/current (shown in `report` and `charge status`).
- Reliability: add unit tests for the new power-derivation behavior.

## 0.1.85 — 2026-01-30
- Better UX: improve the `--yes` safety gate error with a copy/paste re-run suggestion (and add a unit test).

## 0.1.84 — 2026-01-30
- Bugfix/UX: add the missing `--json` flag to `charge-port status` (it was documented and implemented, but not wired in argparse).

## 0.1.83 — 2026-01-30
- Bugfix: fix a CLI startup error caused by defining `--raw-json` twice (argparse conflict). The flag is now defined once with clear help text.

## 0.1.82 — 2026-01-30
- Bugfix/UX: wire up the documented `--raw-json` flag so `report --json --raw-json` / `summary --json --raw-json` actually emit the full raw `vehicle_data` payload (may include location).

## 0.1.81 — 2026-01-30
- Better UX: add global `--metric` flag to show distances in kilometers for human-readable outputs (summary/report/status/charge status).
- Reliability: add unit tests for the new metric output formatting.

## 0.1.80 — 2026-01-29
- Better UX: when actively charging, `report` now shows the requested charging current (and max) when Tesla provides it.
- Reliability: add unit tests for the new report line.

## 0.1.79 — 2026-01-29
- Reliability: add unit tests for `_fmt_local_timestamp_ms` (used by `report` to show "Updated" time) to prevent regressions.

## 0.1.78 — 2026-01-29
- Reliability/privacy: write `~/.my_tesla.json` atomically (prevents partial/corrupt JSON) and keep it private (0600) without a brief world-readable window.
- Reliability: expand unit tests for defaults file permissions + newline/JSON validity.

## 0.1.77 — 2026-01-29
- Better UX: add `--no-wake` to `lock` and `unlock` so you can refuse waking a sleeping/offline vehicle (exits 3 if asleep).

## 0.1.76 — 2026-01-29
- Better UX: `scheduled-charging set` now accepts compact time formats like `2330` / `730` (in addition to `HH:MM`).
- Reliability: add unit tests for the new time parsing behavior.

## 0.1.75 — 2026-01-29
- Better UX: `report` now includes vehicle software version (`car_version`) and an "Updated" timestamp when Tesla provides it.
- Reliability: add unit tests covering the new report fields.

## 0.1.74 — 2026-01-29
- New capability: add `valet` command (status/on/off/reset-pin). Enabling/disabling is safety gated with `--yes`; enabling also requires `--pin`.
- Reliability: add unit tests for the new valet command behavior.

## 0.1.73 — 2026-01-29
- Dev hygiene: add repo-local `sitecustomize.py` so ad-hoc Python runs don’t create `__pycache__/` / `*.pyc` files.

## 0.1.72 — 2026-01-29
- Better UX: when actively charging, `report` now shows an estimated finish time ("full at HH:MM") when Tesla provides `minutes_to_full_charge`.
- Better UX: `report --json` now includes `charging.full_at_local_hhmm` (derived from `minutes_to_full_charge`).
- Reliability: add unit tests for the new time helper.

## 0.1.71 — 2026-01-29
- Docs: document CLI exit codes for easier automation; remove a duplicated `seats status` snippet.

## 0.1.70 — 2026-01-29
- Reliability: add versioning guardrail unit tests to ensure `VERSION`/`VERSION.txt` match and the changelog includes the current version heading.

## 0.1.69 — 2026-01-29
- New capability: add `seats off --yes` to turn off all seat heaters in one command (best-effort for heater ids 0–6).
- Reliability: add unit test coverage for the new `seats off` behavior.

## 0.1.68 — 2026-01-29
- Better UX: `report` now includes fast-charger info (e.g., Supercharger/CCS) when the vehicle reports it.
- Reliability: add unit test coverage for the new sanitized report JSON fields.

## 0.1.67 — 2026-01-29
- Docs: add explicit usage examples for `honk` and `flash` (both safety gated).

## 0.1.66 — 2026-01-29
- Reliability: add `fetch_vehicle_data` retry/backoff to reduce transient API errors on read-only commands.
- UX: new global flags `--retries` and `--retry-delay` to tune/disable retries.
- Reliability: add unit tests for the retry helper.

## 0.1.65 — 2026-01-29
- Safety: `wake` now requires `--yes` to avoid accidental wake-ups.
- Docs: add the safety-gated `wake --yes` example.

## 0.1.64 — 2026-01-29
- Better UX: `charge status` now shows usable battery + (when charging) power details (kW/V/A) and charge port/cable state.
- Reliability: add unit tests for charging status JSON helper.

## 0.1.63 — 2026-01-29
- Better UX: show "Usable battery" (when available) in `report`, and include `usable_level_percent` in `summary --json`.
- Reliability: add unit tests for usable battery formatting.

## 0.1.62 — 2026-01-29
- Better UX: add `scheduled-departure status` (read-only) for scheduled departure / preconditioning / off-peak charging.
- Reliability: add unit tests for scheduled-departure JSON formatting.

## 0.1.61 — 2026-01-29
- Better UX: `mileage export` now supports time-window filtering via `--since-days` or `--since-ts`.
- Reliability: add unit tests for mileage export filtering helpers.

## 0.1.60 — 2026-01-29
- Better UX: add global `--debug` (or `MY_TESLA_DEBUG=1`) to print full tracebacks on errors.

## 0.1.59 — 2026-01-29
- Better UX / safety: `location` now supports `--digits N` (0–6) to control rounding precision for approximate coordinates.
- Reliability: add unit tests for coordinate rounding helper.

## 0.1.58 — 2026-01-29
- Better UX: `report` now includes scheduled departure / preconditioning / off-peak charging status when the vehicle reports it.

## 0.1.57 — 2026-01-29
- Dev hygiene: ignore common Python tooling caches (e.g., `.pytest_cache/`, `.mypy_cache/`) to keep the repo clean.

## 0.1.56 — 2026-01-29
- Better UX: `summary --json` now outputs a small **sanitized** JSON object (no location) for easy scripting; `--raw-json` is still available when you explicitly want raw `vehicle_data`.
- Reliability: add unit tests for summary JSON sanitization.

## 0.1.55 — 2026-01-29
- Better UX: `report` now includes a compact seat-heater summary line when the vehicle reports seat heater levels.
- JSON: `report --json` includes `climate.seat_heaters` when available.

## 0.1.54 — 2026-01-29
- New capability (safe): add `seats` command for seat heater status + setting levels (set requires `--yes`).

## 0.1.53 — 2026-01-29
- Better UX: `report` now includes a one-line openings summary (doors/trunk/frunk/windows) when the vehicle reports it.

## 0.1.52 — 2026-01-29
- New capability (safe): add `windows status` (read-only) with `--no-wake` + `--json`.

## 0.1.51 — 2026-01-29
- Fix: remove an invalid f-string escape in `list` output so `scripts/tesla.py` compiles cleanly and tests can import it.

## 0.1.50 — 2026-01-29
- Reliability: make `windows` command handler defensive (explicitly errors on unknown actions) and add unit tests.

## 0.1.49 — 2026-01-29
- Fix: repair an indentation bug in `report` output formatting that could break `python3 -m py_compile` / CLI execution.

## 0.1.48 — 2026-01-29
- Security: set best-effort `0600` permissions on local token cache (`~/.tesla_cache.json`) and defaults (`~/.my_tesla.json`).
- Reliability: add unit test for defaults file permission behavior.

## 0.1.47 — 2026-01-29
- Reliability: make `tests/` a package that disables Python bytecode writing, so running tests won’t create `__pycache__/` in the repo.

## 0.1.46 — 2026-01-29
- Fix: `mileage record` now supports `--json` (subcommand flag) so hourly cron runs can log machine-readable output.

## 0.1.45 — 2026-01-29
- New capability: add `mileage` tracking (local SQLite) to record odometer miles across **all cars**.
  - Default behavior: `--no-wake` style (skip sleeping cars)
  - Auto-wake policy: allow waking a car only if it hasn’t recorded mileage in **24 hours**.
  - Includes `init`, `record`, `status`, and `export` commands.
- Docs: added a quick-start + an hourly `launchd` example.
- Tests: added unit tests for mileage DB helpers + record skip behavior.

## 0.1.44 — 2026-01-29
- New capability: add `climate defrost on|off` (max defrost / preconditioning).
- Reliability: add unit tests for the new defrost command wiring.

## 0.1.43 — 2026-01-29
- Reliability: prevent Python from writing `__pycache__/` bytecode when running the CLI (keeps the repo clean).

## 0.1.42 — 2026-01-29
- UX: `report` now includes charging power details (kW / V / A) when the car is actively charging.
- Reliability: add unit test coverage for the new report output.

## 0.1.41 — 2026-01-29
- UX: improve error/help messages by printing a copy/pastable invocation that works outside the repo (uses the script’s absolute path).

## 0.1.40 — 2026-01-29
- New capability (safe): add `charge-port status` (read-only) with `--no-wake` + `--json`.
- Reliability: add unit test coverage for the new charge port status formatter.

## 0.1.39 — 2026-01-29
- UX: add `version` / `--version` so you can quickly confirm the installed skill version.

## 0.1.38 — 2026-01-29
- UX: `list --json` now outputs a privacy-safe, machine-readable vehicle list (no VINs).

## 0.1.37 — 2026-01-29
- Packaging: keep `VERSION.txt` in sync with `VERSION` so installed skills report the correct version.

## 0.1.36 — 2026-01-29
- Reliability: harden test runner to clean stray Python bytecode and fail if `__pycache__` / `*.pyc` are produced.

## 0.1.35 — 2026-01-29
- Docs/privacy: document `MY_TESLA_DEFAULT_CAR` and clarify that `status --json` outputs raw `vehicle_data` (may include location); recommend `report --json` for sanitized output.

## 0.1.34 — 2026-01-29
- UX: make `--car` selection errors clearer when a partial name matches multiple vehicles (shows matches + suggests using an index).

## 0.1.33 — 2026-01-29
- UX: add `climate status` (read-only) with `--no-wake` and `--json` support for a focused climate-only view.

## 0.1.32 — 2026-01-29
- Reliability: add `./scripts/run_tests.sh` and recommend `PYTHONDONTWRITEBYTECODE=1` to prevent repo-local `__pycache__`.

## 0.1.31 — 2026-01-29
- UX: fix `status --summary` to actually include the one-line summary *and* the detailed status output.

## 0.1.30 — 2026-01-29
- New capability (safe): add `openings` command to show which doors/trunks/windows are open (supports `--no-wake` + `--json`).

## 0.1.29 — 2026-01-29
- UX: `report` now includes charge port door + cable status. `report --json` now includes scheduled charging + charge port fields.

## 0.1.28 — 2026-01-29
- Reliability/privacy: add unit test to ensure `report` output never echoes location fields from raw vehicle_data.

## 0.1.27 — 2026-01-29
- UX/privacy: `report --json` now outputs a sanitized report object by default (no location). Use `--raw-json` to get full vehicle_data.

## 0.1.26 — 2026-01-29
- UX: `charge status --json` now prints *only* JSON (subset of `charge_state`) for piping/parsing.

## 0.1.25 — 2026-01-29
- New capability (safe): add `charge amps <N>` to set charging current (requires `--yes`).

## 0.1.24 — 2026-01-29
- Reliability: add unit tests for scheduled-charging time parsing/formatting helpers.

## 0.1.23 — 2026-01-28
- UX: `status --json` now prints *only* JSON (no extra human text), making it safe to pipe/parse.

## 0.1.22 — 2026-01-28
- UX: include TPMS tire pressures in `report` output when available.
- Docs/privacy: remove personal default-car example from README/SKILL.

## 0.1.21 — 2026-01-28
- Reliability/privacy: remove accidentally committed Python bytecode (`__pycache__`) and sanitize unit test fixtures.

## 0.1.20 — 2026-01-28
- Improve UX: `--car` now accepts partial name (substring match) or a 1-based index from `list`.
- Add unit tests for vehicle selection.

## 0.1.19 — 2026-01-28
- Add `tires` command to show TPMS tire pressures (read-only; supports `--no-wake`).

## 0.1.18 — 2026-01-28
- Add `sentry` command (status/on/off) with `--yes` safety gate for toggles.
- Show Sentry state in `report` output + add a unit test for it.

## 0.1.17 — 2026-01-28
- Add unit tests for `--no-wake` behavior (wake gating + exit code).

## 0.1.16 — 2026-01-28
- Add `--no-wake` to read-only commands to avoid waking the vehicle (fails if asleep/offline).

## 0.1.15 — 2026-01-28
- Add `charge-port` command (open/close) with `--yes` safety gate.

## 0.1.14 — 2026-01-28
- Safety: require `--yes` for `unlock` and `charge start|stop` to avoid accidental disruptive actions.

## 0.1.13 — 2026-01-28
- Improve UX: clearer validation + errors for `charge limit` and `climate temp`.

## 0.1.12 — 2026-01-28
- Make `location` safer by default: show approximate (rounded) coordinates unless `--yes` is provided for precise.

## 0.1.11 — 2026-01-28
- Remove `--yes` safety gate from `location` (prints coordinates + maps link without confirmation).

## 0.1.10 — 2026-01-28
- Refactor: centralize missing-email handling into a single helper with a clearer example.
- Clarify --yes help text to include scheduled-charging set|off.

## 0.1.9 — 2026-01-28
- Add `scheduled-charging` command (status/set/off) with safety gate; show scheduled charging info in `report`.

## 0.1.8 — 2026-01-28
- Improve UX: clearer error when Tesla email is missing (instead of confusing auth failures).

## 0.1.7 — 2026-01-28
- Add `windows` command to vent/close windows (safety gated with `--yes`).

## 0.1.6 — 2026-01-28
- Add unit tests for status/report formatting helpers.
- Clarify `--yes` help text to cover all safety-gated commands.

## 0.1.5 — 2026-01-28
- Include `VERSION.txt` in published skill artifacts (ClawdHub ignores extensionless files like `VERSION`).

## 0.1.4 — 2026-01-28
- Add `trunk` command (trunk/frunk) with safety gate (`--yes`).
- Make `location` safety gated (`--yes`) to reduce accidental sensitive output.

## 0.1.3 — 2026-01-28
- Add `report` command: a one-screen, chat-friendly status report.
- Fix `climate temp` units: default is °F, with `--celsius` for °C.

## 0.1.2 — 2026-01-28
- Add `default-car` command and local defaults file (`~/.my_tesla.json`) so you can set a default vehicle.
- Reduce sensitive output: stop printing VINs in `auth`/`list` by default.

## 0.1.1 — 2026-01-28
- Add `summary` command for a one-line, chat-friendly status output.

## 0.1.0 — 2026-01-28
- Forked from the base `tesla` skill and enhanced into `my-tesla`.
- Added safety confirmation gate for disruptive actions.
- Added `charge limit` command.
- Added author attribution + versioning for publishing.
