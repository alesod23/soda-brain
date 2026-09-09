---
name: feedback_gtm_boards_open_via_script
description: "GTM boards must be opened with ~/gtm-eng/open-board.ps1, never with a browser-automation navigate, or they land in the wrong Chrome tab group"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67360653-a4fa-4a49-9fe9-75fbdcbb9319
  modified: 2026-09-09T17:16:22.442Z
---

Open a GTM board with `powershell ~/gtm-eng/open-board.ps1 <slug>`. Never with the Claude-in-Chrome
`navigate` tool, Playwright, or a bare `Start-Process`. Same for the board index (no slug argument).

**Why:** he reviews boards in a Chrome tab group named **GTM**. Chrome exposes tab groups only to an
extension holding the `tabGroups` permission — no CDP route, no command line, and the Claude-in-Chrome
MCP files its tabs into its own MCP group instead. So a board opened with `navigate` is genuinely open
in his Chrome and looks fine from my side, while he is staring at a GTM group that does not contain it.
He caught this on 2026-09-09 with the ache-sd board: "i dont see it open in my gtm tab group".

The second cause found the same day: **the GTM Tabs extension had never been loaded in any Chrome
profile** (checked all four: Default, Profile, Profile 1, Profile 2). `tabs-queue.json` had been
accumulating unclaimed URLs since 2026-09-07 because nothing was polling `/api/tabs/pending`, which
drains it. So even the correct script would not have grouped anything. `open-board.ps1` now checks the
queue before writing to it and prints a loud banner when it is non-empty, since a non-empty queue can
only mean nothing is polling.

**How to apply:** run the script. If it prints "THE GTM TABS EXTENSION IS NOT RUNNING", say so plainly
and give him the one-time manual fix (`chrome://extensions` -> Developer mode -> Load unpacked ->
`C:\Users\Alessandro\browser-extensions\gtm-tabs`); a script cannot install an unpacked extension, and
the file picker cannot be automated. Never silently accept an ungrouped tab as done. If a board is
already open in an MCP tab, close that tab after running the script so he does not get two copies.

Related: [[feedback_browser_chrome_default]], [[reference_gtm_boards]], [[feedback_diagnose_before_naming_root_cause]].
