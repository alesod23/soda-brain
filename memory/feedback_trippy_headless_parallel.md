---
name: feedback_trippy_headless_parallel
description: "Trippy/travel-search Pass-1 sweeps must run headless + parallel, never headed + sequential; per-site headless vs offscreen mode"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d32292e-8942-4e7f-9ad7-ae4d372f0de1
---

Trippy (and any multi-route browser sweep) MUST run **headless + parallel**, never headed + sequential. Caught 2026-06-04: I ran a US->Italy sweep headed and one-route-at-a-time; user flagged it twice ("you are not running headless and in parallel", "its still not headless").

**Why:** headed + sequential is slow AND pops Chrome windows on the user's desktop (intrusive). The engine already supported the right way; I under-used it.

**How to apply (all verified 2026-06-04 on real ORD/NYC -> Italy routes):**
- **Parallel:** `search.py` takes `--profile-dir` per worker; `write_report` stamps pid+ms so concurrent workers don't collide. One `profile-chrome/` can't be opened by parallel Chrome (profile lock), so first run `seed_worker_profiles(n)` in `lib.py` — clones `profile-chrome/` (minus cache, ~13MB each, <1s/4) into `profile-w1..wN`, each carrying the primed Cloudflare/Akamai clearance cookie. A FRESH profile gets bot-challenged -> 0 results. Then launch N background processes, each its own `--profile-dir`, each a slice of dates/origins.
- **Headless is per-site:** momondo (Akamai) -> `--headless` (Chrome new-headless, invisible, 38 results with seeded cookie). skiplagged (Cloudflare "Just a moment") -> blocks ALL headless even with clearance cookie. **User confirmed 2026-06-04: running skiplagged NON-HEADLESS is accepted — it's the only way, stop trying to force headless.** Default `--offscreen` (headed, window at -32000,-32000, off the visible desktop; 22 results) to stay non-intrusive in a fan-out; plain on-screen headed is also acceptable.
- **Mechanism in `lib.launch_profile`:** `--headless` injects `--headless=new` (not Playwright's detectable old `--headless`); `--offscreen` adds `--window-position=-32000,-32000`; `--profile-dir` workers launch with system Chrome (vanilla Chromium is flagged harder by Cloudflare).
- **Only Pass-2 checkout (user pays) stays headed + on-screen.**
- **skiplagged offscreen Chrome CRASHES after ~2-3 routes in one process** (window dies, `page.goto` then hangs forever; observed 3× 2026-06-05). Don't batch many routes through one skiplagged process — run ONE search.py process per (origin,date) doing <=2 routes (`--to "MXP,TRN"`), looped, fresh browser each call. momondo doesn't have this issue.

Full standing rule lives in the trippy SKILL.md Browser section. See [[feedback_browser_chrome_default]], [[feedback_agent_long_running]].
