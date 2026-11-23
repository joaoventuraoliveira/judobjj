# Pendências (não aparecem no site)

## Marcadores de tempo por fase da técnica
O ambiente de estudo (`#/judo/tecnica/<técnica>`) mostra as fases (Kumi-kata, Kuzushi, Tsukuri, Kake, biomecânica e erros comuns) **sem campos vazios**. Cada fase ganha automaticamente um botão “▶ m:ss” que pula o vídeo oficial para aquele instante quando o tempo existir.

Para preencher: edite `source/portal/explorar/fases-tempo.js` (copiado para `site/explorar/` por `montar_portal.py`):

```js
window.FASES_TEMPO = { "seoi-nage": { kumikata: 12, kuzushi: 31, tsukuri: 44, kake: 52 } };
```
Chaves das fases de projeção: `kumikata`, `kuzushi`, `tsukuri`, `kake`. De solo: `entrada`, `controle`, `finalizacao`, `saidas`. Valores em segundos. Os vídeos são os da série oficial “100 Techniques” (Kodokan × IJF Academy); marque os tempos assistindo a cada um.

## Tradução automática PT-BR → EN (pausada)
Os dicionários `site/assets/i18n-landing.js`, `i18n-explorar.js` e `i18n-livro.js` foram gerados **sem** tradução automática (só nomes de técnicas, faixas, interface e textos que já existiam no app). O restante continua em português no modo EN.
Para completar: feche outros programas e rode `source/portal/retomar_traducao.ps1` (retomável, usa cache). Gatilho: peça “retomar a tradução do portal”.
