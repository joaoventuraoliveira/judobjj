"""Hane-goshi → O-uchi-gari
Renraku-waza em pé: direção oposta (frente → trás).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('tori', 300, 310, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] + 40, 380), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def quadro2():
    s = Scene()
    tori = standing('tori', 268, 1, lean=18)
    uke = standing('uke', 340, -1, lean=-20)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 26, 366), bend=1)
    uke.leg('far', (ux + 20, GROUND - 2), bend=1)
    tori.leg('near', (ux + 20, 380), bend=-1)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

    s.add(tori); s.add(uke)
    return s


if __name__ == '__main__':
    print(panels('ren_hanegoshi_ouchi', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· Hane-goshi'), ('2. 連絡 2º ataque', '· O-uchi-gari')], 'Hane-goshi → O-uchi-gari', ['Uke recua o quadril para anular hane-goshi.', 'Tori segue com o-uchi-gari para trás.'], badges=None))
