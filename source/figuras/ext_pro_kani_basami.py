"""Kani-basami
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = standing('uke', 340, -1, lean=-12)
    tori = Fig('tori', 306, 320, ang=262, facing=1)
    tori.leg('near', (uke.pelvis[0] + 50, 290), bend=1)
    tori.leg('far', (uke.pelvis[0] + 46, 378), bend=1)
    tori.arm('near', (tori.neck[0] - 4, 404), bend=1)
    tori.arm('far', (tori.neck[0] + 20, 406), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 110, 200), (uke.pelvis[0] + 120, 370))
    return s


if __name__ == '__main__':
    print(panels('pro_kani_basami', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Kani-basami', ['Tori salta de lado e prende o tronco e as pernas de uke em tesoura, derrubando-o para trás. Hansoku-make direto (art. 18.2.2).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
