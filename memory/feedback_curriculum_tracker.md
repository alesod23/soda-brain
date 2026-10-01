---
name: feedback-curriculum-tracker
description: "Alessandro tracks his full-stack learning in a curriculum file. When he says `/btw` or asks \"explain what just happened\" / \"what did you do\" / \"/explain\", teach the underlying concept in CS-student first-principles terms AND update the curriculum file with the topic + citation."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 63d287e6-f74a-4ee6-b639-921423892c47
---

# Curriculum tracker workflow

**v2 (2026-06-11): the tracker is now a data-driven web app.** Canonical curriculum data lives in **`C:\Users\Alessandro\.claude\curriculum-server\data\curriculum.json`** (phases → topics with lesson/history/status/video/examples). The server renders `app.html` from it at localhost:4117. Sidecars: `data/inbox.json` (daily CDTM-Eng scrape backlog, approve→topic.examples), `data/notes.json`. Daily scrape: `crawl-daily.mjs`, Task Scheduler `Curriculum-Daily-Crawl` 19:00. Videos per topic: `fetch-videos.mjs` (YouTube most-viewed concise). No chatbot (removed at user request; he uses Comet+Perplexity).

The two files on `/btw` are now:

- **`C:\Users\Alessandro\OneDrive - HEC Paris\learning\fullstack-curriculum.md`** — human-readable text export, durable, version-controllable
- **`C:\Users\Alessandro\.claude\curriculum-server\data\curriculum.json`** — the data the web app serves (status, history entries, lessons)

**Both must be updated on every `/btw`.** They diverge silently if you only update one.

LEGACY (pre-2026-06-11): `fullstack-curriculum.html` in OneDrive with the embedded `PHASES` const is FROZEN — the migration snapshot. Do NOT update it on `/btw` anymore; `migrate.mjs` extracted it into curriculum.json.

## Local server (the canonical viewer)

The HTML is served by a local Node server at **`http://localhost:4117`**.

- Server code: `C:\Users\Alessandro\.claude\curriculum-server\server.mjs`
- Starter: `C:\Users\Alessandro\.claude\curriculum-server\start.ps1`
- Watches `fullstack-curriculum.html` and pushes a live-reload event via SSE → the page in the browser auto-refreshes whenever the source file changes
- No-cache headers so manual refresh also always gets the freshest version

**NO custom recap footer (retired 2026-06-15).** Alessandro killed the `↻ Tracker: localhost:4117` line that used to be appended at the end of every curriculum-session message — he found it noise. Treat the tracker URL like any other link: surface `http://localhost:4117` inline (clickable, standard CLAUDE.md link rules) ONLY when the turn actually calls for it (he asks for the link, or you just made a change he'd want to view). Do not append a standing footer, and never mention it in unrelated sessions.

If the server is not running and Alessandro reports the page does not load, point him at `C:\Users\Alessandro\.claude\curriculum-server\start.ps1`.

The /btw flow now is (v2):
1. Update `fullstack-curriculum.md` (the citations, progress counters, recall index)
2. Update `data/curriculum.json` (same data: topic `history` entry `{date, action, project, file, session_id, note}`, recompute `status`)
3. The app fetches fresh JSON on load (no-cache); `app.html` edits live-reload via SSE
4. Surface the link only if relevant (no standing footer — see above)

## Tutor chat + precious context (built 2026-06-15)

Each topic in the web app has a **tutor chat** (per-topic, so it's unambiguous which topic he means; he can also say "apply to all"). He uses it to steer the explanation: "too long", "idk what this means, you assumed wrong", "could we say X is like Y?". Two outputs on **"Send to curriculum"** (commit):
- an optionally revised `topic.lesson` (only the fields he agreed to change), and
- durable **context**: imperative instructions saved to `topic.context[]` (this topic) or `curriculum.global_context[]` (scope "all"). Shown in-app under "Your instructions to the tutor" and the **Preferences** tab.

**This context is precious and BINDING.** Every tutor turn replays global + per-topic context (lib/chat.mjs), AND every time YOU (Claude) write/refine an explanation for a topic — on `/btw` or otherwise — you MUST read `curriculum.global_context` + that topic's `context[]` first and honor them (length, assumed-knowledge, analogy style, etc.). They encode how he wants to be taught; ignoring them is the main failure mode.

Backend: in-process OpenAI (`lib/llm.mjs`, key from tundratalents/.env, `CHAT_MODEL` default gpt-4o) — same key the crawl classifier uses. No Anthropic key on the machine yet; swap in llm.mjs if one appears. Endpoints: `GET/POST /api/chat`, `POST /api/chat/commit` (accepts `instruction` to commit only PART of the chat), `POST /api/chat/clear`, `DELETE /api/context`. Chats persist in `data/chats.json`.

UI (v3, 2026-06-15): the tutor chat is a **collapsible right-docked widget** (`#chat-widget`), opened per-topic via each topic row's "Chat" button (collapse button + reopen tab; not inline). It's example/project-aware — he can deep-dive any attached example. Examples lists are collapsible (default collapsed when >2).

## Formatting, brevity, edit, undo (2026-06-17)

- **Markdown is the one stored format.** Legacy lessons were HTML (`<strong>`,`<code>`,`&lt;` entities); chat commits emitted markdown → showed literal `**`. Fixed: `migrate-lessons-md.mjs` (one-time, guarded by `curriculum.lessons_md`) converted all 69 lessons HTML→markdown; `app.html` has `renderMd`/`renderInline` (escape-first; **bold**, `code`, *em*, nested `-`/`1.` lists, paragraphs) used for lesson def, fp q/a, example purpose, example text, AND chat + quiz bubbles. **Anything new written into a lesson must be markdown, never HTML.**
- **Brevity is the default** (his standing instruction): chat + commit + quiz system prompts now enforce ~150-word max, lead-with-core-idea + short bullets, markdown. Deep-dives are the only exception (he must ask). Lesson `def` on commit is capped ~120 words markdown.
- **Manual lesson edit**: each topic's Lesson has an "Edit" button → inline editor (def textarea, example code+caption, add/remove fp Q/A rows) → `POST /api/topic/lesson`. Lets him delete parts the chat wrongly added.
- **Undo**: every mutating op (chat commit, backlog approve, manual edit) snapshots the topic first (`data/undo.json`, `pushUndo`, 15 deep). "Undo last change" button on the Lesson (shows when `topic.undo_count>0`) → `POST /api/topic/undo` restores lesson+context+examples+status+strength+quizzes.
- Favicon: both tracker pages use a 🤓 (nerd) inline-SVG emoji favicon (he asked, 2026-06-16).
- Cross-cutting CDTM-Eng tool/best-practice insights that fit no single topic → route to the curriculum's existing "Appendix B / modern stack" area (his call 2026-06-17; no separate bucket built).

## Quiz / strength (built 2026-06-15)

**Quiz tab** = open-ended, chat-based self-test per topic. `lib/quiz.mjs`: `quizQuestion` (one first-principles question), `quizReply` (concise, hint-aware), `quizGrade` (JSON: score 0-100 + level weak/developing/solid/strong + hints_used + rationale + gaps; weights correctness, depth, and INDEPENDENCE = fewer hints scores higher). Endpoints `/api/quiz/start|message|grade|clear` + `GET /api/quiz`. Active quiz transcripts in `data/quiz-chats.json`. Grading writes `topic.strength` (latest score) + `topic.quizzes[]`. UI: weakest/untested-first dropdown, quiz chat panel, "Grade me", grade card, "Your strengths" list; strength chips on curriculum rows. **`topic.strength` is THE weak-topic signal** the project-review flow (next slice) uses to prioritize suggestions.

## Project sources + per-project view (built 2026-06-15)

**`/sde` skill** (`~/.claude/skills/sde/SKILL.md`; renamed from `/cs` at user request 2026-06-15; autocompletes after 2 letters, no sd* collision) marks his own Claude-Code-built tools as curriculum SOURCES. Mines **BOTH** the project's handmade source code AND its Claude Code build-session transcript(s). Pipeline: `lib/project-ingest.mjs` (`collectCodeFiles` strict ignore filter: node_modules/.next/dist/build/lockfiles/minified/generated; `collectSessionSnippets` bounded) → `lib/classify-project.mjs` (recall classifier) → `ingest-project.mjs --path --name --session... [--code-only]` → PENDING backlog items tagged `kind:"project"`, `project`, `origin`; registers in `data/sources.json`. Dedup on `(project, origin, topic)`; re-run safe.

`/sde` and `ingest-project.mjs` accept the project + build-session transcripts. Items land in a **project-specific backlog section** (NOT auto into curriculum). Backlog UI splits "From CDTM Eng chat" vs per-`Project: <name>` sections; project items are flagged + sorted by target-topic priority — **untouched ("new topic") and low-`strength` ("weak") first** ("suggested first"), the weak/new prioritization he asked for. Per-section approve/dismiss-all. Approving attaches the item to the topic as an example with `example.project`/`example.kind`.

**Projects tab** = per-project view: each sourced project → the topics it enriched (weakest-first) with "Open →" jumping to the topic. `GET /api/sources` computes coverage. When he asks for a "project review"/"backlog review", read `data/inbox.json` + `data/curriculum.json` and recommend project items on untouched/low-strength topics first.

The curriculum is anchored to the Codecademy Full-Stack Engineer career path. Topics carry one of three statuses:

- `[ ]` never touched
- `[~]` introduced (saw it in real code, can't yet explain or write from scratch)
- `[x]` mastered (could explain without notes and write from scratch)

**Why:** Alessandro is a CS student new to coding who learns by building (Lobbly, tundratalents, etc.) but struggles to place what he learns in the broader picture of software engineering. The curriculum file is his external map. Without it, every project feels disconnected and he can't tell what he's covered vs. what's still missing.

**How to apply:**

1. **Trigger words.** When Alessandro says any of these, both teach AND update the curriculum:
   - `/btw`
   - "explain what just happened" / "what did you do" / "what just happened"
   - "teach me" / "/explain" / "break it down" / "wtf was that"
   - Any direct question like "what does X actually do" about something we just wrote

2. **The teaching part** (per [[user_background]]): explain the concept in first-principles, CS-student-friendly terms. Connect it to what he already knows. Don't just narrate the code — explain WHY it works and WHEN you'd use it.

3. **The curriculum update part.** Identify which topic(s) in `fullstack-curriculum.md` this maps to. For each:
   - Read the file
   - Find the matching `[ ]` or `[~]` entry
   - If he is now genuinely able to explain it back, upgrade to `[x]`. Otherwise leave at `[~]` or upgrade from `[ ]` to `[~]`.
   - Add an attribution line under the entry: `*touched/mastered YYYY-MM-DD in <project> — <one-sentence what he saw/did>*` followed by `↳ [recall](path-to-jsonl) · [project](path-to-project-folder)`
   - Update the overall progress bar and the per-phase counters at the top
   - Update the **Recall index** section at the bottom of the file with a new dated entry, OR add to the most recent entry if it's the same day/project

4. **Be honest about status.** Don't inflate `[~]` to `[x]` unless Alessandro can actually explain the concept back. Exposure is not mastery. The whole point of the file is honest calibration.

5. **Find the current session ID** at update time with:
   `ls -t /c/Users/Alessandro/.claude/projects/C--Users-Alessandro/*.jsonl | head -1`
   That is the recall link for the current session.

6. **Don't update on every code change.** Only update when Alessandro explicitly invokes the trigger words above, or when finishing a project session and he asks for a wrap-up. The file is precious; don't spam it.

7. **The file lives in OneDrive** per [[reference_onedrive_path]] so it syncs across devices and he can read it on mobile or another machine.

Related: [[user_background]] (CS student, weave first-principles), [[reference_onedrive_path]] (which OneDrive folder).
