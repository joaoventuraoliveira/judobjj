"""Compõe traduções de textos pendentes a partir de partes já traduzidas no manual (sem MT).
Uso: python compor_pendentes.py [--gravar]   -> imprime as partes que ainda faltam traduzir."""
import json, re, subprocess, sys, pathlib
R = pathlib.Path(__file__).resolve().parent
PY = sys.executable
MP = R / "i18n_portal_manual.json"; M = json.loads(MP.read_text(encoding="utf-8"))
out = subprocess.run([PY, "-X", "utf8", str(R / "listar_pendentes.py"), "explorar", "2000"], capture_output=True, text=True, encoding="utf-8").stdout
pend = [json.loads(l) for l in out.splitlines() if l.startswith('"')]
EXEC = ("Execução. Aplicação final da técnica, que leva uke ao chão. É a 3ª fase.", "Execution. Final application of the technique, which takes uke to the ground. It is the 3rd phase.")
falta = {}
def tr(s):
    s = s.strip()
    for k in (s, s.rstrip("."), s.rstrip(".") + "."):
        if k in M: return M[k] if k.endswith(".") == s.endswith(".") or True else M[k]
    return None
def comp(s):
    r = tr(s)
    if r is not None: return r
    if s.startswith("Ação-chave: ") and s.endswith(EXEC[0]):
        x = s[len("Ação-chave: "):-len(EXEC[0])].strip().rstrip(".")
        y = tr(x)
        if y is None: falta[x] = 1; return None
        return "Key action: " + y.rstrip(".") + ". " + EXEC[1]
    if " · " in s:
        ps = [comp(p) for p in s.split(" · ")]
        return None if None in ps else " · ".join(ps)
    m = re.match(r"^([^:]{2,40}): (.+)$", s)
    if m:
        a, b = tr(m.group(1)), comp(m.group(2))
        if a is not None and b is not None: return a + ": " + b
        if b is None: falta[m.group(2)] = 1
    else: falta[s] = 1
    return None
n = 0
for s in pend:
    r = comp(s)
    if r and s not in M: M[s] = r; n += 1
print("compostos:", n, "| partes sem tradução:", len(falta))
for k in list(falta)[:60]: print(json.dumps(k, ensure_ascii=False))
if "--gravar" in sys.argv: MP.write_text(json.dumps(M, ensure_ascii=False, indent=0), encoding="utf-8")
