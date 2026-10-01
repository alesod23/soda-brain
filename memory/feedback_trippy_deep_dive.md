---
name: feedback-trippy-deep-dive
description: Trippy workflow — two-pass depth (broad sweep → deep dive on user-selected config) and the carry-on luggage deep-dive process
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5bf3e4d7-faea-4ab8-a723-c9f3ef764fcf
---

> **2026-09-02: COMET ABANDONED — every "Comet" below now means CHROME (the default browser). See [[feedback-browser-chrome-default]].**

For trippy travel searches, two depth rules:

**1. Ancillary transit under €20 = first pass estimate only.** When trippy returns the initial multi-leg picks-table, short last-mile or first-mile bits (airport bus, S-Bahn, Alibus, SADEM, Orio Shuttle, etc.) should be quick-estimated from knowledge / casual web check and marked `(est)`. Don't drive Trenitalia / Italo / bus-operator forms for these on the first pass. Once the user picks a specific configuration (e.g. "going with config B"), then deep-dive every leg for exact times + prices.

**Why:** Driving 6 train-form lookups during a broad sweep wastes minutes that don't help yet — the user hasn't picked which sweep config to commit to, and 5/6 of those lookups will be thrown away.

**How to apply:** First-pass rows show `~€10 SADEM bus (est)`. Second pass shows `SADEM 12:55 Torino Porta Susa → 13:35 TRN, €10`. Validate "arrive at airport ≥ 1h30-2h before flight" constraint in deep-dive, not the sweep.

---

**2. Luggage = always deep-dive through the booking funnel.** Headline flight prices on Ryanair / easyJet / Wizz Air do NOT include a cabin bag larger than a personal item. When user mentions a bag (carry-on, checked, anything), open the booking flow in Playwright/Comet, advance through "select flight → fare or extras → passenger data" until you reach the page where bags can be added, and screenshot it. Report:

- Cheapest single-bag add-on matching the user's actual need (cabin 55×40×20 vs checked).
- Any fare-tier bundle that includes the bag + other stuff (priority, seat) — note both but flag the surplus.
- Standalone "checked bag" price if it's cheaper than the cabin upgrade.

**Why:** Ryanair's headline €17 flight + Priority bundle is €40-50 actual. Without the deep-dive, the trippy picks-table lies.

**How to apply:** Trigger only on explicit user request ("I need a carry-on" / "with luggage"). For backpack-only trips skip this step. After deep-dive, report `real total = €flight + €bag = €X` and use that as the comparison price across the legs.

---

**3. Hard rules for the FINAL deep dive (the pass after user picks a config):**

- **Never estimate.** If a price is hard to extract, iterate the scrape until you get the real number. Saying "typical €15-25, use ~€20" is unacceptable — the entire point of a deep dive is real numbers. Estimates are only allowed in the broad first-pass sweep.
- **Reach the checkout page for every purchasable leg.** For each flight, train, ferry: drive the booking flow in Comet through passenger details into the payment/checkout screen, then stop. Leave the Comet tab open at that screen so the user can finalize payment manually. The user does not authorize you to pay.
- **Use the user's real booking identity** when filling passenger data en route to checkout: name = "Alessandro Sodano", email = `alesoda2002@gmail.com`. For required-but-don't-yet-have fields (passport, DOB), use plausible placeholders and flag them in the HTML so the user updates them before paying.

**How to apply:** the deliverable of a final-pass deep dive is (a) the HTML in OneDrive `cooked trips\` updated with all-real prices and (b) N open Comet tabs each parked at "select payment / pay now". The user reviews the HTML, opens the matching tab, completes payment.

---

**4. Never stop at the first fare-tier upsell modal — push through to the Extras page.**

Ryanair, Wizz Air, easyJet etc. all show a "REGULAR includes bag + priority + seat!" modal right after you select a flight. The price diff they show (€20-25 typical) is the BUNDLED upgrade — it always includes other stuff you didn't ask for (priority boarding, seat-row choice). It is NOT the real cabin-bag price.

The REAL cabin-bag price lives on the Extras / Ancillaries / "Aggiungi extra" page, which is **after passenger data entry** in the booking funnel. There Ryanair sells "Priority Boarding & 2 Cabin Bags" as a standalone add-on for typically €5-15 cheaper than the REGULAR-tier diff. The user only wants the bag, so that's the right number.

**Why:** Recorded mistake — on a real deep dive for Asti↔Termoli the script stopped at the REGULAR-€24.95 modal and reported that as the bag price. Actual standalone Priority+2CabinBags was €15. The user called it lazy — correctly.

**How to apply:** Whenever a fare-tier upsell modal appears, ALWAYS click "Continua con Basic" (or "No thanks" / "Keep Basic"), then drive the booking funnel through passenger entry into the Extras page, then capture the standalone bag-only add-on price. If the passenger form blocks the script, iterate the selectors until it doesn't — the standalone bag price is the deliverable, not the upsell-bundle price.

Related: [[reference_travel_search]] (the trippy infrastructure), [[feedback_browser_comet]] (use Comet for the booking-flow Playwright sessions so user logins persist).
