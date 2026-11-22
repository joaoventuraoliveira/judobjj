"""Uchi-mata-gaeshi
Kaeshi-waza: uke (azul) ataca no 1º quadro; tori (branco) contra-ataca no 2º.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('uke', 290, 300, ang=232, facing=-1)
    tori.leg('far', (tori.pelvis[0] - 8, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] + 112, 214), bend=1)
    uke = Fig('tori', 340, 250, ang=250, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 40, 360), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 92, 196), bend=-1)
    tori.arm('near', uke.at(0.85), bend=1)
    tori.arm('far', (tori.neck[0] - 60, tori.neck[1] + 70), bend=-1)
    uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 30), bend=1)
    uke.arm('far', (tori.neck[0] - 55, tori.neck[1] + 66), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 70, 170), (uke.pelvis[0] - 60, 90), (uke.pelvis[0] - 170, 260))
    return s


def quadro2():
    s = Scene()
    uke = Fig('uke', 300, 296, ang=162, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('near', (ux + 90, 250), bend=-1)
    uke.leg('far', (ux - 6, 404), bend=-1)
    uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
    uke.arm('far', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
    tori = Fig('tori', 336, 318, ang=172, facing=-1)
    tori.leg('far', (366, GROUND - 2), bend=1)
    tori.leg('near', (ux - 4, 402), bend=1)
    tori.arm('near', uke.at(0.25), bend=1)
    tori.arm('far', uke.at(0.6), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] - 10, uke.head[1] - 20), (ux + 110, uke.head[1] - 60), (ux + 150, 330))
    mark(s, (ux - 4, 402), r=24)
    return s


if __name__ == '__main__':
    print(panels('kae_uchimata_gaeshi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'Uchi-mata-gaeshi', ['Uke ataca com uchi-mata.', 'Tori acompanha o giro e projeta uke de costas sobre a perna de apoio.'], badges=None))
