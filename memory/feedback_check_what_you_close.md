---
name: feedback_check_what_you_close
description: "Before stopping a process or closing anything automatically, record what it IS (session name, command line, owner) and report it; never stop an interactive session blind"
metadata:
  type: feedback
since: 2026-10-10
---

**His words (10 Oct 2026):** "how about we learn to check what we close next time?" after the budget guard stopped two
claude processes (pids 1056, 11900) at the 47% cap and nobody could say afterwards which sessions they were.

**Why:** a stop or close that leaves no identity is unauditable; it may have been one of his own working sessions.

**How to apply:** anything I build that stops or closes things (guards, janitors, clean slates) first captures the
identity (for claude: the `--resume "<name>"` session, the command line, the parent chain), logs it, and tells him the
same tick (one hub card naming each item). An interactive session he may be typing in is reported, not stopped. Applied
in ~/sim/harness/budget_guard.py (identity(), spared interactive sessions, the card). Related: [[reference_window_watch]].
