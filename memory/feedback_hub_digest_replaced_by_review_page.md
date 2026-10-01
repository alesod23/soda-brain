---
name: feedback_hub_digest_replaced_by_review_page
description: "Ruling 2026-09-19 00:35: the 23:00 hub digest ('N cards still open, answer each with its number') is unusable on the phone. He wants a Tailscale web page (hub-review, port 4142) where each open card gets yes/no/skip/free-text change, keyboard a/s/x/c + j/k, one Commit; free text per card and a global 'system-wide feedback' box are commands to the savior; plus a permanent 'hub cards still open (N)' line on the daily page like the CRM line."
metadata:
  type: feedback
---

**His words:** *"do you even see what this message is like? how can i approve them like this?? id like to instead have a web server (connected with tailscale so i can do it on my phone) with a much more intuitive UI to approve each thing ... free-text prompting/modifications for each one ... text shortcuts to move fast ... disregard/skip ... still a commit button ... the text boxes should allow me to also make system wide changes ... a permanent field that reminds me how many cards still open there are."*

**Why:** the digest lists 19 ids and asks for "N yes" replies; on a phone that is unreadable and error-prone. The GTM boards (keyboard-driven review + one Commit) are the pattern he wants everywhere ([[feedback_review_pages_need_keyboard_shortcuts]], [[feedback_commit_batch_is_the_yes]]).

**How to apply:**
1. Nightly digest = one line with the link to `http://100.85.52.84:4142/`, not a list to answer by number.
2. On Commit: yes/no resolve in the hub (drafts: yes = dsend by the hub). Free-text "change" per card and the global box arrive to the savior as HIS Telegram message ("hub-review commit ...") and are executed like `N change:` / a new rule; a system-wide note that states a rule is saved as a memory the same turn ([[feedback_rule_requests_are_binding]]).
3. Daily page: fixed line `Hub cards still open (N)` from `GET :4142/api/open-count`, laptop renders it (handoff `task-land/_system/HANDOFF-20260919-daily-page-open-hub-cards-line.md`).
4. Iterate with him on the page; he said "build it, notify me when done and we iterate".

Related: [[reference_hub_review_ui]], [[reference_approval_hub]], [[reference_gtm_boards]].
