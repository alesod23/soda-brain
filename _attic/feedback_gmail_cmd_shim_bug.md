---
name: gmail.cmd shim mangles multi-line --body (use python.exe direct or --body-file)
description: cmd.exe %* expansion truncates multi-line --body args to first line. Caused real broken emails to TUM profs on 2026-05-10. Fix: python.exe direct OR --body-file flag.
type: feedback
originSessionId: 4ea78cff-05f2-45ae-964c-63e0bf48d72c
---
# What broke (2026-05-10)

I sent 3 emails to real TUM contacts (Anne Tryba, Holger Patzelt, Fritz Tacke — the Fritz one being a first-contact intro on Anne Tryba's recommendation). All three arrived with **only the first line** of the body ("Dear Prof. ...") and nothing else.

# Root cause

`gmail.cmd` is a Windows batch shim:
```
@echo off
"C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe" "%~dp0gmail.py" %*
```

When PowerShell calls `gmail.cmd ... --body $multiLineString`, PowerShell forwards the string with embedded newlines as a single arg to the .cmd file. cmd.exe's `%*` expansion then **truncates at the first newline** when forwarding to python.exe. Python receives `--body "Dear Prof. Tryba,"` and silently sends only that.

This is a known, documented limitation of cmd.exe argument expansion with newlines. There is no quoting trick that fixes it from the PowerShell side.

# Two safe paths going forward

## A. Use `python.exe` directly (bypass the .cmd shim entirely)

```powershell
$body = @'
Multi-line
body here
'@
& "C:\Users\Alessandro\AppData\Local\Programs\Python\Python312\python.exe" `
  "C:\Users\Alessandro\triage\gmail.py" send `
  --account cdtm --to addr@x.com --subject "..." --body $body --thread-id ... --confirmed
```

PowerShell→python.exe passes args directly with newlines intact. No cmd.exe in the chain. **Verified working 2026-05-10** with the Anne body and the Fritz body (longest multi-paragraph), both arriving in full.

## B. Use `--body-file <path>` (works through any shell, including the .cmd shim)

```powershell
$body = @'
Multi-line
body here
'@
$tmp = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllText($tmp, $body, [System.Text.UTF8Encoding]::new($false))
gmail.cmd send --account cdtm --to addr@x.com --subject "..." --body-file $tmp --thread-id ... --confirmed
Remove-Item $tmp
```

`gmail.py` was patched 2026-05-10 to accept `--body-file <path>` on both `send` and `draft` subcommands. File path is a single short arg (no newlines), so it survives `%*` expansion. The .cmd shim is fine for everything else.

# Default for the triage skill

Triage SKILL.md should default to **path A (python.exe direct)** for any multi-line body — fewer steps, no temp file cleanup. Path B is the fallback for callers that want to keep using the shim or for very long bodies pulled from a file anyway.

For single-line bodies (e.g. quick `wa <X> "ok"` style sends), `--body "single line"` via the shim is still fine — the bug only fires when newlines are in the value.

# Wa-sender check

`wa-sender/send.js` is invoked as `node send.js ...` directly (no .cmd shim). PowerShell→node passes args correctly. So WA sends are immune. Only Gmail's gmail.cmd was affected.
