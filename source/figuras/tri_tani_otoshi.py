"""Tani-otoshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.
Tsukuri: Tori desliza a perna por trás dos pés de uke e começa a cair de lado.
Kake: Cai de lado; uke vai ao canto traseiro.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    tori = standing('tori', 266, 1, lean=14)
    uke = standing('uke', 340, -1, lean=-18)
    uke.leg('near', (uke.pelvis[0] - 30, GROUND - 2), bend=1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    kuzushi_arrow(s, add(uke.at(0.95), (6, -14)), (80, 36))
    return s


def tsukuri():
    s = Scene()
    uke = standing('uke', 340, -1, lean=-16)
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
    uke = Fig('uke', 334, 304, ang=214, facing=1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
    uke.leg('near', (ux + 6, 404), bend=-1)
    tori = Fig('tori', 262, 392, ang=150, facing=1)
    tori.leg('far', (206, GROUND - 4), bend=1)
    tori.leg('near', (ux + 34, 410), bend=-1)
    tori.arm('near', uke.at(0.8), bend=-1)
    tori.arm('far', uke.at(0.5), bend=-1)
    uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
    uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
    s.add(tori); s.add(uke)
    s.arrow((uke.head[0] + 10, uke.head[1] - 20), (uke.head[0] - 90, uke.head[1] - 20), (uke.head[0] - 120, 330))
    return s


if __name__ == '__main__':
    print(triptych('tri_tani_otoshi', [kuzushi(), tsukuri(), kake()], 'Tani-otoshi',
                   ['Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.', 'Tori desliza a perna por trás dos pés de uke e começa a cair de lado.', 'Cai de lado; uke vai ao canto traseiro.']))
