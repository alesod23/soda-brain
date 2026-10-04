/* feedback-box.js: the input box of the rule loop for ANY page (RULE-LOOP.md "The template of a loop", part 3).
 * His ask of 4 Oct 2026 18:45: every place he looks at should learn from what he says about it.
 *
 * One line on a page:  <script src="feedback-box.js" data-surface="system-map"></script>
 * A "Feedback" button bottom right; the box takes one sentence. The last thing he clicked on the page (its id, or its
 * first 80 characters) is sent as the item, so "this is wrong" points at the exact node. Posted to hub-review
 * POST /api/feedback {surface, item, line, text} (text/plain, no preflight; Tailscale only), queued as kind "feedback";
 * feedback_session.py classifies it (like | confirmation | rule | case | system | work, drafts/ledger_verdict.py) and
 * files it in the ledger it is about. Override the endpoint with data-endpoint. No dependency, no storage, no emoji.
 */
(function () {
  var me = document.currentScript;
  var SURFACE = (me && me.dataset.surface) || 'page';
  var ENDPOINT = (me && me.dataset.endpoint) || 'http://100.85.52.84:4142/api/feedback';
  var last = { item: '', line: '' };
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('[id],[data-id],g,section,tr,li,div') : null;
    if (!el || el.closest('#fbx-root')) return;
    var id = el.id || (el.dataset && el.dataset.id) || '';
    var txt = String(el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);
    last = { item: id || txt.slice(0, 40), line: txt };
  }, true);
  var css = '#fbx-root{--fbx-bg:#fff;--fbx-fg:#14171c;--fbx-mute:#5b6370;--fbx-line:#d9dde3;--fbx-acc:#0f766e;position:fixed;right:16px;bottom:16px;z-index:9999;font:14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif}' +
    '@media (prefers-color-scheme:dark){#fbx-root{--fbx-bg:#1b1f26;--fbx-fg:#e8eaee;--fbx-mute:#9aa3b0;--fbx-line:#333a45;--fbx-acc:#2dd4bf}}' +
    '#fbx-root button{font:inherit;cursor:pointer;border-radius:8px;border:1px solid var(--fbx-line);background:var(--fbx-bg);color:var(--fbx-fg);padding:8px 14px}' +
    '#fbx-root .fbx-go{background:var(--fbx-acc);border-color:var(--fbx-acc);color:#fff}' +
    '#fbx-panel{display:none;width:min(360px,calc(100vw - 32px));background:var(--fbx-bg);color:var(--fbx-fg);border:1px solid var(--fbx-line);border-radius:12px;padding:12px;box-shadow:0 6px 24px rgba(0,0,0,.15);margin-bottom:8px}' +
    '#fbx-panel textarea{width:100%;box-sizing:border-box;min-height:72px;font:inherit;color:var(--fbx-fg);background:transparent;border:1px solid var(--fbx-line);border-radius:8px;padding:8px}' +
    '#fbx-panel .fbx-m{color:var(--fbx-mute);font-size:12px;margin:4px 0 8px}#fbx-panel .fbx-row{display:flex;gap:8px;justify-content:flex-end;margin-top:8px}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var root = document.createElement('div'); root.id = 'fbx-root';
  root.innerHTML = '<div id="fbx-panel" role="dialog" aria-label="Feedback on this page"><div class="fbx-m" id="fbx-on"></div>' +
    '<textarea id="fbx-t" placeholder="what is wrong or right here (one sentence)"></textarea><div class="fbx-m" id="fbx-s"></div>' +
    '<div class="fbx-row"><button type="button" id="fbx-x">Cancel</button><button type="button" class="fbx-go" id="fbx-send">Keep it</button></div></div>' +
    '<button type="button" id="fbx-open">Feedback</button>';
  document.body.appendChild(root);
  var panel = root.querySelector('#fbx-panel'), t = root.querySelector('#fbx-t'), s = root.querySelector('#fbx-s');
  function open() { panel.style.display = 'block'; root.querySelector('#fbx-on').textContent = last.line ? 'on: ' + last.line : 'on: the whole page'; s.textContent = ''; t.focus(); }
  function close() { panel.style.display = 'none'; }
  root.querySelector('#fbx-open').onclick = function () { panel.style.display === 'block' ? close() : open(); };
  root.querySelector('#fbx-x').onclick = close;
  t.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } if (e.key === 'Escape') close(); });
  root.querySelector('#fbx-send').onclick = send;
  function send() {
    var text = t.value.trim(); if (!text) return;
    s.textContent = 'sending...';
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' },
      body: JSON.stringify({ surface: SURFACE, item: last.item, line: last.line + ' (' + (document.title || location.pathname) + ')', text: text, by: 'page' }) })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok) { t.value = ''; s.textContent = 'kept; filed within 5 min'; setTimeout(close, 1200); } else { s.textContent = 'not kept: ' + ((j && j.error) || 'unknown'); } })
      .catch(function (e) { s.textContent = 'hub-review not reachable (Tailscale?): ' + e.message; });
  }
})();
