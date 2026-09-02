---
name: ""
metadata: 
  node_type: memory
  originSessionId: 5bf3e4d7-faea-4ab8-a723-c9f3ef764fcf
---

When the user says "OneDrive", they mean:

```
C:\Users\Alessandro\OneDrive - HEC Paris\
```

NOT `C:\Users\Alessandro\OneDrive\` — that one is an empty Windows-default placeholder folder with only `desktop.ini`, never synced.

The HEC Paris OneDrive is the actively-synced workspace. All "save to OneDrive" requests (cooked trip HTMLs, shared docs, etc.) go there. This is also where `$OneDrive` env-var points (`$env:OneDrive` resolves to the HEC Paris path).

**How to apply:** any script writing to a "OneDrive" folder should default to `C:\Users\Alessandro\OneDrive - HEC Paris\`. The cooked-trips HTML goes to `C:\Users\Alessandro\OneDrive - HEC Paris\cooked trips\`.

Related: [[reference_travel_search]] — the trippy `render_html.py` uses this path.
