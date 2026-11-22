"""De-ashi-harai em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.
Tsukuri: Tori acompanha o passo e leva a sola do pé ao pé de uke que vai receber o peso.
Kake: Varre o pé avançado no instante do apoio.
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
    tori = standing('tori', 258, 1, lean=-10)
    uke = standing('uke', 340, -1, lean=14)
    uke.leg('near', (uke.pelvis[0] - 44, 406), bend=1)
    tori.leg('near', (uke.pelvis[0] - 62, 400), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][2], r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=-6)
    uke = standing('uke', 340, -1, lean=10)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 50, 404), bend=1)
    uke.leg('far', (ux + 16, GROUND - 2), bend=1)
    tori.leg('near', (ux - 58, 404), bend=-1)
    s.arrow((uke.head[0] + 10, uke.head[1] - 14), (ux + 110, 200), (ux + 120, 360))

    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(triptych('tri_de_ashi_harai', [kuzushi(), tsukuri(), kake()], 'De-ashi-harai',
                   ['Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.', 'Tori acompanha o passo e leva a sola do pé ao pé de uke que vai receber o peso.', 'Varre o pé avançado no instante do apoio.']))
