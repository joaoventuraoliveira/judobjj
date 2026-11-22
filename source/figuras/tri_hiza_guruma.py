"""Hiza-guruma em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori apoia a sola do pé no joelho de uke como fulcro.
Kake: Gira uke sobre o joelho bloqueado, puxando o tronco.
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
    tori.leg('near', uke.limbs['leg_near'][1], bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=-12)
    uke = standing('uke', 340, -1, lean=22)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 36, GROUND - 2), bend=1)
    tori.leg('near', uke.limbs['leg_near'][1], bend=-1)
    s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))

    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(triptych('tri_hiza_guruma', [kuzushi(), tsukuri(), kake()], 'Hiza-guruma',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori apoia a sola do pé no joelho de uke como fulcro.', 'Gira uke sobre o joelho bloqueado, puxando o tronco.']))
