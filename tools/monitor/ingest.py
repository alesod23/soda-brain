"""Ingest: adapters read their source incrementally, the resolver links each event to a CRM person, the store dedupes.

    adapter.fetch(cursor) -> (events, new_cursor)      incremental: only what is new since the cursor
    resolver.resolve(event) -> event linked to a person (route memo first, then the CRM's exact handles)
    store.write_batch(source, events, cursor)          dedupe by (source, source_id), cursor in the same transaction
    run_once(...) -> IngestReport, plus the newly stored events for the dispatcher

SKELETON: no scheduler, no production adapter instance. See docs/MONITOR-LAYER.md for the run plan.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Protocol

from .events import Event, Handle, StoredEvent
from .store import Store


class Adapter(Protocol):
    """One source instance (gmail:cdtm, whatsapp, linkedin, slack:cdtm ...). Must be:
    - incremental: fetch(cursor) returns only what is new since `cursor` (None = first run, the adapter decides the
      backfill depth) and the cursor to store with them;
    - both directions: what he sent is an event (direction out) exactly like what he received;
    - honest about failure: raise on an unreadable source. An empty list means "nothing new", never "could not read"
      (hub_outdated learned this with the tundra 403: a judge looking at a hole closes the wrong cards);
    - stable: the same message always gets the same source_id, so re-reads dedupe.
    """
    source: str

    def fetch(self, cursor: dict | None) -> tuple[list[Event], dict]: ...

    def fetch_person(self, routes: list[dict]) -> list[Event]:
        """Optional, on demand: read THIS person's thread/chat directly (HANDOFF 6g: the LinkedIn inbox scan only sees
        the ~17 most recent threads, so an open card's person is read by route). Return [] when unsupported."""
        ...


# Which handle kinds may link an event to a person automatically, in order. `name` never does: two people share a
# name too often (the CRM has several), so a name-only event stays unresolved and is proposed, not linked.
AUTO_LINK_KINDS = ("email", "phone", "linkedin", "slack", "wa_chat", "li_thread")


class Resolver:
    """Event -> person. Route memo first (exact handle seen before), then the CRM's own handles. A CRM hit is written
    to the route memo, so the second event from the same handle never touches the CRM index again."""

    def __init__(self, store: Store, crm_people: Iterable[dict] = ()):
        self.store = store
        self.index: dict[tuple[str, str], str] = {}
        self.ambiguous: set[tuple[str, str]] = set()
        for p in crm_people:
            pid = str(p.get("id") or "")
            if not pid:
                continue
            for kind, raw in (("email", p.get("email")), ("phone", p.get("phone")), ("linkedin", p.get("linkedin")),
                              ("slack", p.get("slack"))):
                h = Handle.of(kind, raw) if raw else None
                if not h:
                    continue
                k = (h.kind, h.value)
                if k in self.index and self.index[k] != pid:
                    self.ambiguous.add(k)          # two CRM rows share a handle: never auto-link on it
                self.index.setdefault(k, pid)

    def resolve(self, e: Event) -> Event:
        if e.person_id:
            return e
        hs = [h for h in e.handles if h.kind in AUTO_LINK_KINDS]
        for h in hs:
            pid = self.store.route_get(h)
            if pid:
                return e.linked(pid, "route")
        for h in hs:
            k = (h.kind, h.value)
            if k in self.index and k not in self.ambiguous:
                pid = self.index[k]
                # Remember every handle of this event for this person: the chat/thread id learned here is the fast
                # route next time (and the on-demand backfill target).
                for other in hs:
                    if (other.kind, other.value) not in self.ambiguous:
                        self.store.route_put(other, pid, e.channel, "crm")
                return e.linked(pid, h.kind)
        return e


@dataclass
class IngestReport:
    source: str
    fetched: int = 0
    inserted: int = 0
    duplicates: int = 0
    unresolved: int = 0
    by_direction: dict = field(default_factory=dict)
    error: str | None = None


def run_once(adapter: Adapter, store: Store, resolver: Resolver) -> tuple[IngestReport, list[StoredEvent]]:
    """One incremental pass of one adapter. A source error is reported (fail loud) and leaves the cursor untouched."""
    rep = IngestReport(adapter.source)
    try:
        events, cursor = adapter.fetch(store.get_cursor(adapter.source))
    except Exception as ex:  # noqa: BLE001 - reported, never swallowed: the report carries it to the run log/alert
        rep.error = f"{type(ex).__name__}: {str(ex)[:200]}"
        return rep, []
    linked = [resolver.resolve(e) for e in events]
    new = store.write_batch(adapter.source, linked, cursor)
    rep.fetched, rep.inserted = len(events), len(new)
    rep.duplicates = rep.fetched - rep.inserted
    for s in new:
        rep.by_direction[s.event.direction] = rep.by_direction.get(s.event.direction, 0) + 1
        rep.unresolved += s.event.person_id is None
    return rep, new


def resolve_backlog(store: Store, resolver: Resolver, limit: int = 500) -> int:
    """Re-run the resolver on events still without a person (a CRM row created after the event, a route learned
    since). Returns how many were linked. Meant for the end of every ingest tick."""
    n = 0
    for s in store.unresolved(limit):
        e = resolver.resolve(s.event)
        if e.person_id:
            store.link(s.id, e.person_id, e.person_via)
            n += 1
    return n


def backfill_person(adapter: Adapter, store: Store, resolver: Resolver, person_id: str) -> list[StoredEvent]:
    """On demand: read a person's own thread through their remembered routes (an open card names them and the
    periodic scan cannot reach the thread). New events go through the same dedupe; the cursor is not moved."""
    routes = store.routes_for_person(person_id)
    if not routes:
        return []
    events = [resolver.resolve(e) for e in adapter.fetch_person(routes)]
    return store.write_batch(adapter.source, events, None)
