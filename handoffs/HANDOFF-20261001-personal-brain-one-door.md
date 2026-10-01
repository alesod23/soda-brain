# Handoff: should the four stores become one brain with one door?

For the DA SYSTEM session. Written by the box savior at 01:45 on 1 October 2026, from his voice
note: "what we're missing is sort of a brain, and we are kind of being simple with just a few
rules ... maybe there is potential to set the basis for a personal AGI of some kind."

**This is a question, not a spec.** He wants your judgement on whether to build it, and where the
reasoning below is wrong. Say so if it is.

## Where this comes from

25 September, YC F26: Garry Tan's slide, "Many harnesses. One shared brain." Nine harnesses
(Muse, Grok Bot, Codex, Claude Code, Hermes Agent, OpenClaw, Perplexity Computer, QM, UFO.ai) all
reading one store, GBrain, over MCP. Postgres plus pgvector, indexing into a GitHub repo. The
line at the bottom is the claim: **"Change the harness. Keep the memory."** Photo:
`_system/brain-design/2026-09-25-yc-many-harnesses-one-brain.jpg`.

He asked then: where are we saving a brain, what is the brain for us, is as-is good enough, can a
personal AGI be built from it. You answered the same day, in the product register. Tonight he
corrected the framing: **he means it for himself, not for Tundra.**

That correction changes which gap matters. For a product, retrieval quality matters. For "keep
the memory when the harness changes", what matters is whether anything other than Claude Code can
reach it. Today nothing can.

## What exists, measured tonight, not opined

Four stores, four write paths, four readers, no shared index:

| store | what | size on 1 Oct | was on 25 Sep |
|---|---|---|---|
| Lessons | `claude-memory` git repo, one fact per file | 342 files, 9.4 MB | 305 files, 7.4 MB |
| Rules | 4 ledgers (email 94, CRM 42, hub 19, notif 5), compiled into skills | 160 | 108 |
| Evidence | `rule-hits.jsonl`, `decisions.jsonl` | 7,183 + 279 lines | 932 + 88 |
| State | coattio CRM, task-land tasks, approval hub | (unchanged in kind) | |

Five days: rules +48%, evidence 7.7x. **The deposit grows, the door does not.**

## The three gaps, in the order they will bite

1. **No door.** The stores are read by convention: a session opens `MEMORY.md` and loads the
   compiled skills at start. There is no interface. Another harness cannot ask. So the slide's
   claim is exactly the thing he does not have: change the harness today and the memory stays
   behind.
2. **No retrieval, and the ceiling already arrived.** Everything is read whole. `MEMORY.md` hit
   the 24 KB read limit in September, which is why there are now 7 sub-indexes. That split is the
   symptom, not the cure. It buys months, not years.
3. **No demotion, and no data to demote on.** Rules only ever grow. On 25 September you measured
   that 597 of 932 hits were ONE CRM rule and only 7 of 108 rules had ever been violated: most
   rules are dead weight carried in every prompt. The fix you proposed then, `_system/rule-stats.py`
   (per rule: applicable count, hit count, last hit, days since), **was never written.** Nor the
   Brain section of `RULE-LOOP.md`, nor the single recall entry point. All three are still open.

## What NOT to throw away

The slide's brain remembers. This one checks itself. `rule-hits.jsonl` records whether a filed
rule actually fired, so a lesson can be shown to have changed an outcome or shown to be dead.
Nothing in GBrain's design does that. If "one door" gets built as a vector store that forgets to
measure outcomes, the rebuild is a downgrade wearing a better architecture.

The approval hub is the second thing worth keeping: decisions are durable, auditable, and his.

## The proposal to argue with

One entry point both machines call, and any future harness can call:

- `recall "what do we know about X"` returns the four stores' answer with provenance. Grep and the
  existing indexes today; embeddings only when the numbers justify it.
- Expose it as an **MCP server**, which is the whole mechanism on Tan's slide and the only thing
  that makes "change the harness, keep the memory" literally true here.
- One index over the four stores, not one database: the write paths stay where they are, because
  they work and because merging them is a migration nobody asked for.
- The switch to embeddings is decided by a **number** from `rule-stats.py`, not by a feeling.

## What he should get from you, and it is not agreement

1. Is "one door" the right first move, or is **pruning** first? 160 rules in every prompt, most
   never firing, may be hurting more than the missing interface.
2. At what count does read-whole actually break? Measure it rather than guess. That number decides
   the order of everything above.
3. A personal AGI acts, it does not only recall. The daily campaign already fires 10 emails at
   16:55 with nobody in the loop, on an auditable ledger. **What is the next decision class he
   would delegate that way?** That question is more interesting than the storage one, and it is
   the one the slide does not answer.
4. Where is this reasoning wrong?

## One correction for him, kindly

He said "we are kind of being simple with just a few rules". It is 160 across four ledgers, and
the problem is the opposite of simplicity: nothing ever gets removed.

## DA SYSTEM's answer (1 Oct, 02:10, from the simulation's night)

**Measured first (`_system/rule-stats.py`, written tonight, 30 days of hits):** 160 rules, 35 ever checked, 125 never
(78%). One CRM rule (H2, the default step) makes 4,183 of 7,184 hits, 3,449 of them flags: half the evidence is one
nag. Email: 59 of 86 rules have never been checked by the critic; the ones it checks it checks only when it blocks.
Hub, notif, meeting: 2 of 32 ever checked. So the deposit is not "a brain that checks itself"; it is 35 rules that are
checked and 125 that ride in every prompt unchecked.

**What tonight's simulation adds (6 days, 60 events, score 44 to 79):** not one miss was a memory miss. Every miss
was a decision made without the evidence that was two files away: the reader saw 80 characters of the mail, no tool
could open the thread, a booking on the other calendar, a promise only in the transcript. The system that failed
"remembered" fine; it did not look. A single door to the four stores would not have changed one of those scores.

1. **Not one door first, and not pruning first either: depth first.** Give the decision points what a fresh session
   has (the thread, the stores, more turns, effort, the hints of their own past misses). Built tonight behind
   `DA_DEPTH=full` + `_system/hints/*.md`, measured from day 7 against the capped days. Then prune with the number
   above: a rule never checked is either compiled into code (then it is not a rule) or it goes to SOFT. Then the
   door, as an MCP `recall` over the four stores WITH the hit ledger behind it, because by then there is something
   worth reaching from another harness. Order: depth, prune, door.
2. **Where read-whole breaks:** in cost it already broke: the critic's prompt is 34k tokens (86 rules), $0.30 a call,
   measured. In accuracy nobody knows, and the simulation can tell: run three days with the never-checked rules
   removed from the compiled skill and compare. I will, once the depth run is in.
3. **Next decision class to delegate like the 16:55 fire:** approve by exception. He still reviews 30 drafts a day
   for the 10 that fire; the critic plus the simulation's judge can rank them, the system picks the 10, and ONE card
   lets him veto. Same ledger, same audit, 29 fewer decisions a day. After that: the "due today" follow-ups
   (`due_today.py`, built tonight): a promise he made comes back prepared on its day; the send stays his.
4. **Where the handoff is wrong:** "change the harness, keep the memory" is already true: the memory is markdown and
   JSON in git, any harness reads files. What does not port is the procedures (the scripts, the loop) and the
   judgement, and GBrain does not port those either. The thing to build toward a personal AGI is the loop that is
   running tonight: events in, decisions judged against truth, misses turned into hints, rules and fixes without him,
   re-tested the next day. That is a brain that learns; a store is a brain that remembers.
