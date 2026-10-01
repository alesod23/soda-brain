---
name: feedback_never_collapse_what_he_must_read
description: "UI rule 2026-09-19 (hub-review page, first feedback): anything he must read to decide (contact names, email body, the option details) is visible by default, never behind a click or a collapsed <details>. Collapse only secondary material. Same spirit as the always-visible keyboard legend."
metadata:
  type: feedback
---

**His words (2026-09-19 00:58, first look at the hub-review page):** *"the contact name is the most important thing, cant have it hidden for me to click, cmon... i have to open it. makes no sense to have something closed that i have to for sure open.."*

**Why:** on a phone every extra tap is friction, and a review page exists to decide fast; hiding the decisive content (who the contact is, what the email says) defeats it.

**How to apply:**
1. Decisive content first and open: contact names as the card title, email body expanded, option details visible. Boilerplate ("Add to the CRM? yes = all...") demoted to small grey, never above the content.
2. `<details>` / accordions only for material that is truly secondary (hub context of a draft, sources, logs).
3. Applies to every review surface: hub-review (4142), GTM boards (4141), Trippy boards (4126), daily page callouts (the help callout may stay collapsed: it is help, not content).

Related: [[feedback_review_pages_need_keyboard_shortcuts]], [[feedback_hub_digest_replaced_by_review_page]], [[reference_hub_review_ui]].
