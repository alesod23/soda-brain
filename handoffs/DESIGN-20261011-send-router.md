# DESIGN 11 Oct 2026: one send router, both machines

His ruling (TG voice, 11 Oct 06:26 Rome, top priority): "We need to refine these workflows so that I don't have to worry from which one I'm telling you or giving you confirmation to send something. They just get sent. Push it."

The trigger: the CMIA replies to Jeffrey Smoot and Nahshon Stark (hub #6 `abdgnbuca4o`, "both are good. dsend them on linkedin now. go."). The box job runner claimed a LinkedIn job it cannot send, and told him "waiting for the laptop". On the laptop, the auto-mode classifier then refused the send ([Real-World Transactions]). Earlier: Lena's Slack sat unsent a day on hub #142 (box could not send Slack). WhatsApp from the laptop fails today.

## Two causes

1. **Capability per machine** (checked 11 Oct 00:15 EDT):

   | channel | laptop | box | sender |
   |---|---|---|---|
   | LinkedIn DM | yes | no | `~/.medtech-crm/crm-app/crm_li.py --cmd dm` (laptop browser profile) |
   | WhatsApp | **no**: no wa-daemon running, send.js POSTs to 127.0.0.1:4119 and gets nothing | yes: daemon on 127.0.0.1:4119 | `wa-daemon/send.js` |
   | email | yes | yes | `triage/gmail.py` (send a registered draft) |
   | Slack | yes | no | `~/.claude/slack/slack.py` (user tokens on the laptop) |

2. **The classifier** refuses a real send from an interactive Claude session, even after his explicit dsend. Box `~/.claude/settings.json` has no permissions block at all. The laptop allows `wa-daemon/send.js` only, which is useless now that the daemon lives on the box.

## The design

**One entry, the same on both machines:** `_system/send/send.py` (task-land, so both machines run the same code).

```
send.py --channel linkedin|whatsapp|email|slack --to <username|jid|draft-id|channel> --text-file <f>
        --card <hub card id> [--account ...] [--thread ...]
send.py status [--id X]        the outbox: queued / claimed / sent / failed, per row
send.py drain                  the worker: send every row this machine can send (cron / scheduled task)
```

- **Approval in code, not in the caller.** `send.py` refuses unless `--card` names a hub card whose recorded verdict from him is a yes or a dsend (hub-review queue.jsonl / approval-hub state on the box, read over Tailscale :4142). Campaign steps keep their own engine and standing rulings and do not go through here. This check is what makes the scoped allow-rule below safe: the rule lets a session call the router, and the router itself still refuses anything he did not say yes to.
- **One durable outbox, owned by the box** (always on): `~/.local/state/send-outbox.jsonl` on the box, outside every synced repo. Not a task-land file: the git sync can park for days (memory reference_task_land_sync_parked_conflict). Three routes on the box intake-server (:4137, Tailscale): `POST /send/outbox` (enqueue), `POST /send/claim {host, channels}` (lease 10 min), `POST /send/result {id, sent, proof}`.
- **Dedupe.** The key is sha1(channel | recipient | normalised text). A key already `sent` is refused. A `claimed` key whose lease is still live is refused. Before sending, the drain re-reads the thread (LinkedIn readback, WA store, Gmail Sent) and marks the row sent without sending again if the text is already there. That is the check that held for Smoot/Stark on 11 Oct.
- **Run local when it can, else hand off.** A capable machine sends at once and records the row as sent. Otherwise it enqueues; the other machine's drain picks it up within a minute: box cron `* * * * *` under flock, laptop task DA-SendDrain every minute through run-hidden.vbs. Only the laptop polls the box, so no box-to-laptop connection is needed. The drain is a plain process, not a Claude session, so the classifier is never in the path of an approved send.
- **Laptop offline:** the row stays `queued`, with `waiting: laptop` visible in `send.py status` and on the hub's Scheduled tab. No card to him. After 2 h waiting, the system agent's STUCK path (H54/H56) re-checks; he hears only the outcome.
- **The report is the outcome only.** On result, the router edits the hub card it came from with one line per recipient: sent (with time and proof link) or not sent (with the reason and what happens next). Never "queued" or "waiting" as an outcome (his anger, 11 Oct 06:06 Rome).
- **After send:** the send ledger (`outreach/ledger.py sent`) books it; the CRM learns it the usual way (the message store and pollers, H18).
- **job_runner:** a job whose channel is a send no longer runs a Claude orchestration. It becomes a router call (`send.py ... --card`). The open job is closed by the router's result, with the artifact linked through `jobs.link`.

## Who builds what

- **Laptop (this session):** `send.py` (CLI, approval check, local senders, drain), DA-SendDrain task, tests with a dry sender. Also the job_runner change, with `jobs.py`.
- **Box (savior):** the three outbox routes in intake-server.js (in `.medtech-crm`, so they arrive by the cron pull; written on the laptop and reviewed by the savior), the drain cron, and the WA send path.
- **Him:** the permission lines below, on both machines (a session never edits its own permissions).

## Permission lines (for him to add, scoped to the router only)

Laptop `C:\Users\Alessandro\.claude\settings.json`, inside `permissions.allow`:
```
"Bash(python C:/Users/Alessandro/task-land/_system/send/send.py:*)",
"PowerShell(python C:\\Users\\Alessandro\\task-land\\_system\\send\\send.py *)"
```
Box `/home/da/.claude/settings.json`, a new `permissions` block:
```
"permissions": { "allow": [ "Bash(python3 /home/da/task-land/_system/send/send.py:*)" ] }
```
The two `wa-daemon/send.js` lines on the laptop can go: the router replaces them. Whether an allow-rule lifts the auto-mode refusal is verified on the first real send after he adds it, and reported.
