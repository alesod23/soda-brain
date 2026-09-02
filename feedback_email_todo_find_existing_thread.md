---
name: feedback-email-todo-find-existing-thread
description: "A to-do naming just a first name (\"Email John\") = find WHICH account has the existing thread and REPLY there — never assume the person/account or draft a brand-new email to a different same-named contact"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

Mistake 2026-07-23: the to-do "Email John" was about **John Heilbron** (he'd emailed an intro on the **tundra** account, `alessandro@tundrahealth.ai`, connecting Alessandro to Hunter Witmer) — the right action was a **draft REPLY in that existing thread**. Instead I assumed "John" = John Klink and drafted a NEW email on the **cdtm** account. Wrong person, wrong account, wrong action (new vs reply). User: "make sure mistakes like this are not happening in the future."

**Rule (any email to-do naming just a first name / an ambiguous person):**
1. **Don't assume the person or the account.** Alessandro has multiple Gmail accounts (cdtm, tundra, personal gmail). The same first name can map to different people.
2. **Search ALL relevant accounts for an existing thread first** (`gmail.py search --account tundra/cdtm ...`). If a conversation already exists, the task is almost always a **REPLY in that thread**, not a new email — use `--thread-id`.
3. **Match the account to the context** (Tundra business → tundra account; CDTM → cdtm; personal → personal). A Tundra intro belongs on the tundra account.
4. Only draft a brand-new email when no existing thread exists AND the recipient is unambiguous.
See [[reference_tundra_stack]] for the accounts; tundra account = `gmail.py --account tundra`.
