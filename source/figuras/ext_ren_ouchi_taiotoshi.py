"""O-uchi-gari → Tai-otoshi
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
    tori = Fig('tori', 300, 318, ang=196, facing=-1)
    uke = Fig('uke', 352, 296, ang=222, facing=-1)
    tx, ux = tori.pelvis[0], uke.pelvis[0]

    tori.leg('far', (tx - 22, GROUND - 2), bend=1)
    uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
    uke.leg('near', (ux - 6, GROUND - 2), bend=-1)
    tori.leg('near', (tx + 92, 404), bend=1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
    uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
    uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((ux + 50, 200), (ux - 90, 200 - 90), (ux - 175, 330))
    return s


if __name__ == '__main__':
    print(panels('ren_ouchi_taiotoshi', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· O-uchi-gari'), ('2. 連絡 2º ataque', '· Tai-otoshi')], 'O-uchi-gari → Tai-otoshi', ['Uke reage a o-uchi-gari trazendo o peso à frente.', 'Tori abre o corpo e bloqueia a perna com tai-otoshi.'], badges=None))
