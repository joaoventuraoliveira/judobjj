"""Harai-tsurikomi-ashi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori puxa e eleva, levando o pé à frente do tornozelo de uke.
Kake: Varre o tornozelo pela frente e lança.
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
    tori.leg('near', (uke.pelvis[0] - 66, 398), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, (uke.pelvis[0] - 44, 404), r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=-14)
    uke = standing('uke', 340, -1, lean=18)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 46, 392), bend=1)
    tori.leg('near', (ux - 50, 396), bend=-1)
    s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 20, 120), (tx - 60, 330))

    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(triptych('tri_harai_tsurikomi_ashi', [kuzushi(), tsukuri(), kake()], 'Harai-tsurikomi-ashi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori puxa e eleva, levando o pé à frente do tornozelo de uke.', 'Varre o tornozelo pela frente e lança.']))
