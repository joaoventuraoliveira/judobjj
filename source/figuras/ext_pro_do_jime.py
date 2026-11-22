"""Do-jime
Técnica/ação proibida — HANSOKU-MAKE (IJF SOR, art. 18).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = Fig('uke', 340, 392, ang=200, facing=1)
    uke.leg('near', (450, GROUND - 4), bend=-1)
    uke.leg('far', (440, 404), bend=-1)
    uke.arm('near', (uke.neck[0] + 30, uke.neck[1] + 60), bend=-1)
    tori = Fig('tori', 282, 396, ang=152, facing=1)
    tori.leg('near', (uke.at(0.25)[0] + 34, uke.at(0.25)[1] + 4), bend=-1)
    tori.leg('far', (uke.at(0.3)[0] + 30, uke.at(0.3)[1] + 18), bend=-1)
    tori.arm('near', uke.at(0.9), bend=-1)
    tori.arm('far', uke.at(0.7), bend=-1)
    s.add(tori); s.add(uke)
    mark(s, uke.at(0.25), r=40)
    return s


if __name__ == '__main__':
    print(panels('pro_do_jime', [quadro1()], [('禁止 Proibido', '· hansoku-make')], 'Do-jime', ['Tori aperta o tronco (rins ou abdômen) de uke com as pernas em tesoura. Hansoku-make direto (art. 18.2.2).'], badges=[('HANSOKU-MAKE', '#C8102E')]))
