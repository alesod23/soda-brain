---
name: reference-edge-mcp
description: "Edge (getedge.cc) MCP + prompt nudge, installed on the box 2026-10-03: what it is, the audit, how it is wired without the claude CLI, and his standing rule to check it before a new kind of task"
metadata:
  type: reference
---

**His instruction, 2026-10-03:** "put what I'm about to give you into the laptop and VPS as a tool
where we can look up some good skills for our works [...] whenever I have to do a new task I want
you to first take a look at get edge and look if there is a good skill to iterate on and to use as
a baseline." Free tier is enough: "even if you just the free tier set it all up like I asked."

`@getedge/mcp` describes itself as "finds a fitting public agent skill for the task at hand and
loads it on demand". Version pinned at **0.6.13** (published the same day; 30 versions exist, so
pin and bump deliberately rather than float on latest).

## The audit, done before installing (the precedent is his, see [[reference_getedge_people_search_skill]])

- **Network: two hosts only**, `getedge.cc` and `skills.sh`. No telemetry host, no third party.
- **Env:** an optional `EDGE_KEY`, plus knobs (`EDGE_BACKEND`, `EDGE_LOAD_POLICY`,
  `EDGE_NUDGE=off` to silence the hook). Nothing is set here; the free tier needs no key.
- **Dependencies: two**, the MCP SDK and zod. MIT.
- **The prompt hook is the part that mattered** and it is clean: pure regex, and its own comment
  is accurate, "No network, filesystem reads, prompt logging or child processes". 250 ms internal
  timeout, fails open, never emits a blocking decision.
- **The installer copies the hook LOCALLY** (`~/.claude/hooks/edge-nudge.mjs`) and writes the
  command as `<node> <that path>` with `timeout: 1`. It does NOT run `npx` on every prompt, which
  is what froze sessions in [[reference_pretooluse_hook_hang_npx]]. It also preserves unrelated
  hooks, and the Telegram `tg-reply-context.py` hook survived the install, verified after.

## How it is wired on the box, and why not the usual way

The documented install is `claude mcp add edge -s user -- npx -y @getedge/mcp`, and the savior
**must never run the claude CLI** ([[feedback_never_run_claude_cli_from_savior]]: `claude mcp list`
alone killed the Telegram lane). Editing `~/.claude.json` by hand is also unsafe, because a running
session rewrites that file and would clobber the edit.

So the server is declared in **`/home/da/.mcp.json`** instead, a separate file the running process
does not rewrite, which this setup already understands (`enabledMcpjsonServers` exists per project
in `.claude.json`). A session started after that file appears picks it up; the savior needs
`/mcp reconnect` or a restore, which only he runs.

The hook was installed by running the vendor's own `node hooks/install.mjs claude ~/.claude` (a
node script, not the claude CLI), after backing up `settings.json.bak-20261003-edge`.

## The standing rule it encodes

Before a new KIND of task, ask Edge whether a public skill exists worth using as a baseline, and
compare it with the local skills. The nudge sentence says exactly that and only fires on a
deliverable, staying quiet on small edits, questions and greetings (tested both ways).

Not a licence to install anything it returns: the 2026-09-18 verdict on their `people-search`
skill was **removed after a head-to-head test that it lost**. Finding a candidate is cheap; adopting
one still needs the same test.
