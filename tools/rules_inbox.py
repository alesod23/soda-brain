#!/usr/bin/env python3
"""rules_inbox.py: files the rules an orchestrator proposes in soda-brain/rules/inbox/, after his yes.

Runs on the box from cron every 5 minutes (as da). For each new `rules/inbox/*.md` (frontmatter: surface, rule, quote,
by, item, soft; see rules/inbox/README.md): post ONE hub card and remember its id. For each card already posted: read
its verdict (hub /item/<id>, else decisions.jsonl once the hub pruned it); yes -> addrule.py on that surface's ledger;
no -> declined; `change: <sentence>` in his feedback -> the changed sentence is filed. The outcome is appended to the
file under `## outcome` (the repo sync carries it back to GitHub). State: ~/.local/state/rules-inbox.json.

    rules_inbox.py tick [--dry-run]
"""
import json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(os.environ.get("BRAIN_REPO", "/home/da/soda-brain"))
INBOX = REPO / "rules" / "inbox"
STATE = Path(os.environ.get("RULES_INBOX_STATE", os.path.expanduser("~/.local/state/rules-inbox.json")))
HUB = os.environ.get("HUB_URL", "http://127.0.0.1:4180")
TASKLAND = Path(os.environ.get("TASKLAND", "/home/da/task-land"))
ADDRULE = TASKLAND / "_system" / "drafts" / "addrule.py"
DECISIONS = TASKLAND / "_system" / "decisions.jsonl"
PY = os.environ.get("ADDRULE_PY", "/home/da/triage/venv/bin/python")
SURFACES = {"email", "hub", "crm", "notif", "meeting"}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for ln in m.group(1).splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2)


def hub(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(HUB + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return 0, {"error": str(e)[:200]}


def last_decision(card_id):
    try:
        lines = DECISIONS.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for ln in reversed(lines):
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if str(d.get("item") or d.get("seq") or "") == str(card_id) or d.get("card") == card_id:
            return d
    return None


def append_outcome(path, lines):
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n## outcome\n" + "\n".join(lines) + "\n")


def tick(dry=False):
    state = {}
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        pass
    files = state.setdefault("files", {})
    changed = False
    INBOX.mkdir(parents=True, exist_ok=True)
    for p in sorted(INBOX.glob("*.md")):
        if p.name == "README.md":
            continue
        rec = files.get(p.name)
        if rec and rec.get("done"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "## outcome" in text and not rec:
            files[p.name] = {"done": True, "note": "outcome already present"}; changed = True
            continue
        meta, body = frontmatter(text)
        surface, rule = meta.get("surface", "").lower(), meta.get("rule", "")
        if surface not in SURFACES or not rule:
            if not rec:
                files[p.name] = {"done": True, "note": "unreadable: surface or rule missing"}; changed = True
                if not dry:
                    append_outcome(p, [f"- {now()} not filed: surface must be one of {sorted(SURFACES)} and rule must be present"])
            continue
        if not rec:
            # 1. post the card once
            quote, why = meta.get("quote", ""), body.strip()
            ctx = "\n".join(x for x in [f"proposed by: {meta.get('by', 'unknown')}", f"his words: {quote}" if quote else "", f"item: {meta.get('item')}" if meta.get("item") else "", f"soft: {meta.get('soft', 'false')}", "", why, "", f"file: rules/inbox/{p.name}", "yes = filed with addrule.py on the " + surface + " ledger; no + a sentence = declined; change: <sentence> = your sentence is filed"] if x is not None)
            card_text = f"{meta.get('by', 'the orchestrator')} proposes a rule ({surface}): {rule}"
            if dry:
                print("WOULD POST", card_text); continue
            st, r = hub("POST", "/pending", {"text": card_text[:600], "context": ctx[:4000], "notify": True, "kind": "decision", "origin": "rules-inbox"})
            if st == 200 and r.get("ok"):
                files[p.name] = {"card": r.get("id"), "seq": r.get("seq"), "posted": now(), "surface": surface, "rule": rule}; changed = True
                print("posted", p.name, "->", r.get("id"))
            else:
                print("hub refused", p.name, st, r)
            continue
        # 2. a card exists: look for his verdict
        card = rec.get("card")
        st, it = hub("GET", "/item/" + str(card))
        if st == 200 and isinstance(it, dict) and it.get("resolved"):
            verdict, fb = it.get("verdict"), str(it.get("feedback") or "")
        else:
            d = last_decision(card) if st != 200 else None
            if not d:
                continue
            verdict, fb = d.get("verdict"), str(d.get("feedback") or "")
        verdict = str(verdict or "").lower()
        if dry:
            print("WOULD FILE", p.name, verdict, fb); continue
        if verdict.startswith("y") or fb.lower().startswith("change:"):
            final = fb.split(":", 1)[1].strip() if fb.lower().startswith("change:") else rec["rule"]
            cmd = [PY, str(ADDRULE), "--contract", rec["surface"], "--rule", final, "--source", f"proposed by {meta.get('by', 'the orchestrator')} ({p.name}), his yes on card {card}"]
            if meta.get("quote"):
                cmd += ["--quote", meta["quote"]]
            if meta.get("item"):
                cmd += ["--item", meta["item"]]
            if str(meta.get("soft", "")).lower() in ("true", "1", "yes"):
                cmd += ["--soft"]
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(TASKLAND))
            out = (r.stdout + r.stderr).strip()[-600:]
            ok = r.returncode == 0
            append_outcome(p, [f"- {now()} {'filed' if ok else 'FAILED to file'} on the {rec['surface']} ledger (card {card}, verdict {verdict}{', changed: ' + final if final != rec['rule'] else ''})", f"- addrule: {out}"])
            files[p.name].update({"done": True, "filed": ok, "at": now()}); changed = True
            print("filed" if ok else "FAILED", p.name, out[:200])
        else:
            append_outcome(p, [f"- {now()} declined (card {card}, verdict {verdict}): {fb or 'no reason given'}"])
            files[p.name].update({"done": True, "filed": False, "at": now(), "feedback": fb}); changed = True
            print("declined", p.name, fb[:120])
    if changed and not dry:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")


if __name__ == "__main__":
    tick(dry="--dry-run" in sys.argv)
