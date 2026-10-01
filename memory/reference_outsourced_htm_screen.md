---
name: reference_outsourced_htm_screen
description: "How to check whether a US hospital's clinical engineering is outsourced (TriMedx, Agiliti, Sodexo, Crothall, Renovo, Intelas) before spending outreach on it - including the LinkedIn vendor-staff trick that works with no search engine."
metadata: 
  node_type: memory
  type: reference
  originSessionId: e7351fcb-845d-45ae-b97b-335e70d58b55
  modified: 2026-09-20T02:45:41.127Z
---

**A hospital whose HTM is outsourced has no in-house buyer for Tundra.** Alessandro asked for this
as an explicit extra check on the US campaign (2026-09-20), and it earned its place immediately.

**Two screens, use both:**

1. **Search, when there is budget.** `"<system>" TriMedx`, `"<system>" clinical engineering
   outsourced OR partnership OR "managed services"`. Trade press is where this lives: TechNation
   (1technation.com) "Department of the Month" features and Becker's report these transitions by
   name, usually with headcount.

2. **The LinkedIn vendor-staff trick, when search is gone.** An outsourcer's embedded staff name
   their client hospital in their own job title. One `search_people` for "TRIMEDX site manager
   clinical engineering" returns a free client list: *"Site Manager, Clinical Engineering - Nemours
   Children's Hospital", employer TRIMEDX*. Repeat for Agiliti, Sodexo, Crothall, Renovo, InterMed.
   This is how the screen kept running after the session's WebSearch budget died.

**Confirmed outsourced as of 2026-09-20** (do not cold-target, evidence in
`~/tundra-outreach/us-campaign-100/research/accounts-*.json`):

| Account | Vendor |
|---|---|
| Providence (51 hospitals) | TriMedx, ~250 CE staff transitioned |
| Sentara Health (12 hospitals) | TriMedx system-wide, stated on the record by TriMedx's own senior site manager |
| Ascension | TriMedx national enterprise contract (TriMedx was founded inside Ascension) |
| OSF HealthCare | TriMedx from June 2026, via its Pointcore subsidiary |
| Sharp HealthCare | Sodexo HTM |
| Nemours, IU Health, UChicago Medicine | TriMedx (their site managers name the sites) |
| St. Christopher's Hospital for Children | Intelas Health |
| **UPMC: Children's, Mercy, Magee, Washington, Greene only** | TriMedx at 5 of ~40 sites. The rest of UPMC stays targetable, so block at **facility** level, not account level. |

**The lesson that generalises:** an account can be clean at system level while specific hospitals
inside it are run by an outsourcer, and a fuzzy account matcher will happily attach a person at one
of those hospitals to the clean parent. Keep a facility-level block list separate from the account
list. Also treat "no evidence found" as different from "checked and clean" and different again from
"not checked" - the campaign carries an explicit `htm_screened` flag per person for exactly this.

Also not targets, for the same reason: anyone employed BY one of those vendors, and GPO staff
(Vizient, Premier, HealthTrust) who do not buy for a hospital.
