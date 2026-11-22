"""
build.py — gera o site (index.html) e a versão de impressão (print.html → PDF)
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
for s in sections:
    s['print'] = s['html']
for s in sections:
    if s['id'].startswith('simulado'):
        s['html'] = quiz_from(s['html'])
    # botão "voltar ao sumário" ao fim de cada capítulo
    s['html'] += '<p class="back"><a href="#sumario">↑ Voltar ao sumário</a></p>'

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
INDEX_HTML += '</div><p class="back"><a href="#sumario">↑ Voltar ao sumário</a></p></section>'


def toc_html(cls):
    o = f'<ol class="{cls}">'
    for c in toc:
        o += f'<li><a href="#{c["id"]}"><span class="tn">{c["n"]:02d}</span>{html.escape(c["t"])}</a>'
        if c['sub']:
            o += '<ol>' + ''.join(f'<li><a href="#{s["id"]}">{html.escape(s["t"])}</a></li>' for s in c['sub']) + '</ol>'
        o += '</li>'
    return o + '<li><a href="#indice-remissivo"><span class="tn">★</span>Índice de técnicas</a></li></ol>'


SEARCH_DATA = json.dumps([{'t': n, 'h': h} for n, h in idx] +
                         [{'t': c['t'], 'h': '#' + c['id']} for c in toc] +
                         [{'t': s['t'], 'h': '#' + s['id']} for c in toc for s in c['sub']], ensure_ascii=False)

chapters = ''.join(f'<section class="chapter">{s["html"]}</section>' for s in sections)
chapters_print = ''.join(f'<section class="chapter">{s["print"]}</section>' for s in sections)
css = (ROOT / 'src' / 'style.css').read_text(encoding='utf-8')
js = (ROOT / 'src' / 'app.js').read_text(encoding='utf-8')

PAGE = f'''<!DOCTYPE html>
<html lang="pt-BR" data-theme="auto" data-layout="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{SUB}. Técnicas do Gokyo em três fases, programa de cada faixa, combinações, contragolpes e técnicas proibidas.">
<meta name="theme-color" content="#0f3d8c">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
<script>try{{var t=localStorage.getItem('jt-theme'),l=localStorage.getItem('jt-layout');if(t)document.documentElement.dataset.theme=t;if(l)document.documentElement.dataset.layout=l}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="top">
  <button class="menu-btn" aria-label="Abrir sumário" aria-controls="drawer" aria-expanded="false">☰</button>
  <a class="brand" href="#inicio"><span class="belt"></span>Judô · exames de faixa</a>
  <div class="search"><input type="search" id="q" placeholder="Buscar técnica ou capítulo" aria-label="Buscar"><ul class="results" role="listbox"></ul></div>
  <div class="prefs">
    <div class="seg" role="group" aria-label="Layout">
      <button data-layout-set="auto" title="Ajustar à tela">Auto</button><button data-layout-set="desktop" title="Design para computador">PC</button><button data-layout-set="mobile" title="Design para celular">Celular</button>
    </div>
    <div class="seg" role="group" aria-label="Tema">
      <button data-theme-set="auto" title="Seguir o sistema">◐</button><button data-theme-set="light" title="Modo claro">☀</button><button data-theme-set="dark" title="Modo escuro">☾</button>
    </div>
    <a class="pdf" href="judo-tecnicas-e-exames-de-faixa.pdf" download>PDF</a>
  </div>
</header>
<div class="layout">
  <nav id="drawer" class="side" aria-label="Sumário">
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
      <div class="hero-strip"><img src="assets/img/faixas.webp" alt="Cores das faixas da CBJ" loading="eager"></div>
    </section>
    <section class="chapter" id="sumario">
      <h2><span class="num">00</span>Sumário</h2>
      {toc_html('toc big')}
    </section>
    {chapters}
    {INDEX_HTML}
    <footer class="foot"><p>Ilustrações originais geradas por código (Python). Conteúdo baseado nos regulamentos da CBJ, das federações estaduais e nas regras e classificação da IJF/Kodokan; confira sempre a versão vigente com a sua federação.</p></footer>
  </main>
</div>
<nav class="bottom" aria-label="Navegação rápida">
  <button data-act="menu">☰<span>Sumário</span></button><button data-act="search">⌕<span>Buscar</span></button><button data-act="theme">◐<span>Tema</span></button><button data-act="top">↑<span>Topo</span></button>
</nav>
<dialog class="lightbox" aria-label="Imagem ampliada"><button class="lb-close" aria-label="Fechar">✕</button><div class="lb-stage"><img alt=""></div></dialog>
<script>window.SEARCH={SEARCH_DATA};</script>
<script src="assets/app.js" defer></script>
</body>
</html>'''
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'index.html').write_text(PAGE, encoding='utf-8')
(ROOT / 'dist' / 'assets').mkdir(exist_ok=True)
(ROOT / 'dist' / 'assets' / 'style.css').write_text(css, encoding='utf-8')
(ROOT / 'dist' / 'assets' / 'app.js').write_text(js, encoding='utf-8')

# --------------------------------------------------------------- versão de impressão
PRINT = PAGE.replace(chapters, chapters_print).replace('<link rel="stylesheet" href="assets/style.css">',
                     '<link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/print.css">')
PRINT = PRINT.replace('data-theme="auto" data-layout="auto"', 'data-theme="light" data-layout="desktop" class="print"')
PRINT = re.sub(r'assets/(img|diag)/([a-z0-9_]+)\.webp', r'assets/print/\2.jpg', PRINT)
PRINT = re.sub(r'<script>try\{.*?</script>', '', PRINT, flags=re.S)
PRINT = PRINT.replace('<script src="assets/app.js" defer></script>', '')
(ROOT / 'dist' / 'print.html').write_text(PRINT, encoding='utf-8')
(ROOT / 'dist' / 'assets' / 'print.css').write_text((ROOT / 'src' / 'print.css').read_text(encoding='utf-8'), encoding='utf-8')
print('ok', len(sections), 'capítulos', len(idx), 'entradas no índice')
