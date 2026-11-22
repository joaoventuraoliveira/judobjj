"""Yoko-shiho-gatame → Juji-gatame (solo)
Renraku-waza envolvendo o solo.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    uke = lying('uke', 330, 1, y=398)
    uke.arm('near', (uke.neck[0] - 20, 350), bend=1)
    tori = Fig('tori', 304, 372, ang=180 - 20, facing=1)
    tori.leg('far', (250, GROUND - 4), bend=1)
    tori.leg('near', (262, GROUND - 4), bend=1)
    tori.limbs.pop('leg_near')
    tori.arm('near', (uke.head[0], uke.head[1] + 6), bend=1)
    tori.arm('far', (uke.pelvis[0] - 30, 404), bend=1)
    s.add(uke); s.add(tori)
    return s


def quadro2():
    s = Scene()
    uke = lying('uke', 250, 1, y=398)
    tori = Fig('tori', 372, 396, ang=94, facing=1)
    uke.arm('near', (392, 300), bend=1)
    uke.arm('far', (uke.neck[0] - 10, 406), bend=1)
    tori.leg('far', (316, 404), bend=1)
    tori.leg('near', (300, 390), bend=1)
    tori.arm('near', (394, 302), bend=-1)
    tori.arm('far', (390, 310), bend=-1)
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['arm_near'][1], r=24)
    return s


if __name__ == '__main__':
    print(panels('ren_yokoshiho_juji', [quadro1(), quadro2()], [('1. 抑込技 Osaekomi', '· yoko-shiho-gatame'), ('2. 関節技 Kansetsu', '· juji-gatame')], 'Yoko-shiho-gatame → Juji-gatame (solo)', ['Uke empurra com o braço para escapar de yoko-shiho-gatame.', 'Tori passa a perna sobre a cabeça e aplica juji-gatame no braço estendido.'], badges=None))
