(function(){
"use strict";
const D = window.PORTAL, T = D.tecnicas, J = D.judo, B = D.bjj;
const $ = (s, r) => (r || document).querySelector(s);
const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const slug = s => String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const A = p => "../app/" + String(p).replace(/^img\/(.+)\.(png|jpe?g)$/i, "img/th/$1.jpg");
const yt = id => "https://i.ytimg.com/vi/" + id + "/mqdefault.jpg";
const L = {}; // referências por id
D.refs.forEach(r => L[r.id] = r);

/* ---------- faixa amarrada (SVG) ---------- */
function shade(h, f) { const n = parseInt(h.slice(1), 16); const c = [n >> 16, n >> 8 & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(v * f)))); return "#" + c.map(v => v.toString(16).padStart(2, "0")).join(""); }
function belt(c, label) {
  const c1 = c[0], c2 = c[1] || null, st = "rgba(0,0,0,.4)";
  const bar = (pts) => c2 ? `<polygon points="${pts}" fill="${c2}" stroke="${st}" stroke-width="1"/>` : "";
  return `<svg viewBox="0 0 200 138" role="img" aria-label="Faixa ${esc(label || "")}">
  <polygon points="92,64 52,126 78,134 110,72" fill="${c1}" stroke="${st}" stroke-width="1.5"/>
  <polygon points="108,64 148,122 124,132 90,72" fill="${c1}" stroke="${st}" stroke-width="1.5"/>
  ${bar("60,112 70,126 78,134 83,124")}${bar("133,109 140,117 124,132 118,121")}
  <path d="M6 30 Q100 52 194 30 L194 58 Q100 80 6 58Z" fill="${c1}" stroke="${st}" stroke-width="1.5"/>
  <path d="M6 44 Q100 66 194 44" fill="none" stroke="${shade(c1, .72)}" stroke-width="1.2" opacity=".7"/>
  <rect x="80" y="38" width="40" height="38" rx="8" fill="${shade(c1, .8)}" stroke="${st}" stroke-width="1.5"/>
  <path d="M86 46 L114 46 M86 57 L114 57 M86 68 L114 68" stroke="${shade(c1, .6)}" stroke-width="1.5" opacity=".6"/>
</svg>`;
}

/* ---------- utilidades de interface ---------- */
const crumbs = list => `<nav class="crumbs" aria-label="Você está em">${list.map((x, i) => i === list.length - 1 ? `<span aria-current="page">${esc(x[0])}</span>` : `<span><a href="${x[1]}">${esc(x[0])}</a></span>`).join("")}</nav>`;
const names = o => `<div class="names">${o.ja ? `<div class="jp" lang="ja">${esc(o.ja)}</div>` : ""}<div class="ro">${esc(o.nome || o.ro || "")}</div>${o.en ? `<div class="tr">${esc(o.en)} <em>(inglês, Kodokan)</em></div>` : ""}${o.pt ? `<div class="tr">${esc(o.pt)} <em>(português, sugestão do app)</em></div>` : ""}</div>`;
function player(id, title) {
  return `<div class="player" data-yt="${esc(id)}"><img src="${yt(id)}" alt="Prévia do vídeo: ${esc(title)}" loading="lazy"><button type="button" data-play="${esc(id)}" aria-label="Assistir aqui: ${esc(title)}"><span>▶</span></button></div>`;
}
const tcard = s => { const t = T[s]; if (!t) return ""; const im = t.imgs[0] ? "../" + t.imgs[0].src : yt(t.yt); return `<a class="tcard" href="#/judo/tecnica/${s}"><div class="th" style="background-image:url('${esc(im)}')"></div><div class="tx"><span class="jp" lang="ja">${esc(t.ja)}</span><b>${esc(t.nome)}</b><small>${esc(t.pt || t.en)}</small></div></a>`; };
const tlink = s => T[s] ? `<a class="pill" href="#/judo/tecnica/${s}"><span class="jp" lang="ja">${esc(T[s].ja)}</span> ${esc(T[s].nome)}</a>` : esc(s);
const refsList = ids => `<ol>${ids.map(i => L[i]).filter(Boolean).map(r => `<li><b>${esc(r.titulo)}</b>, ${esc(r.org)}, ${esc(r.ano)}.${r.url ? ` <a target="_blank" rel="noopener" href="${esc(r.url)}">Abrir a fonte</a>` : ""} <small>(arquivo: ${esc(r.arq)})</small></li>`).join("")}</ol>`;
const kids = x => (x || "").toLowerCase().indexOf("infantil") >= 0;

/* ---------- menu lateral ---------- */
const LIVRO = [["sec-fontes-e-escopo", "01 Fontes e escopo"], ["sec-classificacao-oficial-das-tecnicas-kodokan-ijf-2017", "02 Classificação oficial das técnicas"], ["sec-gokyo-no-waza-os-5-grupos-de-ensino", "03 Gokyo-no-waza"], ["sec-fichas-de-estudo-do-gokyo-40-tecnicas", "04 Fichas de estudo do Gokyo"], ["sec-faixas-idade-minima-e-carencia", "05 Faixas: idade e carência"], ["sec-programa-de-exame-das-faixas-kyu-11o-ao-1o", "06 Programa das faixas kyu"], ["sec-programa-de-exame-dos-dans", "07 Programa dos dans"], ["sec-como-e-pontuado", "08 Como é pontuado"], ["sec-outorga-comissoes-e-bancas", "09 Outorga, comissões e bancas"], ["sec-ijf-validacao-e-programa-de-dan-a-partir-de-2026", "10 IJF: dan a partir de 2026"], ["sec-simulado-da-prova-teorica", "11 Simulado da prova teórica"], ["sec-programa-detalhado-por-faixa-do-11o-kyu-a-faixa-preta", "12 Programa detalhado por faixa"], ["sec-renraku-waza-combinacoes-em-pe-e-no-solo", "13 Renraku-waza"], ["sec-kaeshi-waza-contragolpes", "14 Kaeshi-waza"], ["sec-tecnicas-e-acoes-proibidas-regras-ijf-vigentes", "15 Técnicas proibidas"], ["sec-videoteca-oficial", "16 Videoteca oficial"], ["sec-glossario", "文 Glossário"], ["sec-referencias", "Referências do livro"]];
const TOP_J = [["nage", "Projeções (Nage-waza)"], ["katame", "Solo (Katame-waza)"], ["kaeshi", "Contragolpes (Kaeshi-waza)"], ["renraku", "Combinações (Renraku-waza)"], ["fundamentos", "Fundamentos"], ["proibidas", "Técnicas proibidas"], ["glossario", "Glossário"], ["videoteca", "Videoteca oficial"], ["referencias", "Referências"]];
function side(route) {
  const cur = "#" + route; const a = (h, t) => `<a href="${h}" ${cur === h ? 'aria-current="page"' : ""}>${esc(t)}</a>`;
  const mod = route.split("/")[1];
  const jb = J.faixas.map(f => a("#/judo/faixa/" + f.id, f.titulo)).join("");
  const bg = B.comp.map(g => a("#/jiu-jitsu/t/" + g.id, g.nome)).join("");
  const bb = B.faixas.map(f => a("#/jiu-jitsu/faixa/" + f.id, f.titulo)).join("");
  $("#side").innerHTML = `${a("../", "← Início do portal")}${a("#/judo", "Judô 柔道")}${a("#/jiu-jitsu", "Jiu-Jitsu 柔術")}
  <h2>Judô</h2><details ${mod === "judo" ? "open" : ""}><summary>Programa de exames</summary>${jb}</details><details ${mod === "judo" ? "open" : ""}><summary>Tópicos</summary>${TOP_J.map(t => a("#/judo/t/" + t[0], t[1])).join("")}</details>
  <h2>Jiu-Jitsu</h2><details ${mod === "jiu-jitsu" ? "open" : ""}><summary>Programa de exames</summary>${bb}</details><details ${mod === "jiu-jitsu" ? "open" : ""}><summary>Lista de componentes</summary>${bg}${a("#/jiu-jitsu/proibidas", "Golpes proibidos por faixa")}${a("#/jiu-jitsu/t/referencias", "Referências")}</details>
  <h2>Livro interativo</h2><details><summary>Sumário do livro</summary>${LIVRO.map(c => `<a href="../livro.html#${c[0]}">${esc(c[1])}</a>`).join("")}</details>
  <h2>Mais</h2>${a("../livro.html", "Livro interativo (completo)")}${a("../app/", "App: progresso, ficha e idioma EN")}${a("../judo-tecnicas-e-exames-de-faixa.pdf", "PDF do livro")}`;
}

/* ---------- páginas ---------- */
const VIEWS = [];
const route = (re, fn) => VIEWS.push([re, fn]);

function beltLadder(mod, faixas) {
  const groups = []; let last = "";
  faixas.forEach(f => { const g = kids(f.sub) ? "Infantil" : /Dan|Kôdansha|Graus|Vermelha|mestre/i.test(f.sub + f.titulo) && mod === "judo" || /Graus|mestre/i.test(f.titulo) ? "Graus superiores" : "Faixas"; if (g !== last) { groups.push(`<span class="grouplbl">${g}</span>`); last = g; }
    groups.push(`<a class="belt-card" style="--a:${f.cores.para[1] || f.cores.para[0]}" href="#/${mod}/faixa/${f.id}">${belt(f.cores.para, f.titulo)}<b>${esc(f.titulo)}</b><small>${esc(f.sub || "Exame de faixa")}</small></a>`); });
  return `<div class="railrow"><button class="rnav p" aria-label="Ver faixas anteriores" hidden>&#8249;</button><div class="belts" id="belts">${groups.join("")}</div><button class="rnav n" aria-label="Ver mais faixas" hidden>&#8250;</button></div>`;
}
function wireRail() {
  const el = $("#belts"); if (!el) return; const p = $(".rnav.p"), n = $(".rnav.n");
  const upd = () => { const max = el.scrollWidth - el.clientWidth - 2; p.hidden = el.scrollLeft <= 2; n.hidden = el.scrollLeft >= max || max <= 0; };
  p.onclick = () => el.scrollBy({ left: -Math.max(240, el.clientWidth * .8), behavior: "smooth" }); n.onclick = () => el.scrollBy({ left: Math.max(240, el.clientWidth * .8), behavior: "smooth" });
  el.addEventListener("scroll", upd, { passive: true }); upd(); setTimeout(upd, 300);
}

// ---- Judô: hub ----
route(/^\/judo$/, () => ({ crumbs: [["Início", "../"], ["Judô", "#/judo"]], html: `
<div class="hero" style="--a:#2f64c8"><h1>Judô <span lang="ja">柔道</span></h1><p class="lead">Escolha o exame da sua faixa ou explore os tópicos principais. Cada página leva mais fundo, até a técnica, com nomes em japonês, inglês e português, ilustrações e vídeos oficiais.</p></div>
<h2 class="sec">Programa de exames <small style="color:var(--muted)">(clique na faixa)</small></h2>${beltLadder("judo", J.faixas)}
<h2 class="sec">Tópicos principais</h2>
<div class="cards">
 <a class="card" href="#/judo/t/nage"><div class="ic" lang="ja">投技</div><h3>Projeções (Nage-waza)</h3><p>68 técnicas do Kodokan em cinco grupos, com vídeo oficial.</p><span class="n">${J.grupos.filter(g => g.tipo === "nage").reduce((a, g) => a + g.itens.length, 0)} técnicas</span></a>
 <a class="card" href="#/judo/t/katame"><div class="ic" lang="ja">固技</div><h3>Solo (Katame-waza)</h3><p>Imobilizações, estrangulamentos e chaves de braço.</p><span class="n">${J.grupos.filter(g => g.tipo !== "nage").reduce((a, g) => a + g.itens.length, 0)} técnicas</span></a>
 <a class="card" href="#/judo/t/kaeshi"><div class="ic" lang="ja">返技</div><h3>Contragolpes (Kaeshi-waza)</h3><p>A que técnica cada contragolpe responde.</p><span class="n">${D.kaeshi.length} contragolpes</span></a>
 <a class="card" href="#/judo/t/renraku"><div class="ic" lang="ja">連絡技</div><h3>Combinações (Renraku-waza)</h3><p>Em pé e do pé ao solo, com ilustração.</p><span class="n">${D.renraku.length} combinações</span></a>
 <a class="card" href="#/judo/t/fundamentos"><div class="ic" lang="ja">礼 受身</div><h3>Fundamentos</h3><p>Saudação, quedas (ukemi), postura, pegada e deslocamento.</p></a>
 <a class="card" href="#/judo/t/proibidas"><div class="ic">⛔</div><h3>Técnicas proibidas</h3><p>Hansoku-make direto e principais shidos (regras IJF).</p></a>
 <a class="card" href="#/judo/t/glossario"><div class="ic" lang="ja">文</div><h3>Glossário</h3><p>Termos em japonês com kanji.</p><span class="n">${J.glossario.length} termos</span></a>
 <a class="card" href="#/judo/t/videoteca"><div class="ic">▶</div><h3>Videoteca oficial</h3><p>Kodokan × IJF Academy: toca aqui, sem sair da página.</p></a>
 <a class="card" href="#/judo/t/referencias"><div class="ic">📚</div><h3>Referências</h3><p>Fontes do app e referências do livro.</p></a>
 <a class="card" href="../livro.html"><div class="ic">📖</div><h3>Livro interativo</h3><p>Texto completo, simulado e busca.</p></a>
</div>`, init: wireRail }));

// ---- Judô: faixa ----
const jf = id => J.faixas.find(f => f.id === id);
function acumulado(f, campo) { const i = J.faixas.indexOf(f); const set = []; for (let k = 0; k <= i; k++) (J.faixas[k][campo] || []).forEach(s => { if (set.indexOf(s) < 0) set.push(s) }); return set; }
route(/^\/judo\/faixa\/(\w+)$/, m => {
  const f = jf(m[1]); if (!f) return null; const a = f.cores.para[1] || f.cores.para[0];
  const tecCats = f.cats.filter(c => c.grupo === "tec"), fundCats = f.cats.filter(c => c.grupo === "fund"), naoCats = f.cats.filter(c => c.grupo === "nao");
  const card = (h, t, p, n, ic) => `<a class="card" href="#/judo/faixa/${f.id}/${h}"><div class="ic">${ic || ""}</div><h3>${t}</h3><p>${p}</p>${n ? `<span class="n">${n}</span>` : ""}</a>`;
  return { crumbs: [["Início", "../"], ["Judô", "#/judo"], [f.titulo, ""]], html: `
<div class="hero" style="--a:${a}"><div class="hero-belt">${belt(f.cores.para, f.titulo)}<div><h1>${esc(f.titulo)}</h1><p class="lead">${esc(f.sub)} · exame de faixa</p><ul class="facts">${f.fatos.map(x => `<li><b>${esc(x[0])}</b>${esc(x[1])}</li>`).join("")}</ul></div></div></div>
${f.nota ? `<p class="lead" style="margin-top:12px">${esc(f.nota)}</p>` : ""}
<h2 class="sec">O que é cobrado neste exame</h2><div class="cards">
 ${f.nage && f.nage.length ? card("nage", "Projeções (Nage-waza)", "Técnicas deste exame e as acumuladas das faixas anteriores.", f.nage.length + " nova(s) · " + acumulado(f, "nage").length + " no total", "投技") : ""}
 ${f.katame && f.katame.length ? card("katame", "Solo (Katame-waza)", "Imobilizações, estrangulamentos e chaves.", f.katame.length + " nova(s) · " + acumulado(f, "katame").length + " no total", "固技") : ""}
 ${f.renraku !== undefined ? card("combos", "Combinações e contragolpes", "Renraku-waza e kaeshi-waza exigidos.", "", "連絡技") : ""}
 ${tecCats.map(c => card("c-" + c.id, esc(c.nome), "Texto do regulamento da CBJ.", c.itens.length + " item(ns)", "")).join("")}
</div>
<h2 class="sec">Além das técnicas</h2><div class="cards">
 ${card("fund", "Fundamentos", "Saudações, quedas, postura e pegada.", "", "礼")}
 ${card("nao", "O que não se cobra em competições", "Kata, vocabulário, história, teoria e ensino.", "", "形")}
 ${card("proib", "Técnicas proibidas", "Regras IJF de hansoku-make e shido.", "", "⛔")}
 ${card("refs", "Referências bibliográficas", "Fontes deste exame.", "", "📚")}
</div>
<p class="vnote">Programa cumulativo: o conteúdo da graduação anterior também é exigido. Técnicas específicas seguem a Comissão Estadual de Graduação.</p>` };
});
route(/^\/judo\/faixa\/(\w+)\/([\w-]+)$/, m => {
  const f = jf(m[1]); if (!f) return null; const t = m[2]; const base = [["Início", "../"], ["Judô", "#/judo"], [f.titulo, "#/judo/faixa/" + f.id]];
  const items = c => c.itens.map(it => `<div class="item"><p>${esc(it.t)}</p>${it.tm && it.tm.length ? `<div class="chips">${it.tm.map(x => { const s = slug(x.rom); const lk = T[s] ? `href="#/judo/tecnica/${s}"` : ""; return `<${lk ? "a" : "span"} class="chip" ${lk}><span class="jp" lang="ja">${esc(x.ja)}</span> ${esc(x.rom)} · ${esc(x.pt || x.en)}</${lk ? "a" : "span"}>`; }).join("")}</div>` : ""}</div>`).join("");
  const title = (tt, desc) => `<h1>${tt}</h1><p class="lead">${desc || ""}</p>`;
  const a = f.cores.para[1] || f.cores.para[0];
  let body = "", name = "";
  if (t === "nage" || t === "katame") {
    name = t === "nage" ? "Projeções (Nage-waza)" : "Solo (Katame-waza)"; const novas = f[t] || [], acum = acumulado(f, t).filter(s => novas.indexOf(s) < 0);
    body = `${title(name, "Toque em uma técnica para ver o nome em japonês, a descrição, as ilustrações, o vídeo e as técnicas relacionadas.")}<h2 class="sec">Novas neste exame</h2><div class="tcards">${novas.map(tcard).join("")}</div>${acum.length ? `<h2 class="sec">Acumuladas das faixas anteriores</h2><div class="tcards">${acum.map(tcard).join("")}</div>` : ""}<p class="vnote">Lista do livro (quantitativos da CBJ preenchidos em ordem do Gokyo e do Kodokan). A Comissão Estadual define quais técnicas valem.</p>`;
  } else if (t === "combos") {
    name = "Combinações e contragolpes"; const rs = f.renrakuSlugs || [], ks = f.kaeshiSlugs || [];
    const comb = D.renraku.map((c, i) => [c, i]).filter(x => x[0].cadeia.some(s => acumulado(f, "nage").concat(acumulado(f, "katame")).indexOf(s) >= 0));
    body = `${title(name)}<div class="box"><h3>Renraku-waza (combinações)</h3><p>${esc(f.renraku || "—")}</p>${rs.map(tlink).join(" ")}</div><div class="box"><h3>Kaeshi-waza (contragolpes)</h3><p>${esc(f.kaeshi || "—")}</p>${ks.map(tlink).join(" ")}</div>
    <h2 class="sec">Exemplos ilustrados com técnicas já vistas</h2><div class="cards">${comb.length ? comb.map(x => `<a class="card" href="#/judo/combo/${x[1]}"><h3>${x[0].cadeia.map(s => esc(T[s].nome)).join(" → ")}</h3><p>${esc(x[0].tipo)}</p></a>`).join("") : "<p class='lead'>Nenhuma combinação ilustrada usa só as técnicas desta faixa.</p>"}</div>`;
  } else if (t.indexOf("c-") === 0) {
    const c = f.cats.find(x => "c-" + x.id === t); if (!c) return null; name = c.nome;
    body = `${title(c.nome, c.ja ? `<span lang="ja">${esc(c.ja)}</span> · ${esc(c.pt || c.en)}` : "")}${items(c)}<p class="vnote">Texto extraído do regulamento da CBJ (2023). Confira sempre o documento oficial.</p>`;
  } else if (t === "fund") {
    name = "Fundamentos";
    body = `${title(name, "Fundamentos (kihon) cobrados neste exame.")}${f.kihon ? `<div class="box"><h3>Fundamentos desta faixa (livro)</h3><p>${esc(f.kihon)}</p></div>` : ""}${f.cats.filter(c => c.grupo === "fund").map(c => `<h2 class="sec">${esc(c.nome)}</h2>${items(c)}`).join("")}
    <div class="box"><h3>Termos de apoio</h3>${["Rei", "Ukemi", "Shizen-hontai", "Kumi-kata", "Tai-sabaki", "Shintai"].map(x => { const g = J.glossario.find(y => y.termo === x); return g ? `<a class="pill" href="#/judo/t/glossario"><span class="jp" lang="ja">${esc(g.kanji)}</span> ${esc(g.termo)}</a>` : ""; }).join("")}<p style="margin-top:8px"><a href="#/judo/t/fundamentos">Ver a página de fundamentos, com vídeos</a></p></div>`;
  } else if (t === "nao") {
    name = "O que não se cobra em competições";
    body = `${title(name, "Conteúdo de exame que não aparece em uma luta de competição: kata, vocabulário, história, teoria, arbitragem e ensino. Classificação do app, feita a partir das categorias do regulamento.")}${f.kata && f.kata !== "—" ? `<div class="box"><h3>Kata</h3><p>${esc(f.kata)}</p></div>` : ""}${f.teoria ? `<div class="box"><h3>Teoria e regras que o aluno deve conhecer</h3><p>${esc(f.teoria)}</p></div>` : ""}${f.cats.filter(c => c.grupo === "nao").map(c => `<h2 class="sec">${esc(c.nome)}</h2>${items(c)}`).join("")}
    ${f.quant ? `<div class="box"><h3>Quantidades por área (CBJ)</h3><div class="tw"><table>${Object.keys(f.quant).map(k => `<tr><th>${esc(k)}</th><td>${esc(f.quant[k])}</td></tr>`).join("")}</table></div></div>` : ""}`;
  } else if (t === "proib") {
    name = "Técnicas proibidas";
    body = `${title(name)}<div class="warn"><b>INFORMAÇÃO AUSENTE por faixa.</b> As fontes do app (CBJ e IJF) não listam proibições diferentes para cada faixa: as regras de competição da IJF abaixo valem para todas. Restrições por idade nas competições variam por federação; confira a sua.</div>${proibHtml()}`;
  } else if (t === "refs") {
    name = "Referências bibliográficas";
    body = `${title(name, "Fontes usadas neste exame.")}<div class="box"><h3>Fontes do app</h3>${refsList(["cbj2023", "kodokan", "fjerj", "judocanada", "jq_aide", "ijf_tech", "bja_guide"])}</div><div class="box"><h3>Referências do livro (ABNT)</h3><ol>${J.refsLivro.map(r => `<li>${esc(r)}</li>`).join("")}</ol></div>`;
  } else return null;
  return { crumbs: base.concat([[name, ""]]), html: `<div style="--a:${a}">${body}</div>` };
});
function proibHtml() {
  const P = J.proibidas;
  return `<h2 class="sec">Hansoku-make direto</h2><ul>${P.hansoku.map(x => `<li>${esc(x)}</li>`).join("")}</ul><h2 class="sec">Principais shidos</h2><ul>${P.shido.map(x => `<li>${esc(x)}</li>`).join("")}</ul>${P.imgs.length ? `<h2 class="sec">Ilustrações</h2><div class="imgs" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr))">${P.imgs.map(s => `<figure><img loading="lazy" src="../${esc(s)}" alt="Ação proibida"><figcaption>Ilustração produzida por código (IA)</figcaption></figure>`).join("")}</div>` : ""}<p class="vnote">Fonte: regras IJF vigentes, conforme o livro (capítulo 15).</p>`;
}

// ---- Judô: técnica ----
route(/^\/judo\/tecnica\/([\w-]+)$/, m => {
  const t = T[m[1]]; if (!t) return null; const f = t.ficha;
  const where = t.faixas.map(id => jf(id)).filter(Boolean);
  const kae = t.kaeshi, resp = t.respondeA;
  return { crumbs: [["Início", "../"], ["Judô", "#/judo"], [t.tipo === "nage" ? "Projeções" : "Solo", "#/judo/t/" + (t.tipo === "nage" ? "nage" : "katame")], [t.nome, ""]], html: `
<div class="hero" style="--a:${t.tipo === "nage" ? "#2f64c8" : "#7a3fa3"}"><h1 style="font-size:clamp(1.6rem,3.6vw,2.4rem)">${esc(t.grupo)}</h1>${names(t)}<ul class="facts"><li><b>Tipo</b>${t.tipo === "nage" ? "Nage-waza (projeção)" : "Katame-waza (solo)"}</li>${f ? `<li><b>Classe</b>${esc(f.classe)}</li><li><b>Grupo / faixa (Gokyo)</b>${esc(f.faixa)}</li>` : ""}${where.length ? `<li><b>Entra no exame</b>${where.map(w => esc(w.titulo)).join("; ")}</li>` : ""}</ul></div>
<div class="two" style="margin-top:18px"><div>
 <div class="box"><h3>Descrição</h3>${f ? `<p><b>Kuzushi principal (desequilíbrio):</b> ${esc(f.kuzushi)}.</p><p><b>Ação-chave:</b> ${esc(f.acao)}.</p><p class="vnote">Síntese didática do livro, para tori destro (pegada direita); não substitui o professor.</p>` : `<p>${esc(t.nome)}${t.en ? " (" + esc(t.en) + ")" : ""} é uma técnica do grupo ${esc(t.grupo)} da classificação do Kodokan/IJF. O livro não traz ficha de estudo para esta técnica: use o vídeo oficial e a página da IJF.</p>`}</div>
 ${t.imgs.length ? `<div class="imgs">${t.imgs.map(i => `<figure><img loading="lazy" src="../${esc(i.src)}" alt="${esc(t.nome)}: ${esc(i.cap)}" data-zoom><figcaption>${esc(i.cap)} · ilustração produzida por código (IA)</figcaption></figure>`).join("")}</div>` : ""}
</div><div>
 <div class="box"><h3>Vídeo oficial</h3>${player(t.yt, t.nome)}<p class="vnote">Kodokan × IJF Academy, “100 Techniques”. Toca aqui, sem sair da página (modo de privacidade do YouTube).</p><p><a class="pill" target="_blank" rel="noopener" href="${esc(t.ijf)}">Página da IJF</a><a class="pill" href="../livro.html#t-${t.id}">No livro</a></p></div>
</div></div>
<h2 class="sec">Técnicas e textos relacionados</h2>
${kae.length ? `<div class="box"><h3>Kaeshi-waza: contragolpes a ${esc(t.nome)}</h3><ul class="rel">${kae.map(k => `<li><div>${tlink(k.id)}<small>${esc(k.acao)}</small></div></li>`).join("")}</ul></div>` : ""}
${resp.length ? `<div class="box"><h3>Este contragolpe responde a</h3>${resp.map(tlink).join(" ")}</div>` : ""}
${t.combos.length ? `<div class="box"><h3>Renraku-waza: combinações com ${esc(t.nome)}</h3><div class="cards">${t.combos.map(i => { const c = D.renraku[i]; return `<a class="card" href="#/judo/combo/${i}"><h3>${c.cadeia.map(s => esc(T[s].nome)).join(" → ")}</h3><p>${esc(c.tipo)}: ${esc(c.logica)}</p></a>`; }).join("")}</div></div>` : ""}
${t.katame.length ? `<div class="box"><h3>Katame-waza associados</h3>${t.katame.map(tlink).join(" ")}<p class="vnote">Técnicas de solo que aparecem encadeadas com esta nas combinações do livro.</p></div>` : ""}
${!kae.length && !resp.length && !t.combos.length && !t.katame.length ? `<p class="lead">O livro não traz contragolpes nem combinações específicas para esta técnica. Veja a lista completa em <a href="#/judo/t/kaeshi">Kaeshi-waza</a> e <a href="#/judo/t/renraku">Renraku-waza</a>.</p>` : ""}` };
});
route(/^\/judo\/combo\/(\d+)$/, m => {
  const c = D.renraku[+m[1]]; if (!c) return null; const id = c.cadeia.find(s => T[s] && T[s].tipo === "nage") || c.cadeia[0];
  return { crumbs: [["Início", "../"], ["Judô", "#/judo"], ["Combinações", "#/judo/t/renraku"], [c.cadeia.map(s => T[s].nome).join(" → "), ""]], html: `
<div class="hero" style="--a:#2f64c8"><h1>${c.cadeia.map(s => esc(T[s].nome)).join(" → ")}</h1><p class="lead"><span lang="ja">連絡技</span> Renraku-waza · ${esc(c.tipo)}: ${esc(c.logica)}</p></div>
${c.img ? `<div class="imgs" style="margin-top:14px"><figure><img src="../${esc(c.img)}" alt="Combinação" data-zoom><figcaption>Ilustração produzida por código (IA)</figcaption></figure></div>` : ""}
<h2 class="sec">As técnicas da combinação</h2><div class="tcards">${c.cadeia.map(tcard).join("")}</div>
<h2 class="sec">Vídeos</h2><div class="cards">${c.cadeia.map(s => `<div class="box"><h3>${esc(T[s].nome)}</h3>${player(T[s].yt, T[s].nome)}</div>`).join("")}</div>` };
});

// ---- Judô: tópicos ----
function vgrid(list) { return `<div class="cards">${list.map(v => `<div class="box"><h3>${esc(v.t)}</h3><p lang="ja" style="font-family:var(--jp)">${esc(v.ja || "")}</p>${player(v.yt, v.t)}</div>`).join("")}</div>`; }
route(/^\/judo\/t\/([\w-]+)$/, m => {
  const k = m[1]; const base = [["Início", "../"], ["Judô", "#/judo"]]; const nm = (TOP_J.find(x => x[0] === k) || [k, k])[1];
  let body = "";
  if (k === "nage" || k === "katame") body = `<h1>${nm}</h1><p class="lead">${k === "nage" ? "Classificação oficial do Kodokan/IJF (2017): 68 projeções." : "Classificação oficial do Kodokan/IJF: 32 técnicas de controle no solo."}</p>` + J.grupos.filter(g => (k === "nage") === (g.tipo === "nage")).map(g => `<h2 class="sec">${esc(g.nome)}</h2><div class="tcards">${g.itens.map(tcard).join("")}</div>`).join("");
  else if (k === "kaeshi") body = `<h1>Contragolpes <span lang="ja">返技</span> Kaeshi-waza</h1><p class="lead">A resposta de tori a um ataque de uke, aproveitando o desequilíbrio criado pelo próprio ataque.</p><div class="tw"><table><tr><th>Contragolpe</th><th>Grupo</th><th>Responde a</th><th>Ação de tori</th></tr>${D.kaeshi.map(x => `<tr><td>${tlink(x.contra)}</td><td>${esc(x.grupo)}</td><td>${x.responde.map(tlink).join(" ")}</td><td>${esc(x.acao)}</td></tr>`).join("")}</table></div>`;
  else if (k === "renraku") body = `<h1>Combinações <span lang="ja">連絡技</span> Renraku-waza</h1><p class="lead">Encadeamento de duas ou mais técnicas: o primeiro ataque provoca uma reação, e o segundo a aproveita. Nenhuma instituição publica uma lista fechada; estas são as clássicas do livro.</p><div class="cards">${D.renraku.map((c, i) => `<a class="card" href="#/judo/combo/${i}"><h3>${c.cadeia.map(s => esc(T[s].nome)).join(" → ")}</h3><p>${esc(c.tipo)}</p></a>`).join("")}</div>`;
  else if (k === "fundamentos") body = `<h1>Fundamentos <span lang="ja">礼 · 受身 · 基本</span></h1><p class="lead">Saudação (rei), quedas (ukemi), postura (shizen-hontai), pegada (kumi-kata) e deslocamento (tai-sabaki, shintai).</p><div class="box"><h3>Termos</h3>${["Rei", "Seiza", "Ukemi", "Shizen-hontai", "Kumi-kata", "Tai-sabaki", "Shintai", "Kuzushi", "Tsukuri", "Kake"].map(x => { const g = J.glossario.find(y => y.termo === x); return g ? `<div class="item"><p><b lang="ja">${esc(g.kanji)}</b> ${esc(g.termo)}</p><p>${esc(g.def)}</p></div>` : ""; }).join("")}</div><h2 class="sec">Vídeos</h2>${vgrid(J.extras.filter(g => /Fundamentos|Combinações/.test(g.grupo)).flatMap(g => g.itens))}<p class="vnote">Mais material: <a href="#/jiu-jitsu/t/fund">rolamentos, ukemi e tai-sabaki com sequências de fotos</a> (Judo Canada, FJERJ).</p>`;
  else if (k === "proibidas") body = `<h1>Técnicas proibidas</h1>${proibHtml()}`;
  else if (k === "glossario") body = `<h1>Glossário <span lang="ja">文</span></h1><div class="tw"><table><tr><th>Kanji</th><th>Termo</th><th>Definição</th></tr>${J.glossario.map(g => `<tr><td lang="ja" style="font-family:var(--jp);font-size:1.2rem">${esc(g.kanji)}</td><td><b>${esc(g.termo)}</b></td><td>${esc(g.def)}</td></tr>`).join("")}</table></div><p class="vnote">Definições redigidas com IA a partir das fontes do livro.</p>`;
  else if (k === "videoteca") body = `<h1>Videoteca oficial</h1><p class="lead">Série “100 Techniques” do Kodokan com a IJF Academy e vídeos de fundamentos. Toque em ▶ para assistir aqui.</p>${J.grupos.map(g => `<h2 class="sec">${esc(g.nome)}</h2>${vgrid(g.itens.map(s => ({ t: T[s].nome, ja: T[s].ja, yt: T[s].yt })))}`).join("")}${J.extras.map(g => `<h2 class="sec">${esc(g.grupo)}</h2>${vgrid(g.itens)}`).join("")}`;
  else if (k === "referencias") body = `<h1>Referências</h1><div class="box"><h3>Fontes do app</h3>${refsList(D.refs.map(r => r.id))}</div><div class="box"><h3>Referências do livro (ABNT)</h3><ol>${J.refsLivro.map(r => `<li>${esc(r)}</li>`).join("")}</ol></div>`;
  else return null;
  return { crumbs: base.concat([[nm, ""]]), html: body };
});

// ---- Jiu-Jitsu: hub ----
const bf = id => B.faixas.find(f => f.id === id);
const bgrp = id => B.comp.find(g => g.id === id);
const ICON_B = { fund: "基本", quedas: "投", posicoes: "固", guardas: "守", raspagens: "返", saidas: "逃", transicoes: "連", braco: "腕", perna: "足", punho: "手", estrang: "絞", defesa: "護", faltas: "⛔", lbjj: "📘" };
route(/^\/jiu-jitsu$/, () => ({ crumbs: [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"]], html: `
<div class="hero" style="--a:#7a3fa3"><h1>Jiu-Jitsu <span lang="ja">柔術</span></h1><p class="lead">Escolha o exame da sua faixa ou explore a lista de componentes. Cada página leva mais fundo, até a técnica, com nomes em japonês, inglês e português, fotos e vídeos oficiais.</p></div>
<h2 class="sec">Programa de exames <small style="color:var(--muted)">(clique na faixa)</small></h2>${beltLadder("jiu-jitsu", B.faixas)}
<h2 class="sec">Tópicos principais</h2><div class="cards">${B.comp.map(g => `<a class="card" href="#/jiu-jitsu/t/${g.id}"><div class="ic" lang="ja">${ICON_B[g.id] || ""}</div><h3>${esc(g.nome)}</h3><p>${esc(g.desc)}</p><span class="n">${(g.subs && g.subs.length ? g.subs.reduce((a, s) => a + s.itens.length + s.blocos.length, 0) : g.itens.length) || ""} ${g.subs && g.subs.length ? "tópicos" : "itens"}</span></a>`).join("")}
<a class="card" href="#/jiu-jitsu/proibidas"><div class="ic">⛔</div><h3>Golpes proibidos por idade e faixa</h3><p>Tabela da IBJJF/CBJJ, p. 29.</p></a><a class="card" href="#/jiu-jitsu/t/referencias"><div class="ic">📚</div><h3>Referências</h3><p>Fontes do app.</p></a><a class="card" href="../app/#bjj/b01"><div class="ic">📝</div><h3>Ficha de exame e progresso</h3><p>Simulador editável (app).</p></a></div>`, init: wireRail }));

function itemsList(its, bel) { return `<div class="tcards" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">${its.map(i => `<a class="tcard" href="#/jiu-jitsu/item/${slug(i.t)}"><div class="tx"><span class="jp" lang="ja">${esc((i.nm && i.nm.ja || "").split(" · ")[0])}</span><b>${esc(i.nm && i.nm.pt || i.t)}</b><small>${esc(i.t)}</small></div></a>`).join("")}</div>`; }
function matrizCols(f) {
  const alvo = (f.titulo.split("→")[1] || f.titulo).trim().toLowerCase(); const cols = [];
  if (kids(f.sub)) return { cols: [0, 1], nota: "Faixas infantis: valem as colunas de 4 a 12 anos e de 13 a 15 anos." };
  if (/azul|roxa/.test(alvo)) return { cols: [2, 3], nota: "Para " + alvo + ": adultos usam a coluna “azul e roxa”; atletas de 16 e 17 anos seguem a coluna de 16 e 17 anos." };
  if (/marrom|preta/.test(alvo)) return { cols: [4, 5], nota: "Para " + alvo + ": coluna “marrom e preta” (com kimono) e “Sem Kimono”." };
  return { cols: [2, 3, 4, 5], nota: "Faixa branca (adulto) usa a coluna 3; as demais colunas aparecem para comparação." };
}
function matrizHtml(f) {
  const M = B.matriz, mc = f ? matrizCols(f) : { cols: [0, 1, 2, 3, 4, 5], nota: "" };
  const lista = M.golpes.filter(g => g[1].some(c => mc.cols.indexOf(c) >= 0));
  return `${f ? `<div class="box"><h3>Proibidos para esta faixa</h3><p>${esc(mc.nota)}</p><ol>${lista.map(g => `<li>${esc(g[0])}</li>`).join("")}</ol></div>` : ""}${f && /branca/i.test(f.titulo) ? `<div class="warn">${esc(M.extra_branca)}</div>` : ""}
  <div class="box"><h3>Tabela completa: golpes proibidos por idade e faixa</h3><div class="tw"><table><tr><th>#</th><th>Golpe</th>${M.colunas.map(c => `<th style="min-width:90px">${esc(c)}</th>`).join("")}</tr>${M.golpes.map((g, i) => `<tr><td>${i + 1}</td><td>${esc(g[0])}</td>${M.colunas.map((_, c) => `<td>${g[1].indexOf(c) >= 0 ? '<span class="dot" role="img" aria-label="proibido"></span>' : ""}</td>`).join("")}</tr>`).join("")}</table></div><p class="vnote">${esc(M.fonte)} Transcrição do app: confira a tabela original no livro de regras.</p></div>`;
}
route(/^\/jiu-jitsu\/proibidas$/, () => ({ crumbs: [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"], ["Golpes proibidos", ""]], html: `<h1>Golpes proibidos por idade e faixa</h1><p class="lead">Tabela do livro de regras IBJJF/CBJJ (2024).</p>${matrizHtml(null)}` }));

// ---- Jiu-Jitsu: faixa ----
route(/^\/jiu-jitsu\/faixa\/(\w+)$/, m => {
  const f = bf(m[1]); if (!f) return null; const a = f.cores.para[1] || f.cores.para[0];
  const card = (h, t, p, n, ic) => `<a class="card" href="#/jiu-jitsu/faixa/${f.id}/${h}"><div class="ic">${ic || ""}</div><h3>${t}</h3><p>${p}</p>${n ? `<span class="n">${n}</span>` : ""}</a>`;
  const sec = f.secoes.filter(s => !/defesa pessoal|self defense|basic/i.test(s.cat)), fund = f.secoes.filter(s => /basic/i.test(s.cat)), nao = f.secoes.filter(s => /defesa pessoal|self defense/i.test(s.cat));
  return { crumbs: [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"], [f.titulo, ""]], html: `
<div class="hero" style="--a:${a}"><div class="hero-belt">${belt(f.cores.para, f.titulo)}<div><h1>${esc(f.titulo)}</h1><p class="lead">${esc(f.sub || "Exame de faixa")}</p><ul class="facts">${f.fatos.map(x => `<li><b>${esc(x[0])}</b>${esc(x[1])}</li>`).join("")}</ul></div></div></div>
${f.nota ? `<div class="warn">${esc(f.nota)}</div>` : ""}
<h2 class="sec">O que é cobrado neste exame (programa técnico da JJIF)</h2><div class="cards">${sec.map(s => card("s-" + slug(s.cat), esc(s.pt || s.cat), esc(s.cat), s.itens.length + " técnicas", "")).join("") || "<p class='lead'>A JJIF não define exame técnico para esta faixa; consulte as regras da sua federação.</p>"}${f.ficha ? card("ficha", "Ficha de exame (JJIF)", "Critérios de avaliação e simulador editável.", "", "📝") : ""}</div>
<h2 class="sec">Além das técnicas</h2><div class="cards">${card("fund", "Fundamentos", "Técnicas básicas, quedas (ukemi), rolamentos e tai-sabaki.", "", "基本")}${card("nao", "O que não se cobra em competições", "Defesa pessoal e critérios de avaliação do exame.", "", "護")}${card("proib", "Técnicas proibidas para esta faixa", "Tabela da IBJJF/CBJJ por idade e faixa.", "", "⛔")}${card("refs", "Referências bibliográficas", "Fontes deste exame.", "", "📚")}</div>
<p class="vnote">${esc(f.intro || "")}</p>` };
});
route(/^\/jiu-jitsu\/faixa\/(\w+)\/([\w-]+)$/, m => {
  const f = bf(m[1]); if (!f) return null; const t = m[2]; const base = [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"], [f.titulo, "#/jiu-jitsu/faixa/" + f.id]]; const a = f.cores.para[1] || f.cores.para[0];
  let body = "", name = "";
  if (t.indexOf("s-") === 0) { const s = f.secoes.find(x => "s-" + slug(x.cat) === t); if (!s) return null; name = s.pt || s.cat; body = `<h1>${esc(name)}</h1><p class="lead">${esc(s.cat)} · programa técnico da JJIF para ${esc(f.titulo)}</p>${itemsList(s.itens)}${s.imgs.length ? `<h2 class="sec">Coluna do programa JJIF (documento oficial)</h2><div class="imgs">${s.imgs.map(i => `<figure><img loading="lazy" src="${A(i)}" alt="Coluna ${esc(s.cat)} do programa JJIF" data-zoom><figcaption>JJIF Graduation System v11 (miniatura)</figcaption></figure>`).join("")}</div>` : ""}`; }
  else if (t === "ficha") { name = "Ficha de exame (JJIF)"; const k = f.ficha; body = `<h1>${name}</h1><div class="box"><h3>Critérios de avaliação</h3><p>${esc(k.criterios)}</p></div><div class="box"><h3>Opções do examinador</h3><p>${esc(k.opcoes)}</p></div><div class="box"><h3>Seções da ficha</h3><p>${esc(k.secoes)}</p></div><div class="box"><h3>Carga mínima sugerida</h3><p>${esc(k.carga)}</p></div><div class="imgs"><figure><img src="${A(k.img)}" alt="Ficha de exame da JJIF" data-zoom><figcaption>JJIF Graduation System v11, seção Belt Exam</figcaption></figure></div><p><a class="pill" href="../app/#bjj/${f.id}">Abrir o simulador editável (app)</a></p>`; }
  else if (t === "fund") { name = "Fundamentos"; const s = f.secoes.filter(x => /basic/i.test(x.cat)); const g = bgrp("fund"); body = `<h1>${name}</h1>${s.map(x => `<h2 class="sec">${esc(x.pt || x.cat)}</h2>${itemsList(x.itens)}`).join("")}<h2 class="sec">Tai-sabaki, rolamentos e ukemi</h2><p class="lead">${esc(g.desc)}</p><div class="cards">${g.subs.map(s => `<a class="card" href="#/jiu-jitsu/t/fund/${s.id}"><h3>${esc(s.nome)}</h3><p>${esc(s.desc)}</p></a>`).join("")}</div>`; }
  else if (t === "nao") { name = "O que não se cobra em competições"; const s = f.secoes.filter(x => /defesa pessoal|self defense/i.test(x.cat)); body = `<h1>${name}</h1><p class="lead">Itens do exame que não existem em uma luta de competição (IBJJF/CBJJ): defesa pessoal e a avaliação do exame. Classificação do app.</p>${s.map(x => `<h2 class="sec">${esc(x.pt || x.cat)}</h2>${itemsList(x.itens)}`).join("") || "<p class='lead'>Esta faixa não tem defesa pessoal no programa da JJIF.</p>"}${f.ficha ? `<div class="box"><h3>Critérios de avaliação</h3><p>${esc(f.ficha.criterios)}</p></div>` : ""}`; }
  else if (t === "proib") { name = "Técnicas proibidas para esta faixa"; body = `<h1>${name}</h1>${matrizHtml(f)}`; }
  else if (t === "refs") { name = "Referências bibliográficas"; body = `<h1>${name}</h1><div class="box">${refsList(["ibjjf_grad", "jjif_grad", "cbjj_rules", "golpes", "jjif_nw", "jjau", "yt", "kodokan", "lbjj", "lbjj_site", "judocanada", "fjerj"])}</div>`; }
  else return null;
  return { crumbs: base.concat([[name, ""]]), html: `<div style="--a:${a}">${body}</div>` };
});

// ---- Jiu-Jitsu: componentes e itens ----
route(/^\/jiu-jitsu\/t\/([\w-]+)$/, m => {
  const k = m[1]; const base = [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"]];
  if (k === "referencias") return { crumbs: base.concat([["Referências", ""]]), html: `<h1>Referências</h1><div class="box">${refsList(D.refs.map(r => r.id))}</div>` };
  const g = bgrp(k); if (!g) return null;
  const vids = (g.videos || []).filter(v => v.url && /v=/.test(v.url)).map(v => ({ id: v.url.split("v=")[1].split("&")[0], rot: v.rot }));
  let body = `<h1>${esc(g.nome)}</h1>${g.nm && (g.nm.ja || g.nm.en) ? `<div class="names"><div class="jp" lang="ja">${esc((g.nm.ja || "").split(" · ")[0])}</div><div class="tr">${esc(g.nm.en || "")} · ${esc(g.nm.pt || "")}</div></div>` : ""}<p class="lead">${esc(g.desc)}</p>`;
  if (g.subs && g.subs.length) body += `<div class="cards">${g.subs.map(s => `<a class="card" href="#/jiu-jitsu/t/${k}/${s.id}"><h3>${esc(s.nome)}</h3><p>${esc(s.desc || "")}</p><span class="n">${s.itens.length ? s.itens.length + " itens" : s.blocos.length + " blocos"}</span></a>`).join("")}</div>`;
  if (g.itens.length) body += `<h2 class="sec">Técnicas da lista</h2>${itemsList(g.itens)}`;
  if (g.regra.length) body += `<h2 class="sec">Explicação na regra</h2>${g.regra.map(r => `<div class="item"><p><b>${esc(r.titulo)}</b></p><p>${esc(r.texto)}</p></div>`).join("")}`;
  if (vids.length) body += `<h2 class="sec">Vídeos oficiais (IBJJF Rules Tutorials)</h2><div class="cards">${vids.map(v => `<div class="box"><h3>${esc(v.rot)}</h3>${player(v.id, v.rot)}</div>`).join("")}</div>`;
  if (g.fotos.length) body += `<h2 class="sec">Fotos</h2><div class="imgs" style="grid-template-columns:repeat(auto-fill,minmax(220px,1fr))">${g.fotos.map(f => `<figure><img loading="lazy" src="${A(f.img)}" alt="${esc(f.cap)}" data-zoom><figcaption>${esc(f.cap)} · ${esc(f.fonte)}</figcaption></figure>`).join("")}</div>`;
  return { crumbs: base.concat([[g.nome, ""]]), html: body };
});
route(/^\/jiu-jitsu\/t\/([\w-]+)\/([\w-]+)$/, m => {
  const g = bgrp(m[1]); if (!g) return null; const s = (g.subs || []).find(x => x.id === m[2]); if (!s) return null;
  const vids = (s.videos || []).filter(v => v.url && /v=/.test(v.url)).map(v => ({ id: v.url.split("v=")[1].split("&")[0], rot: v.rot }));
  return { crumbs: [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"], [g.nome, "#/jiu-jitsu/t/" + g.id], [s.nome, ""]], html: `<h1>${esc(s.nome)}</h1>${s.nm && (s.nm.ja || s.nm.pt) ? `<div class="names"><div class="jp" lang="ja">${esc((s.nm.ja || "").split(" · ")[0])}</div><div class="tr">${esc(s.nm.en || "")} · ${esc(s.nm.pt || "")}</div></div>` : ""}<p class="lead">${esc(s.desc || "")}</p>
${s.itens.length ? `<h2 class="sec">Técnicas</h2>${itemsList(s.itens)}` : ""}
${s.blocos.map(b => `<div class="box"><h3>${esc(b.titulo)}</h3>${b.nm && (b.nm.ja || b.nm.en) ? `<div class="names"><div class="jp" lang="ja">${esc((b.nm.ja || "").split(" · ")[0])}</div><div class="tr">${esc(b.nm.en || "")}${b.nm.pt ? " · " + esc(b.nm.pt) : ""}</div></div>` : ""}${b.texto ? `<p style="white-space:pre-line">${esc(b.texto)}</p>` : ""}${b.fotos.length ? `<div class="imgs" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr))">${b.fotos.map(f => `<figure><img loading="lazy" src="${A(f.img)}" alt="${esc(f.cap)}" data-zoom><figcaption>${esc(f.cap)}</figcaption></figure>`).join("")}</div>` : ""}<p class="vnote">${esc(b.fonte || "")}</p></div>`).join("")}
${vids.length ? `<h2 class="sec">Vídeos</h2><div class="cards">${vids.map(v => `<div class="box"><h3>${esc(v.rot)}</h3>${player(v.id, v.rot)}</div>`).join("")}</div>` : ""}` };
});
route(/^\/jiu-jitsu\/item\/([\w-]+)$/, m => {
  const id = m[1]; let it = null, where = [], grp = null;
  B.faixas.forEach(f => f.secoes.forEach(s => s.itens.forEach(i => { if (slug(i.t) === id) { it = it || i; where.push([f, s]); } })));
  B.comp.forEach(g => { (g.itens || []).concat((g.subs || []).flatMap(s => s.itens)).forEach(i => { if (slug(i.t) === id) { it = it || i; grp = grp || g; } }); });
  if (!it) return null; const nm = it.nm || {}; const ja = (nm.ja || "").split(" · "), rom = (ja[1] || "").split(" ")[0]; const eq = rom && T[slug(rom)] ? slug(rom) : "";
  const vids = grp ? (grp.videos || []).filter(v => v.url && /v=/.test(v.url)).slice(0, 2).map(v => ({ id: v.url.split("v=")[1].split("&")[0], rot: v.rot })) : [];
  return { crumbs: [["Início", "../"], ["Jiu-Jitsu", "#/jiu-jitsu"], [grp ? grp.nome : "Técnica", grp ? "#/jiu-jitsu/t/" + grp.id : ""], [nm.pt || it.t, ""]], html: `
<div class="hero" style="--a:#7a3fa3"><h1 style="font-size:clamp(1.6rem,3.6vw,2.4rem)">${esc(it.t)}</h1>${names({ ja: ja[0], nome: ja[1] || "", en: nm.en && nm.en !== it.t ? nm.en : "", pt: nm.pt })}${nm.sj || nm.sp ? `<p class="lead" style="font-size:.85rem">Fonte do nome japonês: ${esc(nm.sj || "")}${nm.eq ? " (equivalente aproximado no Kodokan)" : ""}. Português: ${esc(nm.sp === "app" ? "sugestão do app, conferir" : nm.sp || "—")}.</p>` : ""}</div>
<div class="box"><h3>Descrição</h3><p>A fonte (programa da JJIF) lista esta técnica pelo nome, sem texto descritivo. Use as fotos e os vídeos do grupo relacionado e peça a demonstração ao seu professor.</p></div>
${where.length ? `<div class="box"><h3>Aparece nos exames</h3>${where.map(w => `<a class="pill" href="#/jiu-jitsu/faixa/${w[0].id}/s-${slug(w[1].cat)}">${esc(w[0].titulo)} · ${esc(w[1].pt || w[1].cat)}</a>`).join("")}</div>` : ""}
${eq ? `<div class="box"><h3>Equivalente no Judô (Kodokan)</h3>${tlink(eq)}<p class="vnote">Equivalente aproximado: confira nas fontes.</p></div>` : ""}
${grp ? `<div class="box"><h3>Grupo relacionado</h3><a class="pill" href="#/jiu-jitsu/t/${grp.id}">${esc(grp.nome)}</a></div>` : ""}
${vids.length ? `<h2 class="sec">Vídeos oficiais do grupo</h2><div class="cards">${vids.map(v => `<div class="box"><h3>${esc(v.rot)}</h3>${player(v.id, v.rot)}</div>`).join("")}</div>` : ""}
<p><a class="pill" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=${encodeURIComponent(it.t + " jiu-jitsu")}">Buscar vídeo no YouTube</a></p>` };
});

/* ---------- roteador ---------- */
function render() {
  const r = (location.hash || "#/judo").slice(1) || "/judo"; let out = null;
  for (const [re, fn] of VIEWS) { const m = r.match(re); if (m) { out = fn(m); if (out) break; } }
  if (!out) out = { crumbs: [["Início", "../"]], html: `<h1>Página não encontrada</h1><p class="lead">Use o menu para voltar ao Judô ou ao Jiu-Jitsu.</p>` };
  $("#conteudo").innerHTML = (out.crumbs ? crumbs(out.crumbs.map(c => [c[0], c[1] || "#"])) : "") + out.html + `<p class="up"><a class="pill" href="#" data-back>← Voltar</a></p>`;
  $("#m-judo").setAttribute("aria-current", /^\/judo/.test(r)); $("#m-bjj").setAttribute("aria-current", /^\/jiu-jitsu/.test(r));
  side(r); document.body.classList.remove("drawer"); window.scrollTo(0, 0); out.init && out.init();
  document.title = (out.crumbs ? out.crumbs[out.crumbs.length - 1][0] + " · " : "") + "Judô e Jiu-Jitsu";
}
window.addEventListener("hashchange", render);
document.addEventListener("click", e => {
  if (e.target.closest("[data-back]")) { e.preventDefault(); history.back(); return; }
  const p = e.target.closest("[data-play]"); if (p) { const w = p.parentElement; w.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(p.dataset.play)}?autoplay=1&rel=0&modestbranding=1" title="Vídeo" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`; return; }
  const z = e.target.closest("[data-zoom]"); if (z) { $("#dimg").src = z.src; $("#dcap").textContent = z.alt || ""; $("#dlg").showModal(); }
});
$("#menu").onclick = () => { const o = document.body.classList.toggle("drawer"); $("#menu").setAttribute("aria-expanded", o); };
/* busca */
const IDX = []; Object.values(T).forEach(t => IDX.push({ k: [t.nome, t.ja, t.en, t.pt].join(" ").toLowerCase(), l: t.nome, ja: t.ja, s: t.pt || t.en, h: "#/judo/tecnica/" + t.id }));
J.glossario.forEach(g => IDX.push({ k: (g.termo + " " + g.kanji + " " + g.def).toLowerCase(), l: g.termo, ja: g.kanji, s: "glossário", h: "#/judo/t/glossario" }));
B.faixas.forEach(f => IDX.push({ k: f.titulo.toLowerCase() + " jiu-jitsu", l: f.titulo, ja: "", s: "Jiu-Jitsu · exame", h: "#/jiu-jitsu/faixa/" + f.id }));
J.faixas.forEach(f => IDX.push({ k: f.titulo.toLowerCase() + " judo judô " + (f.sub || "").toLowerCase(), l: f.titulo, ja: "", s: "Judô · " + f.sub, h: "#/judo/faixa/" + f.id }));
const q = $("#q"), res = $("#res");
q.addEventListener("input", () => { const v = q.value.trim().toLowerCase(); if (v.length < 2) { res.classList.remove("open"); return; } const hits = IDX.filter(x => x.k.indexOf(v) >= 0).slice(0, 12); res.innerHTML = hits.length ? hits.map(x => `<li><a href="${x.h}"><span class="jp" lang="ja">${esc(x.ja)}</span> <b>${esc(x.l)}</b> <small>${esc(x.s)}</small></a></li>`).join("") : `<li><a href="#"><small>Nada encontrado</small></a></li>`; res.classList.add("open"); });
res.addEventListener("click", () => { res.classList.remove("open"); q.value = ""; });
document.addEventListener("click", e => { if (!e.target.closest(".search")) res.classList.remove("open"); });
render();
})();
