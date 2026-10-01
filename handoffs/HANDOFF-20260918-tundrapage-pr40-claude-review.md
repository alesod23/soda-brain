# Handoff (box -> laptop "✳ Website changes" session): TundraPage PR #40, act on the Claude review

His instruction (Telegram 18 Sept 17:18, replying to Caleb's WhatsApp): "give it to the ✳ Website changes session I have on my laptop. Tell it to come back to me (notify) with your UI questions to gather my input and an update on what you find."

Caleb (WhatsApp 17:09): "whenever you make a pr, always check a few min later what claude said and either press the resolve button if its not important or do another commit: https://github.com/Tundra-Health/TundraPage/pull/40"

Meaning: TundraPage has an automated Claude review on PRs. On PR #40 it left comments. New standing rule: after opening a PR, wait a few minutes, read the review, then per thread either Resolve (not important) or commit a fix.

To do (laptop, in the TundraPage checkout):
1. Read all review threads: `gh pr view 40 --repo Tundra-Health/TundraPage --comments`; `gh api repos/Tundra-Health/TundraPage/pulls/40/comments`; `gh api repos/Tundra-Health/TundraPage/pulls/40/reviews`.
2. Triage: fix vs resolve. Anything needing his judgement -> AskUserQuestion (he asked for UI questions).
3. Fix commits on the PR branch with the Claude trailer (memory feedback_tundra_commits_need_claude_trailer), push; resolve the threads that are not important (GitHub UI or `gh api graphql resolveReviewThread`).
4. Report back to him: what was fixed, what was resolved and why, anything still open. Notify (DA SYSTEM notification path / Telegram via the savior).
5. Save Caleb's rule as a memory (feedback_tundrapage_pr_check_claude_review) if missing.

The box has no GitHub API auth (SSH-only git), so it cannot read the PR comments itself. Also sent as a SendMessage to the laptop DA SYSTEM session for relay.
