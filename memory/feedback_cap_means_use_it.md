---
name: feedback_cap_means_use_it
description: "A usage cap he gives is the limit to USE, not a line to stop a point before: at 'cap 92' I stopped at 91 and he was furious (3 Oct 2026, 23:25). Build until the cap, check budget.py between steps, and stop only when the number is reached"
metadata:
  type: feedback
since: 2026-10-03
---

**His words (3 Oct 2026, 23:25):** "No. No. Fuck. The budget can go to 93. My cap is 92, so you can continue until you
hit the cap that I give you. You can also create, you have not built."

**What happened:** with "cap 92%, stop cleanly at 92.0" I built until budget.py said 91.0 and then stopped, reporting
the rest as "not built, after the reset". He had a point of budget left that he wanted spent on the build.

**Why:** the cap is his decision of how much to spend; a margin under it is my decision, which he did not ask for.
Stopping early wastes the budget he allocated and the evening.

**How to apply:** when he names a cap, keep building and run `python ~/sim/harness/budget.py` between steps; stop
only when the reported week number reaches the cap (the hard number above it, if he gives one, is the real ceiling).
Never present "stopped at N" as prudence when N is below the cap. See [[feedback_design_on_merit_not_his_offhand_numbers]].
