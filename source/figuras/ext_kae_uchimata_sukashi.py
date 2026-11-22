"""Uchi-mata-sukashi
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
    tori = Fig('tori', 250, 300, ang=188, facing=1)
    tori.leg('far', (226, GROUND - 2), bend=-1)
    tori.leg('near', (276, GROUND - 2), bend=-1)
    uke = Fig('uke', 324, 270, ang=262, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 20, GROUND - 2), bend=-1)
    uke.leg('near', (ux + 110, 222), bend=-1)
    tori.arm('near', uke.at(0.9), bend=1)
    tori.arm('far', uke.at(0.6), bend=1)
    uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 40), bend=1)
    uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 80, 190), (ux - 40, 100), (ux - 120, 330))
    mark(s, (296, 330), r=30)
    return s


if __name__ == '__main__':
    print(panels('kae_uchimata_sukashi', [quadro1(), quadro2()], [('1. 攻撃 Ataque', '· de uke'), ('2. 返技 Kaeshi', '· contragolpe de tori')], 'Uchi-mata-sukashi', ['Uke ataca com uchi-mata.', 'Tori esquiva a perna de ataque (sukashi): a perna de uke passa no vazio e tori o gira para a frente.'], badges=None))
