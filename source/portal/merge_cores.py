"""Uma etapa por cor de faixa no Judô infantil/juvenil.

O regulamento da CBJ tem dois exames para cada cor intermediária (ex.: 11º Kyû Branca -> Branca/Cinza e 10º Kyû
Branca/Cinza -> Cinza). Os dados de cada um são diferentes (idade, interstício, técnicas, itens), então nada é descartado:
os dois exames passam a morar numa só etapa por cor ("Branca -> Cinza"), e o que é específico de cada exame fica marcado
com o seu Kyû (campo "et"). O id da etapa é o do primeiro exame; o do segundo vira "alias" (links antigos continuam valendo).
Usado pelo build_dados.py (explorador e início) e pelo montar_portal.py (app)."""
import re

PARES = [("j01", "j02"), ("j03", "j04"), ("j05", "j06"), ("j07", "j08")]


def _titulo(a, b):
    return a["titulo"].split(" → ")[0] + " → " + b["titulo"].split(" → ")[-1]


def _sub(a, b):
    sa, sb = a["sub"], b["sub"]
    na, ra = (sa.split(" ", 1) + [""])[:2]
    nb, rb = (sb.split(" ", 1) + [""])[:2]
    return f"{na} e {nb} {ra}".strip() if ra == rb else f"{sa} · {sb}"


def _uniao(*listas):
    out = []
    for l in listas:
        for x in l or []:
            if x not in out:
                out.append(x)
    return out


def _vazio(s):
    return s is None or str(s).strip() in ("", "—", "-")


def _mstr(a, b, la, lb):
    """Texto de cada exame; só rotula com o Kyû quando os dois dizem coisas diferentes."""
    if a == b:
        return a
    if _vazio(a) and _vazio(b):
        return a if not _vazio(a) else (b or "—")
    if _vazio(a):
        return f"{lb}: {b}"
    if _vazio(b):
        return f"{la}: {a}"
    return f"{la}: {a} · {lb}: {b}"


def _fatos(a, b, sub, la, lb):
    ra, rb = dict((x[0], x[1]) for x in a), dict((x[0], x[1]) for x in b)
    labels = _uniao([x[0] for x in a], [x[0] for x in b])
    out = []
    for k in labels:
        if k == "Graduação":
            out.append([k, sub]); continue
        va, vb = ra.get(k), rb.get(k)
        if va == vb or vb is None or va is None:
            out.append([k, va if vb is None else vb if va is None else va]); continue
        out.append([k, f"{la}: {va} · {lb}: {vb}"])
    return out


def _itens(ia, ib, la, lb, chave):
    """Itens de cada exame; o que é igual nos dois aparece uma vez, sem marca; o resto leva o Kyû."""
    ta = {chave(i) for i in ia}; tb = {chave(i) for i in ib}
    out = []
    for i in ia:
        j = dict(i)
        if chave(i) not in tb:
            j["et"] = la
        out.append(j)
    for i in ib:
        if chave(i) in ta:
            continue
        j = dict(i); j["et"] = lb; out.append(j)
    return out


def _base(a, b):
    la, lb = a["sub"], b["sub"]
    a["_et"], b["_et"] = la, lb
    sub = _sub(a, b)
    return la, lb, sub


def mesclar_portal(faixas, tecnicas):
    """faixas = JUDO_BELTS (explorador). Devolve a lista nova e acerta T[x]['faixas'] (ids) das técnicas."""
    por_id = {f["id"]: f for f in faixas}
    alias = {}; saida = []; usados = set()
    pares = {a: b for a, b in PARES if a in por_id and b in por_id}
    for f in faixas:
        if f["id"] in usados:
            continue
        if f["id"] not in pares:
            saida.append(f); continue
        a, b = f, por_id[pares[f["id"]]]; usados.update([a["id"], b["id"]])
        la, lb, sub = _base(a, b)
        m = dict(b)
        m.update(id=a["id"], alias=[b["id"]], titulo=_titulo(a, b), sub=sub,
                 cores={"de": a["cores"]["de"], "para": b["cores"]["para"]},
                 fatos=_fatos(a["fatos"], b["fatos"], sub, la, lb), nota=a.get("nota") or b.get("nota", ""),
                 pags=sorted(_uniao(a.get("pags"), b.get("pags"))))
        ids = _uniao([c["id"] for c in a["cats"]], [c["id"] for c in b["cats"]])
        cats = []
        for cid in ids:
            ca = next((c for c in a["cats"] if c["id"] == cid), None); cb = next((c for c in b["cats"] if c["id"] == cid), None)
            c = dict(ca or cb)
            c["itens"] = _itens((ca or {}).get("itens", []), (cb or {}).get("itens", []), la, lb, lambda i: i["t"])
            cats.append(c)
        m["cats"] = cats
        for k in ("nage", "katame", "renrakuSlugs", "kaeshiSlugs"):
            m[k] = _uniao(a.get(k), b.get(k))
        for k in ("renraku", "kaeshi", "kihon", "kata", "teoria"):
            if k in a or k in b:
                m[k] = _mstr(a.get(k, "—"), b.get(k, "—"), la, lb)
        if a.get("quant") or b.get("quant"):
            qa, qb = a.get("quant") or {}, b.get("quant") or {}
            m["quant"] = {k: _mstr(qa.get(k, "—"), qb.get(k, "—"), la, lb) for k in _uniao(qa.keys(), qb.keys())}
        for x in (a, b, m):
            x.pop("_et", None)
        alias[b["id"]] = a["id"]; saida.append(m)
    for t in tecnicas.values():
        t["faixas"] = _uniao([alias.get(i, i) for i in t.get("faixas", [])])
    return saida


def mesclar_app(trans):
    """trans = DATA.judo.trans do app (itens com imagem, paginas, nomes de categorias)."""
    por_id = {t["id"]: t for t in trans}
    saida = []; usados = set(); pares = {a: b for a, b in PARES if a in por_id and b in por_id}
    for t in trans:
        if t["id"] in usados:
            continue
        if t["id"] not in pares:
            saida.append(t); continue
        a, b = t, por_id[pares[t["id"]]]; usados.update([a["id"], b["id"]])
        la, lb, sub = _base(a, b)
        m = dict(b)
        m.update(id=a["id"], alias=[b["id"]], titulo=_titulo(a, b), sub=sub, de=a["de"], para=b["para"], bde=a["bde"], bpara=b["bpara"],
                 fatos=_fatos(a["fatos"], b["fatos"], sub, la, lb), nota=a.get("nota") or b.get("nota", ""),
                 pags=sorted(_uniao(a.get("pags"), b.get("pags"))),
                 itens=_itens(a.get("itens", []), b.get("itens", []), la, lb, lambda i: (i.get("c"), i["t"])))
        if "catnm" in a or "catnm" in b:
            m["catnm"] = {**(a.get("catnm") or {}), **(b.get("catnm") or {})}
        if "refs" in a or "refs" in b:
            ra, rb = a.get("refs"), b.get("refs")
            m["refs"] = _uniao(ra, rb) if isinstance(ra or rb, list) else (ra or rb)
        for x in (a, b, m):
            x.pop("_et", None)
        saida.append(m)
    return saida
