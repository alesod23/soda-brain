"""Unit tests for crm_diff.py on a synthetic coattio document."""
import copy
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import crm_diff as cd  # noqa: E402


def _doc():
    return {
        "meta": {"owner": "A", "schemaVersion": 2},
        "templates": [{"id": "t1", "name": "intro", "body": "hi"}],
        "companies": [
            {"id": "c-one", "company": "One Hospital", "sector": "hospital", "people": [
                {"id": "p1", "name": "Anna", "email": "anna@one.org", "stage": "contacted",
                 "next_step": {"date": "2026-10-03", "text": "follow up", "channel": "email"}},
                {"name": "No Id", "email": "", "stage": "new"},
            ]},
            {"id": "c-two", "company": "Two Clinic", "people": [
                {"id": "p2", "name": "Bob", "linkedin": "https://li/bob", "next_step": None},
            ]},
        ],
        "signals": [{"id": "s1", "at": "2026-09-30", "text": "x"}],
    }


def test_canonical_and_sha_are_order_independent():
    a = {"b": 1, "a": [1, {"z": 2, "y": 3}]}
    b = {"a": [1, {"y": 3, "z": 2}], "b": 1}
    assert cd.canonical(a) == cd.canonical(b)
    assert cd.record_sha(a) == cd.record_sha(b)
    assert len(cd.record_sha(a)) == 40


def test_split_doc_keys_and_fields():
    s = cd.split_doc(_doc())
    assert set(s) == {"companies", "people", "templates", "signals"}
    assert list(s["companies"]) == ["c-one", "c-two"]
    assert "people" not in s["companies"]["c-one"]["data"]          # company sha excludes its people
    assert s["companies"]["c-one"]["name"] == "One Hospital"
    assert list(s["people"]) == ["p1", "c-one/no-id", "p2"]          # missing id -> company/slug(name)
    p1 = s["people"]["p1"]
    assert p1["company_id"] == "c-one" and p1["email"] == "anna@one.org"
    assert p1["next_step_date"] == date(2026, 10, 3) and p1["next_step_text"] == "follow up"
    assert s["people"]["p2"]["next_step_date"] is None and s["people"]["p2"]["email"] is None
    assert list(s["templates"]) == ["t1"] and list(s["signals"]) == ["s1"]


def test_duplicate_ids_get_suffixes():
    d = _doc()
    d["companies"].append({"id": "c-one", "company": "One again", "people": [{"id": "p1", "name": "Dup"}]})
    s = cd.split_doc(d)
    assert list(s["companies"]) == ["c-one", "c-two", "c-one#2"]
    assert "p1#2" in s["people"] and s["people"]["p1#2"]["company_id"] == "c-one#2"


def test_company_sha_ignores_people_edits():
    d1, d2 = _doc(), _doc()
    d2["companies"][0]["people"][0]["stage"] = "replied"
    s1, s2 = cd.split_doc(d1), cd.split_doc(d2)
    assert s1["companies"]["c-one"]["sha"] == s2["companies"]["c-one"]["sha"]
    assert s1["people"]["p1"]["sha"] != s2["people"]["p1"]["sha"]


def test_diff_changed_new_deleted_and_undeleted():
    s = cd.split_doc(_doc())
    current = {k: (v["sha"], False) for k, v in s["people"].items()}
    changed, deleted = cd.diff(current, s["people"])
    assert changed == [] and deleted == []                            # same doc -> nothing

    d2 = _doc()
    d2["companies"][0]["people"][0]["stage"] = "replied"              # p1 changed
    d2["companies"][1]["people"] = []                                 # p2 gone
    d2["companies"][0]["people"].append({"id": "p9", "name": "New"})  # p9 new
    s2 = cd.split_doc(d2)
    changed, deleted = cd.diff(current, s2["people"])
    assert set(changed) == {"p1", "p9"} and deleted == ["p2"]

    # a record soft-deleted in the DB and present again in the doc counts as changed
    current2 = dict(current)
    current2["p2"] = (current["p2"][0], True)
    changed, deleted = cd.diff(current2, s["people"])
    assert changed == ["p2"] and deleted == []


def test_parse_date_variants():
    assert cd.parse_date("2026-10-03") == date(2026, 10, 3)
    assert cd.parse_date("2026-10-03T10:00:00Z") == date(2026, 10, 3)
    assert cd.parse_date("") is None and cd.parse_date(None) is None and cd.parse_date("soon") is None


def test_doc_sha_changes_with_content():
    d = _doc()
    a = cd.doc_sha(d)
    d2 = copy.deepcopy(d)
    d2["meta"]["owner"] = "B"
    assert a != cd.doc_sha(d2) and a == cd.doc_sha(copy.deepcopy(d))
