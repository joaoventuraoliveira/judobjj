"""Tsubame-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('uke', 268, 1, lean=-6)
    uke = standing('tori', 340, -1, lean=10)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 50, 404), bend=1)
    uke.leg('far', (ux + 16, GROUND - 2), bend=1)
    tori.leg('near', (ux - 58, 404), bend=-1)
    s.arrow((uke.head[0] + 10, uke.head[1] - 14), (ux + 110, 200), (ux + 120, 360))

    s.add(uke); s.add(tori)
    return s


def quadro2():
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
    print(panels('kae_tsubame_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'Tsubame-gaeshi', ['Uke tenta varrer o pé de tori com de-ashi-harai.', 'Tori ergue o pé, deixa a varrida passar e varre o pé de uke com o outro pé.'], badges=None))
