"""Yoko-wakare em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori se lança à frente de uke, estendendo as pernas.
Kake: Cai de lado e lança uke sobre o corpo estendido.
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
    uke = standing('uke', 340, -1, lean=22)
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
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 396, ang=272, facing=-1)
    tori.leg('far', (412, 408), bend=1)
    tori.leg('near', (420, 398), bend=1)
    uke = Fig('uke', 382, 286, ang=238, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 20, GROUND - 2), bend=-1)
    uke.leg('near', (ux + 44, 392), bend=-1)
    uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 70), bend=1)
    uke.arm('far', (uke.neck[0] - 20, uke.neck[1] + 80), bend=1)
    tori.arm('near', uke.at(0.8), bend=-1)
    tori.arm('far', uke.at(0.6), bend=-1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 30, 220), (ux - 110, 170), (ux - 200, 340))
    return s


if __name__ == '__main__':
    print(triptych('tri_yoko_wakare', [kuzushi(), tsukuri(), kake()], 'Yoko-wakare',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori se lança à frente de uke, estendendo as pernas.', 'Cai de lado e lança uke sobre o corpo estendido.']))
