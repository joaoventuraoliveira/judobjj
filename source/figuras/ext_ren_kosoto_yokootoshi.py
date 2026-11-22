"""Ko-soto-gari → Yoko-otoshi
Renraku-waza em pé: pé → sacrifício.
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('tori', 280, 1, lean=10)
    uke = standing('uke', 342, -1, lean=-16)
    uke.leg('near', (uke.pelvis[0] - 34, GROUND - 2), bend=1)
    tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
    tori.leg('near', (uke.pelvis[0] - 26, 406), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(tori); s.add(uke)
    mark(s, (uke.pelvis[0] - 26, 406), r=24)
    return s


def quadro2():
    s = Scene()
    uke = Fig('uke', 334, 304, ang=226, facing=-1)
    ux = uke.pelvis[0]
    uke.leg('far', (ux + 26, GROUND - 2), bend=-1)
    uke.leg('near', (ux - 4, 404), bend=-1)
    tori = Fig('tori', 262, 392, ang=118, facing=1)
    tori.leg('far', (196, GROUND - 4), bend=1)
    tori.leg('near', (ux - 2, 412), bend=-1)
    tori.arm('near', uke.at(0.85), bend=-1)
    tori.arm('far', uke.at(0.55), bend=-1)
    uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
    uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
    s.add(tori); s.add(uke)
    s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))
    return s


if __name__ == '__main__':
    print(panels('ren_kosoto_yokootoshi', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· Ko-soto-gari'), ('2. 連絡 2º ataque', '· Yoko-otoshi')], 'Ko-soto-gari → Yoko-otoshi', ['Uke tira o pé da varrida de ko-soto-gari e desloca o peso ao lado.', 'Tori cai de lado e projeta com yoko-otoshi.'], badges=None))
