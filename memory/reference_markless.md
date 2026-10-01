---
name: reference_markless
description: markless v0.9.29 (Rust TUI markdown viewer + in-place editor) installed from GitHub release binaries on the laptop (~/.local/bin/markless.exe) and the box (~/.local/bin/markless); no cargo/rustup on either machine.
metadata: 
  node_type: memory
  type: reference
  originSessionId: da99606c-b308-443c-a768-d5a8aa2c0833
  modified: 2026-09-03T18:17:18.053Z
---

# markless (terminal markdown viewer + editor)

Repo: https://github.com/jvanderberg/markless (MIT, Rust). Installed 2026-09-03 so skill `.md` files can be read/edited in the terminal instead of VS Code.

## Install (release binaries, NOT cargo)

Rust is not installed on either machine and `cargo install markless` would need rustup + a 1.95 toolchain. The releases ship prebuilt binaries (`markless-x86_64-pc-windows-msvc.zip`, `markless-x86_64-unknown-linux-gnu.tar.gz`, plus macOS/aarch64), so those are used.

- **Laptop:** `gh release download v0.9.29 --repo jvanderberg/markless --pattern markless-x86_64-pc-windows-msvc.zip`, unzip, copy `markless.exe` to `C:\Users\Alessandro\.local\bin\markless.exe` (that dir was already on the user PATH). Verified: `powershell -NoProfile -Command "markless --version"` prints `markless 0.9.29`.
- **Box (da@box):** curl the linux-gnu tarball from the release, `install -m 755 markless ~/.local/bin/markless`. `~/.profile` already added `~/.local/bin` for login shells; a PATH line was added at the TOP of `~/.bashrc` (before the interactive guard) so `ssh box 'markless --version'` also works. Verified `markless 0.9.29`.
- **Upgrade:** repeat with the new tag; there is no self-update.

## Usage

`markless <file.md>` views a file; `markless <dir>` (or bare `markless`) browses a directory. It is ALWAYS a full-screen TUI: no print/cat/non-interactive mode exists (`--help` lists only `--watch`, `--no-toc`, `--no-images`, `--image-mode`, `--theme`, `--wrap-width`, `--editor`, `--save`, `--clear` ...). On start it queries the terminal (`OSC 11`, Kitty graphics probe) and waits for the reply, so it hangs on a dumb pipe; run it in Windows Terminal / a real tty.

Images: inline via Kitty, Sixel, iTerm2, or a half-block fallback, auto-detected (`--image-mode` to force). Editing is built in (`e`), or `--editor hx|vim` delegates to an external editor; edits are saved to the same file in place, with conflict detection if the file changed on disk.

## 3 most useful keys

1. `e` enter edit mode, `Ctrl-s` save, `Esc` back to view (`Ctrl-e` toggles).
2. `t` toggle the TOC sidebar (`Tab` to jump into it, `Enter` to go to a heading); `/` search.
3. `q` (or `Ctrl-q`) quit. `?` / `F1` shows the full keymap.

Row added to `task-land/_system/SHORTCUTS.md` under "Shell (PowerShell profile)".
