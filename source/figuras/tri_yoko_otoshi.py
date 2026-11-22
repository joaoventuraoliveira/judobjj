"""Yoko-otoshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.
Tsukuri: Tori desliza a perna por fora do pé de uke e começa a cair de lado.
Kake: Cai de lado e lança uke para o mesmo lado.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    tori = standing('tori', 262, 1, lean=-4)
    uke = standing('uke', 342, -1, lean=6)
    uke.leg('near', (uke.pelvis[0] - 40, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 24, 404), bend=1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    kuzushi_arrow(s, uke.at(0.55), (-30, 86))
    mark(s, uke.limbs['leg_near'][2], r=22)
    return s


def tsukuri():
    s = Scene()
    uke = standing('uke', 340, -1, lean=-6)
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
    uke = Fig('uke', 334, 304, ang=226, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 26, GROUND - 2), bend=-1)
    uke.leg('near', (ux - 4, 404), bend=-1)
    tori = Fig('tori', 262, 392, ang=118, facing=1)
    tori.leg('far', (196, GROUND - 4), bend=1)
    tori.leg('near', (ux - 2, 412), bend=-1)
    tori.arm('near', uke.at(0.85), bend=-1)
    tori.arm('far', uke.at(0.55), bend=-1)
    uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
    uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
    s.add(tori); s.add(uke)
    s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))
    return s


if __name__ == '__main__':
    print(triptych('tri_yoko_otoshi', [kuzushi(), tsukuri(), kake()], 'Yoko-otoshi',
                   ['Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.', 'Tori desliza a perna por fora do pé de uke e começa a cair de lado.', 'Cai de lado e lança uke para o mesmo lado.']))
