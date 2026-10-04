# SODA BRAIN door (`soda-brain/tools/`)

One Python service that owns a Postgres 16 + pgvector database on the box and serves it to Claude Code
(MCP) and to any orchestrator (HTTP). The repo is the brain's content (`memory/`, `system/`, `handoffs/`);
this folder is the code. Written and tested on the laptop on 2026-10-01; the box install is run by the owner.

## What runs where

| Where | What | How |
|---|---|---|
| box, `postgresql.service` | Postgres 16 + pgvector 0.6, `listen_addresses=localhost`, db `soda`, role `soda` | apt, `box-install.sh` |
| box, `da-brain.service` | `brain_serve.py --host 100.85.52.84 --port 4150` (FastAPI + MCP at `/mcp`), `User=da`, `Restart=always` | unit in `task-land/_system/vps/` |
| box, `da-brain-index.timer` | `brain_index.py` every 5 min (OnBootSec 2 min): re-indexes only what changed | unit + timer in `task-land/_system/vps/` |
| box, `/home/da/brain/venv` | the Python 3.12 venv, pinned by `requirements.txt`; never inside a repo | `box-install.sh` |
| box, `da-repo-sync@soda-brain.timer` | pulls this repo every 5 min (already in `units.list`) | existing |
| laptop | tests (`tests/`), venv `C:/Users/Alessandro/.venvs/brain`, Claude Code attaching over Tailscale | see below |

Data flow: markdown on disk -> `brain_index.py` -> `brain.pages` / `brain.chunks` (384-d embeddings,
`intfloat/multilingual-e5-small`, CPU) -> `brain.search()` (vector top-k + full-text top-k, reciprocal rank
fusion) -> `/brain/recall` and the MCP `recall` tool. The CRM document (`crm.json`) is pushed whole to
`/crm/put`; the service stores the version and upserts only the records whose sha changed.

## Env file (never in a repo)

`/home/da/.env/soda.env` on the box (`~/.env/soda.env` on the laptop for local runs), mode 0600, owner `da`.
`brain_index.py` and `brain_serve.py` read it when present; existing environment variables win.

```
SODA_DB_PASSWORD=<hex>
SODA_TOKEN=<hex>
SODA_DB_DSN=postgresql://soda:<password>@127.0.0.1/soda
```

Optional: `BRAIN_REPO` (repo root, default: parent of `tools/`), `BRAIN_SOURCES` (`kind=glob,...`, kinds
`memory|system|handoff|rule|hint|other`), `BRAIN_MODEL`, `BRAIN_CHUNK_TOKENS` (default 400), `BRAIN_CHUNK_OVERLAP` (50).

Generate the two secrets without printing them (as `da`, on the box):

```
mkdir -p -m 700 ~/.env
bash -c 'PW=$(openssl rand -hex 24); TK=$(openssl rand -hex 32); umask 077; printf "SODA_DB_PASSWORD=%s\nSODA_TOKEN=%s\nSODA_DB_DSN=postgresql://soda:%s@127.0.0.1/soda\n" "$PW" "$TK" "$PW" > ~/.env/soda.env'
chmod 600 ~/.env/soda.env
```

## Box install

```
sudo bash /home/da/soda-brain/tools/box-install.sh
```

Idempotent. Aborts with the commands above if the env file is missing. Does, in order: apt
`postgresql postgresql-16-pgvector python3-venv`; `listen_addresses=localhost`; role + database `soda`
(password from the env file, re-applied on every run); `CREATE EXTENSION vector` as postgres; `schema.sql`
as `soda` over TCP (proves the DSN); venv at `/home/da/brain/venv` with `requirements.txt`; caches the model;
installs `da-brain.service`, `da-brain-index.service`, `da-brain-index.timer` from
`/home/da/task-land/_system/vps/`; `daemon-reload`, enable, start; runs the first index; prints `/health`.

## Routes (HTTP, port 4150 on the Tailscale IP)

Auth: header `X-Soda-Token: <SODA_TOKEN>` on every route except `GET /health`; requests from loopback are
exempt (the box's own cron and the laptop test). Without `SODA_TOKEN` in the environment every remote request
is refused.

| Route | What |
|---|---|
| `GET /health` | `{ok, db, pages, chunks, people, last_index_at}` |
| `POST /brain/recall {query, k=8}` | hybrid search: `[{path, title, ord, text, score, kind, since, superseded_by}]` |
| `POST /brain/rules {topic, k=10, ledger?}` | what he likes and dislikes about a topic, from his seven ledgers only: `{liked: [...], rules: [...]}`, each `{ledger, rule, text, his_words, source, soft, confirmed, score, path}` (4 Oct 2026, RULE-LOOP template part 6; MCP tool `his_rules`) |
| `POST /brain/match {text, k=8, include_done=false}` | S10: the nearest to-dos (`kind todo`, task-land rows and sub-items `<slug>#<n>`) and CRM people (`kind person`) for an event or a proposed step, k per kind, to-dos first: `[{kind, id, parent_id, title, text, status, due, score}]`; read-only token allowed; MCP tool `match_event` |
| `GET /brain/page?path=memory/x.md` | the page body and fields |
| `POST /brain/reindex` | runs the indexer in a background thread, `{started}` (`{started:false, running:true}` while one runs) |
| `POST /crm/put {source, at, sha, doc}` | stores the doc version (same sha -> `{ok, version, unchanged:true}`), diffs per record, upserts changed, soft-deletes missing, writes meta; `{ok, version, changed:{companies,people,templates,signals}, deleted:{...}}` |
| `POST /crm/events {lines:[{source,id,at,kind,channel,direction,person_id,...}]}` | `ON CONFLICT (source,id) DO NOTHING`; `{inserted, skipped}` |
| `GET /crm/doc` | the latest stored document (`{id, sha, source, received_at, doc}`) |
| `GET /crm/person/{id}` | the person row (+ `company` name) |
| `GET /crm/company/{id}` | the company with its people |
| `GET /crm/people?q=&stage=&due_before=&limit=50` | `q` ilike on name / email / company; `due_before` = next step due on or before (ISO date) |
| `GET /crm/changes?since=<iso>` | companies, people, templates, signals updated after `since` |

MCP (streamable HTTP) at `/mcp`, same token header; tools `recall(query, k)`, `what_is_true(topic)`
(recall grouped by page, newest non-superseded page first, with `since` dates), `page(path)`,
`crm_person(id)`, `crm_search(q, stage, due_before, limit)`.

Record keys in `crm.*`: a company's `id`, a person's `id`; the real document has three people without an id
(key becomes `<company_id>/<slug(name)>`) and one repeated person id and company id (second occurrence gets
`#2`). Keys are stable across pushes because they follow document order.

## Attaching a laptop Claude Code (per session, never global)

```
claude mcp add --transport http brain http://100.85.52.84:4150/mcp --header "X-Soda-Token: <SODA_TOKEN>"
```

Per session only (`cc-with` style, see memory `feedback_mcp_per_session_not_global`): the token is a secret
and the box is reachable only over Tailscale. Local alternative with a laptop Postgres:
`brain_serve.py --stdio` exposes the same five tools over stdio (`claude mcp add brain -- <venv>/python brain_serve.py --stdio`).

How instinct (the cloud orchestrator) attaches later: the same HTTP door, the same `X-Soda-Token`, behind
HTTPS (a reverse proxy or Tailscale Funnel in front of :4150). Not built; nothing in this folder changes for it.

## Re-index

- automatic: `da-brain-index.timer` every 5 min; a page whose sha is unchanged costs one row lookup, nothing else
- by hand on the box: `/home/da/brain/venv/bin/python /home/da/soda-brain/tools/brain_index.py` (`--dry-run` prints
  the plan: files, changed, chunks; `--stats` prints counts)
- over HTTP: `curl -X POST -H "X-Soda-Token: ..." http://100.85.52.84:4150/brain/reindex`

Sources on the box: `memory/*.md` (kind memory), `system/*.md` (system), `handoffs/*.md` (handoff),
`/home/da/task-land/_system/*-CONTRACT.md` (rule: one page per `| H<n> | ... |` row plus one for the prose),
`/home/da/task-land/_system/hints/*.md` (hint). Page `path` is repo-relative (`memory/x.md`) or absolute for
task-land files (`/home/da/task-land/_system/HUB-CARD-CONTRACT.md#H1`). Frontmatter read: `name`,
`description`, `metadata.type`, `since`, `superseded_by`, `checked_last` (top level or under `metadata`).

Chunking: by heading first, then packed to about 400 estimated model tokens (about 170-250 words) with a
50-token overlap. The brief said 600 words; measured on the 351 memory pages, 68% of 600-word chunks exceed the
model's 512-token window (median 670 tokens), so the vector leg would not see their second half. At 400 the
measured median is 393 real tokens, p90 483, 4.4% over. `BRAIN_CHUNK_TOKENS=` changes it.

## Verify

```
curl -s http://100.85.52.84:4150/health
curl -s -X POST -H "X-Soda-Token: $T" -H "content-type: application/json" \
     -d '{"query":"how are hub cards sent","k":3}' http://100.85.52.84:4150/brain/recall
/home/da/brain/venv/bin/python /home/da/soda-brain/tools/brain_index.py --stats
systemctl status da-brain da-brain-index.timer; journalctl -u da-brain -n 30
```

Laptop tests (`C:/Users/Alessandro/.venvs/brain`):

```
cd C:/Users/Alessandro/soda-brain/tools
C:/Users/Alessandro/.venvs/brain/Scripts/python -m pytest -p no:cacheprovider -q tests
```

`tests/test_index.py`, `tests/test_crm_diff.py` and `tests/test_monitor.py` need no database.
`tests/test_monitor_pg.py` runs the monitor layer's migration (`migrations/001_brain_events.sql`, SKELETON, not
applied on the box) and `monitor.store.PgStore` against `SODA_TEST_DSN` or `pgserver`; design in `docs/MONITOR-LAYER.md`. `tests/test_integration.py` needs one:
`SODA_TEST_DSN`, else Docker Desktop (`pgvector/pgvector:pg16` on 55432, removed afterwards), else the
`pgserver` package (embedded Postgres 16 with pgvector, test-only, not in `requirements.txt`), else it skips.
It indexes `memory/` with the real model, starts the service on 127.0.0.1:4150, pushes the laptop's real
`~/.medtech-crm/crm.json` read-only (expects 441 companies, 626 people) and drives the MCP door with the
official client. `tests/conftest.py` holds a laptop-only shim: Windows Application Control blocks psycopg's
binary `pq.pyd`, so the tests use psycopg's pure-Python mode with the `libpq.dll` that ships inside `pgserver`.
