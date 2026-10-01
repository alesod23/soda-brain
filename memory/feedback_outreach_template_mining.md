---
name: feedback-outreach-template-mining
description: "Outreach templates = cluster the user's already-sent LinkedIn messages into template kinds; do NOT learn-to-write-like-him."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

For the Tundra Health outreach work ([[project_outreach_crm]]), the user does NOT want me to imitate his writing style. Instead: collect ALL the messages he has actually sent (bot sends are logged in `~/.claude/linkedin-accept-bot/pending.json` + the CRM; manual sends pulled via the LinkedIn MCP `get_inbox` / `get_conversation` — the first outbound opener of each thread) and **semantically cluster them into distinct templates**.

Tag each cluster on intent dimensions: ask (call-now / call-later / just-learn), angle (expert-opinion / curiosity / direct / traction), pilot-mention (yes/no), audience (hospital director vs ICP-buyer vs non-HEC), language. Near-identical messages collapse into ONE template. Surface the library in the CRM Templates tab; re-runnable so new sends fold in.

**Why:** he wants structure derived from his REAL sends, browsable as "kinds of messages I can send," not invented or imitated prose. He explicitly changed his mind away from "learn to write like me."
**How to apply:** when asked about outreach templates, mine + cluster sent messages; never build a style-learner.

**CRITICAL correction (2026-06-30):** do NOT keep appending each new message as a separate flat template — he flagged the growing flat list as wrong.

**The mechanism (locked 2026-06-30):**
- Each message he sends me → **capture** it to `~/.medtech-crm/template-captures.jsonl` (raw, lightly parameterized `[Prénom]`/`[entreprise]`/`[rôle]`), and **try to fit it into an existing cluster** (clusters live in `~/.medtech-crm/template-state.json`). If it fits, tag it. **If it's clearly different, leave it be (append as "unique")** and increment `uniques_since_recluster`.
- **Every 3 unique (non-fitting) messages** → run a **big-picture re-cluster**: reconsider categories/structure.
- Output is ALWAYS a **human-readable** `…/Healthcare Idea/template-library.md`: a plain-language SUMMARY at the very top, then categories **well-separated with text formatting**. Also reflect categories in crm.json templates (add `category` field, group; never delete).
- **One-time kickoff:** scheduled auto-fire at 2026-06-30 19:00 (CronCreate job, session-only) to cluster everything captured so far. Revert snapshot = `~/.medtech-crm/template-snapshot-pre-cluster.json` ("revert the templates" restores it).
**Salutation (2026-07-01):** first message AFTER a connection is accepted uses **"Bonjour M./Mme [Nom]"** (formal), NOT "Merci pour la connexion, [Prénom]". Applies to pro targets; peers stay casual.

**Monitor-driven CRM (2026-07-01):** the CRM must be populated at the MONITOR level, not only when he sends via the bot (he'll often forget Alt+L). Connection monitor (`connections.js`) → every accepted connection upserts a CRM lead at `connect_accepted`. Message monitor (`messages.js` via `monitor.mjs`) → thread read: he sent last → `dm_sent`; they replied → `replied`. Stages advance **forward-only** (`STAGE_RANK` guard in `ingest-intake.js`; monitor only POSTs on a forward change). Runs on the 20-min watch loop + on-demand ("suivi"). So CRM state = LinkedIn reality regardless of Alt+L/bot.

**Alt+Shift+M profile widget (2026-07-01):** on a LinkedIn profile, Alt+Shift+M injects a floating widget (extension `background.js` → `showMsgWidget`) that fetches the ready message from intake `POST /message` (pre-drafted from pending.json if known, else rule-qualified from the headline via `qualifyDraft`), with Copy, an HEC toggle, and connection-type buttons that advance the CRM. Go link-by-link on the profiles.

**FINAL MODEL (2026-06-30, supersedes single-category):** templates are **multi-tag**, not single-category. Each has a `tags` array across ~10 dimensions (angle: curiosité/solution/expert-opinion/traction/sales-push · voix: je/nous · cible: responsable-direct/directeur-hôpital/achats · étape: 1er-contact/relance/post-connexion · canal · longueur · pilote · réseau HEC/non-HEC · langue · intention:relai). `meta.tag_dims` (in crm.json) maps tag→dimension. Faceted **toggle browser** at `node ~/.medtech-crm/template-browser.js` → http://127.0.0.1:4151 (OR within a dimension, AND across). Granularity was elicited via a trippy-style **duel** tool (`template-duel-server.js` :4150, judgments in `template-judgments.jsonl`, insights in `template-insights.md`). HEC = its own tag but same "category feel" + separate template (A/B). Deleted the disliked `long_fr`/`long_en`/`long_de`.

- Raw captures so far: `expert_opinion_fr` (long, no-pilot, "je cherche des experts" — runs the place but not the exact owner), `conn300_direct_fr` (300-char, direct-responsible), `followup_direction_nonhec_fr`, Julie's curiosity-long, the Mounir post-connect follow-up, and the InMail sales-push + subject "IA dans la gestion du parc des dispositifs médicaux" (direct expert).
