"""Where events live. One interface, two implementations:

- MemoryStore: tests and dry runs (the shadow report can run on a laptop with no database).
- PgStore: brain.events and friends (migrations/001_brain_events.sql) through psycopg 3.

Contract every Store keeps (tests/test_monitor.py runs it against MemoryStore, and against PgStore when a test
database exists):
  1. write_batch is all-or-nothing: the new events and the adapter's cursor land together, so a crash between
     them can only re-read events (deduped), never skip them.
  2. Dedupe by (source, source_id): a second write of the same key is not an event, and is not returned.
  3. Only the newly inserted events are returned, in ts order; they are what the dispatcher delivers.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Iterable, Protocol

from .events import Event, Finding, Handle, StoredEvent


class Store(Protocol):
    def write_batch(self, source: str, events: Iterable[Event], cursor: dict | None) -> list[StoredEvent]: ...
    def get_cursor(self, source: str) -> dict | None: ...
    def route_get(self, h: Handle) -> str | None: ...
    def route_put(self, h: Handle, person_id: str, channel: str, learned_via: str) -> None: ...
    def routes_for_person(self, person_id: str) -> list[dict]: ...
    def events_for_person(self, person_id: str, since: datetime | None = None, until: datetime | None = None,
                          limit: int = 200) -> list[StoredEvent]: ...
    def unresolved(self, limit: int = 500) -> list[StoredEvent]: ...
    def link(self, event_id: int, person_id: str, via: str) -> None: ...
    def record_delivery(self, subscriber: str, event_id: int, mode: str, status: str, result: dict) -> None: ...
    def undelivered(self, subscriber: str, since: datetime | None = None, limit: int = 500) -> list[StoredEvent]: ...
    def record_finding(self, path: str, finder: str, mode: str, f: Finding) -> bool: ...
    def findings(self) -> list[dict]: ...
    def event(self, event_id: int) -> StoredEvent | None: ...


def _now() -> datetime:
    return datetime.now(timezone.utc)


class MemoryStore:
    def __init__(self):
        self._events: dict[int, StoredEvent] = {}
        self._keys: dict[tuple[str, str], int] = {}
        self._cursors: dict[str, dict] = {}
        self._routes: dict[tuple[str, str], dict] = {}
        self._deliveries: dict[tuple[str, int], dict] = {}
        self._findings: list[dict] = []
        self._next = 1

    # -- events
    def write_batch(self, source, events, cursor):
        staged, seen = [], set()
        for e in events:
            if e.source != source:
                raise ValueError(f"adapter {source!r} emitted an event of source {e.source!r}")
            if e.key in self._keys or e.key in seen:
                continue
            seen.add(e.key)
            staged.append(e)
        out = []
        for e in sorted(staged, key=lambda x: x.ts):
            se = StoredEvent(self._next, e, _now())
            self._events[se.id] = se
            self._keys[e.key] = se.id
            self._next += 1
            out.append(se)
        if cursor is not None:
            self._cursors[source] = dict(cursor)
        return out

    def get_cursor(self, source):
        c = self._cursors.get(source)
        return dict(c) if c is not None else None

    def event(self, event_id):
        return self._events.get(event_id)

    def events_for_person(self, person_id, since=None, until=None, limit=200):
        rows = [s for s in self._events.values() if s.event.person_id == person_id
                and (since is None or s.event.ts >= since) and (until is None or s.event.ts <= until)]
        return sorted(rows, key=lambda s: s.event.ts, reverse=True)[:limit]

    def unresolved(self, limit=500):
        return [s for s in self._events.values() if s.event.person_id is None][:limit]

    def link(self, event_id, person_id, via):
        s = self._events[event_id]
        self._events[event_id] = StoredEvent(s.id, s.event.linked(person_id, via), s.ingested_at)

    # -- routes
    def route_get(self, h):
        r = self._routes.get((h.kind, h.value))
        if r:
            r["hits"] += 1
            r["last_seen"] = _now()
            return r["person_id"]
        return None

    def route_put(self, h, person_id, channel, learned_via):
        self._routes.setdefault((h.kind, h.value), {"kind": h.kind, "value": h.value, "person_id": person_id,
                                                    "channel": channel, "learned_via": learned_via,
                                                    "first_seen": _now(), "last_seen": _now(), "hits": 1})

    def routes_for_person(self, person_id):
        return [dict(r) for r in self._routes.values() if r["person_id"] == person_id]

    # -- deliveries
    def record_delivery(self, subscriber, event_id, mode, status, result):
        self._deliveries[(subscriber, event_id)] = {"mode": mode, "status": status, "result": result, "at": _now()}

    def undelivered(self, subscriber, since=None, limit=500):
        rows = [s for s in self._events.values()
                if (since is None or s.event.ts >= since)
                and self._deliveries.get((subscriber, s.id), {}).get("status") in (None, "error")]
        return sorted(rows, key=lambda s: s.event.ts)[:limit]

    def delivery(self, subscriber, event_id):
        return self._deliveries.get((subscriber, event_id))

    # -- findings
    def record_finding(self, path, finder, mode, f):
        key = (f.surface, f.item_id, path, finder, f.event_id)
        if any((r["surface"], r["item_id"], r["path"], r["finder"], r["event_id"]) == key for r in self._findings):
            return False
        self._findings.append({"surface": f.surface, "item_id": f.item_id, "path": path, "finder": finder, "mode": mode,
                               "verdict": f.verdict, "event_id": f.event_id, "evidence": f.evidence,
                               "found_at": _now(), "id": len(self._findings) + 1})
        return True

    def findings(self):
        return [dict(r) for r in self._findings]


class PgStore:
    """brain.events through psycopg 3. `conn` is an open psycopg.Connection (autocommit off). SKELETON: exercised by
    the contract test only when a test database exists; no production code constructs it yet."""

    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def _row(r) -> StoredEvent:
        (id_, source, source_id, channel, direction, ts, prec, thread, pid, via, handles, text, data, ing) = r
        hs = tuple(Handle(h["kind"], h["value"]) for h in (handles or []))
        e = Event(source, source_id, channel, direction, ts, text or "", thread, hs, prec, data or {}, pid, via)
        return StoredEvent(id_, e, ing)

    _COLS = ("id, source, source_id, channel, direction, ts, ts_precision, thread, person_id, person_via, handles, "
             "text, data, ingested_at")

    def write_batch(self, source, events, cursor):
        evs = sorted(events, key=lambda x: x.ts)
        for e in evs:
            if e.source != source:
                raise ValueError(f"adapter {source!r} emitted an event of source {e.source!r}")
        out = []
        with self.conn.transaction(), self.conn.cursor() as cur:
            for e in evs:
                cur.execute(
                    "INSERT INTO brain.events (source, source_id, channel, direction, ts, ts_precision, thread, person_id,"
                    " person_via, handles, text, data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s::jsonb)"
                    " ON CONFLICT (source, source_id) DO NOTHING RETURNING " + self._COLS,
                    (e.source, e.source_id, e.channel, e.direction, e.ts, e.ts_precision, e.thread, e.person_id,
                     e.person_via, json.dumps([h.as_dict() for h in e.handles]), e.text, json.dumps(e.data, default=str)))
                r = cur.fetchone()
                if r:
                    out.append(self._row(r))
            if cursor is not None:
                cur.execute("INSERT INTO brain.event_cursors (source, cursor) VALUES (%s, %s::jsonb)"
                            " ON CONFLICT (source) DO UPDATE SET cursor = EXCLUDED.cursor, updated_at = now()",
                            (source, json.dumps(cursor)))
        return out

    def get_cursor(self, source):
        with self.conn.cursor() as cur:
            cur.execute("SELECT cursor FROM brain.event_cursors WHERE source = %s", (source,))
            r = cur.fetchone()
        self.conn.commit()
        return r[0] if r else None

    def event(self, event_id):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {self._COLS} FROM brain.events WHERE id = %s", (event_id,))
            r = cur.fetchone()
        self.conn.commit()
        return self._row(r) if r else None

    def _select(self, where: str, args: tuple, order: str, limit: int) -> list[StoredEvent]:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {self._COLS} FROM brain.events e WHERE {where} ORDER BY {order} LIMIT %s", args + (limit,))
            rows = cur.fetchall()
        self.conn.commit()
        return [self._row(r) for r in rows]

    def events_for_person(self, person_id, since=None, until=None, limit=200):
        return self._select("person_id = %s AND (%s::timestamptz IS NULL OR ts >= %s) AND (%s::timestamptz IS NULL OR ts <= %s)",
                            (person_id, since, since, until, until), "ts DESC", limit)

    def unresolved(self, limit=500):
        return self._select("person_id IS NULL", (), "ingested_at", limit)

    def link(self, event_id, person_id, via):
        with self.conn.transaction(), self.conn.cursor() as cur:
            cur.execute("UPDATE brain.events SET person_id = %s, person_via = %s WHERE id = %s", (person_id, via, event_id))

    def route_get(self, h):
        with self.conn.transaction(), self.conn.cursor() as cur:
            cur.execute("UPDATE brain.event_routes SET hits = hits + 1, last_seen = now() WHERE kind = %s AND value = %s"
                        " RETURNING person_id", (h.kind, h.value))
            r = cur.fetchone()
        return r[0] if r else None

    def route_put(self, h, person_id, channel, learned_via):
        with self.conn.transaction(), self.conn.cursor() as cur:
            cur.execute("INSERT INTO brain.event_routes (kind, value, person_id, channel, learned_via) VALUES (%s,%s,%s,%s,%s)"
                        " ON CONFLICT (kind, value) DO NOTHING", (h.kind, h.value, person_id, channel, learned_via))

    def routes_for_person(self, person_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT kind, value, person_id, channel, learned_via, first_seen, last_seen, hits"
                        " FROM brain.event_routes WHERE person_id = %s", (person_id,))
            cols = [d.name for d in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        self.conn.commit()
        return rows

    def record_delivery(self, subscriber, event_id, mode, status, result):
        with self.conn.transaction(), self.conn.cursor() as cur:
            cur.execute("INSERT INTO brain.event_deliveries (subscriber, event_id, mode, status, result) VALUES (%s,%s,%s,%s,%s::jsonb)"
                        " ON CONFLICT (subscriber, event_id) DO UPDATE SET mode = EXCLUDED.mode, status = EXCLUDED.status,"
                        " result = EXCLUDED.result, delivered_at = now()",
                        (subscriber, event_id, mode, status, json.dumps(result, default=str)))

    def undelivered(self, subscriber, since=None, limit=500):
        return self._select("(%s::timestamptz IS NULL OR e.ts >= %s) AND NOT EXISTS (SELECT 1 FROM brain.event_deliveries d"
                            " WHERE d.subscriber = %s AND d.event_id = e.id AND d.status <> 'error')",
                            (since, since, subscriber), "e.ts", limit)

    def record_finding(self, path, finder, mode, f):
        with self.conn.transaction(), self.conn.cursor() as cur:
            cur.execute("INSERT INTO brain.event_findings (surface, item_id, path, finder, mode, verdict, event_id, evidence)"
                        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id",
                        (f.surface, f.item_id, path, finder, mode, f.verdict, f.event_id, f.evidence))
            return cur.fetchone() is not None

    def findings(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, surface, item_id, path, finder, mode, verdict, event_id, evidence, found_at"
                        " FROM brain.event_findings ORDER BY found_at, id")
            cols = [d.name for d in cur.description]
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        self.conn.commit()
        return rows
