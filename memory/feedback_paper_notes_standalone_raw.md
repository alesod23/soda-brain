---
name: paper-notes-standalone-raw-with-inline-photo
description: How to handle handwritten/paper notes the user gives — standalone Raw file with the photo embedded inline.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8eabe48f-2156-48dd-b45d-d9c50450f3b1
---

When Alessandro gives handwritten / paper notes (a photo of his writing), capture them as a **standalone Raw file in the vault**, not buried inside a call/meeting note:

1. **Copy the photo into the vault** (e.g. `vault_kb/Raw/<MM-DD title>.jpg`) so Obsidian can render it. An image only embeds if it lives inside the vault.
2. **Create a standalone Raw `.md`** (`vault_kb/Raw/<MM-DD title>.md`) that **embeds the photo inline** with Obsidian syntax `![[<MM-DD title>.jpg]]` at the top, then a **transcription** of the handwriting below. Goal: he sees the photo + transcription directly in Obsidian without opening the image separately.
3. Keep it standalone. If the notes relate to a call, cross-link (`[[Call with …]]`), do not duplicate the notes inside that call note.

**Why:** he wants paper notes visible on his laptop in Obsidian, photo inline. Stated 2026-06-29 ("from now on, whenever i give you my notes in paper do it this way").

**Source photos** come from the "From phone" Google Drive folder, local at `G:\My Drive\From phone\` (see [[project_phone_to_desktop]]) which needs **Google Drive Desktop running** (drive `G:` mounts only then). MM-DD filename, no year (vault Raw convention). See [[feedback_no_em_dashes]].
