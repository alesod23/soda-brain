---
name: reference_linkedin_ingest_new_people
description: "How a LinkedIn event about someone NOT yet in the CRM becomes a row (monitor.js liNewPeople, li_request_sent, accept -> first-message draft in inbound_asks.py); built 2026-10-01 from sim day 2026-10-07"
metadata:
  node_type: memory
  type: reference
  originSessionId: a9e8f86d-8b78-44fd-bea0-3d9e84ec583a
  modified: 2026-10-01T00:44:15.283Z
---

**The gap (sim 2026-10-07, his item):** the li tick read the LinkedIn store but dropped every row whose chat name the
CRM did not carry: his invites to new people, their accepts and the replies left no ledger line and no row. The live
liaccept tick applied accepts without a ledger line; nothing drafted the first message after an accept.

**Now (patch `~/sim/harness/patches/patch_linkedin_ingest.py`, backups `.bak-20261001-feedback`):**
- `~/.medtech-crm/crm-app/monitor.js`: `liNewPeople` opens a row (holding company, source "linkedin: his first
  message", ledger outcome "new person") for a full name he writes to; `liOutKind`: his first message in a chat before
  any of theirs, not connected = `li_request_sent` (connect_sent_date, touch1 sent, step "Wait for X to accept the
  LinkedIn request", them, +7d, origin default); an outbound to nobody is ledgered unmatched; liaccept calls ledgerApplied.
- `~/gtm-eng/agent/inbound_asks.py`: applied `li_connected` ledger line -> `handle_accept` -> ACCEPT_PROMPT (his
  note's language and register) -> step his -> one linkedin-draft card (he pastes). Skipped if either side wrote after.
- Sandbox stand-in `~/sim/harness/fakes/li_accept_tick.js` ledgers unmatched accepts once.
- Tests: `node ~/sim/harness/tests/replay_li_20261007.js` (engine, no model), `python ~/sim/harness/tests/replay_li_asks.py` (3 Opus calls).

**Limit:** a row opened from the store has no profile URL (only the thread URL in `linkedin_thread`), and live
`liPending` needs `p.linkedin` to check the accept: until enrichment or channel search fills it, a live accept of
such a row is only seen when they write. monitor.js runs inside the laptop CRM server: a change is live after its restart.
Related: [[reference_simulation_harness]], [[reference_rule_loop]].
