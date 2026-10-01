---
name: feedback-design-files-live-in-the-repo-not-in-his-export
description: "A deck that has gone out in an email is finished work and must be in the tundra-design GitHub repo; go and read it there, never ask him to export a zip"
metadata:
  type: feedback
---

2026-10-01, his words after I asked him to export a .zip from Claude Design:

> "tu sappia che quello e' il sistema che io voglio. Cioe' anche se non e' davvero cosi', cerca di
> essere proattivo e capisci che questo e' il sistema che io mi aspetto. Mi aspetto di essere in
> grado di poter estrarre questo file perche' c'e' stato, mal che vada, c'e' stato l'aggiornamento
> alla GitHub repo con tutti i file necessari del giorno prima. [...] quando creiamo uno per
> Emanuele, nel momento in cui mandiamo quell'email, e' stato ufficialmente creato. E' stato
> ufficialmente lavorato e quindi quel file deve essere poi messo su GitHub."

**The rule.** The design repo (`alesod23/tundra-design`, mirror of his Claude Design projects under
`live/<person>/<key>/`) is the place a deck is read from. Two things follow:

1. **Never ask him to export a zip.** Go and look in the repo. At worst it carries yesterday's
   state, which is almost always enough. Asking him to produce the input is pushing work back at
   him for a pipeline that exists.
2. **A deck leaving in an email IS the event that marks it finished.** Not "when he remembers to
   sync": the send is the signal. A designed artefact that has been put in front of a customer must
   end up in the repo, and that snapshot should be triggered by the send.

**Why it matters, concretely.** On 2026-10-01 I told him the Humanitas deck source was
unreachable and asked him to export it. That was wrong twice over: the deck is in the mirror as
`Humanitas pitch.dc.html`, and the claim I repeated ("Claude Design cannot be read by any tool")
came from a SKILL.md written on 30 August, a month before the mirror was built. **A capability
statement in a doc has a date; check whether it is still true before repeating it to him.**

**What was actually missing**, found the same evening: the BOX has no credential for that repo.
Five deploy keys exist here (vault_kb, medtech-brain, claude-memory, coattio, travel-search) and
none for tundra-design, and `gh` is not logged in. A sixth read-only deploy key was generated and
the `github-tundradesign` SSH host added; he installs the public key.

**Division of labour, because the mirror cannot move.** The snapshot is taken by the Design Mirror
Chrome extension in HIS Chrome, so only the laptop can refresh the repo. The box can see the send
(it reads the mail) but cannot snapshot. So: box detects the event, laptop takes the snapshot.

See [[reference_design_sync]] for the machinery and its gotchas, and
[[feedback_standing_instruction_becomes_work_now]]: he said "that is the system I want", which is
an instruction to build it, not a preference to note.
