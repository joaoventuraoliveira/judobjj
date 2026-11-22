"""Yoko-gake em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori leva a sola do pé ao pé de uke, na direção do dedo mínimo.
Kake: Varre o pé e cai de lado, projetando uke.
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
    uke = standing('uke', 340, -1, lean=12)
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
    uke = Fig('uke', 332, 304, ang=222, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 22, GROUND - 2), bend=-1)
    uke.leg('near', (ux - 18, 394), bend=-1)
    tori = Fig('tori', 256, 372, ang=124, facing=1)
    tori.leg('far', (206, GROUND - 4), bend=1)
    tori.leg('near', (ux - 24, 400), bend=-1)
    tori.arm('near', uke.at(0.85), bend=-1)
    tori.arm('far', uke.at(0.55), bend=-1)
    uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
    uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
    s.add(tori); s.add(uke)
    s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))
    return s


if __name__ == '__main__':
    print(triptych('tri_yoko_gake', [kuzushi(), tsukuri(), kake()], 'Yoko-gake',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori leva a sola do pé ao pé de uke, na direção do dedo mínimo.', 'Varre o pé e cai de lado, projetando uke.']))
