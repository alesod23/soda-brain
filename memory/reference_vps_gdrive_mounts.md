---
name: reference_vps_gdrive_mounts
description: "What Google Drives the DA VPS mounts, that laptop Downloads/Screenshots now route into CDTM Drive, and that HEC OneDrive on the box is a confirmed dead end."
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-08-29T22:53:32.622Z
---

**DA VPS (da-box, 169.58.128.217) Google Drive mounts** (rclone systemd, `Restart=always`, in `_system/vps/units.list`; config `/home/da/.config/rclone/rclone.conf`, all on OUR OAuth client from `triage/credentials.json`):
- `/home/da/gdrive` = **CDTM My Drive** (alessandro.sodano@cdtm.com), his MAIN drive, same as laptop `G:\`. Token reused from `triage/tokens/drive-cdtm.json` (full drive scope + refresh) — no consent click needed; just rebuild the rclone token json from a google-auth token file and verify the account via the Drive API first.
- `/home/da/tundra-drive` = **Tundra Shared Drive** (team_drive id `0AAJYNQzboqQeUk9PVA`), alessandro@tundrahealth.ai.
- Laptop drive letters: `G:` = CDTM, `H:` = tundrahealth (sparse). Mounts are da-only (no allow_other) so root `ls` = Permission denied, expected.

**Laptop Downloads + Screenshots now route into CDTM Drive (2026-08-29):** `SHSetKnownFolderPath` redirected Downloads → `G:\My Drive\Downloads` and Screenshots → `G:\My Drive\Screenshots` (screenshots previously landed in HEC OneDrive, box-invisible). So files saved on the laptop are readable on the box at `/home/da/gdrive/Downloads` etc. within ~10-20s. This is the standing way to make a laptop file reachable by a box/phone session with the laptop off. Revert = SHSetKnownFolderPath back to `C:\Users\Alessandro\Downloads`.

**THREE screenshot sinks all unified to `G:\My Drive\Screenshots` (2026-08-30) — keep them in sync if ever moved:** (1) Windows Screenshots known folder (SHSetKnownFolderPath), (2) the Ctrl+Alt+V AHK `OneDrive - HEC Paris\Documents\AutoHotkey\copy newest screenshot (ctrl alt v).ahk` (copies newest *.png from that folder to clipboard as CF_HDROP for pasting into the CLI — edit the `folder :=` line AND reload the running AHK process, a file edit alone won't hot-reload), (3) tg-bridge phone-photo bot `~/.claude/tg-bridge/bot.js` `SCREENSHOT_DIR` const (restart via stop.ps1/start.ps1; start.ps1 spawns a keep-awake watcher that holds the shell open — expect the call to "hang", verify via bot.pid instead). All three landing in the CDTM Drive means phone screenshots + OS screenshots are also auto-visible on the box at `/home/da/gdrive/Screenshots`. See [[reference_ahk_autostart]], [[reference_tg_bridge]].

**HEC OneDrive on the box = DEAD END, do not re-attempt.** alessandro.sodano@hec.edu is a locked-down Azure AD tenant: rclone/Graph/any OAuth app hits "admin approval required"; browser-automation login from the datacenter IP fights MFA + Conditional Access + anti-bot (unreliable). Only unlock is HEC IT admin approval. For a one-off HEC file to reach the box, drop it into a mounted Google Drive. Same tenant lock is why [[hec-outlook-cli]] uses Outlook COM (needs laptop on). See [[reference_gdrive_public_share]], [[project_phone_to_desktop]].
