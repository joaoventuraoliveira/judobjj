"""Seoi-nage em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori gira com o cotovelo sob a axila de uke e encaixa as costas no peito dele.
Kake: Carrega uke nas costas e o lança por cima do ombro.
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
    tori = Fig('tori', 300, 338, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.78), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 318, ang=200, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 22, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 28, GROUND - 2), bend=1)
    uke = Fig('uke', 312, 206, ang=262, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 90, 150), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 105, 188), bend=-1)
    tori.arm('near', uke.at(0.8), bend=1)
    tori.arm('far', (tori.pelvis[0] - 70, 300), bend=-1)
    uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
    uke.arm('far', (tori.pelvis[0] - 65, 296), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 60, 150), (uke.pelvis[0] - 120, 110), (uke.pelvis[0] - 160, 300))
    return s


if __name__ == '__main__':
    print(triptych('tri_seoi_nage', [kuzushi(), tsukuri(), kake()], 'Seoi-nage',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori gira com o cotovelo sob a axila de uke e encaixa as costas no peito dele.', 'Carrega uke nas costas e o lança por cima do ombro.']))
