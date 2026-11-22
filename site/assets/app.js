/* Judô · exames de faixa — interações do site (sem dependências) */
(() => {
  const root = document.documentElement;
  const store = { get: k => { try { return localStorage.getItem(k); } catch (e) { return null; } },
                  set: (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} } };

  /* ---------- layout: auto | desktop | mobile ---------- */
  const mq = window.matchMedia('(max-width: 900px)');
  function applyLayout() {
    const pref = root.dataset.layout || 'auto';
    const mobile = pref === 'mobile' || (pref === 'auto' && mq.matches);
    root.classList.toggle('lay-mobile', mobile);
    root.classList.toggle('lay-desktop', !mobile);
    document.querySelectorAll('[data-layout-set]').forEach(b => b.setAttribute('aria-pressed', b.dataset.layoutSet === pref));
    if (!mobile) closeDrawer();
  }
  mq.addEventListener ? mq.addEventListener('change', applyLayout) : mq.addListener(applyLayout);
  document.querySelectorAll('[data-layout-set]').forEach(b => b.addEventListener('click', () => {
    root.dataset.layout = b.dataset.layoutSet; store.set('jt-layout', b.dataset.layoutSet); applyLayout();
  }));

  /* ---------- tema: auto | light | dark ---------- */
  const themes = ['auto', 'light', 'dark'];
  function applyTheme() {
    const t = root.dataset.theme || 'auto';
    document.querySelectorAll('[data-theme-set]').forEach(b => b.setAttribute('aria-pressed', b.dataset.themeSet === t));
    const dark = t === 'dark' || (t === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    document.querySelector('meta[name="theme-color"]').setAttribute('content', dark ? '#161b22' : '#0f3d8c');
  }
  function setTheme(t) { root.dataset.theme = t; store.set('jt-theme', t); applyTheme(); }
  document.querySelectorAll('[data-theme-set]').forEach(b => b.addEventListener('click', () => setTheme(b.dataset.themeSet)));

  /* ---------- gaveta do sumário (celular) ---------- */
  const menuBtn = document.querySelector('.menu-btn'), scrim = document.querySelector('.scrim');
  function openDrawer() { root.classList.add('drawer-open'); scrim.hidden = false; menuBtn.setAttribute('aria-expanded', 'true'); }
  function closeDrawer() { root.classList.remove('drawer-open'); scrim.hidden = true; menuBtn && menuBtn.setAttribute('aria-expanded', 'false'); }
  menuBtn.addEventListener('click', () => root.classList.contains('drawer-open') ? closeDrawer() : openDrawer());
  scrim.addEventListener('click', closeDrawer);
  document.querySelectorAll('.side a').forEach(a => a.addEventListener('click', () => { if (root.classList.contains('lay-mobile')) closeDrawer(); }));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDrawer(); });

  /* ---------- barra inferior ---------- */
  const top = document.querySelector('.top'), q = document.getElementById('q');
  document.querySelectorAll('.bottom button').forEach(b => b.addEventListener('click', () => {
    const a = b.dataset.act;
    if (a === 'menu') openDrawer();
    if (a === 'top') window.scrollTo({ top: 0 });
    if (a === 'theme') setTheme(themes[(themes.indexOf(root.dataset.theme || 'auto') + 1) % 3]);
    if (a === 'search') { top.classList.toggle('searching'); if (top.classList.contains('searching')) q.focus(); }
  }));

  /* ---------- busca ---------- */
  const results = document.querySelector('.results');
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const data = (window.SEARCH || []).map(d => ({ ...d, n: norm(d.t) }));
  q.addEventListener('input', () => {
    const v = norm(q.value.trim());
    results.innerHTML = '';
    if (v.length < 2) { results.classList.remove('open'); return; }
    const hits = data.filter(d => d.n.includes(v)).slice(0, 12);
    hits.forEach(h => { const li = document.createElement('li'); li.innerHTML = `<a href="${h.h}" data-jump>${h.t}</a>`; results.appendChild(li); });
    if (!hits.length) results.innerHTML = '<li style="padding:8px 10px;color:var(--muted)">Nada encontrado</li>';
    results.classList.add('open');
  });
  results.addEventListener('click', () => { results.classList.remove('open'); top.classList.remove('searching'); q.value = ''; });
  document.addEventListener('click', e => { if (!e.target.closest('.search')) results.classList.remove('open'); });

  /* ---------- carrosséis ---------- */
  document.querySelectorAll('.carousel').forEach(c => {
    const track = c.querySelector('.track'), slides = [...track.children];
    const prev = c.querySelector('.car-prev'), next = c.querySelector('.car-next');
    const count = c.querySelector('.car-count'), dots = c.querySelector('.dots');
    slides.forEach(() => dots.appendChild(document.createElement('i')));
    let cur = 0;
    const go = i => { i = Math.max(0, Math.min(slides.length - 1, i)); track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft }); };
    const update = () => {
      cur = Math.round(track.scrollLeft / (slides[0].offsetWidth + 16));
      count.textContent = `${cur + 1} / ${slides.length}`;
      prev.disabled = cur === 0; next.disabled = cur === slides.length - 1;
      [...dots.children].forEach((d, k) => d.classList.toggle('on', k === cur));
    };
    prev.addEventListener('click', () => go(cur - 1)); next.addEventListener('click', () => go(cur + 1));
    track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    track.tabIndex = 0;
    track.addEventListener('keydown', e => { if (e.key === 'ArrowRight') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    update();
  });
  /* links do índice levam ao slide certo dentro do carrossel */
  function jump(hash) {
    const el = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!el) return false;
    if (el.classList.contains('slide')) {
      const track = el.parentElement;
      track.closest('.carousel').scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => track.scrollTo({ left: el.offsetLeft - track.offsetLeft }), 350);
      history.replaceState(null, '', hash);
      return true;
    }
    return false;
  }
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (a && jump(a.getAttribute('href'))) e.preventDefault();
  });
  if (location.hash) setTimeout(() => jump(location.hash), 300);

  /* ---------- lightbox com zoom ---------- */
  const lb = document.querySelector('.lightbox'), lbImg = lb.querySelector('img'), stage = lb.querySelector('.lb-stage');
  document.querySelectorAll('.zoom').forEach(b => b.addEventListener('click', () => {
    lbImg.src = b.dataset.src; lbImg.alt = b.getAttribute('aria-label'); stage.classList.remove('zoomed');
    lb.showModal ? lb.showModal() : lb.setAttribute('open', '');
  }));
  lbImg.addEventListener('click', () => stage.classList.toggle('zoomed'));
  lb.querySelector('.lb-close').addEventListener('click', () => lb.close());
  lb.addEventListener('click', e => { if (e.target === lb || e.target === stage) lb.close(); });

  /* ---------- tabelas em cartões no celular ---------- */
  document.querySelectorAll('.table-wrap').forEach(w => {
    const heads = [...w.querySelectorAll('thead th')].map(th => th.textContent.trim());
    if (heads.length >= 3) {
      w.classList.add('cards');
      w.querySelectorAll('tbody tr').forEach(tr => [...tr.children].forEach((td, i) => td.setAttribute('data-label', heads[i] || '')));
    }
  });

  /* ---------- simulado interativo ---------- */
  document.querySelectorAll('.quiz').forEach(qz => {
    const qs = JSON.parse(qz.dataset.quiz); let right = 0, done = 0;
    const score = document.createElement('div'); score.className = 'quiz-score';
    const render = () => score.innerHTML = `<span>Acertos: ${right} de ${qs.length} · respondidas: ${done}</span><button type="button">Recomeçar</button>`;
    qs.forEach((item, n) => {
      const box = document.createElement('div'); box.className = 'q';
      box.innerHTML = `<p>${n + 1}. ${item.q}</p><div class="opts"></div>`;
      const opts = box.querySelector('.opts');
      item.opts.forEach(([k, t]) => {
        const b = document.createElement('button'); b.type = 'button'; b.textContent = `(${k}) ${t}`;
        b.addEventListener('click', () => {
          if (box.dataset.done) return; box.dataset.done = 1; done++;
          if (k === item.ans) { b.classList.add('right'); right++; }
          else { b.classList.add('wrong'); opts.children[item.opts.findIndex(o => o[0] === item.ans)].classList.add('right'); }
          render();
        });
        opts.appendChild(b);
      });
      qz.appendChild(box);
    });
    qz.appendChild(score); render();
    score.addEventListener('click', e => { if (e.target.tagName === 'BUTTON') { right = 0; done = 0; qz.innerHTML = ''; qz.removeAttribute('data-built'); location.reload(); } });
  });

  /* ---------- sumário ativo + progresso ---------- */
  const links = [...document.querySelectorAll('.side .toc > li > a')];
  const bar = document.querySelector('.progress span');
  const heads = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  function onScroll() {
    const h = document.documentElement;
    bar.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%';
    let act = 0;
    heads.forEach((el, i) => { if (el.getBoundingClientRect().top < 120) act = i; });
    links.forEach((a, i) => { a.classList.toggle('active', i === act); a.parentElement.classList.toggle('open', i === act); });
  }
  window.addEventListener('scroll', () => requestAnimationFrame(onScroll), { passive: true });

  applyLayout(); applyTheme(); onScroll();
})();
