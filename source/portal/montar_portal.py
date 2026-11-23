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
    h = h.replace("</head>", "<style>a.brand{color:var(--ink);text-decoration:none}</style></head>", 1)
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
def landing(www):
    R, nj, nb = refs(www); e = html.escape
    lis = "".join(f'<li><b>{e(r["titulo"])}</b> — {e(r["org"])}, {e(r["ano"])}.' + (f' <a target="_blank" rel="noopener" href="{e(r["url"])}">Abrir a fonte</a>' if r.get("url") else "") + "</li>" for r in R if r["id"] != "app")
    t = (ROOT / "source" / "portal" / "landing_template.html").read_text(encoding="utf-8")
    t = t.replace("{{REFS}}", lis).replace("{{NJ}}", str(nj)).replace("{{NB}}", str(nb))
    t = LC.transformar_html_styles(t)
    (SITE / "index.html").write_text(t, encoding="utf-8"); print("landing ok;", len(R) - 1, "fontes")
if __name__ == "__main__":
    www = sys.argv[1]; app(www); explorar(); landing(www)
