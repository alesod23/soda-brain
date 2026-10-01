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
