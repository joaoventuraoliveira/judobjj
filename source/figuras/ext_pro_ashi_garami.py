"""Ashi-garami
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = standing('uke', 360, -1, lean=24)
    uke.leg('near', (296, 404), bend=1)
    tori = Fig('tori', 230, 396, ang=94, facing=1)
    tori.leg('near', (uke.limbs['leg_near'][1][0] + 10, uke.limbs['leg_near'][1][1] - 10), bend=1)
    tori.leg('far', (uke.limbs['leg_near'][1][0] + 20, uke.limbs['leg_near'][1][1] + 30), bend=1)
    tori.arm('near', uke.limbs['leg_near'][2], bend=-1)
    tori.arm('far', (uke.limbs['leg_near'][2][0] + 6, uke.limbs['leg_near'][2][1] - 8), bend=-1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=30)
    return s


if __name__ == '__main__':
    print(panels('pro_ashi_garami', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Ashi-garami', ['Tori entrelaça a perna de uke e torce a articulação do joelho. Hansoku-make direto (art. 18.2.2).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
