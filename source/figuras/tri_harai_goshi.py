"""Harai-goshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori puxa uke junto ao quadril e gira, com a perna pronta para varrer.
Kake: Varre a coxa de uke com a parte de trás da coxa.
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
    tori = Fig('tori', 300, 312, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 304, ang=222, facing=-1)
    uke = Fig('uke', 338, 270, ang=246, facing=-1)
    tx, ux = tori.pelvis[0], uke.pelvis[0]

    tori.leg('far', (tx - 4, GROUND - 2), bend=1)
    uke.leg('far', (ux + 48, 372), bend=-1)
    uke.leg('near', (ux + 66, 270), bend=-1)
    tori.leg('near', (tx + 110, 276), bend=1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
    uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
    uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 50, 180), (ux - 90, 180 - 90), (ux - 175, 330))
    return s


if __name__ == '__main__':
    print(triptych('tri_harai_goshi', [kuzushi(), tsukuri(), kake()], 'Harai-goshi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori puxa uke junto ao quadril e gira, com a perna pronta para varrer.', 'Varre a coxa de uke com a parte de trás da coxa.']))
