---
name: feedback_tundra_commits_need_claude_trailer
description: "Tundra org repos REQUIRE the Co-Authored-By Claude trailer on commits (Caleb's convention). This OVERRIDES the no-trailer rule that applies to Alessandro's personal repos"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcf4ed36-d8ed-4e48-817b-146c5998e5ca
  modified: 2026-08-12T18:56:38.454Z
---

2026-08-12: *"For the tundra GitHub commits, you needed to put your signature in the commit. Got told by Caleb. Record it from now"*.

**The rule:** on **`Tundra-Health/*` repos**, every Claude-assisted commit carries the Claude attribution trailer. Caleb's own history does this on every single commit, e.g. `8d99aaa`, `237cba9`, `67d4cbd`:

```
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

**Why this needs writing down: it directly contradicts [[reference_git_github_identity]]**, which says *"NO `Co-Authored-By: Claude` trailer on his commits"*. That rule is real but **scoped to Alessandro's OWN public repos** (set 2026-05-25 on terminal-inbox, after he saw "and claude" in the GitHub UI and disliked it). A future session reading only that memory would strip the trailer off Tundra commits, which is exactly what Caleb pushed back on. **Scope matters: personal repos = no trailer, Tundra org repos = trailer required.**

**Verified state of `Tundra-Health/TundraPage` on 2026-08-12** (so a later session does not "fix" something that is already right):
- All three of Alessandro's commits (`e490e8b`, `365d786`, `e3ebab2`) already carry `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, plus a `Claude-Session:` line that Caleb's commits do not have.
- **Nobody signs commits cryptographically** on this repo. Every non-merge commit is `%G? = N`, Caleb's included, and there is no `commit.gpgsign` / `user.signingkey` / `gpg.format` configured locally. The only `E` entries are GitHub's own signatures on merge commits made in the web UI. So "signature" here means **the trailer, not GPG/SSH signing** - do not go set up commit signing off the back of this.

Related: [[project_tundrapage_repo]], [[reference_git_github_identity]], [[feedback_git_commit_message_file_on_powershell]].
