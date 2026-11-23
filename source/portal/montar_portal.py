"""Monta o portal (Judô + Jiu-Jitsu) em site/: página inicial, livro (livro.html) e app faixa a faixa (site/app).
Uso: python source/portal/montar_portal.py <pasta_www_do_app>
O app vem do projeto local Judo_BJJ (webapp gerado por pipelines/gerar_webapp_dados.py; ver source/app-gerador/).
Só miniaturas (img/th) são publicadas; a ampliação usa a própria miniatura, com a fonte sempre citada."""
import sys, re, json, shutil, html, pathlib
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
    (out / "index.html").write_text(h, encoding="utf-8")
    shutil.copy2(www / "data.js", out / "data.js")
    for f in (www / "img" / "th").glob("*.jpg"): shutil.copy2(f, out / "img" / "th" / f.name)
    mb = sum(f.stat().st_size for f in out.rglob("*") if f.is_file()) / 1048576
    print("app:", len(list((out / "img" / "th").glob("*.jpg"))), "miniaturas;", round(mb, 1), "MB")
def refs(www):
    t = (pathlib.Path(www) / "data.js").read_text(encoding="utf-8"); first = t.split(";\nwindow.I18N", 1)[0]
    d = json.loads(first[len("window.DATA = "):].rstrip().rstrip(";"))
    return d["REFS"], len(d["judo"]["trans"]), len(d["bjj"]["trans"])
def landing(www):
    R, nj, nb = refs(www); e = html.escape
    lis = "".join(f'<li><b>{e(r["titulo"])}</b> — {e(r["org"])}, {e(r["ano"])}.' + (f' <a target="_blank" rel="noopener" href="{e(r["url"])}">Abrir a fonte</a>' if r.get("url") else "") + "</li>" for r in R if r["id"] != "app")
    t = (ROOT / "source" / "portal" / "landing_template.html").read_text(encoding="utf-8")
    t = t.replace("{{REFS}}", lis).replace("{{NJ}}", str(nj)).replace("{{NB}}", str(nb))
    (SITE / "index.html").write_text(t, encoding="utf-8"); print("landing ok;", len(R) - 1, "fontes")
if __name__ == "__main__":
    www = sys.argv[1]; app(www); landing(www)
