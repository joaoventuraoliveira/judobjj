"""Mergulho de cabeça (diving)
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('tori', 296, 292, ang=14, facing=-1)
    tori.leg('far', (260, 200), bend=-1)
    tori.leg('near', (330, 210), bend=1)
    uke = Fig('uke', 318, 236, ang=268, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 80, 180), bend=-1)
    uke.leg('near', (ux + 90, 210), bend=-1)
    tori.arm('near', uke.at(0.8), bend=1)
    tori.arm('far', (tori.head[0] - 40, GROUND - 4), bend=1)
    uke.arm('near', (uke.neck[0] - 20, uke.neck[1] + 50), bend=1)
    s.add(uke); s.add(tori)
    mark(s, (tori.head[0], tori.head[1] + 6), r=30)
    return s


if __name__ == '__main__':
    print(panels('pro_mergulho', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Mergulho de cabeça (diving)', ['Tori apoia a cabeça no tatame ao projetar (ex.: uchi-mata, seoi-nage). Hansoku-make, podendo seguir na competição (art. 18.2.1).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
