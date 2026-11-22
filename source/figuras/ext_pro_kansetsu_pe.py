"""Kansetsu-waza aplicado em pé
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = Fig('uke', 340, 300, ang=232, facing=-1)
    uke.leg('far', (370, GROUND - 2), bend=-1)
    uke.leg('near', (340, GROUND - 2), bend=-1)
    tori = Fig('tori', 300, 318, ang=228, facing=-1)
    tori.leg('far', (316, GROUND - 2), bend=1)
    tori.leg('near', (268, GROUND - 2), bend=1)
    uke.arm('near', (tori.at(0.6)[0] - 40, tori.at(0.6)[1] - 10), bend=1)
    tori.arm('near', (uke.limbs['arm_near'][2][0] + 6, uke.limbs['arm_near'][2][1] + 4), bend=1)
    tori.arm('far', uke.limbs['arm_near'][1], bend=1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['arm_near'][1], r=26)
    s.arrow((uke.head[0] + 10, uke.head[1] - 20), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 120, 360))
    return s


if __name__ == '__main__':
    print(panels('pro_kansetsu_pe', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Kansetsu-waza aplicado em pé', ['Chave de braço aplicada durante a projeção, sem chance de escape para uke. Hansoku-make; com risco menor, shido (art. 18).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
