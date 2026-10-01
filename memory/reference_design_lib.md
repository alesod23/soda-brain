---
name: reference_design_lib
description: /design-lib — the git-backed library of finished Claude Design work shared with Caleb across two personal accounts; the push-cheap/pull-expensive rule; the project-ID enumeration trap.
metadata: 
  node_type: memory
  type: reference
  originSessionId: b3102940-5e76-40e1-8354-ffd1883e672a
  modified: 2026-08-03T02:07:51.374Z
---

# /design-lib — shared Claude Design base library (built 2026-08-02)

## 🔴 PENDING: new account has ZERO Design projects

After the 2026-08-02 migration to `alessandro.sodano@cdtm.com`, `DesignSync list_projects` returns
**`[]`** (verified). All originals stayed on `primocaleb@gmail.com` and are **permanently
unreachable** from the new account — two personal accounts cannot share a Design project.
**Nothing is lost:** all 8 entries + the full design system were exported to `~/tundra-design`
BEFORE the switch. Rebuilding = restore from git, never a transfer from Anthropic.

Alessandro's stated minimum: **≥1 good proposal + the design system.** Full step-by-step lives in
the skill's "NEW ACCOUNT BOOTSTRAP" section — read that, do not improvise. Two things that bite:
`create_project` makes design-system projects ONLY (a deck needs the user to hand-create an empty
regular project first), and `finalize_plan` requires `deletes` even when empty.

`~/.claude/commands/design-lib/SKILL.md` + repo `~/tundra-design` (private GitHub, Caleb as
collaborator). **GitHub is the sharing layer, not Anthropic.**

**Why:** two personal Claude accounts CANNOT share a Design project. Live co-editing requires both
people inside ONE Team/Enterprise org (verified 2026-08-02); Alessandro chose not to buy that and
instead logs into Caleb's account in a separate browser profile for true co-editing. What the repo
solves is narrower: **finished work becomes a base either account can start new work from.** Finished
work is immutable, so there is no divergence problem, which is exactly why git fits here and would
NOT fit for syncing live documents.

**⚠️ THE DIRECTION RULE (the whole reason the skill exists):**
- `DesignSync write_files` with **`localPath`** reads from disk and uploads — contents never touch
  the model context. **Cheap. Verified working** (sandbox round-trip on the empty `Design System`
  project `cfc3a9f0`, then cleaned up).
- `DesignSync get_file` returns full content **INTO context**. One README cost ~4k words; a
  `.dc.html` deck is far bigger. **Never bulk-export this way.** Archive via the browser's
  **HTML export** from claude.ai/design instead.

**⚠️ THE ENUMERATION TRAP:** `list_projects` returns **design-system projects ONLY**. A regular
`PROJECT_TYPE_PROJECT` (e.g. `41320ac3`, which holds ALL the pilot decks) appears in **no listing
anywhere** and is reachable only by UUID. `library/INDEX.md` in the repo is the authoritative
project-ID registry — record every ID encountered, or the project is unrecoverable.

**Other constraints:** `DesignSync create_project` creates **design-system projects only**, so
seeding a normal deck needs the user to create an empty project in the web UI first and hand over
the ID. `finalize_plan` **requires `deletes`** even when empty. Seeding overwrites same-named files
with no undo, so target fresh projects only.

**Migration-safe:** the skill and repo are local files, so they survive an Anthropic account switch
untouched. Published artifacts do NOT survive (they never transfer between accounts, not even via
Anthropic's official personal→Team migration).

Related: [[project_account_migration]], [[reference_tundra_bridged_deck_source]],
[[feedback_deck_source_fingerprint_and_render]], [[feedback_tundra_deck_workflow]].
