---
name: triage-askquestion-and-24h
description: "/triage must end with AskUserQuestion chips (locked 2026-05-18) AND post-filter every item against effective_cutoff = max(last_check, now-24h). Both were missed on 2026-05-21."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5a8aa945-389e-497f-8164-c89bd704ff38
---

Two `/triage` round failures on 2026-05-21 — surgical fixes shipped same day to the skill + a new consolidated wrapper.

**1. AskUserQuestion default was bypassed.** The skill's recipe step 6 says "Default UI is AskUserQuestion (locked-in 2026-05-18)" — Alessandro wants the per-item chips with Done / Todo / Suggested-reply / Other for every item. But Hard Rule #1 in the same skill file said `**NO AskUserQuestion.** Compact list + one freeform batch reply.` (stale from before the lock-in). I read Rule #1 first and printed only the freeform "Actions? ..." prompt. **Fix:** Hard Rule #1 inverted to `**ALWAYS end with AskUserQuestion (locked-in 2026-05-18, re-enforced 2026-05-21).**` with explicit "if you're about to type 'Actions?' and stop, STOP — you missed this rule".

**Why:** Alessandro picks faster from chips than from typing comma-separated verbs, and the pre-composed reply in option 3 is what he actually wants 80% of the time.

**How to apply:** Always call AskUserQuestion immediately after printing the actionable list (step 5). One question per item, max 4 per call (batch + re-prompt if N>4). The visible "Actions?" line in the list is a caption ABOVE the chips, not a substitute. Only exception: N=0 ("Inbox clear ✓") just returns.

**The exact 4 options (pin this — do NOT reinvent):** (1) Done, (2) Todo, (3) "Send my suggested reply" = a PRE-COMPOSED 1-2 sentence draft in the option's `description`, (4) the auto "Other" free-text slot where the user types their own reply / `suggest` / `skip` / `mute`. `mute` is a freeform verb under Other, NEVER a dedicated 4th chip. (2026-05-25: when I rewrote the skill from scratch for the public `terminal-inbox` package I fabricated a "Mute" 4th option instead of copying these semantics — Alessandro caught it. Lesson: when packaging/rewriting a skill, transcribe the option semantics from the source skill + this memory; don't invent.)

**2. 24h ceiling was a fetch-scope rule, not a post-filter — old items leaked through.** Rule 7 says "Effective cutoff = `max(last_check_at, now - 24h)`. Only surface items whose latest incoming timestamp is >= effective cutoff." I used the cutoff in the Gmail `after:N` search but didn't post-filter. Gmail's `after:` filters by thread `internalDate` (the latest msg in the thread, including SENT msgs and label-change bumps), so a thread bumped within the window can still have its latest INCOMING older than the cutoff. A Prof Kolisch reply from 2026-05-18 14:38 (>2 days old) was surfaced on 2026-05-21 because the thread popped in `is:unread after:1779289165`. **Fix:** Rule 7 now reads "PER-ITEM POST-FILTER, NOT JUST FETCH SCOPE" with the Kolisch incident named. Step 2 mandates the post-filter for ALL channels (WA, Gmail, Slack) before classification. Carryover (`triage/todo`, `wa-state.json#todo`) is the sole exception.

**Why:** Multiple "old chat re-surfacing" bugs (3-day-old WA after daemon flap, Kolisch reply 3 days old). The 24h ceiling is what bounds noise — if it leaks, signal/noise collapses.

**How to apply:** After every fetch, before classifying, compute `effective_cutoff_unix = max(last_check_unix, now - 86400)` and drop any item where the latest INCOMING timestamp is `< effective_cutoff_unix`. For Gmail this requires per-thread `gmail.cmd get` to find the latest non-SENT `internalDate` — the wrapper does this automatically.

**3. Consolidated `fetch-all.js` wrapper now exists.** Replaces ~15 shell calls per round with ONE. Lives at `C:\Users\Alessandro\triage\fetch-all.js` (+ `.cmd` shim). Reads all 3 state files, dispatches 7 fetches in parallel (Gmail Query A + B × cdtm + lobbly + WA debrief + WA flap + Slack cdtm + xplore), auto-enriches with per-thread `gmail.cmd get` and per-group `show-thread.js`, applies the 24h post-filter inline. Returns one JSON bundle. ~90s wallclock end-to-end. SKILL step 1+2 collapsed to "run the wrapper, read the bundle." Old per-helper commands moved to "Manual fallback (legacy)" appendix.

See [[reference_triage_operations]] for canonical display/state rules. Related: [[reference_triage_aliases_and_state]] (state files), [[feedback_triage_24h_cap]] (the original 24h cap rule, now superseded by the per-item post-filter language).
