"""enrich.py — liga o texto do livro: glossário, técnicas (com miniatura),
citações (autor, ano) e referências ABNT; acrescenta os selos de uso de IA."""
import re, html, unicodedata
from bs4 import BeautifulSoup, NavigableString
from glossary import GLOSSARY

MODEL = 'Claude Opus 5.5'
VENDOR = 'Anthropic'
AI_TEXT = f'Texto redigido com IA ({MODEL}, {VENDOR}) a partir das fontes citadas'
AI_FIG = f'Ilustração original: código Python escrito por IA ({MODEL})'
AI_DIAG = f'Diagrama gerado com IA ({MODEL})'

SKIP = {'a', 'h1', 'h2', 'h3', 'h4', 'button', 'script', 'style', 'figcaption', 'code', 'th'}


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


# ------------------------------------------------------------------ glossário
GLOSS = {}          # chave normalizada → id do termo
GLOSS_DATA = {}     # id → {t, jp, d}
for term, jp, d, alts in GLOSSARY:
    gid = 'g-' + slug(term)
    GLOSS_DATA[gid] = {'t': term, 'jp': jp or '', 'd': d}
    for k in [term] + alts:
        GLOSS[k.lower()] = gid


def build_tech(sections_html):
    """Técnicas com ilustração própria: nome → (âncora, imagem)."""
    tech = {}
    for h in sections_html:
        sp = BeautifulSoup(h, 'html.parser')
        for li in sp.select('li.slide'):
            name = li['data-name']
            if re.fullmatch(r'[A-Z][a-z]+(?:-[a-z]+)+', name):
                tech.setdefault(name.lower(), ('#' + li['id'], li.img['src'], name))
    return tech


def term_regex(keys):
    keys = sorted(keys, key=len, reverse=True)
    return re.compile(r'(?<![\w-])(' + '|'.join(re.escape(k) for k in keys) + r')(?![\w-])', re.I)


# ------------------------------------------------------------------ referências
AUTH = {'IJF': 'INTERNATIONAL JUDO FEDERATION', 'CBJ': 'CONFEDERAÇÃO BRASILEIRA DE JUDÔ',
        'FPJudô': 'FEDERAÇÃO PAULISTA DE JUDÔ', 'FJERJ': 'FEDERAÇÃO DE JUDÔ DO ESTADO DO RIO DE JANEIRO'}
LOC = re.compile(r'\s*Art\.\s.*?\.(?=\s+(?:Disponível|Acesso)|\s*$)')


def ref_key(text):
    t = LOC.sub('', text)
    t = t.split(' Disponível em')[0]
    return re.sub(r'\s+', ' ', t).strip().lower()


class Bib:
    def __init__(self):
        self.items = {}   # key → dict(id, html, text, cited=[(chap_id, chap_title)])

    def add(self, p, chap):
        text = p.get_text(' ', strip=True)
        key = ref_key(text)
        if key not in self.items:
            inner = LOC.sub('', p.decode_contents())
            self.items[key] = {'id': f'ref-{len(self.items) + 1}', 'html': inner, 'text': text, 'cited': []}
        it = self.items[key]
        if chap not in it['cited']:
            it['cited'].append(chap)
        return it

    def find(self, author, year):
        a = AUTH.get(author, author).upper()
        for it in self.items.values():
            if it['text'].upper().startswith(a) and year in it['text']:
                return it
        return None


def enrich_section(sec_html, chap_id, chap_title, tech, bib, uses, printable=False):
    soup = BeautifulSoup(sec_html, 'html.parser')
    keys = list(GLOSS) + list(tech)
    rx = term_regex(keys)
    seen = set()

    # 1) referências do capítulo → ids, lista ABNT estilizada
    nrefs = 0
    for strong in soup.find_all('strong'):
        if strong.get_text(strip=True) == 'Referências' and strong.parent.name == 'p':
            head = strong.parent
            head['class'] = 'refs-h'
            head['id'] = 'refs-' + chap_id
            sib = head.find_next_sibling()
            while sib is not None and sib.name == 'p' and 'back' not in (sib.get('class') or []):
                it = bib.add(sib, (chap_id, chap_title))
                sib['class'] = 'ref'
                sib['data-ref'] = it['id']
                nrefs += 1
                sib = sib.find_next_sibling()

    # 2) termos e técnicas no texto corrido
    def walk(node):
        for child in list(node.children):
            if isinstance(child, NavigableString):
                if child.parent.name in SKIP or type(child).__name__ != 'NavigableString':
                    continue
                s = str(child)
                if not rx.search(s):
                    continue
                parts, last = [], 0
                for m in rx.finditer(s):
                    k = m.group(1).lower()
                    target = GLOSS.get(k) or ('T:' + k)
                    if target in seen:
                        continue
                    seen.add(target)
                    parts.append(html.escape(s[last:m.start()]))
                    word = html.escape(m.group(1))
                    if target.startswith('T:'):
                        href, img, name = tech[k]
                        parts.append(f'<a class="tech" href="{href}" data-img="{img}" data-name="{html.escape(name)}">{word}</a>')
                    else:
                        uid = f'u-{target[2:]}-{chap_id}'
                        uses.setdefault(target, []).append((uid, chap_title))
                        parts.append(f'<a class="term" id="{uid}" href="#{target}" data-g="{target}">{word}</a>')
                    last = m.end()
                if last:
                    parts.append(html.escape(s[last:]))
                    child.replace_with(BeautifulSoup(''.join(parts), 'html.parser'))
            elif getattr(child, 'name', None) and child.name not in SKIP and 'ref' not in (child.get('class') or []) \
                    and 'carousel' not in (child.get('class') or []) and 'quiz' not in (child.get('class') or []):
                walk(child)
    walk(soup)

    # 3) citações (AUTOR, ano) → link à referência com prévia
    cit = re.compile(r'\((IJF|CBJ|FPJudô|FJERJ), (\d{4})\)')
    for s in list(soup.find_all(string=cit)):
        if s.parent.name == 'a':
            continue
        def rep(m):
            it = bib.find(m.group(1), m.group(2))
            if not it:
                return html.escape(m.group(0))
            return f'(<a class="cite" href="#{it["id"]}" data-ref="{it["id"]}">{m.group(1)}, {m.group(2)}</a>)'
        s.replace_with(BeautifulSoup(cit.sub(rep, html.escape(str(s))), 'html.parser'))

    # 4) selos de IA nas figuras
    for fc in soup.find_all('figcaption'):
        fig = fc.find_parent('figure')
        src = fig.img['src'] if fig and fig.img else ''
        label = AI_DIAG if '/diag/' in src else AI_FIG
        fc.append(BeautifulSoup(f' <span class="ai-chip" title="{label}" data-ai="{label}">IA</span>', 'html.parser'))
    for img in soup.find_all('img'):
        img['data-ai-source'] = 'algorithmicMedia' if '/diag/' not in img['src'] else 'trainedAlgorithmicMedia'

    # 5) barra do capítulo: fontes + IA
    h2 = soup.find('h2')
    if h2:
        refs_btn = (f'<a class="meta-chip refs-chip" href="#refs-{chap_id}">📚 {nrefs} referência{"s" if nrefs != 1 else ""}</a>'
                    if nrefs else '<a class="meta-chip refs-chip" href="#referencias">📚 Referências</a>')
        bar = (f'<div class="meta-bar">{refs_btn}'
               f'<a class="meta-chip ai-tag" href="#transparencia" data-ai="{AI_TEXT}">🤖 {AI_TEXT}</a></div>')
        h2.insert_after(BeautifulSoup(bar, 'html.parser'))
    return str(soup)


def bib_chapter(bib):
    items = sorted(bib.items.values(), key=lambda it: slug(it['text']))
    o = ['<section class="chapter" id="sec-referencias"><h2 id="referencias"><span class="num">📚</span>Referências</h2>',
         '<p>Todas as fontes citadas no livro, em ordem alfabética, no formato da ABNT NBR 6023:2018. '
         'Em cada item, “citada em” leva ao capítulo que a usa. Os artigos e páginas específicos de cada '
         'regulamento aparecem na lista do próprio capítulo.</p><ol class="biblio">']
    for it in items:
        where = ' · '.join(f'<a href="#refs-{cid}">{html.escape(t)}</a>' for cid, t in it['cited'])
        o.append(f'<li id="{it["id"]}"><p>{it["html"]}</p><p class="cited">Citada em: {where}</p></li>')
    o.append('</ol></section>')
    return ''.join(o)


def glossary_chapter(uses):
    items = sorted(GLOSS_DATA.items(), key=lambda kv: slug(kv[1]['t']))
    o = ['<section class="chapter" id="sec-glossario"><h2 id="glossario"><span class="num">文</span>Glossário</h2>',
         f'<div class="meta-bar"><a class="meta-chip ai-tag" href="#transparencia" data-ai="Definições redigidas por IA ({MODEL}, {VENDOR}) a partir das fontes do livro">'
         f'🤖 Definições redigidas por IA ({MODEL}, {VENDOR}) a partir das fontes do livro</a></div>',
         '<p>Os termos sublinhados com pontilhado no texto abrem esta definição ao toque. '
         '“Aparece em” leva ao ponto exato do capítulo.</p><dl class="gloss">']
    for gid, d in items:
        jp = f' <span class="jp" lang="ja">{d["jp"]}</span>' if d['jp'] else ''
        where = uses.get(gid, [])
        w = (' · '.join(f'<a href="#{uid}">{html.escape(t)}</a>' for uid, t in where)) if where else ''
        o.append(f'<dt id="{gid}">{html.escape(d["t"])}{jp}</dt><dd><p>{html.escape(d["d"])}</p>'
                 + (f'<p class="cited">Aparece em: {w}</p>' if w else '') + '</dd>')
    o.append('</dl></section>')
    return ''.join(o)


def transparency_chapter(date_pt, n_figs):
    rows = [
        ('Pesquisa e seleção das fontes oficiais', 'IA, com buscas na web', f'{MODEL} ({VENDOR})', 'Fontes listadas em cada capítulo e em Referências'),
        ('Redação do texto dos capítulos', 'IA', f'{MODEL} ({VENDOR})', 'Escrito a partir dos regulamentos citados; pedidos e orientação editorial de Ventura'),
        (f'{n_figs} ilustrações das técnicas', 'Código Python escrito por IA, desenhado por computador', f'{MODEL} ({VENDOR})', 'Poses conferidas com as descrições textuais da IJF/Kodokan; não são fotos nem cópias de imagens de terceiros'),
        ('Diagramas (fluxos e esquemas)', 'IA', f'{MODEL} ({VENDOR})', 'Resumem regras dos regulamentos citados'),
        ('Glossário e questões do simulado', 'IA', f'{MODEL} ({VENDOR})', 'Baseados nas fontes do livro'),
        ('Site, PDF e ligações entre termos', 'Código escrito por IA', f'{MODEL} ({VENDOR})', 'HTML, CSS e JavaScript próprios, sem serviços externos'),
        ('Concepção, escopo e decisões editoriais', 'Pessoa', 'Ventura', 'Definiu o que o material devia cobrir e como seria publicado'),
    ]
    t = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    return (f'<section class="chapter" id="sec-transparencia"><h2 id="transparencia"><span class="num">🤖</span>Transparência sobre o uso de IA</h2>'
            f'<p>Este livro foi produzido com inteligência artificial. O modelo usado foi o <strong>{MODEL}</strong>, da {VENDOR}, '
            f'em {date_pt}. A tabela mostra o que a IA fez e o que foi decidido por uma pessoa.</p>'
            '<div class="table-wrap"><table><thead><tr><th>Parte</th><th>Como foi feita</th><th>Quem / modelo</th><th>Base e observações</th></tr></thead>'
            f'<tbody>{t}</tbody></table></div>'
            '<h3 id="como-identificar">Como identificar o que foi gerado por IA</h3><ul>'
            '<li><strong>No texto:</strong> a faixa 🤖 no início de cada capítulo.</li>'
            '<li><strong>Nas figuras:</strong> o selo <span class="ai-chip">IA</span> na legenda.</li>'
            '<li><strong>Para máquinas:</strong> metadados no código da página (JSON-LD do schema.org com o modelo usado, e o tipo de origem IPTC em cada imagem) e o arquivo <a href="ai-disclosure.json">ai-disclosure.json</a>.</li></ul>'
            '<h3 id="limites-da-ia">Limites e cuidados</h3><ul>'
            '<li>Textos gerados por IA podem conter erros. Cada afirmação tem a fonte indicada; antes de uso oficial, confira no regulamento vigente da sua federação.</li>'
            '<li>Recomenda-se a revisão por um professor faixa-preta antes de usar o material em aula ou banca.</li>'
            '<li>As ilustrações são esquemas didáticos. A referência visual oficial de cada técnica está nos vídeos do Kodokan e da IJF Judo Academy.</li></ul>'
            '<p class="cited">Base para esta rotulagem: Regulamento (UE) 2024/1689 (AI Act), art. 50, e boas práticas de rotulagem em duas camadas (visível e legível por máquina).</p>'
            '</section>')
