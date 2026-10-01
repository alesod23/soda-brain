---
name: feedback_agent_output_file_is_interim
description: "A research subagent's output file on disk is a DRAFT until its completion notification arrives; it often rewrites the file wholesale, so any selection built from the early version has to be redone"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67360653-a4fa-4a49-9fe9-75fbdcbb9319
  modified: 2026-09-01T18:29:52.288Z
---

A research subagent that is told to "write results to `<path>`" will frequently write an **early
version of that file well before it finishes**, keep working, and then **replace it wholesale**.
The rewrite is not an append: names disappear, new and better ones arrive, and the ranking changes.

**Why:** the agent writes as it goes so nothing is lost if it dies, then consolidates parallel
sweeps at the end. Only the completion notification means "this file is final."

**How to apply:**
- Treat a file on disk as **interim until the `<task-notification>` for that agent arrives.** Reading
  it early to plan is fine. Committing downstream work to it is not.
- If you do build on an interim file, **re-diff the names against the final file** before shipping.
  Match on a normalised name (fold accents, strip `(Nick)` parentheticals and `, PhD` / `, MD`
  suffixes) because agents render the same person's name inconsistently across passes.
- Watch the file's **byte size changing between checks** as the tell that it is still being written.

Observed 2026-09-01 on the peer-60 outreach batch: both US sweeps rewrote their files after I had
already drafted messages from the interim version. The US category 1 interim had four pairs of
co-founders from the same company; the final had 20 distinct companies and materially better
people, including the single most relevant name in the batch. Two full selections had to be redone.

Related: [[feedback_agent_long_running]], [[feedback_no_polling_on_background_tasks]],
[[reference_outreach_system]].
