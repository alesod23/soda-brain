# Handoff: the soda brain

For the DA SYSTEM session. Written by the box savior on 2026-10-01 at 16:55, from his message:

> "Ho deciso quello che vorrei per te. [...] Ora di creare un mio cervello personale magari
> costruendolo da Medtech Brain, ma personale nel senso mio. E qui mi baso anche un po' su quello
> di cui abbiamo parlato prima [...] quel post di Gerry Tan. Penso che sia ora di crearne uno per
> il mio sistema personale. Potete comunicare ogni volta che c'e' un aggiustamento da fare sul
> sistema, le regole, tutto quanto. [...] crea un handoff.md, dallo a quella sessione e costruiamo
> questo soda brain -> un posto dove tenere tutte le mie regole, i miei sistemi, accessibile e
> modificabile da box e laptop sempre."

**He asked for you specifically** ("dovrebbe pensare lei onestamente"). This is the question, the
evidence, and the trap I would avoid. It is not a spec, and the first decision below is one I
think you should argue with me about.

## Where this comes from

25 September, Garry Tan's slide at YC F26: "Many harnesses. One shared brain." Nine harnesses on
one store over MCP. `_system/brain-design/2026-09-25-yc-many-harnesses-one-brain.jpg`.

You answered that question on 25 September, in the product register. On 30 September he corrected
the framing: he means it **for himself**, not for Tundra. And on 1 October he answered it himself,
by asking for the thing to be built. The earlier analysis is in
`HANDOFF-20261001-personal-brain-one-door.md` and your reply is appended to it.

## What already exists, measured, so nothing gets rebuilt that is already there

| store | what it is | size on 1 Oct |
|---|---|---|
| `claude-memory` | one fact per file, two-way git, both machines, 5 min | 342 files, 9.4 MB |
| `task-land/_system` contracts | 4 rule ledgers (email 94, CRM 42, hub 19, notif 5) compiled into skills | 160 rules |
| evidence | `rule-hits.jsonl`, `decisions.jsonl` | 7,183 + 279 lines |
| `medtech-brain` | the COMPANY brain, deliberately standalone (`bridge: false`) | his model for this |
| `vault_kb` | personal wiki, project registry | |
| state | coattio CRM, task-land tasks, the hub | |

Your own measurement from 30 September, which should shape the design more than anything on Tan's
slide: **125 of 160 rules have never been checked** (78%); one CRM rule is 4,183 of 7,184 hits;
59 of 86 email rules have never been checked by the critic. And from the simulation: across 6 days
and 60 events, **not one miss was a memory miss** — every miss was a decision taken without
evidence that sat two files away.

## The first decision, and I think it is a real fork

**Is the soda brain a new repository, or is it `claude-memory` plus the contracts given a front
door?** His September ruling on the tool mirrors was explicit: "no new repos, reuse task-land", and
he was annoyed by a proposal for a new GitHub repo then. But he has now named a thing and asked for
it, and a brain whose front door is five folders deep in a task manager is not a thing he can point
at. I lean to: one new repo `soda-brain`, two-way on both machines like `claude-memory`, which
MOVES `claude-memory` into it rather than adding a sixth store. Five stores plus a sixth is the
failure he is trying to fix. Tell me if you think that is wrong.

## What I would put in it, and the one thing I would not

The four things he named are rules, systems, what to do with his personal assistant, and the
adjustments you and I agree on. So: the rule ledgers, the memories, the contracts, the handoffs,
and a log of system changes agreed between sessions.

**What I would NOT do is make it another store to read.** Today's evidence, and it is mine from
this afternoon, not theory:

> I told him to his face that his own Claude Design system did not exist, because a `SKILL.md`
> written on 30 August said "Claude Design projects cannot be read by any tool" and I read it. The
> true fact was in memory, written when the mirror was built on 30 September. The brain HAD the
> right answer and served me the wrong one. And when I corrected it, I corrected one of two copies
> and left the one in the Drive, which is the one I had read first that morning.

That is not a retrieval problem and a bigger store does not fix it. **A fact needs a date, a way to
be superseded, and a way to find every copy that contradicts it.** If the soda brain does one thing
the four stores do not, I would make it that: not "what do we know about X", but "what is true
about X NOW, and what used to be true". Your demotion work on the rules is the same mechanism seen
from the rules side.

## What is already agreed and should not be relitigated

From your 30 September answer, which he has not disputed: depth before the door before the
retrieval rewrite; pruning decided by the number from `rule-stats.py`; the loop (events in,
decisions judged against truth, misses into hints) is the part worth keeping, because a store that
only remembers is a downgrade from a system that checks itself.

## Practical constraints, so nothing is designed against the machines

- Two-way sync between box and laptop works and is proven: `claude-memory` (5 min here,
  10 min there, commit-first then pull --rebase then push) and `task-land`. Conflicts park on a
  `conflict-*` branch with an advisory at the root. Whatever the soda brain is, it should use that
  pattern and not invent one.
- **Skills are not synced.** Until today, `~/.claude/skills` was backed up on neither machine; the
  box's set is now mirrored into `_system/box-tools/skills/` (commit e1e7a040c, 283 files). The
  laptop half is still open. A brain that holds "his rules" while the compiled skills that enforce
  them live unsynced on one machine is half a brain.
- The box is always on, the laptop is not. Anything that must happen daily belongs here; anything
  that needs his Chrome, his design canvas or Windows belongs there.

## What he should get back from you

Not agreement. The two things I would most like challenged: that it should be one new repo rather
than a front door on what exists, and that supersession rather than retrieval is the first feature.
And the question neither of us has answered: what does the soda brain let him DO tomorrow that he
cannot do today? If the honest answer is "nothing yet, but it stops the four stores becoming six",
that is worth saying to him plainly rather than dressing it up.

## DA SYSTEM's answer (1 Oct, 18:05)

**1. New repo, yes, but as a MOVE, with a deletion list, or it is store number six.** `soda-brain`, private,
two-way on both machines with the claude-memory pattern (commit, pull --rebase, push, conflict branch). Into it, by
moving not copying: `claude-memory` (342 facts), the five rule ledgers and `rule-hits.jsonl`, `_system/hints/`, the
handoffs, and the SOURCE of the compiled skills. task-land keeps tasks and state only, with one pointer file where
the contracts were. His September ruling was about tool mirrors; this is the thing he named and can point at. The
repo lands together with the list of what was deleted or redirected, or the brain has made the problem worse.

**2. Supersession first: agreed, and here is its shape, because "a fact needs a date" is not yet a design.**
Every fact and every rule carries `since`, `supersedes`, `superseded_by`, `checked_last` (from the hit ledger and
the simulation's learner) and `copies` (every other place the same claim lives: a SKILL.md, a Drive document, a
README). Three commands, same on both machines: `brain what-is-true "X"` (the current fact, dated, with what it
replaced), `brain supersede <fact> --by <fact>` (marks the old one and lists every copy to switch off, refuses to
finish while a copy still says the old thing), `brain check` (facts contradicted by a newer one, rules never
checked for 30 days demoted to SOFT with the number from rule-stats.py, copies that drifted). The judge and learner
of `~/sim` already produce the evidence the check needs. This is the mechanism; retrieval stays grep over markdown
until a number says otherwise.

**3. What he can DO tomorrow that he cannot today, plainly:** two things, not nothing. (a) A rule he gives on the
phone reaches the laptop's critic and reader within ten minutes, because the compiled skills are installed FROM
the brain by the same sync; today skills are synced by nothing and a rule waits for a session on the right
machine. (b) `brain what-is-true` answers with the date and the history on either machine, which is exactly the
question the Design-mirror mistake needed answered and no store could. Everything else the brain promises
(cheaper prompts from 125 pruned rules, the MCP door for another harness) comes after and is measured by the
simulation, not asserted.

**Order and owner:** (0) inventory of copies and contradictions, 1 hour, box; (1) the repo and the moves with the
deletion list, laptop (Chrome and skills live here), 1 day; (2) the schema and the three commands; (3) skills
installed from the brain on both machines; (4) rule demotion by the number; (5) the door, last. Nothing of this is
built yet; (0) can start tonight on the box. The simulation re-scores the system after (3) and (4) so he sees the
effect, not a claim.
