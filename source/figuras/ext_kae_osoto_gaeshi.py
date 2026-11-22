"""O-soto-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = s.add(standing('uke', 272, 1, lean=22))
    uke = s.add(standing('tori', 338, -1, lean=-26))
    grip(tori, uke)
    uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
    uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
    s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))
    return s


def quadro2():
    s = Scene()
    tori = s.add(standing('tori', 272, 1, lean=22))
    uke = s.add(standing('uke', 338, -1, lean=-26))
    grip(tori, uke)
    uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
    uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
    s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))
    return s


if __name__ == '__main__':
    print(panels('kae_osoto_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'O-soto-gaeshi', ['Uke ataca com o-soto-gari.', 'Tori resiste, gira o eixo e ceifa de volta a perna que ataca; uke cai para trás.'], badges=None))
