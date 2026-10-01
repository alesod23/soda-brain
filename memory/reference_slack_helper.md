---
name: Slack Helper Location
description: Local Python helper at ~/.claude/slack/slack.py owns Slack OAuth/read/send for cdtm + xplore workspaces. Same pattern as triage gmail.py.
type: reference
originSessionId: f9479204-7034-4733-a3f2-da94aa9a073d
---
**Helper:** `C:\Users\Alessandro\.claude\slack\slack.py` (wrapper: `slack.cmd`).

**Why custom helper:** Anthropic ships no Slack MCP. Pattern mirrors `~/triage/gmail.py` (custom OAuth app + per-account user tokens) and `~/.claude/wa-daemon/` (local CLI for sends + reads).

**Workspaces (token files at `~/.claude/slack/tokens/<workspace>.json`):**
- `cdtm`   → alessandro.sodano@cdtm.com (team T0439JA12, user U0AFHUWDUA0)
- `xplore` → alessandro.sodano@tum.de   (team TM5AU8HU7, user U0AG54QGBE3)

**Auth method: browser cookie (NOT OAuth).** CDTM + XPLORE both block custom Slack app installs without admin approval, so the helper uses the `xoxc-` user token + `d` cookie from the user's logged-in browser session — same access as the user has in the Slack UI. The OAuth path (`auth` subcommand + `credentials.json`) exists in the helper but is unused for these two workspaces.

**Re-auth when token expires / cookie rotates** (`not_authed` / `invalid_auth` errors):
1. User opens app.slack.com/client/ logged in to both workspaces.
2. DevTools Console: `copy(JSON.stringify(Object.values(JSON.parse(localStorage.localConfig_v2).teams).map(t => ({name: t.name, domain: t.domain, token: t.token})), null, 2))` — paste clipboard back to Claude.
3. DevTools Application → Cookies → https://app.slack.com → copy `d` value (URL-encoded, ~300 chars).
4. Claude runs `python ~/.claude/slack/slack.py auth-cookie --workspace <cdtm|xplore> --token xoxc-... --cookie xoxd-...` — auth.test validates before saving.

The `d` cookie is shared across workspaces; the `xoxc-` token is per-workspace. URL-encoding in the cookie value (`%2F`, `%2B`, `%3D`) is preserved as-is.

**Subcommands:** `auth`, `whoami`, `list-channels`, `list-users`, `read`, `unread`, `search`, `send`. Run with `--help`.

**Send safety:** dry-run by default; show resolved channel/user + text, get explicit user "go", THEN re-run with `--confirmed`. Mirror gmail/wa confirmation rules.

**Skill doc:** `C:\Users\Alessandro\.claude\commands\slack\SKILL.md`. Setup walkthrough: `C:\Users\Alessandro\.claude\slack\README.md`.
