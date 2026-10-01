---
name: reference_notion_image_upload_via_mcp
description: How to put local photos/files into a Notion page from the box: notion-create-file-upload (per file) + curl POST with the returned bearer, then <image src="file-upload://ID"> in update-page content. Verified 2026-09-14 with 17 jpgs.
metadata:
  type: reference
---

Local files into Notion (worked 2026-09-14, 17 Telegram photos onto the Nocco meeting page):

1. `notion-create-file-upload {filename}` once per file (batch the calls in one turn) → `file_upload_id`, `upload_url`, `upload_headers.authorization`. Slots expire in ~10 min.
2. `curl -X POST -H "authorization: Bearer <tok>" -F file=@<path> <upload_url>` → JSON with `"status":"uploaded"` and `markdown_source: file-upload://<id>`. Save id+token pairs to a TSV and loop.
3. Place with `notion-update-page` (`update_content` / `insert_content`): `<image src="file-upload://<id>"></image>`, one per line. Unattached uploads expire.

`notion-create-attachment` is only for inline text (≤200 KiB) or public HTTPS URLs; Telegram inbox files are local, so use the flow above. See also [[feedback_notion_update_content_fetch_first]] (anchors must match the re-rendered page).
