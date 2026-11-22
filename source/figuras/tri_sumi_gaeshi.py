"""Sumi-gaeshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori entra baixo e apoia o peito do pé atrás da coxa de uke.
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
    tori.leg('near', uke.limbs['leg_near'][1], bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=24)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 248, 396, ang=100, facing=1)
    tori.leg('far', (178, GROUND - 4), bend=1)
    uke = Fig('uke', 302, 270, ang=62, facing=1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux - 96, 230), bend=1)
    uke.leg('near', (ux - 66, 300), bend=1)
    tori.leg('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('near', uke.at(0.85), bend=-1)
    tori.arm('far', uke.at(0.6), bend=-1)
    uke.arm('near', (uke.neck[0] + 34, uke.neck[1] + 60), bend=-1)
    uke.arm('far', (uke.neck[0] + 46, uke.neck[1] + 50), bend=-1)
    s.add(tori); s.add(uke)
    s.arrow((ux - 40, 200), (ux + 110, 130), (ux + 180, 330))
    return s


if __name__ == '__main__':
    print(triptych('tri_sumi_gaeshi', [kuzushi(), tsukuri(), kake()], 'Sumi-gaeshi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori entra baixo e apoia o peito do pé atrás da coxa de uke.', 'Cai para trás e lança uke por cima da cabeça.']))
