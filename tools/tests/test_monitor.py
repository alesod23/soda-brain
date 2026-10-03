"""Unit tests for the monitor layer skeleton (tools/monitor/). No database, no network, fixture data only.
The fixture people are fictional. The Postgres contract test lives in test_monitor_pg.py."""
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from monitor.adapters.linkedin_store import LinkedInStoreAdapter  # noqa: E402
from monitor.events import Event, Finding, Handle, norm_handle  # noqa: E402
from monitor.ingest import Resolver, backfill_person, resolve_backlog, run_once  # noqa: E402
from monitor.store import MemoryStore  # noqa: E402
from monitor.subscribers import (Dispatcher, OpenItem, Result, attribution, attribution_report,  # noqa: E402
                                 sweep)

FIXTURE = Path(__file__).parent / "fixtures" / "linkedin-store.sample.jsonl"
CRM = [
    {"id": "p-giulia", "name": "Giulia Ferri", "linkedin": "https://www.linkedin.com/in/Giulia-Ferri-Example?trk=x"},
    {"id": "p-marco", "name": "Marco Bellini", "email": "marco@example.org"},
]
NOW = datetime(2026, 10, 2, 12, 0, tzinfo=timezone.utc)


@pytest.fixture()
def store_file(tmp_path):
    p = tmp_path / "linkedin-store.jsonl"
    shutil.copy(FIXTURE, p)
    return p


def _ev(**kw):
    base = dict(source="test", source_id="1", channel="email", direction="in", ts=NOW, text="hello")
    base.update(kw)
    return Event(**base)


# ------------------------------------------------------------------ events

def test_handles_normalise_to_one_spelling():
    assert norm_handle("email", "Marco Bellini <Marco@Example.org>") == "marco@example.org"
    assert norm_handle("phone", "+39 333 123 4567") == norm_handle("phone", "393331234567@s.whatsapp.net") == "393331234567"
    assert norm_handle("phone", "0039 333 1234567") == "393331234567"
    assert norm_handle("linkedin", "https://www.linkedin.com/in/Giulia-Ferri-Example/?trk=x") == "in/giulia-ferri-example"
    assert Handle.of("email", "no address here") is None
    with pytest.raises(ValueError):
        Handle.of("fax", "1")


def test_event_rejects_what_the_table_would_reject():
    with pytest.raises(ValueError):
        _ev(channel="sms")
    with pytest.raises(ValueError):
        _ev(direction="sideways")
    with pytest.raises(ValueError):
        _ev(ts=datetime(2026, 10, 2, 12, 0))          # naive
    with pytest.raises(ValueError):
        _ev(source_id="")
    assert len(_ev(text="x" * 20000).text) == 8000


# ------------------------------------------------------------------ the reference adapter

def test_adapter_reads_both_directions_and_skips_junk(store_file):
    events, cursor = LinkedInStoreAdapter(store_file).fetch(None)
    assert [e.source_id for e in events] == ["li:2-AAA:0001", "li:2-AAA:0002", "li:2-BBB:0001", "li:2-AAA:0001"]
    out = [e for e in events if e.direction == "out"]
    assert len(out) == 1 and out[0].text.startswith("Va bene")          # his own reply is an event (HANDOFF 6d)
    assert events[2].ts_precision == "day"
    assert events[0].ts == datetime(2026, 9, 27, 16, 4, tzinfo=timezone.utc)   # message time, not the poll time
    assert cursor["offset"] == store_file.stat().st_size


def test_adapter_is_incremental_and_waits_for_a_torn_last_line(store_file):
    a = LinkedInStoreAdapter(store_file)
    _, c1 = a.fetch(None)
    assert a.fetch(c1)[0] == []
    with open(store_file, "a", encoding="utf-8") as f:
        f.write('{"id": "li:2-BBB:0002", "ts": "2026-10-01T10:00:00+02:00", "chatId": "2-BBB", "text": "half')
    ev2, c2 = a.fetch(c1)
    assert ev2 == [] and c2["offset"] == c1["offset"]                  # incomplete line not consumed
    with open(store_file, "a", encoding="utf-8") as f:
        f.write(' written", "fromMe": true}\n')
    ev3, _ = a.fetch(c2)
    assert [e.source_id for e in ev3] == ["li:2-BBB:0002"] and ev3[0].direction == "out"


def test_adapter_rereads_a_rewritten_file(store_file):
    a = LinkedInStoreAdapter(store_file)
    _, c1 = a.fetch(None)
    lines = store_file.read_text(encoding="utf-8").splitlines(keepends=True)
    store_file.write_text("".join(lines[2:3]), encoding="utf-8")          # rewritten shorter: offset is past the end
    ev, c2 = a.fetch(c1)
    assert [e.source_id for e in ev] == ["li:2-BBB:0001"] and c2["offset"] == store_file.stat().st_size


def test_adapter_missing_file_is_an_error_not_an_empty_feed(tmp_path):
    with pytest.raises(FileNotFoundError):
        LinkedInStoreAdapter(tmp_path / "nope.jsonl").fetch(None)


# ------------------------------------------------------------------ ingest: dedupe, cursor, resolver

def test_run_once_dedupes_by_source_id_and_moves_the_cursor(store_file):
    st = MemoryStore()
    a = LinkedInStoreAdapter(store_file)
    rep, new = run_once(a, st, Resolver(st, CRM))
    assert (rep.fetched, rep.inserted, rep.duplicates) == (4, 3, 1)
    assert rep.by_direction == {"in": 2, "out": 1}
    assert [s.event.ts for s in new] == sorted(s.event.ts for s in new)
    rep2, new2 = run_once(a, st, Resolver(st, CRM))
    assert (rep2.fetched, rep2.inserted, new2) == (0, 0, [])
    # even with the cursor lost, a full re-read inserts nothing twice
    st._cursors.clear()
    rep3, _ = run_once(a, st, Resolver(st, CRM))
    assert (rep3.fetched, rep3.inserted) == (4, 0)


def test_source_error_is_reported_and_leaves_the_cursor(tmp_path):
    st = MemoryStore()
    st._cursors["linkedin"] = {"offset": 10, "head": "x"}
    rep, new = run_once(LinkedInStoreAdapter(tmp_path / "gone.jsonl"), st, Resolver(st, CRM))
    assert rep.error.startswith("FileNotFoundError") and new == []
    assert st.get_cursor("linkedin") == {"offset": 10, "head": "x"}


def test_resolver_learns_the_route_and_reuses_it(store_file):
    st = MemoryStore()
    _, new = run_once(LinkedInStoreAdapter(store_file), st, Resolver(st, CRM))
    by = {s.event.source_id: s.event for s in new}
    assert by["li:2-AAA:0001"].person_id == "p-giulia" and by["li:2-AAA:0001"].person_via == "linkedin"
    # his reply carries no profile url, only the thread: linked through the route learned one line earlier
    assert by["li:2-AAA:0002"].person_id == "p-giulia" and by["li:2-AAA:0002"].person_via == "route"
    # Marco has no LinkedIn handle in the CRM and a name never auto-links
    assert by["li:2-BBB:0001"].person_id is None
    assert {(r["kind"], r["value"]) for r in st.routes_for_person("p-giulia")} == {
        ("li_thread", "2-AAA"), ("linkedin", "in/giulia-ferri-example")}


def test_a_shared_handle_never_auto_links():
    st = MemoryStore()
    r = Resolver(st, [{"id": "a", "email": "office@clinic.org"}, {"id": "b", "email": "office@clinic.org"}])
    e = r.resolve(_ev(handles=(Handle.of("email", "office@clinic.org"),)))
    assert e.person_id is None


def test_backlog_links_events_once_the_crm_row_exists(store_file):
    st = MemoryStore()
    run_once(LinkedInStoreAdapter(store_file), st, Resolver(st, CRM))
    assert len(st.unresolved()) == 1
    crm2 = CRM + [{"id": "p-marco", "linkedin": "x"}]                     # still no thread: stays unresolved
    assert resolve_backlog(st, Resolver(st, crm2)) == 0
    st.route_put(Handle.of("li_thread", "2-BBB"), "p-marco", "linkedin", "manual")
    assert resolve_backlog(st, Resolver(st, crm2)) == 1
    assert st.unresolved() == []


def test_backfill_person_reads_their_thread_and_dedupes(store_file, tmp_path):
    st = MemoryStore()
    a = LinkedInStoreAdapter(store_file)
    run_once(a, st, Resolver(st, CRM))
    # an older message in Giulia's thread that the incremental read never saw (the Ienna case, HANDOFF 6g)
    old = tmp_path / "thread.jsonl"
    old.write_text(store_file.read_text(encoding="utf-8") +
                   '{"id": "li:2-AAA:0000", "ts": "2026-09-20T10:00:00+02:00", "chatId": "2-AAA", "text": "first note", "fromMe": true}\n',
                   encoding="utf-8")
    cursor = st.get_cursor("linkedin")
    new = backfill_person(LinkedInStoreAdapter(old), st, Resolver(st, CRM), "p-giulia")
    assert [s.event.source_id for s in new] == ["li:2-AAA:0000"] and new[0].event.person_id == "p-giulia"
    assert st.get_cursor("linkedin") == cursor                           # backfill never moves the cursor


# ------------------------------------------------------------------ subscribers (path A)

class ReplyClosesCard:
    """Example subscriber: his outgoing message to a person settles that person's open reply card."""
    name = "reply-closes-card"

    def __init__(self, cards):
        self.cards = cards                                                  # person_id -> card id

    def wants(self, ev):
        return ev.event.direction == "out" and ev.event.person_id in self.cards

    def on_event(self, ev, ctx):
        assert any(s.id == ev.id for s in ctx.events)                      # the person's log is the context
        return Result([Finding("hub", self.cards[ev.event.person_id], "done", ev.id, ev.event.text[:80])])


class Flaky:
    name = "flaky"

    def __init__(self):
        self.calls = 0

    def wants(self, ev):
        return True

    def on_event(self, ev, ctx):
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("judge timed out")
        return Result()


def _ingested(store_file):
    st = MemoryStore()
    _, new = run_once(LinkedInStoreAdapter(store_file), st, Resolver(st, CRM))
    return st, new


def test_dispatch_defaults_to_shadow_and_records_findings(store_file):
    st, new = _ingested(store_file)
    d = Dispatcher(st, [ReplyClosesCard({"p-giulia": "card-2"})], clock=lambda: NOW)
    rep = d.dispatch(new)
    assert (rep.delivered, rep.skipped, rep.findings, rep.errors) == (1, 2, 1, [])
    (f,) = st.findings()
    assert (f["path"], f["mode"], f["item_id"], f["verdict"]) == ("A", "shadow", "card-2", "done")
    with pytest.raises(ValueError):
        Dispatcher(st, [ReplyClosesCard({})], modes={"reply-closes-card": "loud"})
    with pytest.raises(ValueError):
        Dispatcher(st, [ReplyClosesCard({}), ReplyClosesCard({})])


def test_a_failed_delivery_is_retried_once_by_catch_up(store_file):
    st, new = _ingested(store_file)
    fl = Flaky()
    rep = Dispatcher(st, [fl], clock=lambda: NOW).dispatch(new)
    assert rep.delivered == 2 and len(rep.errors) == 1
    assert st.delivery("flaky", rep.errors[0][1])["status"] == "error"
    again = Dispatcher(st, [fl], clock=lambda: NOW).catch_up()
    assert again.delivered == 1 and again.errors == [] and fl.calls == 4
    assert Dispatcher(st, [fl], clock=lambda: NOW).catch_up().delivered == 0   # nothing delivered twice


def test_a_new_subscriber_catches_up_on_the_log(store_file):
    st, new = _ingested(store_file)
    Dispatcher(st, [Flaky()], clock=lambda: NOW).catch_up()
    late = ReplyClosesCard({"p-giulia": "card-2"})
    rep = Dispatcher(st, [late], clock=lambda: NOW).catch_up()
    assert rep.findings == 1


# ------------------------------------------------------------------ sweep (path B) and attribution

def _his_reply_settles(item, events):
    for s in events:
        if s.event.direction == "out" and s.event.ts >= item.created_at - timedelta(days=10):
            return Finding(item.surface, item.item_id, "done", s.id, s.event.text[:80])
    return None


def test_sweep_reads_the_person_log_and_reports_unlinked_items(store_file):
    st, _ = _ingested(store_file)
    items = [OpenItem("hub", "card-2", "p-giulia", datetime(2026, 10, 1, tzinfo=timezone.utc), "reply to Giulia"),
             OpenItem("hub", "card-9", None, datetime(2026, 10, 1, tzinfo=timezone.utc), "reply to someone")]
    rep = sweep(st, items, _his_reply_settles)
    assert rep == {"items": 2, "no_person": 1, "checked": 1, "findings": 1}
    assert st.findings()[0]["path"] == "B"


def test_attribution_first_finder_overlap_and_time_to_find(store_file):
    st, new = _ingested(store_file)
    Dispatcher(st, [ReplyClosesCard({"p-giulia": "card-2"})], clock=lambda: NOW).dispatch(new)
    sweep(st, [OpenItem("hub", "card-2", "p-giulia", datetime(2026, 10, 1, tzinfo=timezone.utc), "x"),
               OpenItem("todo", "follow-up-marco", None, datetime(2026, 10, 1, tzinfo=timezone.utc), "x")],
          _his_reply_settles)
    (row,) = attribution(st)
    assert (row["first_path"], row["first_finder"], row["other_path_also"]) == ("A", "reply-closes-card", True)
    assert row["time_to_find_s"] > 0
    rep = attribution_report([row])
    assert rep["path A"]["first"] == 1 and rep["path A"]["overlap"] == 1 and "path A / hub" in rep
