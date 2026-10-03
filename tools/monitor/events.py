"""The event shape every adapter produces and every subscriber reads (one row of brain.events)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone

CHANNELS = ("email", "whatsapp", "linkedin", "slack", "calendar", "meeting", "crm")
DIRECTIONS = ("in", "out", "internal")
PRECISIONS = ("exact", "minute", "day")
HANDLE_KINDS = ("email", "phone", "linkedin", "slack", "wa_chat", "li_thread", "name")
SURFACES = ("hub", "todo", "crm")
TEXT_MAX = 8000          # a mail body beyond this is noise for matching; the source keeps the whole thing


def norm_handle(kind: str, value: str) -> str:
    """One spelling per handle, so a route learned from one source matches the next source."""
    v = str(value or "").strip()
    if kind == "email":
        m = re.search(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", v)
        return m.group(0).lower() if m else ""
    if kind == "phone":
        d = re.sub(r"\D", "", v.split("@")[0])
        return d[2:] if d.startswith("00") else d
    if kind == "linkedin":
        v = v.split("?")[0].rstrip("/").lower()
        m = re.search(r"linkedin\.com/in/([^/]+)", v)
        return "in/" + m.group(1) if m else v
    if kind == "name":
        return re.sub(r"\s+", " ", v).casefold()
    return v


@dataclass(frozen=True)
class Handle:
    kind: str
    value: str

    @staticmethod
    def of(kind: str, value: str) -> "Handle | None":
        if kind not in HANDLE_KINDS:
            raise ValueError(f"unknown handle kind {kind!r}")
        n = norm_handle(kind, value)
        return Handle(kind, n) if n else None

    def as_dict(self) -> dict:
        return {"kind": self.kind, "value": self.value}


@dataclass(frozen=True)
class Event:
    """What an adapter emits. `source` + `source_id` is the dedupe key; everything else is data."""
    source: str
    source_id: str
    channel: str
    direction: str
    ts: datetime
    text: str = ""
    thread: str | None = None
    handles: tuple[Handle, ...] = ()
    ts_precision: str = "exact"
    data: dict = field(default_factory=dict, compare=False, hash=False)
    person_id: str | None = None
    person_via: str | None = None

    def __post_init__(self):
        if not self.source or not self.source_id:
            raise ValueError("an event needs source and source_id (the dedupe key)")
        if self.channel not in CHANNELS:
            raise ValueError(f"channel {self.channel!r} not in {CHANNELS}")
        if self.direction not in DIRECTIONS:
            raise ValueError(f"direction {self.direction!r} not in {DIRECTIONS}")
        if self.ts_precision not in PRECISIONS:
            raise ValueError(f"ts_precision {self.ts_precision!r} not in {PRECISIONS}")
        if self.ts.tzinfo is None:
            raise ValueError("ts must be timezone-aware (UTC in the table)")
        if len(self.text) > TEXT_MAX:
            object.__setattr__(self, "text", self.text[:TEXT_MAX])

    @property
    def key(self) -> tuple[str, str]:
        return (self.source, self.source_id)

    def linked(self, person_id: str | None, via: str | None) -> "Event":
        return replace(self, person_id=person_id, person_via=via if person_id else None)


@dataclass(frozen=True)
class StoredEvent:
    """An event once it has a row id (what subscribers and the sweep receive)."""
    id: int
    event: Event
    ingested_at: datetime

    def __getattr__(self, name):          # ev.person_id, ev.text ... read through to the event
        if name.startswith("__") or name == "event":
            raise AttributeError(name)
        return getattr(self.event, name)


@dataclass(frozen=True)
class Finding:
    """A path found that an item is settled (or judged that it is not: verdict none, kept for the judge's record)."""
    surface: str
    item_id: str
    verdict: str                      # done | moved | outdated | none
    event_id: int | None = None
    evidence: str = ""

    def __post_init__(self):
        if self.surface not in SURFACES:
            raise ValueError(f"surface {self.surface!r} not in {SURFACES}")


def utc(dt: datetime) -> datetime:
    return dt.astimezone(timezone.utc)
