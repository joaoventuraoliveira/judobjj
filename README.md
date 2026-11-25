# Judô: técnicas e exames de faixa

Material de estudo interativo sobre o programa de exames de faixa da CBJ e as regras e a classificação da IJF/Kodokan, com 119 ilustrações originais geradas por código.

- **Site (livro interativo):** um capítulo por página, com botões anterior/próximo; termos do glossário, técnicas e citações ligados no texto, com prévia ao tocar ou passar o mouse (as técnicas mostram a miniatura da ilustração). A gaveta lateral tem busca no texto completo e atalhos para técnicas, glossário, fontes e uso de IA. Também tem carrosséis com deslize, zoom nas imagens, simulado interativo, modo claro/escuro e escolha entre design para computador ou para celular.
- **Videoteca oficial:** os 100 vídeos da série “100 Techniques” do Kodokan com a IJF Academy (68 projeções e 32 katame-waza), além de fundamentos, saídas de imobilização e aulas da série “Waza”. Os vídeos tocam dentro do livro, nas ilustrações e nas prévias das técnicas, pelo modo de privacidade do YouTube. A lista de vídeos fica em `source/videos.py`.
- **Referências:** a lista ABNT aparece no fim de cada capítulo e reunida no capítulo “Referências”, que indica onde cada fonte é citada.
- **Uso de IA:** texto, ilustrações (por código Python), glossário, simulado e site foram gerados com IA (**Claude Opus 5.5, Anthropic**). Cada capítulo e cada figura têm um selo, há um capítulo “Transparência sobre o uso de IA”, e os metadados legíveis por máquina estão em JSON-LD na página e em `site/ai-disclosure.json`.
- **PDF:** `site/judo-tecnicas-e-exames-de-faixa.pdf` (A4, sumário e índice com links, marcadores por capítulo).

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `site/` | Site publicado (HTML, CSS, JS, imagens WebP e o PDF) |
| `source/` | Gerador do site (`build.py`), do PDF (`make_pdf.py`) e o texto-base (`doc.md`) |
| `source/videos.py`, `source/vidbuild.py` | Catálogo dos vídeos oficiais e montagem da videoteca |
| `source/glossary.py`, `source/enrich.py` | Glossário e ligações internas (termos, técnicas, citações, referências e selos de IA) |
| `source/src/` | Estilos (`style.css`, `print.css`) e interações (`app.js`) |
| `source/figuras/` | Scripts Python de cada ilustração (`judoka.py` é o módulo base) |
| `.github/workflows/pages.yml` | Publicação automática no GitHub Pages |

## Publicação (uma vez só)

Em **Settings → Pages → Build and deployment → Source**, escolha **GitHub Actions**. A cada envio para a branch `main`, o site é publicado em `https://<usuario>.github.io/<repositorio>/`.

## Atualizar o conteúdo

1. Edite `source/doc.md` ou os scripts em `source/figuras/` e gere as imagens de novo.
2. Rode `python3 source/build.py` e `python3 source/make_pdf.py` (requer Python 3, `markdown`, `beautifulsoup4`, `playwright` e Google Chrome).
3. Copie o conteúdo de `dist/` para `site/` e envie para a `main`.

Conteúdo baseado nos regulamentos da CBJ, de federações estaduais e nas regras da IJF. Confira sempre a versão vigente com a sua federação.

## Pontos de restauração

- `backup/v1.0`: site em página única, antes do livro interativo (22/11/2026).
- `backup/v2.0`: portal com explorador e app, antes da restauração do conteúdo por faixa (24/11/2026).
- `backup/v3.0`: conteúdo por faixa restaurado e programa acumulado por faixa, conferido com axe-core (25/11/2026).

Para voltar a um deles: `git checkout main && git reset --hard backup/v2.0 && git push --force origin main` (troque pelo ramo desejado). O motivo de cada mudança feita depois do `backup/v2.0` (inclusive o programa acumulado) está em [`CONTEXTO-RESTAURACAO.md`](CONTEXTO-RESTAURACAO.md).

## Portal: Judô e Jiu-Jitsu

A página inicial (`site/index.html`) apresenta as duas modalidades, com os kanjis e os termos habituais:

- **Judô (柔道):** o livro interativo (`site/livro.html`, antigo `index.html`), a videoteca oficial e o app **Faixa a faixa** (`site/app/#judo/j01`) com o programa de cada kyū, dan e grau superior.
- **Jiu-Jitsu (柔術):** o app **Faixa a faixa** (`site/app/#bjj/b01`) com o programa técnico da JJIF por faixa, ficha de exame editável, lista de componentes (guardas, raspagens, transições, chaves, estrangulamentos, defesa pessoal), regras IBJJF/CBJJ, apostila da LBJJ e vídeos oficiais.
- **App:** `site/app/` (HTML, `data.js` e miniaturas) é gerado pelo projeto local Judo_BJJ (ver `source/app-gerador/`), com tema escuro, botão de idioma PT-BR/EN (nomes em japonês sempre mantidos), busca, progresso salvo no aparelho e as fontes de cada página. Links antigos do livro (`.../#capitulo`) são redirecionados para `livro.html`.
- Para remontar: `python source/portal/montar_portal.py <pasta www do app>`.

### Explorar: da faixa até a técnica (`site/explorar/`)

Depois de escolher Judô ou Jiu-Jitsu na página inicial, o explorador abre com **menu lateral** (programa de exames, tópicos, lista de componentes e sumário do livro), **faixas amarradas em ordem** (desenhadas em SVG, com as cores de cada nível) e os **tópicos principais**. O caminho vai afunilando:

1. **Faixa** → o que é cobrado no exame, mais *Fundamentos*, *O que não se cobra em competições*, *Técnicas proibidas* (no Jiu-Jitsu, a tabela da IBJJF/CBJJ por idade e faixa) e *Referências*.
2. **Tópico** (projeções, solo, combinações, textos do regulamento, seções do programa da JJIF…) → lista de técnicas.
3. **Técnica** → nome em japonês (kanji), rōmaji, inglês (Kodokan) e português (sugestão do app), descrição, ilustrações produzidas por código, **vídeo oficial que toca na própria página** (modo de privacidade do YouTube, só carrega ao clicar) e links para os *kaeshi-waza*, as combinações (*renraku-waza*) e os *katame-waza* associados.

Os dados vêm de `source/portal/build_dados.py`, que lê o livro (`site/livro.html`), `source/videos.py`, `source/glossary.py` e o `data.js` do app, e escreve `site/explorar/dados.js`. Cada cor de faixa mostra só o exame daquela cor, com cada técnica marcada pelo seu Kyû; as correções dos itens do regulamento ficam em `source/portal/corrigir_dados.py`. Para gerar de novo só com o repositório: `python source/portal/build_dados.py site/app/data.js`. Limites honestos: só 40 técnicas têm ficha de estudo; o português dos nomes é sugestão; as fontes não definem proibições diferentes por faixa no Judô (valem as regras IJF); no Jiu-Jitsu os itens da JJIF têm só o nome, sem texto descritivo.
