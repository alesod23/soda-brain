---
name: reference-box-utc-timestamps-mktime-trap
description: "Il box gira in CEST e tutto il sistema scrive timestamp in Z: parsarli con time.mktime li sposta di due ore e gonfia ogni eta' calcolata; usare calendar.timegm o fromisoformat con timezone.utc"
metadata:
  type: reference
---

**Il 2026-09-30 questo ha prodotto tre falsi allarmi sul suo telefono durante una call con un
cliente.** `box_linkedin_watch.py` calcolava da quanto LinkedIn fosse giu' cosi':

    time.mktime(time.strptime(ds.replace("Z", "")[:19], "%Y-%m-%dT%H:%M:%S"))

`strptime` torna una struct **naive** e `mktime` la legge come **ora locale**. Il box e' in
Europe/Rome, quindi ogni timestamp UTC finiva due ore nel futuro e ogni eta' usciva **gonfiata
di 120 minuti**. LinkedIn era giu' da due minuti, il controllo leggeva 122, la soglia era 60:
scattava per qualunque intoppo di mezzo minuto. Non era una soglia tarata male, era aritmetica
sbagliata.

**Corretto con:**

    calendar.timegm(time.strptime(v.replace("Z", "")[:19], "%Y-%m-%dT%H:%M:%S"))

`timegm` legge la struct come UTC, che e' cio' che la Z dichiara. In alternativa
`datetime.fromisoformat(v.replace("Z", "+00:00"))`, che e' la forma usata ovunque sul laptop
(verificato il 30/09: agente, meeting loop, inbound asks, feedback worker e coda usano tutti
fromisoformat, e i due `fromtimestamp` passano `timezone.utc`).

**Perche' ricapitera':** praticamente ogni file di stato di questo sistema scrive in Z —
`heartbeat.json`, `decisions.jsonl`, `rule-hits.jsonl`, le attivita' del CRM, i campi
`created_at` / `resolved_at` della hub — mentre il box vive in CEST. Qualunque confronto
ad occhio fra "adesso" e uno di quei campi ha questa trappola dentro.

**Come accorgersene senza aspettare il danno:** se un'eta' calcolata e' esattamente 120 minuti
(o 60 d'inverno) piu' grande del vero, e' questo. Un allarme che scatta *sempre*, subito, per
qualsiasi cosa, non e' una soglia da alzare: e' un timestamp letto male.

Vedi [[reference_approval_hub]] per la guardia "non fare la seconda voce" nata dallo stesso
incidente, e [[feedback_never_touch_synced_repo_on_box_by_hand]] per dove va modificato il file.
