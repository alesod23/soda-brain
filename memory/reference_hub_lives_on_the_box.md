---
name: reference_hub_lives_on_the_box
description: "The live approval hub (4180) runs on the box under systemd; the laptop's approval-hub/server.js is a dead 2026-09-01 copy and laptop 127.0.0.1:4180 is only a TCP forward to the box."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-27T00:21:36.721Z
---

**The live hub is `box:/home/da/approval-hub/server.js`** (760 lines, systemd `da-hub.service`, `User=da`,
`Restart=always`, listens `0.0.0.0:4180`, env `HUB_*` paths in the unit). Its `state.json`, `hub-rules.json`,
`last-rejected.json` are there too. Routes: `GET/POST /pending`, `POST /resolve {id, verdict, device, feedback}`
(a yes runs `executeAction`: gmail-send-draft by draft id only, never edited text), `POST /revise {id, text?,
meta?, action?, ping?}` (in place, same #N, edits the Telegram message; ignores `context`), `POST /close {id,
reason, verdict?, notify?}` (resolves WITHOUT executing, verdict defaults to yes), `GET /item/<id>`,
`GET /unresolved-ids`, `GET /resolved/<id>`. Every resolve/close appends to `task-land/_system/decisions.jsonl`;
the guard in POST /pending appends to `rule-hits.jsonl`. Resolved items are pruned 24 h after resolution; open
cards are never pruned (60 open on 2026-09-27).

**The laptop copy `C:\Users\Alessandro\.claude\approval-hub\server.js` is dead** (mtime 2026-09-01, no
/revise, /close, kind, meta, guard). Laptop `127.0.0.1:4180` is `forward-to-box.js` (task `DA-HubForward`), a
raw TCP pipe to `100.85.52.84:4180`, so laptop producers posting to localhost reach the box hub. Editing the
laptop file changes nothing. hub-review (`/home/da/hub-review/`, :4142 bound to the Tailscale ip, cron-supervised)
reads the SAME `state.json` from local disk on every request (no cache) and writes only through the hub's HTTP
routes; loopback `127.0.0.1:4142` refuses by design.

**How to apply:** any hub change = ssh box, edit under `/home/da/approval-hub/`, `sudo systemctl restart
da-hub` (or ask the savior). Keep a `.bak-<date>` next to the file. See [[reference_approval_hub]],
[[reference_hub_review_ui]].
