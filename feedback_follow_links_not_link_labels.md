---
name: feedback_follow_links_not_link_labels
description: "When hunting for an artifact referenced from a sheet or doc, OPEN the linked targets; grepping the link labels is not a search"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8416f96f-965c-41e3-a618-179e3b6cd758
  modified: 2026-08-04T06:33:24.110Z
---

When looking for something referenced from a spreadsheet, doc, or wiki ("the code", "the template",
"the script"), **enumerate the unique linked targets and read their contents**. Searching the
container's own cell text only searches the *labels*, which are usually generic ("See template
here") and will never contain the keyword. A document linked repeatedly from the same sheet is a
hub document: read it first, not last.

**Why:** on 2026-08-03/04 Alessandro asked me to find the Who-is-Who auto-generation script. I
grepped the CDTM master sheet for `script`/`macro`/`.docx` (zero hits), searched all of Drive for
`*main*`, dumped the one visible Apps Script project, and concluded the code must be a hidden
container-bound script. The code was plain text inside the CDTM email/talk template doc
`1Fl_KGHTX1xtJwrzTkey9VdA1TGKeZyFy`, whose ID I had already printed **four times** from
`links.json` (rows H15, H17, H20, H23, all labelled "See template here") and which is also named in
`~/cdtm-taskforce/_START-HERE.md`. He had told me it was there. He had to find it himself.

**How to apply:**
- Build the set of unique target IDs from the links, then read each one. Six links is nothing; read
  them all before declaring something missing.
- Rank by repetition: the target linked the most times is the most likely hub.
- Never conclude "it does not exist / it must be hidden" while linked targets remain unopened. Say
  "I have not opened X yet" instead.
- A user saying "it is in <place>" is evidence, not a hypothesis to disprove. Exhaust that place
  literally before searching elsewhere.

Related: [[feedback_read_source_thread_before_acting]], [[reference_kb_systems]],
[[feedback_never_fabricate_fetched_content]].
