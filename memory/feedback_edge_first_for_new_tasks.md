---
name: feedback_edge_first_for_new_tasks
description: "His standing instruction (2026-10-03, via the savior): Edge (getedge.cc, MCP @getedge/mcp) is installed on both machines as the skill look-up tool; before any NEW task look there for a skill to use as the baseline and iterate on; the simulation experiments with those skills; free tier is enough"
metadata:
  type: feedback
since: 2026-10-03
---

**His words (relayed by the savior, 3 Oct 2026):** "put what I'm about to give you into the laptop and VPS as a tool
where we can look up some good skills for our works [...] this would be a big part of the simulation [...] I want you
to experiment to some of those skills in the next iterations of it, to see how well it can do, what improvements we
might get from working on those skills. And in general whenever I have to do a new task I want you to first take a
look at get edge and look if there is a good skill to iterate on and to use as a baseline." Free tier, his word.

**Why:** a catalogue of ~20k public skills is cheaper to check than to rebuild, and the simulation needs an outside
baseline to measure our loops against.

**How to apply:**
- Laptop: user-scope MCP `edge` (`claude mcp get edge`), `npx -y @getedge/mcp@0.6.1`, connected 3 Oct; the box pins
  `@getedge/mcp@0.6.13` in `/home/da/.mcp.json` plus the vendor's prompt nudge hook (`~/.claude/hooks/edge-nudge.mjs`,
  regex only, fails open, `EDGE_NUDGE=off`); the box audit is in [[reference_edge_mcp]]. Re-pinning the laptop to
  0.6.13 was refused by the permission classifier (3 Oct 12:40): his command if he wants it:
  `claude mcp remove edge -s user; claude mcp add edge -s user -- npx -y @getedge/mcp@0.6.13`. The nudge hook is
  not installed on the laptop (settings.json hooks are his to change).
- Every NEW task: one `mcp__edge__find_skill` call (task sentence + 2 to 6 keywords) before building; use a hit
  only when it clearly beats what we have; say in one line what was found or that nothing fit.
- The simulation: in the next run (after the plan renews, 7 Oct or later; compute pause of 2 Oct) give the readers
  and the drafter an Edge-found skill as a variant and score it against the measured baseline. The honest prior:
  on 2026-09-18 Edge's `people-search` lost head-to-head to plain WebSearch and he had it removed
  ([[reference_getedge_people_search_skill]]). So the question is "does it beat what we do", on a task with a
  number: the daily campaign research (people found per round, address proof rate) and the critic's hit rate.
  State the Edge version with every result: laptop 0.6.1 and box 0.6.13 are not the same product (30 releases exist,
  0.6.13 carries an activation regex dated "plan C, 2026-10-02"); a score at one version says nothing about the other.
- Sync gap: the box commits every 5 min, the laptop every 10; a file "missing from the repo" is only missing after one
  full cycle has passed (3 Oct: each side reported the other's file absent inside that window).
  See [[reference_simulation_harness]], [[reference_daily_campaign]].
