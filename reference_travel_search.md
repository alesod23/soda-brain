---
name: travel-search Helper + /trippy Skill
description: Local helper at ~/.claude/travel-search/ driving a persistent Chromium profile across Momondo, Skiplagged, Omio, SNCF, Volotea. Wrapped by /trippy skill (~/.claude/skills/trippy/SKILL.md) for natural-language travel search. Same helper-script pattern as wa-daemon / triage-gmail.
type: reference
originSessionId: 84aa499d-8948-409c-abe0-8b0719b7270d
modified: 2026-08-02T23:46:33.479Z
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

Local helper at `C:\Users\Alessandro\.claude\travel-search\` that drives a single persistent Chromium profile across travel sites. User logs in / clears captchas / accepts cookies once per site via `prime.py`; from then on `search.py` reuses the same authenticated session for hours/days.

## Browser lifecycle — persistence is DELIBERATE, reaping is the missing half (2026-08-02)

Site drivers (`paris_rail.py`, `trn_termoli_check.py`, v2's `profile-checkout`) launch
Chrome/Comet **detached** on a fixed CDP port via `subprocess.Popen`, then `connect_over_cdp`.
Playwright never owns the browser, so `with sync_playwright()` tears down only the driver.
Both scripts document this in their docstrings ("NEVER closed", "so state survives between
invocations") — it is **intentional**, protecting SNCF/Trenitalia/lefrecce login state.
**Do NOT "fix" it by adding `atexit`/`finally` teardown to `attach_or_launch()`/`boot_chrome()`** —
that forces a re-login on every subcommand and destroys the design.

The actual defect was that nothing reaped them once a session ended: on 2026-08-02 three trees
(`profile-comet`, `profile-rail-chrome`, `profile-wA` — 37 procs, 1.1 GB) had run **30 h** with
every parent process dead. Fix = `travel-search\reap.py`, age-based (6 h default) so a live run
survives, plus explicit `close` subcommands on both scripts. Preflight is now mandatory in both
`/trippy` and `/trippy-v2` SKILL.md.

`reap.py` guards, both load-bearing: it matches **only real browser executables** AND only those
whose `--user-data-dir` resolves under `travel-search\`. The first guard was learned the hard way —
matching on command-line text alone also matched the launching PowerShell and killed it mid-run.
The user's daily-driver Comet uses the default profile and can never match.

## /trippy skill (the recommended entrypoint)

Skill at `C:\Users\Alessandro\.claude\skills\trippy\SKILL.md` is the natural-language wrapper. User says e.g. "munich to termoli on may 29 by 9pm" or "/trippy ..." and the skill instructs Claude to: parse fields, map city names to nearby IATA codes via world knowledge (NOT a hardcoded list — the skill IS the geography engine), pick adapters, run `search.py` in background, read JSON, present top picks. Keep chat output to one screen.

## Files

- `prime.py <site>` — opens persistent profile, polls for `state/SIGNAL_<site>.txt`, exits cleanly when file appears (cookies persist).
- `search.py` — orchestrator. Args: `--from --to (CSV of IATA codes) --date --arrive-before --depart-after --sites`. Writes `reports/trip-<ts>.{json,md}`.
- `lib.py` — `launch_profile()` (Playwright persistent context at `profile/`), `write_report()`. Includes a small `CITY_TO_AIRPORTS` dict as a CLI fallback (the skill bypasses this).
- `debug_extract.py` — content-based card extractor for iterating on parsers (writes JSON of all elements with price + 2+ times).
- `sites/base.py` — `SiteAdapter` ABC + `TripQuery` + `TripResult` dataclasses (with `category` field).
- `sites/{momondo,skiplagged,omio,sncf,volotea}.py` — per-site adapters.

## Adapter status (as of 2026-05-08)

- **momondo** — working. Selector `.Fxw9-result-item-container > .nrc6.nrc6-mod-pres-default`. Skips bus offers ("Viaggio in autobus"). Aggressive Akamai — re-prime if results empty.
- **skiplagged** — working. Selector `div.trip` with `trip__stops-N` qualifier for stop count. Locale-primed prices in EUR.
- **omio** — partial. SPA form-driving fragile (date input doesn't always set, autocomplete dropdown timing issues). Skip unless user asks for it.
- **sncf** — stub.
- **volotea** — stub.

## User accounts noted in adapters

- SNCF: `alesoda2002@gmail.com` (Carte Avantage Jeune discount).
- Volotea: Facebook login (Megavolotea yearly sub).

## How to apply

When user asks for travel/flight searches, prefer the /trippy skill flow. The skill handles geography reasoning (Asti → TRN/MIL/BGY/GOA, Termoli → PSR/BRI/NAP/FCO, etc.). Re-prime any site whose results come back empty across all destinations (cookies likely expired).

## Why this exists

User picked the "log-in-once, agent roams" pattern (2026-05-07 session) over paid bypass services (Browserbase / 2Captcha) so account-specific discounts (SNCF Carte, Volotea sub) work and no API key cost. /trippy skill (2026-05-08) wraps it in natural language so the user describes trips instead of constructing CLI args.
