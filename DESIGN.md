# DESIGN.md

Plataforma de estudos de Judô (柔道) e Jiu-Jitsu (柔術). Identidade: escura, sóbria e de alto contraste, com rigor técnico japonês e espaço generoso. Sem referências a marcas dentro do app.

## 1. Princípios
1. **Conteúdo primeiro.** A técnica (vídeo, nome, fases) ocupa o centro; o resto recua.
2. **Contraste e silêncio.** Fundo quase preto, superfícies elevadas com borda fina, um único acento por tela.
3. **Rigor japonês.** Kanji sempre presente e legível; alinhamento em grade; poucos ornamentos.
4. **Movimento com propósito.** Microinterações de 120–200 ms; nada de animação decorativa; respeita `prefers-reduced-motion`.
5. **Mesma estrutura no PC e no celular.** O celular é para consulta rápida no tatame; o PC, para análise detalhada.

## 2. Tokens de cor (modo escuro padrão; claro como variante)
| Token | Escuro | Claro | Uso |
|---|---|---|---|
| `--bg` | `#0A0A0B` | `#F6F5F1` | fundo da página |
| `--surface` | `#121215` | `#FFFFFF` | cartões, painéis |
| `--surface-2` | `#1A1A1F` | `#EEEDE8` | elevação 2, campos |
| `--line` | `rgba(255,255,255,.08)` | `rgba(10,10,11,.12)` | borda `1px solid` |
| `--ink` | `#F5F5F2` | `#0E0E10` | texto principal (contraste ≥ 15:1) |
| `--muted` | `#A3A3AD` | `#555560` | texto secundário (≥ 4,5:1) |
| `--accent` | `#C9A84C` (dourado fosco) | `#8A6D1E` | ação principal, foco, progresso |
| `--accent-ink` | `#0A0A0B` | `#FFFFFF` | texto sobre o acento |
| `--danger` | `#B3262E` (carmesim discreto) | `#A31F27` | proibido, falta, alerta |
| `--judo` / `--bjj` | `#2F64C8` / `#7A3FA3` | iguais | identidade de cada modalidade (detalhes, não fundos) |
Faixas (tokens de graduação, usados só nos ícones de faixa): branca `#F5F5F2`, cinza `#9AA3AE`, amarela `#F2C230`, laranja `#EE8A2B`, verde `#2E9B5B`, azul `#2F64C8`, roxa `#7A3FA3`, marrom `#7A4A2B`, preta `#1E2228`, vermelha `#C8352F`.

## 3. Tipografia
- **Display (títulos de módulo e técnica):** serifa editorial de impacto, peso 600–700, tracking −0,02em, ex.: *Fraunces* (latim) com *Shippori Mincho* para kanji.
- **Texto e interface:** sans geométrica de alta legibilidade, ex.: *Inter* (ou *Geist*), 16–17 px, entrelinha 1,55; números tabulares para timestamps.
- **Escala:** 12 / 14 / 16 / 18 / 24 / 32 / 48 / 72 px (relação ≈ 1,333).
- Fontes **hospedadas no próprio site** (woff2, `font-display: swap`), para manter a CSP restrita, o modo offline e a privacidade.

## 4. Espaço, forma e elevação
Base 4 px; blocos de seção 64–96 px; raio 12 (campos) / 16 (cartões) / 999 (pílulas); sombras só em elementos flutuantes (menus, modal). Bordas finas no lugar de sombras pesadas.

## 5. Layout
- Grid de 12 colunas; **vitrine assimétrica** (destaque 7/12 + coluna 5/12; cartões de 3 e 4 colunas abaixo).
- Judô e Jiu-Jitsu como duas portas de mesmo peso, cada uma com kanji grande, termos habituais e as faixas amarradas em ordem.
- **Página da aula:** player 16:9 à esquerda (8/12), painel de estudo à direita (4/12): fases da técnica com marcadores de tempo (Kumi-kata, Kuzushi, Tsukuri, Kake, biomecânica e erros comuns), notas pessoais e checklist. No celular, o painel desce sob o player e o player fica fixo ao rolar.
- Preferências sempre visíveis no topo: **tema (auto/claro/escuro), idioma (PT-BR/EN) e layout (Auto/PC/Celular)**.

## 6. Componentes
Faixa amarrada (SVG), cartão de técnica (miniatura, kanji, nome), cartão de módulo, player com play na página, linha do tempo de fases, lista de checklist, campo de nota, trilha de navegação (breadcrumb), busca global, menu lateral/gaveta.

## 7. Acessibilidade
Navegação completa por teclado, foco visível de 2 px no acento, *skip link*, contraste AA (corpo ≥ 4,5:1; texto grande ≥ 3:1), alvos de toque ≥ 44 px, `lang` correto em trechos em japonês, `prefers-reduced-motion` e `prefers-color-scheme` respeitados, legendas dos vídeos quando houver.

## 8. Fora do escopo
Contas e login (o site é estático, no GitHub Pages: progresso e notas ficam no aparelho), gravação de vídeos próprios e marcação de tempo por IA sem fonte.

## 9. Implementação
- Tokens e fontes: `site/assets/tokens.css` e `site/assets/fonts/` (Inter e Fraunces, SIL OFL, hospedadas no site). O kanji usa a serifa japonesa do sistema.
- Preferências (tema, idioma, layout): `site/assets/prefs.js` e `prefs.css`.
- Aplicado à página inicial e ao explorador. O livro e o app mantêm seus visuais próprios, com os mesmos controles de preferência.
- Aula (`#/judo/tecnica/<técnica>`): player, fases da técnica, checklist e anotações salvos no aparelho. Marcadores de tempo: pendência interna, ver `source/portal/PENDENCIAS.md`.
