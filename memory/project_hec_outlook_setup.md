---
name: hec-outlook-setup
description: HEC.edu Outlook/Microsoft 365 school account setup — OneAuth HRD blob location and tenant info
metadata: 
  node_type: memory
  type: project
  originSessionId: 11fd5c49-9911-4b79-a7fd-814e46ef643c
---

User has attempted to set up their HEC Paris school Outlook (Microsoft 365) account. Setup state is tracked by Windows OneAuth via the HRD (Home Realm Discovery) blob.

- HRD blob path: `C:\Users\Alessandro\AppData\Local\Microsoft\OneAuth\blobs\hec.edu_hrd`
- HEC tenant: `69d4d246-fd23-401b-9745-ff5ecb5a765d` (configProviderName `eudb.microsoftonline.com`, EMEA telemetry region)
- Authority: `login.microsoftonline.com`
- Account type: OrgId (Azure AD work/school), not MSA

**Why:** Came up in a session trying to set up the school account; the HRD blob confirms HEC is on EU data boundary (eudb) tenant on Azure AD.

**How to apply:** If future debugging touches Outlook auth, OneAuth/WAM, school-email login flows, or HEC SSO, point at this blob path and tenant ID rather than re-discovering them. If user reports "school email broken," check whether this blob still exists and whether the tenant ID still matches.

Related: [[reference_env_files]] for general secret-storage convention (this is OS-managed, not in `.env`).
