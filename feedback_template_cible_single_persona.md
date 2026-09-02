---
name: feedback_template_cible_single_persona
description: coattio outreach templates must have exactly ONE persona (cible) tag; the widget scorer is decisive and a boot audit guards it
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c32b433-096b-4c00-9d06-03e5f167f558
---

Every coattio/Alt+Shift+M outreach template must carry **exactly one `cible` persona tag**: `responsable-direct` (biomed/clinical engineer, procurement, IT, doctor — they OWN the topic, address directly), `directeur-hôpital` (hospital director/CFO — the "pas la bonne personne", ask to redirect), or `vendeur-hôpital` (AE — mentorship angle). `relai`/`achats` are intention/redirect tags, not personas.

**Why:** a template tagged with 2 cibles scores for both personas and silently serves the wrong template (2026-07-06: `long_postconnect_direct_fr` was tagged responsable-direct+directeur-hôpital → Stéphane Deville, a clinical engineer, got the director "expert opinion / pas la bonne personne" template and director Nicolas Peju got the direct-responsible one — swapped).

**How to apply:** the scorer (`intake-server.js#scoreTemplates`) is decisive — right cible **+4**, wrong-only **−6**, right+wrong (ambiguous) **neutral** so it can never win a half-match. `intake-server.js#auditCibles()` warns at boot on any template with >1 cible. When adding/editing templates keep it single-persona. Also `classifyCategory` biomed regex is `biom[eé]dica` (catches plural "biomédicaux/ales") in BOTH `intake-server.js` and `ingest-intake.js` — keep them mirrored. Canonical detail in [[reference_outreach_system]].
