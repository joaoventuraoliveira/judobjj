"""Kesa-gatame → Kata-gatame (solo)
Renraku-waza envolvendo o solo.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = lying('uke', 330, 1, y=396)
    uke.arm('near', (uke.neck[0] - 30, 330), bend=1)
    uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
    tori = Fig('tori', 292, 384, ang=150, facing=1)
    tori.leg('far', (tori.pelvis[0] - 118, GROUND - 4), bend=1)
    tori.leg('near', (tori.pelvis[0] + 40, GROUND - 4), bend=-1)
    tori.arm('near', (uke.head[0] + 18, uke.head[1] + 6), bend=1)
    tori.arm('far', (uke.neck[0] - 40, 345), bend=1)
    s.add(uke); s.add(tori)
    return s


def quadro2():
    s = Scene()
    uke = lying('uke', 330, 1, y=396)
    uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
    tori = Fig('tori', 280, 380, ang=118, facing=1)
    tori.leg('far', (170, GROUND - 4), bend=1)
    tori.leg('near', (300, GROUND - 4), bend=-1)
    uke.arm('near', (tori.neck[0] + 4, tori.neck[1] - 6), bend=1)
    tori.arm('near', (uke.head[0] + 12, uke.head[1] - 4), bend=1)
    tori.arm('far', (uke.head[0] + 6, uke.head[1] + 8), bend=1)
    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(panels('ren_kesa_katagatame', [quadro1(), quadro2()], [('1. 抑込技 Osaekomi', '· kesa-gatame'), ('2. 抑込技 Osaekomi', '· kata-gatame')], 'Kesa-gatame → Kata-gatame (solo)', ['Uke empurra e solta o braço para escapar de kesa-gatame.', 'Tori prende o braço de uke junto à cabeça e passa a kata-gatame.'], badges=None))
