"""Monta a Videoteca oficial e os botões de vídeo nas ilustrações."""
import re, html
from bs4 import BeautifulSoup
from videos import GROUPS, EXTRAS, VID, KANJI, KODOKAN_CHANNEL, ijf_url, KODOMO, KODOMO_PLAYLIST, COMBO_UNIT
from enrich import slug

NAMES_RX = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(k) for k in sorted(VID, key=len, reverse=True)) + r')(?![\w-])', re.I)


def yt(v):
    return f'https://www.youtube.com/watch?v={v}'


def techniques_in(text, limit=2):
    out = []
    for m in NAMES_RX.finditer(text):
        n, v = VID[m.group(1).lower()]
        if (n, v) not in out:
            out.append((n, v))
    return out[:limit]


def add_video_buttons(sec_html, printable=False):
    soup = BeautifulSoup(sec_html, 'html.parser')
    n = 0
    for li in soup.select('li.slide'):
        name = li.get('data-name', '')
        hits = [VID[name.lower()]] if name.lower() in VID else techniques_in(name)
        if '→' in name and hits:
            unit = COMBO_UNIT.get(hits[0][0].lower())
            if unit:
                hits = hits + [(f'Combinação oficial — Kodomo-no-kata {unit}', KODOMO[unit][0])]
        if not hits:
            continue
        fig = li.figure
        if printable:
            links = ' · '.join(f'{html.escape(t)}: <a href="{yt(v)}">youtu.be/{v}</a>' for t, v in hits)
            fig.append(BeautifulSoup(f'<p class="vlink">▶ Vídeo oficial (Kodokan × IJF Academy) — {links}</p>', 'html.parser'))
        else:
            btns = ''.join(f'<button type="button" class="vbtn" data-yt="{v}" data-title="{html.escape(t)}">▶ Vídeo oficial: {html.escape(t)}</button>' for t, v in hits)
            fig.append(BeautifulSoup(f'<div class="vrow">{btns}</div><div class="vslot"></div>', 'html.parser'))
        n += 1
    return str(soup), n


def card(name, kanji, v, ill_href=None, extra=False):
    vid_id = 'v-' + slug(name)
    links = []
    if ill_href:
        links.append(f'<a href="{ill_href}">Ilustração</a>')
    if not extra:
        links.append(f'<a href="{ijf_url(name)}" target="_blank" rel="noopener">IJF</a>')
    links.append(f'<a href="{yt(v)}" target="_blank" rel="noopener">YouTube ↗</a>')
    return (f'<li class="vcard" id="{vid_id}"><button type="button" class="vthumb" data-yt="{v}" data-title="{html.escape(name)}" aria-label="Assistir: {html.escape(name)}">'
            f'<img src="https://i.ytimg.com/vi/{v}/mqdefault.jpg" alt="" loading="lazy" decoding="async"><span class="play">▶</span></button>'
            f'<div class="vmeta"><b>{html.escape(name)}</b> <span class="jp" lang="ja">{html.escape(kanji)}</span>'
            f'<span class="vlinks">{" · ".join(links)}</span></div></li>')


REFS = '''<p><strong>Referências</strong></p>
<p>KODOKAN; IJF ACADEMY. <strong>KODOKAN × IJF ACADEMY 100 Techniques</strong>. Tóquio: Kodokan, 2020. Série de 100 vídeos. Disponível em: <a href="https://www.youtube.com/@KODOKANJUDO" target="_blank" rel="noopener">youtube.com/@KODOKANJUDO</a>. Acesso em: 22 nov. 2026.</p>
<p>KODOKAN; INTERNATIONAL JUDO FEDERATION; FÉDÉRATION FRANÇAISE DE JUDO. <strong>Kodomo-no-kata</strong>. Tóquio: Kodokan, 2020. 8 vídeos. Disponível em: <a href="https://www.youtube.com/playlist?list=PLtz539PTepc30cdknyAOAJhdVR2ZoWiC3" target="_blank" rel="noopener">youtube.com/playlist?list=PLtz539PTepc30cdknyAOAJhdVR2ZoWiC3</a>. Acesso em: 22 nov. 2026.</p>
<p>KODOKAN. <strong>講道館柔道「技」/ Kodokan judo “Waza”</strong>. Tóquio: Kodokan, 2021-2025. Série de vídeos. Disponível em: <a href="https://www.youtube.com/@KODOKANJUDO" target="_blank" rel="noopener">youtube.com/@KODOKANJUDO</a>. Acesso em: 22 nov. 2026.</p>
<p>INTERNATIONAL JUDO FEDERATION. <strong>Judo techniques</strong>. [S. l.]: IJF, [s. d.]. Disponível em: <a href="https://judo.ijf.org" target="_blank" rel="noopener">judo.ijf.org</a>. Acesso em: 22 nov. 2026.</p>'''


def videoteca(ill, num):
    """ill: nome em minúsculas → âncora da ilustração no livro."""
    total = sum(len(i) for _, _, i in GROUPS)
    intro = (f'<h2 id="videoteca-oficial"><span class="num">{num:02d}</span>Videoteca oficial: Kodokan × IJF Academy</h2>'
             f'<p>Os {total} vídeos abaixo são a série oficial <strong>“100 Techniques”</strong>, produzida pelo Kodokan com a IJF Academy e publicada no '
             f'<a href="{KODOKAN_CHANNEL}" target="_blank" rel="noopener">canal oficial do Kodokan no YouTube</a>. Cada vídeo mostra uma das 68 projeções ou '
             'dos 32 katame-waza da classificação oficial. Toque na miniatura para assistir aqui mesmo, sem sair do livro. '
             'Os mesmos vídeos também abrem pelos botões “▶ Vídeo oficial” das ilustrações e nas prévias das técnicas.</p>'
             '<p><strong>Combinações e contragolpes:</strong> não há série oficial com um vídeo por combinação. Nas ilustrações de renraku-waza, os botões abrem o vídeo de cada técnica que forma a combinação. '
             'O Kodokan mostra combinações oficiais no Kodomo-no-kata (unidades 1 a 3), indicadas nas ilustrações de combinação. Os contragolpes (kaeshi-waza) fazem parte dos 100 vídeos. A CBJ não publica uma série equivalente de técnicas; as referências brasileiras continuam sendo os regulamentos citados no livro.</p>'
             '<p class="cited">Vídeos: produção do Kodokan e da IJF Academy, sem uso de IA. A IA apenas localizou e organizou os links (busca feita em 22/11/2026). '
             'Os vídeos tocam pelo modo de privacidade do YouTube (youtube-nocookie.com), que só carrega o player depois do toque.</p>')
    web, pr = [intro], [intro]
    pl = (f'<div class="vplaylist"><div class="vpl-meta"><b>Lista de reprodução oficial: Kodomo-no-kata</b>'
          f'<span>Kodokan · 7 unidades + ukemi · toca em sequência, aqui mesmo</span></div>'
          f'<button type="button" class="vbtn" data-list="{KODOMO_PLAYLIST}" data-title="Kodomo-no-kata">▶ Tocar a lista inteira</button>'
          f'<a href="https://www.youtube.com/playlist?list={KODOMO_PLAYLIST}" target="_blank" rel="noopener">abrir no YouTube ↗</a><div class="vslot"></div></div>')
    web.append(pl)
    pr.append(f'<p>Lista de reprodução oficial do Kodomo-no-kata: <a href="https://www.youtube.com/playlist?list={KODOMO_PLAYLIST}">youtube.com/playlist?list={KODOMO_PLAYLIST}</a></p>')
    for title, items in EXTRAS:
        web.append(f'<h3 id="{slug(title)[:60]}">{html.escape(title)}</h3><ul class="vgrid">')
        pr.append(f'<h3 id="{slug(title)[:60]}">{html.escape(title)}</h3><ul class="vlist">')
        for n, k, v in items:
            web.append(card(n, k, v, extra=True))
            pr.append(f'<li>{html.escape(n)} — <a href="{yt(v)}">youtu.be/{v}</a></li>')
        web.append('</ul>'); pr.append('</ul>')
    for title, _, items in GROUPS:
        web.append(f'<h3 id="{slug(title)[:60]}">{html.escape(title)} · {len(items)}</h3><ul class="vgrid">')
        pr.append(f'<h3 id="{slug(title)[:60]}">{html.escape(title)} · {len(items)}</h3><ul class="vlist">')
        for n, k, v in items:
            web.append(card(n, k, v, ill.get(n.lower())))
            pr.append(f'<li><b>{html.escape(n)}</b> <span lang="ja">{k}</span> — <a href="{yt(v)}">youtu.be/{v}</a> · <a href="{ijf_url(n)}">IJF</a></li>')
        web.append('</ul>'); pr.append('</ul>')
    web.append(REFS); pr.append(REFS)
    return ''.join(web), ''.join(pr)
