"""Correções dos itens do regulamento da CBJ extraídos do PDF (app "Faixa a faixa" e explorador).

Por quê: a leitura automática do PDF quebrou palavras, pôs duas imobilizações em "Outros critérios",
juntou imobilizações e viradas do 6º Kyû num item só e não trouxe a idade mínima do 8º Kyû como item
(ela existe nos fatos da etapa). Nas etapas que reúnem dois exames da mesma cor, um item igual nos dois
ficava sem a marca do Kyû; agora leva os dois ("9º e 8º Kyû"), para ficar claro que vale para ambos.
Também acrescenta 9º e 10º Dan, que faltavam (dados do livro: CBJ 2022 e IJF 2024).
Ver CONTEXTO-RESTAURACAO.md. As correções são idempotentes: rodar de novo não muda nada.

Uso: python source/portal/corrigir_dados.py site/app/data.js   (corrige o arquivo no lugar)"""
import json, re, sys, pathlib

OCR = {
    "imob ilização": "imobilização", "imobili zação": "imobilização", "integrante s": "integrantes",
    "nav io": "navio", "C ampeonato": "Campeonato", "M unique": "Munique", "técnic as": "técnicas",
    "Mar rom": "Marrom", "Div isão": "Divisão", "Ki me": "Kime", "p edagógicos": "pedagógicos",
    "pon tos": "pontos", "Fed eração": "Federação", "estadu al": "estadual", "con ce": "conce",
    "resistê ncia": "resistência", "0 1 ano": "01 ano", "09 (nove ) anos": "09 (nove) anos",
    "daAssem": "da Assem",
}
CAT_IMOB = "Imobilização (Osae komi waza)"
CAT_SOLO = "Solo: viradas, escapes e defesas"

VERMELHA = ["#C8352F", None]
DANS_SUPERIORES = [
    {"id": "j20", "titulo": "9º Dan (Ku dan)", "sub": "Kôdansha / graus superiores", "idade": "66 anos", "carencia": "8 anos no 8º Dan",
     "itens": [("Elegibilidade", "Idade mínima: 66 anos; carência de 8 anos (tabela de idades e carências da CBJ)."),
               ("Elegibilidade", "Promoção por indicação, sem exame; homologação pela IJF."),
               ("Atividades de ensino", "Programa mínimo da IJF (a partir de 2026): sem demonstração física; mondo em vídeo atestado por dois 7º Dan.")]},
    {"id": "j21", "titulo": "10º Dan (Jū dan)", "sub": "Kôdansha / graus superiores", "idade": "74 anos", "carencia": "8 anos no 9º Dan",
     "itens": [("Elegibilidade", "Idade mínima: 74 anos; carência de 8 anos (tabela de idades e carências da CBJ)."),
               ("Elegibilidade", "Promoção por indicação; homologação pela IJF, com decisão unânime do Comitê Executivo."),
               ("Atividades de ensino", "Programa mínimo da IJF (a partir de 2026): sem candidatura individual; indicação por federação, união continental ou Comitê Executivo (cerca de 70 anos de idade e 10 de grau).")]},
]


def _ocr(s):
    for a, b in OCR.items():
        s = s.replace(a, b)
    return s


def corrigir(D):
    """Recebe o objeto DATA do app (com D['judo']['trans'] já em uma etapa por cor) e corrige no lugar."""
    trans = D["judo"]["trans"]
    for t in trans:
        novos = []
        for it in t.get("itens", []):
            it["t"] = _ocr(it["t"])
            low = it["t"].lower()
            if it.get("c") == "Outros critérios" and "imobilização" in low:
                it["c"] = CAT_IMOB
            # 6º Kyû: imobilizações e viradas estavam num item só
            m = re.match(r"(Demonstrar cinco técnicas de imobilização \(Osae komi waza\)\.)\s*(Demonstrar três viradas.*)", it["t"])
            if m:
                it["t"] = m.group(1)
                novos.append(it)
                v = dict(it); v["t"] = m.group(2); v["c"] = CAT_SOLO; v["tm"] = []
                novos.append(v)
                continue
            novos.append(it)
        t["itens"] = novos
        # itens iguais nos dois exames da mesma cor: marcar com os dois Kyû
        if t.get("alias"):
            m = re.match(r"(\d+)º e (\d+)º Kyû", t.get("sub", ""))
            if m:
                ambos = f"{m.group(1)}º e {m.group(2)}º Kyû"
                for it in t["itens"]:
                    if not it.get("et"):
                        it["et"] = ambos
        # 8º Kyû: a idade mínima está nos fatos da etapa, mas faltava como item
        if t["id"] == "j03" and not any(it.get("et") == "8º Kyû" and it["t"].startswith("Idade mínima") for it in t["itens"]):
            i = next((k for k, it in enumerate(t["itens"]) if it.get("et") == "8º Kyû"), len(t["itens"]))
            t["itens"].insert(i, {"t": "Idade mínima - 07 (sete) anos.", "i": [], "p": [], "c": "Elegibilidade", "tm": [], "et": "8º Kyû"})
        for f in t.get("fatos", []):
            f[1] = _ocr(f[1])
    # 9º e 10º Dan
    ids = {t["id"] for t in trans}
    base = next((t for t in trans if t["id"] == "j19"), None)
    for d in DANS_SUPERIORES:
        if d["id"] in ids or base is None:
            continue
        n = dict(base)
        n.update(id=d["id"], titulo=d["titulo"], sub=d["sub"], de="Vermelha", para="Vermelha", bde=VERMELHA, bpara=VERMELHA,
                 fatos=[["Idade mínima", d["idade"]], ["Tempo", d["carencia"]], ["Promoção", "Indicação, com homologação da IJF"]],
                 itens=[{"t": x[1], "i": [], "p": [], "c": x[0], "tm": []} for x in d["itens"]], pags=[],
                 nota="Dados do livro (tabela de idades e carências da CBJ e programa mínimo de dans da IJF). O regulamento da CBJ de 2023 lido pelo app vai só até o 8º Dan.")
        n.pop("alias", None)
        trans.append(n)
    return D


def main(path):
    p = pathlib.Path(path)
    raw = p.read_text(encoding="utf-8")
    pre, sep, rest = raw.partition(";\nwindow.I18N=")
    D = json.loads(pre.split("window.DATA = ", 1)[1].rstrip().rstrip(";"))
    corrigir(D)
    p.write_text("window.DATA = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + sep + rest, encoding="utf-8")
    print("corrigido:", p)


if __name__ == "__main__":
    main(sys.argv[1])
