"""O-soto-gari → Kesa-gatame (pé → solo)
Renraku-waza envolvendo o solo.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = s.add(standing('tori', 272, 1, lean=22))
    uke = s.add(standing('uke', 338, -1, lean=-26))
    grip(tori, uke)
    uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
    uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
    s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))
    return s


def quadro2():
    s = Scene()
    uke = lying('uke', 330, 1, y=396)
    uke.arm('near', (uke.neck[0] - 30, 330), bend=1)
    uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
    tori = Fig('tori', 292, 384, ang=150, facing=1)
    tori.leg('far', (tori.pelvis[0] - 118, GROUND - 4), bend=1)
    tori.leg('near', (tori.pelvis[0] + 40, GROUND - 4), bend=-1)
    tori.arm('near', (uke.head[0] + 18, uke.head[1] + 6), bend=1)
    tori.arm('far', (uke.neck[0] - 40, 345), bend=1)
    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(panels('ren_osoto_kesa', [quadro1(), quadro2()], [('1. 立技 Tachi-waza', '· projeção'), ('2. 寝技 Ne-waza', '· imobilização')], 'O-soto-gari → Kesa-gatame (pé → solo)', ['Tori projeta com o-soto-gari sem pontuação máxima.', 'Tori segue no solo e imobiliza com kesa-gatame.'], badges=None))
