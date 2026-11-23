"""Transforma CSS responsivo (@media max-width) para respeitar a escolha de layout (auto / PC / celular):
 - dentro do @media, cada seletor ganha o prefixo html:not(.lay-desktop) (PC forçado desliga as regras de celular);
 - depois do @media, uma cópia com o prefixo html.lay-mobile (celular forçado liga as regras em tela grande)."""
import re

def _balanced(css, i):
    d = 0
    for j in range(i, len(css)):
        if css[j] == "{": d += 1
        elif css[j] == "}":
            d -= 1
            if d == 0: return j
    return len(css) - 1

def _rules(body):
    out = []; i = 0
    while i < len(body):
        o = body.find("{", i)
        if o < 0: break
        c = _balanced(body, o)
        out.append((body[i:o].strip(), body[o + 1:c])); i = c + 1
    return out

def _prefix(sel, pref):
    parts = [s.strip() for s in sel.split(",") if s.strip()]
    res = []
    for s in parts:
        if s.startswith(":root") or s.startswith("html"):
            s2 = re.sub(r"^(:root|html)", pref, s, count=1)
        else:
            s2 = pref + " " + s
        res.append(s2)
    return ",".join(res)

def transformar(css):
    out = []; i = 0
    pat = re.compile(r"@media\s*\(\s*max-width\s*:\s*\d+px\s*\)\s*\{")
    while True:
        m = pat.search(css, i)
        if not m:
            out.append(css[i:]); break
        out.append(css[i:m.start()])
        o = m.end() - 1; c = _balanced(css, o); body = css[o + 1:c]; head = css[m.start():o + 1]
        rs = _rules(body)
        a = "".join(_prefix(s, "html:not(.lay-desktop)") + "{" + d + "}" for s, d in rs)
        b = "".join(_prefix(s, "html.lay-mobile") + "{" + d + "}" for s, d in rs)
        out.append(head + a + "}" + b)
        i = c + 1
    return "".join(out)

def transformar_html_styles(html):
    return re.sub(r"(<style[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + transformar(m.group(2)) + m.group(3), html, flags=re.S)
