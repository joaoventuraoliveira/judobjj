"""Harai-goshi → O-soto-gari
Renraku-waza em pé: direção oposta (frente → trás).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = Fig('tori', 300, 312, ang=190, facing=-1)
    uke = Fig('uke', 340, 298, ang=212, facing=-1)
    tori.leg('far', (tori.pelvis[0] + 18, GROUND - 2), bend=1)
    tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 34, GROUND - 2), bend=-1)
    uke.leg('near', (uke.pelvis[0] + 6, GROUND - 2), bend=-1)
    tori.arm('near', uke.at(0.82), bend=1)
    tori.arm('far', (tori.neck[0] - 66, tori.neck[1] + 56), bend=-1)
    uke.arm('near', (tori.neck[0] - 12, tori.neck[1] + 28), bend=1)
    uke.arm('far', (tori.neck[0] - 56, tori.neck[1] + 58), bend=1)
    s.add(uke); s.add(tori)
    return s


def quadro2():
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


if __name__ == '__main__':
    print(panels('ren_haraigoshi_osoto', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· Harai-goshi'), ('2. 連絡 2º ataque', '· O-soto-gari')], 'Harai-goshi → O-soto-gari', ['Uke bloqueia harai-goshi jogando o quadril para trás.', 'Tori muda para o-soto-gari, ceifando a perna de apoio.'], badges=None))
