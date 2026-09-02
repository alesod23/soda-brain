---
name: daily-briefing
description: "/daily morning briefing — Wilkins routine; auto-run RE-ADDED 2026-06-15 as lightweight SessionStart hook + guarded 4am task (replaces the deleted 08:00 headless auto-run)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a70c6040-04ee-4dc3-9739-dc93453ce49d
---

Built 2026-05-22 as a Wilkins-style upgrade to the original 5-step /daily skill.

## Hard rule — daily page is the source of truth
User only edits the daily page (`task-land/Daily/YYYY-MM-DD.md`). The Today section of the most recent daily note IS the authoritative active-task list. `Tasks/active/` and `Tasks/inbox/` folders are downstream views that `/daily` reconciles on every run.

## Skill location
`C:\Users\Alessandro\.claude\commands\daily\SKILL.md` — full 11-step spec.

## Trigger paths (auto-run RE-ADDED 2026-06-15, new lightweight design)
- **Manual:** user types `/daily` — always works.
- **Triggered:** `/dump` auto-runs `/daily` at the end so dumped items show up immediately.
- **SessionStart hook (live, no headless claude):** on every Claude Code launch, `~/.claude/hooks/session-start.ps1` (registered under `hooks.SessionStart` in `~/.claude/settings.json`) does two cheap things — (1) relaunches the tg-bridge bot idempotently via `tg-bridge/start.ps1` ("bot live each time CC starts"), (2) if `task-land/Daily/<today-local>.md` is missing, emits `hookSpecificOutput.additionalContext` nudging the live session to run `/daily`. Runs INSIDE the interactive session, so prompts work — NO bypass, NO headless spawn.
- **Guarded 4am task (headless, opt-in, user-registered):** `Daily-Morning-Briefing` scheduled task at 04:00 local → `~/.claude/daily-briefing/check-and-run.ps1`, which date-guards: only when today's page is missing does it spawn `claude -p "/daily" --permission-mode bypassPermissions`. **No wake-up** (`WakeToRun=$false`), **no catch-up** (`StartWhenAvailable=$false`) — asleep at 4am ⇒ skipped, SessionStart covers it. Runs on battery.

## Why the 2026-06-15 redesign differs from the deleted 2026-06-07 auto-run
The OLD auto-run was killed because it fired a heavy headless `claude.exe -p` on EVERY startup/resume (3 triggers, 3× retry) for zero benefit. The NEW design fixes exactly that: the per-launch path (SessionStart) is lightweight and runs in-session (never headless); the headless path fires at most ONCE/day and ONLY when the page is genuinely missing (the date-guard in check-and-run.ps1). On 2026-06-15 the user explicitly asked to bring it back this way ("run it if the laptop is already awake, don't wake it").

**Bypass/registration caveat:** the 4am task launches an unattended approval-disabled agent (`bypassPermissions`, needed so it doesn't hang on PowerShell/Calendar-MCP prompts with nobody present). The auto-mode classifier correctly refuses to let Claude register that — so registration is staged for the USER to run knowingly: `~/.claude/daily-briefing/register-task.ps1` (one-liner copied to clipboard). Until the user runs it, `Daily-Morning-Briefing` does NOT exist and only the SessionStart path is active. The old `Slot-Check-<date>` task stays gone (slot events still created inline in step 8e). **SKILL.md step 0 still says "manual-only / no scheduler" and is now STALE — update it if the user keeps this setup.**

## Broader checkbox sync (rules in step 2 of the SKILL)
Edits on the daily page propagate back to task files:
- `[x]` → status: done, archive
- `~~[[slug|...]]~~` strikethrough → status: cancelled, archive
- Line moved between Today/Inbox sections → file moves between `Tasks/active/` and `Tasks/inbox/`
- `📅 YYYY-MM-DD` appended → write `due:` frontmatter
- `⏳ YYYY-MM-DD` → write `defer:` (hides until that date)
- Indented bullets under a task → appended to task body with date prefix
- Alias text changed → write back to `title:` frontmatter
- Line deleted entirely → **parked in `Tasks/waiting/` + flagged once in the brief** (changed 2026-06-05; was previously a no-op). Never silently re-surfaced to Today, never archived. Hard-cancel still needs `[x]`/strike. See [[feedback_daily_deletion_parks_to_waiting]].
- **Plain-text bullet (non-wikilink, non-habit) typed directly on the page → CAPTURE into a task file** (active/inbox/waiting by section), parse trailing `(project)`. Added 2026-05-26 after a hand-typed "Cold call Fraunhofer" Today line was nearly lost.

## Section order (2026-05-26)
Render order is **Today → Inbox → Habits → Next 7 days → Waiting**. `## Waiting` is ALWAYS last (user moved it to the bottom 2026-05-26); it never auto-surfaces and carries no urgency markers.

## Context inputs (read each morning before ordering)
- `task-land/context.md` — user-maintained: Mode block, active projects, prioritisation rules, habits, soft routines
- `task-land/agent-notes.md` — agent-maintained: behavioural patterns, day-of-week shape, recurring slips, streaks/wins

The agent reasons about Today's order using both files (replaces the old fixed lobbly→thesis→tools rule).

## Carry-forward
Unticked tasks simply stay in their folder and reappear next run. **The `rolled_over` mechanic was REMOVED 2026-05-25** (no ⚠ prefix, no rank boost from staleness). The ONLY thing that promotes a task onto Today is a `surface_on`/`due` date reaching today. See [[feedback_daily_waiting_and_no_rollover]].

## Habits
5 daily-streak habits at `task-land/Habits/`: german-learning, 20-min-nothingness, workout, reading, guitar. Schema: streak / longest_streak / last_done / log. /daily reads yesterday's [x]'s and updates streaks.

### Slot-picker habits + /slot-check
`20-min-nothingness` has `duration: 20`, `buffer_before: 15`, `buffer_after: 15`, `prefer: afternoon-evening`, `bump_at: 10`, `bump_to: 30`. /daily proposes 3 free slots each manual run (queries MCP Google Calendar across active calendars), lists them as sub-bullets on the daily page, auto-commits the recommended one, and creates its calendar event **inline** via MCP (step 8e). Idempotent via `task-land/_system/slot-state.json`. **No scheduled `Slot-Check-<date>` task anymore** (removed 2026-06-07 with the auto-run); a later manual `/daily` or `/slot-check` reconciles a changed/late tick. **Streak hit 10 on 2026-06-06 → bump fired: duration now 30 min** (title rerenders to "30-min nothingness", slot window 60).

## Compaction
Daily notes older than the first of the current month → `Daily/YYYY/MM/`. Current-month notes stay flat.

## Weather
`curl -s "https://wttr.in/Munich?format=%l:+%C+%t+(feels+%f),+sunset+%s" --max-time 5`. Rendered as blockquote under the H1 title. Silent skip on failure.

## Why
Original /daily was a 5-step rebuild-from-folders. Wilkins approach (per his blog) flips the model: daily page is canonical, folders are downstream, agent reasons about prioritisation using context+notes files. Better fit for execution sprints (current Lobbly push until mid-June 2026) since priority changes with Mode.
