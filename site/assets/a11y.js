/* Rede de segurança de acessibilidade (norma pétrea do portal): avisa leitores de tela quando um link abre em nova aba
   e injeta o estilo do texto oculto. Os rótulos de ícones, imagens e vídeos vêm do código de cada página; esta rede só complementa. */
(function () {
  var L = function () { return (window.JTPrefs && window.JTPrefs.state && window.JTPrefs.state.lang === "en") ? " (opens in a new tab)" : " (abre em nova aba)"; };
  if (!document.getElementById("sr-a11y-style")) { var s = document.createElement("style"); s.id = "sr-a11y-style"; s.textContent = ".sr-a11y{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}"; document.head.appendChild(s); }
  function fix(root) {
    (root.querySelectorAll ? root : document).querySelectorAll('a[target="_blank"]').forEach(function (a) {
      if (a.querySelector(".sr-newtab") || /nova aba|new tab/i.test(a.textContent)) return;
      var sp = document.createElement("span"); sp.className = "sr-a11y sr-newtab"; sp.textContent = L(); a.appendChild(sp);
    });
  }
  function start() { fix(document); new MutationObserver(function (m) { m.forEach(function (x) { x.addedNodes.forEach(function (n) { if (n.nodeType === 1) fix(n.matches && n.matches("a") ? n.parentNode : n); }); }); }).observe(document.body, { childList: true, subtree: true }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
