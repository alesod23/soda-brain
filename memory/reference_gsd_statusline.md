---
name: reference_gsd_statusline
description: "Context-window bar in the Claude Code statusline — vendored GSD hooks in ~/.claude/gsd-statusline/, wrapper merges the SNM inbox segment."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4c7dee00-4d73-4594-a62e-6b10986085b6
  modified: 2026-07-29T02:00:13.576Z
---

Statusline shows a Codex-style context meter. Layout:
`Opus 5 │ <dir> [█████░░░░░] 50% │ 3 actionable | 1 urgent`

Lives in `C:\Users\Alessandro\.claude\gsd-statusline\`:
- `statusline.js` — the wrapper registered as `statusLine` in settings.json (`node .../statusline.js`). Spawns the two segment producers **concurrently** and joins them with ` │ `. Fails silent on every path.
- `hooks/gsd-statusline.js` + `gsd-core/bin/lib/{semver-compare,package-identity,state-document}.cjs` — vendored from the `@opengsd/gsd-core` npm **tarball**, v1.8.0 (see `VERSION`). Four files, zero external deps.
- `hooks/gsd-context-monitor.js` — registered as a catch-all `PostToolUse` hook; reads the bridge file the statusline writes to `%TEMP%\claude-ctx-<session>.json` and injects a warning at <=35% remaining, critical at <=25%.

Gotchas worth remembering:
- The lib `.cjs` files are **build artifacts** — they are NOT in the GitHub repo (`open-gsd/gsd-core`, compiled from `src/*.cts`). Update via `npm pack @opengsd/gsd-core@latest` and re-copy, never by pulling from GitHub.
- Bare `node` on PATH works here; do NOT apply the full-path rule that governs python ([[feedback_python_full_path]]).
- The SNM segment costs ~0.89s (PowerShell 5.1 startup), the GSD segment ~0.56s. They run in parallel so total ≈ 0.9s — same as the pre-existing SNM-only statusline, no regression. Do not "optimize" by reimplementing `snm-receiver\statusline.ps1` logic in node; that duplicates the focus-mode/staleness rules. See [[reference_snm_receiver]].
- Only the statusline was taken from GSD. The full framework (~40 `/gsd-*` commands, 13 guard hooks, spec-driven STATE.md workflow) was deliberately NOT installed — it would have collided with the existing 15 hooks.
- Backup of the pre-change settings: `~/.claude/settings.json.bak-pre-gsd-statusline`.
