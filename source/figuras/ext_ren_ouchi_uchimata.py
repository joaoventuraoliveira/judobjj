"""O-uchi-gari → Uchi-mata
Renraku-waza em pé: direção oposta (trás → frente).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('tori', 280, 1, lean=16)
    uke = standing('uke', 342, -1, lean=-16)

    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] - 6, 404), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    mark(s, (uke.pelvis[0] - 6, 404), r=24)
    return s


def quadro2():
    s = Scene()
    tori = Fig('tori', 290, 300, ang=232, facing=-1)
    tori.leg('far', (tori.pelvis[0] - 8, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] + 112, 214), bend=1)
    uke = Fig('uke', 340, 250, ang=250, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 40, 360), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 92, 196), bend=-1)
    tori.arm('near', uke.at(0.85), bend=1)
    tori.arm('far', (tori.neck[0] - 60, tori.neck[1] + 70), bend=-1)
    uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 30), bend=1)
    uke.arm('far', (tori.neck[0] - 55, tori.neck[1] + 66), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 70, 170), (uke.pelvis[0] - 60, 90), (uke.pelvis[0] - 170, 260))
    return s


if __name__ == '__main__':
    print(panels('ren_ouchi_uchimata', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· O-uchi-gari'), ('2. 連絡 2º ataque', '· Uchi-mata')], 'O-uchi-gari → Uchi-mata', ['Uke resiste a o-uchi-gari empurrando para a frente e abre as pernas.', 'Tori gira e varre a coxa interna com uchi-mata.'], badges=None))
