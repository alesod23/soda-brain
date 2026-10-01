---
name: feedback_tundrapage_pr_review_loop
description: "Caleb's rule for Tundra-Health/TundraPage PRs: a few minutes after opening a PR, read the automated Claude review comments and either resolve each thread or push a fix commit; never leave them hanging"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-18T15:21:25.177Z
---

**Rule from Caleb (WhatsApp, 2026-09-18 17:09):** "whenever you make a pr, always check a few min later what claude said and either press the resolve button if its not important or do another commit". The repo runs an automated Claude review (`claude[bot]`, inline comments on every push). After opening or pushing to a PR on `Tundra-Health/TundraPage`: wait a few minutes, read every review thread (`gh api repos/Tundra-Health/TundraPage/pulls/<n>/comments`), then for each thread either push a fix commit on the PR branch (valid point) or resolve the thread (cosmetic, out of scope), via GraphQL `resolveReviewThread` with the thread id from `pullRequest.reviewThreads`. Report to Alessandro what was fixed and what was resolved and why.

**Why:** Caleb reads the PRs; an unanswered bot thread looks like nobody looked. First applied on PR #40 (2026-09-18): one thread, the SVG aria-label and file docblock still said "single record" after the copy moved to "layer"; fixed in a follow-up commit and the thread resolved.

**How to apply:** treat "open PR" as unfinished until the review threads are handled; commits carry the Claude trailer ([[feedback_tundra_commits_need_claude_trailer]]); the branch and env gotchas are in [[project_tundrapage_repo]]. A Vercel "must be a member of the team to deploy" comment on his PRs is Caleb's side (add alesod23 to the Vercel team), not a code problem.
