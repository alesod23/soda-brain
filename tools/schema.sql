-- SODA BRAIN schema. Postgres 16 + pgvector. Idempotent: safe to apply on every install.
-- Applied by box-install.sh as the `soda` role (the extension is created by the postgres
-- superuser first; the line below is then a no-op NOTICE).

CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS brain;
CREATE SCHEMA IF NOT EXISTS crm;

-- ---------------------------------------------------------------- brain

CREATE TABLE IF NOT EXISTS brain.pages (
    id            bigserial PRIMARY KEY,
    path          text        NOT NULL UNIQUE,
    kind          text        NOT NULL CHECK (kind IN ('memory','system','handoff','rule','hint','other')),
    title         text,
    description   text,
    type          text,                     -- frontmatter metadata.type (feedback | reference | project | user ...)
    since         date,
    superseded_by text,
    checked_last  date,
    sha           text        NOT NULL,
    body          text        NOT NULL,
    updated_at    timestamptz NOT NULL DEFAULT now(),
    deleted_at    timestamptz
);

CREATE TABLE IF NOT EXISTS brain.chunks (
    id        bigserial PRIMARY KEY,
    page_id   bigint   NOT NULL REFERENCES brain.pages(id) ON DELETE CASCADE,
    ord       int      NOT NULL,
    text      text     NOT NULL,
    tsv       tsvector GENERATED ALWAYS AS (to_tsvector('english', text)) STORED,
    embedding vector(384),
    UNIQUE (page_id, ord)
);

-- the UNIQUE on pages.path already is a btree; this named one keeps the brief's index explicit
CREATE INDEX IF NOT EXISTS pages_path_idx       ON brain.pages (path);
CREATE INDEX IF NOT EXISTS pages_kind_idx       ON brain.pages (kind) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS chunks_page_idx      ON brain.chunks (page_id);
CREATE INDEX IF NOT EXISTS chunks_tsv_gin       ON brain.chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw ON brain.chunks USING hnsw (embedding vector_cosine_ops);

-- small key/value store: last_index_at and friends
CREATE TABLE IF NOT EXISTS brain.meta (
    k text PRIMARY KEY,
    v jsonb NOT NULL
);

-- Hybrid retrieval: vector top-k and full-text top-k fused by reciprocal rank fusion (RRF, k=60).
-- q_emb may be NULL (no model loaded): then only the full-text leg contributes.
-- q may be empty: then only the vector leg contributes.
CREATE OR REPLACE FUNCTION brain.search(q text, q_emb vector(384), k int DEFAULT 8)
RETURNS TABLE (
    path text, title text, ord int, text text, score double precision,
    kind text, since date, superseded_by text
)
LANGUAGE sql STABLE AS $$
WITH params AS (
    SELECT GREATEST(k, 1) AS k,
           CASE WHEN coalesce(q, '') = '' THEN NULL ELSE websearch_to_tsquery('english', q) END AS tsq
),
vec AS (
    SELECT c.id, row_number() OVER (ORDER BY c.embedding <=> q_emb) AS r
    FROM brain.chunks c
    JOIN brain.pages p ON p.id = c.page_id
    WHERE q_emb IS NOT NULL AND p.deleted_at IS NULL AND c.embedding IS NOT NULL
    ORDER BY c.embedding <=> q_emb
    LIMIT (SELECT k * 4 FROM params)
),
ts AS (
    SELECT c.id, row_number() OVER (ORDER BY ts_rank_cd(c.tsv, (SELECT tsq FROM params)) DESC) AS r
    FROM brain.chunks c
    JOIN brain.pages p ON p.id = c.page_id
    WHERE (SELECT tsq FROM params) IS NOT NULL
      AND p.deleted_at IS NULL
      AND c.tsv @@ (SELECT tsq FROM params)
    ORDER BY ts_rank_cd(c.tsv, (SELECT tsq FROM params)) DESC
    LIMIT (SELECT k * 4 FROM params)
),
fused AS (
    SELECT id, SUM(1.0 / (60 + r)) AS score
    FROM (SELECT id, r FROM vec UNION ALL SELECT id, r FROM ts) u
    GROUP BY id
)
SELECT p.path, p.title, c.ord, c.text, f.score::double precision, p.kind, p.since, p.superseded_by
FROM fused f
JOIN brain.chunks c ON c.id = f.id
JOIN brain.pages  p ON p.id = c.page_id
ORDER BY f.score DESC, p.path, c.ord
LIMIT (SELECT k FROM params);
$$;

-- ---------------------------------------------------------------- crm

CREATE TABLE IF NOT EXISTS crm.doc_versions (
    id          bigserial   PRIMARY KEY,
    sha         text        NOT NULL UNIQUE,
    source      text        NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    doc         jsonb       NOT NULL
);

CREATE TABLE IF NOT EXISTS crm.companies (
    id         text        PRIMARY KEY,
    name       text,
    data       jsonb       NOT NULL,
    sha        text        NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE IF NOT EXISTS crm.people (
    id             text        PRIMARY KEY,
    company_id     text        REFERENCES crm.companies(id),
    name           text,
    email          text,
    linkedin       text,
    stage          text,
    next_step_date date,
    next_step_text text,
    data           jsonb       NOT NULL,
    sha            text        NOT NULL,
    updated_at     timestamptz NOT NULL DEFAULT now(),
    deleted_at     timestamptz
);

CREATE TABLE IF NOT EXISTS crm.templates (
    id   text  PRIMARY KEY,
    data jsonb NOT NULL,
    sha  text  NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE IF NOT EXISTS crm.signals (
    id   text  PRIMARY KEY,
    data jsonb NOT NULL,
    sha  text  NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE IF NOT EXISTS crm.meta (
    k text  PRIMARY KEY,
    v jsonb
);

CREATE TABLE IF NOT EXISTS crm.events (
    source    text        NOT NULL,
    id        text        NOT NULL,
    at        timestamptz,
    kind      text,
    channel   text,
    direction text,
    person_id text,
    data      jsonb       NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (source, id)
);

CREATE INDEX IF NOT EXISTS people_email_idx      ON crm.people (email);
CREATE INDEX IF NOT EXISTS people_linkedin_idx   ON crm.people (linkedin);
CREATE INDEX IF NOT EXISTS people_stage_idx      ON crm.people (stage);
CREATE INDEX IF NOT EXISTS people_next_step_idx  ON crm.people (next_step_date);
CREATE INDEX IF NOT EXISTS people_company_idx    ON crm.people (company_id);
CREATE INDEX IF NOT EXISTS people_updated_idx    ON crm.people (updated_at);
CREATE INDEX IF NOT EXISTS companies_updated_idx ON crm.companies (updated_at);
CREATE INDEX IF NOT EXISTS events_at_idx         ON crm.events (at);
CREATE INDEX IF NOT EXISTS events_person_idx     ON crm.events (person_id);

-- ---------------------------------------------------------------- todo (S10, 2026-10-03)
-- The to-do is a first-class row of the brain; the task-land files are the view (phase 1: mirrored by
-- todo_ingest.py on the index timer). Done is a state with evidence and a date, never a delete; deleted_at
-- only marks a file that vanished from task-land, and the row stays.

CREATE SCHEMA IF NOT EXISTS todo;

CREATE TABLE IF NOT EXISTS todo.items (
    id            text        PRIMARY KEY,                 -- the task slug; a sub-item is <slug>#<n>
    parent_id     text        REFERENCES todo.items(id) ON DELETE CASCADE,
    title         text        NOT NULL,
    body          text,                                    -- the notes (never rendered on the page)
    project       text,
    bucket        text,
    status        text        NOT NULL DEFAULT 'open' CHECK (status IN ('open','done','cancelled','parked')),
    stage         text,                                    -- created | in_progress | ready_for_review | finished
    due           date,
    surface_on    date,
    contact_id    text,                                    -- crm.people.id when the task names a person
    hub_card      text,
    source        text,                                    -- capture | intake | coattio | notion | janitor | brain | manual
    origin_path   text,                                    -- Tasks/<dir>/<slug>.md
    sha           text,
    created_at    timestamptz,
    updated_at    timestamptz NOT NULL DEFAULT now(),
    done_at       timestamptz,
    done_evidence jsonb,                                   -- {by, source, quote, at}
    data          jsonb       NOT NULL DEFAULT '{}'::jsonb, -- the rest of the frontmatter
    deleted_at    timestamptz
);

CREATE TABLE IF NOT EXISTS todo.links (
    id      bigserial   PRIMARY KEY,
    item_id text        NOT NULL REFERENCES todo.items(id) ON DELETE CASCADE,
    kind    text        NOT NULL,                          -- person | meeting | thread | calendar_event | notion_page | hub_card | parent
    ref     text        NOT NULL,
    data    jsonb       NOT NULL DEFAULT '{}'::jsonb,
    at      timestamptz NOT NULL DEFAULT now(),
    UNIQUE (item_id, kind, ref)
);

CREATE TABLE IF NOT EXISTS todo.history (                 -- append-only: every change, with its evidence
    id       bigserial   PRIMARY KEY,
    item_id  text        NOT NULL REFERENCES todo.items(id) ON DELETE CASCADE,
    at       timestamptz NOT NULL DEFAULT now(),
    by       text        NOT NULL,                         -- ingest | brain | janitor | him | pipeline
    change   jsonb       NOT NULL,
    evidence jsonb
);

CREATE TABLE IF NOT EXISTS todo.chunks (
    id        bigserial PRIMARY KEY,
    item_id   text      NOT NULL REFERENCES todo.items(id) ON DELETE CASCADE,
    ord       int       NOT NULL,
    text      text      NOT NULL,
    tsv       tsvector  GENERATED ALWAYS AS (to_tsvector('english', text)) STORED,
    embedding vector(384),
    UNIQUE (item_id, ord)
);

CREATE INDEX IF NOT EXISTS todo_items_status_idx  ON todo.items (status) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS todo_items_due_idx     ON todo.items (due);
CREATE INDEX IF NOT EXISTS todo_items_contact_idx ON todo.items (contact_id);
CREATE INDEX IF NOT EXISTS todo_items_parent_idx  ON todo.items (parent_id);
CREATE INDEX IF NOT EXISTS todo_history_item_idx  ON todo.history (item_id, at);
CREATE INDEX IF NOT EXISTS todo_links_item_idx    ON todo.links (item_id);
CREATE INDEX IF NOT EXISTS todo_chunks_tsv_gin    ON todo.chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS todo_chunks_embedding_hnsw ON todo.chunks USING hnsw (embedding vector_cosine_ops);

-- CRM people get a vector too (one chunk per person: name, company, role, step, loops, facts), so an
-- event can find a person by meaning, not only by ilike.
CREATE TABLE IF NOT EXISTS crm.people_chunks (
    id        bigserial PRIMARY KEY,
    person_id text      NOT NULL REFERENCES crm.people(id) ON DELETE CASCADE,
    ord       int       NOT NULL,
    sha       text      NOT NULL,
    text      text      NOT NULL,
    tsv       tsvector  GENERATED ALWAYS AS (to_tsvector('english', text)) STORED,
    embedding vector(384),
    UNIQUE (person_id, ord)
);
CREATE INDEX IF NOT EXISTS people_chunks_tsv_gin ON crm.people_chunks USING gin (tsv);
CREATE INDEX IF NOT EXISTS people_chunks_embedding_hnsw ON crm.people_chunks USING hnsw (embedding vector_cosine_ops);

-- An event (a mail, a calendar change, a Notion note, a verdict) finds the nearest open to-dos and CRM people:
-- the same RRF as brain.search over todo.chunks and crm.people_chunks. include_done = true also returns done
-- items (ranked by the same score, status says so): "did I already do this?".
CREATE OR REPLACE FUNCTION brain.match_event(q text, q_emb vector(384), k int DEFAULT 8, include_done boolean DEFAULT false)
RETURNS TABLE (
    kind text, id text, parent_id text, title text, text text, status text, due date, score double precision
)
LANGUAGE sql STABLE AS $$
WITH params AS (
    SELECT GREATEST(k, 1) AS k,
           CASE WHEN coalesce(q, '') = '' THEN NULL ELSE websearch_to_tsquery('english', q) END AS tsq
),
cand AS (
    SELECT 'todo'::text AS kind, c.id AS cid, i.id, i.parent_id, i.title, c.text, i.status, i.due, c.embedding, c.tsv
    FROM todo.chunks c JOIN todo.items i ON i.id = c.item_id
    WHERE i.deleted_at IS NULL AND (include_done OR i.status = 'open')
    UNION ALL
    SELECT 'person'::text, c.id, p.id, NULL::text, p.name, c.text, p.stage, p.next_step_date, c.embedding, c.tsv
    FROM crm.people_chunks c JOIN crm.people p ON p.id = c.person_id
    WHERE p.deleted_at IS NULL
),
vec AS (
    SELECT kind, cid, row_number() OVER (ORDER BY embedding <=> q_emb) AS r
    FROM cand WHERE q_emb IS NOT NULL AND embedding IS NOT NULL
    ORDER BY embedding <=> q_emb
    LIMIT (SELECT k * 4 FROM params)
),
ts AS (
    SELECT kind, cid, row_number() OVER (ORDER BY ts_rank_cd(tsv, (SELECT tsq FROM params)) DESC) AS r
    FROM cand WHERE (SELECT tsq FROM params) IS NOT NULL AND tsv @@ (SELECT tsq FROM params)
    ORDER BY ts_rank_cd(tsv, (SELECT tsq FROM params)) DESC
    LIMIT (SELECT k * 4 FROM params)
),
fused AS (
    SELECT kind, cid, SUM(1.0 / (60 + r)) AS score
    FROM (SELECT kind, cid, r FROM vec UNION ALL SELECT kind, cid, r FROM ts) u
    GROUP BY kind, cid
),
ranked AS (                    -- k per kind: 641 people never crowd the to-dos out of the answer
    SELECT c.kind, c.id, c.parent_id, c.title, c.text, c.status, c.due, f.score::double precision AS score,
           row_number() OVER (PARTITION BY c.kind ORDER BY f.score DESC, c.id) AS rk
    FROM fused f JOIN cand c ON c.kind = f.kind AND c.cid = f.cid
)
SELECT kind, id, parent_id, title, text, status, due, score
FROM ranked WHERE rk <= (SELECT k FROM params)
ORDER BY kind DESC, score DESC;   -- 'todo' rows first, then 'person'
$$;
