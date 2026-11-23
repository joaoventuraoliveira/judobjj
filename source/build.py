"""
build.py — gera o livro (livro.html) e a versão de impressão (print.html → PDF)
a partir do documento exportado (doc.md) e das ilustrações em assets/.
Uso: python3 build.py && python3 make_pdf.py
"""
import re, html, json, sys, unicodedata
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
MD = (ROOT / 'doc.md').read_text(encoding='utf-8')
sys.path.insert(0, '/home/claude/judo_figs/scripts')
from make_extra import REN, REN_SOLO, KAE, PRO  # títulos das figuras novas
from enrich import (build_tech, enrich_section, Bib, bib_chapter, glossary_chapter,
                    transparency_chapter, GLOSS_DATA, MODEL, VENDOR)

TITLE = 'Judô: técnicas e exames de faixa'
SUB = 'Programa da CBJ, regras e classificação da IJF/Kodokan, ilustrado'


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


# ------------------------------------------------------------ mapa alt → imagem
SECTION_IMG = [('Ritsu-rei', 'ritsu_rei'), ('Ippon', 'ippon'), ('Kesa-gatame: tori', 'kesa_gatame'),
               ('Kumi-kata', 'kumikata'), ('Sequência de cores', 'faixas'), ('Yoko-ukemi', 'yoko_ukemi'),
               ('Za-rei', 'za_rei'), ('Candidato de branco', 'banca'), ('Examinador de azul', 'outorga'),
               ('Shizen-hontai', 'shizen_hontai'), ('Seiza', 'seiza')]
REN_ALL = [(t, n) for n, t, *_ in REN] + [(t, n) for n, t, *_ in REN_SOLO]
KAE_ALL = [(t, n) for n, t, *_ in KAE]
PRO_ALL = [(t, n) for n, t, *_ in PRO]


def img_for(alt):
    if alt.startswith('Figura'):
        num = re.search(r'Figura (\d)', alt).group(1)
        return f'assets/diag/fig{num}.webp', alt, 'diag'
    m = re.match(r'(.+) em três fases', alt)
    if m:
        return f'assets/img/tri_{slug(m.group(1)).replace("-", "_")}.webp', m.group(1), 'tri'
    for key, f in SECTION_IMG:
        if alt.startswith(key):
            return f'assets/img/{f}.webp', alt, 'sec'
    if ' para ' in alt:
        a = alt.replace(' para ', ' → ')
        for t, n in REN_ALL:
            if t.startswith(a):
                return f'assets/img/{n}.webp', t, 'ren'
    head = alt.split(' — ')[0]
    for t, n in KAE_ALL + PRO_ALL:
        if t == head or t.startswith(head + ' ('):
            return f'assets/img/{n}.webp', t, 'kae' if n.startswith('kae') else 'pro'
    raise KeyError(alt)


PH = re.compile(r'^&#91;(?:image|embedded content): (.+?)\\\]$')
CAP = re.compile(r'^\*(.+)\*$')


def figure_html(src, label, caption, eid):
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return (f'<figure class="fig" id="{eid}"><button class="zoom" data-src="{src}" aria-label="Ampliar: {html.escape(label)}">'
            f'<img src="{src}" alt="{html.escape(label)}" loading="lazy" decoding="async"></button>{cap}</figure>')


def carousel_html(items, kind):
    slides = []
    for src, label, cap in items:
        sid = 't-' + slug(label)
        txt = cap or label
        slides.append(f'<li class="slide" id="{sid}" data-name="{html.escape(label)}"><figure>'
                      f'<button class="zoom" data-src="{src}" aria-label="Ampliar: {html.escape(label)}">'
                      f'<img src="{src}" alt="{html.escape(label)}" loading="lazy" decoding="async"></button>'
                      f'<figcaption>{txt}</figcaption></figure></li>')
    return (f'<div class="carousel" data-kind="{kind}" role="region" aria-roledescription="carrossel">'
            f'<div class="car-bar"><span class="car-count">1 / {len(items)}</span>'
            f'<span class="car-hint">deslize ou use as setas</span>'
            f'<button class="car-prev" aria-label="Anterior">‹</button><button class="car-next" aria-label="Próximo">›</button></div>'
            f'<ul class="track">{"".join(slides)}</ul><div class="dots" aria-hidden="true"></div></div>')


def transform(md):
    lines = md.split('\n')
    out, i, fig_n = [], 0, 0
    while i < len(lines):
        m = PH.match(lines[i].strip())
        if not m:
            out.append(lines[i]); i += 1; continue
        group = []
        while i < len(lines):
            m = PH.match(lines[i].strip())
            if not m:
                if lines[i].strip() == '':
                    i += 1; continue
                break
            alt = m.group(1)
            i += 1
            cap = None
            j = i
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and CAP.match(lines[j].strip()) and not PH.match(lines[j].strip()):
                cap = CAP.match(lines[j].strip()).group(1)
                i = j + 1
            src, label, kind = img_for(alt)
            group.append((src, label, cap, kind))
        if len(group) >= 2:
            kind = group[0][3]
            out += ['', carousel_html([(s, l, c) for s, l, c, k in group], kind), '']
        else:
            fig_n += 1
            s, l, c, k = group[0]
            cap = c or (l if k == 'diag' else None)
            out += ['', figure_html(s, l, cap, f'fig-{fig_n}'), '']
    return '\n'.join(out)


def quiz_from(section_html):
    """Converte a lista do simulado em questionário interativo."""
    soup = BeautifulSoup(section_html, 'html.parser')
    ol = soup.find('ol')
    gab = soup.find(string=re.compile('Gabarito'))
    if not ol or not gab:
        return section_html
    gp = gab.find_parent('p')
    key = dict(re.findall(r'(\d+)-([a-d])', gp.get_text()))
    qs = []
    for n, li in enumerate(ol.find_all('li', recursive=False), 1):
        t = li.get_text(' ', strip=True)
        parts = re.split(r'\(([a-d])\)\s*', t)
        q, opts = parts[0].strip(), [(parts[k], parts[k + 1].strip()) for k in range(1, len(parts) - 1, 2)]
        qs.append({'q': q, 'opts': opts, 'ans': key.get(str(n))})
    quiz = soup.new_tag('div', attrs={'class': 'quiz', 'data-quiz': json.dumps(qs, ensure_ascii=False)})
    ol.replace_with(quiz)
    gp.decompose()
    return str(soup)


body_md = transform(MD)
body_md = re.sub(r'^# .+\n', '', body_md, count=1)
body_md = re.sub(r'^Nov 22, 2026 · @Ventura\s*$', '', body_md, flags=re.M)
html_body = markdown.markdown(body_md, extensions=['tables', 'sane_lists'])

soup = BeautifulSoup(html_body, 'html.parser')
toc, chap = [], 0
for h in soup.find_all(['h2', 'h3']):
    txt = h.get_text()
    hid = slug(txt)[:60]
    h['id'] = hid
    if h.name == 'h2':
        chap += 1
        h.insert(0, BeautifulSoup(f'<span class="num">{chap:02d}</span>', 'html.parser'))
        toc.append({'id': hid, 't': txt, 'n': chap, 'sub': []})
    elif toc:
        toc[-1]['sub'].append({'id': hid, 't': txt})
for t in soup.find_all('table'):
    wrap = soup.new_tag('div', attrs={'class': 'table-wrap'})
    t.wrap(wrap)
for a in soup.find_all('a', href=True):
    if a['href'].startswith('http'):
        a['target'] = '_blank'; a['rel'] = 'noopener'
for h4 in soup.find_all('h4'):
    h4['class'] = 'kyo'

# seções
sections, cur = [], None
for el in list(soup.contents):
    if getattr(el, 'name', None) == 'h2':
        cur = {'id': el['id'], 'html': str(el)}
        sections.append(cur)
    elif cur is not None:
        cur['html'] += str(el)
# videoteca oficial (Kodokan × IJF Academy) antes de "Observações e limites"
from vidbuild import videoteca, add_video_buttons
from videos import VID, KANJI
_ill = {}
for s in sections:
    for li in BeautifulSoup(s['html'], 'html.parser').select('li.slide'):
        _ill.setdefault(li['data-name'].lower(), '#' + li['id'])
_pos = len(sections) - 1 if sections[-1]['id'].startswith('observacoes') else len(sections)
_vweb, _vprint = videoteca(_ill, _pos + 1)
sections.insert(_pos, {'id': 'videoteca-oficial', 'html': _vweb, 'vprint': _vprint})
toc.insert(_pos, {'id': 'videoteca-oficial', 't': 'Videoteca oficial: Kodokan × IJF Academy', 'n': _pos + 1,
                  'sub': [{'id': m, 't': t} for m, t in re.findall(r'<h3 id="([^"]+)">([^<]+)</h3>', _vweb)]})
for i, c in enumerate(toc):
    c['n'] = i + 1
for i, s in enumerate(sections):
    s['html'] = re.sub(r'<span class="num">\d+</span>', f'<span class="num">{i + 1:02d}</span>', s['html'], count=1)
    if 'vprint' in s:
        s['vprint'] = re.sub(r'<span class="num">\d+</span>', f'<span class="num">{i + 1:02d}</span>', s['vprint'], count=1)
N_VBTN = 0
for s in sections:
    s['print'] = s.pop('vprint', None) or add_video_buttons(s['html'], printable=True)[0]
    s['html'], k = add_video_buttons(s['html']); N_VBTN += k
for s in sections:
    if s['id'].startswith('simulado'):
        s['html'] = quiz_from(s['html'])

# ligações internas: glossário, técnicas, citações, referências e selos de IA
TECH = build_tech([s['html'] for s in sections])
for _k, (_n, _v) in VID.items():   # técnicas ilustradas ganham o vídeo; as demais apontam para a videoteca
    if _k in TECH:
        TECH[_k] = TECH[_k] + (_v,)
    else:
        TECH[_k] = ('#v-' + slug(_n), f'https://i.ytimg.com/vi/{_v}/mqdefault.jpg', _n, _v)
for _k in list(TECH):
    if len(TECH[_k]) == 3:
        TECH[_k] = TECH[_k] + ('',)
BIB, USES = Bib(), {}
titles = {c['id']: c['t'] for c in toc}
for s in sections:
    s['html'] = enrich_section(s['html'], s['id'], titles[s['id']], TECH, BIB, USES)
    s['print'] = enrich_section(s['print'], s['id'], titles[s['id']], TECH, Bib(), {}, printable=True)
N_FIGS = len(list((ROOT / 'dist' / 'assets' / 'img').glob('*.webp')))
EXTRA = [('glossario', 'Glossário', glossary_chapter(USES)),
         ('referencias', 'Referências', bib_chapter(BIB)),
         ('transparencia', 'Transparência sobre o uso de IA', transparency_chapter('novembro de 2026', N_FIGS))]

# índice remissivo: todas as figuras de carrossel + figuras únicas
index_entries = {}
for s in sections:
    sp = BeautifulSoup(s['html'], 'html.parser')
    for li in sp.select('li.slide'):
        index_entries[li['data-name']] = '#' + li['id']
for t, _ in KAE_ALL + PRO_ALL:
    index_entries.setdefault(t, '#t-' + slug(t))
for row_name in re.findall(r'^\| [^|]+ \| ([A-Z][a-z]+(?:-[a-z]+)+) \| (?:Ashi|Koshi|Te|Ma-|Yoko)', MD, re.M):
    index_entries.setdefault(row_name, '#' + slug('Fichas de estudo do Gokyo (40 técnicas)')[:60])
idx = sorted(index_entries.items(), key=lambda kv: slug(kv[0]))

INDEX_HTML = '<section id="indice-remissivo" class="chapter"><h2><span class="num">★</span>Índice de técnicas</h2>' \
             '<p>Toque no nome para ir direto à ilustração.</p><div class="idx-letters">'
by_letter = {}
for name, href in idx:
    by_letter.setdefault(slug(name)[0].upper(), []).append((name, href))
for L in sorted(by_letter):
    INDEX_HTML += f'<div class="idx-group"><h3 class="idx-l">{L}</h3><ul>' + ''.join(
        f'<li><a href="{h}" data-jump>{html.escape(n)}</a></li>' for n, h in by_letter[L]) + '</ul></div>'
INDEX_HTML += '</div></section>'


def toc_html(cls):
    o = f'<ol class="{cls}">'
    for c in toc:
        o += f'<li><a href="#{c["id"]}"><span class="tn">{c["n"]:02d}</span>{html.escape(c["t"])}</a>'
        if c['sub']:
            o += '<ol>' + ''.join(f'<li><a href="#{s["id"]}">{html.escape(s["t"])}</a></li>' for s in c['sub']) + '</ol>'
        o += '</li>'
    return o + ('<li><a href="#indice-remissivo"><span class="tn">★</span>Índice de técnicas</a></li>'
                '<li><a href="#glossario"><span class="tn">文</span>Glossário</a></li>'
                '<li><a href="#referencias"><span class="tn">📚</span>Referências</a></li>'
                '<li><a href="#transparencia"><span class="tn">🤖</span>Transparência sobre o uso de IA</a></li></ol>')


SEARCH_DATA = json.dumps([{'t': n, 'h': h} for n, h in idx] +
                         [{'t': c['t'], 'h': '#' + c['id']} for c in toc] +
                         [{'t': s['t'], 'h': '#' + s['id']} for c in toc for s in c['sub']] +
                         [{'t': d['t'] + ' (glossário)', 'h': '#' + g} for g, d in GLOSS_DATA.items()] +
                         [{'t': it['text'][:90] + '…', 'h': '#' + it['id'], 'k': 'ref'} for it in BIB.items.values()],
                         ensure_ascii=False)
REFS_JSON = json.dumps({it['id']: it['html'] for it in BIB.items.values()}, ensure_ascii=False)
GLOSS_JSON = json.dumps(GLOSS_DATA, ensure_ascii=False)

# páginas do livro, na ordem, para os botões anterior/próximo
PAGES = [('inicio', 'Capa'), ('sumario', 'Sumário')] + [(c['id'], c['t']) for c in toc] + \
        [('indice-remissivo', 'Índice de técnicas')] + [(a, t) for a, t, _ in EXTRA]


def pager(i):
    prv = PAGES[i - 1] if i > 0 else None
    nxt = PAGES[i + 1] if i + 1 < len(PAGES) else None
    a = f'<a class="pg-prev" href="#{prv[0]}" rel="prev"><small>‹ Anterior</small>{html.escape(prv[1])}</a>' if prv else '<span></span>'
    b = f'<a class="pg-next" href="#{nxt[0]}" rel="next"><small>Próximo ›</small>{html.escape(nxt[1])}</a>' if nxt else '<span></span>'
    return f'<nav class="pager" aria-label="Navegação entre capítulos">{a}{b}</nav>'


def with_pager(sec_html, pid):
    i = [p for p, _ in PAGES].index(pid)
    head, _, tail = sec_html.rpartition('</section>')
    return head + pager(i) + '</section>' + tail


chapters = ''.join(with_pager(f'<section class="chapter" id="sec-{s["id"]}">{s["html"]}</section>', s['id']) for s in sections)
chapters_print = ''.join(f'<section class="chapter" id="sec-{s["id"]}">{s["print"]}</section>' for s in sections)
INDEX_HTML = with_pager(INDEX_HTML, 'indice-remissivo')
EXTRA_HTML = ''.join(with_pager(h, a) for a, _, h in EXTRA)
EXTRA_PRINT = ''.join(h for _, _, h in EXTRA)
AI_JSONLD = json.dumps({
    '@context': 'https://schema.org', '@type': 'Book', 'name': TITLE, 'inLanguage': 'pt-BR',
    'dateModified': '2026-11-22', 'author': {'@type': 'Person', 'name': 'Ventura'},
    'contributor': {'@type': 'SoftwareApplication', 'name': MODEL, 'applicationCategory': 'Large language model',
                    'creator': {'@type': 'Organization', 'name': VENDOR}},
    'creativeWorkStatus': 'AI-assisted',
    'description': f'Texto, ilustrações (via código Python) e site gerados com IA ({MODEL}, {VENDOR}) a partir de fontes oficiais citadas.',
    'citation': [re.sub('<[^>]+>', '', it['html']) for it in BIB.items.values()],
}, ensure_ascii=False)
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'ai-disclosure.json').write_text(json.dumps({
    'work': TITLE, 'date': '2026-11-22', 'human': 'Ventura (concepção e decisões editoriais)',
    'ai_model': MODEL, 'ai_provider': VENDOR,
    'ai_generated': {'text': True, 'glossary': True, 'quiz': True, 'diagrams': True,
                     'illustrations': 'imagens desenhadas por código Python escrito pelo modelo (IPTC digitalSourceType: algorithmicMedia)',
                     'site_code': True},
    'basis': 'Fontes oficiais listadas em Referências (CBJ, IJF/Kodokan, federações estaduais)',
    'disclosure_basis': 'Regulamento (UE) 2024/1689, art. 50',
}, ensure_ascii=False, indent=2), encoding='utf-8')
css = (ROOT / 'src' / 'style.css').read_text(encoding='utf-8')
js = (ROOT / 'src' / 'app.js').read_text(encoding='utf-8')

PAGE = f'''<!DOCTYPE html>
<html lang="pt-BR" data-theme="auto" data-layout="auto" data-book>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{SUB}. Técnicas do Gokyo em três fases, programa de cada faixa, combinações, contragolpes e técnicas proibidas.">
<meta name="theme-color" content="#0f3d8c">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<script src="assets/prefs.js"></script>
<meta name="author" content="Ventura">
<meta name="generator" content="{MODEL} ({VENDOR}) — texto, ilustrações por código e site gerados com IA">
<meta name="ai-disclosure" content="ai-assisted; model={MODEL}; provider={VENDOR}; details=ai-disclosure.json">
<link rel="alternate" type="application/json" href="ai-disclosure.json" title="Declaração de uso de IA">
<script type="application/ld+json">{AI_JSONLD}</script>
<link rel="stylesheet" href="assets/style.css">
<script>try{{var t=localStorage.getItem('jt-theme'),l=localStorage.getItem('jt-layout');if(t)document.documentElement.dataset.theme=t;if(l)document.documentElement.dataset.layout=l}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="top">
  <button class="menu-btn" aria-label="Abrir sumário" aria-controls="drawer" aria-expanded="false">☰</button>
  <a class="brand" href="#inicio"><span class="belt"></span>Judô · exames de faixa</a>
  <nav class="portal" aria-label="Portal"><a href="./">Início</a><a href="explorar/#/judo">Explorar Judô</a><a href="explorar/#/jiu-jitsu">Jiu-Jitsu</a></nav>
  <div class="search"><input type="search" id="q" class="js-search" placeholder="Buscar no livro (técnica, termo, regra)" aria-label="Buscar no livro"><ul class="results" role="listbox"></ul></div>
  <div class="prefs">
    <div class="seg" role="group" aria-label="Layout">
      <button data-layout-set="auto" title="Ajustar à tela">Auto</button><button data-layout-set="desktop" title="Design para computador">PC</button><button data-layout-set="mobile" title="Design para celular">Celular</button>
    </div>
    <div class="seg" role="group" aria-label="Tema">
      <button data-theme-set="auto" title="Seguir o sistema">◐</button><button data-theme-set="light" title="Modo claro">☀</button><button data-theme-set="dark" title="Modo escuro">☾</button>
    </div>
    <div class="seg" role="group" aria-label="Idioma"><button data-lang-set="pt">PT-BR</button><button data-lang-set="en">EN</button></div>
    <a class="pdf" href="judo-tecnicas-e-exames-de-faixa.pdf" download>PDF</a>
  </div>
</header>
<div class="layout">
  <nav id="drawer" class="side" aria-label="Sumário">
    <div class="side-tools">
      <div class="search side-search"><input type="search" class="js-search" placeholder="Buscar no livro" aria-label="Buscar no livro"><ul class="results" role="listbox"></ul></div>
      <div class="quick"><a href="#indice-remissivo">★ Técnicas</a><a href="#glossario">文 Glossário</a><a href="#referencias">📚 Fontes</a><a href="#transparencia">🤖 IA</a></div>
      <div class="side-prefs">
        <div class="seg" role="group" aria-label="Layout"><button data-layout-set="auto">Auto</button><button data-layout-set="desktop">PC</button><button data-layout-set="mobile">Celular</button></div>
        <div class="seg" role="group" aria-label="Tema"><button data-theme-set="auto" title="Seguir o sistema">◐</button><button data-theme-set="light" title="Modo claro">☀</button><button data-theme-set="dark" title="Modo escuro">☾</button></div>
        <div class="seg" role="group" aria-label="Idioma"><button data-lang-set="pt">PT-BR</button><button data-lang-set="en">EN</button></div>
      </div>
    </div>
    <p class="side-h">Sumário</p>
    {toc_html('toc')}
  </nav>
  <div class="scrim" hidden></div>
  <main id="conteudo">
    <section class="hero" id="inicio">
      <p class="eyebrow">Material de estudo · atualizado em 22/11/2026</p>
      <h1>{TITLE}</h1>
      <p class="lede">{SUB}: as 40 técnicas do Gokyo em kuzushi, tsukuri e kake, o programa de cada faixa até a preta, combinações, contragolpes e o que é proibido em competição.</p>
      <div class="hero-cta"><a class="btn" href="#sumario">Ver sumário</a><a class="btn ghost" href="#indice-remissivo">Índice de técnicas</a><a class="btn ghost" href="judo-tecnicas-e-exames-de-faixa.pdf" download>Baixar PDF</a></div>
      <p class="credit">Organização: Ventura · <a href="#transparencia">🤖 Texto, ilustrações e site gerados com IA ({MODEL}, {VENDOR})</a> · <a href="#referencias">📚 Fontes oficiais citadas</a></p>
      <div class="hero-strip"><img src="assets/img/faixas.webp" alt="Cores das faixas da CBJ" loading="eager"></div>
      {pager(0)}
    </section>
    <section class="chapter" id="sumario">
      <h2><span class="num">00</span>Sumário</h2>
      {toc_html('toc big')}
      {pager(1)}
    </section>
    {chapters}
    {INDEX_HTML}
    {EXTRA_HTML}
    <footer class="foot"><p>Conteúdo baseado nos regulamentos da CBJ, das federações estaduais e nas regras e classificação da IJF/Kodokan (ver <a href="#referencias">Referências</a>); confira sempre a versão vigente com a sua federação. Texto, ilustrações (por código Python) e site gerados com IA: {MODEL}, {VENDOR}, nov. 2026 — <a href="#transparencia">detalhes</a>.</p></footer>
  </main>
</div>
<nav class="bottom" aria-label="Navegação rápida">
  <button data-act="menu">☰<span>Sumário</span></button><button data-act="search">⌕<span>Buscar</span></button><button data-act="prev">‹<span>Anterior</span></button><button data-act="next">›<span>Próximo</span></button><button data-act="theme">◐<span>Tema</span></button>
</nav>
<dialog class="lightbox" aria-label="Imagem ampliada"><button class="lb-close" aria-label="Fechar">✕</button><div class="lb-stage"><img alt=""></div></dialog>
<div class="pop" role="tooltip" hidden></div>
<script>window.SEARCH={SEARCH_DATA};window.GLOSS={GLOSS_JSON};window.REFS={REFS_JSON};</script>
<script src="assets/i18n.js" data-dict="assets/i18n-livro.js"></script>
<script src="assets/app.js" defer></script>
</body>
</html>'''
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'livro.html').write_text(PAGE, encoding='utf-8')  # a página inicial (index.html) é o portal: source/portal
(ROOT / 'dist' / 'assets').mkdir(exist_ok=True)
(ROOT / 'dist' / 'assets' / 'style.css').write_text(css, encoding='utf-8')
(ROOT / 'dist' / 'assets' / 'app.js').write_text(js, encoding='utf-8')

# --------------------------------------------------------------- versão de impressão
PRINT = PAGE.replace(chapters, chapters_print).replace(EXTRA_HTML, EXTRA_PRINT).replace(INDEX_HTML, re.sub(r'<nav class="pager".*?</nav>', '', INDEX_HTML)).replace('<link rel="stylesheet" href="assets/style.css">',
                     '<link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/print.css">')
PRINT = PRINT.replace('data-theme="auto" data-layout="auto"', 'data-theme="light" data-layout="desktop" class="print"')
PRINT = re.sub(r'assets/(img|diag)/([a-z0-9_]+)\.webp', r'assets/print/\2.jpg', PRINT)
PRINT = re.sub(r'<script>try\{.*?</script>', '', PRINT, flags=re.S)
PRINT = re.sub(r'<script>window\.SEARCH=.*?</script>', '', PRINT, flags=re.S)
PRINT = PRINT.replace('<script src="assets/app.js" defer></script>', '').replace('<script src="assets/i18n.js" data-dict="assets/i18n-livro.js"></script>', '').replace('<script src="assets/prefs.js"></script>', '')
(ROOT / 'dist' / 'print.html').write_text(PRINT, encoding='utf-8')
(ROOT / 'dist' / 'assets' / 'print.css').write_text((ROOT / 'src' / 'print.css').read_text(encoding='utf-8'), encoding='utf-8')
print('ok', len(sections), 'capítulos', len(idx), 'entradas no índice', N_VBTN, 'ilustrações com vídeo')
