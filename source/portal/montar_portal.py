"""Monta o portal (Judô + Jiu-Jitsu) em site/: página inicial, livro (livro.html) e app faixa a faixa (site/app).
Uso: python source/portal/montar_portal.py <pasta_www_do_app>
O app vem do projeto local Judo_BJJ (webapp gerado por pipelines/gerar_webapp_dados.py; ver source/app-gerador/).
Só miniaturas (img/th) são publicadas; a ampliação usa a própria miniatura, com a fonte sempre citada."""
import sys, re, json, shutil, html, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import layout_css as LC
ROOT = pathlib.Path(__file__).resolve().parents[2]; SITE = ROOT / "site"
def app(www):
    www = pathlib.Path(www); out = SITE / "app"
    if out.exists(): shutil.rmtree(out)
    (out / "img" / "th").mkdir(parents=True)
    h = (www / "index.html").read_text(encoding="utf-8")
    a = '$("#dimg").src=th.dataset.img;'; assert a in h
    h = h.replace(a, '$("#dimg").src=thumbUrl(th.dataset.img);', 1)
    b = '<div class="brand">Faixa a faixa</div>'; assert b in h
    h = h.replace(b, '<a class="brand" href="../" aria-label="Voltar ao início do portal">Faixa a faixa</a>', 1)
    h = h.replace("</head>", "<style>a.brand{color:var(--ink);text-decoration:none}</style><style>" + (ROOT / "source" / "portal" / "app_polish.css").read_text(encoding="utf-8") + "</style></head>", 1)
    # preferências compartilhadas (tema, layout, idioma) e escolha de layout PC/celular
    h = h.replace('<html lang="pt-BR" data-theme="dark">', '<html lang="pt-BR">', 1)
    h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<script src="../assets/prefs.js"></script>\n<link rel="stylesheet" href="../assets/prefs.css">', 1)
    h = h.replace('<input class="search" id="q"', '<div class="prefs-bar" data-prefs="layout"></div>\n    <input class="search" id="q"', 1)
    a = 'let LANG=store.get("lang")==="en"?"en":"pt";'; assert a in h
    h = h.replace(a, 'let LANG=(window.JTPrefs&&JTPrefs.state.lang)||"pt";', 1)
    a = 'store.set("lang",LANG==="en"?"pt":"en"); location.reload()'; assert a in h
    h = h.replace(a, 'JTPrefs.setLang(LANG==="en"?"pt":"en")', 1)
    h = re.sub(r'\$\("#theme"\)\.onclick=\(\)=>\{.*?\n', '$("#theme").onclick=()=>JTPrefs.cycleTheme();\n', h, count=1, flags=re.S)
    h = h.replace('const th = store.get("theme"); if(th) document.documentElement.dataset.theme = th;', '', 1)
    h = h.replace('<meta name="viewport"', '<meta property="og:type" content="website"><meta property="og:title" content="App faixa a faixa: Judô e Jiu-Jitsu"><meta property="og:description" content="Progresso, ficha de exame editável e idioma PT/EN."><meta property="og:url" content="https://joaoventuraoliveira.github.io/judobjj/app/"><meta property="og:image" content="https://joaoventuraoliveira.github.io/judobjj/assets/og/portal.jpg?v=1"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">\n<meta name="viewport"', 1)
    h = LC.transformar_html_styles(h)
    (out / "index.html").write_text(h, encoding="utf-8")
    shutil.copy2(www / "data.js", out / "data.js")
    for f in (www / "img" / "th").glob("*.jpg"): shutil.copy2(f, out / "img" / "th" / f.name)
    mb = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1048576
    print("app:", len(list((out / "img" / "th").glob("*.jpg"))), "miniaturas;", round(mb, 1), "MB")
def explorar():
    out = SITE / "explorar"; out.mkdir(exist_ok=True)
    for n in ("index.html", "explorar.js", "fases-tempo.js"): shutil.copy2(ROOT / "source" / "portal" / "explorar" / n, out / n)
    (out / "explorar.css").write_text(LC.transformar((ROOT / "source" / "portal" / "explorar" / "explorar.css").read_text(encoding="utf-8")), encoding="utf-8")
    print("explorar copiado")
def refs(www):
    t = (pathlib.Path(www) / "data.js").read_text(encoding="utf-8"); first = t.split(";\nwindow.I18N", 1)[0]
    d = json.loads(first[len("window.DATA = "):].rstrip().rstrip(";"))
    return d["REFS"], len(d["judo"]["trans"]), len(d["bjj"]["trans"])
def drawer_slides():
    P = json.loads((SITE / "explorar" / "dados.js").read_text(encoding="utf-8")[len("window.PORTAL="):].rstrip().rstrip(";"))
    e = lambda s: html.escape(str(s or ""), quote=True)
    def item(href, nome, tag="", extra=""):
        q = " ".join(x for x in (nome, tag, extra) if x).lower()
        return f'<li data-q="{e(q)}"><a href="{e(href)}"><span>{e(nome)}</span>' + (f"<small>{e(tag)}</small>" if tag else "") + "</a></li>"
    def mod(titulo, lis): return f'<div class="dm"><h4>{e(titulo)}</h4><ul>{"".join(lis)}</ul></div>'
    J, B = P["judo"], P["bjj"]
    TOP = [("nage", "Projeções (Nage-waza)"), ("katame", "Solo (Katame-waza)"), ("kaeshi", "Contragolpes (Kaeshi-waza)"), ("renraku", "Combinações (Renraku-waza)"), ("fundamentos", "Fundamentos"), ("proibidas", "Técnicas proibidas"), ("glossario", "Glossário"), ("videoteca", "Videoteca oficial"), ("referencias", "Referências")]
    tec = sorted(P["tecnicas"].values(), key=lambda x: x["nome"])
    jm = [mod("Programa de exames", [item("explorar/#/judo/faixa/" + f["id"], f["titulo"], f.get("sub", "")) for f in J["faixas"]]),
          mod("Tópicos", [item("explorar/#/judo/t/" + a, b) for a, b in TOP]),
          mod("Técnicas", [item("explorar/#/judo/tecnica/" + x["id"], x["nome"], x.get("ja", ""), " ".join([x.get("pt") or "", x.get("en") or ""])) for x in tec])]
    bm = [mod("Programa de exames", [item("explorar/#/jiu-jitsu/faixa/" + f["id"], f["titulo"], f.get("sub", "")) for f in B["faixas"]]),
          mod("Lista de componentes", [item("explorar/#/jiu-jitsu/t/" + g["id"], g["nome"]) for g in B["comp"]] + [item("explorar/#/jiu-jitsu/proibidas", "Golpes proibidos por faixa"), item("explorar/#/jiu-jitsu/t/referencias", "Referências")])]
    dr = (f'<section class="dd" data-m="judo"><h3><span class="bd judo" lang="ja">柔道</span><span>Judô</span></h3>{"".join(jm)}</section>'
          f'<section class="dd" data-m="bjj"><h3><span class="bd bjj" lang="ja">柔術</span><span>Jiu-Jitsu</span></h3>{"".join(bm)}</section>')
    G = {"judo": [("o_goshi", "Ilustração: O-goshi, o grande quadril"), ("seoi_nage", "Ilustração: Seoi-nage, projeção por cima do ombro"), ("uchi_mata", "Ilustração: Uchi-mata, a coxa interna"), ("harai_goshi", "Ilustração: Harai-goshi, quadril varrido"), ("tai_otoshi", "Ilustração: Tai-otoshi, queda do corpo"), ("o_soto_gari", "Ilustração: O-soto-gari, grande ceifada exterior"), ("tomoe_nage", "Ilustração: Tomoe-nage, sacrifício em círculo"), ("ura_nage", "Ilustração: Ura-nage, projeção por trás"), ("ippon", "Ilustração: ippon, o ponto máximo"), ("kumikata", "Ilustração: kumi-kata, a pegada")],
         "bjj": [("kesa_gatame", "Ilustração: kesa-gatame, imobilização lateral"), ("ren_kesa_katagatame", "Ilustração: do kesa-gatame ao kata-gatame"), ("ren_yokoshiho_juji", "Ilustração: do yoko-shiho ao juji-gatame"), ("ren_osoto_kesa", "Ilustração: do o-soto-gari ao solo"), ("pro_ashi_garami", "Ilustração: ashi-garami, enredo de pernas"), ("pro_do_jime", "Ilustração: do-jime, estrangulamento de tronco"), ("pro_kansetsu_pe", "Ilustração: chave de articulação em pé"), ("pro_ushiro_sankaku", "Ilustração: ushiro-sankaku, triângulo por trás"), ("faixas", "Ilustração: as faixas, do branco ao preto"), ("banca", "Ilustração: a banca do exame")]}
    sl = []
    for m, lst in G.items():
        for i, (img, alt) in enumerate(lst):
            assert (SITE / "assets" / "img" / (img + ".webp")).exists(), img
            sl.append(f'      <img class="sl{" on" if (m == "judo" and i == 0) else ""}" data-m="{m}" ' + (f'src="assets/img/{img}.webp" ' if (m == "judo" and i == 0) else "") + f'data-src="assets/img/{img}.webp" alt="{e(alt)}" width="800" height="500" decoding="async">')
    return dr, "\n".join(sl)
def landing(www):
    R, nj, nb = refs(www); e = html.escape
    lis = "".join(f'<li><b>{e(r["titulo"])}</b> — {e(r["org"])}, {e(r["ano"])}.' + (f' <a target="_blank" rel="noopener" href="{e(r["url"])}">Abrir a fonte</a>' if r.get("url") else "") + "</li>" for r in R if r["id"] != "app")
    t = (ROOT / "source" / "portal" / "landing_template.html").read_text(encoding="utf-8")
    dr, sl = drawer_slides()
    t = t.replace("{{DRAWER}}", dr).replace("{{SLIDES}}", sl).replace("{{REFS}}", lis).replace("{{NJ}}", str(nj)).replace("{{NB}}", str(nb))
    t = LC.transformar_html_styles(t)
    (SITE / "index.html").write_text(t, encoding="utf-8"); print("landing ok;", len(R) - 1, "fontes")
if __name__ == "__main__":
    www = sys.argv[1]; app(www); explorar(); landing(www)
