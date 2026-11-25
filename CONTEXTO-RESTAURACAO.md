# Contexto da restauração do conteúdo por faixa (25/11/2026)

Este arquivo explica **por que** cada mudança desta etapa foi feita, para quem retomar o projeto depois. As mudanças foram feitas com IA (Claude Opus 5.5, Anthropic) a pedido do autor.

## Pontos de restauração

| Ramo | Estado guardado | Para voltar |
| --- | --- | --- |
| `backup/v1.0` | Site em página única, antes do livro interativo (22/11/2026) | `git reset --hard backup/v1.0` |
| `backup/v2.0` | Portal com explorador, app e "uma etapa por cor", **antes** desta restauração (commit `a41a073`, 24/11/2026) | `git reset --hard backup/v2.0` |
| `backup/v3.0` | Conteúdo por faixa restaurado **e** programa acumulado por faixa, conferido com axe-core (25/11/2026) | `git reset --hard backup/v3.0` |

Para publicar a volta: `git push --force origin main` depois do `reset`.

## Regra que orientou o trabalho

As faixas do Judô agora aparecem **uma vez por cor** (o commit #38 reuniu os dois exames de cada cor). Regra do autor: **tudo o que está numa cor tem de ser o exame dessa cor**. Por exemplo:

- **Cinza:** reúne o exame do 11º Kyû (Branca/Cinza) e o do 10º Kyû (Cinza).
- **Azul:** 9º e 8º Kyû.
- **Amarela:** 7º e 6º Kyû.
- **Laranja:** 5º e 4º Kyû.
- **Verde, Roxa e Marrom:** 3º, 2º e 1º Kyû.
- **Preta e graus superiores:** os dans.

A referência de conteúdo é o **ponto de restauração** (livro, `source/doc.md`). Os capítulos de faixas do livro estavam idênticos ao ponto de restauração; o problema estava na montagem do explorador (`site/explorar/dados.js`) e nos itens do regulamento lidos do PDF (`site/app/data.js`).

## Avaliação de figuras e vídeos (antes de mudar)

- **Livro (`site/livro.html`):** 86 figuras e 205 botões de vídeo, todos na mesma posição do ponto de restauração. Nada a corrigir.
- **Explorador:** os 100 vídeos oficiais (Kodokan × IJF Academy) estão ligados à técnica certa. As 53 técnicas com ilustração apontam para os arquivos certos:
  - três fases (`tri_`);
  - figura (`fig`);
  - contragolpe (`kae_`);
  - ação proibida (`pro_`).

## O que foi mudado e por quê

### 1. Projeções cobradas que tinham sumido da própria faixa (Amarela: O-soto-gari; Laranja: Seoi-nage)

**Causa:** o `build_dados.py` lia as técnicas pelos links do livro, mas o livro só liga a **primeira** vez que cada técnica aparece num capítulo. Quando a técnica já tinha sido citada numa combinação anterior, ela sumia da faixa onde é cobrada.

**Correção:** `techs()` passou a ler os nomes **pelo texto** da célula, com abreviações conhecidas (por exemplo, "Sasae" = Sasae-tsurikomi-ashi).

### 2. "Kyô completo" sem a lista de técnicas (Laranja → Preta)

**Correção:** os grupos do Gokyo (1920) agora são abertos a partir da tabela de fichas do próprio livro:

- **Laranja (4º Kyû):** 2º kyô.
- **Verde:** 3º kyô.
- **Roxa:** 4º kyô.
- **Marrom:** 5º kyô.
- **Preta:** "Gokyo completo (revisão das 40)" e "Katame-waza dos três grupos".

### 3. Marca do Kyû em cada técnica dentro da cor

**Causa:** ao juntar os dois exames da mesma cor, a marca do Kyû ficava só nos textos.

**Correção:**

- Cada técnica leva o seu Kyû (campos `nageKyu` e `katameKyu`).
- O explorador separa "Novas neste exame · 11º Kyû" de "Novas neste exame · 10º Kyû".
- O mapeamento livro → etapa passou a ser **pelo número do Kyû/Dan**, e não pela posição na lista (a posição mudou com a mesclagem).

### 4. Combinações com técnicas faltando e exemplos de faixas posteriores

**Correções:**

- As técnicas das combinações são lidas pelo texto, sem perder elos (Azul: De-ashi-harai; Amarela: Sasae e O-soto-gari; Laranja e Roxa: O-uchi-gari; Marrom: O-soto-gari).
- "+ Sasae" passou a mostrar o nome completo.
- A página de combinações de cada cor mostra primeiro as **exigidas neste exame**, com o Kyû.
- Os demais exemplos só aparecem quando **todas** as técnicas já foram vistas. Antes bastava uma, e a Azul mostrava Kesa-gatame → Kata-gatame e Yoko-shiho-gatame → Juji-gatame, técnicas de faixas posteriores.

### 5. Dans sem o programa do livro (preta 1º ao 8º Dan)

**Correção:** cada dan recebe, do livro, uma tabela "Programa do exame (CBJ, FJERJ e IJF)" com:

- o kata completo e o kata por sorteio, a prova técnica e a teoria e didática (CBJ);
- o exame admissional da FJERJ como exemplo estadual (1º Dan: 6 técnicas por grupo, 5 kaeshi-waza e 5 renraku-henka-waza; 2º Dan: 10 técnicas por grupo e 7 kaeshi-waza; 4º e 5º Dan: todas as técnicas);
- o programa mínimo da IJF a partir de 2026.

Do 6º ao 8º Dan, a CBJ promove por currículo, e isso aparece como "Forma de promoção", não como kata.

### 6. 9º e 10º Dan ausentes

**Correção:** criadas as etapas `j20` e `j21` (faixa vermelha), no explorador e no app. Os dados vêm do livro: a tabela de idades e carências da CBJ e o programa mínimo de dans da IJF. O regulamento da CBJ de 2023 lido pelo app vai só até o 8º Dan, e a nota da etapa diz isso.

### 7. Itens do regulamento fora do lugar

As correções ficam em `source/portal/corrigir_dados.py`, que é idempotente e é chamado pelo `montar_portal.py` e pelo `build_dados.py`.

- A imobilização do 11º e a do 7º Kyû saíram de "Outros critérios" e foram para "Imobilização (Osae komi waza)".
- No 6º Kyû, as imobilizações e as viradas viraram dois itens.
- A idade mínima do 8º Kyû (7 anos) virou item. O valor está nos fatos da própria etapa, lidos do regulamento.
- Um item igual nos dois exames da cor agora leva os dois Kyû (por exemplo, "9º e 8º Kyû"), para ficar claro que vale para ambos.

### 8. Palavras quebradas pela leitura do PDF

**Correção:** 18 ocorrências corrigidas, como "imob ilização", "C ampeonato", "Mar rom" e "Ki me".

### 9. Interface pedida pelo autor (página inicial)

- Os botões de menu (sumário), "Sobre" e busca ficaram **20% maiores**: de 38 para 46 px, com ícones de 22 px.
- **No celular**, os botões passaram da barra inferior para o **alto do cabeçalho**, ao lado do logotipo, que ganhou espaço reservado para não ser coberto. O mesmo vale para o modo "Celular" escolhido no computador.
- O texto "O que é cobrado em cada exame de faixa", acima dos botões Judô e Jiu-Jitsu, **saiu da tela**. Ele continua como título para leitores de tela (classe `sr`), porque a página precisa de um título principal (WCAG).

## Limites honestos

- **Escolha das técnicas:** a CBJ fixa *quantas* técnicas cada faixa mostra. *Quais* técnicas, quem define é a Comissão Estadual. As técnicas por faixa seguem o roteiro do livro, na ordem do Gokyo, como no ponto de restauração.
- **Nomes em inglês:** o `glossario.py` do projeto local precisa de um PDF da Kodokan que não está no repositório. Por isso o `build_dados.py` reaproveita os nomes já publicados. Os nomes não mudaram: 91 técnicas com nome em inglês, antes e depois.
- **Tradução para o inglês:** foi gerada sem tradução automática (`--sem-mt`). Os textos novos sem tradução manual continuam em português no modo EN.

## Arquivos alterados

| Arquivo | Mudança |
| --- | --- |
| `source/portal/build_dados.py` | Técnicas lidas pelo texto, Gokyo aberto, mapeamento por Kyû/Dan, marca do Kyû, combinações exigidas, programa dos dans, nomes em inglês de reserva |
| `source/portal/corrigir_dados.py` (novo) | Correções dos itens do regulamento, 9º e 10º Dan |
| `source/portal/montar_portal.py` | Chama `corrigir_dados` depois da mesclagem por cor |
| `source/portal/explorar/explorar.js` e `site/explorar/explorar.js` | Novas técnicas agrupadas por Kyû, combinações exigidas, título do programa dos dans |
| `source/portal/landing_template.html` e `site/index.html` | Botões 20% maiores, no alto do cabeçalho no celular, título oculto na tela |
| `source/portal/i18n_portal_manual.json` e `site/assets/i18n-*.js` | Traduções dos textos novos |
| `site/explorar/dados.js`, `site/app/data.js` | Dados gerados de novo |

## Etapa seguinte: programa acumulado por faixa (25/11/2026)

**Pedido do autor:** mostrar, nas duas modalidades, o conteúdo das faixas anteriores somado ao da faixa escolhida, sem exagerar, com botões visíveis e com o nome completo, conferido com axe para leitores de tela. Depois, criar o terceiro ponto de restauração (`backup/v3.0`).

**Por que uma página à parte, e não tudo na página da faixa:** somar tudo na página do exame ficaria longo demais no celular (Marrom do Judô: cerca de 40 projeções e 17 técnicas de solo; Jiu-Jitsu: mais de 140 itens) e esconderia o que é específico de cada exame, que é a regra do portal. Por isso a página da faixa continua mostrando o exame, e um botão leva ao acumulado.

**Como cada tópico se comporta:**

- **Somam:** técnicas, combinações, contragolpes e os textos do regulamento (técnica, fundamentos, kata, vocabulário, história, teoria).
- **Não se somam (vale só o exame atual):** idade mínima, carência, quantidades e formato das provas. Ficam no quadro "Vale só para este exame".
- **Aparecem uma vez:** saudação e quedas entram na faixa em que aparecem; textos idênticos não se repetem.
- **Jiu-Jitsu:** a lista da JJIF de cada faixa já repete a maior parte da anterior. O acumulado mostra a lista da faixa e, à parte, os itens de faixas anteriores que não se repetem nela, com o aviso de que as fontes não dizem se continuam sendo cobrados. As cadeias de adultos e infantil são separadas.

**Onde estão os botões:** página de cada faixa (explorador), seção "Programa acumulado por faixa" nas páginas do Judô e do Jiu-Jitsu, menu lateral do explorador, e na página inicial (botão sob a faixa escolhida e lista de links quando nenhuma faixa está escolhida).

**Acessibilidade (leitor de tela):** tópicos recolhíveis com botão dentro do título (`aria-expanded`, `aria-controls`); alternância "acumulado / só desta faixa" como grupo de botões com `aria-pressed`; mudança anunciada por região de status; títulos em ordem (h1 → h2 → h3 → h4); desenhos de faixa decorativos ocultos quando o nome já está escrito; pausas faladas entre título e contagem.

**Verificação com axe-core 4.10.3** (regras WCAG 2.0, 2.1 e 2.2 A/AA e boas práticas), no site publicado, temas claro e escuro, com todos os tópicos abertos: **0 violações** em 9 páginas do explorador (5 páginas acumuladas, os dois hubs e duas páginas de faixa) e em 4 estados da página inicial. Ficaram só itens "a conferir" que o axe não mede (símbolos como ▾ e → e o fundo com imagem do topo), sem problema de contraste. Os testes do repositório (`acessibilidade.js`, `wcag.js`) também passam nas páginas novas; as duas falhas que aparecem já existiam e estão em `PENDENCIAS.md`.

**Observação técnica:** o site tem política de segurança (CSP) que bloqueia scripts de fora, o que está correto. Para rodar o axe no site publicado, a página foi carregada sem essa política em uma aba de teste; o script `source/portal/tests/axe_varredura.js` continua precisando de `site/assets/axe.min.js` na cópia local (não versionado).

**Arquivos:** `source/portal/explorar/explorar.js` e `.css` (páginas e botões), `source/portal/landing_template.html` e `montar_portal.py` (página inicial), `i18n_portal.py`, `i18n_portal_manual.json` e `explorar_strings.json` (textos em inglês), testes em `source/portal/tests/`.
