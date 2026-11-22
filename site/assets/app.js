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
  const top = document.querySelector('.top');
  document.querySelectorAll('.bottom button').forEach(b => b.addEventListener('click', () => {
    const a = b.dataset.act;
    if (a === 'menu') openDrawer();
    if (a === 'prev' || a === 'next') turn(a === 'next' ? 1 : -1);
    if (a === 'theme') setTheme(themes[(themes.indexOf(root.dataset.theme || 'auto') + 1) % 3]);
    if (a === 'search') { openDrawer(); setTimeout(() => document.querySelector('.side-search input').focus(), 260); }
  }));

  /* ---------- busca: títulos, técnicas, glossário, fontes e texto completo ---------- */
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const data = (window.SEARCH || []).map(d => ({ ...d, n: norm(d.t) }));
  let full = null;
  function fullText() {
    if (full) return full;
    full = [];
    document.querySelectorAll('main > section').forEach(sec => {
      const h2 = sec.querySelector('h2'); let anchor = h2 ? h2.id : sec.id, title = h2 ? h2.textContent.replace(/^\S+\s*/, '') : 'Capa';
      sec.querySelectorAll('h3[id], p, li:not(.slide), td').forEach(el => {
        if (el.matches('h3')) { anchor = el.id; return; }
        if (el.closest('.pager, .meta-bar, .toc, .results, .idx-letters')) return;
        const t = el.textContent.trim();
        if (t.length > 25) full.push({ t, n: norm(t), h: '#' + (el.id || anchor), where: title });
      });
    });
    return full;
  }
  function runSearch(input) {
    const box = input.parentElement.querySelector('.results');
    const v = norm(input.value.trim());
    box.innerHTML = '';
    if (v.length < 2) { box.classList.remove('open'); return; }
    const hits = data.filter(d => d.n.includes(v)).slice(0, 8)
      .map(h => `<li><a href="${h.h}" data-jump>${h.k === 'ref' ? '📚 ' : ''}${esc(h.t)}</a></li>`);
    const seen = new Set();
    const ft = fullText().filter(d => d.n.includes(v) && !seen.has(d.h + d.t.slice(0, 20)) && seen.add(d.h + d.t.slice(0, 20))).slice(0, 10)
      .map(d => { const i = d.n.indexOf(v), a = Math.max(0, i - 40);
        const snip = (a ? '…' : '') + esc(d.t.slice(a, i)) + '<mark>' + esc(d.t.slice(i, i + v.length)) + '</mark>' + esc(d.t.slice(i + v.length, i + v.length + 70)) + '…';
        return `<li><a href="${d.h}" class="ft"><small>${esc(d.where)}</small>${snip}</a></li>`; });
    box.innerHTML = (hits.join('') || '') + (ft.length ? '<li class="res-h">No texto</li>' + ft.join('') : '');
    if (!hits.length && !ft.length) box.innerHTML = '<li class="res-h">Nada encontrado</li>';
    box.classList.add('open');
  }
  document.querySelectorAll('.js-search').forEach(inp => {
    inp.addEventListener('input', () => runSearch(inp));
    inp.parentElement.querySelector('.results').addEventListener('click', e => {
      if (!e.target.closest('a')) return;
      inp.parentElement.querySelector('.results').classList.remove('open'); inp.value = '';
      if (root.classList.contains('lay-mobile')) closeDrawer();
    });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.search')) document.querySelectorAll('.results').forEach(r => r.classList.remove('open')); });

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
  /* ---------- livro: um capítulo por página ---------- */
  const pages = [...document.querySelectorAll('main > section')];
  let current = null;
  root.classList.add('paged');
  function pageOf(hash) {
    const el = hash && hash.length > 1 ? document.getElementById(decodeURIComponent(hash.slice(1))) : null;
    return { el, pg: (el && el.closest('main > section')) || pages[0] };
  }
  function show(hash, smooth) {
    const { el, pg } = pageOf(hash);
    if (pg !== current) {
      pages.forEach(p => { p.hidden = p !== pg; });
      document.querySelectorAll('main .vslot.on').forEach(sl => { sl.innerHTML = ''; sl.classList.remove('on'); });
      current = pg; full = full; markToc();
      document.title = (pg.querySelector('h2') ? pg.querySelector('h2').textContent.replace(/^\S+\s*/, '') + ' · ' : '') + BOOK;
    }
    requestAnimationFrame(() => {
      if (el && el.classList.contains('slide')) {
        const track = el.parentElement;
        track.closest('.carousel').scrollIntoView({ block: 'center' });
        setTimeout(() => track.scrollTo({ left: el.offsetLeft - track.offsetLeft }), 120);
        el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1600);
      } else if (el && el !== pg && !(el.matches('h2') && el.parentElement === pg)) {
        el.scrollIntoView({ block: 'start' });
        if (el.matches('.term, dt, li, p')) { el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1600); }
      } else window.scrollTo(0, 0);
      onScroll();
    });
  }
  const BOOK = document.title;
  function turn(d) {
    const i = pages.indexOf(current) + d;
    if (i < 0 || i >= pages.length) return;
    const h2 = pages[i].querySelector('h2[id]');
    location.hash = h2 ? h2.id : pages[i].id;
  }
  window.addEventListener('hashchange', () => { if (root.classList.contains('lay-mobile')) closeDrawer(); show(location.hash); });
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || e.defaultPrevented) return;
    if (a.getAttribute('href') === location.hash) { e.preventDefault(); show(location.hash); }
  });
  document.addEventListener('keydown', e => {
    if (e.target.closest('input, textarea, .track, dialog') || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'ArrowRight') turn(1);
    if (e.key === 'ArrowLeft') turn(-1);
  });
  function markToc() {
    const id = current && current.querySelector('h2[id]') ? current.querySelector('h2[id]').id : (current ? current.id : '');
    document.querySelectorAll('.side .toc > li > a').forEach(a => {
      const on = a.getAttribute('href') === '#' + id;
      a.classList.toggle('active', on); a.parentElement.classList.toggle('open', on);
    });
  }

  /* ---------- prévias: glossário, técnicas, referências, selos de IA ---------- */
  const pop = document.querySelector('.pop');
  let popFor = null, hideT = null;
  function popContent(a) {
    if (a.dataset.g) { const g = window.GLOSS[a.dataset.g];
      return `<p class="pop-k">Glossário</p><p class="pop-t">${esc(g.t)} <span lang="ja">${g.jp}</span></p><p>${esc(g.d)}</p><a href="#${a.dataset.g}">Ver no glossário ›</a>`; }
    if (a.dataset.img) {
      const ill = !a.getAttribute('href').startsWith('#v-');
      const v = a.dataset.yt ? `<button type="button" class="vbtn" data-yt="${a.dataset.yt}" data-title="${esc(a.dataset.name)}">▶ Assistir aqui: vídeo oficial (Kodokan)</button><div class="vslot"></div>` : '';
      return `<p class="pop-k">${ill ? 'Técnica ilustrada' : 'Vídeo oficial · Kodokan × IJF Academy'}</p><img src="${a.dataset.img}" alt="${esc(a.dataset.name)}"><p class="pop-t">${esc(a.dataset.name)}</p>${v}<a href="${a.getAttribute('href')}">${ill ? 'Ir para a ilustração ›' : 'Ver na videoteca ›'}</a>${ill ? '<p class="pop-ai">🤖 Ilustração gerada por código escrito por IA</p>' : ''}`;
    }
    if (a.dataset.ref) return `<p class="pop-k">Referência (ABNT)</p><div class="pop-ref">${window.REFS[a.dataset.ref]}</div><a href="#${a.dataset.ref}">Ver em Referências ›</a>`;
    if (a.dataset.ai) return `<p class="pop-k">Uso de IA</p><p>${esc(a.dataset.ai)}.</p><a href="#transparencia">Como este livro foi feito ›</a>`;
  }
  function openPop(a) {
    clearTimeout(hideT); popFor = a;
    pop.innerHTML = popContent(a); pop.hidden = false;
    const r = a.getBoundingClientRect(), w = Math.min(340, innerWidth - 24);
    pop.style.width = w + 'px';
    pop.style.left = Math.max(12, Math.min(innerWidth - w - 12, r.left + r.width / 2 - w / 2)) + 'px';
    const below = r.bottom + 10, h = pop.offsetHeight;
    pop.style.top = (below + h < innerHeight - 70 ? below : Math.max(10, r.top - h - 10)) + 'px';
  }
  function closePop() { pop.hidden = true; popFor = null; pop.innerHTML = ''; }
  const POP_SEL = 'a.term, a.tech, a.cite, .ai-chip, .ai-tag';
  const hover = window.matchMedia('(hover: hover)').matches;
  if (hover) {
    document.addEventListener('mouseover', e => { const a = e.target.closest(POP_SEL); if (a && a !== popFor) openPop(a); else if (e.target.closest('.pop')) clearTimeout(hideT); });
    document.addEventListener('mouseout', e => { if (e.target.closest(POP_SEL + ', .pop') && !pop.querySelector('iframe')) hideT = setTimeout(closePop, 250); });
  }
  document.addEventListener('click', e => {
    const a = e.target.closest(POP_SEL);
    if (a && !hover && a !== popFor) { e.preventDefault(); openPop(a); return; }   /* 1º toque: prévia; 2º toque: abre */
    if (e.target.closest('.pop a')) { closePop(); return; }
    if (!e.target.closest('.pop')) closePop();
  }, true);
  window.addEventListener('scroll', () => { if (!hover && popFor && !pop.querySelector('iframe')) closePop(); }, { passive: true });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closePop(); });

  /* ---------- vídeos oficiais tocando dentro da página ---------- */
  function stopAll(except) {
    document.querySelectorAll('.vslot.on').forEach(sl => { if (sl !== except) { sl.innerHTML = ''; sl.classList.remove('on'); } });
    document.querySelectorAll('.vcard.playing').forEach(c => { if (!c.contains(except)) c.classList.remove('playing'); });
  }
  function play(btn) {
    const host = btn.closest('.vcard, figure, .pop, .vplaylist');
    let slot = host.querySelector('.vslot');
    if (!slot) { slot = document.createElement('div'); slot.className = 'vslot'; host.appendChild(slot); }
    const key = btn.dataset.yt || btn.dataset.list;
    if (slot.classList.contains('on') && slot.dataset.yt === key) { stopAll(null); return; }
    stopAll(slot);
    const v = btn.dataset.yt, list = btn.dataset.list, t = esc(btn.dataset.title || 'Vídeo');
    slot.dataset.yt = key; slot.classList.add('on');
    const src = list ? `https://www.youtube-nocookie.com/embed/videoseries?list=${list}&autoplay=1&rel=0&playsinline=1`
                     : `https://www.youtube-nocookie.com/embed/${v}?autoplay=1&rel=0&playsinline=1&modestbranding=1`;
    const ext = list ? `https://www.youtube.com/playlist?list=${list}` : `https://www.youtube.com/watch?v=${v}`;
    slot.innerHTML = `<div class="yt"><iframe src="${src}" title="${t} — vídeo oficial do Kodokan" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>` +
      `<p class="yt-foot">Vídeo: Kodokan × IJF Academy · <a href="${ext}" target="_blank" rel="noopener">abrir no YouTube ↗</a> · <button type="button" class="yt-close">fechar</button></p>`;
    if (host.classList.contains('vcard')) host.classList.add('playing');
    if (host.classList.contains('pop')) { const r = pop.getBoundingClientRect(); if (r.bottom > innerHeight - 10) pop.style.top = Math.max(10, innerHeight - r.height - 80) + 'px'; }
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('.vbtn, .vthumb');
    if (b) { e.preventDefault(); play(b); return; }
    if (e.target.closest('.yt-close')) { stopAll(null); if (e.target.closest('.pop')) closePop(); }
  });

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

  /* ---------- progresso de leitura do capítulo ---------- */
  const bar = document.querySelector('.progress span');
  function onScroll() {
    const h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? h.scrollTop / max * 100 : 100) + '%';
  }
  window.addEventListener('scroll', () => requestAnimationFrame(onScroll), { passive: true });

  applyLayout(); applyTheme(); show(location.hash);
})();
