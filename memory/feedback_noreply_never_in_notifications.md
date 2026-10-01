---
name: feedback-noreply-never-in-notifications
description: "noreply/automated senders are NEVER surfaced in SODANOtif notification cards — absolute, no deadline exception (notifications only; /triage keeps the May-18 exception)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
---

User rule 2026-07-19 ("noreply account are never to be shown"): notification cards (SODANOtif watch/recap/digest) must NEVER contain items from automated sender addresses (noreply@*, no-reply@*, donotreply@*, notifications@*, notify@*, alerts@*, mailer@*, ...). ABSOLUTE — overrides the deadline-notice exception that /triage SKILL.md line ~150 (2026-05-18) allows.

**Why:** a noreply item appeared in a notification card on 2026-07-19 morning; the user wants push surfaces pure signal (can't reply to a noreply anyway).

**How to apply:** rule lives in `~/.claude/snm-receiver/prompt.md` NEVER-block (loaded FIRST by sodanotif watch.ps1 + recap.ps1, explicitly overriding the appended skill body). Interactive `/triage` KEEPS the May exception (deadline notices on active services may still surface there) unless the user extends "never" to triage too.
