"""Gera site/explorar/dados.js (dados do explorador Judô + Jiu-Jitsu).
Entradas: site/livro.html (livro interativo), source/videos.py, source/glossary.py e o data.js do app (webapp local do projeto Judo_BJJ).
Uso: python source/portal/build_dados.py <data.js do app> [<pasta pipelines do projeto, com glossario.py>]"""
import sys, re, json, html, pathlib
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "source"))
import videos as V
import glossary as GLOS

DATA_JS = pathlib.Path(sys.argv[1])
PIPE = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None
if PIPE and PIPE.exists():
    sys.path.insert(0, str(PIPE))
    try:
        import glossario as GL
        KD = GL.KD; norm = GL.norm
    except Exception as e:
        print("sem glossario.py local:", e); KD = {}; norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
else:
    KD = {}; norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

txt = lambda x: re.sub(r"\s+", " ", x.get_text(" ", strip=True)) if x else ""
import unicodedata
slug = lambda n: re.sub(r"[^a-z0-9]+", "-", "".join(c for c in unicodedata.normalize("NFD", n.lower()) if not unicodedata.combining(c))).strip("-")

# ---------------- dados do app ----------------
raw = DATA_JS.read_text(encoding="utf-8")
first, _, rest = raw.partition(";\nwindow.I18N=")
APP = json.loads(first[len("window.DATA = "):].rstrip().rstrip(";"))
I18N = json.loads(rest.rstrip().rstrip(";")) if rest else {"pt": {}}
PTMAP = I18N.get("pt", {})
def pt(s):  # texto em inglês -> português (dicionário do app)
    return PTMAP.get(s, s) if isinstance(s, str) else s

# ---------------- livro ----------------
soup = BeautifulSoup((ROOT / "site" / "livro.html").read_text(encoding="utf-8"), "html.parser")
def sec(i): return soup.find("section", id=i)
def tabela(sid, k=0):
    t = sec(sid).find_all("table")[k]
    return [r.find_all(["td", "th"]) for r in t.find_all("tr")][1:]
def techs(cell): return [slug(a["data-name"]) for a in cell.find_all("a", class_="tech")]

# nomes em português das 100 técnicas (convenção do judô brasileiro; ver aviso no explorador)
PT_NAMES = {
 "seoi-nage": "Projeção por cima do ombro", "ippon-seoi-nage": "Projeção por cima do ombro com uma mão", "seoi-otoshi": "Queda por cima do ombro", "tai-otoshi": "Queda com o corpo", "kata-guruma": "Roda de ombro",
 "sukui-nage": "Projeção em concha", "obi-otoshi": "Queda pela faixa", "uki-otoshi": "Queda flutuante", "sumi-otoshi": "Queda de canto", "yama-arashi": "Tempestade da montanha", "obi-tori-gaeshi": "Contragolpe pegando a faixa",
 "morote-gari": "Ceifada com as duas mãos (baianada)", "kuchiki-taoshi": "Queda da árvore podre", "kibisu-gaeshi": "Contragolpe no calcanhar", "uchi-mata-sukashi": "Esquiva de uchi-mata", "ko-uchi-gaeshi": "Contragolpe de ko-uchi-gari",
 "uki-goshi": "Quadril flutuante", "o-goshi": "Grande quadril", "koshi-guruma": "Roda de quadril", "tsurikomi-goshi": "Quadril com puxada", "sode-tsurikomi-goshi": "Quadril com puxada pela manga", "harai-goshi": "Varrida de quadril",
 "tsuri-goshi": "Quadril com elevação", "hane-goshi": "Quadril saltado", "utsuri-goshi": "Troca de quadril", "ushiro-goshi": "Quadril por trás",
 "de-ashi-harai": "Varrida do pé avançado", "hiza-guruma": "Roda de joelho", "sasae-tsurikomi-ashi": "Bloqueio do pé com puxada", "o-soto-gari": "Grande ceifada externa", "o-uchi-gari": "Grande ceifada interna",
 "ko-soto-gari": "Pequena ceifada externa", "ko-uchi-gari": "Pequena ceifada interna", "okuri-ashi-harai": "Varrida dos dois pés", "uchi-mata": "Coxa interna", "ko-soto-gake": "Pequeno gancho externo", "ashi-guruma": "Roda de perna",
 "harai-tsurikomi-ashi": "Varrida do pé com puxada", "o-guruma": "Grande roda", "o-soto-guruma": "Grande roda externa", "o-soto-otoshi": "Grande queda externa", "tsubame-gaeshi": "Contragolpe da andorinha",
 "o-soto-gaeshi": "Contragolpe de o-soto-gari", "o-uchi-gaeshi": "Contragolpe de o-uchi-gari", "hane-goshi-gaeshi": "Contragolpe de hane-goshi", "harai-goshi-gaeshi": "Contragolpe de harai-goshi", "uchi-mata-gaeshi": "Contragolpe de uchi-mata",
 "tomoe-nage": "Projeção em círculo", "sumi-gaeshi": "Queda de canto", "hikikomi-gaeshi": "Queda puxando para dentro", "tawara-gaeshi": "Queda do saco de arroz", "ura-nage": "Projeção por trás",
 "yoko-otoshi": "Queda lateral", "tani-otoshi": "Queda do vale", "hane-makikomi": "Projeção saltada envolvente", "soto-makikomi": "Projeção envolvente externa", "uchi-makikomi": "Projeção envolvente interna", "uki-waza": "Técnica flutuante",
 "yoko-wakare": "Separação lateral", "yoko-guruma": "Roda lateral", "yoko-gake": "Gancho lateral", "daki-wakare": "Separação abraçando", "o-soto-makikomi": "Grande envolvente externa", "uchi-mata-makikomi": "Uchi-mata envolvente",
 "harai-makikomi": "Varrida envolvente", "ko-uchi-makikomi": "Pequena envolvente interna", "kani-basami": "Tesoura de caranguejo", "kawazu-gake": "Gancho do sapo",
 "kesa-gatame": "Controle em echarpe", "kuzure-kesa-gatame": "Echarpe modificada", "ushiro-kesa-gatame": "Echarpe por trás", "kata-gatame": "Controle de ombro", "kami-shiho-gatame": "Quatro pontos por cima",
 "kuzure-kami-shiho-gatame": "Quatro pontos superior modificado", "yoko-shiho-gatame": "Quatro pontos lateral", "tate-shiho-gatame": "Quatro pontos montado", "uki-gatame": "Controle flutuante", "ura-gatame": "Controle invertido",
 "nami-juji-jime": "Estrangulamento em cruz normal", "gyaku-juji-jime": "Estrangulamento em cruz invertido", "kata-juji-jime": "Estrangulamento em meia cruz", "hadaka-jime": "Estrangulamento sem kimono (mata-leão)",
 "okuri-eri-jime": "Estrangulamento deslizando a gola", "kataha-jime": "Estrangulamento com uma asa", "katate-jime": "Estrangulamento com uma mão", "ryote-jime": "Estrangulamento com as duas mãos", "sode-guruma-jime": "Estrangulamento em roda pela manga",
 "tsukkomi-jime": "Estrangulamento com ataque", "sankaku-jime": "Estrangulamento em triângulo", "do-jime": "Estrangulamento de tronco",
 "ude-garami": "Chave de braço enrolada", "juji-gatame": "Chave de braço cruzada", "ude-gatame": "Chave de braço reta", "hiza-gatame": "Chave de joelho", "waki-gatame": "Chave de axila", "hara-gatame": "Chave de barriga",
 "ashi-gatame": "Chave de perna", "te-gatame": "Chave de mão", "sankaku-gatame": "Chave triangular", "ashi-garami": "Enrolamento de perna",
}
IMGDIR = ROOT / "site" / "assets" / "img"
imgs = {}
for f in IMGDIR.glob("*.webp"):
    st = f.stem; k = re.sub(r"[^a-z]", "", re.sub(r"^(tri|kae|ren|pro|fig)_", "", st))
    pref = st.split("_")[0] if st.split("_")[0] in ("tri", "kae", "ren", "pro") else "fig"
    imgs.setdefault(k, {})[pref] = "assets/img/" + f.name

# ---------------- técnicas ----------------
T = {}
for gname, kind, lst in V.GROUPS:
    for nome, kanji, yt in lst:
        s = slug(nome); key = norm(nome)
        kd = KD.get(key, {})
        T[s] = {"id": s, "nome": nome, "ja": kanji or kd.get("ja", ""), "en": kd.get("en", ""), "pt": PT_NAMES.get(s, ""), "grupo": gname, "tipo": "nage" if kind == "nage" else "katame", "yt": yt, "ijf": V.ijf_url(nome) if hasattr(V, "ijf_url") else "https://judo.ijf.org/techniques/" + nome,
                "imgs": [], "kaeshi": [], "respondeA": [], "combos": [], "katame": [], "faixas": [], "ficha": None}
for s, o in T.items():
    k = re.sub(r"[^a-z]", "", s); d = imgs.get(k, {})
    for p, lab in (("tri", "Três fases: kuzushi, tsukuri e kake"), ("fig", "Ilustração"), ("kae", "Contragolpe"), ("pro", "Ação proibida")):
        if p in d: o["imgs"].append({"src": d[p], "cap": lab})
# fichas (40 técnicas do Gokyo)
for r in tabela("sec-fichas-de-estudo-do-gokyo-40-tecnicas"):
    ts = techs(r[1])
    if not ts or ts[0] not in T: continue
    T[ts[0]]["ficha"] = {"faixa": txt(r[0]), "classe": txt(r[2]), "kuzushi": txt(r[3]), "acao": txt(r[4])}
# kaeshi-waza
KAE = []
for r in tabela("sec-kaeshi-waza-contragolpes"):
    a = techs(r[0]); b = techs(r[2])
    if not a: continue
    KAE.append({"contra": a[0], "grupo": txt(r[1]), "responde": b, "acao": txt(r[3])})
    for resp in b:
        if resp in T: T[resp]["kaeshi"].append({"id": a[0], "acao": txt(r[3])})
    if a[0] in T: T[a[0]]["respondeA"] = b
# renraku-waza
REN = []
_sx = sec("sec-renraku-waza-combinacoes-em-pe-e-no-solo")
_fig = {}
for fg in _sx.find_all("figure"):
    im = fg.find("img"); cap = txt(fg.find("figcaption") or fg)
    m = re.match(r"([A-Za-z\-]+) → ([A-Za-z\-]+)", cap)
    if im and m: _fig[(slug(m.group(1)), slug(m.group(2)))] = im.get("src")
for tb in _sx.find_all("table"):
    for r in tb.find_all("tr")[1:]:
        cs = r.find_all("td")
        if len(cs) < 3: continue
        tipo = txt(cs[0]); logica = txt(cs[1])
        for part in cs[2].get_text(" ", strip=True).split(";"):
            chain = [slug(x) for x in part.split("→") if x.strip()]
            chain = [c for c in chain if c in T]
            if len(chain) >= 2 and not any(c["cadeia"] == chain for c in REN):
                REN.append({"tipo": tipo, "logica": logica, "cadeia": chain, "img": _fig.get((chain[0], chain[1]), "")})
                for c in chain: T[c]["combos"].append(len(REN) - 1)
for i, c in enumerate(REN):
    for x in c["cadeia"]:
        if x in T and T[x]["tipo"] == "nage":
            T[x]["katame"] += [y for y in c["cadeia"] if y in T and T[y]["tipo"] == "katame" and y not in T[x]["katame"]]
        elif x in T:
            T[x]["katame"] += [y for y in c["cadeia"] if y in T and y != x and y not in T[x]["katame"]]
# ---------------- faixas do Judô (livro + app) ----------------
rows_nage = tabela("sec-programa-detalhado-por-faixa-do-11o-kyu-a-faixa-preta", 0)
rows_fund = tabela("sec-programa-detalhado-por-faixa-do-11o-kyu-a-faixa-preta", 1)
rows_prog = tabela("sec-programa-de-exame-das-faixas-kyu-11o-ao-1o", 0)
rows_idade = tabela("sec-faixas-idade-minima-e-carencia", 0)
print("linhas por faixa:", len(rows_nage), len(rows_fund), len(rows_prog), len(rows_idade), [txt(r[0]) for r in rows_nage])
NAO_COMP = {"Kata", "Vocabulário", "Histórico, princípios e cultura", "Provas teóricas", "Provas práticas", "Atividades de ensino", "Arbitragem", "Outros critérios", "Elegibilidade"}
FUND = {"Reverência e quedas (Rei/Ukemi)", "Fundamentos de aplicação"}
def cats(tr):
    g = {}
    for it in tr["itens"]:
        g.setdefault(it["c"], []).append({"t": it["t"], "tm": [{"ja": m["ja"], "rom": m["rom"], "en": m["en"], "pt": m.get("pt") or pt(m["en"])} for m in it.get("tm", [])]})
    out = []
    for c, its in g.items():
        n = tr.get("catnm", {}).get(c, {})
        out.append({"id": slug(c), "nome": c, "ja": n.get("ja", ""), "en": n.get("en", ""), "pt": n.get("pt", ""), "itens": its, "grupo": "fund" if c in FUND else ("nao" if c in NAO_COMP else "tec")})
    return out
def colors(tr): return {"de": tr["bde"], "para": tr["bpara"]}
JUDO_BELTS = []
for i, tr in enumerate(APP["judo"]["trans"]):
    b = {"id": tr["id"], "titulo": tr["titulo"], "sub": tr["sub"], "cores": colors(tr), "fatos": tr["fatos"], "nota": tr.get("nota", ""), "cats": cats(tr), "pags": tr.get("pags", [])}
    if i < len(rows_nage):
        rn = rows_nage[i]; rf = rows_fund[i]; rp = rows_prog[i] if i < len(rows_prog) else None
        b["nage"] = [x for x in techs(rn[1]) if x in T]; b["katame"] = [x for x in techs(rn[2]) if x in T]
        b["renraku"] = txt(rn[3]); b["kaeshi"] = txt(rn[4]); b["renrakuSlugs"] = [x for x in techs(rn[3]) if x in T]; b["kaeshiSlugs"] = [x for x in techs(rn[4]) if x in T]
        b["kihon"] = txt(rf[1]); b["kata"] = txt(rf[2]); b["teoria"] = txt(rf[3])
        if rp: b["quant"] = {"Ukemi e fundamentos": txt(rp[1]), "Nage-waza": txt(rp[2]), "Katame-waza": txt(rp[3]), "Kata": txt(rp[4]), "Teoria e cultura": txt(rp[5])}
        for x in b["nage"] + b["katame"]:
            if tr["id"] not in T[x]["faixas"]: T[x]["faixas"].append(tr["id"])
    JUDO_BELTS.append(b)
IDADE = [[txt(c) for c in r] for r in rows_idade]
# proibidas (IJF)
pro = sec("sec-tecnicas-e-acoes-proibidas-regras-ijf-vigentes")
PROIB = {"hansoku": [], "shido": []}
cur = None
for el in pro.find_all(["h3", "ul", "p"]):
    if el.name == "h3": cur = "hansoku" if "Hansoku" in txt(el) else ("shido" if "shido" in txt(el).lower() else None)
    elif el.name == "ul" and cur: PROIB[cur] += [txt(li) for li in el.find_all("li")]
PROIB["imgs"] = sorted(["assets/img/" + f.name for f in IMGDIR.glob("pro_*.webp")])
# glossário
GLO = [{"termo": g[0], "kanji": g[1] or "", "def": g[2]} for g in GLOS.GLOSSARY]
# referências ABNT do livro
LIVRO_REFS = [txt(li) for li in sec("sec-referencias").find_all("li")]
# extras de vídeo
EXTRAS = [{"grupo": g[0], "itens": [{"t": x[0], "ja": x[1], "yt": x[2]} for x in g[1]]} for g in V.EXTRAS]

# ---------------- Jiu-Jitsu (app) ----------------
BJJ_BELTS = []; COMP = None
BJJ_MATRIZ = {
 "colunas": ["4 a 12 anos", "13 a 15 anos", "16 e 17 anos (todas as faixas) e faixa branca (Adulto a Master 7)", "Adulto a Master 7 (azul e roxa)", "Adulto a Master 7 (marrom e preta), exceto Sem Kimono", "Adultos (marrom e preta) Sem Kimono"],
 "golpes": [
  ["Posição de finalização forçando a abertura da virilha", [0]], ["Estrangulamento que force a cervical", [0, 1]], ["Chave de pé reta", [0, 1]], ["Estrangulamento utilizando a manga do kimono (Ezequiel)", [0, 1]],
  ["Gravata técnica de frente", [0, 1]], ["Omoplata", [0, 1]], ["Triângulo (puxando a cabeça)", [0, 1]], ["Triângulo de mão", [0, 1]],
  ["Chave que pressione as costelas ou os rins dentro da guarda fechada", [0, 1, 2]], ["Mão de vaca", [0, 1, 2]], ["Single leg com a cabeça para fora (**)", [0, 1, 2]],
  ["Chave de bíceps", [0, 1, 2, 3]], ["Chave de panturrilha", [0, 1, 2, 3]], ["Leg lock (chave de joelho reta)", [0, 1, 2, 3]], ["Mata-leão no pé", [0, 1, 2, 3]],
  ["Na chave de pé reta, girar na direção do pé que não está sendo atacado", [0, 1, 2, 3]], ["Chave de calcanhar", [0, 1, 2, 3, 4]], ["Chave que torça o joelho", [0, 1, 2, 3, 4]],
  ["Cruzada de perna (ler detalhes na página 32)", [0, 1, 2, 3, 4]], ["No mata-leão no pé, aplicar a pressão para o lado externo do pé", [0, 1, 2, 3, 4]],
  ["Bate estaca", [0, 1, 2, 3, 4, 5]], ["Chave de cervical", [0, 1, 2, 3, 4, 5]], ["Queda-tesoura", [0, 1, 2, 3, 4, 5]], ["Torcer os dedos para trás", [0, 1, 2, 3, 4, 5]],
  ["Segurar na faixa do adversário e projetá-lo de cabeça ao solo enquanto se defende de um single leg com a cabeça para fora", [0, 1, 2, 3, 4, 5]], ["Suplex derrubando o adversário de cabeça ou pescoço ao solo", [0, 1, 2, 3, 4, 5]]],
 "fonte": "Livro de Regras IBJJF/CBJJ 2024 (PT), v6.1, p. 29: tabela de golpes proibidos por idade e faixa. (**) apesar de proibida, a técnica não é punida.",
 "extra_branca": "Faixa branca, em qualquer idade: é falta grave pular para colocar o adversário que está em pé na guarda fechada; a luta recomeça com os dois em pé. (Folha “Golpes proibidos” da IBJJF, 2024.)"}
for tr in APP["bjj"]["trans"]:
    ab = tr["abas"]
    jj = next((a for a in ab if a.get("tipo") == "jjif"), None); fi = next((a for a in ab if a.get("tipo") == "ficha"), None); co = next((a for a in ab if a.get("tipo") == "componentes"), None)
    if COMP is None and co: COMP = co
    secs = []
    if jj:
        for s in jj["secoes"]:
            secs.append({"cat": s["cat"], "pt": s.get("catpt", ""), "itens": [{"t": x["t"], "nm": x.get("nm")} for x in s["itens"]], "imgs": s.get("imgs", [])})
    b = {"id": tr["id"], "titulo": tr["titulo"], "sub": tr.get("sub", ""), "cores": colors(tr), "fatos": tr.get("fatos", []), "nota": tr.get("nota", ""), "secoes": secs, "intro": (jj or {}).get("intro", ""),
         "ficha": ({"criterios": fi["criterios"], "opcoes": fi["opcoes"], "secoes": fi["secoes_ficha"], "carga": fi["carga"], "img": fi["img"]} if fi else None)}
    BJJ_BELTS.append(b)
def slim(g):
    return {"id": g["id"], "nome": g["nome"], "desc": g["desc"], "nm": g.get("nm"), "itens": [{"t": i["t"], "c": i["c"], "nm": i.get("nm")} for i in g.get("itens", [])],
            "fotos": [{"img": f["img"], "cap": pt(f["cap"]), "fonte": f["fonte"]} for f in g.get("fotos", [])[:12]], "videos": g.get("videos", []),
            "regra": [{"titulo": pt(r["titulo"]), "texto": pt(r["texto"])} for r in g.get("regra", [])],
            "subs": [{"id": s["id"], "nome": s["nome"], "desc": s.get("desc", ""), "nm": s.get("nm"), "itens": [{"t": i["t"], "c": i["c"], "nm": i.get("nm")} for i in s.get("itens", [])], "videos": s.get("videos", []),
                      "blocos": [{"titulo": pt(b["titulo"]), "texto": pt(b.get("texto", "")), "nm": b.get("nm"), "fonte": b.get("fonte", ""), "fotos": [{"img": f["img"], "cap": pt(f["cap"]), "fonte": f["fonte"]} for f in b.get("fotos", [])]} for b in s.get("blocos", [])],
                      "fotos": [{"img": f["img"], "cap": pt(f["cap"]), "fonte": f["fonte"]} for f in s.get("fotos", [])[:8]]} for s in g.get("subs", [])] if g.get("subs") else []}
BJJ_COMP = [slim(g) for g in (COMP["grupos"] if COMP else [])]
# ---------------- saída ----------------
REFS = [{k: r.get(k, "") for k in ("id", "titulo", "org", "ano", "url", "arq")} for r in APP["REFS"] if r["id"] != "app"]
OUT = {"tecnicas": T, "kaeshi": KAE, "renraku": REN, "judo": {"faixas": JUDO_BELTS, "idade": IDADE, "proibidas": PROIB, "glossario": GLO, "extras": EXTRAS, "refsLivro": LIVRO_REFS,
        "grupos": [{"nome": g[0], "tipo": g[1], "itens": [slug(x[0]) for x in g[2]]} for g in V.GROUPS]},
       "bjj": {"faixas": BJJ_BELTS, "comp": BJJ_COMP, "matriz": BJJ_MATRIZ}, "refs": REFS}
dest = ROOT / "site" / "explorar"; dest.mkdir(exist_ok=True)
(dest / "dados.js").write_text("window.PORTAL=" + json.dumps(OUT, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print("dados.js:", round((dest / "dados.js").stat().st_size / 1024), "KB;", len(T), "técnicas;", len(KAE), "kaeshi;", len(REN), "combinações;", len(JUDO_BELTS), "faixas judô;", len(BJJ_BELTS), "faixas BJJ;", len(BJJ_COMP), "grupos de componentes")
print("com PT:", sum(1 for t in T.values() if t["pt"]), "com EN:", sum(1 for t in T.values() if t["en"]), "com imagem:", sum(1 for t in T.values() if t["imgs"]), "com ficha:", sum(1 for t in T.values() if t["ficha"]))
