#!/usr/bin/env python3
"""The review mechanism for soda-brain/system/SODA-SYSTEM-MAP.html (his rule 4 Oct 2026: "put a review mechanism that
actually meant you sure you outputted something that is readable ... Continue until loop until you have all those minor
details fixed"). Renders the page headless (Playwright Chromium, 1568 px wide), then CHECKS, not looks:

  1. no wire runs through a node it does not start or end at (every path sampled every 3 px against every node box);
  2. nothing is clipped horizontally (scrollWidth > clientWidth on a node, a chip, a lane header, a table cell);
  3. every gate label is centred in its hexagon (text box centre within 3 px of the node centre);
  4. no two nodes overlap; no node sticks out of its chart;
  5. no console error;
and writes full-page + per-chart screenshots to --out so a human look follows the checks, in light and dark theme.
With --phone N (e.g. 390) it also renders at that width in both themes, screenshots the full page and checks that the
page itself never scrolls sideways (a chart may scroll inside its own box). Exit 0 only when every check passes.

    python soda-brain/tools/review_map.py [--html <path>] [--out <dir>] [--charts id,id] [--sections id,id] [--phone 390]

The defaults screenshot the system map's charts and sections; another page in the same family (the simulation map,
4 Oct 2026) names its own ids.
"""
import argparse
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_HTML = HERE.parent / "system" / "SODA-SYSTEM-MAP.html"

CHECK_JS = r"""
() => {
  const out = {wires: [], loose: [], overflow: [], gates: [], overlaps: [], outside: []};
  const charts = [...document.querySelectorAll('.chart')];
  for (const chart of charts) {
    const grid = chart.querySelector('.grid'); const svg = chart.querySelector('svg.wires'); if (!grid || !svg) continue;
    const cb = grid.getBoundingClientRect();
    // path points are in the SVG's own box; the grid may sit elsewhere (the full-width chart centres it): convert
    const sb = svg.getBoundingClientRect(); const dx = sb.left - cb.left, dy = sb.top - cb.top;
    const nodes = [...grid.querySelectorAll('.node')].filter(n => !n.hidden).map(n => { const r = n.getBoundingClientRect(); return {id: n.dataset.id, l: r.left - cb.left, r: r.right - cb.left, t: r.top - cb.top, b: r.bottom - cb.top}; });
    const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
    const inside = (x, y, n, tol) => x > n.l + tol && x < n.r - tol && y > n.t + tol && y < n.b - tol;
    for (const p of svg.querySelectorAll('path.w')) {
      const len = p.getTotalLength(); const a = p.dataset.a, b = p.dataset.b; const hits = new Set();
      for (let s = 0; s <= len; s += 3) { const pt = p.getPointAtLength(s); for (const n of nodes) { if (n.id === a || n.id === b) continue; if (inside(pt.x + dx, pt.y + dy, n, 1)) hits.add(n.id); } }
      if (hits.size) out.wires.push({chart: chart.id, from: a, to: b, through: [...hits]});
      // 6. every wire starts on the edge of its source and ends on the edge of its target (an arrow into empty space
      //    is what the machines chart showed on 4 Oct: the SVG spanned the chart while the grid was centred inside it)
      const s0 = p.getPointAtLength(0), e0 = p.getPointAtLength(len); const A = byId[a], B = byId[b];
      const onEdge = (pt, n) => n && Math.abs(pt.y - n.t) + 0 >= 0 && pt.y >= n.t - 1 && pt.y <= n.b + 1 && (Math.abs(pt.x - n.l) < 2 || Math.abs(pt.x - n.r) < 2);
      if (!onEdge({x: s0.x + dx, y: s0.y + dy}, A) || !onEdge({x: e0.x + dx, y: e0.y + dy}, B)) out.loose.push({chart: chart.id, from: a, to: b, start: [Math.round(s0.x + dx), Math.round(s0.y + dy)], end: [Math.round(e0.x + dx), Math.round(e0.y + dy)]});
    }
    for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) { const A = nodes[i], B = nodes[j]; if (A.l < B.r - 1 && B.l < A.r - 1 && A.t < B.b - 1 && B.t < A.b - 1) out.overlaps.push({chart: chart.id, a: A.id, b: B.id}); }
    const chartR = chart.getBoundingClientRect();
    for (const n of nodes) { if (n.l + cb.left < chartR.left - 1 || n.r + cb.left > chartR.right + chart.scrollWidth - chart.clientWidth + 1) out.outside.push({chart: chart.id, id: n.id}); }
    for (const g of grid.querySelectorAll('.node.gate')) { const l = g.querySelector('.l'); if (!l) continue; const gr = g.getBoundingClientRect(); const range = document.createRange(); range.selectNodeContents(l); const tr = range.getBoundingClientRect(); const dx = (tr.left + tr.right) / 2 - (gr.left + gr.right) / 2; if (Math.abs(dx) > 3) out.gates.push({chart: chart.id, id: g.dataset.id, dx: Math.round(dx)}); }
  }
  for (const el of document.querySelectorAll('.node, .node .chips span, .lane-h, td, .legend .item, .sample, .flow h3, .chain .node, .chain .arrow span')) {
    if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).textOverflow !== 'ellipsis') out.overflow.push({tag: el.tagName, cls: el.className, text: (el.textContent || '').trim().slice(0, 60), sw: el.scrollWidth, cw: el.clientWidth});
  }
  out.counts = {charts: charts.length, nodes: document.querySelectorAll('.node').length, wires: document.querySelectorAll('path.w').length, rows: document.querySelectorAll('#wtable tbody tr').length};
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default=str(DEFAULT_HTML))
    ap.add_argument("--out", default=str(HERE.parent / "system" / "_review"))
    ap.add_argument("--width", type=int, default=1568)
    ap.add_argument("--charts", default="chart-shape,chart-machines", help="ids of the elements screenshotted one by one")
    ap.add_argument("--sections", default="flows,surfaces,workers", help="ids of the sections screenshotted one by one")
    ap.add_argument("--phone", type=int, default=0, help="also render at this width (390) and check the page does not scroll sideways")
    a = ap.parse_args()
    charts = [c for c in a.charts.split(",") if c]; sections = [c for c in a.sections.split(",") if c]
    from playwright.sync_api import sync_playwright
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    url = pathlib.Path(a.html).resolve().as_uri()
    report = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for theme in ("light", "dark"):
            pg = br.new_page(viewport={"width": a.width, "height": 900}, color_scheme=theme)
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            pg.goto(url); pg.wait_for_timeout(1200)
            pg.evaluate("document.fonts && document.fonts.ready"); pg.wait_for_timeout(400)
            res = pg.evaluate(CHECK_JS); res["console_errors"] = errors
            pg.screenshot(path=str(out / f"full-{theme}.png"), full_page=True)
            for cid in charts:
                el = pg.query_selector("#" + cid)
                if el: el.screenshot(path=str(out / f"{cid}-{theme}.png"))
            for sec in sections:
                el = pg.query_selector("#" + sec)
                if el: el.screenshot(path=str(out / f"{sec}-{theme}.png"))
            res["page_hscroll"] = []
            report[theme] = res
            pg.close()
            if a.phone:
                pg = br.new_page(viewport={"width": a.phone, "height": 844}, color_scheme=theme)
                perr = []
                pg.on("pageerror", lambda e: perr.append(str(e)))
                pg.goto(url); pg.wait_for_timeout(1200)
                sw = pg.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                if sw[0] > sw[1] + 1: res["page_hscroll"].append({"width": a.phone, "scrollWidth": sw[0]})
                res["console_errors"] += perr
                pg.screenshot(path=str(out / f"phone{a.phone}-{theme}.png"), full_page=True)
                pg.close()
        br.close()
    (out / "report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    bad = 0
    for theme, res in report.items():
        for k in ("wires", "loose", "overflow", "gates", "overlaps", "outside", "console_errors", "page_hscroll"):
            n = len(res[k]); bad += n
            print(f"{theme:5} {k:15} {n}")
            for item in res[k][:12]: print("      ", json.dumps(item, ensure_ascii=False)[:200])
        print(f"{theme:5} counts          {res['counts']}")
    print("screenshots ->", out)
    print("RESULT:", "CLEAN" if bad == 0 else f"{bad} findings")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
