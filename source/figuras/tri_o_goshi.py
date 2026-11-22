"""O-goshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori entra fundo com o quadril, abaixo do centro de uke.
Kake: Eleva uke sobre o quadril e gira, lançando-o por cima.
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
    tori = Fig('tori', 300, 322, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.15), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 312, ang=192, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 20, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke = Fig('uke', 330, 292, ang=236, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 50, 392), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 78, 372), bend=-1)
    tori.arm('near', uke.at(0.15), bend=1)
    tori.arm('far', (tori.pelvis[0] - 72, 262), bend=-1)
    uke.arm('near', (tori.neck[0] - 20, tori.neck[1] + 20), bend=1)
    uke.arm('far', (tori.pelvis[0] - 68, 260), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 40, 210), (uke.pelvis[0] - 90, 120), (uke.pelvis[0] - 170, 300))
    return s


if __name__ == '__main__':
    print(triptych('tri_o_goshi', [kuzushi(), tsukuri(), kake()], 'O-goshi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori entra fundo com o quadril, abaixo do centro de uke.', 'Eleva uke sobre o quadril e gira, lançando-o por cima.']))
