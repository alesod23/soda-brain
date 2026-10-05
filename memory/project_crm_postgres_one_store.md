---
name: project_crm_postgres_one_store
description: His 5 Oct 2026 decision: the CRM store is Postgres on the box (phase 3b), to-dos, hub cards and messages go in with embeddings, meetings stay out (RAG as a tool for the meeting loop), native Telegram buttons via a plugin patch
metadata:
  type: project
---

Decided 5 Oct 2026 (laptop UI questions, after "we have to make the CRM much more lightweight" and "the CRM should just be available, should be on the cloud"):

- **Store:** Postgres on the box (the brain's DB, port 5432 local, door :4150) becomes the CRM source (phase 3b in `.medtech-crm/WORKPLAN-20261001-crm-postgres.md`); the service is the one writer; `crm.json` is a nightly export only. History (activity, undo last 5 per person, step match history) = rows loaded on demand; one `pg_dump` a night to Drive.
- **One store for the RAG:** to-dos, hub cards with his verdicts, and messages/events (WhatsApp, Gmail, LinkedIn, Slack) go in with embeddings. Meetings do NOT become rows: "RAG as a tool where it can get their context about a meeting", used by the meeting loop before/during/after, "and about every event". Person id is one join key, not the link: the hybrid search is.
- **Review list:** current text only, previous versions on click, refresh only on change (ETag), and pagination 20 at a time.
- **Telegram:** native inline Yes/No/Change buttons on hub cards by patching the official Telegram plugin on the box (it drops non `perm:` callbacks today); same bot, no new poller; a probe re-applies the patch after plugin updates.

**Why:** the laptop replica proxied every 7 MB read to the box (3 to 5 s), 26 backups per save, two review queues; he wants always-on, cloud, scalable, and the RAG across to-dos, CRM and events.

**How to apply:** no new feature on crm.json readers; build on the Postgres path; keep the laptop a client. See [[reference_soda_brain]], [[project_crm_is_the_followup_surface]].
