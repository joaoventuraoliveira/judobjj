"""Uchi-mata em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori abre os pés de uke e entra com a perna entre as dele.
Kake: Varre fundo a coxa interna de uke, girando.
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
    tori = Fig('tori', 300, 306, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] + 40, GROUND - 2), bend=1)
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
    tori = Fig('tori', 290, 300, ang=232, facing=-1)
    tori.leg('far', (tori.pelvis[0] - 8, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] + 112, 214), bend=1)
    uke = Fig('uke', 340, 250, ang=250, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 40, 360), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 92, 196), bend=-1)
    tori.arm('near', uke.at(0.85), bend=1)
    tori.arm('far', (tori.neck[0] - 60, tori.neck[1] + 70), bend=-1)
    uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 30), bend=1)
    uke.arm('far', (tori.neck[0] - 55, tori.neck[1] + 66), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 70, 170), (uke.pelvis[0] - 60, 90), (uke.pelvis[0] - 170, 260))
    return s


if __name__ == '__main__':
    print(triptych('tri_uchi_mata', [kuzushi(), tsukuri(), kake()], 'Uchi-mata',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori abre os pés de uke e entra com a perna entre as dele.', 'Varre fundo a coxa interna de uke, girando.']))
