# Retention: how the brain keeps its history for ten years

Research note, 2026-10-04. Scope: the Postgres 16 + pgvector database `soda` on the box (schemas `brain`, `crm`,
`todo`, `hub`, see `tools/schema.sql`). The owner's rule is the constraint, not a preference: nothing is deleted;
done is a state, never a delete; Postgres is there to hold a lot, because it is his brain. Every recommendation
below keeps that rule and says why it fits this system. Sources are linked inline and listed at the end.

## Index

1. [Recommendations (read this first)](#1-recommendations)
2. [What the schema does today](#2-what-the-schema-does-today)
3. [Append-only history and event sourcing](#3-append-only-history-and-event-sourcing)
4. [Soft delete vs status](#4-soft-delete-vs-status)
5. [Size projection: ten years of one person](#5-size-projection-ten-years-of-one-person)
6. [Partitioning: when it starts to matter](#6-partitioning-when-it-starts-to-matter)
7. [pgvector indexes and autovacuum as rows grow](#7-pgvector-indexes-and-autovacuum-as-rows-grow)
8. [Ranking old and done items down instead of deleting them](#8-ranking-old-and-done-items-down-instead-of-deleting-them)
9. [Embedding model upgrades and re-embedding](#9-embedding-model-upgrades-and-re-embedding)
10. [Backups on one small VPS](#10-backups-on-one-small-vps)
11. [Measure instead of estimate: queries to run on the box](#11-measure-instead-of-estimate)
12. [Sources](#12-sources)

## 1. Recommendations

1. **Keep "current row + append-only change log", make the log truly immutable, and give the CRM one too.**
   `todo.history` is the right pattern (state table plus audit log, not full event sourcing). Two gaps: its foreign
   key is `ON DELETE CASCADE`, so one `DELETE FROM todo.items` silently erases the history it exists to protect
   (same on `todo.links`, `todo.chunks`); and nothing stops an `UPDATE` on it. Switch the history FKs to `RESTRICT`,
   add a trigger that refuses `UPDATE`/`DELETE`/`TRUNCATE` on history tables, and add `crm.people_history` /
   `crm.companies_history` rows (old -> new per changed record, written in `crm_put` where the sha diff already
   happens). (Sections 3, 4.)
2. **Stop storing the whole CRM document on every save; store per-record changes plus one daily snapshot.**
   `crm.doc_versions` is the only table that can fill the 96 GB disk: one row per distinct save of a document that
   is 6.3 MB today and was 0.5 MB in July. Per-record history (recommendation 1) keeps every change and loses no
   information; the full document stays reconstructible from rows plus the daily checkpoint. This is "store it once",
   not "delete": existing rows stay. Everything else in the database projects to about 2 to 3 GB after ten years.
   No partitioning is needed for ten years. (Sections 5, 6.)
3. **Upgrade pgvector from 0.6.0 (Ubuntu's package) to 0.8.6 or later (PGDG apt repository) and keep HNSW.** 0.8.3 and 0.8.4
   fixed index corruption and `hnsw graph not repaired` errors during HNSW vacuuming; this schema deletes and
   re-inserts chunks on every edit, so it vacuums HNSW constantly. 0.8.0 adds iterative index scans, which this
   schema needs once most rows are `done` (a status filter after an approximate scan otherwise returns too few
   rows). Default autovacuum is enough at this size; set `maintenance_work_mem = '1GB'` for index builds. (Section 7.)
4. **Rank old and done items down at query time, never filter them out of existence.** Multiply the fused RRF score
   by a status weight and a half-life decay per kind (cards fast, to-dos slower, people by last touch), keep `sim`
   undecayed because `todo_match.py` gates on it (0.84), and keep `include_done` for "did I already do this?".
   Store the model name next to every vector and keep the chunk text forever, so a model upgrade is a backfill
   into a second column with its own index, then a cutover. (Sections 8, 9.)
5. **Nightly `pg_dump -Fc` off the box now; add WAL archiving with WAL-G when Postgres becomes the source
   (phase 3b); test a restore every month.** Today the database is mostly derived (git and task-land rebuild
   `brain` and `todo`), except `crm.doc_versions` and `crm.events`, which already exist nowhere else. pgBackRest,
   the usual answer, has been unmaintained since April 2026: do not adopt it. (Section 10.)

## 2. What the schema does today

Read from `tools/schema.sql`, `tools/todo_ingest.py`, `tools/brain_index.py`, `tools/brain_serve.py` on main
(commit `a7b3a81`).

| Table | Write pattern | History today | Retention behaviour |
|---|---|---|---|
| `brain.pages` / `brain.chunks` | upsert by path; chunks deleted and re-inserted when a page changes (unchanged chunk text reuses its embedding) | git (the repo is the source; this schema is a rebuildable copy) | `deleted_at` when a file leaves disk, chunks kept |
| `todo.items` | upsert by slug from task-land files | `todo.history`, one row per change with evidence | `status` open/done/cancelled/parked; `deleted_at` only when the file vanished, row kept |
| `todo.history` | insert only (by convention) | is the history | FK `ON DELETE CASCADE` to items |
| `todo.chunks`, `crm.people_chunks`, `hub.card_chunks` | delete + insert per changed entity, 384-d `multilingual-e5-small` vectors, HNSW cosine index each | none (derived) | follow their parent |
| `crm.doc_versions` | one row per distinct document sha, the whole document as `jsonb` | is the CRM history | grows with every save |
| `crm.people`, `crm.companies`, ... | upsert of changed records by sha | only via `doc_versions` | `deleted_at` when a record leaves the document |
| `crm.events` | insert, `ON CONFLICT DO NOTHING` | is a log | append-only |
| `hub.cards` | upsert from the hub's `state.json`; resolved cards stay (the hub file prunes them after 24 h, Postgres does not) | none per card (status/verdict overwritten once) | `status` open/resolved |

Current scale (memory `reference_soda_brain`, 3 Oct): 545 pages, 1,480 chunks, 310 to-do rows, 641 people, 63 open
cards. This is tiny for Postgres; the decisions below are about not painting the system into a corner over ten years.

## 3. Append-only history and event sourcing

**The pattern options.** Martin Fowler's [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (2005)
defines it as "capture all changes to an application state as a sequence of events", with state rebuilt by replaying
the events and snapshots to avoid replaying from the start. The lighter variant, used by most systems that only need
audit and "what was true when", is a current-state table plus an append-only change log written in the same
transaction. `todo.history` is the second one: `todo.items` is the state, every change writes `{change, evidence}`
with `by` and `at`.

**Why the lighter variant fits this system.** The readers (`match_event`, the daily page, the CRM Today) all want
current state; only "did I already do this?", "when did this change and why" and audits want history. Full event
sourcing would make every reader replay or maintain projections, which is the cost Fowler names, for no reader that
needs it. The state + log design already gives everything his rule asks for: nothing is lost, every change has a
date and evidence.

**Gaps to close (concrete):**

- `todo.history.item_id ... REFERENCES todo.items(id) ON DELETE CASCADE`: a single mistaken delete of an item wipes
  its history. In an append-only design the log outlives the row. Change to `ON DELETE RESTRICT` (Postgres then
  refuses the delete while history exists). Same reasoning for `todo.links` and `todo.items.parent_id` (a parent
  delete cascades to its sub-items).
- Immutability is by convention only. A `BEFORE UPDATE OR DELETE` row trigger plus a `BEFORE TRUNCATE` statement
  trigger that raise an exception make it a property of the table:

  ```sql
  CREATE OR REPLACE FUNCTION brain.refuse_change() RETURNS trigger LANGUAGE plpgsql AS $$
  BEGIN RAISE EXCEPTION '% on %.% is not allowed: append-only', TG_OP, TG_TABLE_SCHEMA, TG_TABLE_NAME; END $$;
  CREATE TRIGGER history_append_only BEFORE UPDATE OR DELETE ON todo.history
      FOR EACH ROW EXECUTE FUNCTION brain.refuse_change();
  CREATE TRIGGER history_no_truncate BEFORE TRUNCATE ON todo.history
      FOR EACH STATEMENT EXECUTE FUNCTION brain.refuse_change();
  ```

  (A superuser can still drop the trigger; that is a deliberate act, not an accident in a script.)
- The CRM has no per-record history; `crm.doc_versions` stands in for it by storing the whole document per save.
  `crm_put` already computes which records changed (`crm_diff.diff`). Writing one `crm.people_history` row
  `{person_id, at, source, version, change: {field: {from, to}}}` per changed record gives the same history as
  `todo.history`, at a few KB per save instead of megabytes (section 5).
- `hub.cards` overwrites `status`, `verdict`, `resolved_by` once. That is one transition, and `created_at` /
  `resolved_at` keep the dates, so a separate history table is optional here. If cards start being revised more
  than once (the hub has `/revise`), give them the same history table.
- Snapshots: keep one full `crm.doc_versions` row per day (the first distinct save after midnight) as the
  checkpoint Fowler describes, so reconstructing "the CRM on 12 March 2029" needs one snapshot plus that day's
  record changes, never a replay from 2026.

## 4. Soft delete vs status

**The critique.** Brandur Leach, [Soft Deletion Probably Isn't Worth It](https://brandur.org/soft-deletion) (2022;
[HN discussion](https://news.ycombinator.com/item?id=32156009)): `deleted_at` leaks into every query
(`deleted_at IS NULL` everywhere, forget it once and deleted data shows up), weakens foreign keys, and in his
experience "never once, in ten plus years, did anyone ... actually use soft deletion to undelete something". His
alternative is to really delete and copy the row into a `deleted_record` table as JSON.

**Why the owner's rule still wins here, and how to take the good part of the critique.** Brandur argues from SaaS
products where deletion is a user action with GDPR obligations. Here, almost nothing is "deleted" in the user sense:
a task is done, a card is resolved, a person moves stage. Those are **states**, and a state column (`status`) is the
correct model, not a soft delete. `deleted_at` in this schema means only "the source file or record vanished"
(`todo_ingest.py`, `brain_index.py`, `crm_put`), which is rare and is itself logged in history. So:

- Keep `status` as the lifecycle and keep `deleted_at` for "source vanished". Do not add `deleted_at` semantics to
  done items.
- Contain the leak Brandur describes with views and partial indexes instead of repeating predicates: e.g.
  `CREATE VIEW todo.live AS SELECT * FROM todo.items WHERE deleted_at IS NULL`, and indexes `WHERE deleted_at IS
  NULL` (the schema already does this for `pages_kind_idx` and `todo_items_status_idx`). A reader that forgets the
  predicate then reads the view and cannot get it wrong.
- His FK point is real and is the reason for recommendation 1: with nothing deleted, foreign keys stay valid, so use
  `RESTRICT` and let Postgres enforce "the row stays".
- The one legitimate deletion is legal (a person asks to be forgotten, GDPR Art. 17). Plan for it as a rare, logged,
  manual procedure (redact the person's row, chunks and history payloads, keep a tombstone row saying a redaction
  happened and when), not as a general delete path.

## 5. Size projection: ten years of one person

**Fixed costs per row** (from the docs): a `vector(384)` takes `4 * 384 + 8 = 1,544` bytes, a `halfvec(384)` 776
bytes ([pgvector README](https://github.com/pgvector/pgvector)). A chunk row also carries its text (about 400
tokens, roughly 1.5 KB) and a stored `tsvector`; above 2 kB a row is TOASTed: compressed first, moved out of line if
still too big ([Postgres 16, TOAST](https://www.postgresql.org/docs/16/storage-toast.html)). Counting the GIN and
HNSW index entries, budget about 6 KB per embedded chunk all-in.

**Volume assumptions** (from today's counts, rounded up; section 11 replaces them with measurements):

| Table | Basis | Per year | 10 years | 10-year size |
|---|---|---|---|---|
| `todo.items` (+ sub-items) | 366 task files after ~4 months | 1,500 | 15,000 | ~50 MB |
| `todo.history` | ~10 changes per item, ~0.5 KB | 15,000 | 150,000 | ~80 MB |
| `todo.chunks` | ~1.3 chunks per item | 2,000 | 20,000 | ~120 MB |
| `hub.cards` | ~40 cards a day | 15,000 | 150,000 | ~300 MB |
| `hub.card_chunks` | one chunk per card | 15,000 | 150,000 | ~900 MB |
| `crm.events` | 13,123 ledger lines so far, ~0.6 KB | 40,000 | 400,000 | ~350 MB with indexes |
| `crm.people` / `companies` / `people_chunks` | 641 people in ~4 months | 1,500 | 15,000 | ~150 MB |
| `crm.people_history` (proposed) | ~20 field changes per person-year | 30,000 | 300,000 | ~150 MB |
| `brain.pages` / `brain.chunks` | 1,480 chunks today, memory grows ~70 facts/month | 3,000 chunks | 30,000 | ~200 MB |
| **Everything except `crm.doc_versions`** | | | **~1.2 M rows** | **~2.3 GB** |

Even at three times these assumptions the database stays under the box's 7.9 GB RAM, which keeps the hot set in
memory (relevant for section 6).

**The outlier: `crm.doc_versions`.** One row per distinct save of the whole CRM document. The document is 6.3 MB
today (`crm.json`, 4 Oct) and was about 0.5 MB in July (the `crm.before-*` backups), so it grows by roughly 2 MB a
month. The laptop's `backups/` ring shows saves in bursts every 10 minutes during the night run; identical documents
are skipped by sha, and the number of distinct versions per day was not measured (section 11 has the query). With
JSON compressing roughly 3 to 5 times under TOAST, a version costs 1.5 to 2 MB now and grows with the document:

| Distinct versions a day | Per year (at today's size) | 10 years (document keeps growing) |
|---|---|---|
| 10 | ~6 GB | well over 100 GB |
| 50 | ~30 GB | far beyond the 96 GB disk |

This is the only thing in the database that threatens the disk, and it is redundancy, not information: two
consecutive versions differ in a handful of records. Per-record history (section 3) keeps every change at a few KB
per save; one snapshot a day keeps cheap reconstruction (365 a year, ~0.7 GB a year at today's size, still growing
with the document; a weekly snapshot is the lever if that ever matters). Existing `doc_versions` rows stay.
`ALTER TABLE crm.doc_versions ALTER COLUMN doc SET COMPRESSION lz4` (new rows only) makes compression faster; it is
not a substitute for not storing copies.

## 6. Partitioning: when it starts to matter

The Postgres manual's rule of thumb: "the exact point at which a table will benefit from partitioning depends on the
application, although a rule of thumb is that the size of the table should exceed the physical memory of the
database server" ([Postgres docs, Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)).
Practitioners on the mailing lists put the row counts far higher than anything here: Stephen Frost (Postgres
committer) answered "no" for an 83 million row, 38.6 GB table that does not grow much
([pgsql-general, 2018](https://www.postgresql.org/message-id/20181011005157.GD4184%40tamriel.snowman.net)); the main
reason to partition is dropping old data a partition at a time, which this system never does by rule.

**Verdict for this system:** no partitioning for ten years. The largest table projects to a few hundred thousand rows
and the whole database to about 2 to 3 GB, below the 7.9 GB RAM threshold. Partitioning would add planner surprises
and per-partition HNSW indexes (each searched separately) for no gain. The tripwire to revisit: any single table
above ~5 GB or ~50 M rows, or `crm.doc_versions` if recommendation 2 is not done (and partitioning does not make it
smaller, only easier to move to cheap storage). If it ever happens, the candidates are the append-only logs
(`crm.events`, `todo.history`) by year, where time-range partitions match how they are read.

## 7. pgvector indexes and autovacuum as rows grow

**Which pgvector is on the box.** `tools/README.md` says pgvector 0.6 from apt; Ubuntu 24.04's universe package is
`postgresql-16-pgvector 0.6.0-1` ([Ubuntu packages](https://packages.ubuntu.com/postgresql-16-pgvector)). Since then
([CHANGELOG](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md)):

- 0.7.0 (2024-04): `halfvec`, `sparsevec`, `binary_quantize`.
- 0.8.0 (2024-10): iterative index scans and better cost estimation for choosing between the ANN index and a B-tree
  ([announcement](https://www.postgresql.org/about/news/pgvector-080-released-2952)).
- 0.8.3 (2026-06-17): "Fixed possible index corruption with HNSW vacuuming".
- 0.8.4 (2026-06-30): "Fixed `hnsw graph not repaired` error with HNSW vacuuming", "Fixed possible error with
  inserts during HNSW vacuuming" (the bug report:
  [pgvector#993](https://github.com/pgvector/pgvector/issues/993), concurrent insert/delete workloads).
- 0.8.7 (2026-10-01): current upstream (IVFFlat build fix); the PGDG repository for Ubuntu 24.04 ships 0.8.6-1 as of 4 Oct 2026, which already has every HNSW fix above.

**Why the upgrade matters for this schema specifically.** Every index pass deletes and re-inserts the chunks of a
changed page, item, person or card (`brain_index.py`, `todo_ingest.py`). Every such change leaves dead tuples in the
HNSW graph, which autovacuum then repairs, concurrently with the next 5-minute index pass inserting. That is exactly
the workload of the vacuum fixes above. Install from the PGDG repository (`apt.postgresql.org`, `postgresql-16-pgvector 0.8.6-1.pgdg24.04`), which ships current
pgvector builds for Postgres 16; then `ALTER EXTENSION vector UPDATE;` and `REINDEX INDEX CONCURRENTLY` each HNSW
index once.

**HNSW, not IVFFlat.** The pgvector README tells you to create IVFFlat "after the table has some data" and to size
`lists` as `rows / 1000`; its centroids are fixed at build time, so recall drifts as data is added and the index
needs periodic rebuilds. HNSW inserts incrementally with no training step, which matches a table that grows a few
rows at a time for ten years. Keep HNSW.

**Dead tuples and recall.** [pgvector#244](https://github.com/pgvector/pgvector/issues/244) (2023) describes HNSW
returning fewer results when the nearest entries are dead tuples from updates and deletes. Two habits keep this
small here: (a) let `todo_ingest.py` and `brain_index.py` update only chunks whose text changed instead of
delete-all-then-insert (the indexer already detects unchanged chunk text for embedding reuse; extend that to the row),
and (b) let autovacuum run; at thousands of rows it finishes in seconds. The README's note "Vacuuming can take a while
for HNSW indexes. Speed it up by reindexing first" is the remedy if a vacuum ever drags.

**The status filter problem (the one that will bite).** With an approximate index, filters apply after the index
scan: "if a condition matches 10% of rows, with HNSW and the default `hnsw.ef_search` of 40, only 4 rows will match on
average" (pgvector 0.8.0 announcement). `match_event` filters `status = 'open'` (unless `include_done`) and
`brain.search` filters `deleted_at IS NULL`. Today most to-dos are open; in five years most will be done, and an
HNSW scan followed by `status = 'open'` would return almost nothing. Options, in order:

1. pgvector 0.8: `SET hnsw.iterative_scan = relaxed_order` (or `strict_order`) for those queries; the scan continues
   until enough rows pass the filter, bounded by `hnsw.max_scan_tuples`.
2. Exact search. pgvector does exact nearest neighbour search when no index is used, with perfect recall. At the
   ten-year size (~150,000 vectors per table) that is a sequential scan of ~250 MB, tens of milliseconds on the box,
   which is fine for a door that answers one person. `match_event` builds its candidates from a `UNION ALL` of three
   joins and orders by distance over that, which very likely runs exactly like this already; confirm with
   `EXPLAIN (ANALYZE, BUFFERS)` on the box.
3. A partial HNSW index on open rows only (the README's advice when "filtering by only a few distinct values"); this
   needs `status` copied onto the chunk tables, so it is the last resort.

**Autovacuum.** Postgres 13 added insert-triggered autovacuum (`autovacuum_vacuum_insert_threshold` 1000,
`autovacuum_vacuum_insert_scale_factor` 0.2), so append-only tables like `todo.history` and `crm.events` get vacuumed
for the visibility map and freezing without any update or delete
([Postgres 16, Routine Vacuuming](https://www.postgresql.org/docs/16/routine-vacuuming.html);
[Laurenz Albe, Cybertec](https://www.cybertec-postgresql.com/en/postgresql-autovacuum-insert-only-tables/), who wrote
the feature). At these row counts the defaults are right; tuning is for tables with tens of millions of rows. Watch
`pg_stat_user_tables.n_dead_tup` and `last_autovacuum` on the chunk tables (section 11).

**Index builds.** "Indexes build significantly faster when the graph fits into `maintenance_work_mem`" (README; the
build emits a NOTICE when it no longer fits). The default is 64 MB. For a rebuild or a new embedding column, run
`SET maintenance_work_mem = '1GB'` in that session (the box has 7.9 GB and runs other services); 0.6.0 and later also
build HNSW in parallel (`max_parallel_maintenance_workers`, 2 by default). Build with `CREATE INDEX CONCURRENTLY` so
the door keeps answering.

## 8. Ranking old and done items down instead of deleting them

**The established shapes.** Search engines have done this for years with decay functions on a date field:
Elasticsearch's `function_score` offers `gauss`, `exp` and `linear` decay with an `origin`, a `scale` and a `decay`
(the score at `scale` distance, default 0.5)
([Elastic docs](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-function-score-query)).
For agent memory specifically, Park et al., [Generative Agents](https://arxiv.org/abs/2304.03442) (UIST 2023), score
each memory as a weighted sum of relevance, recency (exponential decay, factor 0.995 per game hour since last access)
and importance. Both keep everything and let time lower the rank.

**Why this fits:** the owner wants done items to remain findable ("did I already do this?" is exactly what
`include_done` exists for, and `todo_match.py` judges done/moved/none against them), while the daily lanes want open,
recent things first. A multiplier on the score does both without removing a row.

**Concrete proposal for `brain.match_event` and `brain.search`:**

```
final = rrf_score * status_weight * 0.5 ^ (age_days / half_life_days)
```

- `status_weight`: open 1.0, parked 0.8, done 0.5, cancelled 0.3, resolved card 0.5. Applied only when
  `include_done` is true (otherwise done rows are not candidates, as today).
- `age_days` from `updated_at` (to-dos), `resolved_at` or `created_at` (cards), the last CRM event (people: a person
  met three years ago and contacted last week is not old). `brain.pages`: no decay; facts are replaced by
  `superseded_by`, which already ranks them.
- Half-lives as parameters, not constants: cards 30 days, to-dos 180 days, people 365 days. Floor the decay at 0.1 so
  a strong old match still beats a weak new one.
- Keep returning the raw cosine `sim` unchanged: `todo_match.py` gates on `sim >= 0.84` (`match_strong`, auto-adjusted)
  and that gauge must mean the same thing over time.
- Rerank after retrieval: take the top `k * 4` per leg as today, apply the multiplier in the `fused`/`ranked` step.
  Decay inside the ANN scan would need the iterative scan from section 7 and gives no benefit.
- Tune with the simulation (`~/sim`), not by feel: the harness already scores the loops that call `match_event`.

## 9. Embedding model upgrades and re-embedding

Over ten years `intfloat/multilingual-e5-small` (384-d) will be replaced, likely more than once. Vectors from two
models live in different spaces and cannot share an index or be compared, so every model change is a full
re-embedding. The practice that keeps it safe is a shadow column: add the new vector column, write both on insert,
backfill in batches while the old index serves, compare on an evaluation set, cut over, keep the old column until the
new one has proven itself (described by practitioners e.g.
[dbi services, embedding versioning with pgvector](https://www.dbi-services.com/blog/rag-series-embedding-versioning-with-pgvector-why-event-driven-architecture-is-a-precondition-to-ai-data-workflows/)).

**What to do now, cheaply:**

- Never store a vector without its text. Every chunk table already keeps `text`; that is what makes re-embedding
  possible at all. Keep it that way for any new embedded table.
- Record the model per vector: `embedding_model text NOT NULL DEFAULT 'multilingual-e5-small'` on each chunk table
  (or one row in `brain.meta` per table if a table never mixes models). e5 also needs the `query:` / `passage:`
  prefixes; a future model will have its own conventions, which belong next to the model name.
- On upgrade: `ALTER TABLE ... ADD COLUMN embedding_v2 vector(N)` (instant), dual-write in `brain_index.py` /
  `todo_ingest.py`, backfill in batches in the index timer's idle time, `CREATE INDEX CONCURRENTLY` an HNSW on the new
  column, switch `brain.search` / `match_event` behind a parameter, run the simulation on both, then flip. Ten years
  of chunks (~400,000) at the box's measured CPU rate is hours to a day of background work, not a migration project.
- `halfvec` (pgvector 0.7+) halves vector storage with little recall loss; worth considering at the next model
  change, not before (the database is small).

## 10. Backups on one small VPS

**What needs a backup, by phase.** `brain.*` is rebuilt from the repo; `todo.*` is rebuilt from task-land (phase 1);
`crm.people` and friends from `crm.json`. But `todo.history`, `crm.doc_versions`, `crm.events` (the ledger exists on
the laptop too) and resolved `hub.cards` (the hub prunes them after 24 h) already exist only in Postgres. In phase 2
(writers go through the door) and phase 3b (Postgres is the CRM source), the whole database becomes the source.
`DATA-MAP.md` section 4 lists "backup of the Postgres data directory" as open, and the box has no snapshot policy on
record.

**The two methods** ([Postgres 16, Continuous Archiving and PITR](https://www.postgresql.org/docs/16/continuous-archiving.html)):

- `pg_dump` is a logical backup: one file, restorable on a newer major version and on the laptop, but it restores
  to the moment the dump ran, never to one minute before a bad `UPDATE`.
- A base backup plus archived WAL restores to any point in time since the base backup, but only the whole cluster,
  and if archiving fails, "the `pg_wal/` directory will continue to fill with WAL segment files ... (If the file
  system containing `pg_wal/` fills up, PostgreSQL will do a PANIC shutdown.)" On a 96 GB disk shared with
  everything else, that failure mode is real and needs an alarm.

**Tool choice.** pgBackRest was the standard answer for self-hosted PITR; its maintainer announced in April 2026 that
it is no longer maintained ([HN discussion](https://news.ycombinator.com/item?id=47919997), where practitioners point
to WAL-G and Barman, and to Postgres 17's incremental `pg_basebackup`). For a single small server, WAL-G
([github.com/wal-g/wal-g](https://github.com/wal-g/wal-g)) is the fit: one binary used as `archive_command`, writes
compressed base backups and WAL straight to S3-compatible storage, no daemon.

**Recommendation for this box:**

1. Now: a systemd timer (unit in `task-land/_system/vps/`, name in `units.list`) runs `pg_dump -Fc soda` nightly and
   uploads it off the box (the box already runs rclone; any remote that is not the VPS provider). At ~2 GB worst
   case for ten years, keeping a daily dump for 30 days and a monthly dump forever costs little and matches the
   "nothing is lost" rule for backups too. A provider snapshot is a convenience, not a backup: same provider, same
   account.
2. At phase 3b (Postgres becomes the CRM source): add WAL-G with `archive_timeout = 300` so at most five minutes of
   changes can be lost, a weekly base backup, and an alarm on `pg_stat_archiver.failed_count` and on `pg_wal` size
   into the existing `da-alert` path. Keep the nightly `pg_dump` alongside: it is the portable copy and the major
   version upgrade path (Postgres 16 reaches end of life on 9 November 2028,
   [versioning policy](https://www.postgresql.org/support/versioning/), inside the ten years).
3. Always: a monthly restore test (restore the latest dump into a scratch database, compare row counts per table,
   run one `brain.search`), logged like the other health checks. An untested backup is a hope.

## 11. Measure instead of estimate

Run on the box (`psql` as `soda`) to replace the assumptions in section 5 and to watch the indexes over time:

```sql
-- size per table, biggest first (heap + TOAST + indexes)
SELECT n.nspname || '.' || c.relname AS tbl, c.reltuples::bigint AS rows_est,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS total,
       pg_size_pretty(pg_indexes_size(c.oid)) AS indexes
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r' AND n.nspname IN ('brain','crm','todo','hub')
ORDER BY pg_total_relation_size(c.oid) DESC;

-- crm.doc_versions: distinct versions per day and stored bytes per version (the disk question)
SELECT received_at::date AS day, count(*) AS versions,
       pg_size_pretty(avg(pg_column_size(doc))::bigint) AS stored_per_version
FROM crm.doc_versions GROUP BY 1 ORDER BY 1 DESC LIMIT 14;

-- vacuum health of the churny chunk tables and the append-only logs
SELECT schemaname || '.' || relname AS tbl, n_live_tup, n_dead_tup, last_autovacuum, autovacuum_count
FROM pg_stat_user_tables WHERE schemaname IN ('brain','crm','todo','hub') ORDER BY n_dead_tup DESC;

-- pgvector version installed vs available
SELECT extversion FROM pg_extension WHERE extname = 'vector';
SELECT default_version FROM pg_available_extensions WHERE name = 'vector';
```

## 12. Sources

Postgres project:
- Table Partitioning, rule of thumb: https://www.postgresql.org/docs/current/ddl-partitioning.html
- Routine Vacuuming, insert-triggered autovacuum (16): https://www.postgresql.org/docs/16/routine-vacuuming.html
- TOAST (16): https://www.postgresql.org/docs/16/storage-toast.html
- Continuous Archiving and PITR (16): https://www.postgresql.org/docs/16/continuous-archiving.html
- Versioning policy, end-of-life dates: https://www.postgresql.org/support/versioning/
- pgvector 0.8.0 release announcement: https://www.postgresql.org/about/news/pgvector-080-released-2952
- Stephen Frost on when not to partition (pgsql-general, 2018): https://www.postgresql.org/message-id/20181011005157.GD4184%40tamriel.snowman.net

pgvector:
- README (storage sizes, HNSW/IVFFlat, filtering, iterative scans, vacuum): https://github.com/pgvector/pgvector
- CHANGELOG (0.8.3 and 0.8.4 HNSW vacuum fixes): https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md
- Issue #244, HNSW and dead tuples: https://github.com/pgvector/pgvector/issues/244
- Issue #993, `hnsw graph not repaired` under concurrent insert/delete: https://github.com/pgvector/pgvector/issues/993
- Ubuntu 24.04 package (0.6.0): https://packages.ubuntu.com/postgresql-16-pgvector

Engineering posts and papers:
- Martin Fowler, Event Sourcing (2005): https://martinfowler.com/eaaDev/EventSourcing.html
- Brandur Leach, Soft Deletion Probably Isn't Worth It (2022): https://brandur.org/soft-deletion
- Laurenz Albe (Cybertec), autovacuum for insert-only tables: https://www.cybertec-postgresql.com/en/postgresql-autovacuum-insert-only-tables/
- Park et al., Generative Agents (UIST 2023), memory retrieval with recency decay: https://arxiv.org/abs/2304.03442
- Elastic, function score query and decay functions: https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-function-score-query
- dbi services, embedding versioning with pgvector: https://www.dbi-services.com/blog/rag-series-embedding-versioning-with-pgvector-why-event-driven-architecture-is-a-precondition-to-ai-data-workflows/
- WAL-G: https://github.com/wal-g/wal-g

Practitioner discussions:
- HN on soft deletion: https://news.ycombinator.com/item?id=32156009
- HN, "pgBackRest is no longer being maintained" (April 2026) and the alternatives people use: https://news.ycombinator.com/item?id=47919997
