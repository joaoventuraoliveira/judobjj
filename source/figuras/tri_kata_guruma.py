"""Kata-guruma em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori desce sob uke, com o braço entre as pernas e a nuca sob o tronco dele.
Kake: Eleva uke sobre os ombros e o lança à frente.
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
    tori = Fig('tori', 296, 344, ang=146, facing=1)
    tori.leg('far', (262, GROUND - 2), bend=-1)
    tori.leg('near', (318, GROUND - 2), bend=-1)
    tori.arm('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('far', uke.at(0.9), bend=-1)
    uke.arm('near', (tori.neck[0] - 30, tori.neck[1] + 30), bend=1)
    uke.arm('far', (tori.neck[0] - 20, tori.neck[1] + 50), bend=1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=26)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 336, ang=196, facing=-1)
    tori.leg('far', (318, GROUND - 2), bend=1)
    tori.leg('near', (262, GROUND - 2), bend=1)
    uke = Fig('uke', tori.neck[0] + 44, tori.neck[1] - 24, ang=272, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 52, 330), bend=-1)
    uke.leg('near', (ux + 70, 318), bend=-1)
    uke.arm('near', (uke.neck[0] - 12, uke.neck[1] + 80), bend=1)
    uke.arm('far', (uke.neck[0] + 10, uke.neck[1] + 84), bend=1)
    tori.arm('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('far', (uke.neck[0] - 4, uke.neck[1] + 60), bend=-1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 60, 170), (ux - 100, 120), (ux - 190, 320))
    return s


if __name__ == '__main__':
    print(triptych('tri_kata_guruma', [kuzushi(), tsukuri(), kake()], 'Kata-guruma',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori desce sob uke, com o braço entre as pernas e a nuca sob o tronco dele.', 'Eleva uke sobre os ombros e o lança à frente.']))
