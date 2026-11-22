"""Sukui-nage em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.
Tsukuri: Ao lado de uke, tori desce e envolve as coxas dele.
Kake: Eleva uke e o projeta para trás.
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
    uke = standing('uke', 334, -1, lean=6)
    tori = Fig('tori', 290, 336, ang=150, facing=1)
    tori.leg('far', (258, GROUND - 2), bend=-1)
    tori.leg('near', (312, GROUND - 2), bend=-1)
    tori.arm('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('far', uke.at(0.25), bend=1)
    uke.arm('near', tori.at(0.9), bend=-1)
    uke.arm('far', tori.at(0.7), bend=-1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=26)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 330, ang=166, facing=1)
    tori.leg('far', (268, GROUND - 2), bend=-1)
    tori.leg('near', (330, GROUND - 2), bend=-1)
    uke = Fig('uke', 334, 246, ang=122, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux - 92, 290), bend=1)
    uke.leg('near', (ux - 104, 262), bend=1)
    uke.arm('near', (uke.neck[0] + 40, uke.neck[1] - 30), bend=-1)
    uke.arm('far', (uke.neck[0] + 50, uke.neck[1] - 10), bend=-1)
    tori.arm('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('far', uke.at(0.12), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] + 10, uke.head[1] - 20), (ux + 150, 140), (ux + 160, 360))
    return s


if __name__ == '__main__':
    print(triptych('tri_sukui_nage', [kuzushi(), tsukuri(), kake()], 'Sukui-nage',
                   ['Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.', 'Ao lado de uke, tori desce e envolve as coxas dele.', 'Eleva uke e o projeta para trás.']))
