"""Hane-goshi-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('uke', 300, 306, ang=212, facing=-1)
    uke = Fig('tori', 336, 276, ang=240, facing=-1)
    tx, ux = tori.pelvis[0], uke.pelvis[0]

    tori.leg('far', (tx - 4, GROUND - 2), bend=1)
    uke.leg('far', (ux + 46, 378), bend=-1)
    uke.leg('near', (ux + 74, 300), bend=-1)
    tori.leg('near', (tx + 42, 352), bend=-1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
    uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
    uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 50, 180), (ux - 90, 180 - 90), (ux - 175, 330))
    return s


def quadro2():
    s = Scene()
    uke = Fig('uke', 300, 300, ang=166, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('near', (ux + 60, 320), bend=-1)
    uke.leg('far', (ux - 6, 404), bend=-1)
    uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
    uke.arm('far', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
    tori = Fig('tori', 336, 318, ang=172, facing=-1)
    tori.leg('far', (366, GROUND - 2), bend=1)
    tori.leg('near', (ux + 4, 398), bend=1)
    tori.arm('near', uke.at(0.25), bend=1)
    tori.arm('far', uke.at(0.6), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] - 10, uke.head[1] - 20), (ux + 110, uke.head[1] - 60), (ux + 150, 330))
    mark(s, (ux + 4, 398), r=24)
    return s


if __name__ == '__main__':
    print(panels('kae_hanegoshi_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'Hane-goshi-gaeshi', ['Uke ataca com hane-goshi.', 'Tori baixa o quadril, engancha a perna de apoio de uke e o projeta para trás.'], badges=None))
