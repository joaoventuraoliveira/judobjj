"""Ko-uchi-gari → Seoi-nage
Renraku-waza em pé: direção oposta (trás → frente).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('tori', 280, 1, lean=10)
    uke = standing('uke', 342, -1, lean=-14)
    uke.leg('near', (uke.pelvis[0] - 44, GROUND - 2), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] - 18, 406), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    mark(s, (uke.pelvis[0] - 18, 406), r=24)
    return s


def quadro2():
    s = Scene()
    tori = Fig('tori', 300, 318, ang=200, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 22, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 28, GROUND - 2), bend=1)
    uke = Fig('uke', 312, 206, ang=262, facing=-1)
    uke.leg('far', (uke.pelvis[0] + 90, 150), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 105, 188), bend=-1)
    tori.arm('near', uke.at(0.8), bend=1)
    tori.arm('far', (tori.pelvis[0] - 70, 300), bend=-1)
    uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
    uke.arm('far', (tori.pelvis[0] - 65, 296), bend=1)
    s.add(uke); s.add(tori)
    s.arrow((uke.pelvis[0] + 60, 150), (uke.pelvis[0] - 120, 110), (uke.pelvis[0] - 160, 300))
    return s


if __name__ == '__main__':
    print(panels('ren_kouchi_seoi', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· Ko-uchi-gari'), ('2. 連絡 2º ataque', '· Seoi-nage')], 'Ko-uchi-gari → Seoi-nage', ['Ko-uchi-gari leva uke a avançar o peso para recuperar o equilíbrio.', 'Tori gira e entra com seoi-nage para a frente.'], badges=None))
