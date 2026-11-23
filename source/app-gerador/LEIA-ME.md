# Gerador do app “Faixa a faixa” (cópia de referência)

Estes arquivos vêm do projeto local **Judo_BJJ** (sessão de trabalho com o Claude Code): geram o app que fica em `site/app/`.

- `gerar_webapp_dados.py` lê os PDFs oficiais (CBJ, IBJJF/CBJJ, JJIF, IJF/Kodokan, Judo Québec, BJA, LBJJ), extrai textos e imagens e escreve `data.js`.
- `glossario.py`: nomes em japonês, inglês e português (Kodokan, FJERJ, CBJ, CBJJ).
- `index_base.html`, `ficha_form.html`, `visual.py`: interface, ficha de exame editável e visual.
- `i18n_*.py`, `i18n_manual.json`, `i18n_dict.json`: tradução PT-BR/EN (Argos Translate offline + correções manuais).
- `standalone.py`: gera o arquivo único para celular.

Os PDFs de origem e os caminhos (`D:\Claude\Judo_BJJ`) pertencem ao computador do autor e **não** estão neste repositório; por isso os scripts servem como registro, e o resultado pronto está em `site/app/`. Para atualizar o portal: gere o app no projeto local e rode `python source/portal/montar_portal.py <pasta www>`.

Publicamos só **miniaturas** dos recortes de documentos oficiais, sempre com a fonte citada.
