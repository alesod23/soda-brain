---
name: feedback_outreach_ask_first_peer_voice
description: "Alessandro's outreach voice: the ASK goes FIRST (not last), reciprocity over supplication, 'student founder' never translated, plain words over nominalised abstractions. Gold examples live in the skill's examples.md."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67360653-a4fa-4a49-9fe9-75fbdcbb9319
  modified: 2026-09-02T14:56:48.077Z
---

Set 2026-09-02 after he rejected a 60-message LinkedIn batch I had written from the old
`linkedin-outreach` skill (Caleb's, German-first, built for interviewing research subjects).

**Why the batch failed:** the skill put the ask LAST, banned naming the product, mandated a blank
line after the greeting and 3-4 separate sentences, and prescribed "I have already spoken with a few
people" as social proof. Every one of those is wrong for founder-to-founder outreach.

## The rules he stated

1. **The ask goes FIRST**, right after a one-line identity, before any reasoning.
   *"deve essere un formato che devi capire che io preferisco prima la richiesta."*
   `Ciao X, / sono uno student founder a TUM, costruiamo <what>. Avresti 15 minuti per una chiamata? <why this person>.`
2. **One paragraph, no blank line after the greeting** on LinkedIn. It is a DM, not an email.
3. **"student founder" is never translated.** *"non traduce bene."* Same for `fellow founder`,
   `healthcare`, `learnings` when writing to founders: *"stiamo parlando con dei founders, quindi la
   gente giovane può capire."*
4. **Reciprocity, not supplication.** Always pair the ask to learn with what he gives back:
   `"vorrei imparare da te come vendere meglio a ospedali (e condividere la mia esperienza con un
   fellow founder italiano!)"`. His preferred CTA phrasing, in his words *"una bella call to action
   per questi possibili mentori"*.
5. **Plain words, never nominalised abstractions.** He killed "Sei arrivato al front office
   sanitario dalla finanza e dal marketing" with *"Nessuno parla così."* Use "un background
   non-healthcare" or "un profilo tradizionale business school".
6. **Warm referral goes before identity** when a mutual exists, as in his sent Giuseppe Pecere
   message: "Ho da poco parlato con Isabella di Vento, che mi ha consigliato di scriverti."
7. University naming: shortest recognisable form. See [[feedback_cold_email_operator_ask_for_advice]].

## Where this lives

`~/.claude/skills/linkedin-outreach/` — now ONE skill covering all three outreach jobs
(peer/mentor, hospital sales, research interview) because he asked for exactly that, 80/20, no
over-engineering. `SKILL.md` = rules, **`examples.md` = verbatim gold and the learning loop**.

**How to apply: every time he rewrites or approves a message, append it to `examples.md` verbatim in
the same turn.** Do not rewrite the rules off one example; let the pattern accumulate. That file
outranks SKILL.md when they disagree.

**Known gap worth fixing:** the sent-corpus harvester
([[reference_message_builder_corpus]], ~6,500 messages, daily, healthy) still does NOT harvest
LinkedIn, a phase-2 TODO from 2026-07-21. His best outreach examples only exist on LinkedIn, which
is precisely why rule-only drafting produced stiff prose. Fixing that harvester is the single
highest-value upgrade.
