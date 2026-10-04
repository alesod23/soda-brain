"""Per-record merge of two diverged copies of the coattio crm.json (laptop writer vs box replica).

    python crm_merge_conflict.py --laptop crm.json --box crm.conflict-box-<stamp>.json \
        --out merged.json --log merge-log.jsonl [--write-api http://127.0.0.1:4124]

Dry run by default: nothing is written anywhere but --out and --log. `--write-api` PUTs the merged
document to <url>/api/data (the one CRM writer, server.js writeLive) and is a separate decision.
Pure Python, no third-party deps, utf-8 everywhere. Splitter: crm_diff.split_doc (same keys, same
handling of the three id-less people and the duplicated ids).

Rules, per person present on both sides, per field whose values differ (absent == null):
  R1 clock      a side's clock is the `at` of its newest activity entry (no row carries updated_at,
                no activity entry carries an id in either file). The later clock wins the field.
                Equal clocks = TIE: the laptop (the writer, AGENTS.md contract 4) wins and the line
                is flagged rule="tie" so it can be reviewed.
  R2 step       the STEP bundle (next_step, next_step_origin, next_step_default, postpone_days,
                relationship_state) moves as one unit: the side with the later next_step_origin.at
                wins all of it, so a step never travels without its origin; no origin -> R1.
  R3 stamped    a field whose value carries its own write time (dict with updated_at / at, or one of
                WRITE_TS_FIELDS) is decided by that time; a null side is dated at its clock (R1).
                The notion_* fields follow notion_synced_at as one bundle.
  R4 activity   union, multiset, order kept. Key = (at, event) when the entry carries an event id
                (the monitor's lines: linkedin:li:..., mail:..., wa:...), else (at, type, detail).
                The winner's list is the spine, the loser's missing entries are inserted before their
                nearest older shared neighbour. One event id present on both sides with a different
                reading (the box's "Replied via linkedin" vs the laptop's corrected "LinkedIn DM
                sent") is one event: the winner's reading is kept, the loser's dropped and logged.
                The list is then capped at ACTIVITY_CAP = 50 newest-first (model.js pushActivity),
                dropped entries logged.
  R5 ids        identifier_candidates: union by (kind, value), winner's order first.
  R6 rest       everything else: R1.
Rows on one side only are kept as they are. Companies (without people), templates and signals are
merged by key: differing field -> laptop, logged; box-only records appended. meta: laptop wins,
box-only keys added. Document order = the laptop's, box-only records appended at the end.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crm_diff import split_doc  # noqa: E402

STEP_BUNDLE = ("next_step", "next_step_origin", "next_step_default", "postpone_days", "relationship_state")
NOTION_BUNDLE = ("notion_last_touch", "notion_stage", "notion_category", "notion_contact_id", "notion_link_mode")
WRITE_TS_FIELDS = {"li_checked_at", "email_checked_at", "notion_synced_at", "handoff_card_at", "handoff_resolved_at", "meeting_detected_at"}
ACTIVITY_CAP = 50  # model.js ACTIVITY_CAP
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def parse_ts(v: Any) -> datetime | None:
    if not isinstance(v, str) or not v.strip():
        return None
    s = v.strip().replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        try:
            d = datetime.fromisoformat(s[:10])
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def clock(p: dict) -> datetime:
    best = EPOCH
    for a in p.get("activity") or []:
        if isinstance(a, dict):
            t = parse_ts(a.get("at"))
            if t and t > best:
                best = t
    return best


def value_ts(v: Any, field: str) -> datetime | None:
    if isinstance(v, dict):
        return parse_ts(v.get("updated_at")) or parse_ts(v.get("at"))
    if field in WRITE_TS_FIELDS:
        return parse_ts(v)
    return None


def act_key(a: Any) -> tuple:
    if not isinstance(a, dict):
        return ("raw", json.dumps(a, sort_keys=True, ensure_ascii=False))
    if a.get("event") and a.get("at"):
        return ("event", a.get("at"), a.get("event"))
    return (a.get("at"), a.get("type"), a.get("detail"))


class Merger:
    def __init__(self, log_path: Path) -> None:
        self.lines: list[dict] = []
        self.log_path = log_path
        self.stats: Counter = Counter()
        self.field_wins: Counter = Counter()
        self.ties: list[dict] = []
        self.step_text_conflicts: list[dict] = []

    def log(self, **line: Any) -> None:
        self.lines.append(line)

    # ---- person ------------------------------------------------------------------------------
    def merge_person(self, key: str, lp: dict, bp: dict) -> dict:
        lc, bc = clock(lp), clock(bp)
        if lc == bc:
            winner, rule_r1 = "laptop", "tie"
        else:
            winner, rule_r1 = ("laptop" if lc > bc else "box"), "clock"
        name = lp.get("name") or bp.get("name")
        out: dict = {}
        fields = list(lp.keys()) + [k for k in bp.keys() if k not in lp]
        lo, bo = lp.get("next_step_origin"), bp.get("next_step_origin")
        lot, bot = (parse_ts(lo.get("at")) if isinstance(lo, dict) else None) or lc, (parse_ts(bo.get("at")) if isinstance(bo, dict) else None) or bc
        step_winner, step_rule = (winner, rule_r1) if lot == bot else (("laptop" if lot > bot else "box"), "step_origin")
        ln, bn = parse_ts((lp.get("notion_synced_at"))) or lc, parse_ts(bp.get("notion_synced_at")) or bc
        notion_winner, notion_rule = (winner, rule_r1) if ln == bn else (("laptop" if ln > bn else "box"), "stamped:notion_synced_at")
        tied_here = False
        for f in fields:
            lv, bv = lp.get(f), bp.get(f)
            if lv == bv:
                out[f] = copy.deepcopy(lv)
                continue
            if f == "activity":
                out[f] = self.merge_activity(key, name, lv or [], bv or [], winner)
                continue
            if f == "identifier_candidates":
                out[f] = self.union_ids(key, name, lv or [], bv or [], winner)
                continue
            if f in STEP_BUNDLE:
                w, rule, why = step_winner, step_rule, f"next_step_origin.at laptop={lot.isoformat()} box={bot.isoformat()}"
            elif f in NOTION_BUNDLE or f == "notion_synced_at":
                w, rule, why = notion_winner, notion_rule, f"notion_synced_at laptop={ln.isoformat()} box={bn.isoformat()}"
            else:
                lt, bt = value_ts(lv, f), value_ts(bv, f)
                if lt or bt:
                    lt, bt = lt or lc, bt or bc
                    if lt == bt:
                        w, rule = winner, rule_r1
                    else:
                        w, rule = ("laptop" if lt > bt else "box"), "stamped"
                    why = f"value time laptop={lt.isoformat()} box={bt.isoformat()} (a null side is dated at its clock)"
                else:
                    w, rule, why = winner, rule_r1, f"clock laptop={lc.isoformat()} box={bc.isoformat()}"
            out[f] = copy.deepcopy(lv if w == "laptop" else bv)
            self.field_wins[(f, w, rule)] += 1
            if rule == "tie":
                tied_here = True
            if f == "next_step":
                lt_, bt_ = (lv or {}).get("text") if isinstance(lv, dict) else None, (bv or {}).get("text") if isinstance(bv, dict) else None
                if lt_ != bt_:
                    self.step_text_conflicts.append({"key": key, "name": name, "laptop": lv, "box": bv, "chosen": w, "rule": rule})
            self.log(kind="field", table="people", key=key, name=name, field=f, winner=w, rule=rule, why=why, laptop=lv, box=bv)
        if tied_here:
            self.ties.append({"key": key, "name": name, "clock": lc.isoformat()})
        return out

    def merge_activity(self, key: str, name: str | None, la: list, ba: list, winner: str) -> list:
        win, lose = (la, ba) if winner == "laptop" else (ba, la)
        wk = Counter(act_key(a) for a in win)
        by_key: dict[tuple, list] = defaultdict(list)
        for a in win:
            by_key[act_key(a)].append(a)
        dropped: list = []   # same event id on both sides, other reading on the loser: not re-added
        missing: list[tuple[int, dict]] = []
        seen: Counter = Counter()
        for i, a in enumerate(lose):
            k = act_key(a)
            seen[k] += 1
            if seen[k] <= wk.get(k, 0):
                twin = by_key[k][seen[k] - 1]
                if (twin.get("type"), twin.get("detail")) != (a.get("type"), a.get("detail")):
                    dropped.append({"loser": a, "kept": twin})
                continue
            missing.append((i, a))
        merged = list(win)
        for i, a in missing:
            # nearest older shared neighbour in the loser list -> insert before it in the merged list
            pos = len(merged)
            for j in range(i + 1, len(lose)):
                k = act_key(lose[j])
                if wk.get(k, 0):
                    idx = next((n for n, m in enumerate(merged) if act_key(m) == k), None)
                    if idx is not None:
                        pos = idx
                        break
            merged.insert(pos, copy.deepcopy(a))
        capped = merged[ACTIVITY_CAP:]
        merged = merged[:ACTIVITY_CAP]
        self.stats["activity_added_from_" + ("box" if winner == "laptop" else "laptop")] += len(missing)
        self.stats["activity_same_event_other_reading_dropped"] += len(dropped)
        self.stats["activity_capped"] += len(capped)
        self.log(kind="activity", table="people", key=key, name=name, spine=winner, laptop_n=len(la), box_n=len(ba), merged_n=len(merged),
                 added_from_loser=[a for _, a in missing], dropped_same_event=dropped, capped=capped)
        return merged

    def union_ids(self, key: str, name: str | None, li: list, bi: list, winner: str) -> list:
        win, lose = (li, bi) if winner == "laptop" else (bi, li)
        out = list(copy.deepcopy(win))
        have = {(c.get("kind"), c.get("value")) for c in out if isinstance(c, dict)}
        added = [c for c in lose if isinstance(c, dict) and (c.get("kind"), c.get("value")) not in have]
        out.extend(copy.deepcopy(added))
        self.log(kind="identifier_candidates", table="people", key=key, name=name, spine=winner, added_from_loser=added)
        return out

    # ---- flat records (company without people, template, signal) -------------------------------
    def merge_flat(self, table: str, key: str, ld: dict, bd: dict) -> dict:
        out: dict = {}
        for f in list(ld.keys()) + [k for k in bd.keys() if k not in ld]:
            lv, bv = ld.get(f), bd.get(f)
            out[f] = copy.deepcopy(lv if f in ld else bv)
            if lv != bv:
                self.field_wins[(table + "." + f, "laptop" if f in ld else "box", "laptop-wins" if f in ld else "box-only-key")] += 1
                self.log(kind="field", table=table, key=key, field=f, winner="laptop" if f in ld else "box",
                         rule="laptop-wins" if f in ld else "box-only-key", why="no clock on " + table, laptop=lv, box=bv)
        return out

    def write_log(self, summary: dict) -> None:
        with self.log_path.open("w", encoding="utf-8") as fh:
            for line in self.lines:
                fh.write(json.dumps(line, ensure_ascii=False) + "\n")
            fh.write(json.dumps({"kind": "summary", **summary}, ensure_ascii=False) + "\n")


def merge(laptop: dict, box: dict, log_path: Path) -> tuple[dict, dict]:
    m = Merger(log_path)
    sl, sb = split_doc(laptop), split_doc(box)
    # ---- people
    people: dict[str, dict] = {}
    company_of: dict[str, str] = {}
    only_laptop = [k for k in sl["people"] if k not in sb["people"]]
    only_box = [k for k in sb["people"] if k not in sl["people"]]
    changed: list[str] = []
    for k, lr in sl["people"].items():
        br = sb["people"].get(k)
        if br is None:
            people[k] = copy.deepcopy(lr["data"])
            company_of[k] = lr["company_id"]
            continue
        if lr["sha"] == br["sha"]:
            people[k] = copy.deepcopy(lr["data"])
            company_of[k] = lr["company_id"]
            continue
        if (lr.get("name") or "") != (br.get("name") or ""):
            m.log(kind="warning", table="people", key=k, why="same key, different name", laptop=lr.get("name"), box=br.get("name"))
        changed.append(k)
        people[k] = m.merge_person(k, lr["data"], br["data"])
        if lr["company_id"] != br["company_id"]:
            w = "laptop" if clock(lr["data"]) >= clock(br["data"]) else "box"
            m.log(kind="field", table="people", key=k, field="company_id", winner=w, rule="clock", why="row moved between companies", laptop=lr["company_id"], box=br["company_id"])
            company_of[k] = lr["company_id"] if w == "laptop" else br["company_id"]
        else:
            company_of[k] = lr["company_id"]
    for k in only_box:
        people[k] = copy.deepcopy(sb["people"][k]["data"])
        company_of[k] = sb["people"][k]["company_id"]
        m.log(kind="row", table="people", key=k, name=sb["people"][k].get("name"), side="box-only", company=company_of[k])
    for k in only_laptop:
        m.log(kind="row", table="people", key=k, name=sl["people"][k].get("name"), side="laptop-only", company=company_of[k])
    # ---- companies
    companies: dict[str, dict] = {}
    for k, lr in sl["companies"].items():
        br = sb["companies"].get(k)
        companies[k] = copy.deepcopy(lr["data"]) if br is None or lr["sha"] == br["sha"] else m.merge_flat("companies", k, lr["data"], br["data"])
    for k, br in sb["companies"].items():
        if k not in companies:
            companies[k] = copy.deepcopy(br["data"])
            m.log(kind="row", table="companies", key=k, side="box-only")
    for k in sl["companies"]:
        if k not in sb["companies"]:
            m.log(kind="row", table="companies", key=k, side="laptop-only")
    # people into companies, laptop order first
    by_company: dict[str, list] = defaultdict(list)
    for k in list(sl["people"]) + only_box:
        by_company[company_of[k]].append(people[k])
    doc: dict = {}
    for top in laptop:
        if top not in ("companies", "templates", "signals", "meta"):
            doc[top] = copy.deepcopy(laptop[top])
    meta = copy.deepcopy(laptop.get("meta") or {})
    for mk, mv in (box.get("meta") or {}).items():
        if mk not in meta:
            meta[mk] = copy.deepcopy(mv)
            m.log(kind="field", table="meta", field=mk, winner="box", rule="box-only-key", laptop=None, box=mv)
        elif meta[mk] != mv:
            m.log(kind="field", table="meta", field=mk, winner="laptop", rule="laptop-wins", laptop=meta[mk], box=mv)
    doc["meta"] = meta
    for table in ("templates", "signals"):
        out_list: list = []
        for k, lr in sl[table].items():
            br = sb[table].get(k)
            out_list.append(copy.deepcopy(lr["data"]) if br is None or lr["sha"] == br["sha"] else m.merge_flat(table, k, lr["data"], br["data"]))
        for k, br in sb[table].items():
            if k not in sl[table]:
                out_list.append(copy.deepcopy(br["data"]))
                m.log(kind="row", table=table, key=k, side="box-only")
        doc[table] = out_list
    doc["companies"] = []
    for k, cdata in companies.items():
        c = dict(cdata)
        c["people"] = by_company.get(k, [])
        doc["companies"].append(c)
    # keep the laptop's top-level key order
    ordered = {top: doc[top] for top in laptop if top in doc}
    for top in doc:
        ordered.setdefault(top, doc[top])
    summary = {
        "people": {"laptop": len(sl["people"]), "box": len(sb["people"]), "merged": len(people)},
        "companies": {"laptop": len(sl["companies"]), "box": len(sb["companies"]), "merged": len(companies)},
        "templates": {"laptop": len(sl["templates"]), "box": len(sb["templates"]), "merged": len(ordered["templates"])},
        "signals": {"laptop": len(sl["signals"]), "box": len(sb["signals"]), "merged": len(ordered["signals"])},
        "people_only_laptop": only_laptop, "people_only_box": only_box,
        "companies_only_laptop": [k for k in sl["companies"] if k not in sb["companies"]],
        "companies_only_box": [k for k in sb["companies"] if k not in sl["companies"]],
        "people_changed": len(changed),
        "field_wins": [{"field": f, "winner": w, "rule": r, "n": n} for (f, w, r), n in sorted(m.field_wins.items(), key=lambda x: -x[1])],
        "ties_laptop_chosen": m.ties,
        "next_step_text_conflicts": m.step_text_conflicts,
        "activity": dict(m.stats),
    }
    m.write_log(summary)
    return ordered, summary


def diff_vs(laptop: dict, merged: dict) -> dict:
    """Exact per-field diff of the merged document against the laptop file, by split key."""
    sl, sm = split_doc(laptop), split_doc(merged)
    out: dict = {"people_added": [k for k in sm["people"] if k not in sl["people"]],
                 "people_removed": [k for k in sl["people"] if k not in sm["people"]],
                 "companies_added": [k for k in sm["companies"] if k not in sl["companies"]],
                 "people_changed": {}, "field_counter": {}}
    fc: Counter = Counter()
    for k, lr in sl["people"].items():
        mr = sm["people"].get(k)
        if mr is None or mr["sha"] == lr["sha"]:
            continue
        fields = sorted(f for f in set(lr["data"]) | set(mr["data"]) if lr["data"].get(f) != mr["data"].get(f))
        out["people_changed"][k] = fields
        fc.update(fields)
    out["field_counter"] = dict(fc.most_common())
    for table in ("companies", "templates", "signals"):
        out[table + "_changed"] = [k for k, lr in sl[table].items() if k in sm[table] and sm[table][k]["sha"] != lr["sha"]]
    out["meta_changed"] = laptop.get("meta") != merged.get("meta")
    return out


def put_api(base: str, doc: dict) -> str:
    import urllib.request
    body = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")
    req = urllib.request.Request(base.rstrip("/") + "/api/data", data=body, method="PUT", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--laptop", required=True)
    ap.add_argument("--box", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--write-api", default=None, help="PUT the merged document to <url>/api/data (separate decision; off by default)")
    a = ap.parse_args(argv)
    laptop = json.loads(Path(a.laptop).read_text(encoding="utf-8-sig"))
    box = json.loads(Path(a.box).read_text(encoding="utf-8-sig"))
    merged, summary = merge(laptop, box, Path(a.log))
    Path(a.out).write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    d = diff_vs(laptop, merged)
    print(json.dumps({"summary": summary, "diff_vs_laptop": {k: v for k, v in d.items() if k != "people_changed"},
                      "people_changed_vs_laptop": len(d["people_changed"])}, ensure_ascii=False, indent=1))
    print(f"merged -> {a.out}\nlog    -> {a.log}")
    if a.write_api:
        print("PUT", a.write_api, "->", put_api(a.write_api, merged))
    else:
        print("dry run: nothing written to the CRM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
