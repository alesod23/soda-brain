---
name: project_trippy_v2
description: Design of trippy-v2 — a NEW travel-search skill (separate from /trippy) built around deep airport catchment recon + a learned door-to-door comfort/price preference function
metadata: 
  node_type: memory
  type: project
  originSessionId: 47543f5b-c490-4b75-ba65-dd07960b9a91
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

**trippy-v2 = a brand-new skill, separate from the existing `/trippy`.** Do NOT edit the old skill. Validation gate: run v2 on a real trip, then the user compares its output against their own manual momondo search; only trust/promote v2 once it matches or beats the hand search. Design co-developed with the user in the 2026-06-10 session (Munich→Sarzana trip as the test case).

## Pipeline (the v2 spine)
1. **Step 0 — REDESIGNED (2026-06-11): direct-route matrix FIRST, proximity LAST.** The original proximity-ranked catchment failed hard on the Sarzana test: PSA (1h30 last-mile, zero nonstops) got anchor status and produced 0 rule-surviving options from 250; FLR (dismissed as "weak backup" for its 3h last-mile) owns the entire podium; BER (500 km away, reachable by ~€32 advance ICE) wasn't even modeled — but Ryanair PSA↔BER is the route the user himself knew about. Correct algorithm: (a) enumerate airports on BOTH sides incl. far hubs reachable by cheap rail (D-Ticket regional, advance-Sparpreis ICE); (b) build the **direct-route matrix** between the two sets via carrier schedule APIs (Ryanair timtbl/farfnd verified; fares per day available free); (c) score cells = direct-exists × fare-tier × last-mile-feasibility-under-hard-rules × ground-access cost/time; (d) only then spend aggregator searches on surviving cells. Probe verdicts for Sarzana: MUC→FCO easyJet €125 RT exists but 4h last-mile + only-cheap-return-at-07:20 kills it; BLQ €234 + 3h30 last-mile dominated; GOA €295 dominated; FLR anchor confirmed.
2. **Aggregator pull** (momondo/omio), mirroring the user's manual technique: up to **3 origins × 3 dests, ±3 days on each date**; extract **top ~20 by price AND top ~20 by "best"** (momondo's own best-sort, not just cheapest). Per option extract: price, operating airline(s), depart→arrive local times, **#stops + layover airport(s) + layover duration**, total flight duration, which origin/dest airport + date, baggage-included flag.
3. **"Completions" → door-to-door.** Turn each raw row into a D2D pair `(total €, total hours)` = flight + access-to-origin-airport + last-mile-from-dest + bag + €40/night if forced. **Flat assumption: any overnight ≈ €40.** Skip completion on obviously dominated rows (effort-saving).
4. **Deterministic Pareto prune.** Drop any option both pricier AND slower D2D than another (the "I won't even check it" case). Keep only the non-dominated frontier.
5. **Relevance ranking** via the preference function below. ALL options still shown; the function only decides what gets highlighted — never a hard filter that eliminates options.

## The model's 2-FOLD PURPOSE (critical — it is NOT a decision-maker)
The learned preference fn is a **research-effort allocator**, never the chooser of the user's trip. It does two jobs: **(A) Triage what to fully complete** — ~80 raw options (40 cheapest + 40 best, possibly expanded to 80) get cheap ROUGH (€,time) estimates; the model says which deserve the expensive full completion (exact fares + exact last-mile + exact D2D) and which obviously don't, so effort goes only where it could change the final shortlist. **(B) Decide which complicated sub-searches to run** — some completions need a NEW search (e.g. a fast-train last-mile that must be priced on Trenitalia, not a cheap regional estimate); the model flags which of those costly sub-searches are worth launching. Both feed ONE deliverable: narrow ~80 → **the top 20 the user could realistically consider.**

## Presentation
momondo-style dual tiles **per search**: a **Best** (price+comfort balance) and a **Cheapest**. Two-tier searches: **Search 1 = the "obvious"** (nearest airport A → nearest airport B, the 30-second hand search); **Search 2 = the "deep"** (spend a single "complexity budget" on origin OR arrival, never both, + date-flex ±days + €40-night trades).

## The preference function — TWO candidate approaches (user to choose)
- **User's direction (active preference learning):** a *deterministic preference algorithm*, **segmented by trip class** (short EU hop vs long-haul US, parameterized by flight duration AND whole-trip duration), **learned from yes/no questions on REAL found trips** (not hypotheticals). It keeps learning: periodically surface **outliers** outside the current function and **monitor** how the user reasons / whether preferences drift. Not a frozen law — a living guideline that improves which options get surfaced within fixed effort.
- **Claude's alternative (parametric utility):** generalized cost `GC = price_D2D + v·time_D2D`, rank by GC; `v` = value of travel time in €/h (user's gut ≈ €5–10/h), with a **convex** penalty past a comfort threshold and a **hard D2D ceiling**. €/h (not "% saved") because it auto-encodes "depends on trip size" — small trips can't clear the bar with big detours.
- **FIRST PRECEDENT RULES (user, 2026-06-11, trip class "short EU ~≤10d"):** (1) NO transit overnights — airport nights AND forced en-route hotel nights both killed ("I'd rather not"; supersedes the earlier "6am if >€40 cheaper" trade); (2) NO ~8h layovers (8h30 Sofia = the cheap tier's workhorse = dead; ≤3h fine, 4–7h heavy penalty); (3) days ON SITE ≥8 FULL days, strict. Net effect on Sarzana test trip: the entire cheap self-transfer tier died; survivors = Air Dolomiti MUC⇄FLR nonstops + constructible short-layover PSA combos. Lesson: one context sentence from the user killed ~90% of the option space — elicit hard rules EARLY, before ranking effort.
- **DECISION (2026-06-10): synthesis — "start with hypothesis, then empirical."** Seed each trip class with the parametric GC form so trip #1 isn't cold, then the user's yes/no-on-real-trips loop + outlier probes reshape/override it per class. Form + learning procedure are complementary, not rivals.
- **Seed params (rough, to be corrected by the loop):** `v ≈ €8/h` (midpoint of user's €5–10/h gut), linear up to ~6h D2D then convex, soft ceiling ~12h same-day (in-transit overnight only counted as the €40 destination night). These are a starting point, NOT calibrated — the empirical loop owns them.

**STANDING (user 2026-06-11): any VISIBLE result/checkout Chrome window launches `--start-maximized`** — never a small fixed-size window. (Offscreen/headless sweeps unaffected.)

## Webapp = PERSISTENT infra (user 2026-06-11: "i dont want a new webapp each trip")
One Node server at `travel-search\v2\app\server.js` (port 4126, zero deps); a trip = a data folder `app\trips\<slug>\{options.json,duels.jsonl,status.json,meta.json,complete-queue.jsonl}`. Routes: `/` index, `/t/<slug>/duel`, `/t/<slug>/results`, `/t/<slug>/api/{state,duel,complete}`. **Flow: deep search → ~5-10 duels (user adds rich free-text comments = the missing context) → each duel flags rerankPending; I (LLM) rerank the FULL set via `llmRank` fields in options.json (builder respects llmRank over price-sort) and stamp meta.json {duelsAtRerank} → results page shows staleness chip.** Results page = horizontal rank cards, expandable to full D2D timeline; "Complete it live" buttons queue into complete-queue.jsonl for the (pending) exact-completion engine. `build_duel_data.py <slug>` regenerates segment timelines from spec constants. Validated 2026-06-11: duel notes surfaced an underivable constraint — **outbound arrival must be EVENING (pickup only after working hours)** — which inverted the ranking (F99 15:20 flight beat the "full day 1" 07:55 champion at equal €164 fare). Exactly the design's purpose.

## This trip's hard facts (test case)
Munich → Sarzana (final point), via Pisa. Outbound Jun 28 OR 29 2026; returns Jul 6/7/8 with >=8 days in Sarzana (so 29→6 invalid). **CORRECTION (verified 2026-06-10 via Ryanair timetable API): FMM→PSA does NOT exist** — Ryanair FMM→Italy = AHO/BDS/CTA/FCO/NAP/PMO/PSR/SUF only; PSA's only DACH Ryanair route = BER. The earlier recon-agent claim ("direct 3×/week Wed/Thu/Sun", from FlightsFrom) was stale — LESSON: always verify route-existence claims against the carrier's own schedule API before building logic on them. **Pisa still dominates arrival** (~1h30 D2D to Sarzana via PisaMover+Regionale) vs Genoa (~3h, slow coastal line). Luggage: user leans personal-item-only but wants the cabin-bag delta quantified.
**Tooling status (2026-06-10):** momondo headless is NOW BLOCKED by Akamai even with fresh cookie (drift since Jun 4) → all momondo sweeps must run `--offscreen`. Italian bot-page detector added to momondo.py. Ryanair public APIs (no auth): `ryanair.com/api/timtbl/3/schedules/<FROM>/<TO>/years/Y/months/M` + `ryanair.com/api/views/locate/searchWidget/routes/en/airport/<IATA>` — cheap ground truth for route existence. See [[feedback_trippy_headless_parallel]], [[feedback_trippy_metro_airport_normalization]] for the existing-skill mechanics v2 will reuse.

## Trip 2 — "Wisconsin 2026" (2026-06-15): momondo capture/filter lessons
One-way USA(Orfordville WI)→Asti, depart Aug 4/5, 1 carry-on, no return. ORD (O'Hare, ~2h drive)
is the only real transatlantic gate in the 3h catchment; MKE/MSN domestic feeders; Canada
roadtrip idea raised then dropped. **USER HARD RULE (locked): MAX 1 LAYOVER — 2+ stops = kill.**
**Two momondo engine bugs found + fixed in `momondo2.py`:**
1. **Capture depth too shallow + momondo VIRTUAL-SCROLLS.** Old `target_cards=45` and momondo
   keeps only ~50 cards in the DOM no matter how far you scroll (cards swap, count stays ~50).
   So with "best" sort stacking cheap 2-3 stop self-transfers on top, clean 1-stops never enter
   the window. Bumping target_cards alone does NOT help (virtual scroll cap). Added `--target-cards`
   + robust deep-load loop anyway (harmless), but the real fix is #2.
2. **Stops filter is the fix — but ONLY on single-route queries.** momondo path filter
   `/{date}/stops=-1` (=max 1 stop; `stops=0`=nonstop) WORKS and pushes clean 1-stops to the top
   — BUT it is SILENTLY IGNORED when origin is multi-airport (`ORD,MKE,MSN-MIL` commas break the
   path grammar). Must query SINGLE origin + SINGLE dest (e.g. `ORD-MXP`) for the filter to bite.
   Added `--max-stops` flag + grid-level `max_stops`. Verified: ORD→MXP Aug5 stops=-1 → 42×1-stop,
   3 nonstop, and surfaced the user's hand-found **JetBlue ORD-BOS-MXP €342, 14h14, carry-on incl**
   at #1 — which the old 45-card multi-origin sweep had MISSED entirely. LESSON: validation gate
   worked exactly as designed (user's manual search caught the gap). For the clean frontier, sweep
   single-route ORD→{MXP,TRN,GOA} per date with `max_stops:1`, then rank. The €342 JetBlue is the
   champion (cheapest protected 1-stop w/ carry-on); United ORD→MXP NONSTOP ≈ €506 (8h40) is the
   comfort ceiling. Deliverable = standalone `app/trips/asti-2026-08/board.html` (one-way native;
   the RT-shaped build_duel_data.py would render half-empty cards) + an "airports/stations checked"
   recon-transparency section the user explicitly requested.
**HARD RULE re-locked 2026-06-15: the deliverable is ALWAYS the persistent webapp
`http://127.0.0.1:4126/t/<slug>/results` (the same app every trip), NEVER a standalone .html.**
I wrongly shipped a `board.html` first; user pushed back ("you are supposed to always send me to
that same web app"). Fix: made `server.js` ONE-WAY-AWARE (guards every o.ret/segRet/totalsRet/
daysOnSite; renders single leg as GO/TRIP) and hosted the trip in the webapp via a per-trip
`app/trips/<slug>/build.py` that emits preBuilt one-way `options.json` (out-only, no ret,
daysOnSite:null, segOut+totalsOut). build_duel_data.py stays Munich-geo hardcoded → use preBuilt.
After any server.js edit: RESTART node (SHARED_JS baked at require) + headless-verify the page
paints. Deleted the standalone board.html. SKILL.md updated with all of this so it can't recur.
**RECURRING FAILURE re-caught 2026-06-15: treating DUELS as a RANKING tool.** They are NOT — they
are an INTERMEDIATE context-gatherer for a BIG SEARCH. The loop (already in SKILL.md, kept being
ignored): 5-duel batch → "Run big search" button → `meta.rulesState:"proposing"` → **Claude MUST
propose rules** (`meta.proposedRules=[{text,src}]`, `rulesState:"awaiting-confirm"`) → user
yes/no/edit/confirm → `api/confirm-rules` writes a `big-search` request → **Claude runs the COMPLETE
Step-0 bidirectional direct-connection scan** (every direct bus/train/low-cost from BOTH ends →
intersect for coincidence hubs → build custom connections the plain A→B search misses → priced vs a
benchmark so you know when to STOP). I failed by reranking the board and setting rulesState="idle",
ignoring that the user had clicked Run big search (state was "proposing"). The webapp ALREADY
implements the protocol (api/bigsearch, api/confirm-rules, N/5 batch bar, proposedRules render);
the gap was me not following it. Hardened SKILL.md with a ⛔ banner: "if all you did after a duel
batch was reorder the board, YOU FAILED THE SKILL" + "rulesState:proposing means the user is WAITING
for you to propose rules — never reset it." Every duel COMMENT is a candidate rule.
**2026-06-15 more fixes (all now WEBAPP INVARIANTS in SKILL.md — never regress, apply to every trip
since they live in shared server.js): (a)** route regex `api/\w+` silently 404'd `api/confirm-rules`
(hyphen!) → "confirm does nothing" bug; fixed to `api/[\w-]+`. **(b)** Built a GLOBAL live status bar
(`gstatus`+`STATUSJS` injected via `withStatus()` into results/duel/checked/report) that polls
api/state every 4s, shows the big-search banner on ALL pages, and AUTO-RELOADS once when a busy state
clears so new cards appear with no manual refresh (user demand). **(c)** Durations must be ACTUAL
travel time (store totalsOut.d2dMin), never local-clock spans (timezone inflation made ORD→MXP read
15h40 instead of 8h40). **(d)** Dedicated `/checked` page + nav. User stressed: these must REMAIN
across all future modifications → added a "WEBAPP INVARIANTS" list to SKILL.md + "verify after every
server.js edit (restart + headless grep)". **CROSS-TRIP PREFERENCE WIKI (built 2026-06-15):** `travel-search\v2\preferences.json` — ONE
structured JSON file (the "readable precedent wiki" the design always called for; NOT a DB/ML/app).
LOAD AT THE START OF EVERY TRIP. Each rule: statement, class tags (all/method/user-context/trip-class),
numeric value, status, strength (provisional 1-2 / established 3-5 / strong 6+), confirmations,
contradictions, evidence[], lastConfirmed, reconfirm. Apply strong/established silently; quick-confirm
provisional/shaky with ONE duel; user-context only when appliesWhen matches. MATCH similar cases to
existing rules (don't re-derive) → confirmations++ + refine value (e.g. nonstop-comfort-premium ~€77
on a ~€400 long-haul). UPDATE after each trip's duels (violations → contradictions++ + shaky). Seeded
with 10 rules. Full how-to in SKILL.md "CROSS-TRIP PREFERENCE WIKI". Over ~50 trips it recompiles into
a confident segmented preference fn. **PHILOSOPHY (user-locked 2026-06-17): infer STATEMENTS, not a
function.** Biggest statement: time is NOT one quantity — TRANSIT time (bus/plane/bench, aversive) vs
FIXED/STOPOVER time (a day in a city, neutral/positive); never count a stopover night as travel time
(d2dMin excludes it). **GATED SEARCH BRANCHES**: ideas that multiply search cost (e.g. split-day
stopovers — fly to a cheap hub, overnight in the layover city on a SEPARATE ticket, fly on next day)
must be DUEL-TESTED before the big search invests. Seeded `overnight-stopover-willingness` (status
untested, gatesSearchBranch) + `transit-vs-fixed-time` rules, a `philosophy` field in preferences.json,
an illustrative `SO` concept card on the asti board (stopover:true, night shown as FIXED not travel,
+probeFor selector). Always ask: is the system capturing the statements, not forcing a function?
**2026-07-19 (August-triple session) — three user-locked workflow rules:** (1) **Step -1 PREFLIGHT**:
every NEW trip starts with a tool map + ~30s live probe per needed tool (momondo, carrier APIs,
LeFrecce, bahn/Comet, FlixBus, ferries) and ONE compact ✓/⚠/✗ checklist so the user gives logins/
cookie-accepts up front, then Claude works long uninterrupted. (2) **Pass 1 must be the FULL search**
(complete Step-0 bidirectional + real prices where APIs allow) — thin Pass-1 boards caused "same four
options" duel fatigue; duels only ENRICH a good first search. (3) **Big-search output = REAL prices
only** (est chips surviving a big search on main legs = defect). Also: trip index now splits
Upcoming/Past by latest travel date (webapp invariant 4b); **Trenitalia LeFrecce BFF API works from
plain curl** (locations/search + POST ticket/solutions → live journeys+prices; found ICN 89512
REG→Asti direct €59.90 — user's hand-find, verified). All codified in SKILL.md.
**BIG SEARCH #1 result (asti-2026-08):** complete
bidirectional ORD-nonstop-hub × onward-to-Asti scan confirmed NOTHING beats JetBlue €342/€368 — cheap
ORD nonstops (NAP/FCO/MUC) are wrong-side-of-Alps (6-9h rail, killed); good-onward hubs (ZRH live €513
→ €566 d2d +€198, CDG TGV 5h35) erase the saving. JetBlue stays champion; stop-condition hit.
