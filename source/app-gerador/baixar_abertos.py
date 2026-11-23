"""Descobre PDFs e salva paginas como texto.
  python -I baixar_abertos.py descobrir URL [URL...]        -> lista links de PDF/documento
  python -I baixar_abertos.py pdf URL DESTINO_DIR [nome]    -> baixa PDF (sha256, dedupe por hash em _dados/hashes.csv)
  python -I baixar_abertos.py pagina URL DESTINO_DIR nome   -> salva texto da pagina como .md (com URL e data)
Apenas fontes aprovadas pelo usuario. Nada e sobrescrito.
"""
import sys, re, hashlib, csv, pathlib, datetime
from urllib.parse import urljoin, unquote, urlparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bs4 import BeautifulSoup
from rede import sessao
S = sessao(); S.headers["User-Agent"] = "Judo_BJJ-research/1.0 (pesquisa academica)"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
HASHES = RAIZ / "_dados" / "hashes.csv"
HOJE = datetime.date.today().isoformat()


def descobrir(urls):
    for u in urls:
        r = S.get(u, timeout=40); r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        print("##", u, r.status_code)
        vistos = set()
        for a in soup.find_all("a", href=True):
            h = urljoin(u, a["href"]); t = a.get_text(" ", strip=True)[:90]
            if h in vistos: continue
            if re.search(r"\.pdf|\.docx?|active_storage|uploads/|download", h, re.I):
                vistos.add(h); print(f"  {t} | {h}")


def conhecidos():
    if not HASHES.exists(): return {}
    return {r["sha256"]: r["arquivo"] for r in csv.DictReader(open(HASHES, encoding="utf-8"))}


def pdf(url, destino, nome=None):
    r = S.get(url, timeout=120); r.raise_for_status()
    b = r.content
    if not b.startswith(b"%PDF"):
        print("NAO E PDF:", url, r.headers.get("content-type")); return
    h = hashlib.sha256(b).hexdigest()
    k = conhecidos()
    if h in k: print("duplicata de", k[h]); return
    d = pathlib.Path(destino); d.mkdir(parents=True, exist_ok=True)
    nome = nome or unquote(pathlib.Path(urlparse(r.url).path).name) or h[:12] + ".pdf"
    alvo = d / nome
    if alvo.exists(): print("ja existe", alvo); return
    alvo.write_bytes(b)
    novo = not HASHES.exists()
    with open(HASHES, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if novo: w.writerow(["sha256", "arquivo", "url", "data", "bytes"])
        w.writerow([h, str(alvo), url, HOJE, len(b)])
    print("baixado", alvo, len(b))


def pagina(url, destino, nome):
    r = S.get(url, timeout=40); r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    for t in soup(["script", "style", "nav", "footer", "header", "noscript"]): t.decompose()
    txt = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n", strip=True))
    d = pathlib.Path(destino); d.mkdir(parents=True, exist_ok=True)
    alvo = d / nome
    if alvo.exists(): print("ja existe", alvo); return
    alvo.write_text(f"---\nfonte: {url}\nacesso_em: {HOJE}\ntipo: pagina-oficial (texto extraido automaticamente)\n---\n\n{txt}\n", encoding="utf-8")
    print("salvo", alvo, len(txt))


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "descobrir": descobrir(sys.argv[2:])
    elif c == "pdf": pdf(*sys.argv[2:5])
    elif c == "pagina": pagina(*sys.argv[2:5])
