// ---- Judô: técnica = ambiente de estudo (aula) ----
/* PENDENTE (invisível no site): marcadores de tempo de cada fase da técnica no vídeo.
   Preencher em site/explorar/fases-tempo.js: window.FASES_TEMPO = { "seoi-nage": { kumikata: 12, kuzushi: 31, tsukuri: 44, kake: 52 } }  (segundos).
   Enquanto um tempo não existir, a interface não mostra nenhum campo vazio. Ver source/portal/PENDENCIAS.md. */
const TEMPOS = window.FASES_TEMPO || {};
const ST = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
const GL = n => (J.glossario.find(g => g.termo === n) || {}).def || "";
const mmss = s => Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
function fasesDe(t) {
  const f = t.ficha, tri = t.imgs.find(i => /tri_/.test(i.src));
  if (t.tipo === "nage") return [
    { id: "kumikata", nome: "Kumi-kata", ja: "組み方", pt: "Pegada", texto: GL("Kumi-kata") + " Nas fichas do livro, a descrição considera tori destro, com pegada direita." },
    { id: "kuzushi", nome: "Kuzushi", ja: "崩し", pt: "Desequilíbrio", texto: (f ? "Direção principal: " + f.kuzushi + ". " : "") + GL("Kuzushi"), img: tri, slice: 0 },
    { id: "tsukuri", nome: "Tsukuri", ja: "作り", pt: "Entrada", texto: GL("Tsukuri"), img: tri, slice: 1 },
    { id: "kake", nome: "Kake", ja: "掛け", pt: "Execução", texto: (f ? "Ação-chave: " + f.acao + ". " : "") + GL("Kake"), img: tri, slice: 2 },
    { id: "erros", nome: "Biomecânica e erros comuns", ja: "", pt: "", texto: "Erros frequentes em projeções: tentar a técnica sem desequilibrar uke antes; entrar sem apoio firme dos pés; soltar a pegada da manga; olhar para baixo e perder a postura; puxar só com os braços em vez de usar o quadril e as pernas; terminar sem controlar a queda de uke. Orientação geral de ensino do judô, redigida com IA; confirme com o seu professor." }];
  const g = /imobiliza/i.test(t.grupo) ? "Osaekomi-waza" : /estrangul/i.test(t.grupo) ? "Shime-waza" : "Kansetsu-waza";
  const fim = { "Osaekomi-waza": "Manter uke imobilizado de costas pelo tempo regulamentar, sem deixar o tronco e o quadril abrirem espaço.", "Shime-waza": "Aplicar o estrangulamento com controle até a desistência de uke ou a decisão do árbitro; confira as variações permitidas na sua federação.", "Kansetsu-waza": "Aplicar a chave com controle; em competição só é permitida no cotovelo, e a pressão deve ser progressiva." }[g];
  return [
    { id: "entrada", nome: "Entrada e controle inicial", ja: "", pt: "", texto: "Passagem do combate em pé ou do solo para a posição de controle. Veja, mais abaixo, as combinações em que esta técnica aparece." },
    { id: "controle", nome: "Posição de controle", ja: "", pt: "", texto: GL(g) },
    { id: "finalizacao", nome: "Finalização", ja: "", pt: "", texto: fim },
    { id: "saidas", nome: "Saídas e defesas", ja: "", pt: "", texto: "Estude também a técnica pelo lado de uke: saídas e defesas. A videoteca traz saídas oficiais de algumas imobilizações (kuzure-kesa-gatame, kata-gatame, uki-gatame e ura-gatame)." },
    { id: "erros", nome: "Biomecânica e erros comuns", ja: "", pt: "", texto: "Erros frequentes no solo: perder o controle do tronco ou do quadril; abrir espaço entre os corpos; ter pressa de finalizar antes de estabilizar; deixar a cabeça sem proteção. Orientação geral de ensino do judô, redigida com IA; confirme com o seu professor." }];
}
function studyAside(key, fases, nomeTec) {
  const chk = ST.get("jt-chk:" + key, {}), nota = ST.get("jt-nota:" + key, ""), feitos = fases.filter(f => chk[f.id]).length;
  return `<aside class="aula-panel" aria-label="Painel de estudo">
 <div class="panel-h"><h2>Fases da técnica</h2><span class="prog-txt" data-prog-txt>${feitos} de ${fases.length}</span></div>
 <div class="meter" role="progressbar" aria-label="Progresso nesta técnica" aria-valuemin="0" aria-valuemax="${fases.length}" aria-valuenow="${feitos}"><span style="width:${Math.round(feitos * 100 / fases.length)}%"></span></div>
 <!-- PENDENTE: marcadores de tempo por fase (site/explorar/fases-tempo.js). Não aparece no site. -->
 <ol class="fases" data-pendente-tempos="true">${fases.map((f, i) => { const sec = (TEMPOS[key] || {})[f.id]; return `<li class="fase ${chk[f.id] ? "ok" : ""}"><div class="fase-h"><label><input type="checkbox" data-fase="${f.id}" ${chk[f.id] ? "checked" : ""}> <span class="fn">${i + 1}</span><span class="ft"><b>${esc(f.nome)}</b>${f.ja ? ` <span class="jp" lang="ja">${esc(f.ja)}</span>` : ""}${f.pt ? `<small>${esc(f.pt)}</small>` : ""}</span></label>${typeof sec === "number" ? `<button type="button" class="seek" data-seek="${sec}" aria-label="Ir para ${mmss(sec)} no vídeo">▶ ${mmss(sec)}</button>` : ""}</div>
   <div class="fase-b">${f.img ? `<div class="slice" role="img" aria-label="${esc(f.nome)}: trecho da ilustração" style="background-image:url('../${esc(f.img.src)}');background-position:${f.slice * 50}% 0"></div>` : ""}<p>${esc(f.texto)}</p></div></li>`; }).join("")}</ol>
 <h2 class="panel-t">Minhas anotações</h2>
 <label class="sr" for="nota">Anotações sobre ${esc(nomeTec)}</label><textarea id="nota" data-nota="${esc(key)}" rows="5" placeholder="Escreva o que percebeu ao treinar esta técnica">${esc(nota)}</textarea>
 <p class="vnote">As anotações e o checklist ficam só neste aparelho.</p></aside>`;
}
route(/^\/judo\/tecnica\/([\w-]+)$/, m => {
  const t = T[m[1]]; if (!t) return null; const f = t.ficha; ST.set("jt-ultima", { h: "#/judo/tecnica/" + t.id, nome: t.nome, ja: t.ja });
  const where = t.faixas.map(id => jf(id)).filter(Boolean), kae = t.kaeshi, resp = t.respondeA, fases = fasesDe(t);
  return { crumbs: [["Início", "../"], ["Judô", "#/judo"], [t.tipo === "nage" ? "Projeções" : "Solo", "#/judo/t/" + (t.tipo === "nage" ? "nage" : "katame")], [t.nome, ""]], html: `
<div class="aula" data-tec="${t.id}">
 <section class="aula-main">
  <p class="kicker">${esc(t.grupo)}</p>${names(t)}
  <div class="player-wrap" id="pw">${player(t.yt, t.nome)}</div>
  <p class="vnote">Kodokan × IJF Academy, “100 Techniques”. Toca aqui, sem sair da página (modo de privacidade do YouTube).</p>
  <ul class="facts"><li><b>Tipo</b>${t.tipo === "nage" ? "Nage-waza (projeção)" : "Katame-waza (solo)"}</li>${f ? `<li><b>Classe</b>${esc(f.classe)}</li><li><b>Grupo / faixa (Gokyo)</b>${esc(f.faixa)}</li>` : ""}${where.length ? `<li><b>Entra no exame</b>${where.map(w => esc(w.titulo)).join("; ")}</li>` : ""}</ul>
  <p><a class="pill" target="_blank" rel="noopener" href="${esc(t.ijf)}">Página da IJF</a><a class="pill" href="../livro.html#t-${t.id}">No livro</a></p>
  ${t.imgs.length ? `<div class="imgs">${t.imgs.map(i => `<figure><img loading="lazy" src="../${esc(i.src)}" alt="${esc(t.nome)}: ${esc(i.cap)}" data-zoom><figcaption>${esc(i.cap)} · ilustração produzida por código (IA)</figcaption></figure>`).join("")}</div>` : ""}
 </section>
 ${studyAside(t.id, fases, t.nome)}
</div>
<h2 class="sec">Técnicas e textos relacionados</h2>
${kae.length ? `<div class="box"><h3>Kaeshi-waza: contragolpes a ${esc(t.nome)}</h3><ul class="rel">${kae.map(k => `<li><div>${tlink(k.id)}<small>${esc(k.acao)}</small></div></li>`).join("")}</ul></div>` : ""}
${resp.length ? `<div class="box"><h3>Este contragolpe responde a</h3>${resp.map(tlink).join(" ")}</div>` : ""}
${t.combos.length ? `<div class="box"><h3>Renraku-waza: combinações com ${esc(t.nome)}</h3><div class="cards">${t.combos.map(i => { const c = D.renraku[i]; return `<a class="card" href="#/judo/combo/${i}"><h3>${c.cadeia.map(s => esc(T[s].nome)).join(" → ")}</h3><p>${esc(c.tipo)}: ${esc(c.logica)}</p></a>`; }).join("")}</div></div>` : ""}
${t.katame.length ? `<div class="box"><h3>Katame-waza associados</h3>${t.katame.map(tlink).join(" ")}<p class="vnote">Técnicas de solo encadeadas com esta nas combinações do livro.</p></div>` : ""}
${!kae.length && !resp.length && !t.combos.length && !t.katame.length ? `<p class="lead">O livro não traz contragolpes nem combinações específicas para esta técnica. Veja a lista completa em <a href="#/judo/t/kaeshi">Kaeshi-waza</a> e <a href="#/judo/t/renraku">Renraku-waza</a>.</p>` : ""}`, init: wireStudy };
});
function wireStudy() { /* os eventos são delegados no documento (ver handlers abaixo) */ }
function progTec(slug, n) { const c = ST.get("jt-chk:" + slug, {}); return Object.keys(c).filter(k => c[k]).length / n; }
function nFases(t) { return t.tipo === "nage" ? 5 : 5; }
function progGrupo(slugs) { if (!slugs.length) return 0; return slugs.reduce((a, s) => a + (T[s] ? progTec(s, nFases(T[s])) : 0), 0) / slugs.length; }
const meter = p => `<div class="meter sm" role="progressbar" aria-label="Progresso de estudo" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(p * 100)}"><span style="width:${Math.round(p * 100)}%"></span></div>`;
function dashJudo() {
  let u = ST.get("jt-ultima", null); if (u && !/^#\/[\w\/-]+$/.test(String(u.h))) u = null;
  return `<h2 class="sec">Módulos de estudo</h2><div class="cards">${J.grupos.map((g, i) => { const p = progGrupo(g.itens); return `<a class="card" href="#/judo/modulo/${i}"><div class="ic" lang="ja">${g.tipo === "nage" ? "投技" : "固技"}</div><h3>${esc(g.nome)}</h3><p>${g.itens.length} técnicas</p>${meter(p)}<span class="n">${Math.round(p * 100)}% estudado</span></a>`; }).join("")}</div>` + (u ? `<div class="box cont"><h3>Continuar de onde parou</h3><a class="pill" href="${esc(u.h)}"><span class="jp" lang="ja">${esc(u.ja)}</span> ${esc(u.nome)}</a></div>` : "");
}
route(/^\/judo\/modulo\/(\d+)$/, m => {
  const g = J.grupos[+m[1]]; if (!g) return null;
  return { crumbs: [["Início", "../"], ["Judô", "#/judo"], [g.nome, ""]], html: `<h1>${esc(g.nome)}</h1><p class="lead">Toque em uma técnica para abrir a aula: vídeo, fases, anotações e checklist.</p><div class="tcards">${g.itens.map(s => `<div class="tcw">${tcard(s)}${meter(progTec(s, nFases(T[s])))}</div>`).join("")}</div>` };
});
document.addEventListener("change", e => {
  const c = e.target.closest("[data-fase]"); if (!c) return; const slug = c.closest("[data-tec]") ? c.closest("[data-tec]").dataset.tec : null; if (!slug) return;
  const k = "jt-chk:" + slug, v = ST.get(k, {}); v[c.dataset.fase] = c.checked; ST.set(k, v);
  const n = document.querySelectorAll("[data-fase]").length, feitos = Object.keys(v).filter(x => v[x]).length;
  const tx = document.querySelector("[data-prog-txt]"); if (tx) tx.textContent = feitos + " de " + n;
  const mt = document.querySelector(".aula-panel .meter"); if (mt) { mt.setAttribute("aria-valuenow", feitos); mt.firstElementChild.style.width = Math.round(feitos * 100 / n) + "%"; }
  c.closest(".fase").classList.toggle("ok", c.checked);
});
document.addEventListener("input", e => { const n = e.target.closest("[data-nota]"); if (n) ST.set("jt-nota:" + n.dataset.nota, n.value); });
document.addEventListener("click", e => { const s = e.target.closest("[data-seek]"); if (!s) return; const t = s.closest("[data-tec]"); if (!t) return; const id = T[t.dataset.tec].yt; $("#pw").innerHTML = `<div class="player"><iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0&modestbranding=1&start=${+s.dataset.seek}" title="Vídeo" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>`; });
