/* Preferências compartilhadas do portal: tema (auto/claro/escuro), layout (auto/PC/celular) e idioma (PT-BR/EN).
   Chaves em localStorage: jt-theme, jt-layout, jt-lang (as mesmas do livro). Roda no <head> para não piscar. */
(function () {
  "use strict";
  var R = document.documentElement, BOOK = R.hasAttribute("data-book");
  var S = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  var st = { theme: S.get("jt-theme") || "auto", layout: S.get("jt-layout") || "auto", lang: S.get("jt-lang") === "en" ? "en" : "pt" };
  if (["auto", "light", "dark"].indexOf(st.theme) < 0) st.theme = "auto";
  if (["auto", "desktop", "mobile"].indexOf(st.layout) < 0) st.layout = "auto";
  var mqL = matchMedia("(max-width: 900px)"), mqD = matchMedia("(prefers-color-scheme: dark)");
  var vp = null, vp0 = null;
  function press() {
    [["data-layout-set", "layout"], ["data-theme-set", "theme"], ["data-lang-set", "lang"]].forEach(function (p) {
      document.querySelectorAll("[" + p[0] + "]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute(p[0]) === st[p[1]]); });
    });
  }
  function applyLayout() {
    if (BOOK) return;
    var m = st.layout === "mobile" || (st.layout === "auto" && mqL.matches);
    R.setAttribute("data-layout", st.layout); R.classList.toggle("lay-mobile", m); R.classList.toggle("lay-desktop", !m);
    vp = vp || document.querySelector('meta[name="viewport"]'); if (vp && vp0 === null) vp0 = vp.getAttribute("content");
    if (vp) vp.setAttribute("content", st.layout === "desktop" ? "width=1100" : vp0);
    press();
  }
  function applyTheme() {
    if (BOOK) return;
    var d = st.theme === "dark" || (st.theme === "auto" && mqD.matches);
    R.setAttribute("data-theme", d ? "dark" : "light"); R.setAttribute("data-theme-pref", st.theme);
    var tc = document.querySelector('meta[name="theme-color"]'); if (tc) tc.setAttribute("content", d ? "#0b0d11" : "#f2f4f7");
    press();
  }
  R.setAttribute("lang", st.lang === "en" ? "en" : "pt-BR"); R.setAttribute("data-lang", st.lang);
  applyLayout(); applyTheme();
  (mqL.addEventListener ? mqL.addEventListener("change", applyLayout) : mqL.addListener(applyLayout));
  (mqD.addEventListener ? mqD.addEventListener("change", applyTheme) : mqD.addListener(applyTheme));
  function setTheme(t) { st.theme = t; S.set("jt-theme", t); if (BOOK) { R.setAttribute("data-theme", t); } applyTheme(); press(); }
  function setLayout(l) { st.layout = l; S.set("jt-layout", l); applyLayout(); }
  function setLang(l) { if (l === st.lang) return; S.set("jt-lang", l); location.reload(); }
  window.JTPrefs = { state: st, setTheme: setTheme, setLayout: setLayout, setLang: setLang, cycleTheme: function () { setTheme({ auto: "light", light: "dark", dark: "auto" }[st.theme]); } };
  var T = { pt: { layout: "Layout", tema: "Tema", idioma: "Idioma", auto: "Auto", pc: "PC", cel: "Celular", t0: "Seguir o sistema", t1: "Modo claro", t2: "Modo escuro", l0: "Ajustar à tela", l1: "Design para computador", l2: "Design para celular" },
            en: { layout: "Layout", tema: "Theme", idioma: "Language", auto: "Auto", pc: "Desktop", cel: "Phone", t0: "Follow the system", t1: "Light mode", t2: "Dark mode", l0: "Fit to screen", l1: "Desktop design", l2: "Phone design" } }[st.lang];
  function build(c) {
    var only = c.getAttribute("data-prefs"), h = "";
    if (only !== "lang" && only !== "theme") h += '<div class="seg" role="group" aria-label="' + T.layout + '"><button type="button" data-layout-set="auto" title="' + T.l0 + '">' + T.auto + '</button><button type="button" data-layout-set="desktop" title="' + T.l1 + '">' + T.pc + '</button><button type="button" data-layout-set="mobile" title="' + T.l2 + '">' + T.cel + '</button></div>';
    if (only !== "layout" && only !== "lang") h += '<div class="seg" role="group" aria-label="' + T.tema + '"><button type="button" data-theme-set="auto" title="' + T.t0 + '" aria-label="' + T.t0 + '"><span aria-hidden="true">◐</span></button><button type="button" data-theme-set="light" title="' + T.t1 + '" aria-label="' + T.t1 + '"><span aria-hidden="true">☀</span></button><button type="button" data-theme-set="dark" title="' + T.t2 + '" aria-label="' + T.t2 + '"><span aria-hidden="true">☾</span></button></div>';
    if (only !== "layout" && only !== "theme") h += '<div class="seg" role="group" aria-label="' + T.idioma + '"><button type="button" data-lang-set="pt" lang="pt-BR" aria-label="Português (Brasil)">PT-BR</button><button type="button" data-lang-set="en" lang="en" aria-label="English">EN</button></div>';
    c.innerHTML = h;
  }
  document.addEventListener("DOMContentLoaded", function () { document.querySelectorAll("[data-prefs]").forEach(build); press(); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-layout-set],[data-theme-set],[data-lang-set]"); if (!b) return;
    if (b.hasAttribute("data-lang-set")) { setLang(b.getAttribute("data-lang-set")); }
    else if (b.hasAttribute("data-theme-set")) { if (!BOOK) setTheme(b.getAttribute("data-theme-set")); }
    else if (b.hasAttribute("data-layout-set")) { if (!BOOK) setLayout(b.getAttribute("data-layout-set")); }
  });
  document.addEventListener("DOMContentLoaded", press);
})();
