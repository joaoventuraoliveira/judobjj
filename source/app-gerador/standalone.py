"""Gera webapp/JudoBJJApp_celular.html: arquivo ÚNICO e independente (dados + imagens embutidos em base64),
para enviar por WhatsApp/e-mail e abrir em qualquer smartphone sem pastas ao lado."""
import re, io, json, base64, pathlib
from PIL import Image
W = pathlib.Path(__file__).resolve().parent.parent / "webapp"
def gerar(maxpx=600, q=62):
    html = (W / "index_unico.html").read_text(encoding="utf-8")
    dj = (W / "data.js").read_text(encoding="utf-8")
    paths = sorted(set(re.findall(r"img/[A-Za-z0-9_\-./]+?\.(?:png|jpe?g)", dj)))
    im_map = {}; tot = 0
    for p in paths:
        f = W / p
        if not f.exists(): continue
        try:
            im = Image.open(f).convert("RGB"); im.thumbnail((maxpx, maxpx)); b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
        except Exception: continue
        d = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode(); im_map[p] = d; tot += len(d)
    a = 'const thumbUrl=s=>String(s).replace(/^img\\/(.+)\\.(png|jpe?g)$/i,"img/th/$1.jpg");'
    assert a in html, "thumbUrl nao encontrado"
    html = html.replace(a, 'const thumbUrl=s=>{s=String(s);return (window.__IM&&window.__IM[s])||s.replace(/^img\\/(.+)\\.(png|jpe?g)$/i,"img/th/$1.jpg")};', 1)
    b2 = '$("#dimg").src=th.dataset.img;'
    assert b2 in html, "lightbox nao encontrado"
    html = html.replace(b2, '$("#dimg").src=(window.__IM&&window.__IM[th.dataset.img])||th.dataset.img;', 1)
    mark = "<script>\nfunction boot(){"
    assert mark in html
    html = html.replace(mark, "<script>window.__IM=" + json.dumps(im_map, separators=(",", ":")) + ";</script>\n" + mark, 1)
    out = W / "JudoBJJApp_celular.html"; out.write_text(html, encoding="utf-8")
    print("celular independente:", len(im_map), "imagens;", round(out.stat().st_size / 1048576, 1), "MB")
if __name__ == "__main__": gerar()
