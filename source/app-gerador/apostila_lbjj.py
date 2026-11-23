"""Apostila da Liga Brasileira de Jiu-Jitsu (LBJJ, nov/2007; PDF digitalizado, sem texto pesquisavel).
Recorta as figuras (sequencias desenhadas) por pagina e monta o grupo "Apostila LBJJ" da Lista de componentes do BJJ. Sem LLM."""
import pymupdf, glob, subprocess, io, csv, json, pathlib
import numpy as np
from PIL import Image
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
Z = 2.4; MINH = 190
CACHE = pathlib.Path(__file__).resolve().parent / "_cache_lbjj_bandas.json"
ARQ = "Apostila - Liga brasileira de Jiu Jitsu.pdf"


def pdf_path():
    return glob.glob(r"D:\Obsidian\Dominios\Judo_BJJ\fontes_livros\Apostila*Liga*Jiu*.pdf")[0]


def _bandas(png_bytes):
    im = Image.open(io.BytesIO(png_bytes)).convert("L"); a = np.array(im); H, W = a.shape
    ink = a < 150
    out = subprocess.run([TESS, "stdin", "stdout", "-l", "eng", "--psm", "4", "tsv"], input=png_bytes, capture_output=True).stdout.decode("utf-8", "ignore")
    txt = np.zeros((H, W), bool)
    for r in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
        try: conf = float(r["conf"]); t = (r["text"] or "").strip()
        except Exception: continue
        if conf > 55 and sum(c.isalpha() for c in t) >= 3:
            x, y, w, h = int(r["left"]), int(r["top"]), int(r["width"]), int(r["height"]); txt[max(0, y - 3):y + h + 3, max(0, x - 3):x + w + 3] = True
    resid = ink & ~txt
    resid[:, :int(W * 0.06)] = False; resid[:, int(W * 0.96):] = False; resid[:int(H * 0.02)] = False; resid[int(H * 0.97):] = False
    rows = resid.sum(axis=1) > 3; bands = []; y = 0
    while y < H:
        if rows[y]:
            y0 = y; gap = 0
            while y < H and (rows[y] or gap < 28):
                gap = 0 if rows[y] else gap + 1; y += 1
            y1 = y - gap
            if y1 - y0 >= MINH:
                cols = np.where(resid[y0:y1].sum(axis=0) > 1)[0]
                if len(cols): bands.append([max(0, int(cols[0]) - 8), max(0, y0 - 8), min(W, int(cols[-1]) + 8), min(H, y1 + 8)])
        y += 1
    return bands


def bandas_todas(doc):
    if CACHE.exists():
        c = json.loads(CACHE.read_text(encoding="utf-8"))
        if c.get("n") == doc.page_count: return {int(k): v for k, v in c["b"].items()}
    res = {}
    for p in range(2, 42):
        res[p] = _bandas(doc[p - 1].get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=False).tobytes("png"))
    CACHE.write_text(json.dumps({"n": doc.page_count, "b": res}), encoding="utf-8"); return res

# ---------------- Conteudo (resumo do assistente a partir da leitura das paginas) ----------------
FONTE = "Apostila da Liga Brasileira de Jiu-Jitsu (LBJJ, alterações de nov/2007), p. {} do PDF digitalizado. Resumo do assistente; o texto original está na imagem."
# (sub_id, sub_nome, desc, [ (titulo, [paginas com figuras], [paginas citadas], texto, [chaves Kodokan], pt) ])
SUBS = [
 ("rol", "Rolamentos e saltos", "Rolamentos e saltos do exame, com a sequência desenhada de cada movimento.", [
  ("Rolamentos 01 a 12", [2, 3], [2, 3], "Lista da apostila: 01 Frontal (estático); 02 Frontal (dinâmico); 03 Okemi de costas em defesa; 04 Okemi de costas (dinâmico); 05 Rolamento lateral (estático), esquerda/direita; 06 Rolamento lateral (dinâmico); 07 Queda lateral, esquerda/direita; 08 Cócoras; 09 Facial para a frente; 10 Facial para trás; 11 Tábua; 12 Palha de arroz ou folha seca. Cada item traz a descrição passo a passo; os desenhos numerados (1, 2, 3…) mostram a sequência.", [], "Rolamentos"),
  ("Rolamento 13 (gato) e saltos 01 a 06", [], [4], "13 Gato: de costas para o examinador, mãos sobrepostas na altura do peito, giro de 180° e queda sobre os antebraços. Saltos: 01 peixe (para a frente, sem obstáculo); 02 para a frente “com obstáculo” (o parceiro fica em posição fetal); 03 para a frente “com distância e obstáculo”; 04 em rolamento (mortal); 05 em distância/altura; 06 “sapo”.", [], "Gato e saltos")]),
 ("proj", "Projeções (quedas) e defesas", "As 15 projeções da apostila, com a sequência desenhada, e as defesas/contra-ataques de cada uma.", [
  ("Tabela de projeções (nome e significado)", [4], [4, 5], "01 Osoto-gari (grande ceifagem externa); 02 Ouchi-gari (grande ceifagem interna); 03 Ogoshi (grande projeção de quadril); 04 Ippon-seoi-nage (projeção pelo ombro); 05 Deashi-barai (rasteira lateral); 06 Koshi-guruma (quadril-giro); 07 Tai-otoshi (queda com o corpo); 08 Harai-goshi (varrida de quadril); 09 Sasae-tsuri-komi-ashi (varrida de pé com giro); 10 Tomoe-nage (projeção em círculo); 11 Hane-goshi (quadril levantado); 12 Uchimata (golpe interno); 13 Kata-guruma (rotação pelo ombro); 14 Morote-gari (baianada); 15 Seoi-nage (arremesso sobre o ombro).", [], "Projeções"),
  ("Projeção 01 Osoto-gari e 02 Ouchi-gari: defesas e contra-ataques", [5], [5], "Considera o oponente entrando pelo lado direito, com saídas por tai-sabaki. Osoto-gari: pequeno passo à frente, defesa caindo em base e calçada no calcanhar do oponente, projetando-o para trás. Ouchi-gari: pequeno passo com a perna direita para trás, entra em base (defendendo-se com a perna esquerda) e calça o calcanhar esquerdo do oponente, projetando-o para trás.", ["osotogari", "ouchigari"], "Osoto-gari; Ouchi-gari"),
  ("Projeção 03 Ogoshi, 04 Ippon-seoi-nage e 05 Deashi-barai", [6], [6], "Ogoshi: cair em defesa (posição de cavaleiro) e projetar o oponente para a frente com o quadril; ele cai em posição de chave de braço. Ippon-seoi-nage: tai-sabaki (giro de 180°) posicionando-se de frente com o oponente, usando a força dele; posição final montado. Deashi-barai: usar como defesa a mesma rasteira aplicada pelo oponente.", ["ogoshi", "ipponseoinage", "deashiharai"], "Ogoshi; Ippon-seoi-nage; Deashi-barai"),
  ("Projeção 06 Koshi-guruma, 07 Tai-otoshi e 08 Harai-goshi", [7], [7], "Koshi-guruma: após a defesa (cavaleiro), projetar-se à frente do oponente usando o quadril. Tai-otoshi: calçar o pé do oponente, dar um passo à frente com giro; o contragolpe é aplicado na altura do joelho. Harai-goshi: na entrada do oponente, “barrigada” para a frente, estabilizando-se na base; em seguida inverter a posição projetando o oponente.", ["koshiguruma", "taiotoshi", "haraigoshi"], "Koshi-guruma; Tai-otoshi; Harai-goshi"),
  ("Projeção 09 Sasae-tsuri-komi-ashi, 10 Tomoe-nage e 11 Hane-goshi", [8], [8], "Sasae-tsuri-komi-ashi: segurar na altura do joelho (pelo lado de fora) e entrar com ouchi-gari (queda 02), projetando o oponente. Tomoe-nage: soltar os braços da lapela do oponente, efetuando a estrela, e terminar em posição de kamishiho-gatame. Hane-goshi: calçar o pé (sentido contrário) do adversário, restabelecer a base, puxando-o para trás.", ["sasaetsurikomiashi", "tomoenage", "hanegoshi"], "Sasae-tsuri-komi-ashi; Tomoe-nage; Hane-goshi"),
  ("Projeção 12 Uchimata, 13 Kata-guruma e 14 Morote-gari", [9], [9], "Uchimata: travar as duas pernas na altura do joelho do oponente e retirar a perna que sofre o golpe; outra defesa é travar e usar a queda tani-otoshi. Kata-guruma: puxar a perna para trás, cruzar em posição adversa fazendo uma queda lateral; terminar em posição de aplicar uma chave cervical. Morote-gari: projetar o corpo para trás, esgrimir o braço do oponente e entrar na queda sumi-gaeshi.", ["uchimata", "kataguruma", "morotegari"], "Uchimata; Kata-guruma; Morote-gari"),
  ("Projeção 15 Seoi-nage e movimento de esportiva (cinturagem e esgrima)", [10], [10], "Seoi-nage: tai-sabaki saindo na lateral, buscando a perna de apoio e realizando o contragolpe, com montada em seguida. Movimento de esportiva: 01 os dois lutadores se posicionam, o examinando faz a esgrima com um dos braços (cotovelo do oponente) até a cintura, repete do outro lado e entra na queda 03 (Ogoshi); 02 movimento na busca do domínio, com os braços acima do ombro e entrada na queda 10 (Tomoe-nage).", ["seoinage"], "Seoi-nage")]),
 ("atemi", "Atemis e chutes", "Golpes de ataque (atemi waza) e chutes do exame, com os desenhos de cada ponto de contato.", [
  ("Atemis: ataques e defesas", [11, 12], [11, 12], "Ataques ilustrados: ippon nukite, empi, seiken, uraken, uedo, keito, washide, nihon nukite, teisho, seryuto, kumade, kakuto, haito, shuto, haishu, ippon-ken, nakadaka-ken, hiraken, yonhon nukite, hiza, haisoku, kakato, sokuto e teisoku. Lista: 01 soco regular à frente (base seiken); 02 golpe à frente com a mão aberta (teishou); 03 soco com as costas da mão (uraken); 04 pata de leão (martelo ou tetsui); 05–06 shuto; 07 tapão (simples/duplo); 08 chicote (esquerda/direita); 09 cotoveladas. Defesas: para fora, para dentro, para o alto, para baixo (púbis), de tapão (simples/duplo) e de chicote.", [], "Atemis (golpes)"),
  ("Chutes", [13, 14], [13, 14], "01 Mae-geri; 02 Mawashi-geri; 03 Yoko-geri; 04 Ura-mawashi; 05 Ushiro-geri; 06 Meia lua; 07 Circular para fora; 08 Circular para dentro.", [], "Chutes")]),
 ("imob", "Imobilizações (ne-waza)", "Imobilizações do solo, cada uma com a defesa correspondente.", [
  ("Imobilizações 01 a 05", [15, 16], [15, 16], "01 Kesa-gatame (cabeça alta); 02 Kesa-gatame (cabeça baixa); 03 Yoko-shiho (“Yoko Shiro”); 04 Yoko-shiho, variação com as pernas esticadas; 05 Kami-shiho-gatame. Cada item traz uma ou mais defesas (por exemplo: facão no pescoço, reversão, “camarão” com reposição de guarda).", ["kesagatame", "yokoshihogatame", "kamishihogatame"], "Imobilizações"),
  ("Imobilizações 06 a 11", [17, 18, 19], [17, 18, 19], "06 Kami-shiho-gatame (variação com as pernas esticadas); 07 Ushiro-kesa-gatame; 08 Tate-shiho-gatame (montada/frontal); 09 Kata-gatame; 10 Kuzure-gesa-gatame; 11 Makura-gesa-gatame. Defesas: puxar a perna entrando em reversão, retirar a cabeça, “upa” com sustentação de ombro, entre outras.", ["ushirokesagatame", "tateshihogatame", "katagatame", "kuzurekesagatame"], "Imobilizações")]),
 ("estr", "Estrangulamentos", "Estrangulamentos (shime waza) com a defesa de cada um.", [
  ("Estrangulamentos 01 a 04", [19, 20], [19, 20], "01 Mão de sabre (nami-juji-jime; sempre a mão direita sobre a esquerda); 02 Bico de águia (gyaku-juji-jime); 03 Mãos inversas (kata-juji-jime); 04 Cruz direta (a quatro dedos de distância, segurar a lapela; estrangular com a “cana do braço”).", ["namijujijime", "gyakujujijime", "katajujijime"], "Estrangulamentos"),
  ("Estrangulamentos 05 a 13", [21, 22, 23, 24], [21, 22, 23, 24], "05 Contornada; 06 Garrote lateral (katame-jime); 07 Compressão (“brinquinhos”; morote-jime); 08 Ajoelhado (okuri-eri-jime); 09 Braços elevados (kataha-jime); 10 Mata-leão; 11 Garrote com perna; 12 Gravada de frente; 13 Hadaka-jime. A última página deste bloco também apresenta o início das chaves de braço (01 Senador).", ["okuriierijime", "katahajime", "hadakajime"], "Estrangulamentos")]),
 ("chave", "Chaves de braço, armlock e perna", "Chaves de braço (kansetsu waza), armlock, leg lock e chave de perna.", [
  ("Chaves de braço 01 a 06", [25, 26], [24, 25, 26], "01 Senador ou chave em L (ude-garami); 02 Kimura ou chave em C; 03 Esticada; 04 Kimura inversa; 05 Trava de pé (hiza-gatame); 06 Kimura avançada, montando em tate-shiho.", ["udegarami", "hizagatame"], "Chaves de braço"),
  ("Armlock 01 a 12", [27, 28, 29, 30], [26, 27, 28, 29, 30], "01 Montado (juji-gatame); 02–03 Lateral; 04 De lado (hiza-gatame); 05 De braços; 06 Alavanca lateral; 07 Alicate; 08 Triângulo (com variação na imobilização yoko); 09 Crucifixo; 10 Voadora; 11 Cruzado; 12 Duplo. Na p. 30: leg lock, chave de punho (“mão de vaca”), omoplata e imobilização com joelho na barriga.", ["jujigatame", "udegatame"], "Armlock"),
  ("Chave de perna", [], [35], "01 Aplicando sentado em uma das pernas: travar a perna na panturrilha com a “cana” do braço, forçar a outra perna do oponente, resistir à defesa com “upa”/“barrigada” e partir para cima buscando a montada. 02 Aplicando sentado em ambas as pernas: repetir o movimento nas duas pernas.", [], "Chave de perna")]),
 ("guarda", "Guarda, montadas e raspagem", "Passagem e saída de guarda, montadas que pontuam, balancinho e raspagem.", [
  ("Passagem técnica de guarda e saídas de guarda", [31], [31], "Passagem técnica de guarda: segurar um dos braços do oponente com a palma da mão virada para cima, forçar a perna, colocar os dois joelhos juntos, bater a mão no dojô e finalizar em montada. Saída de guarda: 01 mão abaixo da perna na altura do joelho, passar uma das pernas; 02 passar somente uma das pernas; 03 passar com a perna “cruzamento” até o joelho na barriga; 04 duas mãos na faixa. Saída da meia guarda: com a perna presa e com a perna cruzada.", [], "Passagem e saída de guarda"),
  ("Montada lateral e montadas completas (04 pontos)", [32, 33], [32, 33], "Montada lateral: 01 direta; 02 indireta (o parceiro defende encolhendo a perna). Montadas completas que permitem 04 pontos: 01 por cima (tate-shiho); 02 lateral; 03 por trás; 04 clássica; 05 pegada por trás. “Pegada com 2 pontos”: pelas costas, saindo da guarda.", ["tateshihogatame"], "Montadas"),
  ("Balancinho, raspagem, deslizamento e colocar na guarda", [34], [34, 36], "Balancinho: com o oponente em meia guarda, prender a perna, fazer “camarão” e reverter. Raspagem: esticar a perna, apoiando a sola do pé, e inverter a posição. Deslizamento (kuzushi), movimentos de base (handori). Colocar na guarda corretamente: 01 de pé; 02 no solo; 03 variação. Também: estrangulado de pé e dominado na guarda; levantado pela cintura (bate-estaca), com defesas 01 a 04.", ["kuzushi"], "Raspagem e guarda")]),
 ("defesa", "Defesa pessoal", "Defesas conjugadas com domínio, agarramento e queda; defesa contra armas (apenas texto, sem figuras na apostila).", [
  ("Defesas conjugadas e defesa pessoal", [], [37, 38, 39, 40], "Defesas conjugadas com domínio, agarramento e queda: 01 no peito; 02 na garganta; 03 chute regular (mae-geri); 04 chute circular (mawashi-geri); 05 tapão simples; 06 tapão duplo. Agarramentos: cabelos, pulso, lapela/blusão, mãos na garganta, pela frente (braços soltos/presos) e por trás (braços presos/soltos). Gravatas (lateral, frente, atrás), bastão (lateral e alto da cabeça), cadeirada, faca (peito, rins, abdome, garganta) e revólver (peito, cabeça e costas): cada situação traz a defesa descrita.", [], "Defesa pessoal")]),
 ("tai", "Tai-sabaki (diagramas)", "Diagramas de passos para giro e esquiva.", [
  ("Tai-sabaki: direções e diagramas de pés", [35, 41], [35, 36, 41], "Direções de deslocamento: para a frente, para trás, para a frente à esquerda/direita, lateral esquerda/direita e para trás à esquerda/direita (“não fechar, não cruzar, não abrir as pernas demais”). Diagramas: tai-sabaki para a frente (1ª e 2ª formas); para trás (forma direta e lateral); giro (1ª forma; 2ª pelo interior; 3ª pelo exterior). A apostila também menciona “movimentos simples em 90 e 180 graus”.", ["taisabaki"], "Tai-sabaki")]),
]


CIRC = "LBJJ, Circular Oficial do exame de faixa preta e concessão de graus de 05/12/2026 (lbjj.com.br/examefxpreta), pp. 1–3"
FILI = "LBJJ, formulário de filiação de atleta (lbjj.com.br/filiacao-de-atleta), consultado em 10/11/2026"
EXAME = [
 ("Quais são as faixas e graus da LBJJ", "No formulário de filiação de atleta a LBJJ lista as faixas: Branca, Cinza, Amarela, Laranja, Verde, Azul, Roxa, Marrom, Preta, Vermelha/Preta, Vermelha/Branca e Vermelha; e os graus Lisa e 1º ao 10º. A filiação distingue atletas “até 17 anos” e “acima de 17 anos”. As faixas Cinza, Amarela, Laranja e Verde são as dos menores de idade (no sistema IBJJF/CBJJ, 4 a 15 anos); as páginas consultadas da LBJJ não publicam a idade mínima de cada cor.", FILI),
 ("Exame de faixa preta (aspirante vindo da Marrom)", "Condições da circular de 2026 (exame em 05/12/2026): autorização prévia, por escrito, do professor; mínimo de 1 ano na faixa marrom, com participação em competições estaduais e/ou nacionais (exceções analisadas pelo Departamento Técnico); idade mínima de 18 anos; carteira LBJJ de 2025 ou 2026; ter participado de reuniões, cursos e reciclagens da LBJJ; conhecer o Regulamento Geral e o Programa Oficial da LBJJ; estar em dia com a equipe e o professor; ensino fundamental completo; não ter penalidade disciplinar nem processo criminal; conduta compatível com os princípios da LBJJ. Taxa: R$ 1.700,00. Horários podem mudar (a própria circular traz horários diferentes em páginas distintas).", CIRC),
 ("Reciclagem das técnicas tradicionais", "A circular oferece, no mesmo dia, o curso de “Reciclagem das Técnicas Tradicionais do Jiu-Jitsu, Noções de Ética e Disciplina”, aberto a faixas azuis, roxas e marrons que quiserem fazê-lo (R$ 250,00 para quem nunca fez; R$ 200,00 para quem já participou). A circular não lista as técnicas.", CIRC),
 ("Concessão de grau (faixa preta)", "Autorização prévia, por escrito, do professor; carteira LBJJ de 2025 ou 2026; cópia do diploma de faixa preta de entidade reconhecida pela LBJJ (FMJJ, LBJJ, CBJJ ou IBJJF), com carência analisada pelo Corpo de Oficiais e pela banca; para o 3º grau (título de Professor), curso de Regras e Arbitragem atualizado (LBJJ, CBJJ ou IBJJF). Taxas: R$ 1.700,00 do 1º ao 3º grau; R$ 700,00 a partir do 4º.", CIRC),
 ("Branca → Cinza → Amarela → Laranja → Verde → Azul → Roxa → Marrom: o que é cobrado", "INFORMAÇÃO AUSENTE. Não encontrei programa técnico público por faixa da LBJJ, nem para os menores de 18 anos nem para os adultos: o site (páginas de organização, história, cursos, filiação, exames, vídeos) e a circular não o publicam, e a circular apenas remete ao “Programa Oficial da LBJ-J”. A apostila de 2007 também não associa técnicas a faixas (não cita cor, grau nem idade). Para obter o programa, a LBJJ informa na circular o e-mail lbjjbr@gmail.com e o WhatsApp (31) 9232-2403. Quando você tiver esse documento, ele entra aqui por faixa.", "LBJJ, pesquisa no site em 10/11/2026 e circular de 2026; Apostila LBJJ (nov/2007)"),
 ("Enquanto isso: como usar a apostila", "INFERÊNCIA, não confirmada pela LBJJ: como a circular cita a “reciclagem das técnicas tradicionais do Jiu-Jitsu” e o “Programa Oficial”, a apostila de 2007 (rolamentos, projeções, atemis, solo, defesa pessoal) pode ser o conteúdo-base do exame. Use as outras subcategorias de “Apostila LBJJ” como referência de execução, sem tratá-las como exigência de uma faixa específica.", "Inferência do assistente a partir da circular e da apostila"),
]


def grupo_exame():
    bl = [{"titulo": t, "texto": x, "fotos": [], "fonte": f, "nm": {"ja": "", "en": "", "pt": "", "sj": ""}} for t, x, f in EXAME]
    return {"fotos": [], "regra": [], "videos": [], "itens": [], "id": "lbjj_exame", "nome": "Exame por faixa (LBJJ)", "desc": "O que a LBJJ publica sobre exames: faixas e graus, requisitos do exame de faixa preta e das concessões de grau, e a lacuna do programa técnico de cada faixa (incluindo as dos menores).", "nm": {"ja": "", "en": "", "pt": "Exame por faixa (LBJJ)", "sj": "LBJJ"}, "blocos": bl}


def grupo(IMG, GL, save=True):
    doc = pymupdf.open(pdf_path()); bands = bandas_todas(doc); subs = []; nfig = 0
    def nm(keys, pt):
        ja = []; en = []
        for k in keys:
            e = GL.KD.get(GL.norm(k))
            if e: ja.append(f"{e['ja']} · {e['rom']}"); en.append(e["en"])
        return {"ja": "; ".join(ja), "en": "; ".join(en), "pt": pt, "sj": "japonês/inglês: IJF/Kodokan; português: LBJJ"}
    def fotos(p):
        nonlocal nfig; out = []
        pg = None
        for k, (x0, y0, x1, y1) in enumerate(bands.get(p, [])):
            fn = f"lbjj_p{p:02d}_{k + 1}.jpg"; f = IMG / fn
            if save and not f.exists():
                if pg is None: pg = doc[p - 1].get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=False)
                im = Image.frombytes("RGB", (pg.width, pg.height), pg.samples).crop((x0, y0, x1, y1)); im.save(f, "JPEG", quality=82)
            out.append({"img": "img/" + fn, "cap": f"Apostila LBJJ, p. {p} do PDF: figura {k + 1}", "fonte": f"Apostila LBJJ (nov/2007), p. {p} do PDF digitalizado"}); nfig += 1
        return out
    base = {"fotos": [], "regra": [], "videos": [], "itens": []}
    for sid, snome, desc, blocks in SUBS:
        bl = []
        for titulo, pf, pc, texto, keys, pt in blocks:
            pcs = ", ".join(str(x) for x in pc)
            bl.append({"titulo": titulo, "texto": texto, "fotos": [f for p in pf for f in fotos(p)], "fonte": FONTE.format(pcs), "nm": nm(keys, pt)})
        subs.append(dict(base, id="lbjj_" + sid, nome=snome, desc=desc, nm={"ja": "", "en": "", "pt": snome, "sj": "LBJJ"}, blocos=bl))
    subs.insert(0, grupo_exame())
    print("Apostila LBJJ:", len(subs), "subcategorias,", nfig, "figuras")
    return {"id": "lbjj", "nome": "Apostila LBJJ", "desc": "Apostila da Liga Brasileira de Jiu-Jitsu (LBJJ, nov/2007): programa de um Jiu-Jitsu “tradicional” brasileiro, com rolamentos, projeções, atemis, chutes, solo, guarda e defesa pessoal. É um sistema próprio, diferente do BJJ esportivo da IBJJF/CBJJ e do programa da JJIF; serve como referência complementar com sequências desenhadas. O PDF é uma digitalização sem texto pesquisável: os textos aqui são resumos do assistente a partir da leitura das páginas (consulte a imagem para o texto original).",
            "itens": [], "fotos": [], "regra": [], "videos": [], "nm": {"ja": "", "en": "", "pt": "Apostila LBJJ (Jiu-Jitsu tradicional)", "sj": "LBJJ"}, "subs": subs}

