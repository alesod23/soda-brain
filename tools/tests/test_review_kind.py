"""G12 (4 Oct 2026): CRM review items are rows of the brain with their own kind `review` in brain.match_event.

A temp Postgres (SODA_TEST_DSN, else pgserver in a temp dir; never the live index), the real schema.sql applied twice
(idempotent on a fresh database), a fixture review board, a bag-of-words stand-in for the embedder. Checks: an event
about a person with an open review item returns a `review` hit for that pid; a dealt item only with include_done; a
second identical pass changes nothing; an item that left the board becomes `gone` (row kept); an unreachable board
changes nothing."""
import hashlib
import math
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import todo_ingest as ti  # noqa: E402


def embed(texts):
    """Hashed bag of words, 384 dims, unit length: two texts sharing words are near each other."""
    out = []
    for t in texts:
        v = [0.0] * 384
        for w in re.findall(r"[a-z]{3,}", t.lower()):
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 384] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        out.append([x / n for x in v])
    return out


def item(pid, name, kind, step_text, date, dealt=None, draft=None, org=""):
    return {"pid": pid, "name": name, "org": org, "kind": kind, "dealt": dealt, "channel": "email", "waiting": None,
            "commented": None, "work_job": None,
            "step": {"text": step_text, "date": date, "overdue": 0, "channel": "email", "who_owes": "him"},
            "review": {"versions": 1 if draft else 0,
                       "current": {"v": 1, "at": "2026-10-04T10:00:00Z", "subject": "Piacere di conoscerla a Siena", "text": draft} if draft else None}}


BOARD = [
    item("severi-unibo", "Stefano Severi", "coming", "send Stefano the saved light nudge in the 'Piacere di conoscerla a "
         "Siena' thread, recalling the introductions to ASL Romagna and Prof. Corsi", "2026-10-05",
         draft="Gentile Professore, le riscrivo dopo Siena", org="Universita di Bologna"),
    item("andria-davis", "Andria Davis", "due", "Send Andria one short follow-up email as a reply in the thread", "2026-10-04"),
    item("lucas", "Lucas Meyer", "reply", "answer Lucas (WhatsApp)", "2026-10-04"),
    item("giancarlo-conti", "Giancarlo Conti", "done", "call Giancarlo about the pilot", "2026-10-04",
         dealt={"kind": "approve", "at": "2026-10-04T09:00:00Z", "day": "2026-10-04", "sent": True}),
]


@pytest.fixture(scope="module")
def conn():
    import psycopg
    srv = tmp = None
    dsn = os.environ.get("SODA_TEST_DSN")
    if not dsn:
        try:
            import pgserver
        except ImportError:
            pytest.skip("no SODA_TEST_DSN and pgserver not installed")
        tmp = tempfile.mkdtemp(prefix="soda-pg-g12-")
        srv = pgserver.get_server(tmp, cleanup_mode="delete")
        dsn = srv.get_uri()
    with psycopg.connect(dsn, autocommit=True) as c:
        c.execute("DROP SCHEMA IF EXISTS brain CASCADE; DROP SCHEMA IF EXISTS crm CASCADE; "
                  "DROP SCHEMA IF EXISTS todo CASCADE; DROP SCHEMA IF EXISTS hub CASCADE")
        c.execute("CREATE EXTENSION IF NOT EXISTS vector")
        sql = (TOOLS / "schema.sql").read_text(encoding="utf-8")
        c.execute(sql)
        c.execute(sql)   # idempotent: twice is fine
    c = psycopg.connect(dsn)
    try:
        yield c
    finally:
        c.close()
        if srv:
            srv.cleanup()
            shutil.rmtree(tmp, ignore_errors=True)


def match(conn, text, include_done=False, k=8):
    cur = conn.execute("SELECT kind, id, parent_id, title, text, status, due, score, sim "
                       "FROM brain.match_event(%s, %s::vector, %s, %s)", [text, embed([text])[0], k, include_done])
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def test_review_rows_and_match(conn):
    s1 = ti.upsert_reviews(conn, embed, items=BOARD)
    assert s1 == {"items": 4, "open": 3, "changed": 4, "gone": 0}, s1
    rows = {r[0]: r[1:] for r in conn.execute("SELECT pid, kind, status, step_text, version_head FROM crm.review_items")}
    assert rows["lucas"][:2] == ("owed", "open")               # the board's reply = a reply he owes
    assert rows["giancarlo-conti"][:2] == ("done", "dealt")
    assert rows["severi-unibo"][0] == "coming" and "Piacere di conoscerla" in rows["severi-unibo"][2]
    assert rows["severi-unibo"][3].startswith("subject: Piacere di conoscerla a Siena")

    # an event about Stefano Severi -> a `review` hit for his pid, open, kind and step date carried
    hits = match(conn, "Email from Stefano Severi (Bologna): thanks for the introductions to ASL Romagna, happy to talk next week")
    rev = [h for h in hits if h["kind"] == "review"]
    assert rev and rev[0]["id"] == "severi-unibo", hits
    assert rev[0]["status"] == "open" and rev[0]["parent_id"] == "coming" and str(rev[0]["due"]) == "2026-10-05"
    assert rev[0]["title"] == "Stefano Severi" and rev[0]["sim"] is not None
    print("[G12] review hit:", {k: rev[0][k] for k in ("kind", "id", "parent_id", "status", "due", "score", "sim")})

    # a dealt item is not an open review item: only include_done returns it
    q = "Giancarlo Conti called about the pilot"
    assert not [h for h in match(conn, q) if h["kind"] == "review" and h["id"] == "giancarlo-conti"]
    assert [h for h in match(conn, q, include_done=True) if h["kind"] == "review" and h["id"] == "giancarlo-conti"][0]["status"] == "dealt"


def test_idempotent_gone_and_unreachable(conn):
    ti.upsert_reviews(conn, embed, items=BOARD)
    assert ti.upsert_reviews(conn, embed, items=BOARD)["changed"] == 0          # same board: nothing written
    s = ti.upsert_reviews(conn, embed, items=[x for x in BOARD if x["pid"] != "andria-davis"])
    assert s["gone"] == 1
    assert conn.execute("SELECT status FROM crm.review_items WHERE pid = 'andria-davis'").fetchone()[0] == "gone"   # row kept
    assert not [h for h in match(conn, "Andria Davis follow-up email reply", include_done=True) if h["kind"] == "review" and h["id"] == "andria-davis"]
    s = ti.upsert_reviews(conn, embed, url="http://127.0.0.1:9/review/items")   # nothing listens on port 9
    assert "skipped" in s
    assert conn.execute("SELECT count(*) FROM crm.review_items WHERE status = 'gone'").fetchone()[0] == 1
    # back on the board -> open again
    assert ti.upsert_reviews(conn, embed, items=BOARD)["changed"] == 1
    assert conn.execute("SELECT status FROM crm.review_items WHERE pid = 'andria-davis'").fetchone()[0] == "open"
