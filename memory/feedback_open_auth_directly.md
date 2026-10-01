---
name: feedback_open_auth_directly
description: "For any interactive auth/login/OAuth-consent step, OPEN the auth page directly in the user's browser instead of handing him a copy-paste command to run."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 760f12cc-7fa9-4277-8fe0-40d35a51cb76
---

When a task needs the user to authenticate or authorize (OAuth consent, Google sign-in, a "this app wants access" page, `gcloud auth login`, etc.), **trigger the flow DIRECTLY so the auth page opens in his browser** — run the script myself so its `run_local_server()`/`webbrowser` pops the consent page, or `Start-Process` the consent URL. He wants to click-to-validate.

**Do NOT** hand him a copy-paste shell command to run himself for the auth step.

**Why:** Caught 2026-06-23 on the Drive upload — I gave a `!`-command to paste instead of opening the consent page. He said "always do this [open directly]... ensure it doesn't reoccur across sessions."

**How to apply:** This OVERRIDES the harness session-default that says "suggest the user type `! <command>` for interactive logins." That default loses; open the auth page directly. Mirrored in `~/.claude/CLAUDE.md` (auto-open section). Related: [[feedback_output_delivery_rules]].
