"""Lista os próximos textos PT ainda sem tradução EN para traduzir à mão, em blocos.
Uso: python source/portal/listar_pendentes.py explorar|livro [N=150] [saida.json]
Depois de traduzir, grave os pares em source/portal/i18n_portal_manual.json e rode i18n_portal.py ... --sem-mt."""
import sys, json, pathlib, re
alvo = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 150
R = pathlib.Path(__file__).resolve().parents[2]
sys.argv = ["x", r"D:\Claude\Judo_BJJ\pipelines", r"D:\Claude\Judo_BJJ\webapp\data.js", "--sem-mt"]
src = (R / "source/portal/i18n_portal.py").read_text(encoding="utf-8").split("what = sys.argv[3:]")[0]
ns = {"__file__": str(R / "source/portal/i18n_portal.py")}; exec(compile(src, "i18n_portal", "exec"), ns)
if alvo == "explorar":
    S = set(json.loads((R / "source/portal/explorar_strings.json").read_text(encoding="utf-8"))); S = {s[1:] if s.startswith("@") else s for s in S}
    w = set(); ns["walk_strings"](ns["PORTAL"], w); S |= w; S |= ns["html_strings"](R / "site/explorar/index.html")
else: S = ns["html_strings"](R / "site/livro.html")
pend = [s for s in sorted({ns["norm"](x) for x in S}, key=len) if ns["eh_pt"](s) and ns["traduzir"](s) == s]
print("pendentes:", len(pend), "| mostrando", min(n, len(pend)))
for s in pend[:n]: print(json.dumps(s, ensure_ascii=False))
