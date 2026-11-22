"""Ko-uchi-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('uke', 268, 1, lean=10)
    uke = standing('tori', 340, -1, lean=-16)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 46, 398), bend=1)
    uke.leg('far', (ux + 22, GROUND - 2), bend=1)
    tori.leg('near', (ux - 10, 404), bend=-1)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

    s.add(uke); s.add(tori)
    return s


def quadro2():
    s = Scene()
    tori = standing('tori', 266, 1, lean=-4)
    uke = standing('uke', 336, -1, lean=28)
    uke.leg('near', (tori.pelvis[0] + 6, 400), bend=1)
    uke.leg('far', (uke.pelvis[0] + 30, 400), bend=1)
    tori.leg('near', (tori.pelvis[0] - 30, 392), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] - 6, uke.head[1] - 20), (tori.pelvis[0] - 30, 120), (tori.pelvis[0] - 80, 330))
    return s


if __name__ == '__main__':
    print(panels('kae_kouchi_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'Ko-uchi-gaeshi', ['Uke tenta varrer o calcanhar de tori por dentro com ko-uchi-gari.', 'Tori retira o pé atacado e, com as mãos, gira uke e o projeta no sentido do próprio ataque.'], badges=None))
