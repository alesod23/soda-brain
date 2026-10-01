# Handoff (box -> laptop): CDTM community mail must not reach Telegram (his rule, 2026-09-18 13:35)

His words (Telegram, replying to the 12:23 CATCH-UP card with Josephine Sieveking's "[CDTM Jobs] ... Hypersonica" mail):
> I don't want to see any of these CDTM community emails here on Telegram. It's not relevant for me. ... unless it's for an event that I could attend and we were invited to, I don't want to see it. Only the event ones are interesting to me.

Where the leak is: the card was a `🚨📬 CATCH-UP` from the LAPTOP `recap.ps1` (SODANOtif-Recap). The box's live poller (`/home/da/sodanotif/pollers/gmail_poll.py`) already dropped that mail (List-Unsubscribe + Precedence: list) and now also carries an explicit rule (`CDTM_GROUP_RE` / `CDTM_EVENT_RE`, `cdtm-group:not-an-event`).

TO DO on the laptop (`~/.claude/sodanotif/recap.ps1`, `Process-GmailThreads` unread feed): drop any thread whose To/Cc/List headers point at a cdtm.com Google Group (jobs@, community@, all@, alumni@, `X-BeenThere: *@cdtm.com`, `Mailing-list: list *@cdtm.com`, `List-Unsubscribe` with groups.google.com/a/cdtm.com) UNLESS subject or preview matches an event pattern (invit|einlad|event|workshop|talk|meetup|dinner|party|conference|summit|save the date|rsvp|kickoff|hackathon|demo day|founders night|networking|panel|fireside|session). Mirror the regexes from the box poller so both lanes agree. Then scp the poller? No: pollers are box-only; recap.ps1 is laptop-only. Log the change in this file and in the memory `feedback_no_cdtm_community_mail_on_telegram`.
