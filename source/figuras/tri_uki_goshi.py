"""Uki-goshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori entra com o quadril e envolve a cintura de uke com o braço.
Kake: Gira e lança uke sobre o quadril, sem elevá-lo.
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
    tori = Fig('tori', 300, 316, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.18), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 312, ang=190, facing=-1)
    uke = Fig('uke', 330, 300, ang=228, facing=-1)
    tx, ux = tori.pelvis[0], uke.pelvis[0]

    tori.leg('far', (tx + 20, GROUND - 2), bend=1)
    tori.leg('near', (tx - 26, GROUND - 2), bend=1)
    uke.leg('far', (ux + 40, GROUND - 2), bend=-1)
    uke.leg('near', (ux + 66, 380), bend=-1)
    tori.arm('near', uke.at(0.18), bend=1)
    tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
    uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
    uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 50, 220), (ux - 90, 220 - 90), (ux - 175, 330))
    return s


if __name__ == '__main__':
    print(triptych('tri_uki_goshi', [kuzushi(), tsukuri(), kake()], 'Uki-goshi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori entra com o quadril e envolve a cintura de uke com o braço.', 'Gira e lança uke sobre o quadril, sem elevá-lo.']))
