#!/usr/bin/env python3
"""todo_match.py: an event finds the nearest open to-dos and CRM people in the brain (S10, his words 3 Oct 2026:
"when an event or an email happens, based on what's inside that email, we can understand which parts of the brain
to explore, and we're going to find a to-do item there. We're going to find a CRM item there ... 'Okay, this is
done.'"). Two uses:

  1. lookup (no model): `match(text, k)` -> hits from POST /brain/match on the door. Producers (the meeting loop,
     any card maker) call it BEFORE proposing a step, so the card can say "already on your to-do" or not be made.
  2. judge (one Opus call, headless, no window): `judge(event, hits)` -> for each hit: done / redate / none, with the
     evidence quote. `--apply` ticks through `pipeline.py tick` (the only writer of a task's state) and never
     deletes anything. Every outcome is one line in task-land/_system/todo-match.jsonl (judgeable, H34).

    todo_match.py lookup "text" [--k 8] [--done]
    todo_match.py judge --text "event text" --source "email:<thread>" [--k 8] [--apply] [--dry]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DOOR = os.environ.get("SODA_DOOR", "http://100.85.52.84:4150")
ENV = Path.home() / ".env" / "soda.env"
TASKLAND = Path(os.environ.get("TASKLAND") or (Path.home() / "task-land"))
LOG = TASKLAND / "_system" / "todo-match.jsonl"
PIPELINE = TASKLAND / "_system" / "pipeline.py"
CLAUDE = str(Path.home() / ".local" / "bin" / ("claude.exe" if os.name == "nt" else "claude"))
NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def token(ro=True) -> str:
    for name in (("SODA_TOKEN_RO", "SODA_TOKEN") if ro else ("SODA_TOKEN",)):
        v = os.environ.get(name)
        if v:
            return v
    try:
        for ln in ENV.read_text(encoding="utf-8").splitlines():
            k, _, v = ln.partition("=")
            if k.strip() in (("SODA_TOKEN_RO", "SODA_TOKEN") if ro else ("SODA_TOKEN",)) and v.strip():
                return v.strip().strip('"')
    except OSError:
        pass
    return ""


def match(text: str, k: int = 8, include_done: bool = False, timeout: int = 30) -> list[dict]:
    """The nearest to-dos and people for an event text. [] when the door is unreachable (the caller goes on)."""
    import urllib.request
    body = json.dumps({"text": text[:6000], "k": k, "include_done": include_done}).encode("utf-8")
    req = urllib.request.Request(DOOR + "/brain/match", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Soda-Token": token()})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8") or "[]")
    except Exception as e:
        log_line(event="lookup-failed", error=type(e).__name__ + " " + str(e)[:160])
        return []


def open_todos(hits: list[dict]) -> list[dict]:
    return [h for h in hits if h.get("kind") == "todo" and h.get("status") == "open"]


def already_open_text(hits: list[dict], max_items: int = 6) -> str:
    """One block for a producer's prompt: what is already open for this person or action."""
    todos = open_todos(hits)[:max_items]
    people = [h for h in hits if h.get("kind") == "person"][:3]
    if not todos and not people:
        return ""
    L = ["Already in his system (the brain lookup; judge whether any of it IS the step you are about to propose):"]
    for h in todos:
        L.append(f"- to-do {h['id']}" + (f" (due {h['due']})" if h.get("due") else "") + f": {str(h.get('title') or '')[:160]}")
    for h in people:
        txt = re.sub(r"\s+", " ", str(h.get("text") or ""))[:220]
        L.append(f"- CRM {h['id']}: {txt}")
    return "\n".join(L)


JUDGE_PROMPT = """An event just happened in Alessandro Sodano's world. Decide, for each candidate item below, whether the event
shows that item is DONE (the thing it asks for happened), MOVED (its date changed), or UNCHANGED. Only what the event text
proves; never a guess. A reply that merely mentions a topic does not complete a to-do about it.

EVENT (__SOURCE__):
__EVENT__

CANDIDATES:
__CANDS__

Answer with ONE JSON array and nothing else: [{"id": "<candidate id>", "verdict": "done" | "moved" | "none",
"due": "YYYY-MM-DD when moved, else \\"\\"", "quote": "the words of the event that prove it, \\"\\" when none", "why": "one line"}]
Candidates you leave out count as "none"."""


def judge(event: str, source: str, hits: list[dict], model: str = "opus", timeout: int = 240) -> list[dict]:
    cands = open_todos(hits) + [h for h in hits if h.get("kind") == "card" and h.get("status") == "open"]
    if not cands:
        return []
    cl = "\n".join(f"- {h['id']}" + (" (hub card: done = the thing it asks about already happened; its action is never executed)" if h.get("kind") == "card" else "")
                   + (f" (due {h['due']})" if h.get("due") and h.get("kind") != "card" else "") + f": {str(h.get('title') or '')[:200]}" for h in cands)
    prompt = JUDGE_PROMPT.replace("__SOURCE__", source).replace("__EVENT__", event[:5000]).replace("__CANDS__", cl)
    r = subprocess.run([CLAUDE, "-p", prompt, "--model", model, "--output-format", "text", "--max-turns", "1"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, creationflags=NOWIN)
    txt = r.stdout or ""
    i, j = txt.find("["), txt.rfind("]")
    if i < 0 or j < i:
        raise RuntimeError("judge gave no JSON: " + (r.stderr or txt)[-200:])
    out = json.loads(txt[i:j + 1])
    byid = {h["id"]: h for h in cands}
    return [dict(v, title=byid[v["id"]].get("title"), kind=byid[v["id"]].get("kind")) for v in out if isinstance(v, dict) and v.get("id") in byid]


HUB_CLOSE = os.environ.get("HUB_CLOSE", "http://100.85.52.84:4180/close")


def close_card(cid: str, source: str, quote: str, why: str, dry: bool) -> dict:
    """A card whose outcome an event proves: closed with the evidence, NO verdict (never a yes), nothing executed."""
    reason = f"done, seen in {source}: \"{quote[:160]}\" {why[:120]}".strip()
    if dry:
        return {"applied": False, "dry": "close " + cid + ": " + reason}
    import urllib.request
    req = urllib.request.Request(HUB_CLOSE, data=json.dumps({"id": cid, "reason": reason, "notify": False}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        return dict(json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8") or "{}"), applied=True)
    except Exception as e:
        return {"applied": False, "error": str(e)[:160]}


def apply(verdict: dict, source: str, dry: bool) -> dict:
    """done -> pipeline.py tick <id> --evidence; moved -> pipeline.py redate; a hub card -> /close with the evidence.
    Nothing else writes a task file."""
    if verdict.get("kind") == "card":
        return close_card(verdict["id"], source, verdict.get("quote") or "", verdict.get("why") or "", dry) if verdict.get("verdict") == "done" else {"applied": False}
    if verdict.get("verdict") not in ("done", "moved"):
        return {"applied": False}
    ev = json.dumps({"by": "brain", "source": source, "quote": verdict.get("quote") or "", "why": verdict.get("why") or ""}, ensure_ascii=False)
    cmd = [sys.executable, str(PIPELINE)] + (["tick", verdict["id"], "--evidence", ev] if verdict["verdict"] == "done"
                                              else ["redate", verdict["id"], verdict.get("due") or "", "--evidence", ev])
    if dry:
        return {"applied": False, "dry": " ".join(cmd[2:5])}
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, creationflags=NOWIN, cwd=str(TASKLAND))
    try:
        return dict(json.loads((r.stdout or "").strip().splitlines()[-1]), applied=r.returncode == 0)
    except Exception:
        return {"applied": False, "error": (r.stderr or r.stdout)[-200:]}


def log_line(**e):
    e = dict(at=datetime.now(timezone.utc).isoformat(timespec="seconds"), **e)
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    except OSError:
        pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lookup"); l.add_argument("text"); l.add_argument("--k", type=int, default=8); l.add_argument("--done", action="store_true")
    j = sub.add_parser("judge"); j.add_argument("--text", required=True); j.add_argument("--source", default="manual")
    j.add_argument("--k", type=int, default=8); j.add_argument("--apply", action="store_true"); j.add_argument("--dry", action="store_true")
    j.add_argument("--model", default="opus")
    a = ap.parse_args(argv)
    if a.cmd == "lookup":
        hits = match(a.text, a.k, a.done)
        for h in hits:
            print(f"{h.get('score', 0):.4f} {h.get('kind')} {h.get('id')} [{h.get('status')}] {str(h.get('title') or '')[:90]}")
        return 0
    hits = match(a.text, a.k)
    verdicts = judge(a.text, a.source, hits, a.model)
    for v in verdicts:
        res = apply(v, a.source, a.dry or not a.apply) if v.get("verdict") != "none" else {"applied": False}
        log_line(event="judged", source=a.source, id=v["id"], verdict=v.get("verdict"), due=v.get("due"), quote=v.get("quote"), why=v.get("why"), **{k: res[k] for k in res if k != "ok"})
        print(json.dumps(dict(v, **res), ensure_ascii=False))
    if not verdicts:
        log_line(event="no-candidates", source=a.source, hits=len(hits))
        print("no open to-do near this event")
    return 0


if __name__ == "__main__":
    sys.exit(main())
