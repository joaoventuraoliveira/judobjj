/* Auditoria de nomes acessíveis (leitores de tela): playwright-cli --raw run-code --filename=acessibilidade.js
   Regras: toda imagem, ícone (svg/emoji/kanji de ícone), faixa desenhada e controle só com ícone precisa de texto associado
   (alt, aria-label, <title>, texto oculto .sr) ou ser decorativo explícito (aria-hidden) ao lado de texto visível. */
async page => {
  const BASE = 'http://127.0.0.1:8793';
  const URLS = ['/', '/#/sobre', '/#/judo', '/#/judo/j04', '/#/jiu-jitsu/b03', '/explorar/#/judo', '/explorar/#/jiu-jitsu', '/explorar/#/judo/faixa/j04', '/explorar/#/judo/faixa/j04/nage',
    '/explorar/#/judo/tecnica/uchi-mata', '/explorar/#/judo/t/videoteca', '/explorar/#/jiu-jitsu/t/quedas', '/explorar/#/judo/t/glossario', '/explorar/#/judo/t/proibidas', '/explorar/#/jiu-jitsu/faixa/b03', '/explorar/#/jiu-jitsu/faixa/b03/proib', '/explorar/#/jiu-jitsu/t/guardas', '/explorar/#/jiu-jitsu/item/o-soto-gari', '/explorar/#/jiu-jitsu/item/single-leg',
    '/livro.html', '/app/#judo/j01', '/app/#bjj/b03'];
  const bad = [], seen = new Set();
  for (const u of URLS) {
    await page.setViewportSize({ width: 1366, height: 820 });
    await page.goto(BASE + '/'); await page.evaluate(() => { localStorage.setItem('jt-theme', 'dark'); localStorage.setItem('jt-lang', 'pt'); localStorage.removeItem('jt-layout'); });
    await page.goto(BASE + u, { waitUntil: 'networkidle' }); await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(900);
    const r = await page.evaluate(() => {
      const out = [];
      const txt = e => (e.textContent || '').replace(/\s+/g, ' ').trim();
      const hidden = e => { for (let n = e; n && n !== document.body; n = n.parentElement) { if (n.getAttribute && (n.getAttribute('aria-hidden') === 'true' || n.hidden)) return true; const s = getComputedStyle(n); if (s.display === 'none' || s.visibility === 'hidden') return true; } return false; };
      const content = e => { let out = ''; e.childNodes.forEach(n => { if (n.nodeType === 3) out += n.textContent; else if (n.nodeType === 1) { if (n.getAttribute('aria-hidden') === 'true' || n.hidden) return; const al = n.getAttribute('aria-label'); if (al) out += ' ' + al + ' '; else if (n.tagName === 'IMG') out += ' ' + (n.getAttribute('alt') || '') + ' '; else if (n.tagName.toLowerCase() === 'svg') { const ti = n.querySelector('title'); if (ti) out += ' ' + ti.textContent + ' '; } else out += ' ' + content(n) + ' '; } }); return out.replace(/\s+/g, ' ').trim(); };
      const name = e => {
        const al = e.getAttribute('aria-label'); if (al && al.trim()) return al.trim();
        const lb = e.getAttribute('aria-labelledby'); if (lb) { const t = lb.split(/\s+/).map(i => { const x = document.getElementById(i); return x ? txt(x) : ''; }).join(' ').trim(); if (t) return t; }
        if (e.tagName === 'IMG') return (e.getAttribute('alt') || '').trim();
        if (e.tagName === 'SVG' || e.tagName === 'svg') { const t = e.querySelector('title'); return t ? txt(t) : ''; }
        let t = content(e); if (t) return t;
        const img = e.querySelector('img[alt]:not([alt=""])'); if (img) return img.getAttribute('alt');
        const sv = e.querySelector('svg[aria-label],svg title'); if (sv) return sv.getAttribute('aria-label') || txt(sv);
        const ti = e.getAttribute('title'); if (ti && ti.trim()) return ti.trim();
        if (e.tagName === 'INPUT' || e.tagName === 'TEXTAREA' || e.tagName === 'SELECT') { if (e.id) { const l = document.querySelector('label[for="' + e.id + '"]'); if (l && txt(l)) return txt(l); } if (e.closest('label') && txt(e.closest('label'))) return txt(e.closest('label')); return (e.getAttribute('placeholder') || '').trim(); }
        return '';
      };
      const desc = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
      document.querySelectorAll('img').forEach(e => { if (hidden(e)) return; if (!e.hasAttribute('alt')) out.push('img sem alt: ' + desc(e) + ' ' + (e.getAttribute('src') || e.dataset.src || '').slice(-30)); else if (!e.getAttribute('alt').trim() && !e.closest('[aria-hidden="true"]') && e.closest('a,button') && !name(e.closest('a,button'))) out.push('img de alt vazio dentro de controle sem nome: ' + desc(e)); });
      document.querySelectorAll('svg').forEach(e => { if (hidden(e)) return; if (e.closest('[aria-hidden="true"]')) return; const interactive = e.closest('a,button'); const n = name(e); const role = e.getAttribute('role');
        if (role === 'img' && !n) out.push('svg role=img sem nome: ' + desc(e));
        else if (!role && !n && interactive && !name(interactive)) out.push('svg em controle sem nome: ' + desc(interactive));
        else if (!role && !n && !interactive && (e.getBoundingClientRect().width > 16)) out.push('svg informativo sem role/nome: ' + desc(e.parentElement) + '>svg'); });
      document.querySelectorAll('a[href],button,[role=button],[role=option],[role=tab],input,select,textarea,summary').forEach(e => { if (hidden(e)) return; if (e.type === 'hidden') return; if (!name(e)) out.push('controle sem nome: ' + desc(e) + ' "' + txt(e).slice(0, 20) + '"'); });
      document.querySelectorAll('[role=img]').forEach(e => { if (hidden(e)) return; if (!name(e)) out.push('[role=img] sem nome: ' + desc(e)); });
      // ícones em texto (emoji/kanji soltos em círculos .ic, .toc-badge, .kc): devem ser decorativos (aria-hidden) ou ter nome
      document.querySelectorAll('.ic,.kc,.bd,.kj,.sel .go,.arr').forEach(e => { if (hidden(e)) return; if (e.getAttribute('role') === 'button' && name(e)) return; if (e.closest('[aria-hidden="true"]')) return; const t = txt(e); if (t && /[^\x00-\x7F]/.test(t) && !e.hasAttribute('aria-label') && !e.closest('a,button')) out.push('ícone em texto sem tratamento: ' + desc(e) + ' "' + t.slice(0, 6) + '"'); });
      // fundos de imagem com significado (miniaturas, recortes de ilustração)
      document.querySelectorAll('[style*="background-image"], .slice, .th').forEach(e => { if (hidden(e)) return; if (e.closest('[aria-hidden="true"]')) return; if (e.getAttribute('role') === 'img' && name(e)) return; if (e.closest('a,button') && name(e.closest('a,button'))) return; out.push('imagem de fundo sem texto: ' + desc(e)); });
      document.querySelectorAll('.belt').forEach(e => { if (hidden(e)) return; if (e.closest('[aria-hidden="true"]')) return; const c = e.closest('a,button,li,div'); if (e.getAttribute('role') === 'img' && name(e)) return; if (!(e.closest('a,button') && name(e.closest('a,button')))) out.push('faixa (div .belt) sem texto: ' + desc(e)); });
      // regra das faixas: todo desenho de faixa precisa ter nome iniciando por "Faixa"
      const beltName = e => { const c = e.closest('a,button,[role=option]') || e; const own = name(e) || ''; const outer = name(c) || ''; return own || outer; };
      document.querySelectorAll('svg.bsvg, svg[aria-label^="Faixa"], .belt-card svg, .belt-svg').forEach(e => { if (hidden(e)) return; const c = e.closest('a,button,[role=option]'); const n = (c && name(c)) || name(e); if (!/^Faixa\b/i.test(n || '')) out.push('desenho de faixa sem nome "Faixa …": ' + desc(e) + ' → "' + (n || '').slice(0, 40) + '"'); });
      document.querySelectorAll('.bb, .belt-card, .ladder button').forEach(e => { if (hidden(e)) return; const n = name(e); if (!/Faixa/i.test(n || '') ) out.push('controle de faixa sem a palavra "Faixa": ' + desc(e) + ' → "' + (n || '').slice(0, 40) + '"'); });
      // emoji/símbolos soltos precisam estar ocultos ao leitor de tela ou ter rótulo
      const EMO = /[\u{1F300}-\u{1FAFF}\u2600-\u27BF\u2B50\u25B6\u2190-\u21FF]/u;
      document.querySelectorAll('h1,h2,h3,h4,button,a,span,div,p,li,summary').forEach(e => { if (hidden(e)) return; if (e.children.length) return; const t = txt(e); if (!t || !EMO.test(t) || e.closest('[aria-hidden="true"]')) return; if (t.replace(EMO, '').replace(/[\s\u2190-\u21FF‹›✕☰★]/g, '').length > 0 && !/^[\W]*$/.test(t.replace(EMO,''))) { if (!/^[\u{1F300}-\u{1FAFF}\u2600-\u27BF\u25B6\s]+\S/u.test(t)) return; out.push('emoji junto de texto, sem ocultar: ' + desc(e) + ' "' + t.slice(0, 24) + '"'); return; } if (!e.getAttribute('aria-label')) out.push('símbolo/emoji sem rótulo: ' + desc(e) + ' "' + t.slice(0, 6) + '"'); });
      document.querySelectorAll('.ic').forEach(e => { if (hidden(e)) return; if (e.closest('[aria-hidden="true"]')) return; if (!e.hasAttribute('aria-hidden') && !e.getAttribute('aria-label')) out.push('.ic sem aria-hidden: ' + desc(e) + ' "' + txt(e).slice(0, 6) + '"'); });
      // NORMA PÉTREA: vídeos, iframes, diálogos, canvas, elementos clicáveis sem papel, alt genérico e links em nova aba
      const GEN = /^(v[ií]deo|video|imagem|image|foto|photo|frame|iframe|player|youtube|figura|ícone|icone|icon|img)$/i;
      document.querySelectorAll('iframe').forEach(e => { if (hidden(e)) return; const ti = (e.getAttribute('title') || e.getAttribute('aria-label') || '').trim(); if (!ti) out.push('iframe sem title: ' + desc(e)); else if (GEN.test(ti)) out.push('iframe com title genérico "' + ti + '": ' + desc(e)); });
      document.querySelectorAll('video, audio').forEach(e => { if (hidden(e)) return; if (!(e.getAttribute('aria-label') || e.getAttribute('title') || e.querySelector('track'))) out.push('mídia sem rótulo/legenda: ' + desc(e)); if (!e.hasAttribute('controls')) out.push('mídia sem controles: ' + desc(e)); });
      document.querySelectorAll('canvas').forEach(e => { if (hidden(e)) return; if (e.getAttribute('role') !== 'img' || !name(e)) out.push('canvas sem role=img e nome: ' + desc(e)); });
      document.querySelectorAll('dialog').forEach(e => { if (!(e.getAttribute('aria-label') || e.getAttribute('aria-labelledby'))) out.push('dialog sem nome: ' + desc(e)); });
      document.querySelectorAll('input[type=image]').forEach(e => { if (!(e.getAttribute('alt') || '').trim()) out.push('input image sem alt: ' + desc(e)); });
      document.querySelectorAll('img[alt]').forEach(e => { if (hidden(e)) return; const al = e.getAttribute('alt').trim(); if (al && (GEN.test(al) || /\.(jpe?g|png|webp|svg|gif)$/i.test(al) || /^(img|dsc|image)[-_ ]?\d+/i.test(al))) out.push('alt genérico ou nome de arquivo "' + al.slice(0, 30) + '": ' + desc(e)); });
      document.querySelectorAll('div, span, li, p, td, section, article').forEach(e => { if (hidden(e) || e.closest('a,button,label,summary,[role=button],[tabindex]')) return; if (e.getAttribute('role') || e.hasAttribute('tabindex')) return; const cs = getComputedStyle(e); if (cs.cursor === 'pointer' && !e.querySelector('a,button,input,select,textarea')) out.push('elemento clicável sem papel de botão/link: ' + desc(e) + ' "' + txt(e).slice(0, 18) + '"'); });
      document.querySelectorAll('a[target=_blank]').forEach(e => { if (hidden(e)) return; if (!/nova aba|new tab|nova janela|new window/i.test(name(e))) out.push('link em nova aba sem aviso para leitor de tela: ' + desc(e) + ' "' + txt(e).slice(0, 24) + '"'); });
      document.querySelectorAll('[role=button]:not(button):not(a)').forEach(e => { if (hidden(e)) return; if (!e.hasAttribute('tabindex')) out.push('role=button sem tabindex (inacessível por teclado): ' + desc(e)); });

      // LEITURA POR MOUSE (rastreamento do NVDA): o elemento informativo precisa receber o ponteiro, sem sobreposição que o esconda,
      // e o objeto sob o ponteiro precisa ter nome/texto. Testa o centro de cada imagem, ícone, botão, link, título e vídeo.
      const inf = [...document.querySelectorAll('img[alt]:not([alt=""]), svg[role=img], [role=img], button, a[href], h1, h2, h3, iframe, video, input, summary, [role=button]')].filter(e => { if (hidden(e)) return false; const s = getComputedStyle(e); if (parseFloat(s.opacity) === 0 || s.pointerEvents === 'none') return !!(e.matches('img,svg,[role=img]') && parseFloat(s.opacity) > 0); if (e.closest('.sl') && !e.classList.contains('on')) return false; return true; }).slice(0, 140);
      inf.forEach(e => {
        e.scrollIntoView({ block: 'center', inline: 'center' });
        const b = e.getBoundingClientRect(); if (b.width < 2 || b.height < 2) return;
        const cx = Math.min(innerWidth - 2, Math.max(2, b.left + b.width / 2)), cy = Math.min(innerHeight - 2, Math.max(2, b.top + b.height / 2));
        const top = document.elementFromPoint(cx, cy); if (!top) return;
        const ok = e === top || e.contains(top) || top.contains(e);
        const tn = name(top) || name(top.closest('a,button,[role],h1,h2,h3,h4,li,summary,label,p') || top);
        if (!ok && !tn && !e.matches('a.skip,.skip')) out.push('mouse: ' + desc(e) + ' coberto por ' + desc(top) + ' sem texto (o leitor não anuncia ao passar o ponteiro)');
        else if (!name(e) && !(e.matches('img,svg,[role=img]') && name(e))) out.push('mouse: objeto sob o ponteiro sem nome: ' + desc(e));
      });
      window.scrollTo(0, 0);
      return out;
    });
    r.forEach(m => { const k = m; if (!seen.has(k)) { seen.add(k); bad.push(u + ' → ' + m); } });
  }
  return JSON.stringify({ ok: bad.length === 0, total: bad.length, problemas: bad.slice(0, 80) }, null, 1);
}

