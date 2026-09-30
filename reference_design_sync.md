---
name: reference_design_sync
description: "Claude Design <-> GitHub sync with Caleb (built 2026-09-28/30) - Chrome extension mirror, local server :4190, /design-sync EOD 3-way merge, onboarding via sync/setup.py; the gotchas that bit."
metadata:
  node_type: memory
  type: reference
  originSessionId: 8394f77f-8970-44ae-939f-8c1a6508b8b3
  modified: 2026-09-29T23:34:44.455Z
---

System lives in `~/tundra-design/sync/` (repo alesod23/tundra-design, Caleb = CodeCLS collaborator). Canonical docs: `sync/README.md` (EOD + sharing), `sync/ONBOARDING.md` (new teammate), skill `sync/skill/SKILL.md` installed to `~/.claude/skills/design-sync/` by `python sync/setup.py --person <name>`.

- Mirror = Design Mirror Chrome extension (his everyday Chrome, load unpacked `sync/extension`) -> `dsync.py serve` on 127.0.0.1:4190 (task `DesignMirror-Server`, pythonw, `--log sync/mirror.log`) -> commits `live/<person>/<key>/`. Headless Playwright is blocked by Cloudflare: never retry that path.
- Pushes into Claude Design only via DesignSync (`/design-login` needed); probing Claude Design's internal write API was classifier-denied: don't.
- Claude Design injects `data-omelette-injected` style+script into every file read through its API; a copy made inside Claude Design can bake it in (UPMC pitch had it twice). `dsync.clean()` strips it; never push unstripped mirror content.
- He loaded the extension in ~3 Chrome profiles (triple log lines): server answers 429 to concurrent snapshots instead of queueing.
- Git on this laptop can stall for an hour (task-land push 2026-09-30 00:17); all dsync git calls have a 120 s timeout and GIT_TERMINAL_PROMPT=0.
- His Tundra Pitch Deck project = f56e8ca4; Caleb's decks were stacked into its `caleb/` folder on 2026-09-28 as a one-off copy (not live). Humanitas deck: `Humanitas pitch.dc.html`, generator in the session scratchpad; he edits it in the web UI too, so always rebase on the mirror before pushing.

Related: [[reference_design_lib]], [[feedback_designsync_pull_before_write]], [[reference_window_watch]].
