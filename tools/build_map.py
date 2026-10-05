#!/usr/bin/env python3
"""build_map.py: the system ledger is the manual, the map is a view (his word, 4 Oct 2026 19:13: "we always need to
have somewhere a ledger that is up to date, not necessarily visualized in the HTML ... that always gets tapped into
whenever we make modifications to the system, which will become the manual that this agent uses").

THE LEDGER. `soda-brain/system/nodes.json` = {"about", "nodes": [ ... ]}, one object per node:
  display fields (what the map draws): id, label, kind, machine, cadence, code, reads, writes, llm, gate, status,
    broken, note, group (the comment heading in NODES)
  manual fields (what the System Agent reads): ports [{host, port}], tasks [name], paths [file or dir that must exist],
    owner, checks {<check key>: {probe, healthy_when, if_fails, known_fixes, rollback, files, escalate, his_command,
    for_him}}, last_verified, status_before_broken, hidden (true = in the ledger only, never drawn)

  build_map.py              render NODES in SODA-SYSTEM-MAP.html from nodes.json (between the NODES markers);
                            a node line edited by hand in the HTML since the last build is absorbed into the ledger first
                            (display fields only), so a session that edited the HTML loses nothing
  build_map.py --bootstrap  create nodes.json from the HTML's NODES once (ports/tasks/paths derived), merge runbooks
  build_map.py --check      exit 1 when the HTML is not what nodes.json renders (a test for the same-turn rule), or when
                            a map page lost its feedback box
FEEDBACK BOX (goal run G109, 5 Oct 2026; RULE-LOOP.md section 7 part 3). Every render also makes sure each map page in
FEEDBACK_PAGES carries ONE `<script src="feedback-box.js" data-surface="...">` line right before </body> (the system map
as surface system-map, the hand-written simulation map as simulation-map; ledger_verdict.SURFACE_LEDGER routes both), so
no rebuild or hand edit of the page can drop the box. Env SODA_SIM_MAP_HTML overrides the simulation map's path (tests).

The System Agent (task-land/_system/system-agent/) writes `status`/`broken` through registry.map_sync(), which edits
nodes.json and calls render(). Idempotent: the same ledger gives the same HTML byte for byte.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SYSTEM = Path(__file__).resolve().parent.parent / "system"
LEDGER = Path(os.environ.get("SODA_LEDGER") or (SYSTEM / "nodes.json"))
HTML = Path(os.environ.get("SODA_MAP_HTML") or (SYSTEM / "SODA-SYSTEM-MAP.html"))
STAMP = Path(os.environ.get("SODA_MAP_STAMP") or (SYSTEM / ".nodes-render.sha"))
SIM_HTML = Path(os.environ.get("SODA_SIM_MAP_HTML") or (SYSTEM / "SODA-SIMULATION-MAP.html"))
FEEDBACK_PAGES = ((HTML, "system-map"), (SIM_HTML, "simulation-map"))   # page -> data-surface of its feedback box
DISPLAY = ["label", "kind", "machine", "cadence", "code", "reads", "writes", "llm", "gate", "status", "broken", "note"]
NODE_LINE = re.compile(r'^(?P<id>[a-z][a-z0-9_]*):\{(?P<body>.*)\},\s*$')
PAIR = re.compile(r'([a-z_]+):"((?:[^"\\]|\\.)*)"')


def js(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def unjs(v):
    return re.sub(r'\\(.)', r'\1', v)


def parse_block(html):
    """-> (start, end, [(group, id, {display fields in order})]) of the NODES literal in the HTML."""
    a = html.index("const NODES = {")
    b = html.index("\n};", a)
    out, group = [], None
    for ln in html[a:b].split("\n")[1:]:
        if ln.startswith("//"):
            group = ln[2:].strip(); continue
        m = NODE_LINE.match(ln)
        if m:
            out.append((group, m.group("id"), {k: unjs(v) for k, v in PAIR.findall(m.group("body"))}))
    return a, b, out


def node_line(n):
    return n["id"] + ":{" + ",".join(f"{k}:{js(n[k])}" for k in DISPLAY if n.get(k) not in (None,)) + "},"


def render_block(nodes):
    L, group = ["const NODES = {", "// generated from soda-brain/system/nodes.json by soda-brain/tools/build_map.py: edit the ledger, not this block"], object()
    for n in nodes:
        if n.get("hidden"):
            continue
        if n.get("group") != group:
            group = n.get("group")
            if group:
                L.append("// " + group)
        L.append(node_line(n))
    return "\n".join(L)


def load():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(led):
    tmp = LEDGER.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, LEDGER)


def absorb(led, html):
    """Node lines edited by hand in the HTML since the last render go into the ledger (display fields), new nodes too."""
    a, b, rows = parse_block(html)
    cur = hashlib.sha1(html[a:b].encode("utf-8")).hexdigest()
    last = STAMP.read_text().strip() if STAMP.exists() else None
    if last == cur:
        return []
    by = {n["id"]: n for n in led["nodes"]}
    changed = []
    for group, nid, f in rows:
        n = by.get(nid)
        if not n:
            n = {"id": nid, "group": group}
            led["nodes"].append(n); by[nid] = n; changed.append(nid + " (new)")
        for k in DISPLAY:
            if k in ("status", "broken") and n.get("broken") and k == "status":
                continue          # the registry owns broken nodes
            if f.get(k) != n.get(k) and not (k == "broken"):
                if f.get(k) is None:
                    n.pop(k, None)
                else:
                    n[k] = f[k]
                changed.append(f"{nid}.{k}")
    return changed


def feedback_line(surface):
    return f'<script src="feedback-box.js" data-surface="{surface}"></script>'


def with_feedback_box(html, surface):
    """-> html carrying exactly one feedback-box include for `surface`, right before </body> (idempotent)."""
    line = feedback_line(surface)
    if line in html:
        return html
    html = re.sub(r'[ \t]*<script src="feedback-box\.js"[^>]*></script>\n?', "", html)   # a stale surface name
    i = html.rindex("</body>")
    return html[:i] + line + "\n" + html[i:]


def ensure_feedback_boxes(write=True):
    """The pages of FEEDBACK_PAGES other than the system map (rendered by render()) -> [pages that lacked the box]."""
    out = []
    for page, surface in FEEDBACK_PAGES:
        if page == HTML or not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        new = with_feedback_box(html, surface)
        if new != html:
            out.append(page.name)
            if write:
                page.write_text(new, encoding="utf-8", newline="\n")
    return out


def render(led=None, write=True):
    """-> (changed?, html). Writes the HTML and the stamp when changed."""
    led = led or load()
    html = HTML.read_text(encoding="utf-8")
    a, b, _ = parse_block(html)
    new = with_feedback_box(html[:a] + render_block(led["nodes"]) + html[b:], dict(FEEDBACK_PAGES).get(HTML, "system-map"))   # HTML may be repointed (registry.map_sync, tests)
    if write and new != html:
        HTML.write_text(new, encoding="utf-8", newline="\n")
    if write:
        a2, b2, _ = parse_block(new)
        STAMP.write_text(hashlib.sha1(new[a2:b2].encode("utf-8")).hexdigest())
    return new != html, new


# ------------------------------------------------------------------ bootstrap (once)
def derive(n):
    """ports / tasks / paths from the display text, conservatively (the drift check trusts these)."""
    txt = " ".join(str(n.get(k) or "") for k in ("label", "cadence", "code"))
    ports = sorted({int(p) for p in re.findall(r":(\d{4})\b", n.get("label") or "")})
    host = "127.0.0.1" if n.get("machine") == "laptop" else "box"
    tasks = sorted(set(re.findall(r"\btask ([A-Z][A-Za-z0-9-]+)", n.get("cadence") or "")))
    if n["id"].startswith("w_") and re.fullmatch(r"[A-Z][A-Za-z0-9-]+", (n.get("label") or "").split(" ")[0]):
        tasks = sorted(set(tasks) | {n["label"].split(" ")[0]})
    paths = []
    for part in re.split(r"[,;]\s*", n.get("code") or ""):
        p = part.strip().split(" ")[0]
        if n.get("machine") == "laptop" and re.match(r"^(~/|task-land/|gtm-eng/|\.medtech-crm/|soda-brain/|\.claude/|tundra-design/|cdtm-taskforce/|tundra-outreach/)", p) and not re.search(r"[<>{}*]", p):
            paths.append(p if p.startswith("~/") else "~/" + p)
        if n.get("machine") == "box" and p.startswith("/home/da/") and not re.search(r"[<>{}*]", p):
            paths.append(p)
    out = {}
    if ports:
        out["ports"] = [{"host": host, "port": p} for p in ports]
    if tasks:
        out["tasks"] = tasks
    if paths:
        out["paths"] = paths
    return out


def bootstrap(runbooks_path=None):
    html = HTML.read_text(encoding="utf-8")
    _, _, rows = parse_block(html)
    nodes = []
    for group, nid, f in rows:
        n = {"id": nid, "group": group, **f}
        n.update(derive(n))
        nodes.append(n)
    led = {"about": "THE SYSTEM LEDGER (his word 4 Oct 2026 19:13): the manual the System Agent reads and the source the map renders. "
                    "Every session that changes a service, port, job, store or rule edits THIS file the same turn, then runs "
                    "python soda-brain/tools/build_map.py. Fields: see the docstring of tools/build_map.py.",
           "nodes": nodes}
    if runbooks_path and Path(runbooks_path).exists():
        rb = json.loads(Path(runbooks_path).read_text(encoding="utf-8"))
        by = {n["id"]: n for n in nodes}
        for key, e in rb.items():
            if key.startswith("_") or not isinstance(e, dict):
                continue
            nid = e.get("node") or e.get("ledger_node")
            if nid not in by:
                continue
            c = {k: v for k, v in e.items() if k not in ("node", "ledger_node")}
            if "expected" in c:
                c["healthy_when"] = c.pop("expected")
            by[nid].setdefault("checks", {})[key] = c
    return led


def main():
    if "--bootstrap" in sys.argv:
        if LEDGER.exists() and "--force" not in sys.argv:
            print(f"{LEDGER} exists: not bootstrapped again"); return 1
        rb = sys.argv[sys.argv.index("--runbooks") + 1] if "--runbooks" in sys.argv else None
        led = bootstrap(rb)
        save(led)
        print(f"ledger written: {len(led['nodes'])} nodes")
        return 0
    led = load()
    if "--check" in sys.argv:
        ch, _ = render(led, write=False)
        boxless = ensure_feedback_boxes(write=False)
        print("the map is what the ledger renders" if not ch else "DRIFT: the map's NODES (or its feedback box) differ from nodes.json (run build_map.py)")
        if boxless:
            print("DRIFT: no feedback box on " + ", ".join(boxless) + " (run build_map.py)")
        return 1 if ch or boxless else 0
    ab = absorb(led, HTML.read_text(encoding="utf-8"))
    if ab:
        save(led)
    ch, _ = render(led)
    print(json.dumps({"absorbed_from_html": ab, "html_changed": ch, "feedback_box_added": ensure_feedback_boxes()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
