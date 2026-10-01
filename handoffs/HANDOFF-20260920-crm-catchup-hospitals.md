# HANDOFF 2026-09-20 · CRM check board: hospital items + "s asks why"

From: the CRM session on the laptop (coattio). To: the savior, who owns `research-page/crm-catchup.html`
and executes his `crm-catchup commit ...` Telegram messages.

His two rulings today, both given to the CRM session in chat:

1. *"integra nella crm check board questo check per ospedale"* after: *"Tu mi dici quali ospedali pensi
   che io stia bersagliando e io controllo se te ne manca qualcuno. Poi capiamo come mai. [...] un
   ospedale su cui sai che ho fatto ricerca, ma ti manca l'email; magari fai un'altra ricerca, lo
   scopri che c'e un email/contatto."*
2. *"quando schiaccio S, poi mi esce una textbox che io posso skippare schiacciando Enter, oppure
   aggiungo del testo e poi schiaccio Enter"* so the reason *"ti possa andare in memoria"*.

## What changed on the box

- `research-page/build_crm_catchup.py` patched (backup: `build_crm_catchup.py.bak-20260920-pre-hosp`,
  page backup `crm-catchup.html.bak-20260920-pre-hosp`). Your `crm_catchup_data.py` is untouched.
- New input: `research-page/data/hospitals.json`, built on the laptop (sources: coattio crm.json,
  gtm-eng boards, task-land, his sent mail via gmail.py over 180 days). Rebuild = `python3 build_crm_catchup.py`.
- Page: after your person items, a divider and one item per hospital (same zones: left = what I think he
  is doing there / people in the CRM / evidence; right = gaps / what I would do / a note box / verdict).
  Last item `hosp:missing` asks which hospitals he researched that the list does not show.
- `s` (and the Skip button) opens a one-line box: Enter = plain skip, text + Enter = skip with reason,
  Esc = no verdict. A bug in the old `verdict()` that overwrote the note when a verdict was pressed is fixed.

## What his commit now contains, and what to do with it

    crm-catchup commit 2026-09-20
    <id> (<name>): ok|skip|change [| perche': <reason>] [| <note>]
    hosp:<key> (<hospital>): ok|skip|change [| perche': <reason>] [| <note>]
    hosp:missing (Ne manca qualcuno?): ok|change | <hospital names, one per line flattened>

- `perche': <reason>` on ANY skip line: that is the memory he wants extracted. Put it where the
  lesson belongs (a feedback memory if it is a rule about how he works, a note on the CRM person or
  company if it is about them). Do not drop it.
- `hosp:<key>: ok` = yes he targets it, nothing to do unless a note says otherwise.
- `hosp:<key>: skip` = he does not target it; with a reason, record it (company note in the CRM via the
  CRM session, or memory if it is a pattern like "never rehab clinics").
- `hosp:<key>: change | <note>` = something in my picture is wrong or missing (a person he already
  talked to, an attempt from a channel I do not read). The note is the lead: search his mail/chats,
  and if an address or a person turns up, it goes through the rake path (`contact_rake.py` /
  `POST :4137/enrich-result`), never straight into crm.json.
- `hosp:missing: change | <names>` = hospitals he researched that I never saw. For each name: search
  sent mail, drafts, WhatsApp store, task-land; report in the 23:00 card what was found (contact, email,
  attempt) and propose the CRM row. This is the gap-finder he described.

## Gap semantics in hospitals.json

`no_people` (org known, zero CRM people) · `no_email` (people, none with an address) · `no_attempt` (no
sent mail to the org domain and no outreach-looking CRM activity) · `stale_90d` · `no_next_step`.
Urgency 1 = no_people or no_attempt, 2 = any other gap, 3 = clean. Items are sorted by urgency, then country, then name.

The CRM session keeps the laptop-side builder of hospitals.json; ask it (a task in task-land or a hub card)
when the file needs a refresh after a batch of CRM changes.

## Laptop-side builder (added after the first run)

The inventory pipeline is committed in the coattio repo, folder hospital-check/ (README there). Box copy arrives with the usual pull. First run: 321 orgs seen, 83 decision items, 5 country lists (165), 73 cold names counted only.

## Update, same evening: a asks too

On both boards a and s open the comment box (Enter = verdict, text + Enter = verdict with comment, Esc = nothing). On the CRM board an ok with a comment prints as `<id>: ok | <text>`: treat it as his instruction for that item (e.g. the email goes to his drafts first). On GTM boards the comment is `note` in the commit file, printed by run-commit.py as NOTE.
