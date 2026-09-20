---
name: reference_linkedin_scraper_direct_stdio
description: "When the linkedin-mcp transport drops mid-session, drive the same local scraper directly over stdio from Python instead of giving up; /mcp reconnect is not the only option."
metadata: 
  node_type: memory
  type: reference
  originSessionId: e7351fcb-845d-45ae-b97b-335e70d58b55
  modified: 2026-09-20T02:45:20.274Z
---

**The `linkedin-mcp` server is a local stdio process, so a dead MCP transport is not a dead
capability.** It is launched from
`C:\Users\Alessandro\.linkedin-mcp\venv\Scripts\python.exe C:\Users\Alessandro\.linkedin-mcp\launcher.py`
with `HEADLESS=true`. When the connection dropped mid-sweep on 2026-09-20 (and only he can type
`/mcp reconnect`), the recovery was to spawn it as an ordinary MCP stdio client from Python:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
params = StdioServerParameters(
    command=r"C:\Users\Alessandro\.linkedin-mcp\venv\Scripts\python.exe",
    args=[r"C:\Users\Alessandro\.linkedin-mcp\launcher.py", "--tool-timeout", "600"],
    env={**os.environ, "HEADLESS": "true", "HOST": "127.0.0.1", "LOG_LEVEL": "WARNING",
         "PYTHONIOENCODING": "utf-8"})
async with stdio_client(params) as (read, write):
    async with ClientSession(read, write) as s:
        await s.initialize()
        res = await s.call_tool("search_people", arguments={"keywords": q, "location": "United States"})
```

Same logged-in browser profile, same tools. There are precedent scripts in that folder
(`find_welter.py`, `check_caleb.py`). Working examples from the US campaign:
`~/tundra-outreach/us-campaign-100/campaign/li-sweep.py` (batch search, one browser session, raw
output checkpointed per query so a crash costs one query) and `li-resolve.py` (resolve a profile URL
for a known name + employer).

**Which tool to use.** `search_people` is the good one: real names, exact titles, employers,
locations and profile URLs, roughly 6 usable US rows per query.
`get_company_employees` is NOT a filtered employee list - it returns loose "People you may know"
suggestions and its `keywords` filter barely applies, so it wasted a call and returned research
assistants when asked for clinical engineering directors.

**Rules that keep it safe and honest.** Pace it (8 to 15 s between queries; this is his own account,
about 150 page loads in a night was fine). **Never construct a profile slug from a name** - take the
URL only from the result's `references` array. When resolving a known person, require the surname
AND first initial to match AND the employer to appear on the same card; anything weaker is recorded
as a candidate, not promoted to a usable URL.

Pairs with [[reference_linkedin_mcp]] and [[reference_websearch_budget_and_fallbacks]].
