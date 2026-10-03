# MONITOR LAYER: one event log, every channel, both directions

Status: DESIGN + SKELETON (4 Oct 2026). Nothing here runs in production. The skeleton is `tools/migrations/001_brain_events.sql`
and `tools/monitor/`, tested by `tools/tests/test_monitor.py` (no database) and `tools/tests/test_monitor_pg.py` (Postgres 16 +
pgvector). Source of the requirements: task-land `_system/HANDOFF-20261003-quick-claude-to-system.md`, sections 6d to 6g.

## 1. Why

Today four loops each read their own sources (system/LOOPS.md 1, 2, 3, 5):

| Loop | Reads | Misses it caused |
|---|---|---|
| CRM monitor (`monitor.js`) | Gmail, WA store, LinkedIn store, sent corpus, Calendar, Notion | no Slack |
| inbound asks (`inbound_asks.py`) | WA store, LinkedIn store, Gmail | inbound only by design |
| meeting loop (`meeting_loop.py`) | Notion meeting notes over MCP | its own island; the CRM monitor re-reads Notion separately |
| `hub_outdated.py` + reverse pass | every Gmail account, WA store, CRM events, LinkedIn store | no Slack (card #28, Lena); his outgoing LinkedIn never existed (card #2, Ienna) |

Each reader has its own idea of "new", its own person matching and its own blind spots. Two misses he named (6g) are
the same failure: the evidence was never in any log the checker read. A hole in one feed is invisible because no one
counts what each feed holds.

The monitor layer replaces the four feeds with ONE ingest: every source is read once, incrementally, in both
directions, into `brain.events`; each event is linked to a CRM person; the loops become subscribers of that log; the
periodic sweep reads the same log instead of re-fetching sources.

## 2. Shape

```
 sources                   adapters (one per source instance)     brain.events (one row per message/booking/note)
 Gmail cdtm/tundra/...  -> gmail:<acct>   fetch(cursor)  --+
 WA store (box)         -> whatsapp                         |    Resolver: route memo -> CRM exact handles
 LinkedIn store         -> linkedin                         +--> store.write_batch(source, events, cursor)
 Slack cdtm/xplore      -> slack:<ws>                       |    dedupe (source, source_id), cursor same transaction
 Calendar               -> calendar:<acct>                  |
 Notion Meetings        -> notion:meetings                  |
 CRM writes (H33/H34)   -> crm                           --+
                                                                   |
                         path A: Dispatcher.dispatch(new events) --+--> subscribers (todo_match, reverse pass,
                                                                   |     inbound asks, CRM reader, meeting loop)
                         path B: sweep(open items) reads events_for_person(...)  (no source fetch)
                                                                   |
                                     both write brain.event_findings -> brain.event_attribution (A vs B)
```

One process on the box (`monitor_tick`, see 9) runs: every adapter's `run_once`, `resolve_backlog`, `dispatch` of the
new events, `catch_up` for retries, and on its slower cadence the sweep. Embeddings are filled by the existing index
pass (`brain_index.py`, every 5 min), never by ingest, so a tick stays cheap.

## 3. Schema (`tools/migrations/001_brain_events.sql`)

Not folded into `schema.sql`: `box-install.sh` applies `schema.sql` on every run, and nothing writes these tables
before the shadow phase is started by hand. Idempotent, runs twice cleanly (tested).

### `brain.events`: the per-person log

| Column | Meaning |
|---|---|
| `id` bigserial | row id; deliveries and findings point at it |
| `source`, `source_id` | **dedupe key**, `UNIQUE (source, source_id)`. `source` is the adapter instance (`gmail:cdtm`, `whatsapp`, `linkedin`, `slack:cdtm`, `calendar:cdtm`, `notion:meetings`, `crm`); `source_id` is the id the source gives the thing (Gmail message id, WA message key, LinkedIn store `id`, Slack `channel:ts`, Calendar event id + updated, Notion page id + last edit, CRM ledger id) |
| `channel` | `email whatsapp linkedin slack calendar meeting crm` |
| `direction` | `in` (to him), `out` (he sent it), `internal` (a CRM write, a booking with no sender) |
| `ts`, `ts_precision` | when it happened at the source (not when we read it), `exact/minute/day` (35 of 87 LinkedIn lines are day-precision) |
| `thread` | thread / chat / conversation id at the source |
| `person_id`, `person_via` | link to `crm.people.id`; NULL until resolved; `via` = `route email phone linkedin slack manual`. No FK on purpose: an event may arrive before the CRM row exists, and `resolve_backlog` links it later |
| `handles` jsonb | the raw counterpart handles `[{kind, value}]`, normalised (`events.norm_handle`): what the resolver and the route memo work from |
| `text` | body, capped at 8,000 chars (the source keeps the rest) |
| `data` jsonb | adapter extras: subject, url, account, chat name, attachment names |
| `tsv` | generated full-text vector (`simple` config: mixed IT/DE/EN/FR) |
| `embedding` vector(384) | e5-small, filled by the index pass, same model as `brain.chunks` |
| `ingested_at` | when we stored it; time-to-find is measured from `ts`, lag from `ingested_at` |

Indexes: `(person_id, ts DESC)` (the per-person read every subscriber and the sweep do), `ts`, partial on unresolved,
`(source, thread)`, GIN on `tsv`, HNSW on `embedding`.

### Companion tables

- `brain.event_routes (kind, value) -> person_id`: the remembered route (6d "memorize the paths"). Written the first
  time a CRM handle resolves an event, with every other handle of that event (so the LinkedIn thread id learned from
  the first message links his reply, which carries no profile URL). Read FIRST on every later event. `hits` and
  `last_seen` show which routes are alive. Also the target of on-demand backfill (6g).
- `brain.event_cursors (source) -> cursor jsonb`: incremental reading, written in the same transaction as the events.
- `brain.event_deliveries (subscriber, event_id)`: exactly-once delivery per subscriber, `mode shadow|live`,
  `status ok|skipped|error` (error = retried by the next `catch_up`).
- `brain.event_findings` + view `brain.event_attribution`: the measurement (section 8).

### Relation to `crm.events`

`crm.events` (filled by `POST /crm/events` from `monitor.js`' ledger) stays as it is during the migration. The `crm`
adapter reads it into `brain.events` with `channel crm, direction internal`, so CRM writes are on the same per-person
timeline. After cutover `crm.events` becomes what monitor.js writes about its own actions, nothing else.

## 4. Adapters

Interface (`monitor/ingest.py`, `Adapter` protocol):

```python
class Adapter(Protocol):
    source: str
    def fetch(self, cursor: dict | None) -> tuple[list[Event], dict]: ...   # only what is new since cursor
    def fetch_person(self, routes: list[dict]) -> list[Event]: ...         # on demand, THIS person's thread
```

Four rules every adapter keeps, each with a test in the reference adapter:

1. **Incremental.** `fetch(cursor)` returns only what is new; the cursor is opaque to everything but the adapter.
2. **Both directions.** What he sent is an event exactly like what he received (`direction out`).
3. **Fail loud.** An unreadable source raises; `[]` means "nothing new", never "could not read". `run_once` reports
   the error and leaves the cursor untouched (the tundra 403 lesson: a judge looking at a hole closes the wrong cards).
4. **Stable ids.** The same message always gets the same `source_id`; the store dedupes repeats (the real LinkedIn
   store held 87 lines for 63 ids on 4 Oct).

| Source | Adapter (`source`) | Reads | Cursor | Out direction | Handles | Status |
|---|---|---|---|---|---|---|
| LinkedIn store | `linkedin` | `/home/da/gdrive/DA/linkedin-store.jsonl` | byte offset + hash of the first line (rewrite detection) | `fromMe` | `li_thread` chatId, `linkedin` profile URL, `name` (never auto-links) | **built** (`adapters/linkedin_store.py`, the reference). Needs poll.py Fix 1 (stop dropping `fromMe`, ~line 127) before out-events exist |
| WhatsApp | `whatsapp` | `/home/da/wa-daemon/message-store.jsonl` (box original, not the Drive copy) | byte offset + head hash, same as LinkedIn | `fromMe` | `phone` (JID digits), `wa_chat` for 1:1 chats only; groups carry no person handle | design |
| Gmail | `gmail:<acct>` per account | `triage/gmail.py` history API | Gmail `historyId` | label SENT | `email` From/To/Cc minus his own addresses | design |
| Slack | `slack:<ws>` | `/home/da/slack/slack.py` conversations.history on DMs + mentions | per-channel latest `ts` | `user == self` | `slack` user id, `email` from users.info | design; closes the #28 gap |
| Calendar | `calendar:<acct>` | `gcal.py` sync token | sync token | organiser == him | attendee `email` | design |
| Notion meetings | `notion:meetings` | Meetings database, relation Contact | last edited time | `internal` | Contact relation -> CRM id (`person_via manual`) | design; emitted only after the note settles (22 to 49 min) |
| CRM ledger | `crm` | `crm.events` | max `at` + id | `internal` | `person_id` already set | design |

`fetch_person(routes)` is the 6g fix for the Ienna miss: the LinkedIn poller sees only the ~17 most recent threads, so
an open card's person whose thread went quiet is read by route, on demand, through `backfill_person` (same dedupe,
cursor not moved). The skeleton filters the store file by thread id; the live version opens that thread in the poller
profile.

## 5. Resolver: event -> person

`monitor/ingest.py:Resolver`, in order:

1. Event already carries a `person_id` (CRM ledger, Notion relation): keep it.
2. **Route memo**: any auto-link handle of the event in `brain.event_routes` -> that person, `via route`.
3. **CRM exact handles** (email, phone, LinkedIn URL, Slack id from `crm.people`): first hit links, `via <kind>`, and
   every auto-link handle of the event is written to the route memo.
4. Otherwise unresolved. `resolve_backlog` retries at the end of every tick (a CRM row created later, a route learned
   since, a route he set by hand).

Never automatic: a `name` handle (several CRM people share names), and a handle two CRM rows share (`office@clinic`):
both stay unresolved and are counted. Semantic person matching (`crm.people_chunks` through `brain.match_event`) is a
subscriber's job on unresolved events, proposing a route through the hub, never a silent link.

## 6. Loops as subscribers (path A)

Interface (`monitor/subscribers.py`):

```python
class Subscriber(Protocol):
    name: str                                            # keys deliveries and attribution
    def wants(self, ev: StoredEvent) -> bool: ...        # cheap, no I/O
    def on_event(self, ev: StoredEvent, ctx: PersonContext) -> Result: ...   # Result.findings
```

`PersonContext` gives the person's last 30 days of events and routes, lazily, from the log: 6d "when we have a card
about a person, we should have its events as context". `ctx.mode` is `shadow` or `live`; the `Dispatcher` defaults
every subscriber to shadow, so nothing acts by accident. A raising subscriber gets an `error` delivery and is retried
by `catch_up`; a subscriber added later catches up on the log from any date.

| Today | As a subscriber | wants() |
|---|---|---|
| `todo_match.on_event` (wired 3 Oct into hub_outdated + meeting loop) | `todo-match`: `brain.match_event` on every event (6e "why wouldn't it fire on every event"), judge only on `sim >= match_strong` | every event with text |
| hub_outdated reverse pass | `card-outcome`: an event about a person with an open card -> judge that card with the person's context (his messages up to 10 days before the card count) | resolved events whose person has an open card |
| inbound asks | `inbound-asks`: question or request -> draft card | `direction in`, channel email/whatsapp/linkedin/slack |
| CRM monitor `applyEvent` + reader queue | `crm-reader`: replied/accepted/booked + queue the person for the reader with `last_read_event_id` = the event id | resolved events |
| meeting loop | `meeting-loop`: reads the note, `dated_items`, open loops | `channel meeting` |
| sodanotif (Telegram push) | out of scope: it stays a 60 s notifier on its own pollers until the log is proven faster | n/a |

The judges and their prompts do not change; only where their input comes from changes.

## 7. The periodic sweep (path B)

`subscribers.sweep(store, items, check)`: each open item (hub card, to-do, CRM next step) with a person reads that
person's events from the log, from 10 days before the item to now, and a `check` (rule or model) judges. It never
fetches a source. Items without a person are counted as `no_person`: the blind spot this layer exists to shrink,
reported every run. A status-only finding (the item is settled by the current state of the system, 6f "he may say
events and mean status") is a finding with `event_id NULL`.

## 8. Measurement (6f)

Both paths write `brain.event_findings (surface hub|todo|crm, item_id, path A|B, finder, mode, verdict, event_id,
evidence)`. `brain.event_attribution` (SQL) and `subscribers.attribution()` (Python, same answer, tested against each
other) give per item: first path and finder, time-to-find (`found_at - event.ts`), and whether the other path also
found it ("would also have found it"). `attribution_report` aggregates per path and per surface.

How it plugs into the existing learning layer (`task-land/_system/cleaning_eval.py`, OFF until `cleaning-eval.on`):

- `cleaning_eval` keeps owning success (72 h without a reverse or a "wrong"), the weekly 3 random successes in the
  Cleaning tab, failure traces in Langfuse, and threshold / exception auto-adjust. It reads path and finder from
  `brain.event_findings` instead of inferring them from `todo-match.jsonl`.
- A live action writes `event_findings.id` into its `todo-match.jsonl` line, so a reverse in the Cleaning tab maps to
  exactly one finding, and its failure lands on the right path and finder.
- Shadow findings are measured the same way but compared against what the legacy loop actually did: a shadow finding
  the legacy loop missed = a catch; a legacy action with no shadow finding = a gap of the new layer.

Per-channel coverage is part of the same report: events per `(source, direction)` per day and the unresolved share.
"LinkedIn out = 0" is then a red number on day one, not a miss discovered on card #2.

## 9. Migration with shadow mode

1. **Schema + read-only ingest (shadow).** Apply `001_brain_events.sql` by hand on the box. A `da-monitor.timer`
   (2 min) runs `monitor_tick`: adapters `run_once`, `resolve_backlog`, no subscribers. Check per-source counts against
   each store's own count for a week. Prerequisites: poll.py Fix 1 (LinkedIn `fromMe`), the Slack adapter.
2. **Subscribers in shadow.** Register the subscribers with `mode shadow`: they judge, record deliveries and findings,
   act on nothing. The legacy loops keep running and acting. Daily shadow report: catches, gaps, latency vs legacy,
   per-channel coverage. Re-run the two named misses as acceptance tests: Ienna #2 (LinkedIn out + `fetch_person`) and
   Lena #28 (Slack) must be found in shadow.
3. **Cutover per subscriber.** One subscriber at a time goes `live` (the modes map) and its legacy reader stops reading
   its own source (a flag in that script, not a delete). Order: `card-outcome` (hub_outdated's reverse pass), then
   `todo-match`, `inbound-asks`, `crm-reader`, `meeting-loop` last (the Notion MCP read moves into the adapter).
4. **Retire the feeds.** When every subscriber is live for a week without a regression in `cleaning_eval`, the legacy
   source readers are removed and LOOPS.md sections 1, 2, 3, 5 are rewritten to point here.

Rollback at any step: set the subscriber back to `shadow`, re-enable the legacy reader's flag. Events stay; nothing is
lost because the log only appends.

## 10. What the skeleton is, and is not

Built and tested (`tools/monitor/`):

- `events.py`: `Event`, `StoredEvent`, `Finding`, handle normalisation, validation mirroring the table's checks.
- `store.py`: `Store` protocol, `MemoryStore` (tests, laptop dry runs), `PgStore` (psycopg 3). Contract: batch is
  all-or-nothing with the cursor, dedupe by `(source, source_id)`, only new events returned in `ts` order.
- `ingest.py`: `Adapter` protocol, `Resolver`, `run_once`, `resolve_backlog`, `backfill_person`.
- `subscribers.py`: `Subscriber` protocol, `Dispatcher` (shadow default, retries, catch-up), `sweep`, `attribution`.
- `adapters/linkedin_store.py`: the reference adapter on a fictional fixture of the real line shape.

Not built: the other adapters, the concrete subscribers, `monitor_tick` and its timer, the embedding pass over
`brain.events`, the shadow report. Nothing imports `monitor` in production; the migration is applied nowhere.

Open decisions:

- Box Postgres version: `UNIQUE NULLS NOT DISTINCT` on findings needs PG 15+ (the box runs 16; fine).
- Which Gmail accounts: cdtm and tundra certainly; sodano23's token is expired (FINDINGS-20261001.md).
- Retention of `text` for personal WhatsApp chats in the log (today the same text already sits in the WA store).

## Tests

```
cd tools
C:/Users/Alessandro/.venvs/brain/Scripts/python -m pytest -p no:cacheprovider -q tests/test_monitor.py tests/test_monitor_pg.py
```

`test_monitor.py`: no database. `test_monitor_pg.py`: `SODA_TEST_DSN` (a throwaway database; the test drops schema
`brain` in it, never the box), else the `pgserver` package, else skipped.
