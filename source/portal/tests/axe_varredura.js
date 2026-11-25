async page => {
  const BASE = 'http://127.0.0.1:8793';
  const URLS = ['/', '/#/judo', '/#/judo/j04', '/#/jiu-jitsu/b03', '/#/sobre', '/explorar/#/judo', '/explorar/#/jiu-jitsu', '/explorar/#/judo/faixa/j04', '/explorar/#/judo/tecnica/uchi-mata', '/explorar/#/jiu-jitsu/faixa/b03', '/explorar/#/jiu-jitsu/item/o-soto-gari', '/explorar/#/judo/t/videoteca', '/livro.html', '/app/#judo/j01', '/app/#bjj/b03', '/explorar/#/judo/faixa/j05/acumulado', '/explorar/#/judo/faixa/j13/acumulado', '/explorar/#/jiu-jitsu/faixa/b03/acumulado', '/explorar/#/jiu-jitsu/faixa/k2/acumulado'];
  const agg = {}, inc = {};
  for (const th of ['dark', 'light']) for (const u of URLS) {
    await page.setViewportSize({ width: 1366, height: 820 });
    await page.goto(BASE + '/'); await page.evaluate(t => { localStorage.setItem('jt-theme', t); localStorage.setItem('jt-lang', 'pt'); localStorage.removeItem('jt-layout'); }, th);
    await page.goto(BASE + u, { waitUntil: 'networkidle' }); await page.reload({ waitUntil: 'networkidle' }); await page.waitForTimeout(900);
    await page.addScriptTag({ url: BASE + '/assets/axe.min.js' });
    const r = await page.evaluate(async () => { const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }); return { v: res.violations.map(v => ({ id: v.id, impact: v.impact, help: v.help, n: v.nodes.length, ex: v.nodes.slice(0, 2).map(n => n.target.join(' ').slice(0, 70) + ' :: ' + (n.failureSummary || '').split('\n').slice(1, 2).join(' ').slice(0, 90)) })), inc: res.incomplete.map(i => ({ id: i.id, n: i.nodes.length })) }; });
    r.v.forEach(v => { const k = v.id; agg[k] = agg[k] || { impact: v.impact, help: v.help, pages: [], ex: v.ex[0], n: 0 }; agg[k].n += v.n; agg[k].pages.push(th[0] + ':' + u); });
    r.inc.forEach(i => { inc[i.id] = (inc[i.id] || 0) + i.n; });
  }
  return JSON.stringify({ violacoes: Object.entries(agg).map(([id, a]) => ({ id, impacto: a.impact, ajuda: a.help, ocorrencias: a.n, paginas: [...new Set(a.pages)].length, exemplo: a.ex, onde: a.pages.slice(0, 3) })), incompleto: inc }, null, 1);
}
