"""Camada visual compartilhada (webapp e versões multiplataforma): cabeçalho fixo, destaque da faixa e fileiras de cartões, tema escuro."""
import re
CSS = r"""
/* ===== camada visual da versão multiplataforma ===== */
:root[data-theme="dark"],:root:not([data-theme="light"]){--bg:#0b0d11;--panel:#14181f;--ink:#f3f5f8;--muted:#a1acb8;--line:#262d38;--soft:#1b212b;--hh:64px}
:root[data-theme="light"]{--bg:#f2f4f7;--panel:#ffffff;--ink:#141a21;--muted:#586674;--line:#d5dce3;--soft:#eaeef2;--hh:64px}
body{background:var(--bg)}
.app{display:block}
.rail{position:sticky;top:0;z-index:30;height:auto;display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;padding:12px clamp(16px,4vw,48px);border:0;overflow:visible;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.brand{margin:0;font:800 1.3rem/1 var(--display);letter-spacing:-.02em}
.brand small{display:none}
.mode{margin:0;display:inline-grid;grid-template-columns:auto auto;gap:4px;min-width:230px}
.mode button{padding:8px 18px;min-height:40px}
.langbtn{display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line);background:var(--soft);color:var(--ink);font:700 .85rem var(--display);cursor:pointer}
.langbtn:hover{background:var(--a);color:var(--a-ink);border-color:var(--a)}
.search{width:min(300px,100%);margin:0 0 0 auto;border-radius:999px;padding:10px 16px;background:var(--soft);border-color:transparent}
.rails{padding:8px 0 0}
.railt{font:700 1.15rem var(--display);margin:14px clamp(16px,4vw,48px) 0;letter-spacing:-.01em}
.rails .ladder{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x proximity;padding:14px clamp(16px,4vw,48px) 22px;margin:0;scrollbar-width:thin}
.rails .ladder li{flex:0 0 auto;scroll-snap-align:start}
.rails .ladder li.group{align-self:center;margin:0 2px;font:700 .7rem var(--display);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);writing-mode:vertical-rl;transform:rotate(180deg);white-space:nowrap}
.rails .ladder button{display:flex;flex-direction:column;align-items:stretch;gap:0;width:172px;height:226px;padding:0;border-radius:14px;overflow:hidden;background:var(--panel);box-shadow:0 6px 18px rgba(0,0,0,.35);transition:transform .22s ease,box-shadow .22s ease;position:relative;text-align:left}
.rails .ladder button:hover,.rails .ladder button:focus-visible{transform:translateY(-6px) scale(1.04);box-shadow:0 14px 30px rgba(0,0,0,.5);background:var(--panel)}
.rails .ladder button[aria-current="true"]{box-shadow:0 0 0 3px var(--a),0 14px 30px rgba(0,0,0,.5);background:var(--panel)}
.rails .ladder .belt{height:112px;width:100%;border-radius:0;box-shadow:none;flex:0 0 112px}
.rails .ladder .belt::after{width:24%}
.rails .ladder button>span{display:block;padding:0 14px}
.rails .ladder button>span:nth-of-type(1){padding-top:12px;flex:1}
.rails .ladder .t{display:block;font:700 1.02rem/1.15 var(--display);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.rails .ladder .s{margin-top:6px;font-size:.76rem;color:var(--muted)}
.rails .ladder .p{padding-bottom:10px;min-height:26px;color:var(--a);font-weight:700}
main{padding:6px clamp(16px,4vw,48px) 72px;max-width:1320px;margin:0 auto}
.hero{position:relative;overflow:hidden;border:0;border-radius:22px;padding:clamp(22px,4vw,48px);background:linear-gradient(120deg,color-mix(in srgb,var(--a) 62%,#000) 0%,color-mix(in srgb,var(--a) 22%,var(--bg)) 46%,var(--panel) 100%)}
.hero h1{font-size:clamp(2.2rem,6vw,4.4rem);color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.35)}
:root[data-theme="light"] .hero h1{color:#fff}
.hero .sub{color:rgba(255,255,255,.82);font-size:1.05rem}
.hero .note{background:rgba(0,0,0,.28);color:#fff;border-left-color:rgba(255,255,255,.55)}
.hero .belts .lbl,.hero .belts small{color:rgba(255,255,255,.78)}
.hero .arrow{color:#fff}
.hero .facts{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.18)}
.hero .facts dd{font-size:.95rem;font-weight:600}\n.rails .ladder{padding-left:calc(clamp(16px,4vw,48px) + 18px)}\n.hero .facts div{background:rgba(8,10,14,.55);color:#fff}
.hero .facts dt{color:rgba(255,255,255,.72)}
.sec,.blk,.comp-list,.refs{border-radius:16px}
.sec{border-color:var(--line);background:var(--panel)}
.tabs button,.sub button{border-radius:999px}
.stick{top:var(--hh)}
.sec{scroll-margin-top:150px}
.theme{background:var(--soft);border-color:transparent}
.thumbs button,.jgt,.fig figure{border-radius:12px}
.skip:focus{z-index:50}
.railwrap{position:relative}
.railwrap::before,.railwrap::after{content:"";position:absolute;top:0;bottom:0;width:56px;z-index:4;pointer-events:none}
.railwrap::before{left:0;background:linear-gradient(90deg,var(--bg),transparent)}
.railwrap::after{right:0;background:linear-gradient(270deg,var(--bg),transparent)}
.rnav{position:absolute;top:50%;margin-top:-26px;z-index:6;width:48px;height:48px;border-radius:50%;border:1px solid var(--line);background:color-mix(in srgb,var(--panel) 92%,transparent);color:var(--ink);font:700 1.7rem/1 var(--display);display:grid;place-items:center;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.45);padding:0 0 4px}
.rnav:hover{background:var(--a);color:var(--a-ink);border-color:var(--a)}
.rnav[hidden]{display:none}
.rnav.prev{left:10px}.rnav.next{right:10px}
@media (max-width:700px){.rnav{width:40px;height:40px;margin-top:-20px;font-size:1.4rem}.rnav.prev{left:4px}.rnav.next{right:4px}}
@media (max-width:700px){
  .rail{gap:8px 12px;padding:10px 14px}.brand{font-size:1.1rem}.mode{min-width:0;flex:1}.search{flex:1 1 100%;margin:0;width:100%}
  .rails .ladder button{width:148px;height:204px}.rails .ladder .belt{height:96px;flex-basis:96px}
  .hero{border-radius:16px}.stick{top:0}
}
"""

RAILJS = """<script>
(function(){var ul=document.getElementById('ladder'),p=document.querySelector('.rnav.prev'),n=document.querySelector('.rnav.next');if(!ul||!p||!n)return;
function upd(){var max=ul.scrollWidth-ul.clientWidth-2;p.hidden=ul.scrollLeft<=2;n.hidden=ul.scrollLeft>=max||max<=0}
function go(d){ul.scrollBy({left:d*Math.max(240,ul.clientWidth*.8),behavior:'smooth'})}
p.addEventListener('click',function(){go(-1)});n.addEventListener('click',function(){go(1)});
ul.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);
new MutationObserver(function(){var c=ul.querySelector('[aria-current="true"]');if(c){var a=c.getBoundingClientRect(),b=ul.getBoundingClientRect();if(a.left<b.left+8||a.right>b.right-8)ul.scrollLeft+=(a.left-b.left)-(b.width-a.width)/2}upd()}).observe(ul,{childList:true,subtree:true,attributes:true,attributeFilter:['aria-current']});
setTimeout(upd,300);})();
</script>
"""


def aplicar(h):
    if "camada visual da versão multiplataforma" in h: return h
    h = re.sub(r"<script>try\{ if\(matchMedia\('\(max-width:700px\)'\).*?</script>\n?", "", h, count=1, flags=re.S)
    h = h.replace('<html lang="pt-BR">', '<html lang="pt-BR" data-theme="dark">', 1)
    h = h.replace("<title>Faixa a faixa — Judô e Jiu-Jitsu</title>", "<title>JudoBJJApp — Judô e Jiu-Jitsu</title>", 1)
    h = h.replace('<meta name="viewport" content="width=device-width, initial-scale=1">', '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#0b0d11">', 1)
    a = h.index('<aside class="rail"'); b = h.index("</aside>", a) + len("</aside>")
    novo = '''<header class="rail" aria-label="Navegação">
    <div class="brand">Faixa a faixa</div>
    <div class="mode" role="group" aria-label="Modalidade">
      <button id="m-judo" aria-pressed="true">Judô</button>
      <button id="m-bjj" aria-pressed="false">Jiu-Jitsu</button>
    </div>
    <button id="lang" class="langbtn" type="button" aria-label="Idioma"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 4 5.8 4 9s-1.4 6.2-4 9c-2.6-2.8-4-5.8-4-9s1.4-6.2 4-9z"/></svg><span class="lt">PT-BR</span></button>
    <input class="search" id="q" type="search" placeholder="Buscar técnica ou termo" aria-label="Buscar técnica ou termo">
  </header>
  <section class="rails" aria-label="Transições de faixa"><h2 class="railt">Escolha o exame</h2><div class="railwrap"><button class="rnav prev" type="button" aria-label="Ver faixas anteriores (rolar para a esquerda)" hidden>&#8249;</button><ul class="ladder" id="ladder"></ul><button class="rnav next" type="button" aria-label="Ver mais faixas (rolar para a direita)" hidden>&#8250;</button></div></section>'''
    h = h[:a] + novo + h[b:]
    h = h.replace("</body>", RAILJS + "</body>", 1)
    return h.replace("</style>\n</head>", CSS + "</style>\n</head>", 1) if "</style>\n</head>" in h else h.replace("</head>", "<style>" + CSS + "</style></head>", 1)
