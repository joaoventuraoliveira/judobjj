/* Carrega o dicionário de tradução (PT-BR -> EN) da página e o tradutor, só quando o idioma é inglês.
   Uso: <script src=".../i18n.js" data-dict=".../i18n-PAGINA.js"></script> */
(function () {
  var R = document.documentElement; if (R.getAttribute("data-lang") !== "en") return;
  var me = document.currentScript, dict = me.getAttribute("data-dict"), base = me.src.replace(/i18n\.js(\?.*)?$/, "");
  document.write('<script src="' + dict + '"><\/script><script src="' + base + 'i18n-run.js"><\/script>');
})();
