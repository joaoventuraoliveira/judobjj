"""Dicionários PT-BR -> EN do portal (página inicial, explorador e livro). Tradução offline (Argos) com glossário e cache.
Rodar com o python do venv de tradução (precisa de argostranslate e beautifulsoup4):
  python source/portal/i18n_portal.py <pasta pipelines do projeto> <data.js do app>
Saída: site/assets/i18n-landing.js, i18n-explorar.js, i18n-livro.js  (window.I18N_PAGE = {en:{pt:en}, rules:[...]}).
Ordem de busca de cada texto: manual -> nomes de técnicas (PT->EN do próprio explorador) -> dicionário do app -> UI do app -> tradução automática."""
import sys, re, json, pathlib, importlib.util, unicodedata
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[2]
PIPE = pathlib.Path(sys.argv[1]); DATA_JS = pathlib.Path(sys.argv[2])
sys.path.insert(0, str(PIPE))
SEM_MT = "--sem-mt" in sys.argv
sys.argv = [a for a in sys.argv if a != "--sem-mt"]
try:
    if SEM_MT: raise ImportError("sem MT")
    import i18n_mt as M          # lang(), prot(), mt(), pos(), glossários (não executa main)
except ImportError:
    class M:                      # modo sem tradução automática: só dicionários e regras
        EN_SW = set("the of and to in is are a an with for on by from as at be or that this which when it its into than not can may if each their his her he she they will must shall".split())
        PT_SW = set("o a os as de do da dos das e em um uma para com por que se na no nas nos é são ao à ou como mais sua seu pelo pela entre sobre quando deve deverá".split())
        @staticmethod
        def lang(s):
            w = re.findall(r"[a-zA-ZÀ-ÿ']+", s.lower())
            if len(w) < 2: return "?"
            e = sum(x in M.EN_SW for x in w); p = sum(x in M.PT_SW for x in w)
            if re.search(r"[ãõçáéíóúâêô]", s.lower()) and p >= e: return "pt"
            return "en" if e > p else ("pt" if p > e else "?")
        G_PT_EN = []
        @staticmethod
        def mt(s, a, b, g): return s
import i18n_ui as UI
CACHE = ROOT / "source" / "portal" / "i18n_portal_cache.json"
MANUAL = ROOT / "source" / "portal" / "i18n_portal_manual.json"
cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
manual = json.loads(MANUAL.read_text(encoding="utf-8")) if MANUAL.exists() else {}

raw = DATA_JS.read_text(encoding="utf-8"); first, _, rest = raw.partition(";\nwindow.I18N=")
APP_EN = json.loads(rest.rstrip().rstrip(";")).get("en", {}) if rest else {}
UI_EN = UI.UI_EN
norm = lambda s: re.sub(r"\s+", " ", s).strip()
JP = re.compile(r"[぀-ヿ一-鿿]")

# ---- nomes de técnicas: PT -> EN do explorador ----
PORTAL = json.loads((ROOT / "site" / "explorar" / "dados.js").read_text(encoding="utf-8")[len("window.PORTAL="):].rstrip().rstrip(";"))
NAMES = {}
for t in PORTAL["tecnicas"].values():
    if t["pt"] and t["en"]: NAMES[t["pt"]] = t["en"]
def _bjj_items():
    for f in PORTAL["bjj"]["faixas"]:
        for s in f["secoes"]:
            for i in s["itens"]:
                n = i.get("nm") or {}
                if n.get("pt") and n.get("en"): NAMES[n["pt"]] = n["en"]
    for g in PORTAL["bjj"]["comp"]:
        for i in g["itens"]:
            n = i.get("nm") or {}
            if n.get("pt") and n.get("en"): NAMES[n["pt"]] = n["en"]
_bjj_items()
# faixas: "Branca → Cinza" etc.
BELT = UI.BELT_EN
def belt_en(s):
    r = re.sub(r"\b(" + "|".join(map(re.escape, BELT)) + r")\b", lambda m: BELT[m.group(1)], s)
    r = re.sub(r"(\d+)º Kyû", r"\1th Kyu", r); r = r.replace("º Dan", "th Dan")
    return r
BELT_STR = set()
for f in PORTAL["judo"]["faixas"] + PORTAL["bjj"]["faixas"]:
    BELT_STR.add(f["titulo"]); BELT_STR.add(f.get("sub", ""))
for row in PORTAL["judo"]["idade"]:
    for c in row: BELT_STR.add(c)

def traduzir(s):
    k = norm(s)
    if k in manual: return manual[k]
    if k in BELT_STR and re.search(r"Branca|Cinza|Amarela|Laranja|Verde|Azul|Roxa|Marrom|Preta|Vermelha|Kyû|Dan", k): return belt_en(k)
    if k in NAMES: return NAMES[k]
    if k in UI_EN: return UI_EN[k]
    if k in APP_EN: return APP_EN[k]
    if k in cache: return cache[k]
    if SEM_MT: return k            # sem MT: texto fica em português (nada é gravado no cache)
    r = M.mt(k, "pt", "en", M.G_PT_EN)
    cache[k] = r; return r

def eh_pt(s):
    k = norm(s)
    if len(k) < 3 or JP.fullmatch(k) or not re.search(r"[A-Za-zÀ-ÿ]{2}", k): return False
    if re.fullmatch(r"[\d\s/.,:%\-–—·|→()pP]+", k) or k.startswith(("http", "img/", "assets/", "#")): return False
    l = M.lang(k)
    if l == "pt": return True
    if l == "en": return False
    # indeterminado: texto com 2+ palavras minúsculas ou acentos -> PT; nomes próprios/romaji ficam
    if re.search(r"[ãõçáéíóúâêôà]", k.lower()): return True
    w = re.findall(r"[a-zà-ÿ]{4,}", k)
    return len(w) >= 2 and not re.fullmatch(r"[A-Z][\w\-ōūŌŪ]*( [A-Z][\w\-ōūŌŪ]*)*", k)

def walk_strings(o, out):
    if isinstance(o, str): out.add(o)
    elif isinstance(o, list):
        for x in o: walk_strings(x, out)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ("id", "src", "img", "yt", "url", "ija", "ijf", "arq", "imgs", "cores", "ja", "rom"): continue
            walk_strings(v, out)

# ---- coletores ----
def html_strings(path, attrs=("alt", "title", "aria-label", "placeholder", "data-ai", "data-cap")):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser"); out = set()
    for t in soup.find_all(string=True):
        p = t.parent.name if t.parent else ""
        if p in ("script", "style", "noscript") or isinstance(t, type(soup.Comment if hasattr(soup, "Comment") else str)) and False: continue
        if t.__class__.__name__ in ("Comment", "Doctype", "CData"): continue
        out.add(norm(str(t)))
    for e in soup.find_all(True):
        for a in attrs:
            if e.get(a): out.add(norm(e[a]))
    d = soup.find("meta", attrs={"name": "description"})
    if d and d.get("content"): out.add(norm(d["content"]))
    if soup.title: out.add(norm(soup.title.get_text()))
    return {s for s in out if s}

EXTRA_RULES = [[r"^(.+) · programa técnico da JJIF para (.+)$", "$1 · JJIF technical program for $2"], [r"^Linked technique: (.+)$", "Linked technique: $1"], [r"^Anotações sobre (.+)$", "Notes on $1"], [r"^Fonte do nome japonês: (.*)\. Português: (.*)\.$", "Source of the Japanese name: $1. Portuguese: $2."], [r"^(.+): Três fases: kuzushi, tsukuri e kake$", "$1: Three phases: kuzushi, tsukuri and kake"], [r"^Renraku-waza: combinações com (.+)$", "Renraku-waza: combinations with $1"], [r"^Assistir aqui: Saídas do (.+)$", "Watch here: Escapes from $1"], [r"^Assistir aqui: (.+)$", "Watch here: $1"], [r"^(.+): Ilustração$", "$1: Illustration"], [r"^(.+): Ação proibida$", "$1: Prohibited action"], [r"^Prévia do vídeo: (.+)$", "Video preview: $1"], [r"^(\d+) nova\(s\) · (\d+) no total$", "$1 new · $2 in total"], [r"^(\d+) anos \+ (\d+) anos de Zempo$", "$1 years + $2 years of Zempo"], [r"^(\d+) meses \+ (\d+) anos? de Zempo$", "$1 months + $2 year(s) of Zempo"], [r"^(\d+) anos \(homologação IJF ?\)$", "$1 years (IJF approval)"], [r"^Saídas do (.+)$", "Escapes from $1"], [r"^(\d+) tópicos?$", "$1 topics"], [r"^(\d+) combinações$", "$1 combinations"], [r"^(\d+) imobilizações$", "$1 pins"]]
def build(nome, strings, extra_rules=EXTRA_RULES):
    pt = sorted({norm(s) for s in strings if eh_pt(s)}, key=len)
    print(nome, ":", len(pt), "textos a traduzir"); sys.stdout.flush()
    dic = {}; n = 0
    for s in pt:
        had = norm(s) in cache
        dic[s] = traduzir(s)
        if not had: n += 1
        if n and n % 100 == 0: CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    dic = {k: v for k, v in dic.items() if v and v != k}
    rules = [r for r in UI.RULES_EN] + list(extra_rules)
    out = ROOT / "site" / "assets" / f"i18n-{nome}.js"
    out.write_text("window.I18N_PAGE=" + json.dumps({"en": dic, "rules": rules}, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(nome, "(sem MT)" if SEM_MT else "", ": gravado", len(dic), "entradas;", round(out.stat().st_size / 1024), "KB; novas via MT:", n); sys.stdout.flush()

what = sys.argv[3:] or ["landing", "explorar", "livro"]
if "landing" in what: build("landing", html_strings(ROOT / "site" / "index.html"))
if "explorar" in what:
    S = set(json.loads((ROOT / "source" / "portal" / "explorar_strings.json").read_text(encoding="utf-8")))
    S = {s[1:] if s.startswith("@") else s for s in S}
    walk = set(); walk_strings(PORTAL, walk); S |= walk
    S |= html_strings(ROOT / "site" / "explorar" / "index.html")
    build("explorar", S)
if "livro" in what: build("livro", html_strings(ROOT / "site" / "livro.html"))
