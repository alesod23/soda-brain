---
name: Triage workflow rules — drafts and auto-done
description: For email replies, ALWAYS show the full previous message + the draft together. For triage, items not explicitly mentioned in the user's batch reply are treated as read (do NOT mention next round even if still UNREAD).
type: feedback
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
Two rules added 2026-05-10. Both apply to the triage skill and to any "answer this email" / "reply to X" request that arises outside triage too.

## Rule A — drafts always come paired with the original

When drafting an email reply, show in the same response:

1. **The full previous message** (sender + subject + body, untruncated). Pull from `gmail.cmd get --account <X> --thread-id <Y>` if not already in conversation context.
2. **The proposed draft** (recipient + subject + body) underneath it.

Reason: the user wants to verify the original is what they remember and that the draft actually addresses it. A draft alone has no anchor.

This applies any time the user asks for an email response — not just inside `/triage`. If they say "reply to X" or "draft a reply about Y," produce both halves.

## Rule B — silence = read (cross-tool, /triage AND /snm)

After the triage skill displays its actionable list and the user provides a batch response, items the user did NOT mention are treated as **read** even if they're still UNREAD on the source side. Do NOT re-surface them in the next triage round.

**Strengthened 2026-05-14**: if the user takes the time to give EXPLICIT instructions for SOME items (e.g., `1 reply: ...`, `2 answer ok`, detailed multi-step instructions), then everything else in that round is treated as **considered red / not worth keeping alive**. The signal is: when the user invests effort in selecting items to act on, the unselected items are explicitly NOT worth a future round — drop them all.

User's verbatim 2026-05-14: "If I take the time to exactly tell you what to do for certain items… then it means that nothing else is worth keeping alive for another triage session, because they're all red. This should be known between SnM, and Triage through shared memory."

**This applies BOTH ways across `/triage` and `/snm`:**

| User action | Effect |
|---|---|
| `/triage` round: user gives verbs for items 1, 2 | Items 3..N auto-marked done (per-channel state). SNM's `state.json#actionable` also cleared at round end (per `/triage` step 7d). |
| `/snm`: user says `1 done, 2 not urgent` (or detailed verbs) | Items 1+2 marked done in per-channel state. Other items in SNM's surfaced list also auto-marked done — because the user has reviewed the list, picked what mattered, and the rest is signal-noise. |

Implementation — at the end of every round, after applying explicit user verbs:

- Gmail: for each unmentioned displayed item → apply `triage/done` + remove `UNREAD`.
- WA: for each unmentioned displayed item → append to `wa-state.json#done` with current `lastInTimestamp`.
- Slack: rely on shared cutoff (`~/triage/state.json#last_check_unix`) to exclude prior rounds' shown items in next fetch. (For Slack DMs/mentions where the user explicitly wants something to NOT resurface even on new activity, would need a `slack-state.json` mirror — not built today; the cutoff handles it for typical patterns.)
- SNM state file: clear `state.json#actionable[]` at round end (the surfaced items are either acted on or auto-done; either way they shouldn't stay in the list).

Only carryover trigger phrases keep an item alive across rounds: `todo`, `defer`, `keep for later`, `keep this for later`, `save for to-do`, `save this for my to-do`, `preserve`, or anything that semantically reads as "hold for next round". Anything else (including silence, "ok", `done`, `read`, a `reply: ...`, a `suggest`) drops the item.

## Rule C — state.json cutoff is sacred

Every successful triage round MUST update `C:\Users\Alessandro\triage\state.json` `last_triage_at` + `last_triage_unix`. The next round MUST fetch only items strictly after that timestamp:

- Gmail: `after:<last_triage_unix>` in every Query B.
- WA: `--hours ceil((now - last_triage_at) / 3600)` (rounded up).
- Slack: same `--hours` value.

**Plus** apply the local state filters:

- WA: every chatId present in `wa-state.json#done` whose `lastInTimestamp >= currentChat.lastIn.timestamp` MUST be dropped before display. (Equality counts — a same-timestamp entry means it was processed last round.)
- WA cleanup: drop `done[chatId]` only when the new incoming has a strictly newer timestamp AND is not a pure reaction/emoji.

The user explicitly stated 2026-05-11: "you are saving in your memory when the triages requests are made. then you are only looking at unread messages FROM the last triage and so the ones in the previous triage will never show up again". An item that already showed in a prior round must never appear again unless a NEW non-reaction message arrived after the cutoff. Missing this filter is the #1 way to re-surface noise — verify wa-state.json IS being checked before printing the table.
