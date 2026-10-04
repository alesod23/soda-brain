# DESIGN 2026-10-04: THE SYSTEM AGENT, the maintainer of the whole SODA SYSTEM

Written 4 Oct 2026, 16:57 to 17:30 Rome. A design, not a build: the week's usage is spent elsewhere and the build is
sized in section 6 for him to schedule. Inputs read: `memory/reference_system_agent.md`, `gtm-eng/agent/gtm_agent.py`
(1,105 lines) and `config.json`, `gtm_agent.py status` and `incidents` at 16:49 and 16:52, `system/SODA-SYSTEM-MAP.html`
(94 nodes) and `.md`, `system/LOOPS.md`, `system/MACHINES.md`, `system/FINDINGS-20261001.md`,
`task-land/_system/job_runner.py`, `jobs.py`, `HUB-CARD-CONTRACT.md` (H1 to H42), `_system/window-watch/`,
`sim/harness/budget.py`; a read-only look at the box at 16:56 (ports, the contacts, digest and reconcile logs);
`Get-ScheduledTask` on the laptop at 16:55; 6 web sources and one Edge `find_skill` call (section 5).

His decisions this design implements (4 Oct 16:50, verbatim where it matters):

- "This is supposed to be a maintainer for the whole SODA SYSTEM. The parts that are in the SODA SYSTEM map resulted
  as down or not working, those are the ones that you will need to pick up ... not as in they're waiting for me to
  implement them, but 'broken' ... all the ones that are about maintenance get fixed."
- Fix session: a LOCAL Opus session (not cloud), 30 to 45 min wall ("more than that, I know that you're not working the
  way you should"), 1% of the week per fix, extendable to 2%, no monthly bookkeeping.
- Stuck protocol approved in full (section 4).
- What counts as broken: option b, everything the map tags down / broken / off / armed / paused / failed with an age,
  each line with an owner (agent / fix session / him) and an age; things waiting for HIS decision are not broken.
- Name: "the System Agent". A separate GTM agent keeps the campaigns ("just focusing on the campaigns and making sure
  that runs smoothly"); the two collaborate.

---

## 1. Purpose and the split

**Purpose.** The System Agent keeps every node of the SODA SYSTEM map working. Every 10 minutes it runs cheap checks
over the laptop, the box and the map; what is broken lands as one line in a registry with an owner and an age; what a
whitelisted fix can repair it repairs at once; what needs reading and editing code goes to ONE capped local Opus fix
session (a `fix` job of the existing job runner) that must prove the repair by making the failing check pass; what
only he can unblock reaches him as ONE "STUCK on X" card whose yes performs the unblocking action for him. It never
sends to a person, never logs in, never deletes data, and never treats a thing waiting for his decision as broken.

**The split.**

| | the System Agent | the GTM agent |
|---|---|---|
| job | maintainer of everything on the map | the campaigns go out, every business day |
| cadence | every 10 min (task `DA-SystemAgent`, through `run-hidden.vbs`) | every 10 min (task `GTM-Agent`, as today) |
| code | `task-land/_system/system-agent/system_agent.py` (synced, so the box half reads the same registry) | `gtm-eng/agent/gtm_agent.py`, trimmed |
| owns | the registry `broken.jsonl`, fix sessions, STUCK cards, the box watch, the combined report | campaign checks, its campaign fixes, the campaign section of the report |

What moves out of `gtm_agent.py` (function by function, by line today):

| function | goes to | why |
|---|---|---|
| `check_campaigns` (137), daily board and fire, push-by-noon | stays GTM | campaigns |
| `check_followups` (242), `check_contacts` (261) | stays GTM | people and steps; mostly HIS decisions, never "broken" |
| `check_audit` (369): booked-and-never-sent, auto-reply named a person | stays GTM | campaign outcomes |
| `check_audit`: own cards stale or twice, the same card open twice, drafts closed by a closed tab, the meeting loop not reading Notion | System | system hygiene |
| `check_feedback` (285), `system-feedback.jsonl` | System | his sentences about the system |
| `check_hub` (329) | System, report only | hub health is system; cards waiting for him are his decision, listed, never "broken" |
| `check_ports` (492), `check_tasks` (507), `check_gmail` (546), `check_linkedin` (630) incl. `li_probe` / `li_restore`, `check_sync` (699), `check_windows` (714) | System | infrastructure |
| fixes `start_task`, `start_servers`, `li_repair`, `hide_task`, `close_own_cards` | System | infrastructure |
| fix `release_channel` | stays GTM, gated on the System Agent's verdict that the channel's tool works | a campaign action, a system precondition |
| `investigate` (842) | System, replaced by the fix session for anything code-shaped | |
| `process`, `hub_post`, `flush_outbox`, `hub_close`, `calm`, `F`, `runs.jsonl` writing | a shared `agentlib.py` imported by both | one incident engine, not two copies (DRY) |
| `heartbeat` and `task-land/_system/gtm-agent/box_watch.py` | System | the box watches the laptop for the whole system, not for GTM |

**Collaboration protocol.**

1. GTM to System: a GTM check that fails for a non-campaign cause (Gmail does not answer, the LinkedIn tool is down,
   the CRM port refuses, a scheduled task crashed) appends ONE line to `_system/system-agent/inbox.jsonl`
   `{at, from:"gtm-agent", key, text, evidence}` and posts no card of its own. The System Agent ingests it at its next
   tick as an incident in the registry (dedup by key with its own checks).
2. System to GTM: the System Agent writes `_system/system-agent/blockers.json` (`{key, text, since, owner, eta}` per
   open item that touches a campaign channel). The GTM agent reads it and reports "held: LinkedIn is not answering, the
   System Agent is on it since 15:41" instead of a second alert. `release_channel` runs only when the blocker is gone.
3. One card per incident in the whole system (H5, H7): the card belongs to whoever owns the registry line.
4. **Report: recommend ONE combined report**, 09:00 and 18:15 as today, posted by the System Agent: head line
   "GTM: pushing today YES/NO" (the GTM agent's own section, verbatim from `gtm_agent.py section --json`, so campaign
   health reaches him only through the GTM agent), then "SYSTEM: N broken, a for the agent, b in a fix session, c need
   you", then AUDIT, then "since the last update". One card is one thing to read on the phone; two cards at the same
   minute double the pings for one picture. `calm()` still runs on it (the alert-word rule of `hub_outdated.py`).

---

## 2. The known-broken registry

**Shape.** One JSON line per broken item, newest state wins by `id`, in `task-land/_system/system-agent/broken.jsonl`
(append-only, `merge=union` like every jsonl in task-land):

```
{"id": "...", "node": "<map node id or check key>", "what": "...", "since": "<iso>", "class": "maintenance|his_command|his_decision",
 "owner": "agent|fix_session|him", "attempts": n, "last_action": "...", "next": "...", "status": "open|fixing|stuck|fixed|gone", "evidence": "<path>"}
```

**Map sync, the same-turn rule.** The map keeps a `broken` field on each node in `NODES` (today the map only has
`status:"broken"` plus a free `note`). `system_agent.py map-sync` writes, for every open line, `broken:"<since> ·
<owner> · <next>"` onto the node and sets `status`, and clears both when the line closes; it moves "Last verified" in
the HTML and the `.md`. It runs in the same tick that changes a line, and is idempotent (same registry, same file).

**Classification.** Only `maintenance` is the agent's to-do. `his_command` = the fix is known and ready, and only his
hand or his sign-in can run it (a login, a remote write the auto-mode classifier refuses, a permission change): these
become STUCK cards with a one-click action. `his_decision` = waiting for him to choose: never "broken", never a card
from the System Agent, listed in the report under "waiting for you" only when the owning surface has no card of its
own.

**TODAY's inventory (4 Oct 16:49 to 16:57; live checks + map + box read + `Get-ScheduledTask`).**

Maintenance (owner agent or fix session), 12:

| # | node | what | since | owner | attempts / last action | next |
|---|---|---|---|---|---|---|
| M1 | `linkedin:poll` (map `w_lipoll`) | the LinkedIn inbox poller completed no poll for 68 min | 4 Oct ~15:41 | agent | 1: `start_task` held 16:49; task ran 16:53 with 0 | confirm a completed poll at the next tick; `li_repair` if not; a fix session on the 3rd time today (it also went down at 07:09) |
| M2 | `w_winwatch` (check `task:DA-WindowWatch:exit`) | the tick ended `0xc000012d` (STATUS_COMMITMENT_LIMIT: the page file was full at 16:47); the watcher itself, pid 12936, alive since 30 Sep | 4 Oct 16:47 | fix session | 0 | find what held the commit charge at 16:47 (memory pressure, 16 GB laptop seen as 11.7); a tick that fails on a full page file must not look like a crash of the watcher |
| M3 | `task:DA-FeedbackWorker` | `0x800710e0` three times today (03:09, 04:19, 07:19), each gone by itself | 4 Oct 03:09 | agent (watch) | 0 | a flapping counter: a 4th in 24 h = a fix session |
| M4 | `b_eod` | the 23:00 digest: "digest sent by Bot API: http 400", "posted card None", every night (log has 1, 2, 3 Oct; FINDINGS: since 28 Sep) | 28 Sep | fix session | 0 | read the body Telegram rejects (FINDINGS: markup), fix, prove with a dry post of the same body |
| M5 | `b_eod` pre-sweep | the 22:47 watchdog fired on 1, 2, 3 Oct: the savior's 22:12 pre-sweep does not run | 28 Sep | fix session | 0 | re-arm the session cron in the savior (memory `feedback_presweep_deep_check_before_23`) |
| M6 | `b_pages` | research-page :4143, :4144, :4145 do not listen any more (the map says "unsupervised"; at 16:56 nothing is on those ports) | before 4 Oct 16:56 | fix session | 0 | one `da-research-page@<port>` unit with `Restart=always` (FINDINGS box 6); if the events are past, this line becomes `his_decision` (keep or retire) |
| M7 | `b_trippy` | the supervisor spawns a second node every 5 min that dies on EADDRINUSE (5 MB of log noise) | before 1 Oct | fix session | 0 | supervise by port, not `pgrep` (FINDINGS box 1) |
| M8 | audit: cards #11 and #13 | "Il savior e' stopped su una richiesta di permesso e aspetta te" is open twice | 4 Oct | agent | 0 | close the younger as a duplicate (extend `close_own_cards` to identical cards of any producer, H5); the cause is H2 below |
| M9 | box `systemd --failed` | `cloud-init` and `systemd-networkd-wait-online` failed while `health-vps.json` says 0 faults | before 1 Oct | fix session | 0 | count failed units in `health-vps.sh` (FINDINGS box 16) |
| M10 | laptop one-offs | `Scheduled-Email-Test-20260531-1230` (last `0xc000013a`, 24 Jul) and `WA-Test-Send-1350` (last `0x1`, 18 Jun) still Ready | Jun/Jul | agent | 0 | disable (never delete: the never-list), note in MACHINES.md |
| M11 | map drift | `LOOPS.md` lines 255 and 355 still say `due_today.py` is not scheduled (task DA-DueToday runs 08:30) | 4 Oct 04:10 | agent | 0 | map-sync edits the two lines |
| M12 | map stale notes | see "stale notes" below: three nodes say broken or in conflict and are not | 4 Oct | agent | 0 | map-sync |

His command (the fix is known; his hand or sign-in runs it), 5:

| # | node | what | since | the one action |
|---|---|---|---|---|
| H1 | box Gmail `sodano23` | `draft-reconcile.log`: "AUTH REQUIRED for account 'sodano23' (token present but unusable)" | 26 Sep | sign in: Google consent with `login_hint` for that account (stuck action a) |
| H2 | the savior | stopped on a permission prompt, waiting for him (cards #11, #13) | 4 Oct | answer the prompt in the savior's tmux (stuck action b: a terminal with `ssh box -t tmux attach -t <savior>` pre-typed) |
| H3 | `b_coattio` clone | `start-box.sh` modified in the pull-only box clone (`git status`: ` M start-box.sh`), the next laptop commit to it breaks the sync | 1 Oct | the laptop half is the fix session's (copy the guard into the laptop file, commit, push); the box half `git checkout start-box.sh` is his (memory: never touch a synced repo on the box by hand) |
| H4 | iteration log on the box | THE PLAN item 12: three `ssh box python3 - --restart < patch-...` lines "still to run" | 4 Oct 16:40 | run the three lines (stuck action b, pre-typed in order) |
| H5 | box secrets modes | `slack/tokens/*.json`, `sodanotif/push.env`, `tg-reply-resolver/user.session` are 0644 (FINDINGS box 14) | before 1 Oct | `chmod 600` (a permission change: never-list) |

His decision (NOT broken; the report lists them, no System Agent card), 14:

| node | state | waiting for |
|---|---|---|
| `rd_instinct`, `b_rulesinbox`, `c_instinct` | paused 4 Oct 01:50 | his word "forget about instinct for now" |
| `rd_research` | paused to 7 Oct | `research-pause.json`, his budget call |
| `rd_feedback` | armed, inert | the P3 cut-over: `touch ~/hub-review/no-telegram` when the peer says "commits processed" (THE PLAN item 4) |
| `ln_cleaning` | off | after the Tuesday 6 Oct reset; Langfuse keys on the box are an env file (his) |
| `ln_sim` | off | the next night he orders |
| `w_ab` | armed, one shot 9 Oct 10:00 | the date; nothing to do |
| `pipeline.py pickup --auto` | paused to 6 Oct 20:20 | `AUTO_PAUSED_UNTIL`, his trial cards |
| monitor layer | migration 001 merged, not applied | THE PLAN, LONG TERM (c) |
| `b_coattio` | status broken | S11, one writer: a build he ordered, not a breakage (the merge part is done) |
| box `gtm-board-server` :4141, box `gtm-eng` copy | dead since 19 Sep | FINDINGS box 8: "Decide" (delete or unit) |
| hub-review images (H21), skills install on the box (S4) | missing features | builds |
| CRM Today: 23 due, 2 replies owed, 13 outdated steps | his steps | the CRM surface (GTM agent / reader), not the System Agent |
| hub: 4 cards waiting too long (oldest 376 h) | his cards | his verdicts |
| contacts: 2 found and waiting for his yes, 1 with nothing found | his yes; a search | GTM agent |

GTM agent's (campaign outcomes, from the AUDIT block): booked and never sent (fde-health 1 LinkedIn invite 1 Oct;
daily-2026-09-29 2 emails 2 Oct; us-campaign-emails 4 emails 2 Oct); automatic replies naming Susanne Holz and Stacy
Bolton, nobody wrote to them.

**Counts:** 12 maintenance (5 agent, 7 fix session), 5 his command, 14 his decision, 3 GTM agent lines.

**Stale map notes found (map-sync fixes them on its first run):**

- `st_crm`: "The box copy is a pull replica and is in conflict tonight (647 vs 645 people, card #10)": merged per
  record 4 Oct 04:07 (THE PLAN item 1), cards #10 closed.
- `b_coattio`: status `broken`, note "Plan items 1 and 2": item 1 is done; item 2 is a planned build. Its real broken
  part is the dirty clone (H3).
- `b_contacts`: "Failing since 21 Sep (token)" and the same line in the "Known broken" card and `LOOPS.md` 356: the box
  log at 16:30 reads "alesoda2002: 7 new/changed -> contacts-inbox.jsonl; cards posted 1"; the token was re-minted
  (last `invalid_grant` at log line 10554 of 10963). Live, not broken.
- `b_pages`: "Unsupervised; a reboot kills them": it happened, they are down (M6).
- "Known broken": the map drift line about MACHINES is fixed (MACHINES has DA-Supervisor and DA-DueToday); the
  LOOPS half is not (M11).

**Seed for `broken.jsonl`** (the first content, written by the build's first step, not by this design):

```
{"id":"M1","node":"w_lipoll","what":"LinkedIn inbox poller no completed poll for 68 min","since":"2026-10-04T13:41:00Z","class":"maintenance","owner":"agent","attempts":1,"last_action":"start_task held 16:49","next":"confirm a poll; li_repair; fix session on 3rd outage today","status":"open"}
{"id":"M2","node":"w_winwatch","what":"tick exit 0xc000012d (commit limit)","since":"2026-10-04T14:47:42Z","class":"maintenance","owner":"fix_session","attempts":0,"last_action":"","next":"find the commit-charge holder at 16:47","status":"open"}
{"id":"M4","node":"b_eod","what":"23:00 digest Telegram http 400, card None","since":"2026-09-28T21:00:00Z","class":"maintenance","owner":"fix_session","attempts":0,"last_action":"","next":"fix the rejected body, prove with a dry post","status":"open"}
{"id":"H1","node":"box:gmail:sodano23","what":"token unusable, AUTH REQUIRED","since":"2026-09-26T00:00:00Z","class":"his_command","owner":"him","attempts":0,"last_action":"","next":"sign-in with login_hint","status":"stuck"}
```
(the remaining lines follow the tables above, same fields)

---

## 3. The three stages

**Stage 1, check (every 10 min, no model).** Everything `gtm_agent.py` checks today for infrastructure, plus one probe
per map node that has a port, a task, a cron or a log (`runbooks.json`: `{node: {probe, healthy_when, known_fixes,
escalate}}`); box probes go through one read-only ssh call per tick (`ss -ltn`, `systemctl --failed`, the tail of the
named logs), the same shape as the read at 16:56 today. Each check has a stable key and can run alone:
`system_agent.py check --only <key>`. That single entry point is what makes "reproduce" and "prove" possible.

**Stage 2, whitelist fix (as today).** `start_task`, `start_servers`, `li_repair`, `hide_task`, `close_own_cards`,
each capped per incident (`fix_caps`), 25 min between tries, written to `incidents.jsonl`. New whitelist entries
only with a test, and only for reversible actions (a restart, a disable, closing its own or a duplicate card).

**Stage 3, the fix session (a `fix` job of the job runner).**

When: a `maintenance` line whose owner is `fix_session`, or a whitelist fix that did not hold after
`escalate_after_runs`, or a flapping counter over its limit. One attempt per incident per day; one fix session at a
time (the runner's mutex `_system/jobs/runner.lock`); not started when the 5-hour window is at or over 80
(`budget.py FIVE_PAUSE`) or the kill switch `_system/system-agent/OFF` exists.

How: `jobs.py add --type fix --incident <id>` (new field `type: work|fix`; `fix` jobs skip the artifact-kind
expectations and are linked to the registry line, not to a hub card). `job_runner.py` gets a per-type profile:

| | work job (today) | fix job |
|---|---|---|
| wall | 90 min | 30 min soft (the session is told), 45 min hard (killed) |
| budget | none | 1.0 week point, read from `budget.py` before start (W0) and every 2 min; at W0 + 1.0 the runner stops it unless it is extended once to W0 + 2.0 (below) |
| tools | Agent, Read, Edit, Write, Bash(python, git, curl, node...) | the same minus `Agent` fan-out beyond 2 specialists, plus a PreToolUse guard for the never-list |
| done | an artifact linked | the check passes twice (below) |

The brief it gets (built by `system_agent.py brief <id>`): the registry line; the check's key and its exact command;
the evidence (log tails, the incident timeline from `incidents.jsonl`); the runbook entry; the files that own the node
(from the map's `code:` field); what was already tried (whitelist fixes and any earlier fix session's JSON); the
never-list; the protocol: (1) reproduce: run `check --only <key>` and see it fail, record the output; (2) diagnose,
write the one-paragraph cause in `progress.json` (`phase: reproduced|diagnosed|fixing|verifying`); (3) back up and
commit before any edit (`.bak-<date>`, one commit per step, his rule); (4) fix the root cause, smallest change;
(5) re-run the check, it must pass; (6) update `system/` in the same turn if a service, port, job or rule changed;
(7) last line ONE JSON: `{"status":"fixed_pending|stuck|failed", "cause":"...", "changed":["file: what"],
"proof":"the passing check output", "rollback":"how to undo", "for_him": null | {"kind":"auth|terminal|run",
"what":"one sentence", "account":"...", "url":"...", "command":"...", "why_only_him":"..."}}`.

**The proof before "fixed".** The session's own passing run is the first pass. The System Agent's next independent
tick (10 min later, a different process) is the second. Only then does the line close as `fixed` with
`how: "fix session <job id>"`. A session that says `fixed_pending` and the next tick still fails = the attempt counts
as failed, the change is reverted by its `rollback` if the check is worse than before, and the line moves to stuck.

**The extension to 2%.** Automatic, once, only when `progress.json` says `phase: fixing` or `verifying` at the 1-point
mark (it reproduced and has a diagnosis): the runner logs the extension and the reason. Without a reproduction at the
1-point mark the session is stopped: a session that cannot reproduce in one point is not working the way it should.

**The never-list (in the brief, and enforced by the guard hook, not by trust):** never log in or open a sign-in; never
send anything to a person (no `gmail.py send`, no WA, no LinkedIn send, no Slack post); never delete data (`rm`,
`Remove-Item`, `git clean`, `git checkout .`, `git reset --hard`, `schtasks /delete`, `DROP`/`DELETE` on Postgres;
it may disable, rename to `.bak` and stop); never change an env file (`.env*`, `~/.env/*`) or a permission (`chmod`,
`icacls`, the Claude allowlist, `settings.json`); never touch a synced repo on the box by hand (a box repo changes
only through a laptop commit and the box's own sync); never open a window (CREATE_NO_WINDOW, `run-hidden.vbs`); never
kill a process it did not start, except the one the runbook names (his rule: kill without asking is forbidden).
Anything on the list it needs = `status: stuck` with `for_him`.

---

## 4. The stuck protocol

**When.** A fix session returns `stuck` (or `failed` twice on two days), or the registry line is `his_command` from
the start (H1 to H5 today).

**The card** (HUB contract: kind `update` is wrong here because his yes acts, so kind `decision`; H5 one card, H7 one
escalation, H9 first line is the decision, H10 full, H31 what YES and NO do, H35 real context):

```
🟣 Ping hub
❓ #N · STUCK on <node>: <what is broken, one line>
I did: A (<when>), B, C. Logs: <incidents.jsonl line>, <jobs/<id>/run-1.json>
I need you to do exactly this: <the one action>
YES = I open it for you now: <the sign-in page for alesoda2002 | a terminal with `<command>` typed, you press Enter | I run `<command>` myself>
NO = it stays broken; this line stays in the System list with its age, no second card.
```

It is not a question with options. It never asks him to diagnose. It closes by itself when the check passes (as the
GTM agent's cards do today).

**"I need you to do exactly this" is derived, not written by hand:** it is the `for_him` object of the fix session's
last JSON (`kind`, `what`, `account`, `url`, `command`, `why_only_him`), validated by `system_agent.py` (one action,
a known account, a command with no secrets in it, a `kind` from the three). For `his_command` lines that never had a
session (H1 to H5), the object comes from the runbook entry. A `for_him` that fails validation becomes a fix-session
retry the next day, never a vague card.

**The three unstuck actions on his yes** (executed by `unstuck.py` on the LAPTOP, in his interactive session, picked up
within a minute by task `DA-Unstuck` every 1 min through `run-hidden.vbs`, which reads the hub for closed-with-yes cards
whose `meta.action.type` is `unstuck`):

- (a) **auth**: the consent URL with the account forced in (`login_hint=<email>` on Google OAuth URLs,
  `AccountChooser?Email=<email>&continue=<url>` on other Google URLs; for a tool that opens its own browser, its
  no-browser flag and the captured URL), opened with `Start-Process` in Chrome: his standing rule in CLAUDE.md (trigger
  it directly, pre-select the account, never a bare chooser). After it, `unstuck.py` re-runs the check and the card says
  the outcome on its next tick.
- (b) **terminal**: `wt.exe new-tab --title "SODA unstuck #N" powershell -NoExit -Command <prelude>` where the prelude
  prints the card's one line and pre-types the command at the prompt without running it
  (`Register-EngineEvent PowerShell.OnIdle -MaxTriggerCount 1 -Action { [Microsoft.PowerShell.PSConsoleReadLine]::Insert('<command>') }`;
  to be proven in the build's drill, fallback: the command on the clipboard and printed). This is the approved per-card
  exception to the no-console-window rule, and the recorder must see it as his: before launching, `unstuck.py` appends
  `{at, card, pid_expected_parent, command_hash, by:"his yes on #N"}` to `_system/window-watch/expected.jsonl`;
  `window_watch.verdict()` gets one more branch: a window whose owner chain contains an `unstuck.py` pid listed there
  within 120 s = verdict `his-yes` (not a culprit, not counted by `check_windows`). Nothing else may write that file.
  `window_lint.py` is unchanged: `DA-Unstuck` itself runs hidden.
- (c) **run**: when his yes is enough authority (the action is inside the never-list only because it needs his word,
  for example disabling a task or `chmod 600` on the box through the laptop's ssh, NOT a sign-in), `unstuck.py` runs
  the command itself with CREATE_NO_WINDOW, logs the output into the registry line, re-runs the check, and the card
  closes when it passes. Which kind applies is decided by the session's `for_him.kind`, checked against the runbook:
  a sign-in is always (a), an interactive prompt is always (b).

**Wording he decides (draft):** "Exception, approved 4 Oct 2026: a console window may open in front of him only as the
direct result of his YES on a STUCK card, titled 'SODA unstuck #N', recorded by window-watch as `his-yes`. Nothing
scheduled ever opens one."

---

## 5. Best practices copied, with sources

1. **The orchestrator owns "done", and done means verified end to end.** Anthropic's long-running harness keeps a
   feature list with `passes:false` and lets a session mark a feature passing only after it tested it end to end; the
   failure mode it names is "declaring complete prematurely". Copied as: a fix closes only when the check passes twice,
   the second time in the System Agent's own independent tick; the registry is the feature list.
   https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
2. **Reproduce first, then repair, then validate with the reproduction.** Agentless (localize, repair, validate)
   generates a reproduction test that must show the original error and uses it to select the patch. Copied as: the
   session's first act is `check --only <key>` failing; the same command passing is the proof.
   https://github.com/OpenAutoCoder/Agentless/blob/main/README_swebench.md
3. **A hard session cap, not a soft hope.** GitHub's Copilot cloud agent has a 59-minute hard limit per session and a
   stuck session times out; it works on a draft PR a human reviews. Copied as: 30 min soft, 45 min hard kill, and every
   change is a commit with a `.bak` and a rollback line.
   https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/troubleshooting-copilot-coding-agent
4. **Iteration and spend ceilings plus a stuck detector.** OpenHands' controller carries `max_iterations` and a
   per-task budget and a stuck detector that kills pathological loops early. Copied as: the 1-point budget read from
   `budget.py`, extended once only when progress shows a reproduction, and the "no reproduction at 1 point = stop" rule.
   https://github.com/OpenHands/OpenHands/issues/17691
5. **Pre-approved remediation for known classes, a human for the rest, confirm restoration.** PagerDuty's SRE agent
   runs only approved automations, escalates when a human is needed, and confirms the service is restored. Copied as:
   the whitelist (stage 2) stays the only thing that acts without a session or him, and every action ends with the
   check re-run. https://www.pagerduty.com/platform/ai-agents/sre/
6. **Every page is actionable, with a playbook.** Google SRE: every paging alert must carry an action a human is
   expected to take that the system cannot take itself; playbooks cut MTTR about 3x. Copied as: the STUCK card names
   exactly one action and performs it on his yes; `runbooks.json` per node.
   https://sre.google/workbook/on-call/

**Edge.** One `find_skill` call ("autonomous maintenance agent ... self-healing ops agent runbook") returned three:
`itallstartedwithaidea/agent-skills@self-healing-agents` (generic retry, mutate, fallback-model patterns in
TypeScript for one agent's own errors: not a base, it has no notion of services, proof or a human action),
`anthropics/knowledge-work-plugins@runbook` (vendor-authored runbook template: steps with expected result and "if it
fails", verification, rollback, escalation), `sickn33/agentic-awesome-skills@autonomous-agents` (general guidance).
Verdict: none is a base for the System Agent. The runbook skill is worth adopting as the FORMAT of `runbooks.json`
entries (probe, expected result, if it fails, rollback, escalation). Its test (memory: adopt only after a test): write
the runbook for M4 (the digest 400) with the skill and without it, give each to a fix session on the same fault in a
dry run, adopt if the skill's version reaches a reproduction faster or with fewer wrong turns.

---

## 6. The build plan

Reused: `job_runner.py` (mutex, wall, `needs_him` path become the fix profile), `jobs.py` (a `type` field),
`gtm_agent.py` (its checks move, its engine becomes `agentlib.py`), the hub (`POST /pending`, `/close`, the existing
action executor pattern), `window_watch.py` and `run-hidden.vbs`, `budget.py` (`read()` and the week and 5-hour
figures), `box_watch.py`, `close_own_cards`.

Order (each step one commit and a `.bak`, tests first):

| step | files | tests | week points | wall |
|---|---|---|---|---|
| 1 shared engine | `task-land/_system/system-agent/agentlib.py`; `gtm_agent.py` imports it | replay the last 7 days of `runs.jsonl` through both: the union of findings equals today's agent's | 0.8 | 50 min |
| 2 System Agent checks + split | `system_agent.py` (check, status, incidents, `check --only`, section), `runbooks.json`, `inbox.jsonl`, `blockers.json`; task `DA-SystemAgent`; GTM agent trimmed; `window_lint.py` clean | `test_split.py`, `test_inbox_dedup.py`, one live tick of each side by side for an hour | 1.5 | 90 min |
| 3 registry + map sync | `broken.jsonl` seeded with section 2; `map-sync` (NODES `broken` field, Last verified) | `test_registry.py` (idempotent, closes clear the node) | 0.8 | 45 min |
| 4 fix jobs | `jobs.py --type fix`; `job_runner.py` profiles (45 min, budget watch, extension rule), the guard hook `fix_guard.py` (never-list) | a stub `claude` (fake JSON): fixed without proof stays open; proof + next tick closes; wall kill; budget kill with a stub reader; the guard blocks each never-list pattern | 1.5 | 90 min |
| 5 stuck protocol | the card builder, `unstuck.py`, task `DA-Unstuck`, `expected.jsonl` + the `his-yes` branch in `window_watch.py` | card shape against H5/H9/H10/H31; a drill card on a harmless command: the window opens pre-typed, recorded `his-yes`, `check_windows` stays ok; auth URL carries `login_hint` | 1.0 | 60 min |
| 6 combined report + first real run | report merge; M2 or M4 as the first real fix session | the report dry run; one real fix session end to end | 0.6 + the session (1 to 2) | 30 min + 45 |

**Estimate: about 6 to 7 week points and 6 to 7 hours wall for the build, plus 1 to 2 points per real fix after it.**
Known weak points: the usage endpoint reports whole percent (`week 30.0`), so "1 point" is read in steps of one and a
session may spend between 0.5 and 1.5 before it is seen; the runner also logs the session's own usage from
`claude -p --output-format json` to calibrate, and the 45-minute wall is the backstop. The pre-typed terminal trick is
unproven on this machine (the drill decides, the clipboard is the fallback). The box checks depend on ssh from a
sleeping laptop; the box half (`box_watch.py`) keeps watching when the lid is closed.

**What he decides:**

1. One combined report (recommended) or two.
2. The terminal exception wording (section 4).
3. A daily ceiling on fix sessions (proposed: at most 3 a day, so at most 3 to 6 week points, one at a time), or none.
4. M6: keep the research-page servers (a unit) or retire them; and the box `gtm-board-server` / `gtm-eng` copy (keep or
   delete).
