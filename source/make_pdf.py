"""make_pdf.py — gera o PDF (A4) a partir de dist/print.html com Chrome headless.
O sumário e o índice viram links clicáveis; os capítulos viram marcadores (outline) do PDF."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent / 'dist'
OUT = ROOT / 'judo-tecnicas-e-exames-de-faixa.pdf'
FOOT = ('<div style="width:100%;font-size:8px;color:#777;padding:0 14mm;display:flex;justify-content:space-between;'
        'font-family:sans-serif"><span>Judô: técnicas e exames de faixa</span>'
        '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page()
    pg.goto((ROOT / 'print.html').as_uri(), wait_until='networkidle')
    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    pg.wait_for_timeout(1500)
    pg.pdf(path=str(OUT), format='A4', print_background=True, display_header_footer=True,
           header_template='<div></div>', footer_template=FOOT, prefer_css_page_size=True,
           margin={'top': '16mm', 'bottom': '18mm', 'left': '14mm', 'right': '14mm'},
           outline=True, tagged=True)
    b.close()
print(OUT, OUT.stat().st_size // 1024, 'KB')
