/* Nomes acessíveis das faixas desenhadas (leitores de tela): ["#2f64c8"] -> "Faixa azul" (PT) ou "Blue belt" (EN);
   duas cores -> "Faixa branca e cinza". A cor é identificada pela paleta oficial do portal (tokens.css). */
(function () {
  var PAL = [["branca", "white", "#f5f5f2"], ["cinza", "gray", "#9aa3ab"], ["amarela", "yellow", "#f2c230"], ["laranja", "orange", "#ee8a2b"], ["verde", "green", "#2e9b5b"],
    ["azul", "blue", "#2f64c8"], ["roxa", "purple", "#7a3fa3"], ["marrom", "brown", "#7a4a2b"], ["preta", "black", "#1e2228"], ["vermelha", "red", "#c8352f"]];
  function rgb(h) { h = String(h || "").replace("#", ""); if (h.length === 3) h = h.replace(/(.)/g, "$1$1"); var n = parseInt(h, 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function near(h) { var c = rgb(h), best = 0, bd = 1e9; PAL.forEach(function (p, i) { var q = rgb(p[2]), d = Math.pow(c[0] - q[0], 2) + Math.pow(c[1] - q[1], 2) + Math.pow(c[2] - q[2], 2); if (d < bd) { bd = d; best = i; } }); return best; }
  function lang() { return (window.JTPrefs && window.JTPrefs.state && window.JTPrefs.state.lang === "en") ? "en" : "pt"; }
  window.JTBelts = {
    label: function (cols, l) {
      cols = (cols || []).filter(Boolean); if (!cols.length) return l === "en" ? "Belt" : "Faixa";
      l = l || lang(); var a = near(cols[0]), b = cols[1] ? near(cols[1]) : a, i = l === "en" ? 1 : 0;
      if (l === "en") return a === b ? PAL[a][1].replace(/^./, function (c) { return c.toUpperCase(); }) + " belt" : (PAL[a][1].replace(/^./, function (c) { return c.toUpperCase(); }) + " and " + PAL[b][1] + " belt");
      return "Faixa " + PAL[a][0] + (a === b ? "" : " e " + PAL[b][0]);
    }
  };
})();
