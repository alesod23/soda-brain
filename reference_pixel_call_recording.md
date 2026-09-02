---
name: reference-pixel-call-recording
description: "How Alessandro records calls: Google Phone recorder on the Pixel, OBS 'Call Recorder' dual-track profile on the laptop. NOT MacroDroid, which physically cannot capture call audio."
metadata: 
  node_type: memory
  type: reference
  originSessionId: b75b1302-8e9b-4e42-b796-f57031e2eebf
  modified: 2026-09-01T11:49:42.735Z
---

Verified 2026-07-23. Alessandro wanted to record calls he takes on his Pixel **with AirPods** (both sides).

**MacroDroid / any third-party app CANNOT do this.** Android blocks apps from the call audio stream since Android 10 (tightened in 14/15); MacroDroid's "Record Microphone" only hears the device mic, and with AirPods the audio routes through the earbuds so the phone mic captures ~nothing. No MacroDroid recipe records both sides. Do NOT suggest one.

**The only method that works with AirPods: the native Google Phone (Dialer) app's built-in Call Recording** — it taps the call stream at OS level, upstream of the Bluetooth route, so it captures both sides cleanly on AirPods. Enable: Phone app → ☰ menu → **Call Assist → Call Recording** → toggle on. Rolled out to Italy & Germany Feb 2026 (Pixel 6+/Android 14+). Unavoidable catch: it plays an audible "this call is being recorded" to both parties (legal). Fallback if the region lacks it: speakerphone + a voice recorder (loses the AirPods benefit, mediocre quality).

**Re-confirmed 2026-09-01** from a screenshot of his MacroDroid macro "Record phone calls": triggers Call Active / Call Ended, action **Record Microphone (Until Cancelled) carrying a warning triangle** — MacroDroid's own text: "This feature requires the file path to be reconfigured due to new file access restrictions in Android 10+." Two stacked failures: (1) scoped storage means the action errors before writing; (2) even fixed, "Record Microphone" is the mic, never the call. The Vibrate / Popup / blinking-icon actions fire regardless, which is why it *looks* like it works. Its files would be at `Internal storage/MacroDroid/Recordings`; check MacroDroid → ☰ → System Log to see the action erroring.

**LAPTOP LANE (built 2026-09-01) — the general answer to "record mic + media audio even on headphones".**
Windows WASAPI loopback taps audio at the render endpoint, *after* the app mixes it and *before* it reaches the headphones, so Bluetooth changes nothing. Phone-side that is impossible; laptop-side it is a hotkey. **So: book any call worth keeping as a video call and take it on the laptop.**
- OBS 32.2.1 (already installed, was unconfigured). New **profile + scene collection both named `Call Recorder`**; the pre-existing `Untitled` profile is deliberately untouched.
- `%APPDATA%\obs-studio\basic\profiles\Call Recorder\basic.ini` — Advanced output, `RecTracks=7`, MKV, 320x180 @ 5fps (video cost ~nil), out to `C:\Users\Alessandro\Recordings\Calls`.
- `%APPDATA%\obs-studio\basic\scenes\Call_Recorder.json` — mic source "Me (mic)" `mixers:5` (tracks 1+3), "Them (desktop audio)" `mixers:6` (tracks 2+3). Track 1 = him, track 2 = them, track 3 = mix. **Separate tracks beat diarization** — transcribe 1 and 2 separately for perfect attribution.
- `~\.claude\scripts\Split-CallRecording.ps1` — no args = newest .mkv; ffmpeg-splits to `_me/_them/_mix.m4a` and prints the `transcribe.py` command. Tested end-to-end on a synthetic 3-track MKV.
- Left for him: open OBS, switch Profile + Scene Collection, bind a Start/Stop Recording hotkey, and **pin the mic device** (both sources are on `default`, so a non-default mic silently records the wrong input).
- ffmpeg 8.1.2 is installed but there is **no WASAPI loopback via dshow and no Stereo Mix** on this machine, so ffmpeg alone cannot capture system audio here. OBS is required for the desktop-audio side.

Guide artifact: https://claude.ai/code/artifact/e5850f3a-673b-42c3-999b-b2ccb91b038a

Related: [[reference_approval_hub]] (the other MacroDroid work), [[reference_voice_lane]], [[reference_audio_to_notes]], [[reference_phone_to_desktop]].
