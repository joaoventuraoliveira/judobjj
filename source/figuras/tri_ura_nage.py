"""Ura-nage em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente, contra o corpo de tori: tori traz uke para junto de si.
Tsukuri: Tori envolve a cintura de uke com os dois braços e o cola ao corpo.
Kake: Levanta e cai para trás, projetando uke por cima do ombro.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    tori = standing('tori', 272, 1, lean=-6)
    uke = standing('uke', 336, -1, lean=16)
    grip(tori, uke); tori.arms_top = True
    tori.arm('near', uke.at(0.3), bend=1)
    s.add(uke); s.add(tori)
    kuzushi_arrow(s, add(uke.at(0.9), (0, -16)), (-70, 20))
    return s


def tsukuri():
    s = Scene()
    uke = standing('uke', 334, -1, lean=6)
    tori = Fig('tori', 290, 336, ang=150, facing=1)
    tori.leg('far', (258, GROUND - 2), bend=-1)
    tori.leg('near', (312, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.15), bend=1)
    tori.arm('far', uke.at(0.25), bend=1)
    uke.arm('near', tori.at(0.9), bend=-1)
    uke.arm('far', tori.at(0.7), bend=-1)
    s.add(uke); s.add(tori)
    mark(s, uke.at(0.15), r=26)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 346, ang=222, facing=1)
    tori.leg('far', (330, GROUND - 2), bend=-1)
    tori.leg('near', (350, GROUND - 2), bend=-1)
    uke = Fig('uke', tori.neck[0] - 70, tori.neck[1] - 70, ang=318, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 60, uke.pelvis[1] - 90), bend=-1)
    uke.leg('near', (ux + 30, uke.pelvis[1] - 100), bend=-1)
    uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
    uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 60), bend=1)
    tori.arm('near', uke.at(0.1), bend=-1)
    tori.arm('far', uke.at(0.3), bend=-1)
    s.add(tori); s.add(uke)
    s.arrow((ux + 60, uke.pelvis[1] - 110), (ux - 80, uke.pelvis[1] - 120), (ux - 140, 360))
    return s


if __name__ == '__main__':
    print(triptych('tri_ura_nage', [kuzushi(), tsukuri(), kake()], 'Ura-nage',
                   ['Para a frente, contra o corpo de tori: tori traz uke para junto de si.', 'Tori envolve a cintura de uke com os dois braços e o cola ao corpo.', 'Levanta e cai para trás, projetando uke por cima do ombro.']))
