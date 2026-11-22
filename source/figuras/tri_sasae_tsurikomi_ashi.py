"""Sasae-tsurikomi-ashi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori bloqueia a perna de apoio logo acima do tornozelo.
Kake: Inclina-se para trás e gira, lançando uke por cima do bloqueio.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    tori = standing('tori', 262, 1, lean=-8)
    uke = standing('uke', 342, -1, lean=20)
    uke.leg('far', (uke.pelvis[0] + 26, 408), bend=1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    kuzushi_arrow(s, add(uke.at(0.95), (-6, -14)), (-78, 34))
    return s


def tsukuri():
    s = Scene()
    tori = standing('tori', 258, 1, lean=-10)
    uke = standing('uke', 340, -1, lean=14)
    uke.leg('near', (uke.pelvis[0] - 44, 406), bend=1)
    tori.leg('near', (uke.pelvis[0] - 48, 392), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, (uke.pelvis[0] - 44, 394), r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=-16)
    uke = standing('uke', 340, -1, lean=22)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 38, GROUND - 2), bend=1)
    k, f = uke.limbs['leg_near'][1], uke.limbs['leg_near'][2]
    tori.leg('near', (k[0] + (f[0]-k[0])*0.78, k[1] + (f[1]-k[1])*0.78), bend=-1)
    s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))

    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(triptych('tri_sasae_tsurikomi_ashi', [kuzushi(), tsukuri(), kake()], 'Sasae-tsurikomi-ashi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori bloqueia a perna de apoio logo acima do tornozelo.', 'Inclina-se para trás e gira, lançando uke por cima do bloqueio.']))
