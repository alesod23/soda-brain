"""Unit tests for brain_index.py: chunking, frontmatter, sha skip, dry-run plan on the real memory folder."""
import glob
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import brain_index as bi  # noqa: E402

REPO = TOOLS.parent


# ----------------------------------------------------------------- frontmatter

def test_frontmatter_quoted_nested_and_block():
    text = '''---
name: feedback_x
description: "\\"Ping\\" is his word: a card, never chat"
since: 2026-09-04
metadata:
  node_type: memory
  type: feedback
  originSessionId: abc
notes: |
  line one
  line two
---
# Body

text'''
    meta, body = bi.parse_frontmatter(text)
    assert meta["name"] == "feedback_x"
    assert meta["description"] == '"Ping" is his word: a card, never chat'
    assert meta["metadata"]["type"] == "feedback"
    assert meta["since"] == "2026-09-04"
    assert meta["notes"] == "line one\nline two"
    assert body.strip().startswith("# Body")


def test_frontmatter_absent_or_unterminated():
    assert bi.parse_frontmatter("# no fm\nhello") == ({}, "# no fm\nhello")
    meta, body = bi.parse_frontmatter("---\nname: x\nno end")
    assert meta == {} and body.startswith("---")


def test_page_fields_from_real_memory_file():
    f = REPO / "memory" / "feedback_approvals_are_pings.md"
    p = bi.page_from_file(f, "memory", REPO)
    assert p.path == "memory/feedback_approvals_are_pings.md"
    assert p.title == "feedback_approvals_are_pings"
    assert p.type == "feedback"
    assert p.description and "approval-hub" in p.description
    assert len(p.sha) == 40
    assert p.chunks and all(c.strip() for c in p.chunks)


# ----------------------------------------------------------------- chunking

def _words(s: str) -> int:
    return len(s.split())


def _w(i: int) -> str:
    """A unique 3-letter word: cost 1 estimated token, so word counts == cost in these tests."""
    return chr(97 + i % 26) + chr(97 + (i // 26) % 26) + chr(97 + (i // 676) % 26)


def test_cost_estimator():
    assert bi._cost("abc") == 1 and bi._cost("abcd") == 2 and bi._cost("x" * 40) == 11 and bi._cost("\n\n") == 0
    assert bi.CHUNK_TOKENS == 400 and bi.CHUNK_OVERLAP == 50


def test_chunk_short_text_is_one_chunk():
    assert bi.chunk_text("# T\n\nhello world") == ["# T\n\nhello world"]


def test_chunk_long_section_windows_with_overlap():
    body = " ".join(_w(i) for i in range(1500))
    chunks = bi.chunk_text(body, size=600, overlap=60)
    assert [_words(c) for c in chunks] == [600, 600, 420]
    # overlap: last 60 words of chunk 0 == first 60 words of chunk 1
    assert chunks[0].split()[-60:] == chunks[1].split()[:60]
    assert chunks[-1].split()[-1] == _w(1499)
    # the default budget on the same text: every chunk within the budget, nothing lost
    d = bi.chunk_text(body)
    assert all(_words(c) <= bi.CHUNK_TOKENS for c in d) and d[-1].split()[-1] == _w(1499)


def test_chunk_splits_by_heading_first_and_packs_small_sections():
    secs = [f"## h{i}\n" + " ".join(_w(i * 250 + j) for j in range(250)) for i in range(5)]
    chunks = bi.chunk_text("\n".join(secs), size=600, overlap=60)
    # 5 sections of 250 words (+ heading, cost 2): packed 2 per chunk -> never cut mid-section
    for c in chunks:
        assert _words(c) <= 600
    assert chunks[0].startswith("## h0")
    assert "## h2" in chunks[1] and "## h4" in chunks[-1]
    assert chunks[1].split()[:60] == chunks[0].split()[-60:]   # 60-token overlap between packed chunks


def test_chunk_keeps_newlines():
    out = bi.chunk_text("a b\n\nc d")
    assert out == ["a b\n\nc d"]


# ----------------------------------------------------------------- sha skip

def _page(path, sha):
    return bi.Page(path=path, kind="memory", title=path, description=None, type=None, since=None,
                   superseded_by=None, checked_last=None, sha=sha, body="x", chunks=["x"])


def test_plan_changes_sha_skip_and_soft_delete():
    pages = [_page("a.md", "1"), _page("b.md", "2"), _page("c.md", "3")]
    existing = {"a.md": ("1", False), "b.md": ("old", False), "c.md": ("3", True), "gone.md": ("9", False),
                "already_gone.md": ("8", True)}
    changed, gone = bi.plan_changes(pages, existing)
    assert [p.path for p in changed] == ["b.md", "c.md"]    # b: sha differs; c: was soft-deleted and is back
    assert gone == ["gone.md"]                               # a: unchanged -> skipped entirely


# ----------------------------------------------------------------- sources / env

def test_parse_sources_env_and_default(monkeypatch, tmp_path):
    assert bi.parse_sources("memory=/x/*.md, hint=/y/*.md") == [("memory", "/x/*.md"), ("hint", "/y/*.md")]
    with pytest.raises(SystemExit):
        bi.parse_sources("bogus=/x/*.md")
    d = bi.default_sources(tmp_path)
    assert [k for k, _ in d][:3] == ["memory", "system", "handoff"]


def test_load_env_does_not_override(monkeypatch, tmp_path):
    f = tmp_path / "soda.env"
    f.write_text('SODA_TOKEN="abc"\nexport SODA_DB_DSN=postgresql://x\n# c\nBAD\n', encoding="utf-8")
    monkeypatch.setenv("SODA_TOKEN", "keep")
    monkeypatch.delenv("SODA_DB_DSN", raising=False)
    bi.load_env(f)
    import os
    assert os.environ["SODA_TOKEN"] == "keep"
    assert os.environ["SODA_DB_DSN"] == "postgresql://x"


# ----------------------------------------------------------------- rule pages

def test_rule_pages_one_per_row(tmp_path):
    f = tmp_path / "X-CONTRACT.md"
    f.write_text("# X contract\n\nintro\n\n| # | Rule | Source |\n|---|---|---|\n"
                 "| H1 | **first** rule | src1 |\n| H2 | second | src2 |\n\n## tail\nprose\n", encoding="utf-8")
    pages = bi.rule_pages(f, tmp_path)
    paths = [p.path for p in pages]
    assert paths == ["X-CONTRACT.md#H1", "X-CONTRACT.md#H2", "X-CONTRACT.md"]
    assert pages[0].body.startswith("H1: **first** rule") and "src1" in pages[0].body
    assert "intro" in pages[2].body and "| H1 |" not in pages[2].body
    assert all(p.kind == "rule" for p in pages)


# ----------------------------------------------------------------- dry-run on the real repo

def test_dry_run_plan_on_real_memory_folder():
    expected = len(glob.glob(str(REPO / "memory" / "*.md")))
    assert expected > 300, "soda-brain/memory is expected to hold the 300+ memory pages"
    plan = bi.dry_run([("memory", str(REPO / "memory" / "*.md"))], REPO, dsn=None)
    assert plan["files"] == expected
    assert plan["by_kind"] == {"memory": expected}
    assert plan["changed"] == expected and plan["db"] is False
    assert plan["chunks"] >= expected
    print(f"\nmemory pages on disk: {expected}, chunks: {plan['chunks']}")
