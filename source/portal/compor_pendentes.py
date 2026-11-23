"""Compõe traduções de textos pendentes a partir de partes já traduzidas no manual (sem MT).
Uso: python compor_pendentes.py [--gravar]   -> imprime as partes que ainda faltam traduzir."""
import json, re, subprocess, sys, pathlib
R = pathlib.Path(__file__).resolve().parent
ALVO = "livro" if "livro" in sys.argv else "explorar"
PY = sys.executable
MP = R / "i18n_portal_manual.json"; M = json.loads(MP.read_text(encoding="utf-8"))
out = subprocess.run([PY, "-X", "utf8", str(R / "listar_pendentes.py"), ALVO, "3000"], capture_output=True, text=True, encoding="utf-8").stdout
pend = [json.loads(l) for l in out.splitlines() if l.startswith('"')]
EXEC = ("Execução. Aplicação final da técnica, que leva uke ao chão. É a 3ª fase.", "Execution. Final application of the technique, which takes uke to the ground. It is the 3rd phase.")
DESEQ = ("Desequilíbrio. Ação de tirar o oponente da postura estável, puxando ou empurrando, para preparar a projeção. É a 1ª das três fases.", "Off-balancing. Action of taking the opponent out of a stable posture, pulling or pushing, to prepare the throw. It is the 1st of the three phases.")
DIRS = {"Trás":"Back","Frente":"Front","Lateral":"Side","Para trás":"Backward","Trás-direita":"Back-right","Frente-direita":"Front-right","Lateral direita":"Right side","Trás, em diagonal":"Back, diagonal","Frente e para cima":"Front and up","Frente, em diagonal":"Front, diagonal","Trás, sobre o calcanhar":"Back, onto the heel","Lateral, no deslocamento":"Side, while moving","para cima":"upward","Contra-ataque: para cima":"Counter-attack: upward","Lateral, sobre o pé que avança":"Side, over the advancing foot","Contra-ataque: para cima e para trás":"Counter-attack: upward and backward"}
falta = {}
def tr(s):
    s = s.strip()
    if re.fullmatch(r"JJIF Ne-Waza Rules V2\.8\.1, p\. \d+", s): return s
    for k in (s, s.rstrip("."), s.rstrip(".") + "."):
        if k in M: return M[k] if k.endswith(".") == s.endswith(".") or True else M[k]
    return None
MES = {"nov.":"Nov","dez.":"Dec","jan.":"Jan","fev.":"Feb","mar.":"Mar","abr.":"Apr","mai.":"May","jun.":"Jun","jul.":"Jul","ago.":"Aug","set.":"Sep","out.":"Oct"}
def cit(s):
    m = re.search(r"Citada em: (.+)$", s)
    if not m: return None
    ts = [tr(x) for x in m.group(1).split(" · ")]
    if None in ts:
        for x, y in zip(m.group(1).split(" · "), ts):
            if y is None: falta[x] = 1
        return None
    h = s[:m.start()]
    h = h.replace(" Disponível em: ", " Available at: ").replace(" Acesso em: ", " Accessed on: ").replace("[s. d.]", "[n.d.]").replace("Série de vídeos", "Video series").replace("Tóquio", "Tokyo")
    h = re.sub(r"(\d{1,2}) (\w{3,4}\.) (\d{4})", lambda g: f"{MES.get(g.group(2), g.group(2))} {g.group(1)}, {g.group(3)}", h)
    return h + "Cited in: " + " · ".join(ts)
def frag(s):
    if "Disponível em:" not in s and "Acesso em:" not in s: return None
    h = s.replace("Disponível em:", "Available at:").replace("Acesso em:", "Accessed on:").replace("[s. d.]", "[n.d.]").replace("[S. l.]", "[S. l.]").replace("Série de vídeos", "Video series").replace("Série de 100 vídeos", "Series of 100 videos").replace("Tóquio", "Tokyo").replace(" ciclo ", " cycle ").replace("Cap. ", "Ch. ").replace("Art. ", "Art. ").replace("Art.s", "Art.")
    h = re.sub(r"(\d+) vídeos", r"\1 videos", h)
    h = re.sub(r"(\d{1,2}) (\w{3,4}\.) (\d{4})", lambda g: f"{MES.get(g.group(2), g.group(2))} {g.group(1)}, {g.group(3)}", h)
    h = re.sub(r"\bjan\. (\d{4})", r"Jan. \1", h)
    if re.search(r"\b(de|do|da|em|para|com|que|dos|das)\b", h.replace("Available at:", "")): return None
    return h
def comp(s):
    r = tr(s)
    if r is not None: return r
    if "Citada em: " in s: return cit(s)
    r = frag(s)
    if r: return r
    if s.startswith("Ação-chave: ") and s.endswith(EXEC[0]):
        x = s[len("Ação-chave: "):-len(EXEC[0])].strip().rstrip(".")
        y = tr(x)
        if y is None: falta[x] = 1; return None
        return "Key action: " + y.rstrip(".") + ". " + EXEC[1]
    if s.endswith(DESEQ[0]):
        d = s[:-len(DESEQ[0])].strip().rstrip(".")
        pre = ""
        if d.startswith("Direção principal: "): d = d[len("Direção principal: "):]; pre = "Main direction: "
        if d in DIRS: return pre + DIRS[d] + ". " + DESEQ[1]
        falta[d] = 1; return None
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
