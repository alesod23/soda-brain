---
name: reference_crm_catchup_board
description: "The CRM check board: http://100.85.52.84:4143/crm-catchup.html (box, research-page/build_crm_catchup.py + crm_catchup_data.py, savior-owned). Person items from real conversations, plus one item per hospital he seems to target (data/hospitals.json, built on the laptop), verdicts a/s/c, commit = one Telegram message the savior executes; s asks why."
metadata:
  type: reference
---

**What it is.** The page he calls the "CRM check board": http://100.85.52.84:4143/crm-catchup.html (Tailscale), served by a plain `python3 -m http.server 4143` from `/home/da/research-page/` on the box. Built by `research-page/build_crm_catchup.py` from the hand-written `crm_catchup_data.py` (ITEMS: one per open thread with a person, urgency 1-3, evidence, proposed step, draft). The savior owns the person items.

**Hospital check (added 2026-09-20 by the CRM session, his ruling: "integra nella crm check board questo check per ospedale").** After the person items, a divider and one item per hospital / ASL / CHU he appears to target, read from `/home/da/research-page/data/hospitals.json`. That file is built on the laptop from four sources: coattio `crm.json` companies+people, `~/gtm-eng/boards/*/board.json`, task-land, and his sent mail (gmail.py on the box, 180 days). Gaps are computed per hospital: `no_people`, `no_email`, `no_attempt`, `stale_90d`, `no_next_step`. Verdicts mean: a = yes I target it, s = no, drop it (asks why), c = something is missing (note). The last item, `hosp:missing`, asks which hospitals he researched that the list does not show; those names are the lead for a search in his mail and chats. Commit lines for hospitals are prefixed `hosp:`.

**Keys.** j/k move, a/s/c decide, e draft, n note, ? hide the bar. s opens the why box (Enter = skip, text+Enter = skip with reason, Esc = cancel). Verdicts in localStorage `crm-catchup-v1`; the Commit button prints the one message he pastes to Telegram; the savior executes it.

**Rebuild.** `ssh box "cd ~/research-page && python3 build_crm_catchup.py"`; the http.server needs no restart. Check with a 1568x773 screenshot that the current item fits between header and key bar (design system [[feedback_review_page_design_system]]).

Related: [[project_coattio_v2]], [[feedback_found_contact_details_go_to_crm]], [[reference_hub_review_ui]].
