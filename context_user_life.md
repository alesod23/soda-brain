---
name: User Life Context (running notes)
description: Living document of Alessandro's commitments, projects, recurring activities, and personal rules. Append here whenever new life context emerges. Used to deprioritize / contextualize triage items and other agent decisions.
type: user
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
# Life context

This is a **living document** — append, never overwrite. Update it whenever Alessandro shares anything about his life, work, projects, deadlines, people, or commitments. Future agents read this to understand the context behind his requests.

User has explicitly asked for this file to grow over time. He plans to send a first proper context dump soon; integrate it into the sections below when it arrives.

## Affiliations / accounts

- **CDTM (Munich)** — primary affiliation. Email: `alessandro.sodano@cdtm.com`.
- **lobbly.tech** — personal/side project. Email: `alessandro@lobbly.tech`.
- **HEC Paris** — additional affiliation (presumably via exchange / parallel program). Email: `alessandro.sodano@hec.edu`. NOT currently in the triage helper (no token, no labels). Some HEC outgoing mail auto-delivers into the lobbly inbox (BCC or forwarding rule), which can produce false-positive "actionable" classifications when the snippet looks like an outgoing email body. Always check `From:` header.

## Taskforces & projects

- **CDTM Onboarding TF** — DEPRIORITIZED for daily triage. Most events cluster in a 2-week intense period in late August. Subject keywords that trigger this rule: `Kickoff`, `Pre-Kickoff`, `Class Photo`, `Navigating Life`, `Onboarding TF Sync`, `Tour Fall`. When these appear in inbox, **skip silently, no label**. They get re-evaluated each triage run and may auto-promote to `triage/action` if/when within 7 days.

## Triage rules

- **Actionable definition (updated 2026-05-18):** an item is actionable if ANY of:
  1. It would affect what Alessandro does next (changes plans, requires action, surfaces info he'd want for an upcoming commitment), even if not directly addressed to him.
  2. It mentions a deadline that regards him.
  3. It's a project update for one of his priority projects.
- **Priority projects (always-flag — surface every new msg, any channel):**
  - **BMW / MPD BMW** (WA `MPD BMW - ALERTS` group + Slack `#26-1_mpd_bmw_only-us` + any thread)
  - **Lobbly** (any thread, any account, anywhere)
  - **CDTM Onboarding Taskforce (TF)** — note: this OVERRIDES the prior late-August deprioritization. The TF is now a priority. (Old subject-skip rule for `Kickoff`/`Pre-Kickoff`/etc. is RETIRED.)
  - **xplore** (Slack workspace + any project work)
  - **Thesis**
- **Time window: any real commitment, however far out.** Previous 7-day cap is REMOVED. A booking decision for June, a deadline in 3 weeks, a confirmed event in 2 months all count if they require action from him. Still respect the 24h fetch ceiling (see `feedback_triage_24h_cap`); the question is whether to ACT on the item, not when it lands in the inbox.
- **Always-skip categories** (silently, never display):
  - Reactions, emojis, single-word closures ("ok", "thanks", "noted")
  - Newsletters, automated digests, calendar acks
  - Community-broad asks (jobs, events, surveys not directed at him)
  - Group banter, sports banter, past-tense / moot questions, threads where he was the last sender
  - **BUT:** before skipping a reaction/closure/banter as the latest msg, ALWAYS check the burst (last N msgs in the chat) — if there's an earlier actionable msg the user hasn't acted on, surface that one instead. The classifier looks at the burst, not just the latest line.
- `triage/todo` is reserved for items the USER explicitly postponed via "N todo". These carry forward to every subsequent debrief until marked done — they're the persistent "things I committed to do later" list.

## Per-contact / per-group triage rules (WhatsApp)

- **Renata Arlaud (grandma)** — sends images frequently (newspaper clippings, photos). Image-only messages from Renata are normal background noise → **skip silently** in triage. Surface only if she sends actual text asking for something.
- **MPD BMW - ALERTS group** (`120363408044433629@g.us`) — ALWAYS surface in triage, treat every incoming message as actionable. This is his BMW project group and signals there are high-priority. (Apply standard past-tense check still: if a message references a clearly-passed time today, classifier can drop.)
- **DMs with explicit questions to him** — ALWAYS actionable when not yet replied (`repliedSinceLastIncoming: false`). Don't second-guess by content classification when it's clearly a question directed at him.
- **Muted groups** (auto-filtered by `wa-daemon/wa-groups-block.json`, never appear in triage):
  - MMT 25/26 (`120363420239747940@g.us`)
  - Erasmus Italiani a Parigi-LVP (`120363045848737915@g.us`)
  - Bâtiment B (`33658006127-1568484734@g.us`)
  - Patti (`120363331508133404@g.us`)
  - Sons of Terry (`16087511054-1546811026@g.us`)
  - FRIENDS (`120363420552972797@g.us`)
  - Basketball thursday (`120363418162804201@g.us`)
  - Sodano's newspapers (`120363185312174779@g.us`)
  - Add more via `node wa-daemon/wa-mute.js add <jid-or-name>` whenever a group consistently produces noise. User explicitly cited "cheaper compute" as a reason — mutes filter at the daemon layer, before LLM classification, so they're free.

## Family & Catholic network (identity-level, stated 2026-07-21)

- **Alessandro is the grand-nephew of Cardinal Angelo Sodano** (Vatican Secretary of State under John Paul II). His father is Angelo Sodano's nephew (Angelo was the brother of Alessandro's grandfather). Deep Catholic-world connections run through the family.
- **Alessandro's own Catholic credentials:** ICLN (Catholic legislators' fellowship, meets yearly in Fatima; introduced by John Klink); Order of Malta (went to Lourdes 2026, met the Grand Master); Università Cattolica Milan (BSc Economics, thesis on Giuseppe Toniolo; lived at Collegio Augustinianum).
- **John Klink** — very close friend of Alessandro & his father; ex-Holy See UN delegation; the key network connector.
- **Father's background:** worked for **Daedalus** (Italian software co.), attempted US expansion ~2018–22 via Catholic connections — now reactivating that network for **US hospital intros for Tundra** (3 channels: Ascension via an old-president contact; Cardinal/Abp Broglio; a "UP" group).
- Full detail: `vault_kb/Raw/07-21 Catholic background, family, and network.md` (personal) + `medtech-brain/Raw/07-21 Father's Catholic healthcare network...md` (the healthcare channels).

## Pending context

- Awaiting Alessandro's first proper life-context message (he flagged it on 2026-05-07). When it arrives, distribute the info across the sections above; don't dump it raw.
