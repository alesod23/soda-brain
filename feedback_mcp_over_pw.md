---
name: feedback-mcp-over-pw
description: "Tool routing rule (applies EVERY time, all tools): MCP is primary and MUST be used whenever it can do the task. Playwright/browser is a fallback ONLY for genuine MCP gaps. If an MCP is down, restore the MCP before falling back to pw. LinkedIn pw was reinstated 2026-06-02 scoped to MCP-gap reads (e.g. saved posts)."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5b79f08b-7900-4194-840e-4800be587dbe
---

**Standing tool-routing rule — apply this EVERY time, for ALL tools (not just LinkedIn):**

1. **MCP is primary.** If an MCP tool can perform the task, it MUST be used. Playwright/browser automation is never the first choice.
2. **Playwright/browser only for genuine MCP gaps** — tasks the MCP literally cannot do (e.g. LinkedIn saved posts, which has no MCP endpoint).
3. **If the MCP is down/unavailable, do NOT jump to Playwright.** First try to bring the MCP back up (reconnect/restart). Only fall back to pw if restoration fails AND the task is a true gap.

**Why:** The MCP path is URL/API-driven (no selector breakage, no mojibake, no wrong-recipient sidebar misfire) and is the safer, more stable surface. Browser automation is brittle and higher-risk, so it is reserved strictly for what the MCP can't reach — not used as a convenience or an outage shortcut.

**LinkedIn specifics (reversed 2026-06-02):**
- On 2026-05-27 the user demanded deleting LinkedIn Playwright entirely. On **2026-06-02 the user reversed this**: reinstate pw "for such occasions" — i.e. the MCP gaps. The old "never recreate any pw path" rule is SUPERSEDED by the routing rule above.
- All LinkedIn actions that the MCP supports still go through `linkedin-mcp` (`send_message`, `connect_with_person`, `search_*`, `get_*_profile`, `get_inbox`, `get_conversation`, `get_feed`). See [[reference_linkedin_mcp]].
- MCP `send_message`/`connect_with_person` SEND immediately — no draft stage. For review-before-send, show the text in chat first, then send on the user's go.
- **pw is reinstated ONLY for MCP-gap reads.** The current gap is **saved posts** (`linkedin.com/my-items/saved-posts/`), which no MCP tool exposes. Helper lives at `~/.claude/linkedin-pw/` with its own dedicated Chrome user-data-dir (never the real Chrome profile, per [[feedback_browser_chrome_default]]); requires a one-time interactive login.
- If `linkedin-mcp` drops mid-session: reconnect/restart the MCP first. Do NOT improvise a browser workaround for anything the MCP can normally do.
