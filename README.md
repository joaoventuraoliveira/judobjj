# Judô: técnicas e exames de faixa

Material de estudo interativo sobre o programa de exames de faixa da CBJ e as regras e a classificação da IJF/Kodokan, com 119 ilustrações originais geradas por código.

- **Site (livro interativo):** um capítulo por página, com botões anterior/próximo; termos do glossário, técnicas e citações ligados no texto, com prévia ao tocar ou passar o mouse (as técnicas mostram a miniatura da ilustração). A gaveta lateral tem busca no texto completo e atalhos para técnicas, glossário, fontes e uso de IA. Também tem carrosséis com deslize, zoom nas imagens, simulado interativo, modo claro/escuro e escolha entre design para computador ou para celular.
- **Referências:** a lista ABNT aparece no fim de cada capítulo e reunida no capítulo “Referências”, que indica onde cada fonte é citada.
- **Uso de IA:** texto, ilustrações (por código Python), glossário, simulado e site foram gerados com IA (**Claude Opus 5.5, Anthropic**). Cada capítulo e cada figura têm um selo, há um capítulo “Transparência sobre o uso de IA”, e os metadados legíveis por máquina estão em JSON-LD na página e em `site/ai-disclosure.json`.
- **PDF:** `site/judo-tecnicas-e-exames-de-faixa.pdf` (A4, sumário e índice com links, marcadores por capítulo).

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `site/` | Site publicado (HTML, CSS, JS, imagens WebP e o PDF) |
| `source/` | Gerador do site (`build.py`), do PDF (`make_pdf.py`) e o texto-base (`doc.md`) |
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

## Ponto de restauração

A versão anterior (site em página única, antes do livro interativo) está no ramo `backup/v1.0`. Para voltar a ela: `git checkout main && git reset --hard backup/v1.0 && git push --force origin main`.
