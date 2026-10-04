"""G109 (5 Oct 2026): the map builder puts the rule loop's feedback box on both map pages and keeps it there; review_map.py
writes the observer's hit line for PROACTIVE H25. Everything on temp copies: the real map, ledger and rule-hits.jsonl are
never touched. Run: python -m pytest soda-brain/tools/tests/test_map_feedback_box.py -q"""
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
SYSTEM = TOOLS.parent / "system"
TL_SYS = Path.home() / "task-land" / "_system"
SYS_LINE = '<script src="feedback-box.js" data-surface="system-map"></script>'
SIM_LINE = '<script src="feedback-box.js" data-surface="simulation-map"></script>'


def _copies(tmp):
    for name in ("nodes.json", "SODA-SYSTEM-MAP.html", "SODA-SIMULATION-MAP.html"):
        shutil.copy(SYSTEM / name, tmp / name)
    env = dict(os.environ, SODA_LEDGER=str(tmp / "nodes.json"), SODA_MAP_HTML=str(tmp / "SODA-SYSTEM-MAP.html"),
               SODA_MAP_STAMP=str(tmp / ".stamp"), SODA_SIM_MAP_HTML=str(tmp / "SODA-SIMULATION-MAP.html"))
    return env


def _run(env, *args):
    r = subprocess.run([sys.executable, str(TOOLS / "build_map.py"), *args], env=env, capture_output=True, text=True,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return r.returncode, r.stdout


def test_builder_adds_the_box_once_and_keeps_it(tmp_path):
    env = _copies(tmp_path)
    for name, line in (("SODA-SYSTEM-MAP.html", SYS_LINE), ("SODA-SIMULATION-MAP.html", SIM_LINE)):   # start boxless
        p = tmp_path / name
        p.write_text(p.read_text(encoding="utf-8").replace(line + "\n", ""), encoding="utf-8", newline="\n")
    assert _run(env, "--check")[0] == 1                       # a page without its box is drift
    code, out = _run(env)
    assert code == 0, out
    for name, line in (("SODA-SYSTEM-MAP.html", SYS_LINE), ("SODA-SIMULATION-MAP.html", SIM_LINE)):
        html = (tmp_path / name).read_text(encoding="utf-8")
        assert html.count("feedback-box.js") == 1 and html.count(line) == 1
        assert html.index(line) < html.rindex("</body>")
    first = {n: (tmp_path / n).read_bytes() for n in ("SODA-SYSTEM-MAP.html", "SODA-SIMULATION-MAP.html")}
    code, out = _run(env)                                     # idempotent: a rebuild changes nothing
    assert json.loads(out.strip().splitlines()[-1]) == {"absorbed_from_html": [], "html_changed": False, "feedback_box_added": []}
    assert first == {n: (tmp_path / n).read_bytes() for n in first}
    assert _run(env, "--check") == (0, "the map is what the ledger renders\n")


def test_a_stale_surface_name_is_replaced(tmp_path):
    env = _copies(tmp_path)
    p = tmp_path / "SODA-SIMULATION-MAP.html"
    html = p.read_text(encoding="utf-8").replace(SIM_LINE + "\n", "")
    p.write_text(html.replace("</body>", '<script src="feedback-box.js" data-surface="sim-map"></script>\n</body>'),
                 encoding="utf-8", newline="\n")
    assert _run(env)[0] == 0
    html = p.read_text(encoding="utf-8")
    assert html.count("feedback-box.js") == 1 and SIM_LINE in html


def _review_map(tmp, with_rule=True):
    shutil.copy(TL_SYS / "PROACTIVE-CONTRACT.md", tmp / "PROACTIVE-CONTRACT.md")
    if not with_rule:
        led = tmp / "PROACTIVE-CONTRACT.md"
        led.write_text("\n".join(l for l in led.read_text(encoding="utf-8").splitlines() if not l.startswith("| H25 |")), encoding="utf-8")
    os.environ["TASKLAND_SYSTEM"] = str(tmp)
    sys.path.insert(0, str(TOOLS))
    import review_map
    return importlib.reload(review_map)


CLEAN = {k: [] for k in ("wires", "loose", "overflow", "gates", "overlaps", "outside", "console_errors", "page_hscroll")}


def test_observer_hit_line_ok_flag_and_none(tmp_path):
    rm = _review_map(tmp_path)
    ok = rm.hit_line({"light": dict(CLEAN), "dark": dict(CLEAN)}, "C:/x/SODA-SYSTEM-MAP.html")
    assert (ok["surface"], ok["rule"], ok["action"], ok["item"], ok["by"]) == ("proactive", "H25", "ok", "SODA-SYSTEM-MAP.html", "review_map.py")
    bad = rm.hit_line({"light": dict(CLEAN, wires=[{"from": "a"}]), "dark": dict(CLEAN, gates=[1, 2])}, "SODA-SIMULATION-MAP.html")
    assert bad["action"] == "flag" and bad["note"] == "3 findings: wires 1, gates 2"
    hits = tmp_path / "hits.jsonl"
    rm.log_hit(bad, hits)
    assert json.loads(hits.read_text(encoding="utf-8"))["action"] == "flag"
    rm2 = _review_map(tmp_path, with_rule=False)               # no ledger row = nothing is scored
    assert rm2.hit_line({"light": dict(CLEAN)}, "x.html") is None
    os.environ.pop("TASKLAND_SYSTEM", None)
