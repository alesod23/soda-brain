---
name: reference_overnight_harness
description: The /overnight skill + reusable harness for reliable long-running/unattended agent runs
metadata: 
  node_type: memory
  type: reference
  originSessionId: 040b02ee-cbd5-4294-b80e-6e8423801f02
  modified: 2026-08-12T04:33:21.227Z
---

`/overnight` skill at `~/.claude/skills/overnight/` (SKILL.md + reusable Workflow engine `harness.js`). Built 2026-07-03 after a fire-and-forget Workflow burned ~1.3M tokens and wrote nothing (parse returned 0 rows, no error-catching, no checkpointing, no cap).

Encodes the 2026 multi-agent reliability consensus (full scan saved at `~/multi-agent-review-2026.md`): fail-loud gate (0 items → `_HALTED.md`, never "succeeds" empty), per-item checkpoint to `items/<id>.json` (crash costs 1 item; resumable — re-run skips `status:pass`), an INDEPENDENT read-only verifier loop (generator never self-grades; one bounded refine), hard `tokenCap` + circuit breaker via `budget.spent()` (works even with no `+Nk` directive), auth-quarantine (LinkedIn/OAuth work → `_NEEDS-AUTH.md` for a daytime pass), honest `REPORT.md`.

GOTCHA (verified 2026-07-03, caused 2 silent "empty/0-row" failures): this runtime delivers the Workflow `args` global to the script as a **JSON STRING**, not an object — always `const A = (typeof args==='string')?JSON.parse(args):(args||{})` at the top. harness.js already does this.

GOTCHAS FOUND 2026-08-12 (Rheine downtime dossier, 51 items / 4 waves / ~23M subagent tokens):
1. **args >~10KB silently breaks the run** — a ~30KB run-config died with `JSON Parse error: Expected ']'` before any agent started. FIX: put the shared brief and every per-item assignment in `.md` files in the out dir; `args` carries only ids + file pointers. Also makes the run human-readable and resumable.
2. **The final checkpoint step OVERWRITES the gen agent's own file.** `processItem` writes the structured output to `cp(it)` — the same path an agent may already have written its full result to. Four Wave-A agents wrote full JSON to that path and returned a summary stub, so the harness destroyed their work; recovered only by grepping `subagents/workflows/<runId>/agent-*.jsonl` for the Write tool_use. ALWAYS instruct agents: "return the COMPLETE result object as structured output; do NOT write it to a file and return a stub."
3. **WebSearch has a shared ~200-call SESSION quota**, not per-agent. With 16 concurrent agents it is exhausted early and later-starting items silently get none — they fall back to WebFetch and look "thin on evidence" when they were actually starved. For deep waves, build the brief around direct fetching + scholarly APIs (Crossref, OpenAlex, Europe PMC, Semantic Scholar, Unpaywall, DNB SRU) + `gemini-fetch.sh`, and run fewer items per wave.
4. **`tokenCap` counts OUTPUT tokens via `budget.spent()`, not total.** A 2.5M cap did not fire on a wave that consumed 10.6M total subagent tokens. Size caps accordingly or gate on item count.
5. **A workflow can stall without notifying.** Wave D wrote 5 of 8 checkpoints then went silent for 70+ min with no completion event; `TaskStop` + salvage the checkpoints. Check file mtimes rather than waiting.
6. Optional model routing added: `A.genModel` / `A.verifyModel`, per-item `it.genModel` / `it.verifyModel` (additive, back-compatible; omit = inherit session model).

Launch: `Workflow({ scriptPath: "~/.claude/skills/overnight/harness.js", args: { runName, outDir, tokenCap, items:[{id,data}], generatePrompt, verifySpec, rules, maxRefine, genModel, verifyModel } })`. Pass `items` in directly (don't rely on a flaky parse sub-step). Define `verifySpec` (the done-condition) FIRST. First test = Tundra hospital enrichment (24 accounts, 500k cap) in `tundra-outreach\overnight-2026-07-03\`. Related: the failed run's lessons; [[reference_kb_systems]]-style tooling discipline.
