---
name: reference_tundra_crm_taxonomy
description: Tundra CRM category taxonomy + graded email verification + agentic-search source (2026-07-06 refactor)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 040b02ee-cbd5-4294-b80e-6e8423801f02
---

Tundra medtech/coattio CRM (`~/.medtech-crm/`, UI 127.0.0.1:4124) contact model, refactored 2026-07-06:

**Category = persona (single-valued):** Clinical engineer (senior) · Clinical engineer (junior) · Procurement · CFO (Finance Director) · IT · Doctor · Hospital sales · Director (hospital) · autre. A clinical engineer who ALSO buys → keep category + `does_procurement=true` (a `+achats` chip), NOT the Procurement category. Defined in FIVE places — KEEP IN SYNC: `crm-app/public/app.js` (`CATEGORIES`), `classifyCategory()` in `intake-server.js` AND `ingest-intake.js` (mirrors), + the Alt+L popup `DEFAULT_CATS` in `medtech-capture-extension/popup.js` (SYNCED 2026-07-08 to the canonical 8; was old labels). `does_procurement` now settable from the popup via a **"+achats (procurement)" toggle** → posts `{action:'categorize',does_procurement}` → intake-server passes it through → ingest applies it in the categorize block; `/lookup` returns `does_procurement`. Migration `~/.medtech-crm/migrate-categories.js` (idempotent) remapped 97 contacts.

**LinkedIn in-page badge (`coattio-badge.js`, ext v1.22+):** now a 2-line card (stage x/4 + category/+achats/email-trust/via) that is a **clickable link to the coattio profile** via deep-link `http://localhost:4124/#/p/<cid>/<pid>`. `/lookup` returns `cid`+`pid`; `app.js applyRoute()` + boot handle `#/p/<cid>/<pid>` to open that person's drawer. `cid`/`pid` are é-stripped slugs but match via the person's stored `linkedin` url (NOT reconstructed from the id — the id strips accents).

**Multiple contact points (added 2026-07-08):** a person can hold several emails/phones ("not sure which is correct — keep both"). Model: `p.email`/`p.phone` = PRIMARY (drives `email_status`/verification/readiness); `p.emails`/`p.phones` = arrays of EXTRAS. Helpers in `app.js`: `allEmails(p)`/`allPhones(p)` (deduped union), `emailsTo(p)` = comma-joined → **every gmail-draft `to` sends to ALL emails** (gmail.py `msg["to"]=args.to` accepts a comma list). Appels/call cards + `canauxCell` (✉/☎ with a `+N` superscript) show ALL. Drawer Propriétés has a multi-value editor (`data-farr`/`data-addarr`/`data-delarr`; empties auto-stripped on blur). Ingest `addContactPoint(p,kind,val)` (case/format-normalized dedup) means capture/enrichment/comment-extract/vision-recapture APPEND new values and preserve the old primary as an extra — never overwrite/drop.

**Email trust = graded `email_status`:** none 🔴 / inferred 🟠 / published 🟡 / verified 🟢 (colored badge; `email_verified` = derived mirror). published = printed on a real source; verified = confirmed deliverable. Verifier = free-tier **Hunter.io** API (NO paid plan), script `~/tundra-outreach/hunter-verify.js` (reads a CSV of emails → v2 email-verifier endpoint; key was pasted in-session, not committed). **Invalid/undeliverable emails MUST carry a note that the address was tried + is dead ("find a better one")** so no session reuses them.

**`contact_source`** person field = provenance of email/phone/role (separate from the free `notes`). **`source` value `agentic-search`** = a contact found by an agentic web search (vs alt-l / apollo / lemlist / manual).

**Flow:** `/overnight` harness enriches → Hunter verifies → deliver a **Google Sheet** in the Tundra Shared Drive (`H:\Shared drives\Tundra Shared Drive`, usually `Outreach/`; [[feedback_tundra_deliverables_gdrive]]) → insert into CRM **company-first** (a deliberate, OBSERVED step, never auto-dump). Full docs: `medtech-brain/_system/TUNDRA-STACK.md` + `OUTREACH-SYSTEM.md`. See [[reference_coattio_servers]], [[reference_overnight_harness]].
