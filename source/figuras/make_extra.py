"""
make_extra.py — gera ext_<nome>.py para os capítulos novos:
  ren_*  : renraku-waza (combinações) em pé, transição pé→solo e no solo
  kae_*  : kaeshi-waza (contragolpes) reconhecidos pelo Kodokan
  pro_*  : técnicas e ações proibidas nas regras de arbitragem da IJF
Uso: python3 make_extra.py && python3 run_extra.py
Fontes de validação: IJF/Kodokan Classification (2017); IJF SOR – Refereeing Rules,
art. 18 (ciclo 2025-2028); atualizações IJF de jan./2026.
"""
import os
from make_scripts import SCENES
from make_tri import SPEC

HERE = os.path.dirname(os.path.abspath(__file__))
TK = {n: tk for n, kz, tk, kk in SPEC}


def swap(code):
    """Troca as cores: quem ataca passa a vestir azul (uke) — usado no 1º quadro dos contragolpes."""
    return code.replace("'tori'", "'@@'").replace("'uke'", "'tori'").replace("'@@'", "'uke'")


def kake(n):
    return SCENES[n][2]


def tsukuri(n):
    return TK[n][0]


# ----------------------------------------------------------------- cenas novas no solo
NEW = {}
NEW['kata_gatame'] = """uke = lying('uke', 330, 1, y=396)
uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
tori = Fig('tori', 280, 380, ang=118, facing=1)
tori.leg('far', (170, GROUND - 4), bend=1)
tori.leg('near', (300, GROUND - 4), bend=-1)
uke.arm('near', (tori.neck[0] + 4, tori.neck[1] - 6), bend=1)
tori.arm('near', (uke.head[0] + 12, uke.head[1] - 4), bend=1)
tori.arm('far', (uke.head[0] + 6, uke.head[1] + 8), bend=1)
s.add(uke); s.add(tori)
"""
NEW['juji_gatame'] = """uke = lying('uke', 250, 1, y=398)
tori = Fig('tori', 372, 396, ang=94, facing=1)
uke.arm('near', (392, 300), bend=1)
uke.arm('far', (uke.neck[0] - 10, 406), bend=1)
tori.leg('far', (316, 404), bend=1)
tori.leg('near', (300, 390), bend=1)
tori.arm('near', (394, 302), bend=-1)
tori.arm('far', (390, 310), bend=-1)
s.add(uke); s.add(tori)
mark(s, uke.limbs['arm_near'][1], r=24)
"""
NEW['yoko_shiho'] = """uke = lying('uke', 330, 1, y=398)
uke.arm('near', (uke.neck[0] - 20, 350), bend=1)
tori = Fig('tori', 304, 372, ang=180 - 20, facing=1)
tori.leg('far', (250, GROUND - 4), bend=1)
tori.leg('near', (262, GROUND - 4), bend=1)
tori.limbs.pop('leg_near')
tori.arm('near', (uke.head[0], uke.head[1] + 6), bend=1)
tori.arm('far', (uke.pelvis[0] - 30, 404), bend=1)
s.add(uke); s.add(tori)
"""

# ----------------------------------------------------------------- RENRAKU-WAZA
REN = [
    ('ren_deashi_osoto', 'De-ashi-harai → O-soto-gari', 'de_ashi_harai', 'o_soto_gari',
     'Uke recua o pé para escapar da varrida de de-ashi-harai.', 'Tori aproveita o peso de uke atrás e entra com o-soto-gari.', 'mesma direção (frente → trás)'),
    ('ren_kouchi_seoi', 'Ko-uchi-gari → Seoi-nage', 'ko_uchi_gari', 'seoi_nage',
     'Ko-uchi-gari leva uke a avançar o peso para recuperar o equilíbrio.', 'Tori gira e entra com seoi-nage para a frente.', 'direção oposta (trás → frente)'),
    ('ren_ouchi_uchimata', 'O-uchi-gari → Uchi-mata', 'o_uchi_gari', 'uchi_mata',
     'Uke resiste a o-uchi-gari empurrando para a frente e abre as pernas.', 'Tori gira e varre a coxa interna com uchi-mata.', 'direção oposta (trás → frente)'),
    ('ren_ouchi_taiotoshi', 'O-uchi-gari → Tai-otoshi', 'o_uchi_gari', 'tai_otoshi',
     'Uke reage a o-uchi-gari trazendo o peso à frente.', 'Tori abre o corpo e bloqueia a perna com tai-otoshi.', 'direção oposta (trás → frente)'),
    ('ren_sasae_osoto', 'Sasae-tsurikomi-ashi → O-soto-gari', 'sasae_tsurikomi_ashi', 'o_soto_gari',
     'Uke inclina-se para trás para resistir a sasae-tsurikomi-ashi.', 'Tori entra com o-soto-gari na direção da resistência.', 'direção oposta (frente → trás)'),
    ('ren_haraigoshi_osoto', 'Harai-goshi → O-soto-gari', 'harai_goshi', 'o_soto_gari',
     'Uke bloqueia harai-goshi jogando o quadril para trás.', 'Tori muda para o-soto-gari, ceifando a perna de apoio.', 'direção oposta (frente → trás)'),
    ('ren_kosoto_yokootoshi', 'Ko-soto-gari → Yoko-otoshi', 'ko_soto_gari', 'yoko_otoshi',
     'Uke tira o pé da varrida de ko-soto-gari e desloca o peso ao lado.', 'Tori cai de lado e projeta com yoko-otoshi.', 'pé → sacrifício'),
    ('ren_hanegoshi_ouchi', 'Hane-goshi → O-uchi-gari', 'hane_goshi', 'o_uchi_gari',
     'Uke recua o quadril para anular hane-goshi.', 'Tori segue com o-uchi-gari para trás.', 'direção oposta (frente → trás)'),
]
REN_SOLO = [
    ('ren_osoto_kesa', 'O-soto-gari → Kesa-gatame (pé → solo)', kake('o_soto_gari'), NEW['kesa'] if 'kesa' in NEW else kake('kesa_gatame'),
     'Tori projeta com o-soto-gari sem pontuação máxima.', 'Tori segue no solo e imobiliza com kesa-gatame.', ('1. 立技 Tachi-waza', '· projeção'), ('2. 寝技 Ne-waza', '· imobilização')),
    ('ren_kesa_katagatame', 'Kesa-gatame → Kata-gatame (solo)', kake('kesa_gatame'), NEW['kata_gatame'],
     'Uke empurra e solta o braço para escapar de kesa-gatame.', 'Tori prende o braço de uke junto à cabeça e passa a kata-gatame.', ('1. 抑込技 Osaekomi', '· kesa-gatame'), ('2. 抑込技 Osaekomi', '· kata-gatame')),
    ('ren_yokoshiho_juji', 'Yoko-shiho-gatame → Juji-gatame (solo)', NEW['yoko_shiho'], NEW['juji_gatame'],
     'Uke empurra com o braço para escapar de yoko-shiho-gatame.', 'Tori passa a perna sobre a cabeça e aplica juji-gatame no braço estendido.', ('1. 抑込技 Osaekomi', '· yoko-shiho-gatame'), ('2. 関節技 Kansetsu', '· juji-gatame')),
]

# ----------------------------------------------------------------- KAESHI-WAZA
BACK_COUNTER = """uke = Fig('uke', 300, {upy}, ang={uang}, facing=-1)
ux = uke.pelvis[0]
uke.leg('near', (ux + {lx}, {ly}), bend=-1)
uke.leg('far', (ux - 6, {fy}), bend=-1)
uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
uke.arm('far', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
tori = Fig('tori', 336, 318, ang=172, facing=-1)
tori.leg('far', (366, GROUND - 2), bend=1)
tori.leg('near', {tl}, bend=1)
tori.arm('near', uke.at(0.25), bend=1)
tori.arm('far', uke.at(0.6), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] - 10, uke.head[1] - 20), (ux + 110, uke.head[1] - 60), (ux + 150, 330))
mark(s, {tl}, r=24)
"""

KAE = [
    ('kae_osoto_gaeshi', 'O-soto-gaeshi', 'o_soto_gari', swap(kake('o_soto_gari')), kake('o_soto_gari'),
     'Uke ataca com o-soto-gari.', 'Tori resiste, gira o eixo e ceifa de volta a perna que ataca; uke cai para trás.'),
    ('kae_ouchi_gaeshi', 'O-uchi-gaeshi', 'o_uchi_gari', swap(kake('o_uchi_gari')), """tori = standing('tori', 262, 1, lean=-6)
uke = standing('uke', 334, -1, lean=-30)
uke.leg('near', (tori.pelvis[0] + 8, 344), bend=1)
uke.leg('far', (uke.pelvis[0] + 10, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] - 34, GROUND - 2), bend=-1)
grip(tori, uke); tori.arms_top = True
tori.arm('far', (uke.limbs['leg_near'][1][0], uke.limbs['leg_near'][1][1] + 6), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 110, 200), (uke.pelvis[0] + 120, 370))
""", 'Uke engancha a perna de tori por dentro com o-uchi-gari.', 'Tori recua a perna atacada, conduz a perna de uke com o corpo e o projeta para trás.'),
    ('kae_kouchi_gaeshi', 'Ko-uchi-gaeshi', 'ko_uchi_gari', swap(kake('ko_uchi_gari')), """tori = standing('tori', 266, 1, lean=-4)
uke = standing('uke', 336, -1, lean=28)
uke.leg('near', (tori.pelvis[0] + 6, 400), bend=1)
uke.leg('far', (uke.pelvis[0] + 30, 400), bend=1)
tori.leg('near', (tori.pelvis[0] - 30, 392), bend=-1)
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
s.arrow((uke.head[0] - 6, uke.head[1] - 20), (tori.pelvis[0] - 30, 120), (tori.pelvis[0] - 80, 330))
""", 'Uke tenta varrer o calcanhar de tori por dentro com ko-uchi-gari.', 'Tori retira o pé atacado e, com as mãos, gira uke e o projeta no sentido do próprio ataque.'),
    ('kae_hanegoshi_gaeshi', 'Hane-goshi-gaeshi', 'hane_goshi', swap(kake('hane_goshi')),
     BACK_COUNTER.format(upy=300, uang=166, lx=60, ly=320, fy=404, tl='(ux + 4, 398)'),
     'Uke ataca com hane-goshi.', 'Tori baixa o quadril, engancha a perna de apoio de uke e o projeta para trás.'),
    ('kae_haraigoshi_gaeshi', 'Harai-goshi-gaeshi', 'harai_goshi', swap(kake('harai_goshi')),
     BACK_COUNTER.format(upy=298, uang=164, lx=86, ly=300, fy=404, tl='(ux - 6, 402)'),
     'Uke ataca com harai-goshi.', 'Tori varre a perna de apoio de uke enquanto a perna de ataque está no ar.'),
    ('kae_uchimata_gaeshi', 'Uchi-mata-gaeshi', 'uchi_mata', swap(kake('uchi_mata')),
     BACK_COUNTER.format(upy=296, uang=162, lx=90, ly=250, fy=404, tl='(ux - 4, 402)'),
     'Uke ataca com uchi-mata.', 'Tori acompanha o giro e projeta uke de costas sobre a perna de apoio.'),
    ('kae_uchimata_sukashi', 'Uchi-mata-sukashi', 'uchi_mata', swap(kake('uchi_mata')), """tori = Fig('tori', 250, 300, ang=188, facing=1)
tori.leg('far', (226, GROUND - 2), bend=-1)
tori.leg('near', (276, GROUND - 2), bend=-1)
uke = Fig('uke', 324, 270, ang=262, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 20, GROUND - 2), bend=-1)
uke.leg('near', (ux + 110, 222), bend=-1)
tori.arm('near', uke.at(0.9), bend=1)
tori.arm('far', uke.at(0.6), bend=1)
uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 80, 190), (ux - 40, 100), (ux - 120, 330))
mark(s, (296, 330), r=30)
""", 'Uke ataca com uchi-mata.', 'Tori esquiva a perna de ataque (sukashi): a perna de uke passa no vazio e tori o gira para a frente.'),
    ('kae_tsubame_gaeshi', 'Tsubame-gaeshi', 'de_ashi_harai', swap(kake('de_ashi_harai')), kake('de_ashi_harai'),
     'Uke tenta varrer o pé de tori com de-ashi-harai.', 'Tori ergue o pé, deixa a varrida passar e varre o pé de uke com o outro pé.'),
]

# ----------------------------------------------------------------- PROIBIDAS
PRO = [
    ('pro_kani_basami', 'Kani-basami', 'HANSOKU-MAKE', """uke = standing('uke', 340, -1, lean=-12)
tori = Fig('tori', 306, 320, ang=262, facing=1)
tori.leg('near', (uke.pelvis[0] + 50, 290), bend=1)
tori.leg('far', (uke.pelvis[0] + 46, 378), bend=1)
tori.arm('near', (tori.neck[0] - 4, 404), bend=1)
tori.arm('far', (tori.neck[0] + 20, 406), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 110, 200), (uke.pelvis[0] + 120, 370))
""", 'Tori salta de lado e prende o tronco e as pernas de uke em tesoura, derrubando-o para trás. Hansoku-make direto (art. 18.2.2).'),
    ('pro_kawazu_gake', 'Kawazu-gake', 'HANSOKU-MAKE', """tori = Fig('tori', 290, 304, ang=204, facing=1)
uke = standing('uke', 336, -1, lean=-18)
tori.leg('far', (266, GROUND - 2), bend=-1)
tori.leg('near', (uke.pelvis[0] + 20, 360), bend=-1)
tori.limbs['leg_near'] = (tori.pelvis, (uke.pelvis[0] + 24, 350), (uke.pelvis[0] - 18, 382))
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.95), bend=-1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 40, 120), (uke.pelvis[0] - 120, 330))
""", 'Tori enrola a perna na perna de uke e cai para trás junto com ele. Hansoku-make direto (art. 18.2.2).'),
    ('pro_do_jime', 'Do-jime', 'HANSOKU-MAKE', """uke = Fig('uke', 340, 392, ang=200, facing=1)
uke.leg('near', (450, GROUND - 4), bend=-1)
uke.leg('far', (440, 404), bend=-1)
uke.arm('near', (uke.neck[0] + 30, uke.neck[1] + 60), bend=-1)
tori = Fig('tori', 282, 396, ang=152, facing=1)
tori.leg('near', (uke.at(0.25)[0] + 34, uke.at(0.25)[1] + 4), bend=-1)
tori.leg('far', (uke.at(0.3)[0] + 30, uke.at(0.3)[1] + 18), bend=-1)
tori.arm('near', uke.at(0.9), bend=-1)
tori.arm('far', uke.at(0.7), bend=-1)
s.add(tori); s.add(uke)
mark(s, uke.at(0.25), r=40)
""", 'Tori aperta o tronco (rins ou abdômen) de uke com as pernas em tesoura. Hansoku-make direto (art. 18.2.2).'),
    ('pro_ashi_garami', 'Ashi-garami', 'HANSOKU-MAKE', """uke = standing('uke', 360, -1, lean=24)
uke.leg('near', (296, 404), bend=1)
tori = Fig('tori', 230, 396, ang=94, facing=1)
tori.leg('near', (uke.limbs['leg_near'][1][0] + 10, uke.limbs['leg_near'][1][1] - 10), bend=1)
tori.leg('far', (uke.limbs['leg_near'][1][0] + 20, uke.limbs['leg_near'][1][1] + 30), bend=1)
tori.arm('near', uke.limbs['leg_near'][2], bend=-1)
tori.arm('far', (uke.limbs['leg_near'][2][0] + 6, uke.limbs['leg_near'][2][1] - 8), bend=-1)
s.add(uke); s.add(tori)
mark(s, uke.limbs['leg_near'][1], r=30)
""", 'Tori entrelaça a perna de uke e torce a articulação do joelho. Hansoku-make direto (art. 18.2.2).'),
    ('pro_mergulho', 'Mergulho de cabeça (diving)', 'HANSOKU-MAKE', """tori = Fig('tori', 296, 292, ang=14, facing=-1)
tori.leg('far', (260, 200), bend=-1)
tori.leg('near', (330, 210), bend=1)
uke = Fig('uke', 318, 236, ang=268, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 80, 180), bend=-1)
uke.leg('near', (ux + 90, 210), bend=-1)
tori.arm('near', uke.at(0.8), bend=1)
tori.arm('far', (tori.head[0] - 40, GROUND - 4), bend=1)
uke.arm('near', (uke.neck[0] - 20, uke.neck[1] + 50), bend=1)
s.add(uke); s.add(tori)
mark(s, (tori.head[0], tori.head[1] + 6), r=30)
""", 'Tori apoia a cabeça no tatame ao projetar (ex.: uchi-mata, seoi-nage). Hansoku-make, podendo seguir na competição (art. 18.2.1).'),
    ('pro_kansetsu_pe', 'Kansetsu-waza aplicado em pé', 'HANSOKU-MAKE', """uke = Fig('uke', 340, 300, ang=232, facing=-1)
uke.leg('far', (370, GROUND - 2), bend=-1)
uke.leg('near', (340, GROUND - 2), bend=-1)
tori = Fig('tori', 300, 318, ang=228, facing=-1)
tori.leg('far', (316, GROUND - 2), bend=1)
tori.leg('near', (268, GROUND - 2), bend=1)
uke.arm('near', (tori.at(0.6)[0] - 40, tori.at(0.6)[1] - 10), bend=1)
tori.arm('near', (uke.limbs['arm_near'][2][0] + 6, uke.limbs['arm_near'][2][1] + 4), bend=1)
tori.arm('far', uke.limbs['arm_near'][1], bend=1)
s.add(uke); s.add(tori)
mark(s, uke.limbs['arm_near'][1], r=26)
s.arrow((uke.head[0] + 10, uke.head[1] - 20), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 120, 360))
""", 'Chave de braço aplicada durante a projeção, sem chance de escape para uke. Hansoku-make; com risco menor, shido (art. 18).'),
    ('pro_pegar_pernas', 'Agarrar as pernas em pé', 'SHIDO', """uke = standing('uke', 340, -1, lean=-8)
tori = Fig('tori', 280, 334, ang=124, facing=1)
tori.leg('far', (246, GROUND - 2), bend=-1)
tori.leg('near', (300, GROUND - 2), bend=-1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', uke.limbs['leg_far'][1], bend=1)
s.add(uke); s.add(tori)
mark(s, uke.limbs['leg_near'][1], r=30)
""", 'Agarrar, bloquear ou tocar as pernas com as mãos em tachi-waza. Shido; só é permitido em ne-waza já estabelecido (art. 18.1.2).'),
    ('pro_ushiro_sankaku', 'Ushiro-sankaku de alto risco', 'HANSOKU-MAKE', """uke = Fig('uke', 330, 396, ang=210, facing=1)
uke.leg('near', (440, GROUND - 4), bend=-1)
uke.leg('far', (430, 404), bend=-1)
uke.arm('near', (uke.neck[0] + 40, uke.neck[1] + 50), bend=-1)
tori = Fig('tori', 230, 398, ang=104, facing=1)
tori.leg('near', (uke.neck[0] + 30, uke.neck[1] - 4), bend=1)
tori.leg('far', (uke.neck[0] + 26, uke.neck[1] + 22), bend=1)
tori.arm('near', uke.at(0.6), bend=-1)
s.add(uke); s.add(tori)
mark(s, uke.neck, r=30)
""", 'Triângulo de pernas por trás do pescoço de uke em ne-waza, com risco ao pescoço e à coluna. Hansoku-make desde jan./2026.'),
    ('pro_cair_costas', 'Cair para trás com o oponente nas costas', 'HANSOKU-MAKE', """tori = Fig('tori', 300, 316, ang=208, facing=1)
tori.leg('far', (330, GROUND - 2), bend=-1)
tori.leg('near', (350, GROUND - 2), bend=-1)
uke = Fig('uke', 262, 300, ang=196, facing=1)
uke.leg('near', (300, 360), bend=-1)
uke.leg('far', (310, 380), bend=-1)
uke.arm('near', tori.neck, bend=-1)
uke.arm('far', tori.at(0.8), bend=-1)
tori.arm('near', (tori.neck[0] - 20, tori.neck[1] - 30), bend=-1)
s.add(uke); s.add(tori)
s.arrow((tori.head[0] + 10, tori.head[1] - 20), (tori.head[0] - 90, tori.head[1] - 30), (tori.head[0] - 140, 360))
""", 'Com uke agarrado às suas costas, tori se joga para trás de propósito, controlando a queda. Hansoku-make direto (art. 18.2.2).'),
]

HEADER = '''"""{title}
{desc}
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)
'''


def ind(code):
    return ''.join('    ' + l + '\n' if l.strip() else '\n' for l in code.strip('\n').split('\n'))


def write(name, title, desc, scenes, heads, captions, badges=None):
    src = HEADER.format(title=title, desc=desc)
    for i, code in enumerate(scenes):
        src += f'\n\ndef quadro{i+1}():\n    s = Scene()\n{ind(code)}    return s\n'
    calls = ', '.join(f'quadro{i+1}()' for i in range(len(scenes)))
    src += f"\n\nif __name__ == '__main__':\n    print(panels({name!r}, [{calls}], {heads!r}, {title!r}, {captions!r}, badges={badges!r}))\n"
    with open(os.path.join(HERE, f'ext_{name}.py'), 'w', encoding='utf-8') as f:
        f.write(src)


def write_all():
    n = 0
    for name, title, a, b, c1, c2, kind in REN:
        write(name, title, f'Renraku-waza em pé: {kind}.', [tsukuri(a), kake(b)],
              [('1. 連絡 1º ataque', '· ' + SCENES[a][0].split(' (')[0]), ('2. 連絡 2º ataque', '· ' + SCENES[b][0].split(' (')[0])],
              [c1, c2]); n += 1
    for name, title, s1, s2, c1, c2, h1, h2 in REN_SOLO:
        write(name, title, 'Renraku-waza envolvendo o solo.', [s1, s2], [h1, h2], [c1, c2]); n += 1
    for name, title, base, s1, s2, c1, c2 in KAE:
        write(name, title, 'Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.', [s1, s2],
              [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], [c1, c2]); n += 1
    for name, title, pen, code, cap in PRO:
        color = '#E08A00' if pen == 'SHIDO' else '#C8102E'
        write(name, title, f'Técnica/ação proibida — {pen} (IJF SOR, art. 18).', [code], [('禁止 Proibido', '· ' + pen.lower())], [cap],
              badges=[(pen, color)]); n += 1
    return n


if __name__ == '__main__':
    print(write_all(), 'scripts ext_*.py gerados')
