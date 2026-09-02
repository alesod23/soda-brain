---
name: Use plan compute, not API keys
description: User prefers Claude Code (plan compute) over a separate Anthropic API key for AI workflows
type: feedback
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
When designing AI workflows for Alessandro, default to Claude Code skills + MCP tools rather than a standalone Python/Node tool that calls the Anthropic SDK directly.

**Why:** he pays for the Claude plan; using an API key would double-bill compute he already has. He noticed and pushed back when the first triage plan proposed an API-key-based Python CLI.

**How to apply:**
- Reach for skills (`~/.claude/commands/<name>/SKILL.md`) and slash commands first.
- Use MCP tools (Gmail MCP, etc.) instead of building API wrappers.
- Reach for the Anthropic SDK only when the workflow MUST run outside Claude Code: a true background daemon on a server, scheduled jobs that don't open a Claude session, or shipping to other users.
- When unsure, ask: "can this be a skill that runs in his Claude Code session?" — if yes, do that.
