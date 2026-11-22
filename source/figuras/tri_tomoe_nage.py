"""Tomoe-nage em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori entra sob uke e apoia o pé no abdômen inferior dele.
Kake: Cai para trás e lança uke por cima da cabeça.
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
    uke = standing('uke', 342, -1, lean=24)
    tori = Fig('tori', 280, 352, ang=160, facing=1)
    tori.leg('far', (250, GROUND - 2), bend=-1)
    tori.leg('near', uke.at(0.08), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, uke.at(0.08), r=24)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 250, 396, ang=100, facing=1)
    tori.leg('far', (tori.pelvis[0] - 70, GROUND - 4), bend=1)
    uke = Fig('uke', 300, 262, ang=58, facing=1)
    uke.leg('far', (uke.pelvis[0] - 100, 210), bend=1)
    uke.leg('near', (uke.pelvis[0] - 92, 240), bend=1)
    tori.leg('near', uke.at(0.1), bend=1)
    tori.arm('near', uke.at(0.9), bend=-1)
    tori.arm('far', add(uke.at(0.95), (10, 10)), bend=-1)
    uke.arm('near', (uke.neck[0] + 30, uke.neck[1] + 60), bend=-1)
    uke.arm('far', (uke.neck[0] + 45, uke.neck[1] + 50), bend=-1)
    s.add(tori); s.add(uke)
    s.arrow((uke.pelvis[0] - 30, 190), (uke.pelvis[0] + 120, 130), (uke.pelvis[0] + 190, 330))
    return s


if __name__ == '__main__':
    print(triptych('tri_tomoe_nage', [kuzushi(), tsukuri(), kake()], 'Tomoe-nage',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori entra sob uke e apoia o pé no abdômen inferior dele.', 'Cai para trás e lança uke por cima da cabeça.']))
