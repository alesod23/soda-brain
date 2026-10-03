# Hub-review, the two commits of 4 Oct 2026 (01:20 and 01:36)

Written by the savior right after executing them. What follows is what is DONE, what is OPEN,
and the three builds his sentences created.

## 1. The thing he must know first

**The two AIIC mails went out at 01:36, not at 11:04 / 11:06.** He wrote "send this message
tomorrow morning at 11:04" (Volonterio) and "send it sunday (tomorrow at 11:06)"
(Franciacorta/Boniotti) as COMMENTS on cards he was marking yes. The hub sends on the yes, and the
comment only reaches the savior afterwards, in the commit summary. Both are in SENT:
`1a0c5eda19cb6c7c` 01:36:37 (his own edited text) and `1a0c5ec74e95d1f7` 01:36:39.

Rule filed: **HUB H31**. The fix, not built: `/resolve` takes `send_at`, hub-review shows a time
field next to the yes, the hub holds the draft until then.

## 2. Rules filed (all compiled into the skills except email, see below)

| # | Ledger | What |
|---|--------|------|
| H97 | email | Recent dates are said the way he says them: "last Friday" under a week, "a couple of weeks ago" around two, "a few weeks" + the date past three. Absolute for anything older and for every FUTURE appointment. Mapped into `absolute-dates`, which it partly reverses. |
| H98 | email | Real accents, always. `e'` `a'` `o'` are not accents. Mapped into `mechanics`, which is now a front rule. |
| H99 | email | Availability in the window the reader can act on (Monday "questa settimana", Thursday on "in questi giorni"), then the calendar link, at the bottom. Mapped into `one-ask`. |
| H19 | proactive | A card proposing an outreach carries the DRAFT. His no then teaches us not to draft that shape. |
| H20 | proactive | Instinct is not a research engine: proactive agent only. |
| H30 | hub | A context line must say what the thing IS without opening the link. |
| H31 | hub | A time in a comment is a schedule (above). |

`compile_skill.py --contract email` hit the 110-line ceiling at 113 lines; fixed by MAPPING the
three new rules into existing ones instead of letting them sit in "New, not yet mapped". Recompiled:
drafting 110 lines, proactive 74, hub 88.

## 3. Done

- **#3 Tobias Doeringer:** his question was "do we actually have a deck sent?". YES: `Generic Hospital
  PoC Proposal.pdf`, 1,543,567 bytes, sent 5 Sep 08:53 with the blurb, same thread. The draft said
  "in my email below" while the quoted message below is TOBIAS's, so it now says "The deck I sent you
  on 5 September". Also: `register.py` refused with "already answered" because our own 5 Sep reply is
  newer than the parent; fixed by giving the sidecar a `source: ... (2026-10-03)` so `source_event_ms`
  moves the cutoff. Card #3 live.
- **#19 Foch (Carte-Jacquesson):** date made relative; **the pitch deck is now actually attached**
  (`Tundra Pitch Deck_EN.pdf`, 2,807,080 bytes, verified on the draft). It promised two attachments and
  carried none, the same failure as the Galbiati mail. The pilot proposal is deliberately NOT attached:
  its cover still reads "For Klinikum XXX". The mail now says the proposal will come adapted to Foch,
  which is also what its own ask asks for.
- **#8 Franciacorta, #10 Volonterio:** accents, calendar paragraph, "questa settimana"; Volonterio built
  from HIS page rewrite, not mine. Both sent (see section 1).
- **#53 Notion:** his 1 Oct "Personal Finances" voice note was sitting in the COMPANY Meetings database
  (Internal / Client Call / Ecosystem, Organization relation, Caleb in the workspace) with his balance and
  runway in it. Moved under his private page "Personal runway", renamed "Personal Finances - 1 Oct 2026".
- **#2 Google token:** `phone_auth.py` only knew gmail and calendar, so the contacts token could not be
  renewed at all. Added `--kind contacts` (backup `phone_auth.py.bak-20261004-contacts`), built the URL
  with `login_hint=alesoda2002@gmail.com`, sent it to him. Waiting for the redirect URL.
- **#5 Caravaggi:** phone `+393346997272` (from `senderPn` on his WhatsApp thread `255550738690268@lid`)
  and email `s.caravaggi@assing.it` (he gave it himself, 26 Sep) written to the CRM row
  `c-assing/sebastiano-caravaggi-assing`.
- **#3/#4 Bifulco and Severi:** the drafts HE asked for already existed in their threads and had never been
  registered, so they had no card and he could never see them. That is the actual bug behind "you
  should've made a draft". Both reworded (relative date) and registered: cards **#8** and **#9**.
- **#14 Nevio PoC:** parked to 2026-11-03 with his reason on the task.
- **#2 Sophie Tollmann:** verified, "Reach out to Pietro (CDTM)" is already line 18 of
  `healthcare-ecosystem-push`. He was right, nothing to add.
- **#10 Merone:** follow-up draft placed in his WhatsApp self-chat, as asked.
- **hub `/revise` now accepts `context`** (backup `server.js.bak-20261004-revisectx`, syntax checked).
  It is NOT live: restarting `da-hub` needs root.

## 4. My own mistake in this pass

`POST /intake` created **duplicate CRM rows** for Bifulco and Severi: the instinct yes had already
created `bifulco-unina` and `severi-unibo` from `propose_row`, and "Paolo Bifulco" did not match
"Bifulco" by name. The originals are the live ones (they carry the step), and I put the emails on
THEM. The two orphans `paolo-bifulco-universita-di-napoli-federico-ii` and
`stefano-severi-universita-di-bologna` need merging or deleting in the UI; there is no delete API.
Lesson: read the CRM for the row BEFORE calling /intake, because a yes on an instinct card has
already created it.

## 5. The three builds his sentences created

### A. The deck pipeline (his words, card #19)
"all the decks that we might build automatically ... with the new GitHub way of pulling a bunch of
existing decks and also modifying them with cloud design ... if I tell you that I would like to give
them the exact same deck that we prepared for Humanitas, but instead, you also have it as in French."

The shape he described, in order:
1. a first pass that checks the whole document reads as a French business reader expects;
2. the translation;
3. **a terminology review agent** that checks every technical, clinical, hospital, maintenance and
   tech term against how that sector says it in French, **looping until all terms are checked**;
4. then attach it to the mail, and give him a clickable Drive link
   (`Sales & Marketing/ALE/Customer proposals`) so he can open it in a tab and review quickly.

What exists already: the deck sources are HTML in `tundra-design/live/ale/tundra-pitch-deck/`
(`Humanitas pitch.dc.html` is the source he means), the decks are bilingual in one file via
`<span lang="..">` + a toggle, and there are already three French artefacts
(`Besancon one-pager*.dc.html`) as prior art. Missing: the third language in the toggle, the review
loop, and the Drive upload + link step.

### B. The OEM deck for Sebastiano Caravaggi / Assing (card #20)
Start from the Humanitas pitch, change the problem and solution slides, keep team and theme slides,
quote his own margin-improvement figures from the Notion meeting notes, all in Italian. Reuse the
slide from one of Caleb's old pitches with the device at the centre and six-to-eight capabilities
around it. Same slide count as now, no more. Use cases: keep #3 (reporting) and the chatbot at #1,
make #2 a preventive/predictive maintenance algorithm citing a well-known standard, then a big
emphasis on the business case. Two judging agents: one reading as an OEM ("is this valuable for me?"),
one checking it does not still read as a hospital offering adapted sideways.

### C. Timed sends (section 1).

## 6. Still owed

- Drafts for Sandrine Roussel (Besancon), Vittoria Di Marco Berardino (Santi Paolo e Carlo),
  Erica Donarini (ASST Lodi). Rows exist, stage inbox, no email on any of them. For Roussel he
  dictated the content: not going to the AFIB office, ask whether there is interest and whether we
  could show a demo to her and someone else from the department for feedback.
- Martina Andellini: a draft already exists in her thread; it needs a card like Bifulco and Severi got.
- Jeffrey Smoot on the CRM Call page: `pipeline.py call` refuses because the task is archived
  (merged into `us-trip-prep`). Needs either a fresh task or a row by hand.
- Caravaggi's LinkedIn (`linkedin.com/in/sebastiano-caravaggi-b6826466`): `/enrich-result` only
  accepts email and phone. Extending it is a LAPTOP change, `coattio` is pull-only on the box.
- `da-hub` restart so `/revise` can carry a context.
