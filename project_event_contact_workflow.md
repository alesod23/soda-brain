---
name: project_event_contact_workflow
description: Conference contact workflow (capture -> one hub card -> coattio + Notion + 48h follow-up task); the /intake route that was missing; workplan path
metadata:
  type: project
---

**Event contact workflow (started 2026-09-15, MEDICON Siena).** Workplan: `task-land/_system/WORKPLAN-20260915-event-contact-workflow.md`. His ask: a repeatable way every conference contact (phone contact, dictated name, third-party name, badge photo, LinkedIn URL) lands in coattio, Notion Contacts, and a follow-up task due 48 h after the meeting, with verified vs unverified kept in the record.

**The bug that hid everything:** `triage/contacts_sync.py` (box cron, 30 min) posted approved Google-Contacts rows to `127.0.0.1:4137/intake`, a route that did not exist anywhere, so approved rows sat at "coattio skipped (HTTPError)" and Notion never got them. `POST /intake` exists since 2026-09-15 in `~/.medtech-crm/intake-server.js` (`contactsIntake`): idempotent (Google resource, email, phone, name+org), writes through the CRM's `PUT /api/data`, stores `p.event {name, session, met_on, verified, given_by}` and `p.google_resource`.

**Why:** one owner per person and never auto-file: every batch is ONE hub card (yes / no + numbers / no), Notion rows only after that yes. See [[reference_contacts_sync]], [[project_coattio_v2]], [[reference_notion_tundra_system]].
**How to apply:** open items are in the workplan's build order (add command for the savior, task per approved row, Notion sync mapping for event people, dedup against wa-daemon contacts). Do not touch the Telegram lane; the savior keeps the conference side.
