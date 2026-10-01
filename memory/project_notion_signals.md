---
name: project_notion_signals
description: "Notion 📥 Inbox — hand-fillable Tundra drop-box for the team; CC/DA writes directly to target DBs instead, gated by approval-hub pings. Machine plumbing stays OUT of Notion."
metadata: 
  node_type: memory
  type: project
  originSessionId: 03bd0192-2326-44a8-a159-5f4f0698c975
  modified: 2026-08-10T22:48:13.420Z
---

**`📥 Inbox` is the Tundra team's shared drop-box in Notion.** Built 2026-08-10. Canonical spec +
the full agent prompt: `medtech-brain/_system/NOTION-INBOX.md`. DB
`da24a2861f9748789108d888f913b80d`, data source `collection://5e74025c-1e36-485e-9fa4-f24531b27294`.

**The correction that shaped it (same day):** the first build was a machine-flavored "Signals"
pipeline with External ID / Source / Route / Confidence columns and a PUBLIC anonymous form. He
killed it: *"I'm making public something that is just working for me… make it a system that one can
fill by hand. that big signal stuff should rather be on the CC/da system side. I want something
that my cofounder that DOESN'T HAVE da system, not even his email connected to Claude, can use."*
Form closed (nothing was ever shared; DB was still private), machine columns dropped.
**Lesson: a team-facing Notion surface must look like Notion, not like my pipeline. Producer
plumbing (dedupe keys, sources, confidence) lives local, never as shared-DB columns.**

**Final shape (LIVE 2026-08-11 — he built and evolved the agent himself in the Notion UI; the
agent's canonical instructions live in the Notion agent config, not in my spec file):**
- **Schema:** Name · Details (sacred) · Status (Inbox → Proposed → Approved → Done, + Skip) ·
  Intended outputs (human hint, agent infers if empty, never overrides) · Affiliation · Proposed
  meeting date/type · Proposed contact name · Proposed task title (structured preview columns) ·
  Proposal · Rationale · **Change request** (non-empty = revise; post-Done it adjusts created items
  in place, never deletes) · relations Created Task/Contact/Meeting.
- **ONE agent `Inbox filer`, THREE triggers:** row created · Status changed · **@mentioned anywhere
  in Notion** (creates the Inbox row from the mention text and notifies the mentioner).
- **Task policy (his correction):** a meeting existing is NOT a reason to create a Task — only
  clear action items or explicit Task in Intended outputs. Only a human sets Approved.
- Known cruft: `Input type` select duplicates Intended outputs (drop pending his confirm).
- **Caleb's lane:** type a row, read Proposal, flip Approved or Skip. Approval belongs to whoever
  wrote the row; Alessandro's phone is never in the team's path.
- **Alessandro's lane (to build later, STARTING FROM DA SYSTEM):** CC/DA does the watching and
  classifying locally (plan-included, not Notion credits) and pushes the result as an ordinary
  Inbox row via Notion MCP — same doorway as Caleb, then the same Notion agent files it. He does
  NOT want Notion agents doing his side's heavy lifting (expensive) and he does NOT hand-type.
  Dedupe/source/confidence stay in CC local state, never as Inbox columns. How his approval lands
  (hub ping at push time vs flipping Approved in Notion) is decided when the watcher gets built.
  Non-Tundra findings keep going to task-land/vault_kb.

**Granola, verified 2026-08-10, do not re-research:** Granola→Notion is manual click-to-share on
every plan INCLUDING Business (he has Business). Folder auto-share targets Slack only; automatic
needs Zapier's note-added-to-folder trigger. He chose click-to-share; phase-2 agent on Granola's
own DB dedupes vs Meetings (granola-auto may have written the call) and drops Inbox rows for
action items — never post-call scans Internal meetings.

**Do not re-route granola-auto or coattio→Contacts through the Inbox** — they keep their own lanes.
Custom Agents need Business (he has it) and burn Notion Credits ($10/1k).
See [[project_da_system]], [[reference_approval_hub]], [[reference_notion_tundra_system]],
[[feedback_notion_write_needs_approval]].
