# Handoff (box -> laptop DA SYSTEM): permanent "hub cards still open (N)" line on the daily page

His words (Telegram 19 Sept 00:35, replying to the 23:00 hub digest): "similar to the crm way in which we have on our to do a permanent field, i want one that reminds me there how many cards still open there are."

What exists: `Render-Bucket` in `task-land/_system/daily-lib.ps1` already renders one fixed, non-task line under `## Today`: `- [ ] Today's items in the CRM (n) [open](http://127.0.0.1:4124/#today)` (see task-land/CLAUDE.md, "Daily-page line"); `Parse-Section` skips it via `$script:CrmLineRe`.

To build (laptop side, same family):
1. A second fixed line right under the CRM line: `- [ ] Hub cards still open (N) [review](http://100.85.52.84:4142/)`. N comes from the box: `GET http://100.85.52.84:4142/api/open-count` -> `{"open": N, "by_type": {...}}` (hub-review server on the box, Tailscale only; being built tonight, endpoint contract fixed). Timeout 2 s; on failure render `(offline)` like the CRM line does.
2. Auto-checked when N = 0. Never a task: add its regex to the skip list next to `$script:CrmLineRe` so ticking or deleting it does nothing.
3. Link target = the phone review page (Tailscale). On the laptop the same URL works when Tailscale is up.
4. Log the change in task-land/CLAUDE.md under the daily-page line section and in the memory reference_hub_review_ui (box writes it).
