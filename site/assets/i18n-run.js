/* Tradutor de interface: troca textos e atributos usando window.I18N_PAGE = {en:{pt:en}, rules:[[regex, substituição]]}. */
(function () {
  "use strict";
  var P = window.I18N_PAGE || {}, DICT = P.en || {}, RULES = (P.rules || []).map(function (r) { return [new RegExp(r[0]), r[1]]; });
  var ATTR = ["placeholder", "aria-label", "alt", "title", "data-cap", "data-ai", "content"];
  function t0(k) { if (!k) return null; var r = DICT[k]; if (r !== undefined) return r; for (var i = 0; i < RULES.length; i++) if (RULES[i][0].test(k)) return k.replace(RULES[i][0], RULES[i][1]); return null; }
  function trs(s) {
    if (s == null || s === "") return s; s = String(s); var m = s.match(/^(\s*)([\s\S]*?)(\s*)$/), k = m[2].replace(/\s+/g, " "); if (!k) return s;
    var r = t0(k);
    if (r === null) { var parts = k.split(/( — | · |: |\n)/); if (parts.length > 1) { var ch = false, o = parts.map(function (p, i) { if (i % 2) return p; var q = t0(p.trim()); if (q !== null) { ch = true; return q; } return p; }); if (ch) r = o.join(""); } }
    return r === null ? s : m[1] + r + m[3];
  }
  function node(n) {
    if (n.nodeType === 3) { var p = n.parentElement; if (!p || /^(SCRIPT|STYLE|TEXTAREA|NOSCRIPT)$/.test(p.tagName) || p.closest("[data-no-tr]")) return; var v = n.nodeValue; if (!v.trim()) return; var r = trs(v); if (r !== v) n.nodeValue = r; }
    else if (n.nodeType === 1) { if (/^(SCRIPT|STYLE)$/.test(n.tagName) || n.hasAttribute("data-no-tr")) return; ATTR.forEach(function (a) { if (a === "content" && n.tagName !== "META") return; var v = n.getAttribute(a); if (v) { var r = trs(v); if (r !== v) n.setAttribute(a, r); } }); for (var c = n.firstChild; c; c = c.nextSibling) node(c); }
  }
  var OPT = { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTR }, pend = false, mo;
  function run() { pend = false; mo.disconnect(); node(document.documentElement); var t = trs(document.title); if (t !== document.title) document.title = t; mo.observe(document.documentElement, OPT); }
  mo = new MutationObserver(function () { if (!pend) { pend = true; requestAnimationFrame(run); } });
  function start() { run(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
  window.JTI18N = { trs: trs };
})();
