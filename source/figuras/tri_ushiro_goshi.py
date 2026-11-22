"""Ushiro-goshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Contragolpe: uke ataca com o quadril; tori baixa o quadril e bloqueia, tirando uke do chão para cima.
Tsukuri: Tori se afasta do ataque e envolve a cintura de uke por trás.
Kake: Levanta uke no ar e o arremessa de costas.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    uke = Fig('uke', 292, 300, ang=204, facing=-1)
    uke.leg('far', (318, GROUND - 2), bend=-1)
    uke.leg('near', (262, GROUND - 2), bend=-1)
    uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 50), bend=1)
    uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
    tori = Fig('tori', 342, 322, ang=176, facing=-1)
    tori.leg('far', (368, GROUND - 2), bend=1)
    tori.leg('near', (316, GROUND - 2), bend=1)
    tori.arm('near', uke.at(0.2), bend=1)
    tori.arm('far', uke.at(0.35), bend=1)
    s.add(uke); s.add(tori)
    kuzushi_arrow(s, add(uke.pelvis, (-10, -20)), (0, -90))
    return s


def tsukuri():
    s = Scene()
    uke = Fig('uke', 292, 292, ang=200, facing=-1)
    uke.leg('far', (318, 410), bend=-1)
    uke.leg('near', (262, 408), bend=-1)
    uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 50), bend=1)
    uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
    tori = Fig('tori', 336, 334, ang=170, facing=-1)
    tori.leg('far', (364, GROUND - 2), bend=1)
    tori.leg('near', (310, GROUND - 2), bend=1)
    tori.arm('near', uke.at(0.15), bend=1)
    tori.arm('far', uke.at(0.3), bend=1)
    s.add(uke); s.add(tori)
    mark(s, uke.at(0.15), r=28)
    return s


def kake():
    s = Scene()
    uke = Fig('uke', 296, 224, ang=168, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux - 30, 350), bend=-1)
    uke.leg('near', (ux - 10, 344), bend=-1)
    tori = Fig('tori', 330, 324, ang=172, facing=-1)
    tori.leg('far', (356, GROUND - 2), bend=1)
    tori.leg('near', (304, GROUND - 2), bend=1)
    tori.arm('near', uke.at(0.15), bend=1)
    tori.arm('far', uke.at(0.3), bend=1)
    uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 20), bend=1)
    uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux - 40, 130), (ux + 40, 40), (ux + 160, 300))
    return s


if __name__ == '__main__':
    print(triptych('tri_ushiro_goshi', [kuzushi(), tsukuri(), kake()], 'Ushiro-goshi',
                   ['Contragolpe: uke ataca com o quadril; tori baixa o quadril e bloqueia, tirando uke do chão para cima.', 'Tori se afasta do ataque e envolve a cintura de uke por trás.', 'Levanta uke no ar e o arremessa de costas.']))
