# Handoff to DRAFTING (laptop QC session) - close the Chrome tab when a draft is done

> **DONE on the laptop, 2026-09-20 (DRAFTING).** Point 3 is implemented, and he then widened it:
> the group is now a two-way surface. See "What was built" at the bottom. Two manual steps are
> still his: reload the unpacked extension at `chrome://extensions`, and restart the intake server
> so the two new routes exist.

Written by the savior on the box, 2026-09-20, on his instruction: *"La cosa del draft tab delle
email spostala sulla claude session on laptop (QC) che si chiama DRAFTING. Ci lavoriamo, fagli
risolvere la cosa."*

## What he asked for

> Ci sono tipo 30 draft nella mia tab Draft di Chrome. E' importante che lo stesso sistema che
> controlla se le mie email sono state inviate o no sia in grado di capire se un'email che era in
> draft alla fine e' stata mandata. A volte lo mando io per conto mio e voglio quella tab
> eliminata, perche' sennò c'e' troppa roba che so che non devo guardare. Voglio invece che ci sia
> solo roba che so che e' ancora rilevante o ancora aperta.

So: the Drafts tab group must contain **only live, still-open drafts**. Anything sent (by the hub
or by him, by hand, from Gmail), rejected or binned must have its tab closed.

## Diagnosis already done on the box - do not redo it

Three separate leaks, two already fixed here.

1. **FIXED (box).** `reconcile.py` dropped a queue entry only on the single pass that marked its
   sidecar done. If that pass failed (dead Gmail token, box down), the entry stayed in the queue
   forever. Now every pass re-drops any entry whose sidecar is already `sent` / `rejected` /
   `draft_gone_unsent`.
2. **FIXED (box).** 23 of the 33 queue entries had **no sidecar at all** (pre-sidecar drafts and
   drafts whose sidecar was never written). The reconciler only ever iterated over sidecars, so
   those could never be dropped. It now also walks the queue itself: for an entry with no sidecar
   it asks Gmail directly, keeps it if the draft still exists, drops it if it is gone (whether it
   was sent or binned). Queue went **33 -> 10** on the first real run.
3. **STILL OPEN - this is the piece for DRAFTING.** `drafts-tabs` (the Chrome extension) never
   closes a tab once the entry leaves the queue. It only deletes the key from its
   `chrome.storage.local` "opened" map, which just means it would reopen it if it came back. So
   every tab it ever opened stays open until he closes it by hand.

## The fix, in the extension

Mirror (read-only backup, do NOT load it from here):
`task-land/_system/laptop-tools/browser-extensions/drafts-tabs/background.js`
The live one is the laptop copy that Chrome has loaded.

No new permission is needed: the manifest already has `tabs` + `tabGroups`, and the worker already
calls `chrome.tabs.remove` in `closeReplaced()` for superseded revisions. It is only missing the
same call for entries that left the queue.

In `poll()`, right where the "forget entries the reconciler dropped" loop is:

```js
// Forget entries the reconciler dropped (sent / rejected), so the map cannot grow forever.
for (const k of Object.keys(opened)) if (!live.has(k)) { delete opened[k]; changed = true; }
```

add, before or after it, the tab close itself:

```js
// His rule (2026-09-20): the Drafts group holds ONLY what is still open. An entry the
// reconciler dropped is done - sent by the hub, sent by him from Gmail, rejected, or binned -
// so its tab is closed here. Forgetting the key was never enough: the tab stayed open.
let closed = 0;
for (const g of await chrome.tabGroups.query({ title: GROUP })) {
  for (const t of await chrome.tabs.query({ groupId: g.id })) {
    const m = (t.url || "").match(/compose=([A-Za-z0-9]+)/);
    if (m && !live.has(m[1]) && !liveDraftIds.has(m[1])) {
      try { await chrome.tabs.remove(t.id); closed++; } catch (_) {}
    }
  }
}
status.closed = closed;
```

Two things to get right:

- `live` is currently built as `new Set(entries.map(e => e.message_id || e.draft_id))`, but the
  tab URL carries the **message_id** (`compose=<message_id>`). Build a set of message_ids
  explicitly for the comparison, or the first draft whose entry only had a draft_id will have its
  tab closed by mistake.
- **Never close a tab the queue has not yet been seen to contain.** If the fetch to
  `:4137/drafts/queue` failed, `entries` is empty and this loop would close the entire group.
  Guard it: only run the close pass when the fetch returned 200 **and** `entries.length > 0`.

Bump the manifest to 1.3 and update the description (it currently claims the worker "skips
anything the reconciler has since marked sent or rejected", which is true only at open time).

## How to verify

1. `GET http://127.0.0.1:4137/drafts/queue` - count entries (10 as of this writing).
2. Count the tabs in the Drafts group. After one poll cycle (30 s) the two numbers must match.
3. Send one of the queued drafts by hand from Gmail. Within 5 minutes the box reconciler drops it
   from the queue; within 30 s more its tab must disappear on its own.
4. Kill the intake server, wait a poll, and check that **no** tab was closed (the guard above).

## Files

- box, already changed: `task-land/_system/drafts/reconcile.py` (backup of the queue:
  `queue.jsonl.bak-20260920`)
- laptop, to change: the loaded `drafts-tabs/background.js` + `manifest.json`
- mirror to keep in step afterwards:
  `task-land/_system/laptop-tools/browser-extensions/drafts-tabs/`
- lane contract: `task-land/_system/WORKPLAN-20260908-draft-review-lane.md`

---

## What was built (laptop, 2026-09-20)

Point 3 as specified, plus his extension of it the same evening: *"sometimes I close a tab myself.
That means we're done with it and you should know it (could also be that we're just not sending it
anymore)"*, and *"if I want to reinstate it, or add a new one to the mix (e.g. I start a draft
myself and want to put it in the system), I just move that tab inside the group"*.

So the Drafts group is now the surface, read in both directions:

| Gesture | Meaning | Effect |
|---|---|---|
| Entry leaves the queue | sent / rejected / binned | Its tab is closed (point 3) |
| He closes a tab | done, or not sending it after all | Sidecar `abandoned`, entry dropped, hub card pulled. **The Gmail draft is left alone** |
| He drags a tab into the group | put this draft in the lane | Adopted: queue entry + stub sidecar, or an `abandoned` sidecar flipped back to `open` |

Both of his gestures must hold for **60 s** before they count: he shifts tabs along the strip with
ctrl+shift+pgup/pgdn, so a tab can sit in the group for a few seconds without meaning anything.
Nothing uses a timer (an MV3 worker dies after ~30 s idle): each poll writes a first-seen stamp to
`chrome.storage.local` and the gesture is applied on a later poll.

Guards, all in `readGestures()`:
- A close only counts for an id seen present **in the same browser session** (a counter bumped on
  `onStartup`). After a Chrome restart every tab is gone while the queue is unchanged, which would
  otherwise read as him closing all of them at once.
- `chrome.windows.onRemoved` pauses close-reading for 2 minutes: a closing window takes its tabs.
- Nothing is read at all unless the queue fetch returned 200 with at least one entry.
- `closeDone()` only closes ids the worker has seen **in the queue** (`wasQueued`), so a tab he
  dragged in is never swept away while it is settling.

### Files
- `browser-extensions/drafts-tabs/background.js` + `manifest.json` (now **1.4**), mirrored to
  `task-land/_system/laptop-tools/browser-extensions/drafts-tabs/`.
- `task-land/_system/drafts/tabgesture.py` (new): `abandon` / `adopt`. Idempotent both ways.
- `.medtech-crm/intake-server.js`: `POST /drafts/abandon`, `POST /drafts/adopt` relay to it.
- `task-land/_system/drafts/reconcile.py`: `abandoned` added to `DONE`. Required, because the Gmail
  draft deliberately survives: without it the reconciler would see a live draft and re-chase it.

### Verified here
`node --check` on both JS files, `py_compile` on both Python files, `abandon` run against a
temporary queue + sidecar (status flipped, log line added, entry dropped, second call a no-op).

### Verified on the live server (2026-09-20, after a restart through Coattio-Watchdog)
`POST /drafts/abandon` with an id that is not queued -> `{"ok":true,"noop":"not in queue"}`; with a
malformed id -> 400 `bad message_id`; `POST /drafts/adopt` with an unknown compose id -> the Gmail
lookup runs across the accounts and answers `no Gmail draft with that compose id` in 7.5 s.

### NOT verified yet (needs the extension reload)
Tab counts matching the queue after a poll; a hand-closed tab producing `abandoned`; a dragged-in
tab being adopted (this one calls Gmail, which the sandbox this session runs in cannot reach);
the window-close and server-down guards.
