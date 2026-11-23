"""Tradução offline (Argos Translate) dos textos do app: EN→PT-BR e PT→EN, com glossário de Judô/BJJ e cache.
Rodar com o python do venv de tradução: D:\Claude\_toolchain\mt-venv\Scripts\python.exe i18n_mt.py
Saída: pipelines/i18n_dict.json  {"pt": {fonte_en: pt}, "en": {fonte_pt: en}}. Nomes em japonês nunca são traduzidos."""
import json, re, pathlib, sys
try:
    import truststore; truststore.inject_into_ssl()
except Exception: pass
import argostranslate.translate as AT
P = pathlib.Path(__file__).resolve().parent; W = P.parent / "webapp"
CACHE = P / "i18n_cache.json"; OUT = P / "i18n_dict.json"; MANUAL = P / "i18n_manual.json"
EN_SW = set("the of and to in is are a an with for on by from as at be or that this which when it its into than not can may if each their his her he she they will must shall".split())
PT_SW = set("o a os as de do da dos das e em um uma para com por que se na no nas nos é são ao à ou como mais sua seu pelo pela entre sobre quando deve deverá".split())
JP = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
def lang(s):
    w = re.findall(r"[a-zA-ZÀ-ÿ']+", s.lower())
    if len(w) < 2: return "?"
    e = sum(x in EN_SW for x in w); p = sum(x in PT_SW for x in w)
    if re.search(r"[ãõçáéíóúâêô]", s.lower()) and p >= e: return "pt"
    return "en" if e > p else ("pt" if p > e else "?")
# glossários (aplicados antes da MT; termos já no idioma de destino passam intactos)
G_EN_PT = [("rear naked choke", "mata-leão"), ("rear-naked choke", "mata-leão"), ("naked choke", "mata-leão"), ("knee on belly", "joelho na barriga"), ("back control", "controle das costas"),
 ("back mount", "montada nas costas"), ("full mount", "montada"), ("side control", "controle lateral"), ("closed guard", "guarda fechada"), ("close guard", "guarda fechada"), ("open guard", "guarda aberta"),
 ("half guard", "meia-guarda"), ("spider guard", "guarda aranha"), ("guard pass", "passagem de guarda"), ("guard passing", "passagem de guarda"), ("guard", "guarda"), ("mount position", "montada"), ("mount", "montada"),
 ("sweeps", "raspagens"), ("sweep", "raspagem"), ("takedowns", "quedas"), ("takedown", "queda"), ("submissions", "finalizações"), ("submission", "finalização"), ("chokes", "estrangulamentos"), ("choke", "estrangulamento"),
 ("armbar", "chave de braço"), ("armlock", "chave de braço"), ("leglock", "chave de perna"), ("footlock", "chave de pé"), ("heel hook", "chave de calcanhar"), ("kneebar", "chave de joelho"), ("triangle", "triângulo"),
 ("bear hug", "abraço de urso"), ("headlock", "gravata lateral"), ("double leg", "queda de duas pernas"), ("single leg", "queda de uma perna"), ("turtle", "tartaruga"), ("advantages", "vantagens"), ("advantage", "vantagem"),
 ("referee", "árbitro"), ("examinators", "examinadores"), ("examinator", "examinador"), ("athlete", "atleta"), ("opponent", "oponente"), ("breakfall", "queda (ukemi)"), ("belt", "faixa"), ("grips", "pegadas"), ("grip", "pegada"),
 ("hip throw", "projeção de quadril"), ("front kick", "chute frontal"), ("knee strike", "joelhada"), ("elbow strike", "cotovelada"), ("headbutt", "cabeçada"), ("punch", "soco"), ("escape", "saída"), ("MR ", "árbitro central "),
 ("points", "pontos"), ("point", "ponto"), ("bridge", "ponte")]
G_PT_EN = [("meia guarda", "half guard"), ("meia-guarda", "half guard"), ("guarda fechada", "closed guard"), ("guarda aberta", "open guard"), ("passagem de guarda", "guard pass"), ("guarda", "guard"), ("montada nas costas", "back mount"),
 ("montada", "mount"), ("raspagens", "sweeps"), ("raspagem", "sweep"), ("chave de braço", "armlock"), ("chave de perna", "leg lock"), ("chave de pé", "foot lock"), ("estrangulamentos", "chokes"), ("estrangulamento", "choke"),
 ("finalização", "submission"), ("mata-leão", "rear naked choke"), ("mata leão", "rear naked choke"), ("joelho na barriga", "knee on belly"), ("controle lateral", "side control"), ("controle das costas", "back control"),
 ("examinando", "examinee"), ("o baia", "the training partner"), ("baia", "training partner"), ("camarão", "shrimp (hip escape)"), ("upa", "bridge"), ("barrigada", "belly push"), ("tapão", "open-hand slap"), ("dojô", "dojo"),
 ("imobilizações", "pins"), ("imobilização", "pin"), ("projeções", "throws"), ("projeção", "throw"), ("queda", "fall"), ("faixa", "belt"), ("oponente", "opponent"), ("árbitro", "referee")]
def prot(s, glo):
    for a, b in sorted(glo, key=lambda x: -len(x[0])):
        s = re.sub(r"(?<![A-Za-zÀ-ÿ])" + re.escape(a) + r"(?![A-Za-zÀ-ÿ])", b, s, flags=re.I)
    return s
def mt(s, a, b, glo):
    if JP.search(s) and len(s) < 40: return s
    lines = s.split("\n"); out = []
    for ln in lines:
        ln0 = ln; ln = prot(ln, glo)
        if not re.search(r"[A-Za-zÀ-ÿ]{3}", ln): out.append(ln0); continue
        sents = re.split(r"(?<=[.!?;])\s+", ln); res = []
        for x in sents:
            if not x.strip(): continue
            try: res.append(AT.translate(x, a, b))
            except Exception as e: res.append(x)
        out.append(" ".join(res))
    return "\n".join(out)
def collect():
    t = (W / "data.js").read_text(encoding="utf-8"); first = t.split(";\nwindow.I18N", 1)[0]
    d = json.loads(first[len("window.DATA = "):].rstrip().rstrip(";"))
    en, pt = set(), set()
    def put(s, force=None):
        if not isinstance(s, str) or len(s.strip()) < 3 or JP.fullmatch(s.strip()) or re.fullmatch(r"[\d\s/.,:%\-–—·|→()pP]+", s) or s.startswith("img/") or s.startswith("http"): return
        l = force or lang(s)
        if l == "?" and not force and len(re.findall(r"[A-Za-zÀ-ÿ]{3,}", s)) >= 2 and re.search(r"[a-zà-ÿ]{4}", s) and not re.fullmatch(r"[A-Z][\w\-ōūŌŪ ]+( [A-Z][\w\-ōūŌŪ]+)*", s.strip()): l = "pt"
        if l == "en": en.add(s)
        elif l == "pt": pt.add(s)
    def walk(o, ctx):
        if isinstance(o, str): put(o); return
        if isinstance(o, list):
            for x in o: walk(x, ctx)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("img", "url", "id", "refs", "arq", "pat", "bde", "bpara", "ja", "sj", "sp", "rom", "f", "col", "form"): continue
                if k == "en" and isinstance(v, str): put(v, "en"); continue
                if k == "pt" and isinstance(v, str): put(v, "pt"); continue
                if k == "nm": walk(v, dict(ctx, nm=True)); continue
                if k == "t" and isinstance(v, str): put(v, "en" if ctx.get("bjj") else "pt"); continue
                if k in ("judo", "bjj"): walk(v, dict(ctx, bjj=(k == "bjj"))); continue
                if isinstance(v, str): put(v)
                else: walk(v, ctx)
    walk(d, {}); return en, pt
POS_PT = [(r"\bsaida\b", "saída"), (r"\bSaida\b", "Saída"), (r"gravidade lateral", "gravata lateral"), (r"Gravidade lateral", "Gravata lateral"), (r"Gragata", "Gravata"), (r"\bacções\b", "ações"), (r"\bcontrolo\b", "controle"), (r"\bcontrolo\b", "controle"), (r"pára-quedas", "chute"), (r"\bMetade passagem de guarda", "Passagem de meia-guarda"), (r"\bmontanha\b", "montada")]
def pos(s):
    for a, b in POS_PT: s = re.sub(a, b, s)
    return s
def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {"pt": {}, "en": {}}
    manual = json.loads(MANUAL.read_text(encoding="utf-8")) if MANUAL.exists() else {"pt": {}, "en": {}}
    en, pt = collect(); n = 0
    print("EN→PT:", len(en), "| PT→EN:", len(pt)); sys.stdout.flush()
    for s in sorted(en, key=len):
        if s.lower() in manual["pt"]: cache["pt"][s] = manual["pt"][s.lower()]; continue
        if s not in cache["pt"]: cache["pt"][s] = pos(mt(s, "en", "pt", G_EN_PT)); n += 1
        if n % 100 == 0 and n: CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    for s in sorted(pt, key=len):
        if s.lower() in manual["en"]: cache["en"][s] = manual["en"][s.lower()]; continue
        if s not in cache["en"]: cache["en"][s] = mt(s, "pt", "en", G_PT_EN); n += 1
        if n % 100 == 0 and n: CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    out = {"pt": {s: pos(cache["pt"][s]) for s in en if cache["pt"].get(s) and cache["pt"][s] != s}, "en": {s: cache["en"][s] for s in pt if cache["en"].get(s) and cache["en"][s] != s}}
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8"); print("novas:", n, "| dict pt:", len(out["pt"]), "en:", len(out["en"]))
main()
