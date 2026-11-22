"""Agarrar as pernas em pé
Técnica/ação proibida — SHIDO (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = standing('uke', 340, -1, lean=-8)
    tori = Fig('tori', 280, 334, ang=124, facing=1)
    tori.leg('far', (246, GROUND - 2), bend=-1)
    tori.leg('near', (300, GROUND - 2), bend=-1)
    tori.arm('near', uke.limbs['leg_near'][1], bend=1)
    tori.arm('far', uke.limbs['leg_far'][1], bend=1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][1], r=30)
    return s


if __name__ == '__main__':
    print(panels('pro_pegar_pernas', [quadro1()], [('禁止 Proibido', '· shido')], 'Agarrar as pernas em pé', ['Agarrar, bloquear ou tocar as pernas com as mãos em tachi-waza. Shido; só é permitido em ne-waza já estabelecido (art. 18.1.2).'], badges=[('SHIDO', '#E08A00')]))
