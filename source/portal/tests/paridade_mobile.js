/* Testes de paridade desktop x smartphone (Playwright CLI: playwright-cli --raw run-code --filename=paridade_mobile.js).
   Exige o site servido em http://127.0.0.1:8793/ (ver rodar_testes_mobile.ps1).
   O que cada perfil de celular precisa ter igual ao desktop: estrutura, animações e design (fontes, tokens, cartões), sem rolagem horizontal. */
async page => {
  const BASE = 'http://127.0.0.1:8793';
  const PAGES = [
    { id: 'inicio', url: '/', fonts: true },
    { id: 'sobre', url: '/#/sobre', fonts: true },
    { id: 'bjj-item', url: '/explorar/#/jiu-jitsu/item/o-soto-gari', fonts: true },
    { id: 'explorar', url: '/explorar/#/judo', fonts: true },
    { id: 'livro', url: '/livro.html', fonts: true },
    { id: 'app', url: '/app/#judo/j01', fonts: false }
  ];
  const PROFILES = [
    { id: 'desktop', w: 1366, h: 820, layout: '' },
    { id: 'celular-390', w: 390, h: 844, layout: '' },
    { id: 'celular-320', w: 320, h: 568, layout: '' },
    { id: 'layout-celular-no-pc', w: 1366, h: 820, layout: 'mobile' }
  ];
  const THEMES = ['dark', 'light'];
  const fails = [], notes = [], sigs = {};
  const fail = (m) => fails.push(m);
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERR ' + e.message));

  for (const pg of PAGES) {
    for (const th of THEMES) {
      for (const pr of PROFILES) {
        const tag = pg.id + '/' + th + '/' + pr.id;
        errs.length = 0;
        await page.setViewportSize({ width: pr.w, height: pr.h });
        await page.goto(BASE + '/');
        await page.evaluate(([t, y]) => { localStorage.setItem('jt-theme', t); localStorage.setItem('jt-lang', 'pt'); if (y) localStorage.setItem('jt-layout', y); else localStorage.removeItem('jt-layout'); }, [th, pr.layout]);
        await page.goto(BASE + pg.url, { waitUntil: 'networkidle' });
        await page.reload({ waitUntil: 'networkidle' });
        await page.waitForTimeout(1100);
        const r = await page.evaluate((opt) => {
          const vis = e => { const b = e.getBoundingClientRect(), s = getComputedStyle(e); return b.width > 0 && b.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
          const hdr = document.querySelector('header.top, header, .top');
          const hb = hdr ? hdr.getBoundingClientRect() : { height: 0 };
          const small = [];
          document.querySelectorAll('button, a.nc, a.btn, .sel, .bb, .pbtn, nav a, .seg button').forEach(e => {
            if (!vis(e)) return; const b = e.getBoundingClientRect();
            if (b.top > innerHeight * 3) return; if (Math.min(b.width, b.height) < 30) small.push((e.id || e.className || e.tagName).toString().slice(0, 30) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height));
          });
          const hs = [...document.querySelectorAll('h1,h2,h3')].map(h => h.textContent.trim().replace(/\s+/g, ' ')).filter(Boolean);
          return {
            overflow: document.documentElement.scrollWidth - innerWidth,
            headerRatio: hb.height / innerHeight,
            small: small.slice(0, 6), smallN: small.length,
            fontsDisplay: opt.fonts ? document.fonts.check('16px Fraunces') && document.fonts.check('16px Inter') : true,
            bodyBg: getComputedStyle(document.body).backgroundColor,
            headings: hs
          };
        }, { fonts: pg.fonts });
        if (r.overflow > 1) fail(tag + ': rolagem horizontal de ' + r.overflow + 'px');
        if (pr.w <= 600 && r.headerRatio > (pr.h < 600 ? 0.46 : 0.3)) fail(tag + ': cabeçalho ocupa ' + Math.round(r.headerRatio * 100) + '% da altura (máx. 30%, 46% em telas de 568px)');
        if (r.smallN > 0) notes.push(tag + ': ' + r.smallN + ' alvo(s) de toque < 30px: ' + r.small.join('; '));
        if (!r.fontsDisplay) fail(tag + ': fontes locais (Fraunces/Inter) não carregaram');
        if (errs.length) fail(tag + ': erros no console: ' + errs.slice(0, 2).join(' | '));
        const key = pg.id + '/' + th;
        sigs[key] = sigs[key] || {};
        sigs[key][pr.id] = r.headings.slice().sort().join('|');
        if (th === 'dark' && pg.id === 'inicio' && r.bodyBg === 'rgb(255, 255, 255)') fail(tag + ': fundo claro no tema escuro');
      }
    }
  }
  // paridade de estrutura: os mesmos títulos existem no desktop e em cada perfil de celular
  for (const key of Object.keys(sigs)) {
    const d = sigs[key]['desktop'];
    for (const pr of PROFILES.slice(1)) if (sigs[key][pr.id] !== d) fail(key + '/' + pr.id + ': títulos (h1-h3) diferentes do desktop');
  }

  // fluxo da tela inicial (estrutura, animações e navegação) idêntico em todos os perfis
  const flow = {};
  for (const pr of PROFILES) {
    await page.setViewportSize({ width: pr.w, height: pr.h });
    await page.goto(BASE + '/');
    await page.evaluate(y => { localStorage.setItem('jt-theme', 'dark'); localStorage.setItem('jt-lang', 'pt'); if (y) localStorage.setItem('jt-layout', y); else localStorage.removeItem('jt-layout'); }, pr.layout);
    await page.goto(BASE + '/', { waitUntil: 'networkidle' }); await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(900);
    const s0 = await page.evaluate(() => {
      const mot = sel => { const e = document.querySelector(sel); if (!e) return 'ausente'; const c = getComputedStyle(e); return (c.transitionDuration !== '0s' || c.animationName !== 'none') ? 'anima' : 'parado'; };
      const g = document.querySelector('.gallery').getBoundingClientRect();
      return { sels: document.querySelectorAll('.sel').length, slides: document.querySelectorAll('.sl').length, fnav: !!document.querySelector('.fnav'), drawerLinks: document.querySelectorAll('#dc a').length,
        galleryVisibleAbove: g.top < innerHeight, motion: ['.sel', '.gallery .sl', '.dot', '.fnav button'].map(mot).join(','), kanji: [...document.querySelectorAll('.sel .kc')].map(k => k.textContent).join('') };
    });
    await page.click('.sel[data-m="judo"]'); await page.waitForTimeout(1000);
    const s1 = await page.evaluate(() => ({ hash: location.hash, study: document.body.classList.contains('in-study'), belts: document.querySelectorAll('.bb').length }));
    await page.click('.bb:nth-of-type(4)'); await page.waitForTimeout(900);
    const s2 = await page.evaluate(() => {
      const mot = sel => { const e = document.querySelector(sel); if (!e) return 'ausente'; const c = getComputedStyle(e); return (c.transitionDuration !== '0s' || c.animationName !== 'none') ? 'anima' : 'parado'; };
      return { hash: location.hash, crumbPills: document.querySelectorAll('.cp').length, cards: document.querySelectorAll('.nc').length, motion: ['.nc', '.cp', '.bb', '.study-view'].map(mot).join(','), titles: [...document.querySelectorAll('.nc h4')].map(h => h.textContent).join('|') };
    });
    await page.click('.nc[data-h]'); await page.waitForTimeout(800);
    const s3 = await page.evaluate(() => ({ hash: location.hash, items: document.querySelectorAll('.nc').length, firstHref: (document.querySelector('.nc') || {}).getAttribute ? document.querySelector('.nc').getAttribute('href') : '' }));
    await page.goBack(); await page.waitForTimeout(600);
    const s4 = await page.evaluate(() => location.hash);
    await page.click('#stHome'); await page.waitForTimeout(700);
    const s5 = await page.evaluate(() => ({ study: document.body.classList.contains('in-study'), hash: location.hash }));
    flow[pr.id] = { s0, s1, s2, s3, s4, s5 };
    if (!s1.study || s1.belts < 10) fail('fluxo/' + pr.id + ': ao tocar em Judô a tela de faixas não abriu (faixas=' + s1.belts + ')');
    if (s2.cards < 5) fail('fluxo/' + pr.id + ': a faixa não mostrou os tópicos (cards=' + s2.cards + ')');
    if (s3.items < 1 || !/explorar\/#\/judo\/tecnica\//.test(s3.firstHref || '')) fail('fluxo/' + pr.id + ': a seção não levou às técnicas do explorador');
    if (s5.study) fail('fluxo/' + pr.id + ': o botão Início não voltou à tela inicial');
    if (!s0.galleryVisibleAbove) fail('fluxo/' + pr.id + ': a galeria não aparece na primeira tela');
  }
  const d = flow['desktop'];
  for (const pr of PROFILES.slice(1)) {
    const f = flow[pr.id];
    for (const k of ['sels', 'slides', 'fnav', 'drawerLinks', 'motion', 'kanji']) if (JSON.stringify(f.s0[k]) !== JSON.stringify(d.s0[k])) fail('paridade/' + pr.id + ': inicio.' + k + ' = ' + f.s0[k] + ' (desktop ' + d.s0[k] + ')');
    for (const k of ['belts']) if (f.s1[k] !== d.s1[k]) fail('paridade/' + pr.id + ': quantidade de faixas ' + f.s1[k] + ' != ' + d.s1[k]);
    for (const k of ['crumbPills', 'cards', 'motion', 'titles']) if (f.s2[k] !== d.s2[k]) fail('paridade/' + pr.id + ': faixa.' + k + ' diferente do desktop');
    if (f.s3.items !== d.s3.items) fail('paridade/' + pr.id + ': itens da seção diferem do desktop');
  }
  return JSON.stringify({ ok: fails.length === 0, falhas: fails, avisos: notes.slice(0, 12), perfis: PROFILES.map(p => p.id), paginas: PAGES.map(p => p.id) }, null, 1);
}

