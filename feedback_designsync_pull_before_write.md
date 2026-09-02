---
name: feedback_designsync_pull_before_write
description: "NEVER push a Claude Design file from a local copy. Always get_file the remote first and apply edits on top, or the user's own edits get overwritten."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e29d7091-5808-492a-b725-082f5123e799
  modified: 2026-07-31T00:24:20.135Z
---

Alessandro edits Tundra decks directly in **claude.ai/design** between my turns. If I rebuild from the copy I cached earlier in the session and then `DesignSync write_files`, **his edits are silently destroyed**. He caught this on 2026-07-30: *"a volte faccio modifiche con edit e tu le mangi"*.

**Rule, every single time before a `write_files` on a Design project:**
1. `DesignSync get_file` the target `.dc.html` **fresh** from the remote.
2. Diff it against my last-known local copy. If they differ, **his edits landed in between**: rebase my changes onto the remote version, never the other way round.
3. Only then apply my edits and push.

Never treat a local scratchpad `.dc.html` as the source of truth. The **remote is always the source of truth**; the local file is a working buffer that goes stale the moment I hand control back.

Same discipline for the deck-provenance rule in [[feedback_deck_source_fingerprint_and_render]] (fingerprint the real source before translating) and [[feedback_tundra_deck_workflow]].
