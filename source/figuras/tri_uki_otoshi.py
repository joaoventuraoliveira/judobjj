"""Uki-otoshi em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.
Tsukuri: Tori recua e desce sobre um joelho, mantendo uke flutuando à frente.
Kake: Puxa para baixo e projeta uke em círculo.
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
    uke = standing('uke', 344, -1, lean=28)
    uke.leg('near', (uke.pelvis[0] - 44, GROUND - 2), bend=1)
    tori = Fig('tori', 256, 352, ang=186, facing=1)
    tori.leg('far', (306, GROUND - 2), bend=-1)
    tori.limbs['leg_near'] = (tori.pelvis, (226, 410), (186, 412))
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, (226, 410), r=22)
    return s


def kake():
    s = Scene()
    tori = Fig('tori', 300, 356, ang=196, facing=-1)
    tori.leg('far', (252, GROUND - 2), bend=1)
    tori.limbs['leg_near'] = (tori.pelvis, (330, 410), (378, 412))
    uke = Fig('uke', 322, 212, ang=292, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 84, 160), bend=-1)
    uke.leg('near', (ux + 64, 136), bend=-1)
    uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 70), bend=1)
    uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 54), bend=1)
    tori.arm('near', uke.at(0.85), bend=1)
    tori.arm('far', (tori.neck[0] - 64, tori.neck[1] + 56), bend=-1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 70, 120), (ux - 80, 70), (ux - 170, 320))
    return s


if __name__ == '__main__':
    print(triptych('tri_uki_otoshi', [kuzushi(), tsukuri(), kake()], 'Uki-otoshi',
                   ['Para a frente / canto frontal (mae, mae-sumi): tori puxa e uke fica na ponta dos pés.', 'Tori recua e desce sobre um joelho, mantendo uke flutuando à frente.', 'Puxa para baixo e projeta uke em círculo.']))
