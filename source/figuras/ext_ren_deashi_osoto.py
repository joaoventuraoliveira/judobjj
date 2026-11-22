"""De-ashi-harai → O-soto-gari
Renraku-waza em pé: mesma direção (frente → trás).
Gerado por make_extra.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, badge, panels)


def quadro1():
    s = Scene()
    tori = standing('tori', 258, 1, lean=-10)
    uke = standing('uke', 340, -1, lean=14)
    uke.leg('near', (uke.pelvis[0] - 44, 406), bend=1)
    tori.leg('near', (uke.pelvis[0] - 62, 400), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, uke.limbs['leg_near'][2], r=24)
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
    print(panels('ren_deashi_osoto', [quadro1(), quadro2()], [('1. 連絡 1º ataque', '· De-ashi-harai'), ('2. 連絡 2º ataque', '· O-soto-gari')], 'De-ashi-harai → O-soto-gari', ['Uke recua o pé para escapar da varrida de de-ashi-harai.', 'Tori aproveita o peso de uke atrás e entra com o-soto-gari.'], badges=None))
