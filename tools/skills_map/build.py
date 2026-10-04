"""Builds soda-brain/system/SODA-SKILLS-MAP.html and .md from the live files (ledgers, skills, maps, hits, coverage).

    python soda-brain/tools/skills_map/build.py "<one sentence on the box copies, printed in the footer>"
Written by the 22:25 skills-map builder of the 4 Oct 2026 goal run; moved here from its scratchpad by G137 (23:05) so the
map can be rebuilt after a recompile. Reads page.css next to it. Laptop only (reads ~/.claude/skills)."""
import json, re, glob, os, subprocess, datetime as dt, html, collections, sys
from zoneinfo import ZoneInfo

HOME = os.path.expanduser('~').replace('\\', '/')
TL = HOME + '/task-land/_system'
SK = HOME + '/.claude/skills'
OUTDIR = HOME + '/soda-brain/system'
BER = ZoneInfo('Europe/Berlin')
NOW = dt.datetime.now(BER)
BOX_EXTRA = ['people-search', 'tundra-poc-deck']   # read on the box over ssh at build time (only there)
BOX_CHECKED = sys.argv[1] if len(sys.argv) > 1 else ''


def furl(p):
    p = p.replace('\\', '/')
    return 'file:///' + p.lstrip('/').replace(' ', '%20') if p[1:2] == ':' else 'file:///' + p


def win(p):  # /c/Users -> C:/Users ; C:/Users stays
    p = p.replace('\\', '/')
    if re.match(r'^/[a-z]/', p): p = p[1].upper() + ':' + p[2:]
    return p


HOMEW = win(HOME)
TLW, SKW, OUTW = HOMEW + '/task-land/_system', HOMEW + '/.claude/skills', HOMEW + '/soda-brain/system'


def fm(path):
    t = open(path, encoding='utf-8').read()
    m = re.match(r'---\r?\n(.*?)\r?\n---', t, re.S); f = {}
    if m:
        cur = None
        for line in m.group(1).splitlines():
            mm = re.match(r'^(\w[\w-]*):\s*(.*)$', line)
            if mm: cur = mm.group(1); f[cur] = mm.group(2).strip()
            elif cur: f[cur] = (f[cur] + ' ' + line.strip()).strip()
    f['desc'] = re.sub(r'^[>|]\s*', '', f.get('description', '')).strip().strip('"')
    f['lines'] = t.count('\n') + 1
    f['tags'] = len(re.findall(r'\[ledger H', t))
    ex = None
    for line in t.splitlines():
        if line.startswith('**R1.**'):
            ex = line; break
    if ex:
        tag = re.findall(r'\[ledger [^\]]+\]', ex)
        body = re.sub(r'\s*\[ledger [^\]]+\]\s*$', '', ex).replace('**R1.**', '').strip()
        body = re.sub(r'\s*\[item: [^\]]*\]', '', body).replace('`', '')
        body = re.sub(r'\*e\.g\.\*', 'e.g.', body).replace('*"', '"').replace('"*', '"')
        if len(body) > 300: body = body[:297].rsplit(' ', 1)[0] + ' ...'
        f['example'] = (body, tag[-1] if tag else '')
    return f


def ledger(name):
    t = open(f'{TL}/{name}', encoding='utf-8').read()
    rows = re.findall(r'^\| H(\d+) \|(.*)$', t, re.M)
    n = len(rows)
    top = max(rows, key=lambda r: int(r[0])) if rows else None
    date = None
    if top:
        d = re.findall(r'20\d\d-\d\d-\d\d', top[1].split('|')[-2] if top[1].count('|') >= 2 else top[1])
        date = d[0] if d else None
    return {'rules': n, 'top': 'H' + top[0] if top else None, 'date': date}


hits = collections.Counter(); bad = collections.Counter(); last = {}
for l in open(TL + '/rule-hits.jsonl', encoding='utf-8'):
    try: d = json.loads(l)
    except Exception: continue
    s = d.get('surface'); hits[s] += 1
    if d.get('action') != 'ok': bad[s] += 1
    ts = d.get('ts')
    if ts:
        try:
            t = dt.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(BER)
            if s not in last or t > last[s]: last[s] = t
        except Exception: pass

# coverage table from the checker
cov = {}
try:
    md = subprocess.run([sys.executable, TL + '/rule_loop_check.py', '--md'], capture_output=True, text=True, encoding='utf-8',
                        timeout=180, cwd=HOME + '/task-land', stdin=subprocess.DEVNULL,
                        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
    for line in md.splitlines():
        if line.startswith('| ') and not line.startswith('| surface') and not line.startswith('|---'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) == 7: cov[cells[0]] = cells[1:]
    cov_total = next((l for l in md.splitlines() if l.startswith('G green')), '')
except Exception as e:
    cov_total = f'rule_loop_check.py did not run: {e}'
PARTS = ['ledger', 'skill', 'box', 'route', 'observer', 'brain']

# surfaces with a ledger
SURF = [
    dict(key='email', ledger='EMAIL-REVIEW-CONTRACT.md', skill='drafting', title='Messages to a person', cov=['email (drafts)'],
         loads='every session before it writes a message to a person (email, WhatsApp, LinkedIn); the draft critic reads the ledger itself; the event-page Confirmed worker reads it too',
         inp='On the CRM review, a / s / c on the message (the reason box), or one sentence on Telegram or in a session: filed into this ledger the same turn.'),
    dict(key='crm', ledger='CRM-CONTRACT.md', skill='crm', title='The CRM', cov=['CRM review + Ask box'],
         loads='review-api.js (the CRM reader, before it decides a next step) and every session before it writes to the CRM; the event-page Confirmed worker',
         inp='On the CRM row, a / s / r / c or the Ask box; or say it on Telegram: filed the same turn.'),
    dict(key='hub', ledger='HUB-CARD-CONTRACT.md', skill='hub', title='Hub cards (the Ping hub)', cov=['hub cards'],
         loads='every session before it posts a card to the hub (127.0.0.1:4180); the hub guard checks hub-rules.json',
         inp='The comment box under any verdict on hub-review, or a reply to the card: filed the same turn.'),
    dict(key='proactive', ledger='PROACTIVE-CONTRACT.md', skill='proactive', title='What the system picks up on its own', cov=['proactive (to-do pickup)', 'proactive-todo (to-dos from an ask he accepted, G118)', 'daily page + to-do lines'],
         loads='pipeline.py (pickup --auto / ready --auto), proactive_todo.decide on every call, and the daily page decider (Resolve-TaskDirective)',
         inp='A comment on the hub card of the picked-up task, or ((rule: ...)) on any line of the daily page: filed the same turn.'),
    dict(key='notif', ledger='NOTIF-CONTRACT.md', skill='notif', title='What reaches your phone unasked', cov=['notifications (SODANOtif)'],
         loads='the SODANOtif classifier on the box (sodanotif/daemon.js, buildSystemPrompt) on every batch',
         inp='On Telegram, a message starting notif: (or a quote-reply to the card): filed the same turn.'),
    dict(key='whitelist', ledger='WHITELIST-CONTRACT.md', skill='whitelist', title='Fixes made without asking', cov=['whitelist fixes'],
         loads='drafts/whitelist_judge.py on every call (made at once, or an approval card)',
         inp='The verdict box on the Whitelist tab of hub-review ("this needed approval", "this was fine"): filed the same turn.'),
    dict(key='board', ledger='BOARD-CONTRACT.md', skill='board', title='GTM boards', cov=['GTM boards (s/c boxes)'],
         loads='the daily-campaign research workers (gtm-eng/daily-campaign/workers.js) on every run',
         inp='The comment box under a board card (a / s / c, "why skip?"): filed the same turn.'),
    dict(key='cleaning', ledger='CLEANING-CONTRACT.md', skill='cleaning', title='Cleanup (the janitor)', cov=['cleaning (janitor)'],
         loads="hub_outdated.py's judge on every call (before it ticks, closes, merges or rewords an item on its own)",
         inp='The box next to each line of the Cleaning tab on hub-review: filed the same turn.'),
    dict(key='meeting', ledger='MEETING-CONTRACT.md', skill=None, title='Meeting notes into steps', cov=['meeting notes'],
         governs='Meeting notes (the Notion meeting AI page) turned into steps: what the meeting loop asks of each transcript and the steps it proposes.',
         loads='gtm-eng/agent/meeting_loop.py reads the ledger itself on every run (no compiled skill)',
         inp='A comment on the hub card the meeting loop produces, or one sentence on Telegram: filed the same turn.'),
    dict(key='trippy', ledger='TRIPPY-CONTRACT.md', skill='trippy', handskill=True, title='Trips (trippy)', cov=['trippy boards'],
         governs='How a trip is searched and judged: modes, layovers, overnights, departure times, comfort against price. preferences.json stays the engine\'s own store.',
         loads='the trip worker reads the ledger and preferences.json; the trippy skill itself is hand-written',
         inp='A comment on a rule on the trip board, or a context duel: filed the same turn.'),
]

skills = {os.path.basename(os.path.dirname(p)): fm(p) for p in sorted(glob.glob(SK + '/*/SKILL.md'))}
maps = {}
for p in glob.glob(TL + '/drafts/skill-map-*.json'):
    d = json.load(open(p, encoding='utf-8')); maps[d['surface']] = os.path.basename(p)
used = {s['skill'] for s in SURF if s['skill']}
hand = [n for n in skills if n not in used or n == 'trippy']
hand = [n for n in hand if not skills[n].get('compiled')]


def ago(t):
    return t.strftime('%-d %b %H:%M') if os.name != 'nt' else t.strftime('%d %b %H:%M').lstrip('0')


# ---------- HTML ----------
E = html.escape


def link(label, path, box=False):
    w = win(path)
    if box:
        return f'<div class="lk"><span class="mono boxp">{E(path)}</span><span class="note">on the box (text only)</span></div>'
    u = furl(w)
    return (f'<div class="lk"><a href="{E(u)}">{E(label)}</a>'
            f'<code class="md">[{E(label)}]({E(u)})</code></div>')


def chips(rowname):
    c = cov.get(rowname)
    if not c: return ''
    out = []
    for part, cell in zip(PARTS, c):
        g = cell.split(' ', 1)[0]
        cls = {'G': 'g', 'A': 'a', 'R': 'r'}.get(g, 'n')
        lab = {'g': 'green', 'a': 'amber', 'r': 'red', 'n': 'n/a'}[cls]
        out.append(f'<span class="chip {cls}" title="{E(cell)}"><i></i>{part}<b class="sr"> {lab}</b></span>')
    ev = ''.join(f'<li><b>{p}</b> {E(cell)}</li>' for p, cell in zip(PARTS, c))
    return (f'<div class="covrow"><span class="covname">{E(rowname)}</span><div class="chips">{"".join(out)}</div></div>'
            f'<details class="ev"><summary>why each colour</summary><ul>{ev}</ul></details>')


def obs(key):
    if not hits.get(key):
        return 'no line in rule-hits.jsonl yet'
    t = last.get(key)
    return (f'{hits[key]:,} lines, {bad[key]:,} of them a hit (not "ok"); last line {ago(t)}' if t else f'{hits[key]:,} lines')


cards = []
md_cards = []
nocompile = []
for s in SURF:
    L = ledger(s['ledger']); sk = skills.get(s['skill']) if s['skill'] else None
    compiled = bool(sk and sk.get('compiled'))
    governs = sk['desc'] if compiled else s['governs']
    tag = 'compiled' if compiled else ('ledger, skill hand-written' if s.get('handskill') else 'ledger only, no skill')
    rows = []
    mdrows = []
    led_p = f'{TLW}/{s["ledger"]}'
    rows.append(('Ledger', link(s['ledger'], led_p) +
                 f'<p class="facts">{L["rules"]} rules; newest row {L["top"]}{", " + L["date"] if L["date"] else " (no date on the row)"}</p>'))
    mdrows.append(f'- Ledger: [{s["ledger"]}]({furl(led_p)}) · {L["rules"]} rules · newest row {L["top"]}{", " + L["date"] if L["date"] else " (no date on the row)"}')
    if s['skill']:
        inst = f'{SKW}/{s["skill"]}/SKILL.md'; mir = f'{TLW}/laptop-tools/skills/{s["skill"]}/SKILL.md'
        box = f'/home/da/.claude/skills/{s["skill"]}/SKILL.md'
        if compiled:
            newer = L['rules'] - int(sk.get('rules_in_ledger', 0))
            facts = (f'compiled {sk["compiled"]} (skill_v {sk.get("skill_v", "?")}); {sk.get("rules_in_front")} rules in front, '
                     f'compiled from {sk.get("rules_in_ledger")} ledger rules; {sk["tags"]} [ledger H..] tags')
            if newer > 0: facts += f'; {newer} ledger row{"s" if newer > 1 else ""} newer than this compile, not in the skill yet'
        else:
            facts = f'hand-written, {sk["lines"]} lines, no [ledger H..] tags'
        rows.append(('Skill', link(f'{s["skill"]}/SKILL.md (installed)', inst) + link(f'{s["skill"]}/SKILL.md (mirror in task-land)', mir) +
                     link('', box, box=True) + f'<p class="facts">{E(facts)}</p>'))
        mdrows.append(f'- Skill: [{s["skill"]}/SKILL.md (installed)]({furl(inst)}) · [mirror in task-land]({furl(mir)}) · box `{box}` · {facts}')
    else:
        rows.append(('Skill', '<p class="facts">none: the decider reads the ledger itself</p>'))
        mdrows.append('- Skill: none, the decider reads the ledger itself')
    if s['key'] in maps:
        mp = f'{TLW}/drafts/{maps[s["key"]]}'
        rows.append(('Map', link(maps[s['key']], mp) + f'<p class="facts">which ledger rows merge into which rule, the group, the example; compile: <code>python task-land/_system/drafts/compile_skill.py --contract {s["key"]} --install</code></p>'))
        mdrows.append(f'- Map: [{maps[s["key"]]}]({furl(mp)}) · compile with `python task-land/_system/drafts/compile_skill.py --contract {s["key"]} --install`')
    else:
        rows.append(('Map', '<p class="facts">no skill map (nothing is compiled for this surface)</p>'))
        mdrows.append('- Map: none (nothing is compiled for this surface)')
    rows.append(('Loaded by', f'<p class="facts">{E(s["loads"])}</p>'))
    mdrows.append(f'- Loaded by: {s["loads"]}')
    rows.append(('Observer', f'<p class="facts">{E(obs(s["key"]))}</p>'))
    mdrows.append(f'- Observer: {obs(s["key"])}')
    ex = ''
    if compiled and sk.get('example'):
        b, t = sk['example']
        ex = f'<figure class="ex"><figcaption>How a rule reads in the skill (R1)</figcaption><p>{E(b)} <span class="tag">{E(t)}</span></p></figure>'
        mdrows.append(f'- R1 as it reads in the skill: "{b}" `{t}`')
    covh = ''.join(chips(r) for r in s['cov'])
    for r in s['cov']:
        if r in cov:
            mdrows.append(f'- Coverage ({r}): ' + ', '.join(f'{p} {c.split(" ", 1)[0]}' for p, c in zip(PARTS, cov[r])))
    mdrows.append(f'- Your input: {s["inp"]}')
    dl = ''.join(f'<div class="kv"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    cls = 'compiled' if compiled else 'plain'
    cards.append((compiled, f'''<article class="card" id="s-{s["key"]}">
  <header><h3>{E(s["title"])}</h3><span class="badge {cls}">{tag}</span></header>
  <p class="gov">{E(governs)}</p>
  <dl>{dl}</dl>
  {ex}
  <div class="cov">{covh}</div>
  <p class="input"><b>Your input</b> {E(s["inp"])}</p>
</article>'''))
    md_cards.append((compiled, f'### {s["title"]} ({tag})\n\n{governs}\n\n' + '\n'.join(mdrows) + '\n'))

hand_cards = []; md_hand = []
for n in hand:
    sk = skills[n]
    inst = f'{SKW}/{n}/SKILL.md'; mir = f'{TLW}/laptop-tools/skills/{n}/SKILL.md'
    d = sk['desc']
    if len(d) > 260: d = d[:257].rsplit(' ', 1)[0] + ' ...'
    hand_cards.append(f'''<article class="mini"><header><h4>{E(n)}</h4><span class="facts">{sk["lines"]} lines</span></header>
  <p class="gov">{E(d)}</p>{link(n + "/SKILL.md (installed)", inst)}{link(n + "/SKILL.md (mirror)", mir)}{link("", f"/home/da/.claude/skills/{n}/SKILL.md", box=True)}</article>''')
    md_hand.append(f'- **{n}** ({sk["lines"]} lines): [installed]({furl(inst)}) · [mirror]({furl(mir)}) · box `/home/da/.claude/skills/{n}/SKILL.md`. {d}')
for n in BOX_EXTRA:
    bm = f'{TLW}/box-tools/skills/{n}/SKILL.md'
    if os.path.exists(bm):
        bd = fm(bm)['desc']
        if len(bd) > 260: bd = bd[:257].rsplit(' ', 1)[0] + ' ...'
        hand_cards.append(f'''<article class="mini boxonly"><header><h4>{E(n)}</h4><span class="facts">box only</span></header>
  <p class="gov">{E(bd)}</p>{link(n + "/SKILL.md (box copy mirrored in task-land)", bm)}{link("", f"/home/da/.claude/skills/{n}/SKILL.md", box=True)}</article>''')
        md_hand.append(f'- **{n}** (box only, not installed on the laptop): [box copy mirrored in task-land]({furl(bm)}) · box `/home/da/.claude/skills/{n}/SKILL.md`. {bd}')

n_comp = sum(1 for c, _ in cards if c)
compiled_html = '\n'.join(h for c, h in cards if c)
other_html = '\n'.join(h for c, h in cards if not c)

STEPS = [
    ('You say it', 'One sentence, anywhere: Telegram, a card comment, a box on a page, ((rule: ...)) on the daily page, the CRM row.', []),
    ('addrule.py files it', 'The same turn, into the ledger the sentence is ABOUT (you never pick it).', [('addrule.py', f'{TLW}/drafts/addrule.py')]),
    ('The ledger', 'Your words, dated, verbatim, never edited: one row H&lt;n&gt; per sentence.', [('_system/', f'{TLW}/')], '&lt;SURFACE&gt;-CONTRACT.md'),
    ('The skill map', 'Which ledger rows merge into which rule, the group, one example in your voice.', [], 'drafts/skill-map-&lt;surface&gt;.json'),
    ('compile_skill.py', 'Turns ledger + map + hit counts into one screen; checks itself; writes nothing if a check fails.', [('compile_skill.py', f'{TLW}/drafts/compile_skill.py')]),
    ('The compiled skill', 'Up to 15 rules in front, each tagged [ledger H&lt;n&gt;]; the rest under "Assumed". Three copies: installed, mirrored in task-land, on the box.', [], '~/.claude/skills/&lt;name&gt;/SKILL.md'),
    ('Who loads it', 'The code that decides, on every call (named in the skill\'s first line), or a session about to do that kind of work.', []),
    ('The observer', 'Checks each thing made against the rules after the fact; one line per check in rule-hits.jsonl. Never edits, never blocks.', [('rule-hits.jsonl', f'{TLW}/rule-hits.jsonl')]),
]
steps_html = ''
for i, st in enumerate(STEPS, 1):
    t, body, lks = st[0], st[1], st[2]
    pat = f'<code class="pat">{st[3]}</code>' if len(st) > 3 else ''
    lh = ''.join(link(a, b) for a, b in lks)
    steps_html += f'<li class="step"><span class="n">{i}</span><h4>{t}</h4><p>{body}</p>{pat}{lh}</li>'

loop_html = f'''<ol class="steps">{steps_html}</ol>
<p class="back"><b>Back to step 5.</b> The hit counts decide what stays in front: a rule that keeps firing comes forward, a rule that has not fired in its last 50 checked cases sinks to "Assumed" (still checked, back in front the moment it fires). A "like" becomes the example of the rule it fits.</p>
<div class="srcs">{link("RULE-LOOP.md (section 7 is the template)", TLW + "/RULE-LOOP.md")}{link("rule_loop_check.py (the six parts, measured)", TLW + "/rule_loop_check.py")}</div>'''

NUM = {8: 'Eight', 9: 'Nine', 10: 'Ten', 7: 'Seven'}
m_ = re.match(r'G green (\d+), A amber (\d+), R red (\d+) of (\d+)', cov_total)
cov_short = f'{m_[1]} green, {m_[2]} amber, {m_[3]} red of {m_[4]} parts' if m_ else cov_total
built = NOW.strftime('%d %b %Y %H:%M').lstrip('0')
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page.css'), encoding='utf-8').read()

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SODA Skills Map</title>
<meta name="description" content="Every skill of the SODA system in its current state: the rule loop, each surface's ledger, compiled skill, map, loader, observer and coverage, and the hand-written skills.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
{CSS}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <span class="brand">SODA Skills Map</span>
  <nav class="sections"><a href="#first">Read first</a><a href="#loop">The loop</a><a href="#compiled">Compiled</a><a href="#ledger-only">Ledger, not compiled</a><a href="#hand">Hand-written</a></nav>
</div></header>
<main>
<section class="hero"><div class="wrap">
  <div class="eyebrow">soda-brain / system</div>
  <h1>Every skill, as it is tonight</h1>
  <p class="lede">A skill is the one screen a model reads before it does a kind of work. {NUM.get(n_comp, n_comp)} of them are compiled from your own sentences (a ledger per surface); two ledgers are read directly without a compiled skill; the other {len(hand_cards)} are written by hand (two of those exist only on the box). Every file below opens on this laptop.</p>
  <div class="meta"><span>Built <b>{built}</b> from the live files</span><span><b>{n_comp}</b> compiled</span><span><b>{len(SURF) - n_comp}</b> ledger, not compiled</span><span><b>{len(hand_cards)}</b> hand-written</span><span>Loop coverage: <b>{E(cov_short)}</b></span></div>
  <p class="see">See also</p>{link("SODA-SYSTEM-MAP.html", OUTW + "/SODA-SYSTEM-MAP.html")}
</div></section>

<section class="block" id="first"><div class="wrap">
  <div class="first">
    <h2>Read this first</h2>
    <ol>
      <li><b>Read it.</b> Open a skill's <code>SKILL.md</code> (installed copy, or the mirror in task-land: same file). Start with <a href="#s-email">drafting</a> or <a href="#s-hub">hub</a>, the two with the most of your rules.</li>
      <li><b>Say what is wrong.</b> One sentence where you see the thing it made (the "your input" line on each card), or on Telegram. It is filed into the right ledger the same turn; you never edit a skill or a ledger.</li>
      <li><b>See which rule produced a line.</b> Every rule in a compiled skill ends with a tag like <span class="tag">[ledger H12]</span>: that is row H12 of its ledger, your sentence, dated and verbatim.</li>
    </ol>
    <p class="note">The file links open on your laptop only. On claude.ai they do not open; the Markdown line under each link is the same address for Obsidian or any viewer.</p>
    {link("SODA-SKILLS-MAP.md (this page as Markdown links)", OUTW + "/SODA-SKILLS-MAP.md")}
  </div>
</div></section>

<section class="block" id="loop"><div class="wrap">
  <div class="eyebrow">The rule loop</div>
  <h2>From your sentence to the line a model reads</h2>
  <p class="intro">You say what is wrong once. That sentence is filed the same turn into the ledger it is about, in your words, with the date. A small map says which of your sentences belong together; the compiler turns ledger and map into one screen, with an example in your voice for each rule, and installs it. The code that makes the thing (a draft, a card, a CRM step, a phone notification) reads that screen on every call. Afterwards an observer checks what was made against the same rules and writes one line per check; those counts go back into the next compile, so what still goes wrong stays in front and what never fires steps back.</p>
  {loop_html}
</div></section>

<section class="block" id="compiled"><div class="wrap">
  <div class="eyebrow">Compiled from a ledger</div>
  <h2>The {n_comp} compiled skills</h2>
  <p class="intro">Coverage chips are the six parts of a loop measured by <code>rule_loop_check.py</code> tonight: green works, amber partly, red missing. Open "why each colour" for the evidence.</p>
  <div class="cards">{compiled_html}</div>
</div></section>

<section class="block" id="ledger-only"><div class="wrap">
  <div class="eyebrow">A ledger, no compiled skill</div>
  <h2>Read directly from the ledger</h2>
  <p class="intro">These two learn from your sentences too, but the code reads the ledger itself instead of a compiled screen.</p>
  <div class="cards">{other_html}</div>
</div></section>

<section class="block" id="hand"><div class="wrap">
  <div class="eyebrow">Hand-written</div>
  <h2>The {len(hand_cards)} hand-written skills</h2>
  <p class="intro">No ledger behind them: a session loads one when your ask matches its first line. A sentence about how a message, a card or a CRM row is made still goes into that surface's ledger; a change to how one of these skills works is an edit of the file, by a session, when you ask.</p>
  <div class="minis">{''.join(hand_cards)}</div>
</div></section>
</main>
<footer class="foot"><div class="wrap"><p>Built {built} by reading the ledgers (<code>task-land/_system/*-CONTRACT.md</code>), the skills (<code>~/.claude/skills/*/SKILL.md</code>), the maps, <code>rule-hits.jsonl</code> and <code>rule_loop_check.py --md</code>. {E(BOX_CHECKED)}</p></div></footer>
</body>
</html>
'''
open(OUTDIR + '/SODA-SKILLS-MAP.html', 'w', encoding='utf-8', newline='\n').write(page)

# ---------- MD ----------
mdsteps = '\n'.join(f'{i}. **{re.sub("&lt;", "<", re.sub("&gt;", ">", st[0]))}**: {re.sub("&gt;", ">", re.sub("&lt;", "<", st[1]))}' +
                    (f' `{re.sub("&gt;", ">", re.sub("&lt;", "<", st[3]))}`' if len(st) > 3 else '') +
                    ''.join(f' [{a}]({furl(b)})' for a, b in st[2]) for i, st in enumerate(STEPS, 1))
md = f'''# SODA SKILLS MAP: every skill, as it is tonight

The visual page is [SODA-SKILLS-MAP.html]({furl(OUTW + "/SODA-SKILLS-MAP.html")}); this file is the same content as Markdown links,
for Obsidian or any viewer. Built {built} from the live files. See also [SODA-SYSTEM-MAP.md]({furl(OUTW + "/SODA-SYSTEM-MAP.md")}).

{n_comp} compiled skills, {len(SURF) - n_comp} ledgers read without a compiled skill, {len(hand_cards)} hand-written skills.
Coverage (rule_loop_check.py --md): {cov_total}

## Read this first

1. **Read it.** Open a skill's `SKILL.md` (installed copy, or the mirror in task-land: same file).
2. **Say what is wrong.** One sentence where you see the thing it made (the "your input" line of each surface), or on Telegram. It is filed into the right ledger the same turn; you never edit a skill or a ledger.
3. **See which rule produced a line.** Every rule in a compiled skill ends with a tag like `[ledger H12]`: row H12 of its ledger, your sentence, dated and verbatim.

The file links open on the laptop only; on claude.ai they do not open.

## The rule loop

You say what is wrong once. That sentence is filed the same turn into the ledger it is about, in your words, with the date. A small map says which of your sentences belong together; the compiler turns ledger and map into one screen, with an example in your voice for each rule, and installs it. The code that makes the thing reads that screen on every call. Afterwards an observer checks what was made against the same rules and writes one line per check; those counts go back into the next compile, so what still goes wrong stays in front and what never fires steps back.

{mdsteps}

Back to step 5: the hit counts decide what stays in front; a rule with no hit in its last 50 checked cases sinks to "Assumed" (still checked, back in front the moment it fires). A "like" becomes the example of the rule it fits.

Sources: [RULE-LOOP.md]({furl(TLW + "/RULE-LOOP.md")}) (section 7 is the template) · [rule_loop_check.py]({furl(TLW + "/rule_loop_check.py")}) · [compile_skill.py]({furl(TLW + "/drafts/compile_skill.py")}) · [addrule.py]({furl(TLW + "/drafts/addrule.py")})

## The {n_comp} compiled skills

{chr(10).join(m for c, m in md_cards if c)}
## Read directly from the ledger

{chr(10).join(m for c, m in md_cards if not c)}
## The {len(hand_cards)} hand-written skills

No ledger behind them: a session loads one when your ask matches its first line.

{chr(10).join(md_hand)}

{BOX_CHECKED}
'''
open(OUTDIR + '/SODA-SKILLS-MAP.md', 'w', encoding='utf-8', newline='\n').write(md)
print('ok', n_comp, len(SURF) - n_comp, len(hand_cards), 'cov rows', len(cov), cov_total)
