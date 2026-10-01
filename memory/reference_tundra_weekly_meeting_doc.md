---
name: reference_tundra_weekly_meeting_doc
description: "The Tundra 'Weekly' recurring event carries a Google Doc ('Notizen') per occurrence — how to find it, and the ONLY working write path (Docs API + tokens/drive-tundra.json)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 26333c6f-5f43-43b7-badf-07594a1db485
  modified: 2026-08-09T23:17:35.564Z
---

Alessandro + Caleb run a recurring **"Weekly"** meeting (Google Calendar, organiser
`caleb@tundrahealth.ai`, on the **`alessandro@tundrahealth.ai`** calendar — NOT his cdtm primary,
which returns zero events). Recurring id `0jdbjrmmvff5g47r69edqb9qrq`; first occurrence Mon
2026-08-10 19:30–20:30 CEST. **Each occurrence gets its own Google Doc attachment titled
"Notizen"** (German — Caleb's locale), auto-created by Google Meet, and Alessandro opens it from the
calendar. He uses it to pre-load agenda items before the call, so "add X to the weekly notes"
means this doc, **not** Notion (he corrected me on exactly that, 2026-08-05).

**Find the doc for a given week:**
`list_events` with `calendarId: alessandro@tundrahealth.ai` over the target range → the occurrence's
`attachments[0].fileUrl` is the Doc. A new occurrence gets a NEW doc, so re-resolve every week
rather than caching the file id. (2026-08-10's is `1ByUiaKC4FswvlHC8u0aP3EKYQQWTjrjcyVOKrwUNGgk`.)

**Reading:** the claude.ai Drive connector (`read_file_content`) works — it's on the tundrahealth
account.

**Writing — the Drive connector CANNOT do it. It has no update tool.** And the local
`~/triage/drive_token.json` is bound to `alessandro.sodano@cdtm.com`, which gets a hard **404** on
these docs (they live in tundrahealth). The working path, set up 2026-08-05:
- `~/triage/setup_docs_tundra.py` → one-time OAuth, `login_hint` + account **verified before the
  token is saved** (same contract as `setup_all_accounts.py`, per
  [[feedback_oauth_login_hint_and_verify]]). Writes `~/triage/tokens/drive-tundra.json`,
  scope `https://www.googleapis.com/auth/drive`, confirmed account `alessandro@tundrahealth.ai`.
- Then the **Google Docs API** (`build('docs','v1')`) `documents().batchUpdate()` with that token.

## USE THE SCRIPT — `~/triage/gdoc_agenda.py` (SOLVED 2026-08-05, don't re-derive this)

```
python gdoc_agenda.py <doc_id> --owner Alessandro --item "EWOR hacker house"
python gdoc_agenda.py <doc_id> --show
```
`add_item` puts the item under the owner's level-0 bullet, creating that section if it doesn't
exist yet, and appending to it if it does. Both paths verified live.

**Sub-bullets (level 2) — the CLI cannot do them, but the module can.** `--owner`/`--item` only
expresses the 2-level shape. For a deeper row, import the module and call
`rebuild_section(docs, doc_id, "Notizen", tree)` with the tree from
`current_tree(paras, *find_section(paras,"Notizen")[1:])` and your `(level, text)` row spliced in
(driver: `scratchpad/add_subbullet.py`, used 2026-08-09 for "Founders Inc follow up?"). `add_item`'s
insert scan skips any row with level > 0, so later `--item` calls still land correctly around it. **Alessandro's instruction
(2026-08-05): "you're gonna have to figure out a way to go through this doc's limitation yourself
because it's gonna happen quite often" — so never hand him a formatting caveat again, just write it.**

**The API limitation the script works around:** you cannot set a bullet's nesting level.
`bullet.nestingLevel` lives on the bullet and is NOT recomputed from `indentStart` /
`indentFirstLine` — `updateParagraphStyle` moves the line visually but leaves the level (and the
bullet glyph) wrong; `deleteParagraphBullets` + `createParagraphBullets` on a paragraph sitting
BETWEEN members of an existing list re-normalizes it back to its neighbours' level. The only
reliable primitive is **inheritance** (`insertText` at the start of a paragraph adopts that
paragraph's level), which cannot produce "a level-0 bullet after a level-1 block".

**The workaround that does work — rebuild the whole section:** delete every bullet paragraph in the
section → strip the leftover paragraph's bullet and zero its indent (so nothing remains to
normalize against) → re-insert all lines as PLAIN paragraphs → set each paragraph's indent to
`36pt × level` → run `createParagraphBullets` ONCE over the whole fresh range. With no surrounding
list to inherit from, the nesting comes out exactly as specified.

**Method note for the next tricky Docs edit:** prove it on a `files().copy()` sandbox first, then
apply to the real doc, then delete the sandbox. That is how this got solved after three failed
in-place attempts.

Related: [[reference_notion_tundra_system]], [[reference_granola_auto]],
[[feedback_notion_write_needs_approval]]; stack map `medtech-brain/_system/TUNDRA-STACK.md`.
