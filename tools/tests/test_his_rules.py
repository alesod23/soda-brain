"""his_rules (RULE-LOOP "The template of a loop", part 6): the brain answers "what does he like / dislike about X" from
the ledger rows, in his words. No database: the rows brain.search would return are built with brain_index.rule_pages over
fixture ledgers, so the shape is tested against the indexer's real page format."""
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import brain_index as bi  # noqa: E402
import brain_serve as bs  # noqa: E402

NOTIF = """# Notification contract

## HARD

| # | Rule | Source |
|---|---|---|
| H1 | Every line names who wrote it. *"you're not saying who sent what"* | his feedback Telegram 2026-09-29 14:23 |

| H2 | LIKED: he liked this sentence as written. *"good one, exactly who wrote it"* [item: n20261004T161153317] [maps-to: H1] | he liked it 2026-10-04 |

## SOFT (judgement)

| # | Rule | Source |
|---|---|---|
| H3 | **SOFT, flag only.** Do not list missed things unverified. *"I have answered to all these"* | his feedback 2026-09-29 |
"""


def _hits(tmp_path):
    f = tmp_path / "NOTIF-CONTRACT.md"
    f.write_text(NOTIF, encoding="utf-8")
    pages = bi.rule_pages(f, tmp_path)
    return [{"path": "/home/da/task-land/_system/" + p.path.split("/")[-1], "kind": p.kind, "title": p.title,
             "text": p.body, "score": 1.0 / (i + 1)} for i, p in enumerate(pages)]


def test_shape_splits_liked_and_rules(tmp_path):
    hits = _hits(tmp_path)
    hits.append({"path": "memory/reference_sodanotif.md", "kind": "memory", "text": "not a rule", "score": 0.9})
    conf = tmp_path / "c.jsonl"
    conf.write_text(json.dumps({"rule": "notif:H1"}) + "\n" + json.dumps({"rule": "notif:H1"}) + "\n", encoding="utf-8")
    out = bs.shape_rules(hits, bs.confirmation_counts(str(conf)))
    assert [r["rule"] for r in out["rules"]] == ["H1", "H3"]
    assert [r["rule"] for r in out["liked"]] == ["H2"]
    h1 = out["rules"][0]
    assert h1["ledger"] == "notif" and h1["his_words"] == "you're not saying who sent what" and h1["confirmed"] == 2
    assert h1["source"].startswith("his feedback Telegram") and "*" not in h1["text"]
    assert out["rules"][1]["soft"] is True
    assert out["liked"][0]["his_words"] == "good one, exactly who wrote it"


def test_ledger_filter(tmp_path):
    out = bs.shape_rules(_hits(tmp_path), {}, ledger="crm")
    assert out == {"liked": [], "rules": []}
