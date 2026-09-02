---
name: Always fetch YouTube transcripts when needed
description: When a YouTube URL appears and the question requires its content, fetch the transcript via the local helper instead of WebFetch (which only returns YouTube's HTML boilerplate)
type: feedback
originSessionId: 9dcc63dd-d1fa-4cb5-95be-fe42b5adf524
---
When a YouTube URL appears in conversation and the user's question depends on the video's content (comparison, fact-check, "what does this video say"), do NOT rely on WebFetch — YouTube's HTML doesn't include the transcript and you'll get only navigation/footer noise.

**Why:** This was confirmed in practice. WebFetch returned only YouTube boilerplate when the user asked me to compare a video's WhatsApp-MCP approach to my Baileys setup. User had to correct me ("you're not using the right approach").

**How to apply:**
```powershell
node C:\Users\Alessandro\.claude\scripts\yt-transcript\fetch.js <url-or-video-id>
```
Accepts either full URL (`https://www.youtube.com/watch?v=ID`, `https://youtu.be/ID`, `/shorts/ID`) or the bare 11-character video ID. Prints joined transcript text to stdout, exits 1 on error, exits 2 if captions are disabled.

If captions are disabled (exit 2), tell the user honestly that this video has no captions and ask them to summarize, rather than fabricate.

Project: `C:\Users\Alessandro\.claude\scripts\yt-transcript\` (uses `youtube-transcript` npm package).
