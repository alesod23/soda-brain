"""Integration test: a real Postgres 16 + pgvector, schema.sql, the indexer on soda-brain/memory with the
real model, the service on 127.0.0.1:4150, the HTTP routes with the laptop's real crm.json (read-only),
and the MCP door at /mcp.

Database, in this order:
  1. SODA_TEST_DSN env (any Postgres with pgvector; the test creates its own schemas in it)
  2. Docker Desktop running (`docker info`): pgvector/pgvector:pg16 on port 55432, throwaway password, removed after
  3. the `pgserver` package (embedded Postgres with pgvector, no Docker)
  otherwise the whole module is skipped with the reason printed.
"""
import glob
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))

import brain_index as bi  # noqa: E402

CRM_JSON = Path(os.environ.get("SODA_TEST_CRM_JSON", str(Path.home() / ".medtech-crm" / "crm.json")))
PORT = int(os.environ.get("SODA_TEST_PORT", "4150"))
HOST = "127.0.0.1"
PY = sys.executable
NO_WINDOW = {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)} if os.name == "nt" else {}


def _docker_ok() -> bool:
    if not shutil.which("docker"):
        return False
    try:
        return subprocess.run(["docker", "info"], capture_output=True, timeout=20, **NO_WINDOW).returncode == 0
    except Exception:
        return False


def _port_free(port: int) -> bool:
    with socket.socket() as s:
        return s.connect_ex((HOST, port)) != 0


@pytest.fixture(scope="module")
def dsn():
    if os.environ.get("SODA_TEST_DSN"):
        yield os.environ["SODA_TEST_DSN"]
        return
    if _docker_ok():
        pw = secrets.token_hex(12)
        name = "soda-brain-test-pg"
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, **NO_WINDOW)
        subprocess.run(["docker", "run", "-d", "--rm", "--name", name, "-e", f"POSTGRES_PASSWORD={pw}",
                        "-e", "POSTGRES_DB=soda", "-p", "55432:5432", "pgvector/pgvector:pg16"],
                       check=True, capture_output=True, **NO_WINDOW)
        d = f"postgresql://postgres:{pw}@127.0.0.1:55432/soda"
        import psycopg
        for _ in range(60):
            try:
                psycopg.connect(d).close()
                break
            except Exception:
                time.sleep(1)
        try:
            yield d
        finally:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True, **NO_WINDOW)
        return
    try:
        import pgserver
    except ImportError:
        pytest.skip("no SODA_TEST_DSN, Docker Desktop is not running, pgserver not installed")
    import tempfile
    tmp = tempfile.mkdtemp(prefix="soda-pg-")
    srv = pgserver.get_server(tmp, cleanup_mode="delete")
    print(f"\n[db] embedded Postgres via pgserver at {tmp}")
    try:
        yield srv.get_uri()
    finally:
        srv.cleanup()
        shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(scope="module")
def schema(dsn):
    import psycopg
    with psycopg.connect(dsn, autocommit=True) as conn:
        conn.execute("DROP SCHEMA IF EXISTS brain CASCADE; DROP SCHEMA IF EXISTS crm CASCADE")
        conn.execute((TOOLS / "schema.sql").read_text(encoding="utf-8"))
        conn.execute((TOOLS / "schema.sql").read_text(encoding="utf-8"))   # idempotent: twice is fine
        ver = conn.execute("SELECT version()").fetchone()[0]
        ext = conn.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()[0]
    print(f"[db] {ver.split(',')[0]} pgvector {ext}")
    return dsn


def test_index_memory_with_real_model(schema):
    t = time.time()
    sources = [("memory", str(REPO / "memory" / "*.md"))]
    s1 = bi.run_index(schema, sources, REPO, log=lambda m: print("[index]", m))
    expected = len(glob.glob(str(REPO / "memory" / "*.md")))
    assert s1["files"] == expected and s1["changed"] == expected
    assert s1["embedded"] == s1["chunks"] > expected * 0.9
    print(f"[index] first run {s1['seconds']}s for {expected} pages / {s1['chunks']} chunks")
    s2 = bi.run_index(schema, sources, REPO, log=lambda m: print("[index]", m))
    assert s2["changed"] == 0 and s2["embedded"] == 0 and s2["seconds"] < 5   # sha fast path
    # a page vanishing from the sources is soft-deleted; every other page unchanged
    one = sorted(glob.glob(str(REPO / "memory" / "*.md")))[0]
    rest = [("memory", p) for p in sorted(glob.glob(str(REPO / "memory" / "*.md")))[1:]]
    s3 = bi.run_index(schema, rest, REPO, log=lambda m: print("[index]", m))
    assert s3["deleted"] == 1 and s3["changed"] == 0
    s4 = bi.run_index(schema, sources, REPO, log=lambda m: print("[index]", m))
    assert s4["changed"] == 1 and s4["embedded"] == 0 and s4["reused"] >= 1   # back: embedding reused
    import psycopg
    with psycopg.connect(schema) as conn:
        st = bi.stats(conn)
    assert st["pages"]["memory"] == expected and st["pages_deleted"] == 0
    print(f"[index] stats {json.dumps(st, default=str)} ({time.time() - t:.0f}s total)")


@pytest.fixture(scope="module")
def service(schema):
    assert _port_free(PORT), f"port {PORT} is in use on {HOST}; set SODA_TEST_PORT"
    env = dict(os.environ, SODA_DB_DSN=schema, SODA_TOKEN="test-token-" + secrets.token_hex(4),
               PYTHONDONTWRITEBYTECODE="1", HF_HUB_DISABLE_PROGRESS_BARS="1")
    import tempfile
    logf = tempfile.NamedTemporaryFile(prefix="soda-serve-", suffix=".log", delete=False)   # never a pipe: a pipe
    proc = subprocess.Popen([PY, str(TOOLS / "brain_serve.py"), "--host", HOST, "--port", str(PORT)],  # nobody reads blocks
                            cwd=str(TOOLS), env=env, stdout=logf, stderr=logf, **NO_WINDOW)

    def tail() -> str:
        logf.flush()
        return Path(logf.name).read_text(encoding="utf-8", errors="replace")[-3000:]

    import httpx
    base = f"http://{HOST}:{PORT}"
    for _ in range(120):
        if proc.poll() is not None:
            raise RuntimeError("service died:\n" + tail())
        try:
            r = httpx.get(base + "/health", timeout=2)
            if r.status_code == 200 and r.json().get("db"):
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        proc.kill()
        raise RuntimeError("service did not come up:\n" + tail())
    try:
        yield base, env["SODA_TOKEN"]
    finally:
        proc.terminate()
        try:
            proc.wait(10)
        except subprocess.TimeoutExpired:
            proc.kill()
        logf.close()
        try:
            os.unlink(logf.name)
        except OSError:
            pass   # Windows may still hold the handle for a moment; it is a temp file


def test_health_and_recall(service):
    import httpx
    base, _ = service
    h = httpx.get(base + "/health").json()
    print("\n[http] /health", h)
    assert h["ok"] and h["db"] and h["pages"] > 300 and h["chunks"] >= h["pages"]
    r = httpx.post(base + "/brain/recall", json={"query": "how are hub cards sent"}, timeout=60).json()
    assert len(r) == 8 and all(k in r[0] for k in ("path", "title", "score", "text", "since", "superseded_by"))
    print("[http] /brain/recall top 3:", [(x["path"], round(x["score"], 4)) for x in r[:3]])
    assert any("hub" in x["path"] or "ping" in x["path"] for x in r[:3])
    p = httpx.get(base + "/brain/page", params={"path": r[0]["path"]}).json()
    assert p["path"] == r[0]["path"] and p["body"]
    assert httpx.get(base + "/brain/page", params={"path": "nope.md"}).status_code == 404


def test_auth_is_only_exempt_on_loopback(service):
    """Loopback is exempt by design; the token check itself is exercised on the ASGI gate directly."""
    import brain_serve as bs
    scope = {"type": "http", "path": "/brain/recall", "method": "POST", "client": ("100.127.7.80", 1),
             "headers": [(b"x-soda-token", b"wrong")]}
    os.environ["SODA_TOKEN"] = "right"
    assert not bs.TokenAuth.allowed(scope)
    scope["headers"] = [(b"x-soda-token", b"right")]
    assert bs.TokenAuth.allowed(scope)
    assert bs.TokenAuth.allowed({"type": "http", "path": "/health", "method": "GET", "client": ("1.2.3.4", 1),
                                 "headers": []})
    assert not bs.TokenAuth.allowed({"type": "http", "path": "/mcp", "method": "POST", "client": ("1.2.3.4", 1),
                                     "headers": []})
    os.environ.pop("SODA_TOKEN")
    assert not bs.TokenAuth.allowed(scope)   # no token configured -> closed


@pytest.mark.skipif(not CRM_JSON.is_file(), reason=f"{CRM_JSON} not found")
def test_crm_put_and_reads(service):
    import httpx
    base, _ = service
    doc = json.loads(CRM_JSON.read_text(encoding="utf-8"))
    n_people = sum(len(c.get("people") or []) for c in doc["companies"])
    body = {"source": "laptop-test", "at": "2026-10-01T23:00:00+02:00", "doc": doc}
    t = time.time()
    r = httpx.post(base + "/crm/put", json=body, timeout=300).json()
    print(f"\n[http] /crm/put {r} in {time.time() - t:.1f}s")
    assert r["ok"] and r["changed"]["companies"] == len(doc["companies"]) == 441
    assert r["changed"]["people"] == n_people == 626
    assert r["changed"]["templates"] == len(doc["templates"]) and r["changed"]["signals"] == len(doc["signals"])
    r2 = httpx.post(base + "/crm/put", json=body, timeout=300).json()
    assert r2 == {"ok": True, "version": r["version"], "unchanged": True}

    # change one person: only that record is upserted
    doc2 = json.loads(CRM_JSON.read_text(encoding="utf-8"))
    pid = next(p["id"] for c in doc2["companies"] for p in c.get("people") or [] if p.get("id"))
    for c in doc2["companies"]:
        for p in c.get("people") or []:
            if p.get("id") == pid:
                p["notes"] = (p.get("notes") or "") + " [integration-test]"
    r3 = httpx.post(base + "/crm/put", json={"source": "laptop-test", "doc": doc2}, timeout=300).json()
    assert r3["changed"] == {"companies": 0, "people": 1, "templates": 0, "signals": 0}
    assert r3["deleted"] == {"companies": 0, "people": 0, "templates": 0, "signals": 0}

    person = httpx.get(base + f"/crm/person/{pid}").json()
    assert person["id"] == pid and person["data"]["notes"].endswith("[integration-test]") and person["company"]
    print("[http] /crm/person", pid, "->", ascii(person["name"]), "@", ascii(person["company"]))
    comp = httpx.get(base + f"/crm/company/{person['company_id']}").json()
    assert comp["id"] == person["company_id"] and any(p["id"] == pid for p in comp["people"])

    q = (person["name"] or "").split()[0]
    people = httpx.get(base + "/crm/people", params={"q": q, "limit": 10}).json()
    assert any(p["id"] == pid for p in people) and len(people) <= 10
    print(f"[http] /crm/people?q={ascii(q)} -> {len(people)} rows")
    assert len(httpx.get(base + "/crm/people", params={"stage": "nope-stage"}).json()) == 0
    due = httpx.get(base + "/crm/people", params={"due_before": "2030-01-01", "limit": 500}).json()
    assert all(p["next_step_date"] for p in due)

    h = httpx.get(base + "/health").json()
    assert h["people"] == 626
    latest = httpx.get(base + "/crm/doc", timeout=120).json()
    assert latest["version"] == r3["version"] if "version" in latest else latest["id"] == r3["version"]
    ch = httpx.get(base + "/crm/changes", params={"since": "2000-01-01T00:00:00Z"}).json()
    assert len(ch["people"]) == 626 and len(ch["companies"]) == 441

    ev = httpx.post(base + "/crm/events", json={"lines": [
        {"source": "ledger", "id": "e1", "at": "2026-10-01T10:00:00Z", "kind": "email", "direction": "out", "person_id": pid},
        {"source": "ledger", "id": "e2", "kind": "wa", "direction": "in"},
        {"source": "ledger", "id": "e1", "kind": "dup"},
        {"id": "no-source"}]}).json()
    assert ev == {"inserted": 2, "skipped": 2}
    assert httpx.post(base + "/crm/events", json={"lines": [{"source": "ledger", "id": "e2"}]}).json() == \
        {"inserted": 0, "skipped": 1}


def test_mcp_door(service):
    import anyio
    base, token = service
    from mcp.client.session import ClientSession
    from mcp.client.streamable_http import streamable_http_client
    from mcp.shared._httpx_utils import create_mcp_http_client

    def result(res):
        """A list return arrives as one text block per item (and structured under 'result')."""
        assert not res.is_error, res.content
        sc = res.structured_content
        if isinstance(sc, dict) and set(sc) == {"result"}:
            return sc["result"]
        if sc is not None:
            return sc
        items = [json.loads(c.text) for c in res.content]
        return items[0] if len(items) == 1 else items

    async def go():
        client = create_mcp_http_client(headers={"X-Soda-Token": token})
        async with streamable_http_client(base + "/mcp", http_client=client) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                tools = sorted(t.name for t in (await s.list_tools()).tools)
                assert tools == ["crm_person", "crm_search", "page", "recall", "what_is_true"]
                hits = result(await s.call_tool("recall", {"query": "how are hub cards sent", "k": 3}))
                assert len(hits) == 3 and "path" in hits[0]
                out = result(await s.call_tool("what_is_true", {"topic": "hub cards"}))
                assert out["pages"] and out["current"]["path"]
                pg = result(await s.call_tool("page", {"path": hits[0]["path"]}))
                assert pg["body"]
                people = result(await s.call_tool("crm_search", {"q": "a", "limit": 2}))
                assert len(people) == 2 and "id" in people[0]
                one = result(await s.call_tool("crm_person", {"id": people[0]["id"]}))
                assert one["id"] == people[0]["id"]
                print("\n[mcp] tools", tools, "| recall", hits[0]["path"], "| what_is_true", out["current"]["path"],
                      "| crm_search", ascii(people[0]["name"]))
                return tools

    anyio.run(go)
