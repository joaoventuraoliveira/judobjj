"""Glossario trilingue (japones, ingles, portugues do Brasil) para os termos do app.
Fontes e rotulos:
  - JA/EN dos termos do Kodokan: dicionario do documento 'IJF Kodokan Classification of Judo' (lido do PDF, com pagina).
  - JA/PT de termos de ukemi, tai sabaki, shintai etc.: slides da palestra da FJERJ (2018) e regulamento CBJ 2023.
  - Equivalentes aproximados no Kodokan para golpes de BJJ (armlock = ude-hishigi-juji-gatame etc.): marcados 'eq'.
  - PT-BR de termos de BJJ sem fonte: 'sugestao do app' (src 'app'); onde nao ha traducao segura, fica vazio.
"""
import re, unicodedata, pymupdf, pathlib

KD_PDF = pathlib.Path(r"D:\Claude\Judo_BJJ\judo\00_geral_regras_IJF_CBJ\fontes_pdf\IJF_Kodokan_Classification_of_Judo_via_BritishJudo.pdf")


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def carregar_kodokan():
    """romaji normalizado -> {ja, rom, en, pag}"""
    out = {}
    if not KD_PDF.exists(): return out
    d = pymupdf.open(KD_PDF)
    for pno in range(len(d)):
        t = " ".join(d[pno].get_text("text").split())
        for m in re.finditer(r"(\d{3,4})\s+([\u3040-\u30ff\u4e00-\u9fff々]+)\s+([A-Z][A-Za-z\u014d\u016b\-]+)\s+\(([^)]*)\)", t):
            out.setdefault(norm(m.group(3)), {"ja": m.group(2), "rom": m.group(3), "en": m.group(4), "pag": pno + 1})
    return out


KD = carregar_kodokan()

# equivalentes aproximados (BJJ -> Kodokan); chave: regex no nome do item (minusculas), valor: chave romaji no KD
EQ = [(r"\barm ?bar\b|armlock|arm lock", "udehishigijujigatame"), (r"\btriangle\b", "sankakujime"), (r"rear.?naked|mata le", "hadakajime"),
      (r"\bamericana\b", "udegarami"), (r"kata gatame", "katagatame"), (r"cross choke", "namijujijime")]

# nomes japoneses sem entrada no dicionario do Kodokan do PDF (kanji de uso corrente; fonte: FJERJ/CBJ ou 'app')
JA_EXTRA = {"ukemi": ("受身", "Ukemi", "FJERJ"), "maeukemi": ("前受身", "Mae-ukemi", "FJERJ"), "yokoukemi": ("横受身", "Yoko-ukemi", "FJERJ"), "ushiroukemi": ("後受身", "Ushiro-ukemi", "FJERJ"),
            "zempokaiten": ("前方回転", "Zempō-kaiten", "FJERJ"), "kohokaiten": ("後方回転", "Kōhō-kaiten", "FJERJ"), "taisabaki": ("体捌", "Tai-sabaki", "FJERJ"), "shintai": ("進退", "Shintai", "FJERJ"),
            "ayumiashi": ("歩み足", "Ayumi-ashi", "FJERJ"), "suriashi": ("摺足", "Suri-ashi", "FJERJ"), "tsugiashi": ("継足", "Tsugi-ashi", "FJERJ"), "hadakajime": ("裸絞", "Hadaka-jime", "KD"),
            "renrakuwaza": ("連絡技", "Renraku-waza", "FJERJ"), "renzokuwaza": ("連続技", "Renzoku-waza", "FJERJ"), "kesagatame": ("袈裟固", "Kesa-gatame", "KD"),
            "kumikata": ("組み方", "Kumi-kata", "CBJ"), "shisei": ("姿勢", "Shisei", "CBJ"), "kuzushi": ("崩し", "Kuzushi", "CBJ"), "tsukuri": ("作り", "Tsukuri", "CBJ"), "kake": ("掛け", "Kake", "CBJ"),
            "kaeshiwaza": ("返技", "Kaeshi-waza", "CBJ"), "nogare": ("逃れ", "Nogare", "CBJ"), "fusegi": ("防ぎ", "Fusegi", "CBJ"), "goshinjutsu": ("護身術", "Goshin-jutsu", "CBJ")}

# ---- itens (nome do item em ingles no programa JJIF) -> (regex, kd_key | None, pt, src_pt) ----
# kd_key = chave romaji normalizada do dicionario Kodokan para termos japoneses que aparecem no proprio item
ITENS = [
    (r"^front roll$", "zempokaiten", "Rolamento para a frente (zempo kaiten ukemi)", "FJERJ"),
    (r"^back roll$", "kohokaiten", "Rolamento para trás (koho kaiten ukemi)", "FJERJ"),
    (r"back and side break ?fall", "ushiroukemi", "Queda para trás e queda lateral (ushiro ukemi, yoko ukemi)", "FJERJ"),
    (r"^sit and hip escape", None, "Fuga de quadril (camarão)", "app"),
    (r"^grips and footwork", "kumikata", "Pegadas e deslocamento", "app"),
    (r"^idea of base", None, "Noção de base", "app"),
    (r"^leverage principles", None, "Princípios de alavanca", "app"),
    (r"rocking and technical stand", None, "Balanço e levantada técnica", "app"),
    (r"^underhook switch", None, "Troca de underhook (pegada por baixo do braço)", "app"),
    (r"^o soto gari$", "osotogari", "Grande ceifada externa", "app"),
    (r"^de ashi harai$", "deashiharai", "Varrida do pé que avança", "app"),
    (r"^o uchi gari$", "ouchigari", "Grande ceifada interna", "app"),
    (r"^ko uchi gari$", "kouchigari", "Pequena ceifada interna", "app"),
    (r"^o goshi$", "ogoshi", "Grande projeção de quadril", "app"),
    (r"^koshi guruma$", "koshiguruma", "Roda de quadril", "app"),
    (r"^tomoe nage$", "tomoenage", "Projeção em círculo (sacrifício para trás)", "app"),
    (r"^sumi gaeshi$", "sumigaeshi", "Projeção de canto (sacrifício)", "app"),
    (r"^ippon seoi nage$", "ipponseoinage", "Projeção de ombro com uma mão", "app"),
    (r"^knee drop seoi nage", "seoinage", "Projeção de ombro com joelho no chão", "app"),
    (r"osoto guruma", "osotoguruma", "Grande roda externa", "app"),
    (r"^double leg$", None, "Queda de duas pernas (double leg)", "app"),
    (r"^single leg$", None, "Queda de uma perna (single leg)", "app"),
    (r"^sprawl$", None, "Defesa de queda (sprawl)", "app"),
    (r"^crucifix$", None, "Crucifixo", "app"),
    (r"^pulling to guard", None, "Puxada de guarda", "CBJJ"),
    (r"^guard recovery", None, "Recuperação de guarda", "app"),
    (r"^open closed guard standing", None, "Abrir a guarda fechada em pé", "app"),
    (r"stand up passing guard", None, "Passagem de guarda em pé com um braço preso", "app"),
    (r"^half guard passing", None, "Passagem de meia-guarda", "app"),
    (r"^open guard with knees", None, "Guarda aberta com os joelhos no chão", "app"),
    (r"^bull pass", None, "Passagem de touro (bullfighter)", "app"),
    (r"double underhook guard pass", None, "Passagem com dois underhooks", "app"),
    (r"reverse half guard pass", None, "Passagem da meia-guarda invertida", "app"),
    (r"^knee slide pass", None, "Passagem deslizando o joelho (knee slide)", "app"),
    (r"^delariva pass", None, "Passagem da De La Riva", "app"),
    (r"^spider guard passing", None, "Passagem da guarda aranha", "app"),
    (r"^butterfly guard pass", None, "Passagem da guarda borboleta", "app"),
    (r"^cross choke", None, "Estrangulamento cruzado (gola cruzada)", "app"),
    (r"^armlock", None, "Chave de braço (armlock)", "CBJJ"),
    (r"^arm ?bar$", None, "Chave de braço (armbar)", "app"),
    (r"^armbar escape", None, "Saída da chave de braço", "app"),
    (r"^kimura", None, "Kimura (chave de braço)", "app"),
    (r"^americana", None, "Americana (chave de ombro)", "app"),
    (r"^triangle$", None, "Triângulo", "CBJJ"),
    (r"^double attack: armbar and triangle", None, "Ataque duplo: chave de braço e triângulo", "app"),
    (r"^omoplata$", None, "Omoplata", "CBJJ"),
    (r"^closed guard to spider guard", None, "Transição da guarda fechada para a guarda aranha", "app"),
    (r"^guard pull to spider guard and sweep", None, "Puxada para a guarda aranha e raspagem", "app"),
    (r"^wrist ?lock", None, "Chave de punho", "app"),
    (r"^arm drag going to", None, "Arm drag indo para as costas", "app"),
    (r"^sweep with opponent standing", None, "Raspagem com o oponente em pé", "app"),
    (r"^scissor sweep", None, "Raspagem de tesoura", "app"),
    (r"^tripod sweep", None, "Raspagem tripé", "app"),
    (r"^pendulum sweep", None, "Raspagem do pêndulo", "app"),
    (r"^spider guard sweep", None, "Raspagem da guarda aranha", "app"),
    (r"^lapel guard sweep", None, "Raspagem da guarda de lapela", "app"),
    (r"^half guard sweep", None, "Raspagem da meia-guarda", "app"),
    (r"^delariva sweep", None, "Raspagem da De La Riva", "app"),
    (r"^deep half guard sweep", None, "Raspagem da meia-guarda profunda", "app"),
    (r"^butterfly sweep", None, "Raspagem da guarda borboleta", "app"),
    (r"^omoplata sweep", None, "Raspagem de omoplata", "app"),
    (r"^worm guard sweep", None, "Raspagem da worm guard", "app"),
    (r"^sweep from one leg", None, "Raspagem de uma perna", "app"),
    (r"^replace guard from side control", None, "Recuperar a guarda a partir do controle lateral", "app"),
    (r"^going to mount position", None, "Ir para a montada", "app"),
    (r"^americana from side control", None, "Americana a partir do controle lateral", "app"),
    (r"^kimura from side control", None, "Kimura a partir do controle lateral", "app"),
    (r"^knee on belly going to armbar", None, "Joelho na barriga indo para a chave de braço", "app"),
    (r"^knee on belly escape", None, "Saída do joelho na barriga recuperando a guarda fechada", "app"),
    (r"^knee on belly and choke", None, "Joelho na barriga e estrangulamento", "app"),
    (r"^escape from side control", None, "Saída do controle lateral", "app"),
    (r"^north-south choke", None, "Estrangulamento norte-sul", "app"),
    (r"^transition from side to back", None, "Transição do controle lateral para as costas", "app"),
    (r"^seat belt", None, "Pegada de cinto de segurança (seat belt)", "app"),
    (r"^controll?ing the back", None, "Controle das costas: ganchos, pés cruzados, triângulo de corpo", "app"),
    (r"^rear naked choke", "hadakajime", "Mata-leão", "CBJJ"),
    (r"^lapel choke", None, "Estrangulamento com a lapela", "app"),
    (r"^going to back from all four", None, "Ir para as costas a partir de quatro apoios (tartaruga)", "app"),
    (r"^mount control", None, "Controle na montada", "app"),
    (r"^bridge$", None, "Ponte", "app"),
    (r"^armlock from mount", None, "Chave de braço a partir da montada", "app"),
    (r"^escape from mount to guard", None, "Saída da montada para a guarda (fuga de cotovelo)", "app"),
    (r"^ezequiel choke", None, "Estrangulamento com a manga do kimono (Ezequiel)", "CBJJ"),
    (r"^kata gatame", "katagatame", "Kata gatame (no judô, imobilização de ombro; no BJJ, estrangulamento arm triangle)", "app"),
    (r"^inverted armbar", None, "Chave de braço invertida", "app"),
    (r"^baseball choke", None, "Estrangulamento baseball", "app"),
    (r"^pulling guard with guillotine", None, "Puxada de guarda com guilhotina (gravata técnica de frente)", "CBJJ"),
    (r"^back take from half guard", None, "Pegar as costas a partir da meia-guarda", "app"),
    (r"^biceps slice", None, "Chave de bíceps", "CBJJ"),
    (r"^straight footlock", None, "Chave de pé reta", "CBJJ"),
    (r"^toe ?hold", None, "Toe hold (torção do pé)", "app"),
    (r"^knee ?bar", None, "Chave de joelho reta (kneebar)", "CBJJ"),
    (r"^calf slice", None, "Chave de panturrilha", "CBJJ"),
    (r"^technical stand up", None, "Levantada técnica", "app"),
]

GRUPOS_NM = {  # id do grupo BJJ -> (ja, en, pt, fonte_ja)
    "fund": ("基本 · 受身 · 体捌", "Fundamentals (Kihon): breakfalls, rolls, body shifting", "Fundamentos: ukemi, rolamentos e tai sabaki", "FJERJ"),
    "quedas": ("投技 (Nage-waza)", "Throwing techniques / Takedowns", "Quedas e projeções", "IJF/Kodokan"),
    "posicoes": ("固技 (Katame-waza) · 抑込技 (Osaekomi-waza)", "Grappling / Pinning positions", "Posições e controles", "IJF/Kodokan"),
    "guardas": ("— (sem termo padrão no Kodokan)", "Guards and guard passing", "Guardas e passagens de guarda", ""),
    "raspagens": ("— (sem termo padrão no Kodokan)", "Sweeps", "Raspagens", ""),
    "saidas": ("逃れ (Nogare)", "Escapes", "Saídas e recuperações", "CBJ"),
    "braco": ("関節技 (Kansetsu-waza) · 腕挫 (Ude-hishigi)", "Arm locks", "Chaves de braço", "IJF/Kodokan"),
    "perna": ("— (chaves de perna não existem no judô de competição)", "Leg and foot locks", "Chaves de perna e pé", ""),
    "punho": ("関節技 (Kansetsu-waza)", "Wrist locks", "Chaves de punho", "IJF/Kodokan"),
    "estrang": ("絞技 (Shime-waza)", "Chokes / strangles", "Estrangulamentos", "IJF/Kodokan"),
    "defesa": ("護身術 (Goshin-jutsu)", "Self-defense", "Defesa pessoal", "CBJ"),
    "transicoes": ("連絡技 (Renraku-waza)", "Transitions / linked techniques", "Transições entre técnicas e posições", "FJERJ"),
    "faltas": ("— (禁止 Kinshi, proibido)", "Fouls and prohibited actions", "Faltas e golpes proibidos", ""),
}

CAT_JUDO = {  # categoria do Judo -> (ja, en, pt, fonte)
    "Elegibilidade": ("", "Eligibility", "Elegibilidade", ""),
    "Reverência e quedas (Rei/Ukemi)": ("礼 · 受身 (Rei · Ukemi)", "Bow and breakfalls", "Reverência e amortecimento de quedas", "FJERJ"),
    "Fundamentos de aplicação": ("崩し · 作り · 掛け · 組み方 · 姿勢 · 体捌", "Fundamentals of application (kuzushi, tsukuri, kake, kumi-kata, shisei, tai-sabaki)", "Fundamentos de aplicação", "CBJ/FJERJ"),
    "Projeção (Nage waza)": ("投技 (Nage-waza)", "Throwing techniques", "Técnicas de projeção", "IJF/Kodokan"),
    "Imobilização (Osae komi waza)": ("抑込技 (Osaekomi-waza)", "Pinning techniques", "Técnicas de imobilização", "IJF/Kodokan"),
    "Estrangulamento (Shime waza)": ("絞技 (Shime-waza)", "Strangling techniques", "Técnicas de estrangulamento", "IJF/Kodokan"),
    "Chave de cotovelo (Kansetsu waza)": ("関節技 (Kansetsu-waza)", "Joint techniques (elbow)", "Técnicas de chave de articulação (cotovelo)", "IJF/Kodokan"),
    "Solo: viradas, escapes e defesas": ("固技 (Katame-waza) · 逃れ (Nogare) · 防ぎ (Fusegi)", "Ground techniques: turnovers, escapes, defenses", "Solo: viradas, saídas e defesas", "IJF/Kodokan; CBJ"),
    "Sequências e contragolpes": ("連絡技 · 連続技 · 返技 (Renraku · Renzoku · Kaeshi-waza)", "Linked techniques and counters", "Sequências de golpes e contragolpes", "FJERJ; CBJ"),
    "Kata": ("形 (Kata)", "Kata (forms)", "Kata (formas)", ""),
    "Vocabulário": ("", "Vocabulary", "Vocabulário", ""),
    "Histórico, princípios e cultura": ("", "History, principles and culture", "Histórico, princípios e cultura", ""),
    "Arbitragem": ("審判 (Shinpan)", "Refereeing", "Arbitragem", "app"),
    "Provas teóricas": ("", "Theory exam", "Provas teóricas", ""),
    "Provas práticas": ("", "Practical exam", "Provas práticas", ""),
    "Atividades de ensino": ("", "Teaching activities", "Atividades de ensino", ""),
    "Outros critérios": ("", "Other criteria", "Outros critérios", ""),
}

# termos japoneses que aparecem nos textos do regulamento da CBJ -> (ja, rom, en, pt, fonte)
TERMOS_JUDO = [
    (r"\bUkemi\b", "受身", "Ukemi", "breakfall", "amortecimento de queda", "FJERJ"),
    (r"Ushiro ukemi", "後受身", "Ushiro-ukemi", "backward breakfall", "queda para trás", "FJERJ"),
    (r"Yoko ukemi", "横受身", "Yoko-ukemi", "side breakfall", "queda lateral", "FJERJ"),
    (r"Zemp[oô] ?kaiten|Maemawari ukemi", "前方回転", "Zempō-kaiten / Mae-mawari-ukemi", "forward rolling breakfall", "rolamento para a frente", "FJERJ"),
    (r"Nage waza", "投技", "Nage-waza", "throwing techniques", "técnicas de projeção", "IJF/Kodokan"),
    (r"Osae ?komi waza", "抑込技", "Osaekomi-waza", "pinning techniques", "técnicas de imobilização", "IJF/Kodokan"),
    (r"Shime waza", "絞技", "Shime-waza", "strangling techniques", "técnicas de estrangulamento", "IJF/Kodokan"),
    (r"Kansetsu waza", "関節技", "Kansetsu-waza", "joint techniques", "técnicas de chave de articulação", "IJF/Kodokan"),
    (r"Katame waza", "固技", "Katame-waza", "grappling techniques", "técnicas de solo", "IJF/Kodokan"),
    (r"Renraku (?:henka )?waza", "連絡技", "Renraku-waza", "linked techniques", "técnicas de ligação (sequência de golpes)", "FJERJ"),
    (r"Kaeshi waza", "返技", "Kaeshi-waza", "counter techniques", "contragolpes", "CBJ"),
    (r"Kuzushi", "崩し", "Kuzushi", "balance-breaking", "desequilíbrio", "CBJ"),
    (r"Tsukuri", "作り", "Tsukuri", "preparation / fitting in", "preparação", "CBJ"),
    (r"\bKake\b", "掛け", "Kake", "execution", "execução", "CBJ"),
    (r"Kumi kata", "組み方", "Kumi-kata", "grips", "formas de pegar no judogi", "CBJ"),
    (r"Shisei", "姿勢", "Shisei", "postures", "posturas", "CBJ"),
    (r"Shintai", "進退", "Shintai", "body movement / stepping", "deslocamento do corpo", "FJERJ"),
    (r"Ayumi ashi", "歩み足", "Ayumi-ashi", "natural walking steps", "passadas naturais", "FJERJ"),
    (r"Tsugi ashi", "継足", "Tsugi-ashi", "following steps", "passadas sucessivas", "FJERJ"),
    (r"Tai sabaki", "体捌", "Tai-sabaki", "body shifting", "giro e esquiva do corpo", "FJERJ"),
    (r"Nogare", "逃れ", "Nogare", "escape", "escapada / saída", "CBJ"),
    (r"Fusegi", "防ぎ", "Fusegi", "defense", "defesa", "CBJ"),
    (r"Randori", "乱取", "Randori", "free practice", "treino livre", "FJERJ"),
    (r"Shiai", "試合", "Shiai", "match / competition", "competição", "CBJ"),
    (r"Dojô|Dojo", "道場", "Dōjō", "training hall", "academia / local de treino", "CBJ"),
    (r"Tatami", "畳", "Tatami", "mat", "local de treino (tatame)", "CBJ"),
    (r"Judogi", "柔道着", "Judogi", "judo uniform", "uniforme de judô", "FJERJ"),
    (r"Sensei", "先生", "Sensei", "teacher", "professor", "CBJ"),
    (r"\bUchikomi\b", "打込", "Uchikomi", "repetition entries", "treinamento de entrada das técnicas", "CBJ"),
    (r"Nage no Kata", "投の形", "Nage-no-kata", "forms of throwing", "kata de projeções", "FJERJ"),
    (r"Katame no Kata", "固の形", "Katame-no-kata", "forms of grappling", "kata de controle", "CBJ"),
    (r"Ju no Kata", "柔の形", "Jū-no-kata", "forms of gentleness", "kata da suavidade", "CBJ"),
    (r"Kime no Kata", "極の形", "Kime-no-kata", "forms of decision", "kata de defesa pessoal", "CBJ"),
    (r"Kodokan Goshin jutsu", "講道館護身術", "Kōdōkan-goshin-jutsu", "Kodokan self-defense", "defesa pessoal do Kodokan", "CBJ"),
    (r"Koshiki no kata", "古式の形", "Koshiki-no-kata", "ancient forms", "kata antigo", "CBJ"),
    (r"Itsutsu no kata", "五の形", "Itsutsu-no-kata", "forms of five", "kata dos cinco princípios", "CBJ"),
    (r"Ritsu rei", "立礼", "Ritsu-rei", "standing bow", "saudação em pé", "FJERJ"),
    (r"Za rei", "座礼", "Za-rei", "kneeling bow", "saudação ajoelhada", "CBJ"),
    (r"Tori", "取り", "Tori", "the one who throws", "judoca ativo", "FJERJ"),
    (r"\bUke\b", "受け", "Uke", "the one who receives", "judoca passivo", "FJERJ"),
    (r"Hajime", "始め", "Hajime", "begin", "começar", "CBJ"),
    (r"\bMate\b", "待て", "Mate", "wait / stop", "parar", "CBJ"),
]


def _kd(k):
    return KD.get(k)


def nomes_item(texto, cat=""):
    """devolve {ja,en,pt,sj,sp,eq} para um item do programa JJIF"""
    t = " ".join(texto.split()); low = t.lower()
    ja = ""; sj = ""; eq = False; pt = ""; sp = ""; en = t; rom = ""
    for rx, kk, ptx, src in ITENS:
        if re.search(rx, low):
            pt, sp = ptx, src
            # variacao numerada (ex.: sweep 2)
            m = re.search(r"\b(\d)\s*$", t)
            if m and not re.search(r"\d", ptx): pt = f"{ptx} (variação {m.group(1)})"
            if kk:
                e = _kd(kk)
                if e: ja, rom, sj = e["ja"], e["rom"], f"IJF/Kodokan, p. {e['pag']}"; en = f"{t} — {e['en']}" if e["en"] and e["en"].lower() not in low else t
                elif kk in JA_EXTRA: ja, rom, sj = JA_EXTRA[kk][0], JA_EXTRA[kk][1], JA_EXTRA[kk][2]
            break
    if not ja:
        for rx, kk in EQ:
            if re.search(rx, low):
                e = _kd(kk)
                if e: ja, rom, sj, eq = e["ja"], e["rom"] + (" (e variantes gyaku-juji-jime e kata-juji-jime)" if kk == "namijujijime" else ""), f"IJF/Kodokan, p. {e['pag']} (equivalente aproximado)", True
                break
    return {"ja": (f"{ja} · {rom}" if ja else ""), "en": en, "pt": pt, "sj": sj, "sp": sp, "eq": eq}


def termos_judo(texto):
    out = []
    for rx, ja, rom, en, pt, src in TERMOS_JUDO:
        if re.search(rx, texto):
            out.append({"ja": ja, "rom": rom, "en": en, "pt": pt, "f": src})
    # tecnicas nomeadas no proprio texto, procurando no dicionario Kodokan
    for k, e in KD.items():
        if len(k) >= 9 and re.search(re.escape(e["rom"]), texto, re.I):
            out.append({"ja": e["ja"], "rom": e["rom"], "en": e["en"], "pt": "", "f": f"IJF/Kodokan, p. {e['pag']}"})
    seen = set(); res = []
    for o in out:
        if o["rom"] in seen: continue
        seen.add(o["rom"]); res.append(o)
    return res[:8]
