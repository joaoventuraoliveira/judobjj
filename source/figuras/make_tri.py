"""
make_tri.py — gera tri_<nome>.py: cada técnica do Gokyo em três quadros
1. 崩し Kuzushi (desequilíbrio)  2. 作り Tsukuri (entrada)  3. 掛け Kake (execução)

Critério oficial (IJF/Kodokan Classification of Judo Techniques, 2017):
- kuzushi: ação de desequilibrar o oponente preparando a projeção;
- tsukuri: ação de preparar a projeção depois de quebrar o equilíbrio;
- kake: ação de executar a técnica.
A direção do kuzushi de cada técnica segue a descrição oficial da técnica.
O quadro 3 (kake) reaproveita as cenas validadas em make_scripts.py.
Uso: python3 make_tri.py && python3 run_tri.py
"""
import os
from make_scripts import SCENES

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- quadro 1: kuzushi ----------------
KZ = {
    'F': ("""tori = standing('tori', 262, 1, lean=-8)
uke = standing('uke', 342, -1, lean=20)
uke.leg('far', (uke.pelvis[0] + 26, 408), bend=1)
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
kuzushi_arrow(s, add(uke.at(0.95), (-6, -14)), (-78, 34))
""", 'Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.'),
    'B': ("""tori = standing('tori', 266, 1, lean=14)
uke = standing('uke', 340, -1, lean=-18)
uke.leg('near', (uke.pelvis[0] - 30, GROUND - 2), bend=1)
grip(tori, uke); tori.arms_top = True
s.add(tori); s.add(uke)
kuzushi_arrow(s, add(uke.at(0.95), (6, -14)), (80, 36))
""", 'Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.'),
    'L': ("""tori = standing('tori', 262, 1, lean=-4)
uke = standing('uke', 342, -1, lean=6)
uke.leg('near', (uke.pelvis[0] - 40, GROUND - 2), bend=1)
uke.leg('far', (uke.pelvis[0] + 24, 404), bend=1)
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
kuzushi_arrow(s, uke.at(0.55), (-30, 86))
mark(s, uke.limbs['leg_near'][2], r=22)
""", 'Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.'),
    'UP': ("""uke = Fig('uke', 292, 300, ang=204, facing=-1)
uke.leg('far', (318, GROUND - 2), bend=-1)
uke.leg('near', (262, GROUND - 2), bend=-1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 50), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
tori = Fig('tori', 342, 322, ang=176, facing=-1)
tori.leg('far', (368, GROUND - 2), bend=1)
tori.leg('near', (316, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.2), bend=1)
tori.arm('far', uke.at(0.35), bend=1)
s.add(uke); s.add(tori)
kuzushi_arrow(s, add(uke.pelvis, (-10, -20)), (0, -90))
""", 'Contragolpe: uke ataca com o quadril; tori baixa o quadril e bloqueia, tirando uke do chão para cima.'),
    'PULL': ("""tori = standing('tori', 272, 1, lean=-6)
uke = standing('uke', 336, -1, lean=16)
grip(tori, uke); tori.arms_top = True
tori.arm('near', uke.at(0.3), bend=1)
s.add(uke); s.add(tori)
kuzushi_arrow(s, add(uke.at(0.9), (0, -16)), (-70, 20))
""", 'Para a frente, contra o corpo de tori: tori traz uke para junto de si.'),
}

# ---------------- quadro 2: tsukuri ----------------
def tk_turn(tpy=316, tn='uke.at(0.82)', leg=None, cap=''):
    leg_code = f"tori.leg('near', {leg}, bend=1)" if leg else "tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)"
    return (f"""tori = Fig('tori', 300, {tpy}, ang=190, facing=-1)
uke = Fig('uke', 340, 298, ang=212, facing=-1)
tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
{leg_code}
uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
tori.arm('near', {tn}, bend=1)
tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
s.add(uke); s.add(tori)
""", cap)


def tk_reap(foot, tlean=18, ulean=-20, uke_target=None, cap=''):
    ut = f"uke.leg('near', {uke_target}, bend=1)" if uke_target else ''
    return (f"""tori = standing('tori', 280, 1, lean={tlean})
uke = standing('uke', 342, -1, lean={ulean})
{ut}
tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
tori.leg('near', {foot}, bend=-1)
grip(tori, uke); tori.arms_top = True
s.add(tori); s.add(uke)
mark(s, {foot}, r=24)
""", cap)


def tk_sweep(foot, target, cap=''):
    return (f"""tori = standing('tori', 258, 1, lean=-10)
uke = standing('uke', 340, -1, lean=14)
uke.leg('near', (uke.pelvis[0] - 44, 406), bend=1)
tori.leg('near', {foot}, bend=-1)
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
mark(s, {target}, r=24)
""", cap)


def tk_sutemi_back(on='uke.at(0.1)', cap=''):
    return (f"""uke = standing('uke', 342, -1, lean=24)
tori = Fig('tori', 280, 352, ang=160, facing=1)
tori.leg('far', (250, GROUND - 2), bend=-1)
tori.leg('near', {on}, bend=-1)
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
mark(s, {on}, r=24)
""", cap)


def tk_sutemi_side(ulean=10, ufacing=-1, cap=''):
    return (f"""uke = standing('uke', 340, {ufacing}, lean={ulean})
tori = Fig('tori', 272, 336, ang=206, facing=1)
tori.leg('far', (236, GROUND - 2), bend=-1)
tori.leg('near', (uke.pelvis[0] - 6, 410), bend=-1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.55), bend=-1)
uke.arm('near', tori.at(0.8), bend=1)
uke.arm('far', tori.at(0.55), bend=1)
tori.arms_top = True
s.add(uke); s.add(tori)
mark(s, (uke.pelvis[0] - 6, 410), r=24)
""", cap)


def tk_lift_behind(cap=''):
    return ("""uke = Fig('uke', 292, 292, ang=200, facing=-1)
uke.leg('far', (318, 410), bend=-1)
uke.leg('near', (262, 408), bend=-1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 50), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
tori = Fig('tori', 336, 334, ang=170, facing=-1)
tori.leg('far', (364, GROUND - 2), bend=1)
tori.leg('near', (310, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.15), bend=1)
tori.arm('far', uke.at(0.3), bend=1)
s.add(uke); s.add(tori)
mark(s, uke.at(0.15), r=28)
""", cap)


def tk_hug_front(arms='waist', cap=''):
    tgt = "uke.at(0.15)" if arms == 'waist' else "uke.limbs['leg_near'][1]"
    return (f"""uke = standing('uke', 334, -1, lean=6)
tori = Fig('tori', 290, 336, ang=150, facing=1)
tori.leg('far', (258, GROUND - 2), bend=-1)
tori.leg('near', (312, GROUND - 2), bend=-1)
tori.arm('near', {tgt}, bend=1)
tori.arm('far', uke.at(0.25), bend=1)
uke.arm('near', tori.at(0.9), bend=-1)
uke.arm('far', tori.at(0.7), bend=-1)
s.add(uke); s.add(tori)
mark(s, {tgt}, r=26)
""", cap)


def tk_kata_guruma(cap=''):
    return ("""uke = standing('uke', 340, -1, lean=22)
tori = Fig('tori', 296, 344, ang=146, facing=1)
tori.leg('far', (262, GROUND - 2), bend=-1)
tori.leg('near', (318, GROUND - 2), bend=-1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', uke.at(0.9), bend=-1)
uke.arm('near', (tori.neck[0] - 30, tori.neck[1] + 30), bend=1)
uke.arm('far', (tori.neck[0] - 20, tori.neck[1] + 50), bend=1)
s.add(uke); s.add(tori)
mark(s, uke.limbs['leg_near'][1], r=26)
""", cap)


def tk_drop(cap=''):
    return ("""uke = standing('uke', 344, -1, lean=28)
uke.leg('near', (uke.pelvis[0] - 44, GROUND - 2), bend=1)
tori = Fig('tori', 256, 352, ang=186, facing=1)
tori.leg('far', (306, GROUND - 2), bend=-1)
tori.limbs['leg_near'] = (tori.pelvis, (226, 410), (186, 412))
grip(tori, uke); tori.arms_top = True
s.add(uke); s.add(tori)
mark(s, (226, 410), r=22)
""", cap)


SPEC = [
    # nome, kuzushi, tsukuri, legenda do kake
    ('de_ashi_harai', 'L', tk_sweep('(uke.pelvis[0] - 62, 400)', 'uke.limbs[\'leg_near\'][2]', 'Tori acompanha o passo e leva a sola do pé ao pé de uke que vai receber o peso.'), 'Varre o pé avançado no instante do apoio.'),
    ('hiza_guruma', 'F', tk_sweep('uke.limbs[\'leg_near\'][1]', 'uke.limbs[\'leg_near\'][1]', 'Tori apoia a sola do pé no joelho de uke como fulcro.'), 'Gira uke sobre o joelho bloqueado, puxando o tronco.'),
    ('sasae_tsurikomi_ashi', 'F', tk_sweep('(uke.pelvis[0] - 48, 392)', '(uke.pelvis[0] - 44, 394)', 'Tori bloqueia a perna de apoio logo acima do tornozelo.'), 'Inclina-se para trás e gira, lançando uke por cima do bloqueio.'),
    ('uki_goshi', 'F', tk_turn(316, 'uke.at(0.18)', cap='Tori entra com o quadril e envolve a cintura de uke com o braço.'), 'Gira e lança uke sobre o quadril, sem elevá-lo.'),
    ('o_soto_gari', 'B', tk_reap('(uke.pelvis[0] + 10, 330)', 22, -24, cap='Tori pisa ao lado de uke, cola o peito e prepara a perna de ceifa.'), 'Ceifa por trás a perna de apoio; uke cai para trás.'),
    ('o_goshi', 'F', tk_turn(322, 'uke.at(0.15)', cap='Tori entra fundo com o quadril, abaixo do centro de uke.'), 'Eleva uke sobre o quadril e gira, lançando-o por cima.'),
    ('o_uchi_gari', 'B', tk_reap('(uke.pelvis[0] - 6, 404)', 16, -16, cap='Tori entra fundo entre as pernas de uke, com a base dele aberta.'), 'Ceifa por dentro a perna de uke; ele cai para trás.'),
    ('seoi_nage', 'F', tk_turn(338, 'uke.at(0.78)', cap='Tori gira com o cotovelo sob a axila de uke e encaixa as costas no peito dele.'), 'Carrega uke nas costas e o lança por cima do ombro.'),
    ('ko_soto_gari', 'B', tk_reap('(uke.pelvis[0] - 26, 406)', 10, -16, '(uke.pelvis[0] - 34, GROUND - 2)', 'Tori posiciona a sola do pé atrás do calcanhar de uke.'), 'Varre o calcanhar por trás; uke cai para trás.'),
    ('ko_uchi_gari', 'B', tk_reap('(uke.pelvis[0] - 18, 406)', 10, -14, '(uke.pelvis[0] - 44, GROUND - 2)', 'Tori leva a sola do pé por dentro, junto ao calcanhar de uke.'), 'Varre o calcanhar por dentro; uke cai para trás.'),
    ('koshi_guruma', 'F', tk_turn(318, 'uke.neck', cap='Tori envolve o pescoço de uke e encaixa o quadril além do dele.'), 'Roda uke sobre os quadris com amplo movimento.'),
    ('tsurikomi_goshi', 'F', tk_turn(340, 'uke.at(0.97)', cap='Tori desce o quadril abaixo das coxas de uke, puxando a gola para cima.'), 'Eleva com as duas mãos e lança uke sobre os quadris.'),
    ('okuri_ashi_harai', 'L', tk_sweep('(uke.pelvis[0] - 30, 404)', '(uke.pelvis[0] - 20, 404)', 'Tori acompanha o deslocamento lateral de uke, com o pé junto aos pés dele.'), 'Varre os dois pés juntos; uke cai de costas.'),
    ('tai_otoshi', 'F', tk_turn(318, leg='(tori.pelvis[0] + 70, GROUND - 2)', cap='Tori abre o corpo e põe o pé à frente do pé de uke.'), 'Puxa para baixo com as duas mãos sobre a perna estendida.'),
    ('harai_goshi', 'F', tk_turn(312, cap='Tori puxa uke junto ao quadril e gira, com a perna pronta para varrer.'), 'Varre a coxa de uke com a parte de trás da coxa.'),
    ('uchi_mata', 'F', tk_turn(306, leg='(tori.pelvis[0] + 40, GROUND - 2)', cap='Tori abre os pés de uke e entra com a perna entre as dele.'), 'Varre fundo a coxa interna de uke, girando.'),
    ('ko_soto_gake', 'B', tk_reap('(uke.pelvis[0] + 8, 398)', 12, -20, '(uke.pelvis[0] - 14, GROUND - 2)', 'Tori engancha o tornozelo de uke por trás com o pé.'), 'Empurra para trás com o gancho; uke cai de costas.'),
    ('tsuri_goshi', 'F', tk_turn(318, 'uke.at(0.12)', cap='Tori alcança o cinto de uke e puxa-o para a frente.'), 'Eleva uke pelo cinto sobre os quadris e o lança.'),
    ('yoko_otoshi', 'L', tk_sutemi_side(-6, cap='Tori desliza a perna por fora do pé de uke e começa a cair de lado.'), 'Cai de lado e lança uke para o mesmo lado.'),
    ('ashi_guruma', 'F', tk_turn(304, leg='(tori.pelvis[0] + 60, 380)', cap='Tori gira e estende a perna até o joelho de uke.'), 'Lança uke num círculo por cima da perna estendida.'),
    ('hane_goshi', 'F', tk_turn(310, leg='(tori.pelvis[0] + 40, 380)', cap='Tori traz uke junto ao lado e dobra a perna contra a coxa dele.'), 'Lança com impulso para cima do quadril e da perna.'),
    ('harai_tsurikomi_ashi', 'F', tk_sweep('(uke.pelvis[0] - 66, 398)', '(uke.pelvis[0] - 44, 404)', 'Tori puxa e eleva, levando o pé à frente do tornozelo de uke.'), 'Varre o tornozelo pela frente e lança.'),
    ('tomoe_nage', 'F', tk_sutemi_back('uke.at(0.08)', 'Tori entra sob uke e apoia o pé no abdômen inferior dele.'), 'Cai para trás e lança uke por cima da cabeça.'),
    ('kata_guruma', 'F', tk_kata_guruma('Tori desce sob uke, com o braço entre as pernas e a nuca sob o tronco dele.'), 'Eleva uke sobre os ombros e o lança à frente.'),
    ('sumi_gaeshi', 'F', tk_sutemi_back("uke.limbs['leg_near'][1]", 'Tori entra baixo e apoia o peito do pé atrás da coxa de uke.'), 'Cai para trás e lança uke por cima da cabeça.'),
    ('tani_otoshi', 'B', tk_sutemi_side(-16, cap='Tori desliza a perna por trás dos pés de uke e começa a cair de lado.'), 'Cai de lado; uke vai ao canto traseiro.'),
    ('hane_makikomi', 'F', tk_turn(312, leg='(tori.pelvis[0] + 40, 380)', cap='A partir do hane-goshi, tori solta a mão e envolve o braço de uke.'), 'Gira enrolando uke e cai à frente junto com ele.'),
    ('sukui_nage', 'B', tk_hug_front('legs', 'Ao lado de uke, tori desce e envolve as coxas dele.'), 'Eleva uke e o projeta para trás.'),
    ('utsuri_goshi', 'UP', tk_lift_behind('Tori flexiona os joelhos e envolve a cintura de uke.'), 'Eleva uke, troca o quadril e o projeta girando.'),
    ('o_guruma', 'F', tk_turn(304, leg='(tori.pelvis[0] + 60, 330)', cap='Tori conduz o passo de uke e estende a perna à altura do quadril dele.'), 'Gira uke sobre a perna estendida.'),
    ('soto_makikomi', 'F', tk_turn(316, 'uke.at(0.7)', cap='Tori solta a pegada e prende o braço de uke na axila.'), 'Enrola o corpo de uke ao redor do seu e cai à frente.'),
    ('uki_otoshi', 'F', tk_drop('Tori recua e desce sobre um joelho, mantendo uke flutuando à frente.'), 'Puxa para baixo e projeta uke em círculo.'),
    ('o_soto_guruma', 'B', tk_reap('(uke.pelvis[0] + 40, 344)', 22, -24, cap='Tori estende a perna atrás dos dois joelhos de uke.'), 'Roda uke para trás por cima da perna.'),
    ('uki_waza', 'F', tk_sutemi_side(18, cap='Tori abre o corpo e estende a perna bloqueando o pé de uke.'), 'Cai de lado e projeta uke por cima de si.'),
    ('yoko_wakare', 'F', tk_sutemi_side(22, cap='Tori se lança à frente de uke, estendendo as pernas.'), 'Cai de lado e lança uke sobre o corpo estendido.'),
    ('yoko_guruma', 'F', tk_sutemi_side(24, cap='Tori envolve a cintura de uke e desliza a perna entre as pernas dele.'), 'Cai de lado e projeta uke por cima da cabeça.'),
    ('ushiro_goshi', 'UP', tk_lift_behind('Tori se afasta do ataque e envolve a cintura de uke por trás.'), 'Levanta uke no ar e o arremessa de costas.'),
    ('ura_nage', 'PULL', tk_hug_front('waist', 'Tori envolve a cintura de uke com os dois braços e o cola ao corpo.'), 'Levanta e cai para trás, projetando uke por cima do ombro.'),
    ('sumi_otoshi', 'B', tk_reap('(uke.pelvis[0] - 34, GROUND - 2)', 12, -24, cap='Tori pisa ao lado externo do pé de uke.'), 'Projeta uke ao canto traseiro só com o corpo e as mãos.'),
    ('yoko_gake', 'F', tk_sutemi_side(12, cap='Tori leva a sola do pé ao pé de uke, na direção do dedo mínimo.'), 'Varre o pé e cai de lado, projetando uke.'),
]

TITLES = {n: SCENES[n][0] for n in SCENES}

TEMPLATE = '''"""{title} em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: {kzcap}
Tsukuri: {tkcap}
Kake: {kkcap}
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
{kz}    return s


def tsukuri():
    s = Scene()
{tk}    return s


def kake():
    s = Scene()
{kk}    return s


if __name__ == '__main__':
    print(triptych('tri_{name}', [kuzushi(), tsukuri(), kake()], {title!r},
                   [{kzcap!r}, {tkcap!r}, {kkcap!r}]))
'''


def indent(code):
    return ''.join('    ' + line + '\n' if line.strip() else '\n' for line in code.strip('\n').split('\n'))


def write_all():
    for name, kz, (tk_code, tk_cap), kk_cap in SPEC:
        kz_code, kz_cap = KZ[kz]
        title = TITLES[name].split(' (')[0]
        kk_code = SCENES[name][2]
        src = TEMPLATE.format(title=title, name=name, kz=indent(kz_code), tk=indent(tk_code), kk=indent(kk_code),
                              kzcap=kz_cap, tkcap=tk_cap, kkcap=kk_cap)
        with open(os.path.join(HERE, f'tri_{name}.py'), 'w', encoding='utf-8') as f:
            f.write(src)
    return len(SPEC)


if __name__ == '__main__':
    print(write_all(), 'scripts tri_*.py gerados')
