"""Kawazu-gake
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('tori', 290, 304, ang=204, facing=1)
    uke = standing('uke', 336, -1, lean=-18)
    tori.leg('far', (266, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 20, 360), bend=-1)
    tori.limbs['leg_near'] = (tori.pelvis, (uke.pelvis[0] + 24, 350), (uke.pelvis[0] - 18, 382))
    tori.arm('near', uke.at(0.85), bend=-1)
    tori.arm('far', uke.at(0.95), bend=-1)
    s.add(uke); s.add(tori)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (uke.pelvis[0] + 40, 120), (uke.pelvis[0] - 120, 330))
    return s


if __name__ == '__main__':
    print(panels('pro_kawazu_gake', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Kawazu-gake', ['Tori enrola a perna na perna de uke e cai para trás junto com ele. Hansoku-make direto (art. 18.2.2).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
