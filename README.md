# Judô: técnicas e exames de faixa

Material de estudo interativo sobre o programa de exames de faixa da CBJ e as regras e a classificação da IJF/Kodokan, com 119 ilustrações originais geradas por código.

- **Site:** abre em computador e celular, com sumário, índice de técnicas, busca, carrosséis com deslize, zoom nas imagens, simulado interativo, modo claro/escuro e escolha entre design para computador ou para celular.
- **PDF:** `site/judo-tecnicas-e-exames-de-faixa.pdf` (A4, sumário e índice com links, marcadores por capítulo).

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `site/` | Site publicado (HTML, CSS, JS, imagens WebP e o PDF) |
| `source/` | Gerador do site (`build.py`), do PDF (`make_pdf.py`) e o texto-base (`doc.md`) |
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
