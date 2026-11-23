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
import re as _re
UI = ns["UI"]; RX = [_re.compile(r[0]) for r in UI.RULES_EN + ns["EXTRA_RULES"]]
NOMES = _re.compile(r"^[A-Za-zōūŌŪ\-' ]{2,40}$")
def sinal_pt(s):
    return bool(_re.search(r"[ãõçáéíóúâêôà]|\b(de|do|da|dos|das|para|com|que|em|um|uma|os|as|é|se|ou|no|na|nos|nas|ao|por|mais|sua|seu)\b", s))
def ruido(s):
    if not sinal_pt(s): return True
    if any(r.search(s) for r in RX): return True
    if NOMES.match(s) and (s == s.lower() and "-" in s or all(w[:1].isupper() or "-" in w for w in s.split())): return True   # nomes em romaji/inglês
    return False
pend = [s for s in sorted({ns["norm"](x) for x in S}, key=len) if ns["eh_pt"](s) and ns["traduzir"](s) == s and not ruido(s)]
print("pendentes:", len(pend), "| mostrando", min(n, len(pend)))
for s in pend[:n]: print(json.dumps(s, ensure_ascii=False))
