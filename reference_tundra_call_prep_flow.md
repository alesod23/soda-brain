---
name: reference_tundra_call_prep_flow
description: "When a sodaOS audio recording is prep for an upcoming Tundra call, the router flags it (flag_call_prep) and a live Claude Code session must check the calendar and create/update a Notion 'Call prep' page under Validation Reachout."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2128ab65-69ab-46de-9e4c-680c11ed4fc3
---

Set 2026-07-14, after the first real case (a recording prepping market-sizing data for a
"City Venture Fund" call — turned out to be a CDTM Venture Fund meeting with Franz Waltenberger,
per the calendar).

**The flow:**
1. The sodaOS router (`~/.claude/sodaos/route-prompt.md` + `ingest.js`, see
   [[project_sodaos]] round 5) sets `flag_call_prep: true` on a `medtech-brain`-routed capture
   when the content is explicitly prep for an upcoming call/meeting (not a debrief of one that
   already happened — debriefs are just normal medtech-brain content, flag stays false).
2. The Raw note written to `medtech-brain/Raw/` gets a `⚠️ CALL-PREP-FLAG` callout — this is the
   signal a live Claude Code session should act on. The automated bot/watcher CANNOT do this part
   itself (no Notion/Calendar MCP access in the headless `claude -p` calls — same constraint as
   [[feedback_notion_write_needs_approval]]'s reasoning for why Notion writes need a live session).
3. **In the live session, when you see a CALL-PREP-FLAG:**
   - Look up the matching event on Google Calendar (`search_events` / `list_events`) to enrich
     with the real date/time/attendees — the audio content alone may mis-transcribe names (e.g.
     "City Venture Fund" → actually "CDTM Venture Fund", caught by cross-referencing the
     attendee's `@cdtm.de` email on the calendar event).
   - Create a **Meetings** row (Type per the call) in the NEW tundra Notion workspace
     (`alessandro@tundrahealth.ai`, Meetings DB `3a3b30c6-d57e-8037-afdc-c49c85ddbe11`), title
     `<Company/Fund> (<Person>) <date>`, with the `## Call prep` content in the page body and the
     external attendee linked in **Contacts**. (SUPERSEDES the old "Validation Reachout" page.)
     **⚠️ 2026-07-21: Notion MCP still on the OLD cdtm workspace — writes 404 until Alessandro
     reconnects it to the tundra account. Until then do the calendar enrichment + write the Raw
     note, and flag the pending Notion Meetings row rather than attempting it.**
   - Content has (at least) a `## Call prep` section with the prep material (cleaned up from the
     raw transcript, not a verbatim dump), and an empty `## Call notes` heading/placeholder for
     later — "add after the call, or leave it like that" (user's own framing; not every call
     needs a follow-up note).
   - This is a **new-page creation**, not an edit to an existing page — doesn't need the
     per-instance Notion approval gate ([[feedback_notion_write_needs_approval]] targets edits to
     *existing* pages only), but still flag what you created in the response so the user can
     correct a wrong calendar match (e.g. the City/CDTM mishearing) if needed.
4. Raw is immutable — never edit the original Raw file to add the Notion link; the connection
   lives in the Notion page itself (which cites the raw source) and can be added to a `Sources/`
   page in medtech-brain if/when that Raw note gets `/kb-ingest`-ed later.

See [[project_sodaos]] (round 5) for the router mechanics, [[reference_tundra_granola_folder]]
and `medtech-brain/_system/TUNDRA-STACK.md` for how Tundra's Notion/calendar/vault pieces connect
generally.
