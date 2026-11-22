"""O-uchi-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('uke', 268, 1, lean=18)
    uke = standing('tori', 340, -1, lean=-20)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 26, 366), bend=1)
    uke.leg('far', (ux + 20, GROUND - 2), bend=1)
    tori.leg('near', (ux + 20, 380), bend=-1)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

    s.add(tori); s.add(uke)
    return s


def quadro2():
    s = Scene()
    tori = standing('tori', 262, 1, lean=-6)
    uke = standing('uke', 334, -1, lean=-30)
    uke.leg('near', (tori.pelvis[0] + 8, 344), bend=1)
    uke.leg('far', (uke.pelvis[0] + 10, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 34, GROUND - 2), bend=-1)
    grip(tori, uke); tori.arms_top = True
    tori.arm('far', (uke.limbs['leg_near'][1][0], uke.limbs['leg_near'][1][1] + 6), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 110, 200), (uke.pelvis[0] + 120, 370))
    return s


if __name__ == '__main__':
    print(panels('kae_ouchi_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'O-uchi-gaeshi', ['Uke engancha a perna de tori por dentro com o-uchi-gari.', 'Tori recua a perna atacada, conduz a perna de uke com o corpo e o projeta para trás.'], badges=None))
