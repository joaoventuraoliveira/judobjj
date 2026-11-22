"""O-soto-gari em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.
Tsukuri: Tori pisa ao lado de uke, cola o peito e prepara a perna de ceifa.
Kake: Ceifa por trás a perna de apoio; uke cai para trás.
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
    tori = standing('tori', 280, 1, lean=22)
    uke = standing('uke', 342, -1, lean=-24)

    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 10, 330), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    mark(s, (uke.pelvis[0] + 10, 330), r=24)
    return s


def kake():
    s = Scene()
    tori = s.add(standing('tori', 272, 1, lean=22))
    uke = s.add(standing('uke', 338, -1, lean=-26))
    grip(tori, uke)
    uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
    uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
    s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))
    return s


if __name__ == '__main__':
    print(triptych('tri_o_soto_gari', [kuzushi(), tsukuri(), kake()], 'O-soto-gari',
                   ['Para trás / canto traseiro (ushiro, ushiro-sumi): o peso de uke vai para os calcanhares.', 'Tori pisa ao lado de uke, cola o peito e prepara a perna de ceifa.', 'Ceifa por trás a perna de apoio; uke cai para trás.']))
