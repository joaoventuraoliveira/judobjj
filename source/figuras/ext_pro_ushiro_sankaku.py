"""Ushiro-sankaku de alto risco
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = Fig('uke', 330, 396, ang=210, facing=1)
    uke.leg('near', (440, GROUND - 4), bend=-1)
    uke.leg('far', (430, 404), bend=-1)
    uke.arm('near', (uke.neck[0] + 40, uke.neck[1] + 50), bend=-1)
    tori = Fig('tori', 230, 398, ang=104, facing=1)
    tori.leg('near', (uke.neck[0] + 30, uke.neck[1] - 4), bend=1)
    tori.leg('far', (uke.neck[0] + 26, uke.neck[1] + 22), bend=1)
    tori.arm('near', uke.at(0.6), bend=-1)
    s.add(uke); s.add(tori)
    mark(s, uke.neck, r=30)
    return s


if __name__ == '__main__':
    print(panels('pro_ushiro_sankaku', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Ushiro-sankaku de alto risco', ['Triângulo de pernas por trás do pescoço de uke em ne-waza, com risco ao pescoço e à coluna. Hansoku-make desde jan./2026.'], badges=[('HANSOKU-MAKE', '#C8102E')]))
