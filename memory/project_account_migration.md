---
name: project_account_migration
description: "Anthropic account switch from primocaleb@gmail.com to a new Max account — the runbook location, what is account-bound vs local, and the three pre-existing breakages not to misdiagnose."
metadata: 
  node_type: memory
  type: project
  originSessionId: b3102940-5e76-40e1-8354-ffd1883e672a
  modified: 2026-08-02T22:35:20.935Z
---

# Anthropic account migration (opened 2026-08-02, status PENDING)

Switching from **`primocaleb@gmail.com`** to a new Max account.

**THE RUNBOOK:** `~/.claude/MIGRATION-account-switch.md` — read it before touching anything
migration-related. It holds the verified pre-logout `claude mcp list` output as the diff target,
plus per-server "account-bound vs local" classification. A banner in `~/.claude/CLAUDE.md` points
there; delete the banner when the runbook says `Status: DONE`.

**The key structural fact:** `~/.claude/.credentials.json` has `mcpOAuth` as a **sibling** of
`claudeAiOauth`, not a child. Third-party MCP tokens (notion, granola, lemlist, oxygen, vercel) are
grants from those vendors and survive an Anthropic logout. If the file gets wholly rewritten, splice
`mcpOAuth` back from `~/.claude/backups/credentials-premigration.json` rather than re-authing five
servers by hand.

**Only genuinely account-bound:** the three claude.ai Google connectors (Drive
`drivemcp.googleapis.com`, Calendar `calendarmcp.googleapis.com`, Gmail `gmailmcp.googleapis.com`)
— they have NO local config because the account supplies them — plus published Artifacts and quota.
Zotero looks similar but is merely **project-scoped** in `.claude.json` under `C:/Users/Alessandro`,
so it is local and safe. That pair is the easy thing to get wrong.

**The whole Telegram stack is independent of Anthropic** — bot token in
`channels/telegram/.env`, allowlist in `access.json`, and the Telethon **`tg-reply-resolver/user.session`**
authenticating as the human Telegram account. Never re-pair these during a Claude migration;
re-login would need an SMS code for no reason.

**⚠️ Three things were ALREADY broken on 2026-08-02, BEFORE any switch** — do not blame the
migration: claude.ai **Gmail** needs auth; **plugin:vercel** needs auth; **plugin:telegram** fails
with `-32000: Connection closed` (bun 1.3.14 IS installed, so not a missing runtime; cause
undiagnosed).

**Opportunity during restore:** re-add the Google connectors under `alessandro@tundrahealth.ai`
instead of the legacy `alessandro.sodano@cdtm.com`, closing the gap recorded in
`medtech-brain/_system/TUNDRA-STACK.md`. Update that doc and MEMORY.md afterwards.

Related: [[reference_granola_auto]], [[reference_telegram_channel_plugin]], [[reference_tg_bridge]],
[[reference_restore_cc]].
