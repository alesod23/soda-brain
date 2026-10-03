"""Reference adapter: the LinkedIn store (one JSON line per message, written by ~/.claude/linkedin-poll/poll.py,
shipped to `G:/My Drive/DA/linkedin-store.jsonl` = `/home/da/gdrive/DA/linkedin-store.jsonl` on the box).

Line shape (field names as in the real store on 2026-10-04; values here are fictional):
    {"id": "li:<chat>:<hash>", "ts": "2026-09-29T00:26:00+02:00", "iso": "...", "ts_precision": "minute" | "day",
     "timestamp": <poll time, NOT the message time>, "chatId": "2-...", "chatName": "<counterpart>",
     "sender": "<who wrote it>", "text": "...", "url": "<thread url>", "fromMe": false, "source": "linkedin"}

What it shows the other adapters how to do:
- incremental by byte offset; a file that shrank or whose first line changed (rewritten, not appended) is read
  again from 0 and the store's (source, source_id) dedupe absorbs the repeat;
- both directions: `fromMe` -> direction out. On 2026-10-04 the real store held 0 fromMe lines of 87 because the
  poller drops them (poll.py ~line 127, `not it["fromMe"]`, HANDOFF 6d Fix 1); the adapter is ready for the day it
  stops dropping them, and the shadow report counts out-events per channel so the gap stays visible;
- the store repeats ids (87 lines, 63 distinct ids on 2026-10-04): dedupe is the store's job, not the adapter's;
- `timestamp` is the poll time; the message time is `ts`/`iso` with its precision (35 of 87 lines are day-precision);
- handles: the chat id (li_thread) is the stable route; a profile url when the line carries one; the name only as
  data for a human proposal, never an auto-link.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from ..events import Event, Handle

SOURCE = "linkedin"


def _ts(m: dict) -> tuple[datetime | None, str]:
    for k in ("ts", "iso"):
        v = m.get(k)
        if v:
            try:
                dt = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                prec = m.get("ts_precision") if m.get("ts_precision") in ("exact", "minute", "day") else "exact"
                return dt.astimezone(timezone.utc), prec
            except ValueError:
                pass
    return None, "exact"


def line_to_event(m: dict) -> Event | None:
    text = str(m.get("text") or "").strip()
    sid = str(m.get("id") or "").strip()
    ts, prec = _ts(m)
    if not (text and sid and ts):
        return None
    handles = []
    if m.get("chatId"):
        handles.append(Handle.of("li_thread", str(m["chatId"])))
    url = str(m.get("url") or "")
    if "/in/" in url:
        handles.append(Handle.of("linkedin", url))
    if m.get("chatName"):
        handles.append(Handle.of("name", str(m["chatName"])))
    return Event(source=SOURCE, source_id=sid, channel="linkedin", direction="out" if m.get("fromMe") else "in",
                 ts=ts, ts_precision=prec, text=text, thread=str(m.get("chatId") or "") or None,
                 handles=tuple(h for h in handles if h),
                 data={"chat_name": m.get("chatName"), "sender": m.get("sender"), "url": url or None})


class LinkedInStoreAdapter:
    source = SOURCE

    def __init__(self, path: str | os.PathLike):
        self.path = Path(path)

    def _head(self) -> str:
        with open(self.path, "rb") as f:
            return hashlib.sha1(f.readline()).hexdigest()

    def fetch(self, cursor: dict | None) -> tuple[list[Event], dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"LinkedIn store missing: {self.path}")   # unreadable is an error, not "nothing new"
        size, head = self.path.stat().st_size, self._head()
        offset = int((cursor or {}).get("offset") or 0)
        if offset > size or (cursor or {}).get("head") not in (None, head):
            offset = 0                                                      # rewritten, not appended
        events = []
        with open(self.path, "rb") as f:
            f.seek(offset)
            data = f.read()
        complete = data[: data.rfind(b"\n") + 1]                            # a half-written last line waits for the next tick
        for raw in complete.decode("utf-8", "replace").splitlines():
            try:
                e = line_to_event(json.loads(raw))
            except ValueError:
                continue
            if e:
                events.append(e)
        return events, {"offset": offset + len(complete), "head": head}

    def fetch_person(self, routes: list[dict]) -> list[Event]:
        """Skeleton: filters the store by the person's thread ids. Live version: open THAT thread through the LinkedIn
        session (the poller profile) and return every message in it, both directions."""
        threads = {r["value"] for r in routes if r.get("kind") == "li_thread"}
        if not threads or not self.path.exists():
            return []
        out = []
        for raw in self.path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                m = json.loads(raw)
            except ValueError:
                continue
            if str(m.get("chatId") or "") in threads:
                e = line_to_event(m)
                if e:
                    out.append(e)
        return out
