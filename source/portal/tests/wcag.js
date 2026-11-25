/* Auditoria WCAG 2.2 AA automatizável (complementa acessibilidade.js): idioma, título, marcos, hierarquia de títulos, ids duplicados,
   tamanho de alvo (2.5.8), contraste (1.4.3), foco visível (2.4.7), ordem de tabulação sem armadilha (2.1.2), padrões ARIA incorretos e
   controle de pausa para movimento automático (2.2.2). Rodar: playwright-cli --raw run-code --filename=wcag.js (site em 127.0.0.1:8793). */
async page => {
  const BASE = 'http://127.0.0.1:8793';
  const URLS = ['/', '/#/judo', '/#/judo/j04', '/#/jiu-jitsu/b03', '/#/sobre', '/explorar/#/judo', '/explorar/#/judo/faixa/j04', '/explorar/#/judo/tecnica/uchi-mata', '/explorar/#/jiu-jitsu/faixa/b03', '/explorar/#/jiu-jitsu/item/o-soto-gari', '/livro.html', '/app/#bjj/b03', '/explorar/#/judo/faixa/j05/acumulado', '/explorar/#/judo/faixa/j13/acumulado', '/explorar/#/jiu-jitsu/faixa/b03/acumulado', '/explorar/#/jiu-jitsu/faixa/k2/acumulado'];
  const bad = [], manual = new Set();
  for (const th of ['dark', 'light']) {
    for (const u of URLS) {
      await page.setViewportSize({ width: 1366, height: 820 });
      await page.goto(BASE + '/'); await page.evaluate(t => { localStorage.setItem('jt-theme', t); localStorage.setItem('jt-lang', 'pt'); localStorage.removeItem('jt-layout'); }, th);
      await page.goto(BASE + u, { waitUntil: 'networkidle' }); await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(900);
      const r = await page.evaluate(() => {
        const out = [], man = [];
        const vis = e => { const b = e.getBoundingClientRect(), s = getComputedStyle(e); if (s.visibility === 'hidden' || s.display === 'none' || b.width === 0 || b.height === 0) return false; for (let n = e; n; n = n.parentElement) if (n.getAttribute && n.getAttribute('aria-hidden') === 'true') return false; return true; };
        const d = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\s+/)[0] : '');
        if (!document.documentElement.lang) out.push('3.1.1 <html> sem lang');
        if (!document.title || document.title.length < 4) out.push('2.4.2 página sem título');
        if (!document.querySelector('main, [role=main], #conteudo')) out.push('1.3.1 sem marco principal (main)');
        if (!document.querySelector('header, [role=banner]')) out.push('1.3.1 sem marco de cabeçalho');
        const h1 = [...document.querySelectorAll('h1')].filter(vis).length; if (h1 !== 1) out.push('1.3.1 esperado 1 <h1> visível, encontrado ' + h1);
        let last = 0; [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).forEach(h => { const n = +h.tagName[1]; if (last && n > last + 1) out.push('1.3.1 salto de título h' + last + ' → h' + n + ': ' + h.textContent.trim().slice(0, 30)); last = n; });
        const ids = {}; document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id] || 0) + 1; }); Object.keys(ids).filter(k => ids[k] > 1).slice(0, 4).forEach(k => out.push('4.1.1 id duplicado: ' + k));
        const skip = document.querySelector('a.skip, a[href="#conteudo"]'); if (!skip) out.push('2.4.1 sem link "pular para o conteúdo"'); else { const t = skip.getAttribute('href'); if (t && t.startsWith('#') && t.length > 1 && !document.querySelector(t)) out.push('2.4.1 link de pular aponta para alvo inexistente ' + t); }
        // tamanho de alvo 2.5.8 (mínimo 24x24, exceto links em linha de texto)
        const tgt = []; document.querySelectorAll('button, a.nc, a.btn, .sel, .bb, .pbtn, [role=button], input[type=checkbox], input[type=radio], select, nav a, .seg button, .tcard, .card').forEach(e => { if (!vis(e)) return; const b = e.getBoundingClientRect(); if (b.top > innerHeight * 4) return; if (Math.min(b.width, b.height) < 24) tgt.push(d(e) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height)); }); if (tgt.length) out.push('2.5.8 alvos < 24px (' + tgt.length + '): ' + tgt.slice(0, 4).join('; '));
        // padrões ARIA que exigem teclado específico
        document.querySelectorAll('[role=listbox]').forEach(e => { if (vis(e)) out.push('4.1.2 role=listbox exige navegação por setas; use group/botões com aria-pressed: ' + d(e)); });
        document.querySelectorAll('[role=option]').forEach(e => { if (vis(e) && !e.closest('[role=listbox]')) out.push('4.1.2 role=option fora de listbox: ' + d(e)); });
        document.querySelectorAll('[aria-live]').forEach(e => { if (e.getAttribute('aria-live') !== 'off' && e.closest('#gal, .gallery')) out.push('4.1.3 região viva dentro de carrossel automático: ' + d(e)); });
        // movimento automático precisa de pausa (2.2.2)
        if (document.querySelector('.gallery .sl') && !document.querySelector('#gPause')) out.push('2.2.2 carrossel automático sem botão de pausa');
        // contraste 1.4.3 (texto sobre fundo sólido; sobre foto vira verificação manual)
        const parse = c => { let m = c.match(/rgba?\(([^)]+)\)/); if (m) { const p = m[1].split(',').map(x => parseFloat(x)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; } m = c.match(/color\(srgb ([^)]+)\)/); if (m) { const [rgb, al] = m[1].split('/'); const q = rgb.trim().split(/\s+/).map(x => parseFloat(x) * 255); return { r: q[0], g: q[1], b: q[2], a: al ? parseFloat(al) : 1 }; } return null; };
        const over = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
        const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
        const bgOf = e => { let layers = [], overPhoto = false; for (let n = e; n; n = n.parentElement) { if (n.classList && (n.classList.contains('gallery') || n.classList.contains('home-view'))) overPhoto = true; const s = getComputedStyle(n); if (s.backgroundImage && s.backgroundImage !== 'none') overPhoto = true; const c = parse(s.backgroundColor); if (c && c.a > 0) { layers.push(c); if (c.a >= .99) break; } } let base = { r: 255, g: 255, b: 255, a: 1 }; if (!layers.length || layers[layers.length - 1].a < .99) { const bs = parse(getComputedStyle(document.body).backgroundColor); if (bs) base = bs; } let cur = base; for (let i = layers.length - 1; i >= 0; i--) cur = over(layers[i], cur); return { c: cur, overPhoto }; };
        const low = []; const seen = new Set();
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
        while (n = w.nextNode()) { const t = n.textContent.trim(); if (t.length < 2) continue; const e = n.parentElement; if (!e || /SCRIPT|STYLE|NOSCRIPT|OPTION/.test(e.tagName) || !vis(e) || seen.has(e)) continue; seen.add(e);
          const s = getComputedStyle(e), fg = parse(s.color); if (!fg) continue; const bg = bgOf(e); const fgc = fg.a < 1 ? over(fg, bg.c) : fg;
          const L1 = lum(fgc), L2 = lum(bg.c), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05); const px = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700; const large = px >= 24 || (px >= 18.66 && bold); const need = large ? 3 : 4.5;
          if (bg.overPhoto) { man.push('contraste sobre foto (conferir): ' + d(e) + ' "' + t.slice(0, 22) + '"'); continue; }
          if (ratio < need) low.push(d(e) + ' ' + ratio.toFixed(1) + ':1 "' + t.slice(0, 22) + '"'); }
        if (low.length) out.push('1.4.3 contraste insuficiente (' + low.length + '): ' + low.slice(0, 5).join(' | '));
        return { out, man: man.slice(0, 3) };
      });
      r.out.forEach(m => bad.push('[' + th + '] ' + u + ' → ' + m)); r.man.forEach(m => manual.add(m));
      // foco visível e ordem de tabulação (só no tema escuro para poupar tempo)
      if (th === 'dark') {
        await page.evaluate(() => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); window.__tid = 0; });
        const seq = [], noRing = []; let trap = false, last = null, rep = 0;
        for (let i = 0; i < 45; i++) {
          await page.keyboard.press('Tab');
          const info = await page.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; if (!e.__tid) e.__tid = ++window.__tid; const s = getComputedStyle(e); const ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none'); return { id: e.__tid, ring, name: (e.id || e.className || e.tagName).toString().slice(0, 22) }; });
          if (!info) continue; seq.push(info.id); if (!info.ring && !noRing.includes(info.name)) noRing.push(info.name);
          if (info.id === last) { rep++; if (rep >= 3) { trap = true; break; } } else { rep = 0; last = info.id; }
        }
        if (noRing.length) bad.push('[foco] ' + u + ' → 2.4.7 sem indicador de foco ao tabular: ' + noRing.slice(0, 4).join(', '));
        if (trap) bad.push('[teclado] ' + u + ' → 2.1.2 possível armadilha de foco');
        if (new Set(seq).size < 6) bad.push('[teclado] ' + u + ' → poucos elementos alcançáveis por Tab (' + new Set(seq).size + ')');
      }
    }
  }
  return JSON.stringify({ ok: bad.length === 0, total: bad.length, problemas: bad.slice(0, 70), verificarManual: [...manual].slice(0, 12) }, null, 1);
}
