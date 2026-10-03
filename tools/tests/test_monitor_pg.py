"""The monitor migration and PgStore against a real Postgres 16 + pgvector: same contract as MemoryStore.

Database: SODA_TEST_DSN (a throwaway database; the test drops and recreates schema brain in it), else the
`pgserver` package (embedded Postgres, test-only), else skipped. Never point SODA_TEST_DSN at the box."""
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

from monitor.events import Event, Finding, Handle  # noqa: E402
from monitor.store import PgStore  # noqa: E402
from monitor.subscribers import attribution  # noqa: E402

MIGRATION = TOOLS / "migrations" / "001_brain_events.sql"


@pytest.fixture(scope="module")
def dsn():
    if os.environ.get("SODA_TEST_DSN"):
        yield os.environ["SODA_TEST_DSN"]
        return
    try:
        import pgserver
    except ImportError:
        pytest.skip("no SODA_TEST_DSN and pgserver not installed")
    tmp = tempfile.mkdtemp(prefix="soda-pg-monitor-")
    srv = pgserver.get_server(tmp, cleanup_mode="delete")
    try:
        yield srv.get_uri()
    finally:
        srv.cleanup()
        shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(scope="module")
def conn(dsn):
    psycopg = pytest.importorskip("psycopg")
    with psycopg.connect(dsn, autocommit=True) as c:
        c.execute("DROP SCHEMA IF EXISTS brain CASCADE")
        c.execute("CREATE EXTENSION IF NOT EXISTS vector")
        c.execute(MIGRATION.read_text(encoding="utf-8"))
        c.execute(MIGRATION.read_text(encoding="utf-8"))           # idempotent: twice is fine
    c = psycopg.connect(dsn)
    yield c
    c.close()


def _ev(sid, direction="in", person=None, ts=datetime(2026, 9, 29, 10, 0, tzinfo=timezone.utc)):
    return Event("linkedin", sid, "linkedin", direction, ts, f"text {sid}", "2-AAA",
                 (Handle.of("li_thread", "2-AAA"),), "minute", {"k": 1}, person, "route" if person else None)


def test_write_batch_dedupes_and_stores_the_cursor_atomically(conn):
    st = PgStore(conn)
    new = st.write_batch("linkedin", [_ev("a"), _ev("b", "out", "p1"), _ev("a")], {"offset": 10})
    assert [s.event.source_id for s in new] == ["a", "b"]
    assert st.write_batch("linkedin", [_ev("a"), _ev("c")], {"offset": 20})[0].event.source_id == "c"
    assert st.get_cursor("linkedin") == {"offset": 20}
    with pytest.raises(ValueError):
        st.write_batch("linkedin", [Event("gmail:cdtm", "x", "email", "in", datetime.now(timezone.utc))], {"offset": 99})
    assert st.get_cursor("linkedin") == {"offset": 20}               # nothing half-written
    got = st.events_for_person("p1")
    assert len(got) == 1 and got[0].event.handles[0].kind == "li_thread" and got[0].event.data == {"k": 1}


def test_routes_deliveries_findings_and_the_attribution_view(conn):
    st = PgStore(conn)
    h = Handle.of("li_thread", "2-ZZZ")
    st.route_put(h, "p9", "linkedin", "crm")
    st.route_put(h, "p-other", "linkedin", "crm")                    # first writer wins
    assert st.route_get(h) == "p9" and st.routes_for_person("p9")[0]["hits"] == 2
    (s,) = st.write_batch("linkedin", [_ev("z", "out", "p9")], None)
    assert [x.id for x in st.undelivered("sub")] .count(s.id) == 1
    st.record_delivery("sub", s.id, "shadow", "error", {"error": "x"})
    assert s.id in [x.id for x in st.undelivered("sub")]
    st.record_delivery("sub", s.id, "shadow", "ok", {})
    assert s.id not in [x.id for x in st.undelivered("sub")]
    f = Finding("hub", "card-2", "done", s.id, "his reply")
    assert st.record_finding("A", "sub", "shadow", f) is True
    assert st.record_finding("A", "sub", "shadow", f) is False
    assert st.record_finding("B", "sweep", "shadow", f) is True
    assert st.record_finding("B", "sweep", "shadow", Finding("todo", "t1", "done", None, "status")) is True
    assert st.record_finding("B", "sweep", "shadow", Finding("todo", "t1", "done", None, "status")) is False
    rows = {r["item_id"]: r for r in attribution(st)}
    assert rows["card-2"]["first_path"] == "A" and rows["card-2"]["other_path_also"] is True
    with conn.cursor() as cur:
        cur.execute("SELECT first_path, other_path_also FROM brain.event_attribution WHERE item_id = 'card-2'")
        assert cur.fetchone() == ("A", True)
    conn.commit()
