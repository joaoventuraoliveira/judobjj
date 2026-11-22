"""Cair para trás com o oponente nas costas
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('tori', 300, 316, ang=208, facing=1)
    tori.leg('far', (330, GROUND - 2), bend=-1)
    tori.leg('near', (350, GROUND - 2), bend=-1)
    uke = Fig('uke', 262, 300, ang=196, facing=1)
    uke.leg('near', (300, 360), bend=-1)
    uke.leg('far', (310, 380), bend=-1)
    uke.arm('near', tori.neck, bend=-1)
    uke.arm('far', tori.at(0.8), bend=-1)
    tori.arm('near', (tori.neck[0] - 20, tori.neck[1] - 30), bend=-1)
    s.add(uke); s.add(tori)
    s.arrow((tori.head[0] + 10, tori.head[1] - 20), (tori.head[0] - 90, tori.head[1] - 30), (tori.head[0] - 140, 360))
    return s


if __name__ == '__main__':
    print(panels('pro_cair_costas', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Cair para trás com o oponente nas costas', ['Com uke agarrado às suas costas, tori se joga para trás de propósito, controlando a queda. Hansoku-make direto (art. 18.2.2).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
