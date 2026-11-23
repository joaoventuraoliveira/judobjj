"""Gera webapp/data.js + webapp/img/*.png a partir dos PDFs oficiais baixados (sem LLM).
 - Judo: cada trecho (alinea a., b., ...) do Art. 6 do Regulamento CBJ 2023 vira um item com texto do PDF e recorte da imagem.
 - BJJ: tabelas do programa JJIF (colunas por categoria: quedas, passagem, raspagens...) viram listas + recorte da coluna; regras IBJJF via paginas.
Uso: python gerar_webapp_dados.py"""
import sys, re, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pymupdf
import gerar_dashboards as G
import glossario as GL

W = G.P / "webapp"; IMG = W / "img"; IMG.mkdir(parents=True, exist_ok=True)
Z = 2.2


def save_clip(page, rect, name, z=Z):
    f = IMG / name
    page.get_pixmap(matrix=pymupdf.Matrix(z, z), clip=rect, alpha=False).save(f)
    return "img/" + name


def save_page(doc, pno, name, z=1.5):
    f = IMG / name
    if not f.exists(): doc[pno - 1].get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False).save(f)
    return "img/" + name


# ---------------- JUDO ----------------
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX"]
HEAD = re.compile(r"^(XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.\s*FAIXA")
ITEM = re.compile(r"^([a-p])\.\s*(.*)")
STOP = re.compile(r"^§\s*1º\s*$|^-As técnicas solicitadas|^Art\. 7º")


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s-(?=\d)", " – ", t)
    t = re.sub(r"\s-(?!se\b|á\b|ão\b|lo\b|la\b)(?=[A-Za-zÀ-ú(])", " – ", t)
    return t.replace("- se", "-se")


CATS_J = [("provas teóricas", "Provas teóricas"), ("provas práticas", "Provas práticas"), ("idade mínima", "Elegibilidade"), ("interstício", "Elegibilidade"), ("tempo de prática", "Elegibilidade"),
          ("acumulação", "Elegibilidade"), ("pontuação", "Elegibilidade"), ("vocabulário", "Vocabulário"), ("ukemi", "Reverência e quedas (Rei/Ukemi)"), ("saudação", "Reverência e quedas (Rei/Ukemi)"),
          ("projeção", "Projeção (Nage waza)"), ("imobiliza", "Imobilização (Osae komi waza)"), ("estrangulamento", "Estrangulamento (Shime waza)"), ("cotovelo", "Chave de cotovelo (Kansetsu waza)"),
          ("sequência", "Sequências e contragolpes"), ("contragolpe", "Sequências e contragolpes"), ("virada", "Solo: viradas, escapes e defesas"), ("nogare", "Solo: viradas, escapes e defesas"),
          ("fusegi", "Solo: viradas, escapes e defesas"), ("passagem de guarda", "Solo: viradas, escapes e defesas"), ("guarda de pernas", "Solo: viradas, escapes e defesas"),
          ("kuzushi", "Fundamentos de aplicação"), ("kumi kata", "Fundamentos de aplicação"), ("postura", "Fundamentos de aplicação"), ("shintai", "Fundamentos de aplicação"),
          ("tai sabaki", "Fundamentos de aplicação"), ("fases", "Fundamentos de aplicação"), ("histórico", "Histórico, princípios e cultura"), ("princípio", "Histórico, princípios e cultura"),
          ("ordem das faixas", "Histórico, princípios e cultura"), ("kôdansha", "Histórico, princípios e cultura"), ("kata", "Kata"), ("arbitragem", "Arbitragem"), ("oficiais de mesa", "Arbitragem"),
          ("atividades", "Atividades de ensino"), ("ensino", "Atividades de ensino"), ("cargos", "Atividades de ensino"), ("publica", "Atividades de ensino")]


def categoria(t):
    low = t.lower()
    if re.match(r"(idade|interst|acumula|tempo de prática|pontuação)", low): return "Elegibilidade"
    if low.startswith("provas teóricas"): return "Provas teóricas"
    if low.startswith("provas práticas"): return "Provas práticas"
    if low.startswith("vocabulário"): return "Vocabulário"
    for k, c in CATS_J:
        if k in low[:140] or (k in ("projeção", "imobiliza", "estrangulamento", "cotovelo", "virada") and k in low): return c
    return "Outros critérios"


def judo_dados():
    doc = pymupdf.open(G.CBJ)
    seq = []  # (pageno, text, rect)
    for pno in range(12, 21):
        pg = doc[pno - 1]
        ws = sorted(pg.get_text("words"), key=lambda w: (round((w[1] + w[3]) / 2), w[0]))
        lines = []
        for w in ws:
            yc = (w[1] + w[3]) / 2
            if lines and abs(lines[-1]["yc"] - yc) < 3.2: lines[-1]["w"].append(w)
            else: lines.append({"yc": yc, "w": [w]})
        for ln in lines:
            ln["w"].sort(key=lambda w: w[0])
            t = " ".join(w[4] for w in ln["w"]).strip()
            r = pymupdf.Rect(min(w[0] for w in ln["w"]), min(w[1] for w in ln["w"]), max(w[2] for w in ln["w"]), max(w[3] for w in ln["w"]))
            if t: seq.append((pno, t, r))
    seq.sort(key=lambda x: (x[0], x[2].y0, x[2].x0))
    # secoes
    secs = {}; cur = None; item = None; stop = False
    for (pno, t, r) in seq:
        if r.y0 < 50 or r.y0 > 800: continue
        m = HEAD.match(t)
        if m:
            cur = ROMAN.index(m.group(1)) + 1; secs[cur] = []; item = None; stop = False; continue
        if cur is None or stop: continue
        if STOP.match(t) or t.startswith("-As técnicas solicitadas"):
            stop = True; continue
        mi = ITEM.match(t)
        if mi and r.x0 < 120:
            item = {"l": mi.group(1), "lines": [(pno, t, r)]}; secs[cur].append(item)
        elif item is not None:
            item["lines"].append((pno, t, r))
    out = {}
    for n, items in secs.items():
        res = []
        for it in items:
            txt = clean(" ".join(l[1] for l in it["lines"]))
            txt = re.sub(r"^[a-p]\.\s*", "", txt)
            imgs = []
            bypage = {}
            for (pno, t, r) in it["lines"]: bypage.setdefault(pno, []).append(r)
            for pno, rs in bypage.items():
                u = pymupdf.Rect(rs[0])
                for r in rs[1:]: u |= r
                clip = pymupdf.Rect(36, max(0, u.y0 - 4), 560, min(842, u.y1 + 5))
                imgs.append(save_clip(doc[pno - 1], clip, f"judo_{n:02d}_{it['l']}_p{pno}.png"))
            res.append({"t": txt, "i": imgs, "p": sorted(bypage), "c": categoria(txt)})
        out[n] = res
    return out, doc


HEAD2 = re.compile(r"(?m)^(XIX|XVIII|XVII|XVI|XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.\s*FAIXA[^\n]*")
MARK = re.compile(r"(?:(?<=\n)|(?<=\.))([a-p])\.\s+(?=[A-ZÀ-Úa-zà-ú0-9(\-])")


def ytop(pg, frag, lo=0):
    """y do inicio da frase na pagina (search_for devolve y confiavel mesmo sem x)."""
    base = re.sub(r"\s+", " ", frag).strip()
    for n in (26, 18, 12):
        q = base[:n].strip()
        if len(q) < 6: continue
        rs = [r for r in pg.search_for(q) if r.y0 >= lo - 1]
        if rs: return min(r.y0 for r in rs)
    return None


def judo_dados2():
    doc = pymupdf.open(G.CBJ)
    secs = {}; cur = None; heads = {}
    last_item = None
    for pno in range(12, 21):
        pg = doc[pno - 1]; txt = pg.get_text("text")
        stop = re.search(r"As técnicas solicitadas|§\s*1º\s*\n?-?As", txt)
        hs = list(HEAD2.finditer(txt))
        cuts = [(0, cur, None)] + [(m.start(), ROMAN.index(m.group(1)) + 1, m) for m in hs]
        for k, (st, n, m) in enumerate(cuts):
            en = cuts[k + 1][0] if k + 1 < len(cuts) else len(txt)
            seg = txt[st:en]
            if stop and st <= stop.start() < en: seg = txt[st:stop.start()]
            if n is None: continue
            if m is not None:
                cur = n; secs.setdefault(n, []); last_item = None
                head_y = ytop(pg, m.group(0)); heads[n] = (pno, head_y or 0)
                seg = seg[len(m.group(0)):]
            marks = list(MARK.finditer(seg))
            if marks and marks[0].start() > 0 and last_item is not None:
                last_item["frags"].append([pno, seg[:marks[0].start()], None, None])
            elif not marks and last_item is not None:
                last_item["frags"].append([pno, seg, None, None])
            for j, mk in enumerate(marks):
                body = seg[mk.end(): marks[j + 1].start() if j + 1 < len(marks) else len(seg)]
                it = {"l": mk.group(1), "frags": [[pno, body, None, None]]}
                secs[n].append(it); last_item = it
        # fim de pagina e topo: resolver y depois
    out = {}
    for n, items in secs.items():
        res = []
        lo = {heads[n][0]: heads[n][1]} if n in heads else {}
        for idx, it in enumerate(items):
            txt = clean(" ".join(f[1] for f in it["frags"]))
            txt = re.sub(r"^[.\s]+", "", txt)
            imgs = []; pgs = []
            for f in it["frags"]:
                pno = f[0]; pg = doc[pno - 1]
                y0 = ytop(pg, f[1], lo.get(pno, 0)) if f[1].strip() else None
                if y0 is None: continue
                lo[pno] = y0 + 5
                nxt = None
                nitems = items[idx + 1:idx + 2]
                if nitems and nitems[0]["frags"][0][0] == pno: nxt = ytop(pg, nitems[0]["frags"][0][1], y0 + 5)
                y1 = (nxt - 2.5) if nxt else min(790, y0 + 15 * max(1, -(-len(f[1]) // 70)))
                clip = pymupdf.Rect(104, max(0, y0 - 1.5), 560, min(830, y1))
                if clip.height < 12: clip.y1 = clip.y0 + 16
                imgs.append(save_clip(pg, clip, f"judo_{n:02d}_{it['l']}_p{pno}.png")); pgs.append(pno)
            txt = txt.replace("Demo nstrar", "Demonstrar").replace("Demo  nstrar", "Demonstrar")
            parts = [p.strip() for p in re.split(r"(?=Provas (?:Teóricas|Práticas):)", txt) if p.strip()]
            for pt in parts:
                res.append({"t": pt, "i": imgs, "p": pgs, "c": categoria(pt)})
        out[n] = res
    return out, doc


BELT = {"Branca": ("#F5F5F2", None), "Branca/Cinza": ("#F5F5F2", "#9AA3AB"), "Cinza": ("#9AA3AB", None), "Cinza/Azul": ("#9AA3AB", "#2F64C8"), "Azul": ("#2F64C8", None),
        "Azul/Amarela": ("#2F64C8", "#F2C230"), "Amarela": ("#F2C230", None), "Amarela/Laranja": ("#F2C230", "#EE8A2B"), "Laranja": ("#EE8A2B", None), "Verde": ("#2E9B5B", None),
        "Roxa": ("#7A3FA3", None), "Marrom": ("#7A4A2B", None), "Preta": ("#1E2228", None)}


JQ_PDF = G.P / "judo" / "00_geral_regras_IJF_CBJ" / "fontes_pdf" / "JudoQuebec_Aide_Memoire_Judo_avec_Videos_v7.pdf"
BJA_PDF = G.P / "judo" / "00_geral_regras_IJF_CBJ" / "fontes_pdf" / "BJA_Kyu_Grade_Syllabus_Pictorial_Guide.pdf"
# categorias conforme a propria folha do Judo Quebec (contagens: 16/10/21/5/16/10/12/10)
JQ_CATS = [
 ("Te-waza", "Técnicas de braço/mão", "Seoi-nage Ippon-seoi-nage Kata-guruma Sukui-nage Uki-otoshi Sumi-otoshi Tai-otoshi Ko-uchi-gaeshi Obi-otoshi Seoi-otoshi Yama-arashi Morote-gari Kuchiki-taoshi Kibisu-gaeshi Uchi-mata-sukashi Obi-tori-gaeshi"),
 ("Koshi-waza", "Técnicas de quadril", "Uki-goshi O-goshi Koshi-guruma Tsurikomi-goshi Harai-goshi Tsuri-goshi Hane-goshi Utsuri-goshi Ushiro-goshi Sode-tsurikomi-goshi"),
 ("Ashi-waza", "Técnicas de perna/pé", "De-ashi-harai Hiza-guruma Sasae-tsurikomi-ashi O-soto-gari O-uchi-gari Ko-soto-gari Ko-uchi-gari Okuri-ashi-harai Uchi-mata Ko-soto-gake Ashi-guruma Harai-tsurikomi-ashi O-guruma O-soto-guruma O-soto-gaeshi O-uchi-gaeshi Hane-goshi-gaeshi Harai-goshi-gaeshi Uchi-mata-gaeshi O-soto-otoshi Tsubame-gaeshi"),
 ("Ma-sutemi-waza", "Sacrifício para trás", "Tomoe-nage Sumi-gaeshi Ura-nage Hikikomi-gaeshi Tawara-gaeshi"),
 ("Yoko-sutemi-waza", "Sacrifício lateral", "Yoko-otoshi Tani-otoshi Hane-makikomi Soto-makikomi Uki-waza Yoko-wakare Yoko-guruma Yoko-gake Daki-wakare Uchi-mata-makikomi Kani-basami O-soto-makikomi Harai-makikomi Uchi-makikomi Ko-uchi-makikomi"),
 ("Osaekomi-waza", "Imobilizações", "Kesa-gatame Kata-gatame Kuzure-kami-shiho-gatame Yoko-shiho-gatame Tate-shiho-gatame Kuzure-kesa-gatame Ushiro-kesa-gatame Ura-gatame Uki-gatame Kami-shiho-gatame"),
 ("Shime-waza", "Estrangulamentos", "Nami-juji-jime Gyaku-juji-jime Kata-juji-jime Hadaka-jime Okuri-eri-jime Kataha-jime Sankaku-jime Sode-guruma-jime Ryo-te-jime Tsukomi-jime Do-jime Katate-jime"),
 ("Kansetsu-waza", "Chaves de articulação", "Ude-garami Juji-gatame Ude-gatame Hiza-gatame Waki-gatame Hara-gatame Ashi-garami Ashi-gatame Te-gatame Sankaku-gatame"),
]


def judo_galeria():
    """Miniaturas das tecnicas (Judo Quebec, videos Kodokan/IJF) + paginas do guia ilustrado da BJA. Sem LLM."""
    if not JQ_PDF.exists(): return None
    doc = pymupdf.open(JQ_PDF); cat_de = {}
    for ja, pt, nomes in JQ_CATS:
        for n in nomes.split(): cat_de[n] = (ja, pt)
    tecs = []; ign = 0
    for pno in (1, 2):
        pg = doc[pno]
        for l in pg.get_links():
            u = l.get("uri") or ""
            if "judo.ijf.org/techniques/" not in u or u.endswith("/techniques/"): continue
            nome = u.rsplit("/", 1)[1]
            if nome not in cat_de: ign += 1; continue
            r = l["from"]; fn = "jq_" + nome.lower() + ".jpg"
            if not (IMG / fn).exists(): save_clip(pg, pymupdf.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1), fn, 3)
            e = GL.KD.get(GL.norm(nome)) or {}
            tecs.append({"cat": cat_de[nome][0], "catpt": cat_de[nome][1], "rom": nome, "ja": e.get("ja", ""), "en": e.get("en", ""), "sj": f"IJF/Kodokan, p. {e['pag']}" if e else "", "img": "img/" + fn, "url": u, "pag": pno + 1})
    bja = []
    if BJA_PDF.exists():
        bd = pymupdf.open(BJA_PDF)
        tits = {1: "Novice – 6º kyu (faixa branca)", 2: "6º–5º kyu (amarela)", 3: "6º–5º kyu (continuação)", 4: "5º–4º kyu (laranja)", 5: "5º–4º kyu (continuação)", 6: "4º–3º kyu (verde)", 7: "4º–3º kyu (continuação)", 8: "3º–2º kyu (azul)", 9: "3º–2º kyu (continuação)", 10: "3º–2º kyu (continuação)", 11: "3º–2º kyu (continuação)", 12: "2º–1º kyu (marrom)", 13: "2º–1º kyu (continuação)", 14: "2º–1º kyu (continuação)"}
        for p in range(1, bd.page_count + 1):
            fn = f"bja_p{p:02d}.jpg"
            if not (IMG / fn).exists(): bd[p - 1].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False).save(IMG / fn)
            bja.append({"img": "img/" + fn, "pag": p, "tit": tits.get(p, "")})
    print("galeria Judô:", len(tecs), "técnicas;", ign, "links ignorados; BJA:", len(bja), "págs")
    return {"tecs": tecs, "bja": bja}


def judo_app():
    itens, doc = judo_dados2()
    trans = []
    kyu_ids = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}
    for k, idx in kyu_ids.items():
        (i, tit, de, para, kyu, pags, idade, inter, cats, cnt) = G.J[idx]
        trans.append({"id": f"j{k:02d}", "titulo": f"{de} → {para}", "sub": kyu, "de": de, "para": para, "bde": BELT[de], "bpara": BELT[para], "fatos": [["Idade mínima", idade], ["Interstício", inter], ["Graduação", kyu]], "itens": itens.get(k, []), "pags": pags,
                      "nota": "Programa cumulativo: o conteúdo da graduação anterior também é exigido (Art. 6º, §2º). Técnicas de cada Kyô e vocabulário seguem a Comissão Estadual de Graduação (Art. 6º, §1º; Art. 9º)."})
    for k, d in zip(range(12, 17), G.DANS):
        (i, tit, grad, pags, idade, inter, pts, teo, pra) = d
        trans.append({"id": f"j{k:02d}", "titulo": tit.replace("Marrom para Preta 1º Dan", "Marrom → Preta 1º Dan").replace(" para ", " → "), "sub": grad, "de": "Marrom" if k == 12 else "Preta", "para": "Preta", "bde": BELT["Marrom" if k == 12 else "Preta"], "bpara": BELT["Preta"],
                      "fatos": [["Idade mínima", idade], ["Interstício/registro", inter], ["Pontuação", pts]], "itens": itens.get(k, []), "pags": pags,
                      "nota": "Exame estadual; promoção homologada pela CBJ. Tabelas de pontos: Art. 7º (páginas 21–24 do regulamento)."})
    sup = {17: ("6º Dan (Roku dan)", "44 anos", "25 anos de experiência; ≥6 anos como 5º Dan", "6.300 pontos"), 18: ("7º Dan (Shiti dan)", "52 anos", "32 anos de experiência; ≥7 anos como 6º Dan", "7.200 pontos"), 19: ("8º Dan (Hati dan)", "59 anos", "39 anos de experiência; ≥7 anos como 7º Dan", "7.200 pontos")}
    for k, (g, idade, tempo, pts) in sup.items():
        trans.append({"id": f"j{k:02d}", "titulo": g, "sub": "Kôdansha / graus superiores", "de": "Vermelha e branca", "para": "Vermelha e branca", "bde": ("#C8352F", "#F5F5F2"), "bpara": ("#C8352F", "#F5F5F2"),
                      "fatos": [["Idade mínima", idade], ["Tempo", tempo], ["Pontuação", pts]], "itens": itens.get(k, []), "pags": [19, 20], "nota": "Promoção por merecimento (Art. 4º). 9º e 10º Dan: excepcionais, homologação da FIJ."})
    for tr in trans:
        cats = set()
        for it in tr["itens"]:
            it["tm"] = GL.termos_judo(it["t"]); cats.add(it["c"])
        tr["catnm"] = {c: dict(zip(("ja", "en", "pt", "sj"), GL.CAT_JUDO.get(c, ("", c, c, "")))) for c in cats}
        tr["refs"] = ["cbj2023", "jq_aide", "bja_guide", "ijf_tech"]
    return {"id": "judo", "nome": "Judô", "fonte": "CBJ — Regulamento Nacional para Exame e Outorga de Faixas e Graus 2023", "url": G.URL_J, "trans": trans, "galeria": judo_galeria()}


# ---------------- BJJ ----------------
TRAD = {"BASIC TECHNIQUES": "Técnicas básicas", "TAKEDOWNS": "Quedas", "GUARD PASS": "Passagem de guarda", "ATTACKS FROM GUARD": "Ataques da guarda", "SWEEPS": "Raspagens", "SIDE CONTROL": "Controle lateral",
        "BACK CONTROL": "Controle das costas", "MOUNT": "Montada", "LEG/FOOT ATTACKS": "Ataques a pernas e pés", "SELF DEFENSE": "Defesa pessoal"}
HW = {"BASIC", "TECHNIQUES", "TAKEDOWNS", "GUARD", "PASS", "ATTACKS", "FROM", "SWEEPS", "SIDE", "CONTROL", "BACK", "MOUNT", "LEG/FOOT", "SELF", "DEFENSE"}


def jjif_pagina(doc, pno, prefix):
    pg = doc[pno - 1]; words = pg.get_text("words")
    cand = [w for w in words if w[4] in HW and 90 < w[1] < 135]
    if not cand: return {}
    hy = min(w[1] for w in cand)
    hdrw = [w for w in words if w[4] in HW and hy - 3 <= w[1] <= hy + 28]
    body = [w for w in words if w[1] > max(w[3] for w in hdrw) + 4 and w[1] < 700]
    # clusters de cabecalho (palavras vizinhas na mesma linha; linhas empilhadas se fundem)
    lines_h = []
    for w in sorted(hdrw, key=lambda w: (w[1], w[0])):
        if lines_h and abs(lines_h[-1][0][1] - w[1]) < 5: lines_h[-1].append(w)
        else: lines_h.append([w])
    cl = []
    for ln in lines_h:
        cur = None
        for w in sorted(ln, key=lambda w: w[0]):
            if cur and w[0] - cur["x1"] < 10: cur["t"] += " " + w[4]; cur["x1"] = w[2]
            else:
                cur = {"t": w[4], "x0": w[0], "x1": w[2], "y": w[1]}; cl.append(cur)
    merged = []
    for c in sorted(cl, key=lambda c: (c["y"], c["x0"])):
        tgt = next((m for m in merged if abs((m["x0"] + m["x1"]) / 2 - (c["x0"] + c["x1"]) / 2) < 30 and 0 < c["y"] - m["y"] < 22), None)
        if tgt: tgt["t"] += " " + c["t"]; tgt["x0"] = min(tgt["x0"], c["x0"]); tgt["x1"] = max(tgt["x1"], c["x1"])
        else: merged.append(dict(c))
    cl = merged
    for c in cl: c["cx"] = (c["x0"] + c["x1"]) / 2
    gx = set()
    for dr in pg.get_drawings():
        for it in dr["items"]:
            if it[0] == "l" and abs(it[1].x - it[2].x) < 1 and abs(it[1].y - it[2].y) > 30: gx.add(round(it[1].x))
            if it[0] == "re" and it[1].width < 3 and it[1].height > 30: gx.add(round(it[1].x0))
    gx = sorted(gx); bnd = []
    for x in gx:
        if not bnd or x - bnd[-1] > 8: bnd.append(x)
    if len(bnd) < 2: return {}
    edges = [14] + bnd + [bnd[-1] + (bnd[-1] - bnd[-2])]
    cents = [(edges[k] + edges[k + 1]) / 2 for k in range(len(edges) - 1)]
    cols = {k: [] for k in range(len(cents))}
    for w in body:
        cx = (w[0] + w[2]) / 2
        k = max(0, min(len(cents) - 1, sum(1 for b in bnd if b < cx)))
        cols[k].append(w)
    def ovl(c, k): return min(c["x1"], edges[k + 1]) - max(c["x0"], edges[k])
    names = []
    for k in range(len(cents)):
        best = max(cl, key=lambda c: ovl(c, k))
        names.append((best if ovl(best, k) > 0 else min(cl, key=lambda c: abs(c["cx"] - cents[k])))["t"])
    cl = [{"t": names[k], "x0": edges[k], "x1": edges[k + 1], "cx": cents[k]} for k in range(len(cents))]
    res = {}
    hl = []
    for dr in pg.get_drawings():
        for it in dr["items"]:
            if it[0] == "l" and abs(it[1].y - it[2].y) < 1 and abs(it[1].x - it[2].x) > 60: hl.append(it[1].y)
            if it[0] == "re" and it[1].height < 2.5 and it[1].width > 60: hl.append(it[1].y0)
    hl = sorted(hl); hlines = []
    for y in hl:
        if y > hy + 8 and (not hlines or y - hlines[-1] > 6): hlines.append(y)
    for i, c in enumerate(cl):
        ws = sorted(cols[i], key=lambda w: (round(w[1]), w[0]))
        lines = []
        for w in ws:
            if lines and abs(lines[-1]["y"] - w[1]) < 4: lines[-1]["w"].append(w)
            else: lines.append({"y": w[1], "w": [w]})
        items = []; last = None
        if len(hlines) >= 3:
            bands = {}
            for ln in lines:
                txt = " ".join(x[4] for x in sorted(ln["w"], key=lambda x: x[0]))
                bi = sum(1 for y in hlines if y < ln["y"] + 3)
                bands.setdefault(bi, []).append(txt)
            items = [" ".join(v) for _, v in sorted(bands.items())]
        else:
            for ln in lines:
                txt = " ".join(x[4] for x in sorted(ln["w"], key=lambda x: x[0]))
                if last is not None and ln["y"] - last < 30 and items: items[-1] += " " + txt
                else: items.append(txt)
                last = ln["w"][0][3]
        if not ws: continue
        xs = [w[0] for w in ws] + [c["x0"]]; xe = [w[2] for w in ws] + [c["x1"]]
        ybot = max(w[3] for w in ws)
        clip = pymupdf.Rect(max(0, min(xs) - 14), hy - 6, min(pg.rect.x1, max(xe) + 14), min(pg.rect.y1, ybot + 10))
        name = TRAD.get(c["t"], c["t"].title())
        res.setdefault(name, {"itens": [], "imgs": []})
        for x in items:
            x = re.sub(r"\s+", " ", x).strip()
            if x == "Front roll Back roll Back and side break fall": res[name]["itens"] += ["Front roll", "Back roll", "Back and side break fall"]
            elif x == "Front roll back roll Back and side break fall": res[name]["itens"] += ["Front roll", "Back roll", "Back and side break fall"]
            else: res[name]["itens"].append(x)
        res[name]["imgs"].append(save_clip(pg, clip, f"{prefix}_{pno:02d}_{i}.png", 2.4))
    return res



def _tb(nome, linhas, pont, col, fonte): return {"nome": nome, "linhas": linhas, "pontilhadas": pont, "col": col, "fonte": fonte}
Q, R, P, A_, M, D_ = ["Quedas"], ["Raspagens"], ["Passagem de guarda"], ["Ataques da guarda"], ["Montada"], ["Defesa pessoal"]
FORMS = {
 "01": {"titulo": "BELT EXAM - BLUE BELT", "cor": "#2468B3",
        "criterios": ["Right posture", "Basic Knowledge", "Logical Grips", "Balance", "Opponent Control"],
        "opcoes": ["Examinators can ask about the point scoring in the techniques performed", "Examinators can add a free sparring", "Ask for escapes (mount, side control, back control)"],
        "tabelas": [_tb("TAKEDOWNS (not double or single leg)", 2, 2, "L", Q), _tb("GUARD PASSING", 2, 2, "L", P), _tb("SUBMISSIONS FROM CLOSED GUARD", 2, 2, "L", A_),
                    _tb("SWEEPS", 4, 4, "R", R), _tb("SELF DEFENSE", 3, 3, "R", D_), _tb("SUBMISSIONS FROM MOUNT POSITION", 2, 2, "R", M)]},
 "02": {"titulo": "BELT EXAM - PURPLE BELT", "cor": "#6F2F92",
        "criterios": ["Knowledge of the techniques", "Explanation clear and logical", "Logical conection and transitions of the techniques", "Flow of the movements"],
        "opcoes": ["First the examinator will ask for the techniques below.", "After, the athlete will explain detailed two techniques chosen by the examination.", "After, the athlete will explain detailed two techniques chosen by him.", "The athlete will explain detailed two sequences chosen by him."],
        "tabelas": [_tb("TAKEDOWNS (with ground control)", 3, 3, "L", Q), _tb("SWEEPS FROM OPEN GUARD (SPIDER, LASSO, DLR, etc)", 3, 3, "L", R), _tb("SELF DEFENSE", 6, 4, "L", D_),
                    _tb("SWEEPS FROM CLOSED GUARD", 2, 2, "R", R), _tb("GUARD PASSING", 3, 3, "R", P), _tb("SUBMISSIONS FROM MOUNT POSITION", 3, 3, "R", M), _tb("SUBMISSIONS FROM CLOSED GUARD", 5, 3, "R", A_)]},
 "03": {"titulo": "BELT EXAM - BROWN BELT", "cor": "#6B3A2A",
        "criterios": ["Knowledge of the techniques", "Explanation clear and logical", "Logical connection and transitions of the techniques", "Flow of the movements"],
        "opcoes": ["First the examinator will ask for the techniques below", "After, the athlete will explain detailed 5 techniques from the program chosen by the examination.", "Then, the athlete will explain detailed two techniques chosen by him.", "The athlete will explain detailed 5 sequences chosen by him.", "For self defense, the examinator will request techniques from different situations, executed most realistic as possible."],
        "tabelas": [_tb("TAKEDOWNS (with ground control)", 5, 5, "L", Q), _tb("SWEEPS FROM OPEN GUARD (SPIDER, LASSO, DLR, etc)", 5, 5, "L", R), _tb("SELF DEFENSE", 10, 10, "L", D_),
                    _tb("SWEEPS FROM CLOSED GUARD", 4, 4, "R", R), _tb("GUARD PASSING", 5, 5, "R", P), _tb("SUBMISSIONS FROM MOUNT POSITION", 4, 4, "R", M), _tb("SUBMISSIONS FROM CLOSED GUARD", 7, 7, "R", A_)]},
 "04": {"titulo": "BELT EXAM - BLACK BELT", "cor": "#131A22",
        "criterios": ["Knowledge of the techniques", "Explanation clear and logical", "Logical connection and transitions of the techniques", "Flow of the movements"],
        "opcoes": ["First the examinator will ask for the techniques below", "After, the athlete will explain detailed 10 techniques from the program chosen by the examination.", "Then, the athlete will explain detailed two techniques chosen by him.", "The athlete will explain detailed 7 sequences chosen by him.", "For self defense, the examinator will request techniques from different situations, executed most realistic as possible."],
        "tabelas": [_tb("TAKEDOWNS (with ground control)", 10, 5, "L", Q), _tb("SWEEPS FROM OPEN GUARD (SPIDER, LASSO, DLR, etc)", 8, 5, "L", R), _tb("SELF DEFENSE", 15, 10, "L", D_),
                    _tb("SWEEPS FROM CLOSED GUARD", 5, 4, "R", R), _tb("GUARD PASSING", 7, 5, "R", P), _tb("SUBMISSIONS FROM MOUNT POSITION", 5, 4, "R", M), _tb("SUBMISSIONS FROM CLOSED GUARD", 10, 7, "R", A_)]},
}


PLAYLIST = "https://www.youtube.com/watch?v=OUhrE6CnIi8&list=PLndFOMjO-W27bcQWzJbHMhul7llTclJpB"
GRUPOS = [("fund", "Fundamentos", "Rolamentos, quedas de proteção, pegadas, base e deslocamentos do programa JJIF."),
          ("quedas", "Quedas", "Técnicas em pé do programa JJIF que levam o adversário ao solo."),
          ("posicoes", "Posições e controles", "Controle lateral, montada, controle das costas e transições entre elas."),
          ("guardas", "Guardas e passagens", "Entradas na guarda e passagens de guarda."),
          ("raspagens", "Raspagens", "Inversões de posição a partir da guarda."),
          ("saidas", "Saídas e recuperações", "Fugas de posições (montada, controle lateral, joelho na barriga, chave de braço) e recuperação de guarda."),
          ("transicoes", "Transições", "Passagens de uma técnica ou posição para outra (guarda para chave, guarda para raspagem, passagem para controle, etc.), com as posições de origem e de destino."),
          ("braco", "Chaves de braço", "Armlock, armbar, kimura, americana, omoplata e variações."),
          ("perna", "Chaves de perna e pé", "Chave reta de pé, toe hold, kneebar, calf slice e afins."),
          ("punho", "Chaves de punho", "Wristlock e variações."),
          ("estrang", "Estrangulamentos", "Estrangulamentos com a gola, mata-leão, guilhotina, triângulo, ezequiel e afins."),
          ("defesa", "Defesa pessoal", "Programa de defesa pessoal da JJIF (situações de agressão)."),
          ("faltas", "Faltas e golpes proibidos", "Golpes e posições que a regra IBJJF/CBJJ proíbe ou pune.")]
REGRA_PAGS = {"quedas": [18], "posicoes": [19, 21, 22], "guardas": [20], "raspagens": [23], "faltas": [32, 33]}
FOTO_PAGS = {"quedas": [18], "posicoes": [19, 21, 22], "guardas": [20], "raspagens": [23], "faltas": [30, 31, 32, 33]}
RULE_TXT = {}
JJ38_TXT = ''; JJ38_IMG = []
_ESC = re.compile(r"escape|technical stand up|replace guard|guard recovery|sit and hip|bridge", re.I)
_PERNA = re.compile(r"footlock|toe ?hold|knee ?bar|calf slice|leglock|heel", re.I)
_PUNHO = re.compile(r"wrist ?lock", re.I)
_BRACO = re.compile(r"arm ?lock|armbar|kimura|americana|omoplata|biceps slice|kata gatame|inverted armbar", re.I)
_ESTR = re.compile(r"choke|guillotine|ezequiel|baseball|triangle|mata leao", re.I)


def photos_from(doc, pno, prefix, miny=0):
    pg = doc[pno - 1]; rects = []
    for im in pg.get_images(full=True):
        for r in pg.get_image_rects(im[0]):
            if r.width > 120 and r.height > 90 and r.y0 > miny: rects.append(r)
    rects.sort(key=lambda r: (round(r.y0 / 20), r.x0))
    out = []; seen = set()
    for r in rects:
        key = (round(r.x0 / 4), round(r.y0 / 4))
        if key in seen: continue
        seen.add(key)
        try: out.append(save_clip(pg, r, f"{prefix}_{len(out) + 1}.jpg", 2.0))
        except Exception: pass
    return out


def limpar_regra(txt):
    txt = re.sub(r"IBJJF INTERNATIONAL BRAZILIAN JIU-JITSU FEDERATION", " ", txt)
    txt = re.sub(r"PHOTOS: ©IVAN TRINDADE", " ", txt)
    txt = re.sub(r"/?DAN ROD DESIGN & ILLUSTRATION:[^\n]*", " ", txt)
    txt = re.sub(r"VERSION [\d.]+ \d+©ALL RIGHTS RESERVED|VERSÃO [\d.]+ \d+©TODOS OS DIREITOS RESERVADOS", " ", txt)
    txt = re.sub(r"(?<!\S)\d+(?:\.\d+){1,3}(?!\S)", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    txt = re.sub(r"/?\s*DAN\s+ROD\s+DESIGN\s*&\s*ILLUSTRATION:\s*2014-2024\s*©\s*VICTOR\s+GRUZMAN", " ", txt)
    txt = re.sub(r"VERS(?:ION|ÃO)\s+[\d.]+\s+2024\s*©[^A-Za-zÀ-ú]*(?:ALL RIGHTS RESERVED|TODOS OS DIREITOS RESERVADOS)", " ", txt)
    txt = re.sub(r"^\d{1,2}\s+", "", txt.strip())
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:2600] + (" …" if len(txt) > 2600 else "")


_DEF = re.compile(r"defen[cs]e|headlock|bear ?hug|punch|front kick|high kick|low kick|kick on|kick in|intimidation|grab in the hair|against the wall|bare ?hand|elbow strike|knee strike|headbutt|from both hands around the neck", re.I)


def comp_class(cat, t):
    if cat == "Defesa pessoal" or _DEF.search(t): return "defesa"
    if _ESC.search(t): return "saidas"
    if _PERNA.search(t): return "perna"
    if _PUNHO.search(t): return "punho"
    if _BRACO.search(t): return "braco"
    if _ESTR.search(t): return "estrang"
    if cat == "Raspagens": return "raspagens"
    if cat == "Passagem de guarda": return "guardas"
    if cat == "Quedas": return "quedas"
    if cat == "Técnicas básicas": return "fund"
    if cat == "Ataques da guarda": return "guardas"
    return "posicoes"


def build_componentes(secoes):
    bucket = {g[0]: [] for g in GRUPOS}; seen = {g[0]: set() for g in GRUPOS}
    for s in secoes:
        for x in s["itens"]:
            gid = comp_class(s["cat"], x["t"])
            if x["t"] not in seen[gid]:
                seen[gid].add(x["t"]); bucket[gid].append({"t": x["t"], "c": s["cat"], "nm": GL.nomes_item(x["t"], s["cat"])})
    out = []
    for gid, nome, desc in GRUPOS:
        fotos = [{"img": im, "cap": RULES_CAP[n], "fonte": f"Livro de Regras IBJJF/CBJJ 2024 (PT), p. {n}"} for n in FOTO_PAGS.get(gid, []) for im in RULES_IMG.get(n, [])]
        regra = [{"titulo": f"{RULES_CAP[n]} (p. {n})", "texto": RULE_TXT[n]} for n in REGRA_PAGS.get(gid, []) if n in RULE_TXT]
        vids = [{"rot": "IBJJF Rules Tutorials — playlist oficial de regras (YouTube)", "url": PLAYLIST}] if gid in ("quedas", "posicoes", "guardas", "raspagens", "faltas") else []
        T2 = "JJIF Ne-Waza Rules V2.8.1 (2026), seção 9, p. {} (inglês)"
        for pn in {"quedas": [36], "guardas": [38, 40, 41], "raspagens": [39], "posicoes": [42, 43, 44, 45]}.get(gid, []):
            if JJ2_REGRA.get(pn): regra = regra + [{"titulo": T2.format(pn), "texto": JJ2_REGRA[pn]}]
            fotos = fotos + JJ2_FOTO.get(pn, [])
        ILP = {"quedas": [11], "braco": [6], "perna": [8, 1], "punho": [10], "estrang": [2, 3, 4, 5, 7], "faltas": [9]}
        fotos = fotos + [JJ2_ILEG[k_] for k_ in ILP.get(gid, []) if k_ in JJ2_ILEG]
        if gid in ("perna", "faltas"):
            for pn in (56, 57, 58): fotos = fotos + JJ2_FOTO.get(pn, [])
        if gid in ("braco", "perna", "punho", "estrang") and JJ38_TXT:
            regra = regra + [{"titulo": "Finalizações legais por idade e divisão (JJIF Ne-Waza Rules V2.8.1, seção 10.1, p. 47; inglês)", "texto": JJ2_SUB}, {"titulo": "Quando a luta é interrompida (livro JJIF Ne-Waza/JJAU v2.0, seção 10, p. 38; inglês)", "texto": JJ38_TXT}]
            fotos = fotos + [{"img": im, "cap": cap, "fonte": "Livro de regras JJIF Ne-Waza/JJAU v2.0, p. 38"} for im, cap in zip(JJ38_IMG, ["Perigo real de finalização", "Sem perigo (finalização não aplicada)"])]
            vids = [{"rot": "IBJJF Rules Tutorials — playlist oficial de regras (YouTube)", "url": PLAYLIST}]
        vids = vid_cards(gid) or vids
        gn = GL.GRUPOS_NM.get(gid, ("", "", "", ""))
        ent = {"id": gid, "nome": nome, "desc": desc, "itens": bucket[gid], "fotos": fotos, "regra": regra, "videos": vids, "nm": {"ja": gn[0], "en": gn[1], "pt": gn[2], "sj": gn[3]}}
        if gid == "fund": ent["subs"] = build_fund_subs(bucket["fund"])
        if gid == "transicoes":
            ent["subs"] = build_transicoes(secoes); ent["itens"] = [i for sb in ent["subs"] for i in sb["itens"]]
        out.append(ent)
    try:
        import apostila_lbjj as AL
        out.append(AL.grupo(IMG, GL))
    except Exception as e:
        print('Apostila LBJJ ignorada:', e)
    return out



# ---------- Fundamentos: tai sabaki, rolamentos, ukemi (fontes: Judo Canada, FJERJ, IJF/Kodokan, CBJ) ----------
FUND_SRC = G.P / "judo/00_geral_regras_IJF_CBJ/fontes_pdf"
VIDS = {1: ("Principles of the Rules", "LdQErGspI7s", "0:26"), 2: ("Princípios da Partida", "v8OYKn3XtGM", "3:18"), 3: ("Remoção (queda)", "bjg_LwKKja4", "5:23"),
        4: ("Passe de guarda", "-ZCXlsP-bZE", "5:15"), 5: ("Joelho na barriga", "5stRpzfX2P4", "2:06"), 6: ("Montada", "vOXo06x1qaE", "3:04"),
        7: ("Controle de costas", "AQfy0Kfxq7Y", "1:48"), 8: ("Varrer (raspagem)", "S3cSBABL9LQ", "4:29"), 9: ("Pontos cumulativos", "NkB3me-Vdqw", "2:34"),
        10: ("Penalidades disciplinares", "RAwwWq7cI_o", "1:48"), 11: ("Sequence of Penalties", "oKkIEcbUc0g", "0:43"), 12: ("Falta de combatividade", "iGbn75D1ma0", "6:04"),
        13: ("Falta Grave", "_Us_4765FBo", "8:02"), 14: ("Falta Grave", "9Bc6FTevca4", "8:09"), 15: ("Proferindo uma decisão", "HxXVhWRK7zc", "3:07"),
        16: ("Gestos do Árbitro", "1iJWvTMAr3Y", "5:39"), 17: ("Referee Format", "auXdi3HBJrk", "3:25"), 18: ("Deveres do árbitro", "3qL1_cI7mKI", "3:03")}
VID_GRUPOS = {"quedas": [3], "posicoes": [5, 6, 7, 9], "guardas": [4], "raspagens": [8], "faltas": [10, 11, 12, 13, 14, 1, 2, 15, 16, 17, 18]}


def vid_cards(gid):
    return [{"rot": f"{n}. {VIDS[n][0]} ({VIDS[n][2]})", "url": f"https://www.youtube.com/watch?v={VIDS[n][1]}", "canal": "IBJJF Rules Tutorials · canal oficial da IBJJF (verificado no YouTube em 10/11/2026)"} for n in VID_GRUPOS.get(gid, [])]


def _jc_clean(t):
    t = " ".join(t.split())
    t = re.sub(r"BREAKFALLS INSTRUCTION GUIDE Judo Canada programs are funded in part by Sport Canada\s*-\s*\d+\s*-?", "", t)
    t = re.sub(r"Judo Canada programs are funded in part by Sport Canada\s*-?\s*\d*\s*-?$", "", t)
    return t.replace(" ▪ ", "\n• ").replace("▪ ", "• ").strip()


def _seg(t, a, b=None):
    i = t.find(a); i = 0 if i < 0 else i
    j = t.find(b, i + len(a)) if b else -1
    return (t[i:j] if j > 0 else t[i:]).strip()


def _jc_photos(doc, pno, prefix):
    pg = doc[pno - 1]
    rects = sorted([r for im in pg.get_images(full=True) for r in pg.get_image_rects(im[0]) if r.width > 100 and r.height > 50], key=lambda r: (r.y0, r.x0))
    return [save_clip(pg, r, f"{prefix}_p{pno}_{k + 1}.jpg", 2.2) for k, r in enumerate(rects)]


def build_fund_subs(items):
    jc = pymupdf.open(FUND_SRC / "JudoCanada_Breakfalls_Instruction_Guide_2023.pdf")
    fj = pymupdf.open(FUND_SRC / "FJERJ_Palestra_2018_Ortografia_Termos_Judo.pdf")
    kd = pymupdf.open(FUND_SRC / "IJF_Kodokan_Classification_of_Judo_via_BritishJudo.pdf")
    JCF = "Judo Canada, Breakfalls Instruction Guide (2023), p. {}. Texto no idioma original (inglês)."
    def T(p): return _jc_clean(jc[p - 1].get_text("text"))
    def F(p, caps): return [{"img": im, "cap": caps[k] if k < len(caps) else f"Sequência de fotos {k + 1}", "fonte": f"Judo Canada (2023), p. {p}"} for k, im in enumerate(_jc_photos(jc, p, "jc"))]
    def slide(n, cap):
        name = f"fjerj_slide{n}.jpg"; save_clip(fj[n - 1], fj[n - 1].rect, name, 1.3)
        return {"img": "img/" + name, "cap": cap, "fonte": f"FJERJ, Palestra 2018 (Matsuda Iminkan), slide {n}"}
    def slide_txt(n): return " ".join(fj[n - 1].get_text("text").split())
    t7, t8, t9, t10, t11, t12, t13, t14, t15, t16 = [T(p) for p in range(7, 17)]
    ushiro = [
        {"titulo": "Ushiro-ukemi (queda para trás): instruções gerais", "texto": _seg(t7, "USHIRO-UKEMI OR BACKWARD BREAKFALL", "Progression and learning stages"), "fotos": [], "fonte": JCF.format(7)},
        {"titulo": "Ushiro-ukemi: etapas de aprendizado (deitado e sentado)", "texto": _seg(t7, "Progression and learning stages"), "fotos": F(7, ["Ushiro-ukemi: sequência de fotos"]), "fonte": JCF.format(7)},
        {"titulo": "Ushiro-ukemi: agachado, em pé, em movimento, com instrumentos e com parceiro", "texto": t8, "fotos": F(8, ["Ushiro-ukemi: sequência de fotos"]), "fonte": JCF.format(8)}]
    yoko = [
        {"titulo": "Yoko-ukemi (queda lateral): instruções gerais e etapa deitado", "texto": _seg(t9, "YOKO-UKEMI OR SIDEWAYS BREAKFALL"), "fotos": F(9, ["Yoko-ukemi: sequência de fotos"]), "fonte": JCF.format(9)},
        {"titulo": "Yoko-ukemi: sentado e agachado", "texto": t10, "fotos": F(10, ["Yoko-ukemi: sequência de fotos"]), "fonte": JCF.format(10)},
        {"titulo": "Yoko-ukemi: em pé, em movimento, com instrumentos e com parceiro", "texto": t11, "fotos": F(11, ["Yoko-ukemi: sequência de fotos"]), "fonte": JCF.format(11)}]
    mae = [
        {"titulo": "Mae-ukemi (queda para a frente): instruções e etapas", "texto": _seg(t15, "MAE-UKEMI OR FORWARD BREAKFALL"), "fotos": F(15, ["Mae-ukemi: sequência de fotos"]), "fonte": JCF.format(15)},
        {"titulo": "Mae-ukemi: variações", "texto": t16, "fotos": F(16, ["Mae-ukemi: sequência de fotos"]), "fonte": JCF.format(16)}]
    rol = [
        {"titulo": "Rolamento para a frente (zempo kaiten ukemi): instruções gerais", "texto": t12, "fotos": [], "fonte": JCF.format(12)},
        {"titulo": "Rolamento para a frente: etapas deitado e ajoelhado", "texto": t13, "fotos": F(13, ["Etapa 1 — deitado (sequência de fotos)", "Etapa 2 — ajoelhado (sequência de fotos)"]), "fonte": JCF.format(13)},
        {"titulo": "Rolamento para a frente: em pé, em movimento e com instrumentos", "texto": t14, "fotos": F(14, ["Sequência de fotos (p. 14, parte superior)", "Sequência de fotos (p. 14, parte inferior)"]), "fonte": JCF.format(14)},
        {"titulo": "Rolamento para a frente: com parceiro e a partir de projeções", "texto": _seg(t15, "• Throws", "MAE-UKEMI OR FORWARD BREAKFALL"), "fotos": [], "fonte": JCF.format(15)},
        {"titulo": "Rolamento para trás (koho kaiten ukemi)", "texto": slide_txt(23) + "\n\nNo programa da JJIF aparece como “Back roll”. Não há sequência de fotos específica nas fontes baixadas; o ushiro-ukemi (Judo Canada) mostra a rolagem para trás em posição de queda.", "fotos": [slide(23, "Vocabulário de ukemi (mae, yoko, ushiro, zempo kaiten, koho kaiten)")], "fonte": "FJERJ, Palestra 2018, slide 23 (português)"}]
    kt = " ".join(kd[1].get_text("text").split()); i = kt.find("Tai-sabaki")
    tai_def = re.split(r"\s(?=Ukemi \(|Kuzushi \(|Tsukuri \()", kt[i:i + 1400])[0] if i >= 0 else ""
    tai = [
        {"titulo": "Definição oficial (IJF/Kodokan)", "texto": tai_def, "fotos": [], "fonte": "IJF Kodokan Classification of Judo (terminologia, reeditado pela British Judo, 2025), p. 2. Texto em inglês."},
        {"titulo": "Tai sabaki: diagramas dos pés (FJERJ)", "texto": slide_txt(29) + "\n\nOs diagramas do slide mostram: posição natural (shizen hontai), migi ashi mae sabaki, hidari ashi ushiro sabaki e migi ashi mae mawari sabaki.", "fotos": [slide(29, "Tai sabaki: diagramas de movimento dos pés")], "fonte": "FJERJ, Palestra 2018, slide 29 (português)"},
        {"titulo": "Deslocamentos (shintai, ayumi ashi, suri ashi, tsugi ashi)", "texto": slide_txt(27) + "\n\n" + slide_txt(28), "fotos": [slide(27, "Shintai (deslocamento do corpo)"), slide(28, "Modos de andar: ayumi ashi, suri ashi e tsugi ashi")], "fonte": "FJERJ, Palestra 2018, slides 27 e 28 (português)"},
        {"titulo": "O que a CBJ cobra no exame", "texto": "6º Kyû (Amarela): demonstrar dois tipos de deslocamento (shintai) sobre o tatami: passadas naturais em todas as direções (ayumi ashi) e passadas sucessivas (tsugi ashi).\n5º Kyû (Amarela/Laranja): demonstrar formas de movimentos rotatórios do corpo (esquiva) (tai sabaki).", "fotos": [], "fonte": "CBJ, Regulamento de Outorga de Faixas 2023, Art. 6º, p. 14"}]
    def rol_class(t): return "rol" if re.search(r"roll", t, re.I) else ("uke" if re.search(r"break ?fall", t, re.I) else "out")
    it = {"rol": [], "uke": [], "out": []}
    for x in items: it[rol_class(x["t"])].append(x)
    base = {"fotos": [], "regra": [], "videos": []}
    def N(ja, en, pt, sj): return {"ja": ja, "en": en, "pt": pt, "sj": sj}
    for b_ in ushiro: b_["nm"] = N("後受身 · Ushiro-ukemi", "Backward breakfall", "Queda para trás", "FJERJ")
    for b_ in yoko: b_["nm"] = N("横受身 · Yoko-ukemi", "Side breakfall", "Queda lateral", "FJERJ")
    for b_ in mae: b_["nm"] = N("前受身 · Mae-ukemi", "Forward breakfall", "Queda para a frente", "FJERJ")
    for b_ in rol[:4]: b_["nm"] = N("前方回転 · Zempō-kaiten (Mae-mawari-ukemi)", "Forward rolling breakfall", "Rolamento para a frente", "FJERJ")
    rol[4]["nm"] = N("後方回転 · Kōhō-kaiten", "Backward roll", "Rolamento para trás", "FJERJ")
    tai[0]["nm"] = N("体捌 · Tai-sabaki", "Body shifting; body control", "Giro e esquiva do corpo", "IJF/Kodokan; FJERJ")
    tai[1]["nm"] = N("体捌 · Tai-sabaki", "Body shifting (foot diagrams)", "Giro e esquiva: diagramas dos pés", "FJERJ")
    tai[2]["nm"] = N("進退 · Shintai; 歩み足 · Ayumi-ashi; 摺足 · Suri-ashi; 継足 · Tsugi-ashi", "Stepping and footwork", "Deslocamentos: passada natural, deslizante e sucessiva", "FJERJ")
    tai[3]["nm"] = N("体捌 · Tai-sabaki; 進退 · Shintai", "Body shifting; stepping", "O que a CBJ cobra", "CBJ")
    return [dict(base, id="tai", nome="Tai sabaki (giro e esquiva)", nm={"ja": "体捌 · Tai-sabaki", "en": "Body shifting", "pt": "Giro e esquiva", "sj": "FJERJ"}, desc="Movimentos de giro, esquiva e deslocamento do corpo. Sem item específico na lista da JJIF; aparece no exame de judô da CBJ.", itens=[], blocos=tai),
            dict(base, id="rol", nome="Rolamentos", nm={"ja": "回転受身 · Kaiten-ukemi", "en": "Rolling breakfalls", "pt": "Rolamentos", "sj": "FJERJ"}, desc="Rolamentos para a frente e para trás, com as etapas de aprendizado (deitado, ajoelhado, em pé, em movimento, com instrumentos e parceiro).", itens=it["rol"], blocos=rol),
            dict(base, id="uke", nome="Ukemi (quedas)", nm={"ja": "受身 · Ukemi", "en": "Breakfalls", "pt": "Amortecimento de quedas", "sj": "FJERJ"}, desc="Amortecimento de quedas para trás (ushiro), de lado (yoko) e para a frente (mae), com as etapas de aprendizado.", itens=it["uke"], blocos=ushiro + yoko + mae),
            dict(base, id="out", nome="Outros fundamentos", nm={"ja": "基本 · Kihon", "en": "Other fundamentals", "pt": "Outros fundamentos", "sj": ""}, desc="Pegadas, base, alavancas e outros itens básicos do programa JJIF.", itens=it["out"], blocos=[])]



JJ2_PDF = G.P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/JJIF_Jiu-Jitsu_NeWaza_Rules_V2.8.1_EN.pdf"
JJ2_REGRA = {}; JJ2_FOTO = {}; JJ2_SUB = ""; JJ2_ILEG = {}
ILEG_CAP = {1: "Submission stretching the legs apart (U12 and below)", 2: "Choke with spinal lock (U16 and below)", 3: "Arm triangle and other kata gatame variations (U16 and below)",
            4: "Front headlock choke / guillotine (U16 and below)", 5: "Forearm choke using the sleeve / Ezekiel (U16 and below)", 6: "Shoulder lock using the legs / omoplata, etc (U16 and below)",
            7: "Triangle choke pulling on the head (U16 and below)", 8: "Straight ankle lock aligned or facing outwards (U16 and below)", 9: "Torso compression lock using the guard (U16 and below)",
            10: "Wristlock of any kind (U16 and below)", 11: "Single leg with head outside (U16 and below) (NO FOUL)"}


def photos_cap(doc, pno, prefix):
    pg = doc[pno - 1]; blocks = [(pymupdf.Rect(b[:4]), " ".join(b[4].split())) for b in pg.get_text("blocks") if b[4].strip()]
    rects = []; seen = set()
    for im in pg.get_images(full=True):
        for r in pg.get_image_rects(im[0]):
            k = tuple(round(x / 4) for x in r)
            if r.width > 110 and r.height > 80 and r.width < 700 and k not in seen: seen.add(k); rects.append(r)
    rects.sort(key=lambda r: (round(r.y0 / 40), r.x0)); out = []
    for k, r in enumerate(rects):
        best = None
        for br, tx in blocks:
            if len(tx) < 3 or len(tx) > 170: continue
            ov = min(br.x1, r.x1) - max(br.x0, r.x0)
            if br.y0 >= r.y1 - 4 and br.y0 <= r.y1 + 70 and ov > 0.3 * min(br.width, r.width):
                d_ = br.y0 - r.y1
                if best is None or d_ < best[0]: best = (d_, tx)
        cap = best[1] if best else f"Foto {k + 1} (página {pno})"
        try: img = save_clip(pg, r & pg.rect, f"{prefix}_{k + 1}.jpg", 2.0)
        except Exception: continue
        out.append({"img": img, "cap": cap, "fonte": f"JJIF Ne-Waza Rules V2.8.1, p. {pno}"})
    return out


def ileg_photos(doc):
    out = {}; n = 1
    for pno in (61, 62):
        pg = doc[pno - 1]; rects = []; seen = set()
        for im in pg.get_images(full=True):
            for r in pg.get_image_rects(im[0]):
                k = tuple(round(x / 4) for x in r)
                if r.width > 110 and r.height > 80 and r.width < 700 and k not in seen: seen.add(k); rects.append(r)
        rects.sort(key=lambda r: (round(r.y0 / 150), r.x0))
        for r in rects:
            out[n] = {"img": save_clip(pg, r & pg.rect, f"jj2_ileg_{n:02d}.jpg", 2.0), "cap": ILEG_CAP[n], "fonte": f"JJIF Ne-Waza Rules V2.8.1, p. {pno}: ação ilegal nas divisões indicadas; a foto mostra a técnica"}
            n += 1
    return out



REFS = [
 {"id": "cbj2023", "titulo": "Regulamento Nacional para Exame e Outorga de Faixas e Graus 2023", "org": "CBJ — Conselho Nacional de Graus", "ano": "2023", "url": "https://cbj.com.br/pt/governanca/transparencia/regulamentos-esportivos", "arq": "CBJ_Regulamento_Outorga_de_Faixas_2023.pdf", "pat": "CBJ(?!J)"},
 {"id": "ibjjf_grad", "titulo": "General System of Graduation (Sistema Geral de Graduação)", "org": "IBJJF", "ano": "jun/2026", "url": "https://ibjjf.com/graduation-system", "arq": "IBJJF_20260611_IBJJF_Graduacao_EN.pdf", "pat": "Sistema Geral de Gradua|General System of Gradua|IBJJF — Sistema"},
 {"id": "cbjj_rules", "titulo": "Livro de Regras IBJJF/CBJJ 2024 (PT), v6.1", "org": "CBJJ / IBJJF", "ano": "2024", "url": "https://cbjj.com.br/books-videos", "arq": "CBJJ_IBJJF_Regras_PT_2024.pdf", "pat": 'Livro de Regras IBJJF/CBJJ|"sp": ?"CBJJ"'},
 {"id": "golpes", "titulo": "Golpes Proibidos 2024 (PT)", "org": "CBJJ / IBJJF", "ano": "2024", "url": "https://cbjj.com.br/books-videos", "arq": "CBJJ_Golpes_Proibidos_2024_PT.pdf", "pat": "Golpes Proibidos"},
 {"id": "jjif_grad", "titulo": "Jiu-Jitsu Graduation System (técnicas por faixa, fichas de exame, graus)", "org": "JJIF — Rules and Technical Department", "ano": "v11", "url": "https://jjif.sport/organization/about-us/downloads", "arq": "JJIF_Jiu-Jitsu_Graduation_System_Book_v11_copia_JJAU.pdf", "pat": "Programa técnico \\(JJIF\\)|programa da JJIF|Programa da JJIF|JJIF Graduation|Coluna no programa|JJIF, Graduation"},
 {"id": "jjif_nw", "titulo": "JJIF Jiu-Jitsu (Ne-Waza) Rules V2.8.1", "org": "JJIF", "ano": "2026", "url": "https://jjif.sport/organization/about-us/downloads", "arq": "JJIF_Jiu-Jitsu_NeWaza_Rules_V2.8.1_EN.pdf", "pat": "JJIF Ne-Waza Rules V2\\.8\\.1"},
 {"id": "jjau", "titulo": "Rule Book Ne-Waza v2.0 (JJAU, aprovado pela JJIF)", "org": "JJAU / JJIF", "ano": "v2.0", "url": "https://events.uaejjf.org/en/files/9ev/87", "arq": "JJAU_JJIF_NeWaza_Rule_Book_v2.pdf", "pat": "JJAU"},
 {"id": "yt", "titulo": "IBJJF Rules Tutorials (playlist oficial no YouTube; 18 vídeos disponíveis)", "org": "IBJJF (canal verificado)", "ano": "2024", "url": "https://www.youtube.com/playlist?list=PLndFOMjO-W27bcQWzJbHMhul7llTclJpB", "arq": "— (vídeos: apenas link)", "pat": "IBJJF Rules Tutorials|youtube\\.com/watch"},
 {"id": "judocanada", "titulo": "Breakfalls Instruction Guide", "org": "Judo Canada", "ano": "2023", "url": "https://judocanada.org/wp-content/uploads/2023/07/Guide-Chutes_2023_EN.pdf", "arq": "JudoCanada_Breakfalls_Instruction_Guide_2023.pdf", "pat": "Judo Canada"},
 {"id": "fjerj", "titulo": "Palestra: pronúncia, significado e modo de ler em japonês (Assoc. Matsuda Iminkan)", "org": "FJERJ — Federação de Judô do Estado do Rio de Janeiro", "ano": "2018", "url": "https://judorio.org/wp-content/uploads/2018/10/Palestra-FJERJ-2018-Ortografia.pdf", "arq": "FJERJ_Palestra_2018_Ortografia_Termos_Judo.pdf", "pat": "FJERJ"},
 {"id": "kodokan", "titulo": "IJF Kodokan Classification of Judo (terminologia, dicionário Kodokan japonês-inglês)", "org": "IJF / Kodokan (reeditado pela British Judo)", "ano": "2025", "url": "https://www.britishjudo.org.uk/wp-content/uploads/2025/06/IJF-Kodokan-Classification-of-Judo.pdf", "arq": "IJF_Kodokan_Classification_of_Judo_via_BritishJudo.pdf", "pat": "IJF/Kodokan|IJF Kodokan"},
 {"id": "jq_aide", "titulo": "Aide-mémoire — Liste des techniques de judo du Kodokan par grade (avec vidéos)", "org": "Judo Québec (fonte: Judo Canada, syllabus jan/2021; vídeos Kodokan/IJF)", "ano": "2021 (v7)", "url": "https://judo.ijf.org/techniques/", "arq": "JudoQuebec_Aide_Memoire_Judo_avec_Videos_v7.pdf", "pat": "Judo Qu"},
 {"id": "ijf_tech", "titulo": "IJF Judo — técnicas (vídeos oficiais por técnica)", "org": "IJF — International Judo Federation", "ano": "—", "url": "https://judo.ijf.org/techniques/", "arq": "— (vídeos: apenas link)", "pat": "judo\\.ijf\\.org"},
 {"id": "bja_guide", "titulo": "Kyu Grade Syllabus — Pictorial Guide (programa técnico ilustrado por faixa)", "org": "British Judo Association", "ano": "—", "url": "https://www.britishjudo.org.uk/", "arq": "BJA_Kyu_Grade_Syllabus_Pictorial_Guide.pdf", "pat": "BJA"},
 {"id": "lbjj", "titulo": "Apostila da Liga Brasileira de Jiu-Jitsu (LBJJ), alterações de nov/2007 — programa de exame de Jiu-Jitsu tradicional (PDF digitalizado)", "org": "LBJJ — Liga Brasileira de Jiu-Jitsu (fundada em 13/07/1991)", "ano": "2007", "url": "", "arq": "Apostila - Liga brasileira de Jiu Jitsu.pdf (vault: Dominios/Judo_BJJ/fontes_livros)", "pat": "Apostila LBJJ|LBJJ"},
 {"id": "lbjj_site", "titulo": "LBJJ: Circular Oficial do exame de faixa preta e concessão de graus (05/12/2026) e formulário de filiação de atleta", "org": "LBJJ — Liga Brasileira de Jiu-Jitsu", "ano": "2026", "url": "https://lbjj.com.br/examefxpreta/", "arq": "LBJJ_Circular_Exame_Faixa_Preta_e_Graus_2026-12-05.pdf (vault: fontes_livros)", "pat": "lbjj\\.com\\.br|Circular Oficial"},
 {"id": "app", "titulo": "Nomes em português rotulados “app”: sugestões do assistente, sem fonte oficial (conferir)", "org": "Assistente (Claude)", "ano": "2026", "url": "", "arq": "pipelines/glossario.py", "pat": '"sp": ?"app"'},
]


_TR_CUE = re.compile(r"going to|transition|\bto (?:spider|guard|the back|back|mount|side)|double attack|and (?:armbar|triangle|choke|mount|americana|rear)|plus |take from|with guillotine|replac|recover|getting the opponent|turns to all four|pull to|pulling guard|arm drag", re.I)


def _tr_orig(t, cat):
    low = t.lower()
    if "knee on belly" in low and not re.search(r"plus knee on belly", low): return "joelho na barriga"
    if re.search(r"from mount|escape from mount|armlock from mount", low): return "montada"
    if re.search(r"side control|side to back|side headlock", low): return "controle lateral"
    if "half guard" in low: return "guarda"
    if re.search(r"guard", low) and not re.search(r"passing|pass\b", low): return "guarda"
    if re.search(r"double leg|single leg|takedown|bear ?hug|front punch|kick|intimidation|o goshi", low): return "em pé"
    if re.search(r"arm drag", low): return "guarda"
    if cat == "Passagem de guarda": return "passagem"
    if cat in ("Ataques da guarda", "Raspagens"): return "guarda"
    if cat == "Controle lateral": return "controle lateral"
    if cat == "Controle das costas": return "costas"
    if cat == "Montada": return "montada"
    if cat == "Defesa pessoal": return "em pé"
    return ""


def _tr_dest(t):
    low = t.lower()
    if re.search(r"armbar|armlock|arm bar|kimura|americana|omoplata|biceps", low): return "chave de braço"
    if re.search(r"leglock|footlock|kneebar|toe hold|calf", low): return "chave de perna"
    if re.search(r"choke|guillotine|triangle", low): return "estrangulamento"
    if "sweep" in low: return "raspagem"
    if re.search(r"going to (?:the )?back|to back|back take|getting the opponent.s back|all four|side to back", low): return "costas"
    if re.search(r"mount", low): return "montada"
    if re.search(r"knee on belly", low): return "joelho na barriga"
    if re.search(r"takedown", low): return "queda"
    if re.search(r"guard", low): return "guarda"
    return ""


def _posfoto(key, pref):
    m = {"guarda": JJ2_FOTO.get(38, [])[:3], "raspagem": JJ2_FOTO.get(39, [])[:3], "passagem": JJ2_FOTO.get(40, [])[:3], "joelho na barriga": JJ2_FOTO.get(42, [])[:2],
         "montada": JJ2_FOTO.get(43, [])[:2], "costas": JJ2_FOTO.get(45, [])[:2], "queda": JJ2_FOTO.get(36, [])[:2], "em pé": JJ2_FOTO.get(36, [])[:2],
         "controle lateral": [{"img": im, "cap": RULES_CAP[19], "fonte": "Livro de Regras IBJJF/CBJJ 2024 (PT), p. 19"} for im in RULES_IMG.get(19, [])[:2]],
         "chave de braço": [JJ2_ILEG[k] for k in (6,) if k in JJ2_ILEG], "estrangulamento": [JJ2_ILEG[k] for k in (4, 5, 7) if k in JJ2_ILEG], "chave de perna": [JJ2_ILEG[k] for k in (8,) if k in JJ2_ILEG]}
    return [dict(f, cap=f"{pref}: {f['cap']}") for f in m.get(key, [])]


_POSVID = {"guarda": [4], "raspagem": [8], "passagem": [4], "joelho na barriga": [5], "montada": [6], "costas": [7], "queda": [3], "em pé": [3], "controle lateral": [9]}


def _vids(keys):
    ns = []
    for k in keys:
        for n in _POSVID.get(k, []):
            if n not in ns: ns.append(n)
    if 9 not in ns: ns.append(9)
    return [{"rot": f"{n}. {VIDS[n][0]} ({VIDS[n][2]})", "url": f"https://www.youtube.com/watch?v={VIDS[n][1]}", "canal": "IBJJF Rules Tutorials · canal oficial da IBJJF"} for n in ns]


_FAM_KEYS = {"guarda": ["guarda"], "passagem": ["passagem"], "em pé": ["queda"], "controle": ["controle lateral", "montada", "joelho na barriga"], "costas": ["costas"],
             "chave": ["chave de braço", "chave de perna"], "estrangulamento": ["estrangulamento"], "raspagem": ["raspagem"], "queda": ["queda"]}
_FAM_NOME = {"guarda": "Guarda", "passagem": "Passagem de guarda", "em pé": "Em pé (queda e defesa pessoal)", "controle": "Controle (lateral, montada, joelho na barriga)", "costas": "Costas",
             "chave": "chave", "estrangulamento": "estrangulamento", "raspagem": "raspagem", "queda": "queda"}


def _fam_o(o):
    if o in ("guarda",): return "guarda"
    if o == "passagem": return "passagem"
    if o == "em pé": return "em pé"
    if o in ("controle lateral", "montada", "joelho na barriga", "posição"): return "controle"
    if o == "costas": return "costas"
    return "controle"


def _fam_d(d):
    if d in ("chave de braço", "chave de perna"): return "chave"
    if d in ("montada", "joelho na barriga", "controle lateral"): return "controle"
    return d


def _fotos_fam(f, pref):
    out = []
    for k in _FAM_KEYS.get(f, [f]): out += _posfoto(k, pref)[:2]
    return out


def build_transicoes(secoes):
    pares = {}; vistos = set()
    for sc in secoes:
        for x in sc["itens"]:
            t = x["t"]
            if not _TR_CUE.search(t) or t in vistos: continue
            d = _tr_dest(t); o = _tr_orig(t, sc["cat"])
            if not d: continue
            vistos.add(t); pares.setdefault((_fam_o(o), _fam_d(d)), []).append({"t": t, "c": sc["cat"], "nm": GL.nomes_item(t, sc["cat"])})
    base = {"regra": [], "blocos": []}
    subs = []
    ordem = ["guarda", "passagem", "controle", "costas", "em pé"]
    for (fo, fd), its in sorted(pares.items(), key=lambda kv: (ordem.index(kv[0][0]) if kv[0][0] in ordem else 9, kv[0][1])):
        nome = f"{_FAM_NOME[fo].split(' (')[0]} → {_FAM_NOME[fd].split(' (')[0].lower()}"
        keys = _FAM_KEYS.get(fo, [fo]) + _FAM_KEYS.get(fd, [fd])
        subs.append(dict(base, id=f"tr_{len(subs)}", nome=nome, desc=f"Transições do programa JJIF de «{_FAM_NOME[fo]}» para «{_FAM_NOME[fd]}». As fotos mostram a posição de origem e a de destino; as fontes não trazem fotos da passagem entre elas.",
                         itens=its, fotos=_fotos_fam(fo, "Origem") + _fotos_fam(fd, "Destino"), videos=_vids(keys), nm={"ja": "連絡技 (Renraku-waza)", "en": "Linked technique: " + nome, "pt": "Transição: " + nome, "sj": "FJERJ"}))
    def regra_sub(id_, nome, desc, fo, fd, texto_pag):
        keys = _FAM_KEYS.get(fo, [fo]) + _FAM_KEYS.get(fd, [fd])
        return dict(base, id=id_, nome=nome, desc=desc, itens=[], fotos=_fotos_fam(fo, "Origem") + _fotos_fam(fd, "Destino"), videos=_vids(keys),
                    regra=[{"titulo": f"JJIF Ne-Waza Rules V2.8.1, seção 9, p. {p} (inglês)", "texto": JJ2_REGRA[p]} for p in texto_pag if JJ2_REGRA.get(p)],
                    nm={"ja": "連絡技 (Renraku-waza)", "en": "Linked technique (rule-based): " + nome, "pt": "Transição prevista na regra: " + nome, "sj": "FJERJ"})
    subs.append(regra_sub("tr_regra_rasp", "Regra: raspagem → controle", "A regra JJIF 9.2.4 pontua a raspagem que termina direto em joelho na barriga, montada ou costas.", "raspagem", "controle", [39]))
    subs.append(regra_sub("tr_regra_pass", "Regra: passagem de guarda → controle", "Passagem de guarda que termina em controle lateral, montada ou costas.", "passagem", "controle", [40, 41]))
    subs.append(regra_sub("tr_regra_cum", "Regra: queda → passagem → montada (pontos cumulativos)", "A pontuação é cumulativa quando uma posição leva a outra sem perder o controle; veja o vídeo “Pontos cumulativos”.", "queda", "controle", [36]))
    return subs


RULES_CAP = {18: "Pontuação: queda (takedown)", 19: "Controle lateral, norte-sul, joelho na barriga e contra-queda", 20: "Passagem de guarda: definição e exemplos", 21: "Montada e montada nas costas (4 pontos)",
             22: "Controle das costas (4 pontos)", 23: "Raspagem (2 pontos)", 30: "Golpes proibidos, fotos 1 a 14", 31: "Golpes proibidos, fotos 15 a 25", 32: "Knee reaping (falta)", 33: "Pés cruzados e 50/50 (faltas)"}
ILUS = {"Quedas": [18], "Passagem de guarda": [20], "Controle lateral": [19], "Montada": [21], "Controle das costas": [22], "Raspagens": [23], "Ataques a pernas e pés": [32, 33]}
RULES_IMG = {}; GAL = []


def rules_photos(doc, pno):
    pg = doc[pno - 1]; rects = []
    for im in pg.get_images(full=True):
        for r in pg.get_image_rects(im[0]):
            if r.width > 90 and r.height > 70: rects.append(r)
    rects.sort(key=lambda r: (round(r.y0 / 20), r.x0))
    out = []; seen = set()
    for r in rects:
        key = (round(r.x0 / 4), round(r.y0 / 4))
        if key in seen: continue
        seen.add(key)
        out.append(save_clip(pg, r, f"rules_p{pno:02d}_{len(out) + 1}.jpg", 2.0))
    return out


def add_nm(secoes):
    for sc in secoes:
        for x in sc["itens"]: x["nm"] = GL.nomes_item(x["t"], sc["cat"])
    return secoes


def add_ilus(secoes):
    for s in secoes:
        s["ilus"] = [{"img": im, "cap": RULES_CAP[n], "fonte": f"Livro de Regras IBJJF/CBJJ 2024 (PT), p. {n}"} for n in ILUS.get(s["cat"], []) for im in RULES_IMG[n]]
    return secoes


def jjif_faixa(doc, pags, prefix):
    acc = {}
    for p in pags:
        for nome, v in jjif_pagina(doc, p, prefix).items():
            a = acc.setdefault(nome, {"itens": [], "imgs": []})
            a["itens"] += v["itens"]; a["imgs"] += v["imgs"]
    def _limpa(itens):
        out = []
        for x in itens:
            x = re.sub(r"\s+", " ", x).strip()
            if not x: continue
            if out and (x.startswith("(") or x[0].islower()): out[-1] = out[-1] + " " + x; continue
            out.append(x)
        vis = {}; res = []
        for x in out:
            k = re.sub(r"[^a-z]", "", x.lower().replace("controllling", "controlling").replace("close guard", "closed guard").replace("bare hand", "barehand"))
            k = k.replace("armbar", "armbar").replace("kneebar", "kneebar").replace("bearhug", "bearhug").replace("mataleo", "mataleao").replace("onall", "toall")
            if k in vis: continue
            vis[k] = 1; res.append(x)
        return res
    return [{"cat": k, "itens": [{"t": t} for t in _limpa(v["itens"])], "imgs": v["imgs"]} for k, v in acc.items()]


def bjj_app():
    jd = pymupdf.open(G.JJPDF); ib = pymupdf.open(G.IB)
    global RULES_IMG, GAL
    rules = pymupdf.open(G.P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/CBJJ_IBJJF_Regras_PT_2024.pdf")
    proib = pymupdf.open(G.P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/CBJJ_Golpes_Proibidos_2024_PT.pdf")
    RULES_IMG = {n: rules_photos(rules, n) for n in RULES_CAP}
    global JJ2_REGRA, JJ2_FOTO, JJ2_SUB, JJ2_ILEG
    r2 = pymupdf.open(JJ2_PDF)
    JJ2_REGRA = {n: " ".join(r2[n - 1].get_text("text").split())[:1900] for n in (36, 38, 39, 40, 41, 42, 43, 44, 45)}
    JJ2_FOTO = {n: photos_cap(r2, n, f"jj2_p{n}") for n in (36, 38, 39, 40, 41, 42, 43, 44, 45, 56, 57, 58)}
    JJ2_SUB = " ".join(r2[46].get_text("text").split())[:3200]
    JJ2_ILEG = ileg_photos(r2)
    global JJ38_TXT, JJ38_IMG
    jjau = pymupdf.open(G.P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/JJAU_JJIF_NeWaza_Rule_Book_v2.pdf")
    _t = " ".join(jjau[37].get_text("text").split())
    JJ38_TXT = re.sub(r"\*?Please see the table on appendix.*$", "", _t)[:1700]
    JJ38_IMG = [save_clip(jjau[37], pymupdf.Rect(*bx), f"jjau_p38_real_{k + 1}.jpg", 2.4) for k, bx in enumerate([(471, 442, 626, 559), (631, 442, 787, 560)])]  # as duas fotos da p. 38 (posições medidas no PDF)
    global RULE_TXT
    RULE_TXT = {n: limpar_regra(rules[n - 1].get_text("text")) for n in (18, 19, 20, 21, 22, 23, 32, 33)}
    proib_img = save_page(proib, 1, "golpes_proibidos.png", 1.3)
    GAL = [{"img": im, "cap": RULES_CAP[n], "fonte": f"Livro de Regras IBJJF/CBJJ 2024 (PT), p. {n}, foto {k + 1} de {len(RULES_IMG[n])} (fotos: Ivan Trindade)"} for n in sorted(RULES_CAP) for k, im in enumerate(RULES_IMG[n])]
    GAL.append({"img": proib_img, "cap": "Golpes proibidos (folha oficial IBJJF)", "fonte": "CBJJ/IBJJF — Golpes Proibidos 2024 (PT)"})
    ib_p = {n: save_page(ib, n, f"ibjjf_p{n:02d}.png") for n in (4, 5, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17)}
    BB = {"Branca": ("#F5F5F2", None), "Azul": ("#2F64C8", None), "Roxa": ("#7A3FA3", None), "Marrom": ("#7A4A2B", None), "Preta": ("#1E2228", "#C8352F")}
    trans = []
    ficha_box = pymupdf.Rect(478, 36, 986, 748)
    nomes = {"01": ("Branca", "Azul", "Branca", "Azul"), "02": ("Azul", "Roxa", "Azul", "Roxa"), "03": ("Roxa", "Marrom", "Roxa", "Marrom"), "04": ("Marrom", "Preta", "Marrom", "Preta")}
    for (i, tit, de, para, idade, tempo_t, extra, _imgs) in [(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) for a in [
            ("01", "Branca para Azul", "Branca", "Azul", "16 anos ou mais", "Branca: sem tempo mínimo. Ao chegar à Azul, o próximo mínimo é de 2 anos na Azul (ver Azul → Roxa).", "Atletas de 16 anos seguem o sistema adulto: Cinza, Amarela e Laranja passam à Azul; Verde vai à Azul ou Roxa por decisão do professor.", []),
            ("02", "Azul para Roxa", "Azul", "Roxa", "16 anos ou mais", "2 anos na Azul (1 ano se registrado antes como Cinza, Amarela ou Laranja; sem mínimo se registrado como Verde, Azul Juvenil ou campeão mundial adulto azul). Atletas de 16–17 anos só avançam à Marrom na divisão Adulto.", "—", []),
            ("03", "Roxa para Marrom", "Roxa", "Marrom", "18 anos ou mais (Marrom)", "1,5 ano na Roxa (1 ano se vinha de Azul Juvenil; sem mínimo se Laranja/Verde e Azul Juvenil, Roxa Juvenil ou campeão mundial adulto roxo).", "—", []),
            ("04", "Marrom para Preta", "Marrom", "Preta", "18 anos ou mais; aos 18 somente quem foi campeão mundial adulto na Marrom", "1 ano na Marrom (sem mínimo para campeão mundial adulto marrom).", "Certificado de faixa preta: filiação IBJJF, sem graduação provisória, certificado de primeiros socorros/RCP e de Programa de Árbitros, Seminário ou Webinar de Regras (últimos 12 meses). Só assina a faixa preta um preta com ≥2 graus certificados pela IBJJF.", [])]]:
        k = G.JJ[i]; faixa_pt = k[0]
        tec = add_nm(add_ilus(jjif_faixa(jd, k[1], f"jjif_{i}")))
        ficha = save_clip(jd[k[2] - 1], ficha_box, f"jjif_ficha_{i}.png", 2.0)
        trans.append({"id": f"b{i}", "titulo": f"{de} → {para}", "sub": "Exame de faixa", "bde": BB[de], "bpara": BB[para],
                      "fatos": [["Idade mínima (IBJJF)", idade], ["Tempo mínimo (IBJJF)", tempo_t], ["Graus (IBJJF)", "Branca a Marrom: 4 graus, adoção livre pelo professor"], ["Registro (IBJJF)", "Filiação aprovada por professor faixa preta filiado à IBJJF"]],
                      "abas": [{"nome": "Programa técnico (JJIF)", "tipo": "jjif", "refs": ["jjif_grad"], "intro": f"Programa da JJIF para a faixa {faixa_pt} (p. {k[1][0]}–{k[1][-1]}). Cumulativo: repete itens das faixas anteriores e acrescenta novos. Nomes das técnicas no original (inglês/japonês).", "secoes": tec},
                               {"nome": "Ficha de exame (JJIF)", "tipo": "ficha", "refs": ["jjif_grad"], "criterios": k[3], "opcoes": k[4], "secoes_ficha": k[5], "carga": k[6].replace("**", ""), "img": ficha, "form": FORMS[i]},
                               {"nome": "Lista de componentes", "tipo": "componentes", "grupos": build_componentes(tec)},
                               {"nome": "Regras IBJJF", "tipo": "ibjjf", "refs": ["ibjjf_grad"], "extra": extra, "imgs": [ib_p[7], ib_p[9], ib_p[11]]}],
                      "nota": "A IBJJF/CBJJ não publica programa técnico de exame. O programa e a ficha nas abas abaixo são da JJIF, outra federação; na JJIF o exame é obrigatório só de Azul a Preta."})
    # preta graus + mestres
    trans.append({"id": "b05", "titulo": "Preta — graus 1 a 6", "sub": "Graus", "bde": BB["Preta"], "bpara": BB["Preta"],
                  "fatos": [["1º grau", "3 anos de atividade comprovada na Preta"], ["2º grau", "3 anos desde o anterior, ou 6 anos de atividade"], ["3º grau", "3 anos, ou 9 anos"], ["4º grau", "5 anos, ou 14 anos"], ["5º grau", "5 anos, ou 19 anos"], ["6º grau", "5 anos, ou 24 anos"]],
                  "abas": [{"nome": "Regras IBJJF", "tipo": "ibjjf", "refs": ["ibjjf_grad"], "extra": "Prova de atividade (Art. 4.2.1): filiação ativa; academia registrada; aprovação de filiações; certificação anterior; títulos IBJJF; certificados do Programa de Árbitros e Curso de Regras.", "imgs": [ib_p[10], ib_p[11]]}],
                  "nota": "Sem programa técnico oficial para os graus."})
    trans.append({"id": "b06", "titulo": "Graus de mestre (7º ao 9º)", "sub": "Vermelha e preta · vermelha e branca · vermelha", "bde": ("#C8352F", "#1E2228"), "bpara": ("#C8352F", "#F5F5F2"),
                  "fatos": [["7º grau — Vermelha e Preta", "49 anos · 7 anos desde o anterior ou 31 anos de atividade"], ["8º grau — Vermelha e Branca", "56 anos · 7 anos ou 38 anos"], ["9º grau — Vermelha", "66 anos · 10 anos ou 48 anos"], ["10º grau", "Concedido apenas aos pioneiros: Carlos, Oswaldo, George, Gastão e Hélio"]],
                  "abas": [{"nome": "Regras IBJJF", "tipo": "ibjjf", "refs": ["ibjjf_grad"], "extra": "—", "imgs": [ib_p[10]]}], "nota": "Fonte: IBJJF, junho/2026."})
    # infantil JJIF
    kids = [("k1", "Branca → Cinza", "Cinza", [10, 11], ("#F5F5F2", None), ("#9AA3AB", None)), ("k2", "Cinza → Amarela", "Amarela", [12, 13], ("#9AA3AB", None), ("#F2C230", None)),
            ("k3", "Amarela → Laranja", "Laranja", [14, 15], ("#F2C230", None), ("#EE8A2B", None)), ("k4", "Laranja → Verde", "Verde", [16, 17, 18, 19], ("#EE8A2B", None), ("#2E9B5B", None))]
    ages = {"k1": "4 a 15 anos", "k2": "7 a 15 anos", "k3": "10 a 15 anos", "k4": "13 a 15 anos"}
    stripe = {"k1": "21 aulas por grau", "k2": "32 aulas por grau", "k3": "32 aulas por grau", "k4": "32 aulas por grau"}
    for (kid, tit, faixa, pags, b1, b2) in kids:
        TK = add_nm(add_ilus(jjif_faixa(jd, pags, f"jjif_{kid}")))
        trans.append({"id": kid, "titulo": tit, "sub": "Infantil (4–15 anos)", "bde": b1, "bpara": b2,
                      "fatos": [["Idade permitida (IBJJF)", ages[kid]], ["Tempo mínimo (IBJJF)", "Sem tempo mínimo de 4 a 15 anos"], ["Graus sugeridos (JJIF)", stripe[kid]], ["Exame (JJIF)", "Sem exame oficial; pedido à federação nacional"]],
                      "abas": [{"nome": "Programa técnico (JJIF)", "tipo": "jjif", "refs": ["jjif_grad"], "intro": f"Programa infantil da JJIF — faixa {faixa} (p. {pags[0]}–{pags[-1]}). Nomes das técnicas no original.", "secoes": TK},
                               {"nome": "Lista de componentes", "tipo": "componentes", "grupos": build_componentes(TK)},
                               {"nome": "Regras IBJJF", "tipo": "ibjjf", "extra": "As faixas infantis da IBJJF têm 13 níveis (cinza, amarela, laranja e verde, cada uma com branca/preta); aos 16 anos Cinza, Amarela e Laranja passam à Azul.", "imgs": [ib_p[4], ib_p[7], ib_p[8]]}],
                      "nota": "Programa da JJIF; a IBJJF não define conteúdo técnico."})
    return {"id": "bjj", "nome": "Jiu-Jitsu (BJJ)", "fonte": "IBJJF — Sistema Geral de Graduação (jun/2026) · JJIF — Jiu-Jitsu Graduation System v11", "url": G.URL_B, "trans": trans}


if __name__ == "__main__":
    data = {"judo": judo_app(), "bjj": bjj_app(), "REFS": REFS}
    js = "window.DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (W / "data.js").write_text(js, encoding="utf-8")
    # i18n: dicionarios (MT offline + manuais) vao junto do data.js
    import i18n_ui as UI
    dp = pathlib.Path(__file__).resolve().parent / "i18n_dict.json"
    d_i = json.loads(dp.read_text(encoding="utf-8")) if dp.exists() else {"pt": {}, "en": {}}
    I18N = {"pt": d_i["pt"], "en": d_i["en"], "ui_en": UI.UI_EN, "ui_pt": UI.UI_PT, "rules_en": UI.RULES_EN, "belt_en": UI.BELT_EN}
    js = js + "window.I18N=" + json.dumps(I18N, ensure_ascii=False, separators=(",", ":")) + ";\n"
    (W / "data.js").write_text(js, encoding="utf-8")
    FRAG = (W / "ficha_form.html").read_text(encoding="utf-8")
    mark = "<script>\nfunction boot(){"
    for src, dst, emb in (("index_base.html", "index.html", False), ("index_base.html", "mobile.html", False), ("index_base.html", "index_unico.html", True), ("index_base.html", "mobile_unico.html", True)):
        import visual as V
        base = V.aplicar((W / src).read_text(encoding="utf-8"))
        if emb:
            base = base.replace("location.replace('mobile.html'", "location.replace('mobile_unico.html'")
            html = base.replace(mark, FRAG + "<script>\n" + js.replace("</", "<\\/") + "</script>\n" + mark, 1)
        else:
            html = base.replace(mark, FRAG + mark, 1)
        (W / dst).write_text(html, encoding="utf-8")
    # miniaturas (a ampliacao usa o original)
    from PIL import Image
    TH = IMG / "th"; TH.mkdir(exist_ok=True); nth = 0
    for f in IMG.glob("*"):
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg"): continue
        d = TH / (f.stem + ".jpg")
        if d.exists() and d.stat().st_mtime >= f.stat().st_mtime: continue
        try:
            im = Image.open(f).convert("RGB"); im.thumbnail((640, 640)); im.save(d, "JPEG", quality=74, optimize=True); nth += 1
        except Exception as e:
            print("sem miniatura (arquivo antigo/invalido):", f.name)
    print("miniaturas novas:", nth, "| MB:", round(sum(x.stat().st_size for x in TH.glob("*.jpg")) / 1048576, 1))
    for m in ("judo", "bjj"):
        n = len(data[m]["trans"]); print(m, n, "transições")
    print("imgs", len(list(IMG.glob("*.png"))))
