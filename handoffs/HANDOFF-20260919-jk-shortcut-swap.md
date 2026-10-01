# Handoff (box -> laptop): swap j/k in the GTM board page (and any other keyboard review page)

His standing rule (Telegram 19 Sept 01:08): "j is back and k is fwd, not other way around" and it applies "everytime we have this text shortcuts (even in gtm boards)".

Done on the box copy `/home/da/gtm-eng/board-page.html`: the keydown handler now maps `k`/ArrowDown to next and `j`/ArrowUp to previous (the first-keystroke guard follows `k`), and the legend reads "j back / k fwd". Also done in `/home/da/hub-review/page.html` (box-only, no laptop copy).

The LAPTOP is the writer of gtm-eng (hourly tar push to the box), so apply the same two edits in `C:\Users\Alessandro\gtm-eng\board-page.html` or the next push reverts the box copy. Memory: `feedback_jk_shortcuts_j_is_back`.

## Second pass (same evening, his ruling 01:17): align the GTM board keys with hub-review

"lets try to be consistent here between the gtm boards and this approval hub shortcuts to move. adopt the approval thing to the crm boards. keep the things that are there and not in the approval thing ofc"

Applied in the box copy `/home/da/gtm-eng/board-page.html`:
- `k` next, `j` previous (first pass).
- `c` = the free-text key everywhere: on the board it focuses the message textarea (hub-review: the change box). `e` kept as a silent alias.
- `y` = copy (was `c`), so `c` is free for the text box.
- `Ctrl/Cmd+Enter` = Commit (new; the handler used to return early on metaKey, so the check sits before that guard).
- Unchanged and kept: `a` ready, `s`/`x` skip, `o` profile, `1-4` channel, `?` hide legend, Esc leaves a field.
- Legend now reads: j back · k fwd · a ready · s skip · c edit/comment · esc done editing · o profile · y copy · 1-4 channel · Ctrl+Enter commit · ? hide.
Apply the same edits in `C:\Users\Alessandro\gtm-eng\board-page.html` (the laptop is the writer; its next tar push overwrites the box copy).
