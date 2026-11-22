"""Sumi-otoshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.
Tsukuri: Tori pisa ao lado externo do pé de uke.
Kake: Projeta uke ao canto traseiro só com o corpo e as mãos.
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
    tori = standing('tori', 280, 1, lean=12)
    uke = standing('uke', 342, -1, lean=-24)

    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] - 34, GROUND - 2), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    mark(s, (uke.pelvis[0] - 34, GROUND - 2), r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=12)
    uke = standing('uke', 340, -1, lean=-32)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 30, GROUND - 2), bend=1)
    uke.leg('far', (ux + 14, 400), bend=1)
    tori.leg('near', (ux - 30, GROUND - 2), bend=-1)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 360))

    s.add(tori); s.add(uke)
    return s


if __name__ == '__main__':
    print(triptych('tri_sumi_otoshi', [kuzushi(), tsukuri(), kake()], 'Sumi-otoshi',
                   ['Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.', 'Tori pisa ao lado externo do pé de uke.', 'Projeta uke ao canto traseiro só com o corpo e as mãos.']))
