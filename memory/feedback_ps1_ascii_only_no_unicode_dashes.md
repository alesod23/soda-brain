---
name: ps1-ascii-only-no-unicode-dashes
description: "Editing BOM-less .ps1 files (sodanotif scripts etc.) with a literal em-dash or other non-ASCII punctuation can silently corrupt the string and break the script — always use plain ASCII (hyphen, not em-dash) in these files."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 833c9bca-1d56-4c13-a3c5-19bf926ee404
---

`~/.claude/sodanotif/*.ps1` (and likely other BOM-less `.ps1` files in this environment) are read by Windows PowerShell 5.1 as ANSI when there's no BOM — the files' own header comments already document this ("this .ps1 stays pure ASCII... PS 5.1 reads a BOM-less .ps1 as ANSI and would mojibake literal bullets/middots/em-dashes").

**Incident (2026-07-06):** despite that documented warning being right there in the file, I inserted a literal em-dash (`—`, U+2014) into a long double-quoted classifier-prompt string in both `recap.ps1` and `watch.ps1` while adding the sender-email fix. It silently corrupted the string (one instance became a literal U+FFFD replacement char) and broke PowerShell's parser, cascading into unrelated-looking errors dozens of lines later ("Unexpected token 'unread'", "'<' operator is reserved for future use", etc.) that had NOTHING to do with the actual bad character — the real fault was 100+ lines earlier at the mojibake'd em-dash. Caught only because I ran a parser syntax-check (`[System.Management.Automation.Language.Parser]::ParseFile`) before trusting the edit.

**How to apply:** when editing ANY `.ps1` file (check for a BOM first if unsure — `head -c 3 file.ps1 | xxd`, no BOM = ANSI-read risk), NEVER type a literal em-dash/en-dash/smart-quote/curly-quote — use plain ASCII (` - ` or `--`, straight quotes) instead, exactly like the surrounding code already does. After any non-trivial `.ps1` edit, run a parser-only syntax check before considering the edit done:
```powershell
$errs = $null; $tokens = $null
[System.Management.Automation.Language.Parser]::ParseFile('<path>', [ref]$tokens, [ref]$errs)
if ($errs) { $errs | ForEach-Object { "$($_.Extent.StartLineNumber):$($_.Extent.StartColumnNumber) $($_.Message)" } } else { "OK" }
```
A syntax error reported far from the actual edit is a strong sign the real defect is an earlier mojibake'd character, not the reported line.
