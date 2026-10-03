"""The loops become subscribers of the one log.

Path A (event push): Dispatcher.dispatch(new_events) hands every new event to every subscriber that wants it, once
(a delivery row per subscriber and event), with the person's context read from the log (HANDOFF 6d: "when we have a
card about a person, we should have its events as context").
Path B (periodic sweep): sweep(items, check) takes each open item (hub card, to-do, CRM step) and reads ITS person's
events from the same log; nothing is fetched from a source again.
Both paths write findings; attribution() says who found each item first and whether the other path also did.

Shadow mode is per subscriber: a shadow subscriber is called with ctx.mode == "shadow" and must not act (no card
closed, no tick, no CRM write); its findings are recorded with mode shadow so the shadow report can compare them with
what the legacy loop did. SKELETON: the concrete subscribers (todo_match, hub_outdated reverse pass, inbound asks,
the CRM reader, the meeting loop) are described in docs/MONITOR-LAYER.md, not wired here.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, Iterable, Protocol

from .events import Finding, StoredEvent
from .store import Store

CONTEXT_DAYS = 30            # how much of a person's log a subscriber sees by default
HIS_BEFORE_DAYS = 10         # hub_outdated's rule: his own message up to 10 days before a card still settles it


@dataclass
class PersonContext:
    """What a subscriber gets with an event: the person's recent log and routes, read lazily from the store."""
    store: Store
    person_id: str | None
    mode: str                                    # shadow | live
    now: datetime
    _events: list[StoredEvent] | None = None

    @property
    def events(self) -> list[StoredEvent]:
        if self._events is None:
            self._events = ([] if not self.person_id else
                            self.store.events_for_person(self.person_id, since=self.now - timedelta(days=CONTEXT_DAYS)))
        return self._events

    @property
    def routes(self) -> list[dict]:
        return self.store.routes_for_person(self.person_id) if self.person_id else []


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)
    note: str = ""


class Subscriber(Protocol):
    name: str                                    # stable: it keys the delivery rows and the attribution

    def wants(self, ev: StoredEvent) -> bool:
        """Cheap filter, no I/O: channel, direction, resolved person or not."""
        ...

    def on_event(self, ev: StoredEvent, ctx: PersonContext) -> Result:
        """Judge (and, in live mode only, act). Raise on failure: the dispatcher records it and retries next tick."""
        ...


@dataclass
class DispatchReport:
    delivered: int = 0
    skipped: int = 0
    errors: list[tuple[str, int, str]] = field(default_factory=list)
    findings: int = 0


class Dispatcher:
    def __init__(self, store: Store, subscribers: Iterable[Subscriber], modes: dict[str, str] | None = None,
                 clock: Callable[[], datetime] | None = None):
        self.store = store
        self.subs = list(subscribers)
        names = [s.name for s in self.subs]
        if len(set(names)) != len(names):
            raise ValueError(f"subscriber names must be unique: {names}")
        self.modes = {s.name: (modes or {}).get(s.name, "shadow") for s in self.subs}   # default shadow, never live by accident
        bad = {n: m for n, m in self.modes.items() if m not in ("shadow", "live")}
        if bad:
            raise ValueError(f"unknown modes {bad}")
        self.clock = clock or (lambda: datetime.now().astimezone())

    def dispatch(self, events: Iterable[StoredEvent]) -> DispatchReport:
        rep = DispatchReport()
        for ev in events:
            ctx_by_mode: dict[str, PersonContext] = {}
            for sub in self.subs:
                mode = self.modes[sub.name]
                if not sub.wants(ev):
                    self.store.record_delivery(sub.name, ev.id, mode, "skipped", {})
                    rep.skipped += 1
                    continue
                ctx = ctx_by_mode.setdefault(mode, PersonContext(self.store, ev.event.person_id, mode, self.clock()))
                try:
                    res = sub.on_event(ev, ctx)
                except Exception as ex:  # noqa: BLE001 - recorded with the error and retried by catch_up()
                    msg = f"{type(ex).__name__}: {str(ex)[:200]}"
                    self.store.record_delivery(sub.name, ev.id, mode, "error", {"error": msg})
                    rep.errors.append((sub.name, ev.id, msg))
                    continue
                for f in res.findings:
                    rep.findings += self.store.record_finding("A", sub.name, mode, f)
                self.store.record_delivery(sub.name, ev.id, mode, "ok",
                                           {"findings": len(res.findings), "note": res.note[:300]})
                rep.delivered += 1
        return rep

    def catch_up(self, since: datetime | None = None) -> DispatchReport:
        """Events a subscriber has not seen (it was added later, or it errored): delivered in ts order. Only to the
        subscribers missing them; the others are not called twice."""
        total = DispatchReport()
        for sub in self.subs:
            one = Dispatcher(self.store, [sub], {sub.name: self.modes[sub.name]}, self.clock)
            r = one.dispatch(self.store.undelivered(sub.name, since))
            total.delivered += r.delivered
            total.skipped += r.skipped
            total.errors += r.errors
            total.findings += r.findings
        return total


@dataclass(frozen=True)
class OpenItem:
    """An open thing on a surface the sweep checks: a hub card, a to-do, a CRM next step."""
    surface: str
    item_id: str
    person_id: str | None
    created_at: datetime
    text: str


def sweep(store: Store, items: Iterable[OpenItem], check: Callable[[OpenItem, list[StoredEvent]], Finding | None],
          finder: str = "sweep", mode: str = "shadow") -> dict:
    """Path B: each open item against its person's events in the log, from HIS_BEFORE_DAYS before the item to now.
    `check` is the judge (deterministic rule or model); it sees only the log, never a source."""
    out = {"items": 0, "no_person": 0, "checked": 0, "findings": 0}
    for it in items:
        out["items"] += 1
        if not it.person_id:
            out["no_person"] += 1            # the blind spot this layer exists to shrink: reported, not hidden
            continue
        evs = store.events_for_person(it.person_id, since=it.created_at - timedelta(days=HIS_BEFORE_DAYS))
        out["checked"] += 1
        f = check(it, evs)
        if f is not None and f.verdict != "none":
            out["findings"] += store.record_finding("B", finder, mode, f)
    return out


def attribution(store: Store) -> list[dict]:
    """One row per settled item: first path and finder, time-to-find, and whether the other path also found it.
    Same answer as the SQL view brain.event_attribution (that one is for the report on the box)."""
    by_item: dict[tuple[str, str], list[dict]] = {}
    for f in store.findings():
        if f["verdict"] != "none":
            by_item.setdefault((f["surface"], f["item_id"]), []).append(f)
    rows = []
    for (surface, item), fs in by_item.items():
        fs.sort(key=lambda r: (r["found_at"], r["id"]))
        first = fs[0]
        ev = store.event(first["event_id"]) if first.get("event_id") else None
        rows.append({"surface": surface, "item_id": item, "first_path": first["path"], "first_finder": first["finder"],
                     "mode": first["mode"],
                     "time_to_find_s": (first["found_at"] - ev.event.ts).total_seconds() if ev else None,
                     "other_path_also": any(r["path"] != first["path"] for r in fs)})
    return rows


def attribution_report(rows: list[dict]) -> dict:
    """Per path and per surface: items first found, overlap with the other path, median time-to-find."""
    rep: dict[str, dict] = {}
    for r in rows:
        for key in (f"path {r['first_path']}", f"path {r['first_path']} / {r['surface']}"):
            d = rep.setdefault(key, {"first": 0, "overlap": 0, "ttf": []})
            d["first"] += 1
            d["overlap"] += r["other_path_also"]
            if r["time_to_find_s"] is not None:
                d["ttf"].append(r["time_to_find_s"])
    return {k: {"first": v["first"], "overlap": v["overlap"],
                "median_time_to_find_s": statistics.median(v["ttf"]) if v["ttf"] else None} for k, v in sorted(rep.items())}
