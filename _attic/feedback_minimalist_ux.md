---
name: Minimalist UX — one batch reply, not arrow-key loops
description: User strongly prefers compact list + one freeform reply over multi-step pickers
type: feedback
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
For interactive workflows (especially anything inbox/triage-shaped), do NOT use AskUserQuestion loops where the user has to send-and-wait per item. The wait-respond cycle feels slow and the option list feels heavy.

Instead: print a compact numbered list, then accept ONE freeform reply where the user specifies an action per item ("1 todo, 2 done, 3 suggest, 4 reply: text..."). Parse, execute in batch, show one-line summary.

**Why:** he explicitly pushed back after experiencing arrow-key flow in the triage skill — called it "too many options" and "takes too long". He's optimizing for minimum keystrokes and a minimalist setup.

**How to apply:**
- Default to compact list + single freeform parse for ANY multi-item workflow.
- Cap pre-input output to ≤50 words plus the list.
- Reach for AskUserQuestion only when the choice space is genuinely 2-4 mutually-exclusive options at a single decision point (not per-item).
- When you'd normally enumerate "here are your options," instead just give an example ("e.g. `1 todo, 2 done`") and trust him to extrapolate.
