"""Gera dashboards de exame de faixa (Judo e BJJ) no vault e no projeto, com imagens renderizadas dos PDFs baixados.
Fonte dos dados: CBJ Regulamento de Outorga de Faixas 2023 (Art. 6) e IBJJF General System of Graduation (jun/2026).
Nada e inventado: cada item cita a pagina do PDF; o que o documento nao traz vira INFORMACAO AUSENTE."""
import pathlib, shutil, datetime, pymupdf

P = pathlib.Path(r"D:\Claude\Judo_BJJ")
V = pathlib.Path(r"D:\Obsidian\Dominios\Judo_BJJ")
HOJE = datetime.date.today().isoformat()
CBJ = P / "judo/00_geral_regras_IJF_CBJ/fontes_pdf/CBJ_Regulamento_Outorga_de_Faixas_2023.pdf"
IB = P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/IBJJF_20260611_IBJJF_Graduacao_EN.pdf"
POSTER = P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/IBJJF_2026_InfoPoster_Belts_EN.pdf"
JD = V / "Judô/Orientações de exame/Exames de faixas"
BD = V / "BJJ/Orientações de exame/Exames de faixas"
ROT = "FATO EXTRAÍDO"


def render(pdf, pages, prefix, destdir):
    (destdir / "_img").mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf); out = []
    for p in pages:
        f = destdir / "_img" / f"{prefix}_p{p:02d}.png"
        if not f.exists():
            doc[p - 1].get_pixmap(matrix=pymupdf.Matrix(1.3, 1.3)).save(f)
        out.append((p, f.name))
    return out


def embeds(imgs, fonte):
    return "\n\n".join(f"![[_img/{n}]]\n*Fonte: {fonte}, p. {p} (imagem renderizada do PDF baixado).*" for p, n in imgs)


def tabela(rows, cab=("Categoria", "O que é cobrado", "Δ vs. faixa anterior")):
    t = "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n"
    for r in rows: t += "| " + " | ".join(r) + " |\n"
    return t


# ---------------- JUDO ----------------
CATS = ["Reverência e queda (Rei/Ukemi)", "Projeção (Nage waza)", "Imobilização (Osae komi waza)", "Estrangulamento (Shime waza)",
        "Chave de cotovelo (Kansetsu waza)", "Viradas/saídas/defesas no solo", "Sequências (Renraku) e contragolpes (Kaeshi)",
        "Fundamentos de aplicação (Kuzushi/Kumi kata/posturas/deslocamentos)", "Vocabulário", "Histórico e princípio do Judô", "Kata", "Provas teóricas", "Provas práticas/didática/arbitragem"]
J = [  # id, titulo, de, para, kyu, pags, idade, interstício, cats(dict), contagens
 ("01", "Branca para Branca-Cinza", "Branca", "Branca/Cinza", "11º Kyû", [7, 12], "4 anos", "3 meses como Faixa Branca", {
   CATS[0]: ["Saudação em pé (Ritsu rei) e ajoelhado (Za rei)", "Ukemi para trás (Ushiro ukemi) e lateral (Yoko ukemi), executados deitado"],
   CATS[1]: ["1 técnica (integrante do 1º Kyô)"], CATS[2]: ["1 técnica"], CATS[8]: ["Sensei (professor)"]},
  dict(nage=1, osae=1)),
 ("02", "Branca-Cinza para Cinza", "Branca/Cinza", "Cinza", "10º Kyû", [7, 12], "5 anos", "3 meses como Faixa Branca/Cinza", {
   CATS[0]: ["Yoko ukemi a partir da posição agachada, em pé e para frente com rolamento (Zempô kaiten / Maemawari ukemi)"],
   CATS[1]: ["2 técnicas (1º Kyô)"], CATS[2]: ["2 técnicas"], CATS[8]: ["Contar até 10 em japonês; tatami; judogi"], CATS[9]: ["Criador do Judô: Jigoro Kano"]},
  dict(nage=2, osae=2)),
 ("03", "Cinza para Cinza-Azul", "Cinza", "Cinza/Azul", "9º Kyû", [7, 12], "6 anos", "6 meses como Faixa Cinza", {
   CATS[0]: ["Os três tipos de amortecimento de queda (Ukemi) em movimento"], CATS[7]: ["Formas de pegar no judogi (Kumi kata)"],
   CATS[1]: ["3 técnicas (1º Kyô)"], CATS[2]: ["3 técnicas"], CATS[8]: ["Mate (parar), Hajime (começar), Sore-made (terminou), Sonomama (não se mova), Kiotsuke (atenção)"],
   CATS[9]: ["Primeira escola de Judô: Kodokan"]}, dict(nage=3, osae=3)),
 ("04", "Cinza-Azul para Azul", "Cinza/Azul", "Azul", "8º Kyû", [7, 12, 13], "7 anos", "6 meses como Faixa Cinza/Azul", {
   CATS[7]: ["Formas de desequilíbrio (Kuzushi)"], CATS[6]: ["1 sequência de golpes (Renraku waza/Renraku henka waza)"],
   CATS[1]: ["4 técnicas (1º Kyô)"], CATS[2]: ["3 técnicas"], CATS[5]: ["2 viradas, com Uke em decúbito ventral"],
   CATS[8]: ["Judogi, Shitabaki (calça), Uwagi (casaco), Ôbi (faixa), Zoori (chinelo); amarrar corretamente a faixa"],
   CATS[9]: ["Fundação do Kodokan: maio de 1882", "Arte que originou o Judô: Ju jutsu", "Princípio: \"Quem teme perder já está vencido.\""]},
  dict(nage=4, osae=3, renraku=1, viradas=2)),
 ("05", "Azul para Azul-Amarela", "Azul", "Azul/Amarela", "7º Kyû", [7, 13], "8 anos", "6 meses como Faixa Azul", {
   CATS[7]: ["Posturas (Shisei): Shizen hontai, Migi/Hidari shizentai, Jigo hontai, Migi/Hidari jigotai", "Ordem das faixas (Kyû, Yûdansha, Kôdansha, graus superiores)"],
   CATS[6]: ["2 sequências (Renraku)", "1 contragolpe (Kaeshi waza)"], CATS[1]: ["5 técnicas (1º Kyô)"], CATS[2]: ["4 técnicas"], CATS[5]: ["2 viradas, com Uke em decúbito ventral"],
   CATS[8]: ["Uchikomi, Randori, Shiai, Dojô, Shiaijô"], CATS[9]: ["Nascimento de Jigoro Kano: 28/10/1860, Hyogo", "Princípio: \"Conhecer-se é dominar-se, dominar-se é triunfar.\""]},
  dict(nage=5, osae=4, renraku=2, kaeshi=1, viradas=2)),
 ("06", "Azul-Amarela para Amarela", "Azul/Amarela", "Amarela", "6º Kyû", [7, 14], "9 anos", "6 meses como Faixa Azul/Amarela", {
   CATS[6]: ["3 sequências (Renraku)", "2 contragolpes (Kaeshi)"], CATS[1]: ["6 técnicas (1º Kyô)"], CATS[2]: ["5 técnicas"], CATS[5]: ["3 viradas, com Uke em decúbito ventral", "Defesa (Fusegi) com as pernas em Katame waza"],
   CATS[7]: ["Deslocamentos (Shintai): Ayumi ashi e Tsugi ashi"], CATS[8]: ["Tori (judoca ativo) e Uke (passivo)"],
   CATS[9]: ["Morte de Jigoro Kano: 04/05/1938", "Princípio: \"O judoca não se aperfeiçoa para lutar, luta para se aperfeiçoar.\""]},
  dict(nage=6, osae=5, renraku=3, kaeshi=2, viradas=3)),
 ("07", "Amarela para Amarela-Laranja", "Amarela", "Amarela/Laranja", "5º Kyû", [7, 14], "10 anos completos", "1 ano completo como Faixa Amarela", {
   CATS[6]: ["4 sequências (Renraku)", "3 contragolpes (Kaeshi)"], CATS[1]: ["Todas as técnicas do 1º Kyô"], CATS[2]: ["6 técnicas"], CATS[5]: ["4 viradas, com Uke em decúbito ventral", "Defesas (Fusegi) de técnicas em pé (Tachi waza)"],
   CATS[7]: ["Movimentos rotatórios do corpo/esquiva (Tai sabaki)"], CATS[8]: ["Significado de Judô (Ju = suavidade; Dô = caminho)"],
   CATS[9]: ["1º Campeonato Brasileiro de Judô: 1954", "Princípios: Seiryoku zenyô e Jita kyôei"]}, dict(nage="1º Kyô (todas)", osae=6, renraku=4, kaeshi=3, viradas=4)),
 ("08", "Amarela-Laranja para Laranja", "Amarela/Laranja", "Laranja", "4º Kyû", [7, 14, 15], "11 anos completos", "1 ano completo como Faixa Amarela/Laranja", {
   CATS[6]: ["5 sequências (Renraku)", "4 contragolpes (Kaeshi)"], CATS[1]: ["Todas as técnicas do 2º Kyô"], CATS[2]: ["7 técnicas"], CATS[5]: ["5 viradas, com Uke em decúbito ventral", "Escapadas (Nogare) em Katame waza"],
   CATS[7]: ["Fases de aplicação: desequilíbrio (Kuzushi, 8 tipos), preparação (Tsukuri) e execução (Kake)"], CATS[8]: ["Seguir sugestão da Comissão Estadual de Graduação"],
   CATS[9]: ["Judô nos Jogos Olímpicos: Tóquio 1964 (não oficial) e Munique 1972 (oficial)", "Princípio: só se aproxima da perfeição quem a procura com constância, sabedoria e humildade"]},
  dict(nage="2º Kyô (todas)", osae=7, renraku=5, kaeshi=4, viradas=5)),
 ("09", "Laranja para Verde", "Laranja", "Verde", "3º Kyû", [7, 15], "12 anos completos", "1 ano completo como Faixa Laranja e 1 ano de registro na Plataforma Zempo", {
   CATS[6]: ["6 sequências (Renraku)", "5 contragolpes (Kaeshi)"], CATS[1]: ["Todas as técnicas do 3º Kyô"], CATS[2]: ["8 técnicas"], CATS[5]: ["6 viradas/saídas (Nogare) em Katame waza", "1 passagem de guarda de pernas em Katame waza"],
   CATS[10]: ["Grupo de Te waza do Nage no Kata"], CATS[8]: ["A ser sugerido pela Comissão Estadual de Graus"],
   CATS[9]: ["1º Campeonato Mundial: 1956, Japão; Mundiais no Brasil: 1965, 2007 e 2013 (Rio de Janeiro)", "Formas de prática: Randori, Kata, Shiai", "Princípio: a única vitória que perdura é a conquistada sobre a própria ignorância"]},
  dict(nage="3º Kyô (todas)", osae=8, renraku=6, kaeshi=5, viradas=6)),
 ("10", "Verde para Roxa", "Verde", "Roxa", "2º Kyû", [7, 15, 16], "13 anos completos", "1 ano completo como Faixa Verde e 2 anos de registro na Plataforma Zempo", {
   CATS[6]: ["7 sequências (Renraku)", "6 contragolpes (Kaeshi)"], CATS[1]: ["Todas as técnicas do 4º Kyô"], CATS[2]: ["9 técnicas"], CATS[3]: ["2 técnicas"], CATS[4]: ["2 técnicas"],
   CATS[5]: ["4 viradas, com Uke em decúbito ventral", "2 passagens de guarda de pernas com finalização (Katame waza)"], CATS[10]: ["Grupos de Koshi waza do Nage no Kata"],
   CATS[8]: ["A ser sugerido pela Comissão Estadual de Graus"], CATS[9]: ["Classificação das técnicas do Judô (Nage waza: Tachi waza [Te, Koshi, Ashi], Sutemi waza [Masutemi, Yokosutemi]; Katame waza: Osae komi, Shime, Kansetsu, Atemi)", "Princípio: \"Nunca te orgulhes de haver vencido um adversário...\""]},
  dict(nage="4º Kyô (todas)", osae=9, renraku=7, kaeshi=6, shime=2, kansetsu=2, viradas=4)),
 ("11", "Roxa para Marrom", "Roxa", "Marrom", "1º Kyû", [7, 16], "14 anos completos", "1 ano completo como Faixa Roxa e 3 anos de registro na Plataforma Zempo", {
   CATS[6]: ["8 sequências (Renraku)", "7 contragolpes (Kaeshi)"], CATS[1]: ["Todas as técnicas do 5º Kyô"], CATS[3]: ["4 técnicas"], CATS[4]: ["4 técnicas"],
   CATS[5]: ["6 viradas, com Uke em decúbito ventral", "Defesa em guarda de pernas em Katame waza, com finalizações"], CATS[10]: ["Grupo de Ashi waza do Nage no Kata"],
   CATS[8]: ["A ser sugerido pela Comissão Estadual de Graus"], CATS[9]: ["Histórico e princípio: a ser sugerido pela Comissão Estadual de Graus", "Conceito de Kôdansha"],
   CATS[12]: ["Noções básicas de arbitragem (voz de comando, gestos e avaliação)", "Atuação como oficial de mesa em competições"]},
  dict(nage="5º Kyô (todas)", renraku=8, kaeshi=7, shime=4, kansetsu=4, viradas=6)),
]
DANS = [  # id, titulo, grad, idade, inter, pontos, teoricas, praticas, extra
 ("12", "Marrom para Preta 1º Dan", "1º Dan (Sho dan)", [16, 17], "16 anos completos até a data do exame estadual", "2 anos como Faixa Marrom (1 ano se maior de 20 anos) e 4 anos de registro no Sistema Zempo", "700 pontos nos 2 últimos anos",
  ["Histórico, filosofia, ética e disciplina", "Atualidades", "Divisão e classificação das técnicas", "Ortografia do vocabulário técnico", "Descrição escrita sobre Nage no Kata"],
  ["Nage no Kata completo, como Tori", "Nage waza", "Renraku waza/Renraku henka waza", "Kaeshi waza", "Katame waza", "Apresentação prática de arbitragem"]),
 ("13", "Preta 1º para 2º Dan", "2º Dan (Ni dan)", [17], "20 anos completos", "4 anos como 1º Dan e mínimo de 5 anos de registro no Zempo", "750 pontos nos 4 últimos anos",
  ["Descrição escrita sobre Katame no Kata", "Histórico, filosofia, ética e disciplina", "Atualidades", "Divisão e classificação das técnicas", "Ortografia do vocabulário técnico", "Conhecimento de arbitragem"],
  ["Katame no Kata completo, como Tori", "Nage no Kata (uma série por sorteio, como Tori)", "Nage waza", "Renraku henka waza", "Kaeshi waza", "Katame waza", "Conhecimentos didáticos e pedagógicos: ensino de Nage no Kata, Katame no Kata e fundamentos de Judô"]),
 ("14", "Preta 2º para 3º Dan", "3º Dan (San dan)", [18], "25 anos", "5 anos como 2º Dan e mínimo de 6 anos de registro no Zempo", "1.200 pontos nos 5 últimos anos",
  ["Histórico, filosofia, ética e disciplina", "Divisão e classificação das técnicas", "Ortografia do vocabulário técnico", "Descrição escrita sobre Ju no Kata", "Noções básicas de organização de eventos", "Conhecimento de arbitragem"],
  ["Ju no Kata completo, como Tori", "Katame no Kata (um grupo por sorteio, como Tori)", "Conhecimentos didáticos e pedagógicos: Nage no Kata, Katame no Kata, Ju no Kata e fundamentos de Judô"]),
 ("15", "Preta 3º para 4º Dan", "4º Dan (Yon dan)", [18], "30 anos", "5 anos como 3º Dan e mínimo de 7 anos de registro no Zempo", "1.500 pontos nos 5 últimos anos",
  ["Histórico, filosofia, ética e disciplina", "Divisão e classificação das técnicas", "Ortografia do vocabulário técnico", "Descrição escrita sobre Kime no Kata", "Apresentação de organização de eventos", "Conhecimento de arbitragem"],
  ["Kime no Kata completo, como Tori", "Ju no Kata (um grupo por sorteio, como Tori)", "Conhecimentos didáticos e pedagógicos: Nage no Kata, Katame no Kata, Ju no Kata, Kime no Kata e fundamentos de Judô"]),
 ("16", "Preta 4º para 5º Dan", "5º Dan (Go dan)", [19], "36 anos", "6 anos como 4º Dan, mínimo de 8 anos de registro no Zempo e 18 anos de experiência judoística desde o Sho dan", "2.000 pontos nos 6 últimos anos",
  ["Histórico, filosofia, ética e disciplina", "Divisão e classificação das técnicas", "Ortografia do vocabulário técnico", "Descrição escrita sobre Kodokan Goshin jutsu", "Conhecimento de arbitragem"],
  ["Kodokan Goshin jutsu completo, como Tori", "Kime no Kata (um grupo por sorteio, como Tori)", "Conhecimentos didáticos e pedagógicos: Nage no Kata, Katame no Kata, Ju no Kata, Kime no Kata, Kodokan Goshin jutsu e fundamentos de Judô", "Atividades vivenciadas: experiência no ensino de Judô; cursos pedagógicos (participante e/ou ministrante)"]),
]
SRC_J = "CBJ — Regulamento Nacional para Exame e Outorga de Faixas e Graus 2023 (Conselho Nacional de Graus)"
URL_J = "https://cbj.com.br/pt/governanca/transparencia/regulamentos-esportivos"
NOTA_J = ("> [!warning] Limites do documento\n> **INFORMAÇÃO AUSENTE neste regulamento:** a lista das técnicas de cada Kyô (Gokyo) e o vocabulário/histórico "
          "\"a ser sugerido pela Comissão Estadual\". O Art. 6º, §1º diz que as técnicas solicitadas são definidas pela Comissão Estadual de Graduação, e o §2º que o conteúdo da graduação anterior também é exigido (programa cumulativo). "
          "Consulte o programa da sua federação estadual.")


def fm(extra):
    return "---\n" + "\n".join(f"{k}: {v}" for k, v in extra.items()) + "\n---\n\n"


def judo():
    JD.mkdir(parents=True, exist_ok=True)
    prev = {}; linhas = []; geral = render(CBJ, [4, 5, 6, 7, 8, 9], "CBJ_Outorga2023", JD)
    for (i, tit, de, para, kyu, pags, idade, inter, cats, cnt) in J:
        imgs = render(CBJ, pags, "CBJ_Outorga2023", JD)
        rows = []
        for c in CATS:
            if c in cats:
                rows.append([c, "<br>".join(cats[c]), ""])
        delta = []
        for k, rot in [("nage", "Nage waza"), ("osae", "Osae komi"), ("renraku", "Renraku"), ("kaeshi", "Kaeshi"), ("shime", "Shime"), ("kansetsu", "Kansetsu"), ("viradas", "Viradas")]:
            if k in cnt:
                a = prev.get(k); b = cnt[k]
                if isinstance(b, int) and isinstance(a, int) and b < a: d = f"{rot}: {a} → {b} (o texto muda o critério; não comparável — conferir na imagem)"
                elif isinstance(b, int) and isinstance(a, int): d = f"{rot}: {a} → {b} (+{b - a})"
                elif a is None: d = f"{rot}: novo ({b})"
                else: d = f"{rot}: {a} → {b}"
                delta.append(d)
        prev.update(cnt)
        nome = f"{i} {tit} ({kyu})"
        corpo = fm({"titulo": f'"{nome}"', "tipo": "dashboard_exame_faixa", "modalidade": "judo", "faixa_de": f'"{de}"', "faixa_para": f'"{para}"', "graduacao": f'"{kyu}"',
                    "fonte": f'"{SRC_J}"', "paginas_pdf": str(pags), "rotulo": ROT, "confianca_extracao": "alta (texto direto do PDF; conferir na imagem)", "status_revisao_humana": "pendente", "acesso_em": HOJE,
                    "tags": "[judo_bjj, judo, exame_de_faixa, dashboard]"})
        corpo += f"# {nome}\n\n> [!info] Resumo\n> **{de} → {para}** · {kyu} · idade mínima **{idade}** · interstício mínimo **{inter}**\n> Rótulo: {ROT} (CBJ 2023, Art. 6º, p. {', '.join(map(str, pags))}). Programa **cumulativo**.\n\n"
        corpo += "## O que será cobrado, por categoria\n\n" + tabela([[r[0], r[1], ""] for r in rows], ("Categoria", "Exigência")).replace("| Categoria | Exigência |\n|---|---|", "| Categoria | Exigência |\n|---|---|") + "\n"
        corpo = corpo.replace("|  |\n", "|\n")
        if delta: corpo += "## Evolução em relação à faixa anterior (contagens)\n\n" + "\n".join(f"- {d}" for d in delta) + "\n\n"
        corpo += NOTA_J + "\n\n## Ilustração (páginas do próprio regulamento)\n\n" + embeds(imgs, SRC_J) + f"\n\n## Fonte\n\n{SRC_J} · [[Dominios/Judo_BJJ/fontes_livros/CBJ_Regulamento_Outorga_de_Faixas_2023.pdf]] · {URL_J}\n\nVoltar: [[Dashboard Judô]]\n"
        (JD / f"{nome}.md").write_text(corpo, encoding="utf-8")
        linhas.append((nome, de, para, kyu, idade, inter, cnt))
    dl = []
    for (i, tit, grad, pags, idade, inter, pts, teo, pra) in DANS:
        imgs = render(CBJ, pags, "CBJ_Outorga2023", JD)
        nome = f"{i} {tit}"
        corpo = fm({"titulo": f'"{nome}"', "tipo": "dashboard_exame_faixa", "modalidade": "judo", "graduacao": f'"{grad}"', "fonte": f'"{SRC_J}"', "paginas_pdf": str(pags), "rotulo": ROT,
                    "confianca_extracao": "alta (texto direto do PDF; conferir na imagem)", "status_revisao_humana": "pendente", "acesso_em": HOJE, "tags": "[judo_bjj, judo, exame_de_faixa, dan, dashboard]"})
        corpo += f"# {nome}\n\n> [!info] Resumo\n> **{grad}** · idade mínima **{idade}** · **{pts}**\n> Rótulo: {ROT} (CBJ 2023, Art. 6º, p. {', '.join(map(str, pags))}). Exame estadual, homologação pela CBJ; 1 exame de yudansha por ano.\n\n"
        corpo += "## Elegibilidade\n\n" + tabela([["Idade mínima", idade], ["Interstício/registro", inter], ["Pontuação acumulada", pts + " (tabelas de pontos: ver [[Pontuação para graduações superiores]])"], ["Condições gerais (Art. 5º)", "idoneidade moral; conhecimento teórico e prático; membro ativo em federação reconhecida; em dia com a CBJ; nacionalidade/residência; registro válido de 2 anos para 1º Dan em diante"]], ("Item", "Exigência"))
        corpo += "\n## Provas teóricas\n\n" + "\n".join(f"- {x}" for x in teo) + "\n\n## Provas práticas\n\n" + "\n".join(f"- {x}" for x in pra) + "\n\n" + NOTA_J
        corpo += "\n\n## Ilustração (páginas do próprio regulamento)\n\n" + embeds(imgs, SRC_J) + f"\n\n## Fonte\n\n{SRC_J} · [[Dominios/Judo_BJJ/fontes_livros/CBJ_Regulamento_Outorga_de_Faixas_2023.pdf]] · {URL_J}\n\nVoltar: [[Dashboard Judô]]\n"
        (JD / f"{nome}.md").write_text(corpo, encoding="utf-8")
        dl.append((nome, grad, idade, pts))
    # graus superiores + pontos
    sup = render(CBJ, [8, 19, 20], "CBJ_Outorga2023", JD)
    nome_s = "17 Graus superiores (6º ao 10º Dan)"
    (JD / f"{nome_s}.md").write_text(fm({"titulo": f'"{nome_s}"', "tipo": "dashboard_exame_faixa", "modalidade": "judo", "rotulo": ROT, "fonte": f'"{SRC_J}"', "paginas_pdf": "[8, 10, 11, 19, 20]", "status_revisao_humana": "pendente", "tags": "[judo_bjj, judo, kodansha, dashboard]"}) +
        f"# {nome_s}\n\n> [!info] Promoção por merecimento (Kôdansha: 6º e 7º Dan; 8º a 10º: graus superiores). Rótulo: {ROT} (CBJ 2023, Art. 4º e 6º XVII–XIX).\n\n" +
        tabela([["6º Dan (Roku dan)", "44 anos", "25 anos de experiência; ≥6 anos como 5º Dan", "6.300 pontos", "Ensino; cursos/palestras; Ju no Kata (Tori ou Uke)"],
                ["7º Dan (Shiti dan)", "52 anos", "32 anos de experiência; ≥7 anos como 6º Dan", "7.200 pontos", "Ensino; Ju no Kata e Kime no Kata; teoria de Koshiki no Kata; publicações"],
                ["8º Dan (Hati dan)", "59 anos", "39 anos de experiência; ≥7 anos como 7º Dan", "7.200 pontos", "Ensino; Ju, Kime e Kodokan Goshin jutsu; teoria de Itsutsu no Kata; cargos administrativos; publicações"],
                ["9º e 10º Dan", "66 / 74 anos (Tabela 5)", "Interstício 8 anos (Tabela 5)", "—", "Excepcionais; encaminhados à FIJ (10º só por unanimidade do Comitê Executivo da FIJ)"]],
               ("Grau", "Idade mínima", "Tempo", "Pontos", "Atividades/provas")) + "\n" + NOTA_J + "\n\n" + embeds(sup, SRC_J) + "\n\nVoltar: [[Dashboard Judô]]\n", encoding="utf-8")
    pts_imgs = render(CBJ, [21, 22, 23, 24], "CBJ_Outorga2023", JD)
    (JD / "Pontuação para graduações superiores.md").write_text(fm({"titulo": '"Pontuação para graduações superiores"', "tipo": "dashboard_exame_faixa", "modalidade": "judo", "rotulo": ROT, "paginas_pdf": "[21, 22, 23, 24]", "status_revisao_humana": "pendente", "tags": "[judo_bjj, judo, pontos]"}) +
        f"# Pontuação para graduações superiores (Tabelas 1 a 8)\n\n> [!info] Art. 7º CBJ 2023: pontos por competições, atuação em eventos, cargos, escolaridade, arbitragem e publicações. Resultados competitivos contam no máximo 70% dos pontos exigidos (Tabela 1). O período de carência não é reduzido se os pontos forem atingidos antes (§2º).\n\n" +
        embeds(pts_imgs, SRC_J) + "\n\nVoltar: [[Dashboard Judô]]\n", encoding="utf-8")
    # dashboard
    d = fm({"titulo": '"Dashboard Judô"', "tipo": "dashboard_modalidade", "modalidade": "judo", "fonte": f'"{SRC_J}"', "rotulo": ROT, "acesso_em": HOJE, "tags": "[judo_bjj, judo, dashboard]"})
    d += f"# Dashboard Judô — exames de faixa\n\n> [!info] Fonte única nesta versão: {SRC_J}. Cada federação estadual elabora seu próprio programa dentro deste regulamento (Art. 9º). Nota sobre a sequência de faixas: o regulamento intercala faixas de duas cores (ex.: Branca → Branca/Cinza → Cinza); por isso \"Branca para Cinza\" equivale às notas 01 e 02.\n\n"
    d += "## Visão geral (faixas Kyû)\n\n| Nota | De → Para | Graduação | Idade mín. | Interstício | Nage | Osae | Renraku | Kaeshi | Shime | Kansetsu |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
    for (nome, de, para, kyu, idade, inter, cnt) in linhas:
        g = lambda k: str(cnt.get(k, "—"))
        d += f"| [[{nome}]] | {de} → {para} | {kyu} | {idade} | {inter} | {g('nage')} | {g('osae')} | {g('renraku')} | {g('kaeshi')} | {g('shime')} | {g('kansetsu')} |\n"
    d += "\n*Contagens: número de técnicas a demonstrar (Nage: técnicas do Kyô indicado). \"—\" = não exigido nessa faixa no texto.*\n\n## Faixas pretas (Yûdansha)\n\n| Nota | Graduação | Idade mínima | Pontos |\n|---|---|---|---|\n"
    for (nome, grad, idade, pts) in dl: d += f"| [[{nome}]] | {grad} | {idade} | {pts} |\n"
    d += "\n[[17 Graus superiores (6º ao 10º Dan)]] · [[Pontuação para graduações superiores]]\n\n## Progressão das faixas\n\n```mermaid\nflowchart LR\n  A[Branca] --> B[Branca/Cinza 11º] --> C[Cinza 10º] --> D[Cinza/Azul 9º] --> E[Azul 8º] --> F[Azul/Amarela 7º] --> G[Amarela 6º] --> H[Amarela/Laranja 5º] --> I[Laranja 4º] --> J[Verde 3º] --> K[Roxa 2º] --> L[Marrom 1º] --> M[Preta 1º-5º Dan] --> N[Vermelha e branca 6º-8º] --> O[Vermelha 9º-10º]\n```\n\n"
    d += "## Tabelas e contexto do regulamento\n\n" + embeds(geral, SRC_J) + "\n\n## Lacunas e próximos passos\n\n- INFORMAÇÃO AUSENTE: lista de técnicas por Kyô (Gokyo) — buscar em fonte do Kodokan/CBJ; programas das federações estaduais.\n- Cursos de preparação para exame: levantar na etapa seguinte (CBJ: educacaocbj.com.br).\n"
    (V / "Judô" / "Dashboard Judô.md").write_text(d, encoding="utf-8")


# ---------------- BJJ ----------------
SRC_B = "IBJJF — General System of Graduation (junho/2026, v3.x)"
URL_B = "https://ibjjf.com/graduation-system"
NOTA_B = ("> [!warning] Limites do documento\n> **INFORMAÇÃO AUSENTE na IBJJF/CBJJ:** o documento da IBJJF **não traz programa técnico de exame**; o art. 3.2 diz que o tempo para graduar é critério do professor e a IBJJF só reconhece a graduação se cumpridos os mínimos. "
          "**Programa técnico existente: JJIF** (Jiu-Jitsu International Federation), seção abaixo — é outra federação, com exame obrigatório apenas de Azul a Preta; não é regra IBJJF/CBJJ. Associações/academias privadas: ver [[Programas técnicos de BJJ - levantamento]].")
SRC_JJ = "JJIF — Jiu-Jitsu Graduation System (Rules and Technical Department), v11, cópia hospedada pela Jiu-Jitsu Australia"
URL_JJ = "https://jjau.org/wp-content/uploads/2023/02/Graduation-System-Book_v11.pdf"
JJPDF = P / "bjj/00_geral_regras_IBJJF_CBJJ_JJIF/fontes_pdf/JJIF_Jiu-Jitsu_Graduation_System_Book_v11_copia_JJAU.pdf"
CAT_TEC = "Básicas, quedas (takedowns), passagem de guarda, ataques da guarda, raspagens (sweeps), controle lateral, costas, montada, ataques a pernas/pés e defesa pessoal"
JJ = {  # id: (faixa, paginas_tecnicas, pagina_ficha_exame, criterios, opcoes, ficha, aulas)
 "01": ("Azul", [23, 24, 25, 26], 59, "Postura correta; conhecimento básico; pegadas lógicas; equilíbrio; controle do oponente",
        "O examinador pode perguntar sobre a pontuação das técnicas executadas; pode acrescentar treino livre; pode pedir fugas (montada, controle lateral, costas)",
        "Quedas (exceto double e single leg); raspagens; passagem de guarda; defesa pessoal; finalizações da guarda fechada; finalizações da montada",
        "Sugestão de carga: 2 anos, 16 anos, 104 semanas × 3 aulas = **312 aulas**; faixas (graus) sugeridas a cada **63 aulas** (a branca: 21 aulas por grau)"),
 "02": ("Roxa", [27, 28, 29, 30], 58, "Conhecimento das técnicas; explicação clara e lógica; conexão lógica e transições; fluidez dos movimentos",
        "O examinador pede primeiro as técnicas da ficha; o atleta explica em detalhe 2 técnicas escolhidas pelo examinador, 2 escolhidas por ele e 2 sequências escolhidas por ele",
        "Quedas (com controle no solo); raspagens da guarda fechada; raspagens da guarda aberta (spider, lasso, DLR etc.); passagem de guarda; defesa pessoal; finalizações da montada; finalizações da guarda fechada",
        "Sugestão de carga: 1,5 ano, 16 anos, 72 semanas × 4 aulas = **288 aulas**; graus a cada **58 aulas**"),
 "03": ("Marrom", [31, 32, 33, 34, 35, 36], 57, "Conhecimento das técnicas; explicação clara e lógica; conexão lógica e transições; fluidez dos movimentos",
        "O examinador pede primeiro as técnicas da ficha; o atleta explica em detalhe 5 técnicas do programa escolhidas pelo examinador, 2 escolhidas por ele e 5 sequências escolhidas por ele; na defesa pessoal, o examinador pede técnicas de situações diferentes, executadas o mais realisticamente possível",
        "Mesmas categorias da roxa, com mais itens na ficha",
        "Sugestão de carga: 1 ano, 18 anos, 52 semanas × 5 aulas = **260 aulas**; graus a cada **52 aulas**"),
 "04": ("Preta", [37, 38, 39, 40, 41, 42, 43, 44, 45, 46], 56, "Conhecimento das técnicas; explicação clara e lógica; conexão lógica e transições; fluidez dos movimentos",
        "O examinador pede primeiro as técnicas da ficha; o atleta explica em detalhe 10 técnicas do programa escolhidas pelo examinador, 2 escolhidas por ele e 7 sequências escolhidas por ele; na defesa pessoal, situações diferentes, o mais realisticamente possível",
        "Mesmas categorias da marrom, com a maior ficha (10 páginas de técnicas)",
        "Idade mínima sugerida na tabela: 19 anos (JJIF); processo de faixa preta tramitado pelo Comitê de Graduação da JJIF e diploma assinado pelo diretor do comitê"),
}


def jjif_secao(i, destdir):
    if i not in JJ: return ""
    faixa, pags, ficha, crit, opc, fich, aulas = JJ[i]
    imgs = render(JJPDF, pags + [ficha], "JJIF_Grad_v11", destdir)
    t = f"## Programa técnico JJIF — exame de {faixa} (fonte: JJIF, não IBJJF)\n\n> [!info] {ROT} (JJIF Graduation System v11, p. {', '.join(map(str, pags))} e ficha p. {ficha}). O programa é **cumulativo**: a lista de cada faixa repete os itens das anteriores e acrescenta novos (conferir nas imagens). Na JJIF o exame é obrigatório apenas de Azul a Preta.\n\n"
    t += tabela([["Categorias do programa", CAT_TEC], ["Critérios de avaliação", crit], ["Opções adicionais do examinador", opc], ["Seções da ficha de exame", fich], ["Carga mínima sugerida", aulas]], ("Item", "Conteúdo")) + "\n"
    t += "> [!warning] A lista completa de técnicas está nas imagens abaixo (extração de texto mistura colunas). A JJIF afirma que o programa é o mínimo para padronizar o ensino entre federações nacionais.\n\n"
    t += embeds(imgs, SRC_JJ) + f"\n\nFonte: {SRC_JJ} · [[Dominios/Judo_BJJ/fontes_livros/JJIF_Jiu-Jitsu_Graduation_System_Book_v11_copia_JJAU.pdf]] · {URL_JJ}\n\n"
    return t


def bjj():
    BD.mkdir(parents=True, exist_ok=True)
    comuns = render(IB, [4, 5], "IBJJF_Grad2026", BD) + render(POSTER, [1], "IBJJF_Poster2026", BD)
    idad = render(IB, [7, 8], "IBJJF_Grad2026", BD); tempo = render(IB, [9], "IBJJF_Grad2026", BD)
    graus = render(IB, [10], "IBJJF_Grad2026", BD); req = render(IB, [11, 12], "IBJJF_Grad2026", BD)
    kids = render(IB, [14, 15, 16, 17], "IBJJF_Grad2026", BD)
    A = [("01", "Branca para Azul", "Branca", "Azul", "16 anos ou mais (Art. 2.1.2 — Azul)", "Branca: sem tempo mínimo. Azul: 2 anos de permanência na Azul antes da Roxa (ver nota 02); para atletas vindos das faixas infantis: Cinza/Amarela/Laranja → 1 ano; Verde → sem mínimo; Azul Juvenil → sem mínimo; campeão mundial adulto azul → sem mínimo", "Atletas com 16 anos no ano seguem o sistema adulto: Cinza, Amarela e Laranja passam à Azul; Verde pode ir à Azul ou Roxa por decisão do professor (Art. 2.2.3)", idad + tempo),
         ("02", "Azul para Roxa", "Azul", "Roxa", "16 anos ou mais", "2 anos na Azul (1 ano se registrado antes como Cinza/Amarela/Laranja; 0 se registrado como Verde ou Azul Juvenil; 0 para campeão mundial adulto azul). Atletas de 16–17 anos só avançam à Marrom na divisão Adulto", "—", idad + tempo),
         ("03", "Roxa para Marrom", "Roxa", "Marrom", "18 anos ou mais (Marrom)", "1,5 ano na Roxa (1 ano se vinha de Azul Juvenil; 0 se Laranja/Verde e Azul Juvenil, Roxa Juvenil ou campeão mundial adulto roxo)", "—", idad + tempo),
         ("04", "Marrom para Preta", "Marrom", "Preta", "18 anos ou mais (Preta); aos 18 somente quem foi campeão mundial adulto na Marrom", "1 ano na Marrom (0 se campeão mundial adulto marrom)", "Requisitos de certificado de faixa preta (Art. 5): filiação IBJJF; não ter graduação provisória; certificado de primeiros socorros/RCP; certificado de Programa de Árbitros, Seminário ou Webinar de Regras (últimos 12 meses). A faixa preta só pode ser assinada por faixa preta com ≥2 graus certificados pela IBJJF (Art. 6.2)", idad + tempo + req)]
    notas = []
    for (i, tit, de, para, idade, tempo_t, extra, imgs) in A:
        nome = f"{i} {tit}"
        c = fm({"titulo": f'"{nome}"', "tipo": "dashboard_exame_faixa", "modalidade": "bjj", "faixa_de": de, "faixa_para": para, "fonte": f'"{SRC_B}"', "rotulo": ROT, "confianca_extracao": "alta (texto direto do PDF; conferir na imagem)", "status_revisao_humana": "pendente", "acesso_em": HOJE, "tags": "[judo_bjj, bjj, exame_de_faixa, dashboard]"})
        c += f"# {nome}\n\n> [!info] Resumo\n> **{de} → {para}** · idade mínima: **{idade}** · rótulo: {ROT} (IBJJF, Arts. 2, 3, 5 e 6)\n\n## O que o documento oficial exige\n\n"
        c += tabela([["Idade mínima (Art. 2)", idade], ["Tempo mínimo na faixa (Art. 3)", tempo_t], ["Registro/professor (Art. 6)", "O pedido de filiação das faixas Branca a Marrom deve ser assinado/aprovado por professor faixa preta filiado à IBJJF"], ["Notas", extra], ["Graus (Art. 4)", "Branca a Marrom: 4 graus (adoção livre pelo professor até a Marrom)"], ["Conteúdo técnico do exame", "IBJJF/CBJJ: INFORMAÇÃO AUSENTE. JJIF: programa publicado (seção abaixo)"]], ("Categoria", "Exigência"))
        c += "\n" + NOTA_B + "\n\n" + jjif_secao(i, BD) + "## Ilustração (páginas do próprio documento IBJJF)\n\n" + embeds(imgs + comuns, SRC_B) + f"\n\n## Fonte\n\n{SRC_B} · [[Dominios/Judo_BJJ/fontes_livros/IBJJF_20260611_IBJJF_Graduacao_EN.pdf]] · {URL_B}\n\nVoltar: [[Dashboard BJJ]]\n"
        (BD / f"{nome}.md").write_text(c, encoding="utf-8"); notas.append((nome, de, para, idade))
    nome = "05 Preta - graus 1 a 6"
    (BD / f"{nome}.md").write_text(fm({"titulo": f'"{nome}"', "tipo": "dashboard_exame_faixa", "modalidade": "bjj", "rotulo": ROT, "fonte": f'"{SRC_B}"', "status_revisao_humana": "pendente", "tags": "[judo_bjj, bjj, graus, dashboard]"}) +
        f"# {nome}\n\n> [!info] Faixa preta: faixa única com **6 graus** (Art. 4.1.2). Rótulo: {ROT}. O 1º grau pode ser pedido após 3 anos de atividade comprovada.\n\n" +
        tabela([["1º grau", "3 anos de atividade comprovada na Preta"], ["2º grau", "3 anos desde o grau anterior, ou 6 anos de atividade"], ["3º grau", "3 anos desde o anterior, ou 9 anos"], ["4º grau", "5 anos desde o anterior, ou 14 anos"], ["5º grau", "5 anos desde o anterior, ou 19 anos"], ["6º grau", "5 anos desde o anterior, ou 24 anos"]], ("Grau", "Tempo mínimo (IBJJF)")) +
        "\n**Como provar atividade (Art. 4.2.1):** filiação ativa; academia registrada (professor titular/adicional); aprovação de filiações de alunos; certificação anterior; títulos em campeonatos IBJJF; certificados do Programa de Árbitros e Curso de Regras; reconhecimento de contribuição significativa.\n\n" + NOTA_B + "\n\n" + embeds(graus + req, SRC_B) + "\n\nVoltar: [[Dashboard BJJ]]\n", encoding="utf-8")
    nome2 = "06 Graus de mestre (7º ao 10º)"
    (BD / f"{nome2}.md").write_text(fm({"titulo": f'"{nome2}"', "tipo": "dashboard_exame_faixa", "modalidade": "bjj", "rotulo": ROT, "fonte": f'"{SRC_B}"', "status_revisao_humana": "pendente", "tags": "[judo_bjj, bjj, mestres, dashboard]"}) +
        f"# {nome2}\n\n> [!info] Rótulo: {ROT} (IBJJF Arts. 1, 2, 3.1.4 e 4.1.5).\n\n" +
        tabela([["7º grau — Vermelha e Preta", "49 anos (Master)", "7 anos desde o anterior ou 31 anos de atividade na Preta"], ["8º grau — Vermelha e Branca", "56 anos", "7 anos desde o anterior ou 38 anos"], ["9º grau — Vermelha", "66 anos", "10 anos desde o anterior ou 48 anos"], ["10º grau — Vermelha", "—", "Concedido apenas aos pioneiros do BJJ: Carlos, Oswaldo, George, Gastão e Hélio (texto do documento)"]], ("Grau/faixa", "Idade mínima", "Tempo")) +
        "\n" + embeds(render(IB, [6], "IBJJF_Grad2026", BD) + idad[:1], SRC_B) + "\n\nVoltar: [[Dashboard BJJ]]\n", encoding="utf-8")
    nome3 = "00 Infantil 4 a 15 anos (grupos de cor)"
    (BD / f"{nome3}.md").write_text(fm({"titulo": f'"{nome3}"', "tipo": "dashboard_exame_faixa", "modalidade": "bjj", "rotulo": ROT, "fonte": f'"{SRC_B}"', "status_revisao_humana": "pendente", "tags": "[judo_bjj, bjj, infantil, dashboard]"}) +
        f"# {nome3}\n\n> [!info] Rótulo: {ROT} (IBJJF Arts. 1.1, 2.1.1, 3.1.1, 4.1.1 e Anexo I). **Sem tempo mínimo por faixa** para 4–15 anos; a divisão em graus é sugestão da IBJJF.\n\n" +
        "## Sequência de faixas (4 a 15 anos)\n\nBranca → Cinza e Branca → Cinza → Cinza e Preta → Amarela e Branca → Amarela → Amarela e Preta → Laranja e Branca → Laranja → Laranja e Preta → Verde e Branca → Verde → Verde e Preta\n\n" +
        tabela([["Grupo Cinza (Cinza/Branca, Cinza, Cinza/Preta)", "4 a 15 anos (Mighty-Mite 1 a Teen 3)"], ["Grupo Amarelo", "7 a 15 anos (Pee-Wee 1 a Teen 3)"], ["Grupo Laranja", "10 a 15 anos (Junior 1 a Teen 3)"], ["Grupo Verde", "13 a 15 anos (Teen 1 a Teen 3)"], ["Branca", "qualquer idade"]], ("Grupo", "Idade permitida")) +
        "\n**Sistemas de graus sugeridos (Anexo I):** trimestral (3 graus por faixa, o 4º leva à próxima cor), quadrimestral (2 graus; o 3º leva à próxima) e mensal (11 graus; o 12º leva à próxima). **Aos 16 anos:** Cinza, Amarela e Laranja passam à Azul; Verde vai à Azul ou Roxa por decisão do professor; Branca pode permanecer.\n\n" + NOTA_B + "\n\n" + embeds(render(IB, [4], "IBJJF_Grad2026", BD) + kids, SRC_B) + "\n\nVoltar: [[Dashboard BJJ]]\n", encoding="utf-8")
    n7 = "07 Programa JJIF - Branca, infantil, graus e processo"
    (BD / f"{n7}.md").write_text(fm({"titulo": f'"{n7}"', "tipo": "dashboard_exame_faixa", "modalidade": "bjj", "rotulo": ROT, "fonte": f'"{SRC_JJ}"', "status_revisao_humana": "pendente", "tags": "[judo_bjj, bjj, jjif, dashboard]"}) +
        f"# {n7}\n\n> [!info] {ROT} (JJIF Graduation System v11, p. 4–8, 9–19, 21–22, 61–65). Documento da **JJIF**, não da IBJJF/CBJJ.\n\n" +
        tabela([["Exame obrigatório", "Somente Azul, Roxa, Marrom e Preta; faixas infantis **sem exame oficial** (pedido ao representante da federação nacional, que confere idade e registro no SPORTS ID)"],
                ["Quem examina", "Representante local de estilo (Local Style Representative), faixa preta 2º grau no mínimo, aprovado pela JJIF; pode delegar examinadores. Atletas registrados no SPORTS ID; pagam taxa à federação nacional e à JJIF (diploma)"],
                ["Faixa preta", "Evento aberto no SPORTS DATA pelo diretor do Comitê de Graduação da JJIF; diploma assinado pelo diretor e enviado pela sede da JJIF"],
                ["Faixa branca (técnicas)", "Programa de entrada (p. 21–22): quedas, passagem, ataques da guarda, raspagens, controle lateral, costas, montada, ataques a pernas e defesa pessoal; **sem exame**"],
                ["Infantil (Cinza, Amarela, Laranja, Verde)", "Programas técnicos nas p. 10–19; sistema de graus por aulas: 21 aulas por grau (branca e cinza), 32 aulas (amarela, laranja, verde)"],
                ["Sistema de graus (stripes)", "Sugestão da JJIF; o uso e a quantidade de aulas pertencem à organização local e aos treinadores"],
                ["Defesa pessoal", "Programa básico com 43 aulas sugeridas (p. 48–50); exclui defesas contra faca e arma de fogo"],
                ["Valores", "Os valores do esporte (benevolência, caráter, coragem, cortesia etc.) devem ser reforçados na mensagem final da aula (p. 66–70)"]], ("Item", "Conteúdo")) +
        "\n" + NOTA_B + "\n\n" + embeds(render(JJPDF, [6, 7, 8, 10, 11, 21, 22, 61, 62, 63, 64, 65], "JJIF_Grad_v11", BD), SRC_JJ) + f"\n\nFonte: {SRC_JJ} · [[Dominios/Judo_BJJ/fontes_livros/JJIF_Jiu-Jitsu_Graduation_System_Book_v11_copia_JJAU.pdf]] · {URL_JJ}\n\nVoltar: [[Dashboard BJJ]]\n", encoding="utf-8")
    d = fm({"titulo": '"Dashboard BJJ"', "tipo": "dashboard_modalidade", "modalidade": "bjj", "fonte": f'"{SRC_B}"', "rotulo": ROT, "acesso_em": HOJE, "tags": "[judo_bjj, bjj, dashboard]"})
    d += f"# Dashboard BJJ — exames de faixa\n\n> [!info] Fonte: {SRC_B} ([[Dominios/Judo_BJJ/fontes_livros/IBJJF_20260611_IBJJF_Graduacao_EN.pdf]]). A CBJJ publica o mesmo sistema (cbjj.com.br/graduation-system). Faixas adultas: Branca, Azul, Roxa, Marrom, Preta (6 graus), Vermelha e Preta, Vermelha e Branca, Vermelha.\n\n"
    d += "## Visão geral\n\n| Nota | De → Para | Idade mínima | Tempo mínimo | Conteúdo técnico |\n|---|---|---|---|---|\n"
    resumo = {"01": "sem mínimo na Branca", "02": "2 anos na Azul (casos especiais)", "03": "1,5 ano na Roxa (casos especiais)", "04": "1 ano na Marrom (campeão mundial: 0)"}
    for (nome, de, para, idade) in notas:
        d += f"| [[{nome}]] | {de} → {para} | {idade.split(' (')[0]} | {resumo[nome[:2]]} | IBJJF: ausente · JJIF: publicado |\n"
    d += f"| [[07 Programa JJIF - Branca, infantil, graus e processo]] | Programa JJIF (branca, infantil, processo) | por faixa | mínimos JJIF | JJIF: publicado |\n| [[05 Preta - graus 1 a 6]] | Preta, graus 1 a 6 | — | 3 a 5 anos por grau (ou atividade acumulada) | INFORMAÇÃO AUSENTE |\n| [[06 Graus de mestre (7º ao 10º)]] | 7º a 10º | 49 / 56 / 66 anos | 7, 7 e 10 anos | — |\n| [[00 Infantil 4 a 15 anos (grupos de cor)]] | 4 a 15 anos | por grupo de cor | sem mínimo | IBJJF: ausente · JJIF: publicado (p. 10–19) |\n\n"
    d += "## Progressão\n\n```mermaid\nflowchart LR\n  A[Branca] --> B[Azul 16+] --> C[Roxa 16+] --> D[Marrom 18+] --> E[Preta 18+* 6 graus] --> F[Vermelha e Preta 7º] --> G[Vermelha e Branca 8º] --> H[Vermelha 9º-10º]\n```\n*Preta aos 18 anos somente com título mundial adulto na Marrom.*\n\n" + NOTA_B + "\n\n## Pôster e páginas-chave do documento\n\n" + embeds(comuns, SRC_B) + "\n\n## Próximos passos\n\n- Levantamento inicial feito: [[Programas técnicos de BJJ - levantamento]] (nenhum programa oficial; só guias privados).\n- Levantar programas técnicos de exame em federações estaduais de Jiu-Jitsu e academias de referência (rotular como fonte privada/local, não oficial IBJJF).\n"
    (V / "BJJ" / "Dashboard BJJ.md").write_text(d, encoding="utf-8")


if __name__ == "__main__":
    for m in ("Judô", "BJJ"): (V / m).mkdir(parents=True, exist_ok=True)
    judo(); bjj()
    print("ok")
