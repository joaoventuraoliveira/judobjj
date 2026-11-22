"""Okuri-ashi-harai em três fases: 崩し Kuzushi · 作り Tsukuri · 掛け Kake.
Critério: IJF/Kodokan Classification of Judo Techniques (2017).
Kuzushi: Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.
Tsukuri: Tori acompanha o deslocamento lateral de uke, com o pé junto aos pés dele.
Kake: Varre os dois pés juntos; uke cai de costas.
Gerado por make_tri.py — pode ser editado à mão.
"""
from judoka import (Scene, Fig, standing, kneeling, lying, grip, add, GROUND,
                    kuzushi_arrow, mark, triptych)


def kuzushi():
    s = Scene()
    tori = standing('tori', 262, 1, lean=-4)
    uke = standing('uke', 342, -1, lean=6)
    uke.leg('near', (uke.pelvis[0] - 40, GROUND - 2), bend=1)
    uke.leg('far', (uke.pelvis[0] + 24, 404), bend=1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    kuzushi_arrow(s, uke.at(0.55), (-30, 86))
    mark(s, uke.limbs['leg_near'][2], r=22)
    return s


def tsukuri():
    s = Scene()
    tori = standing('tori', 258, 1, lean=-10)
    uke = standing('uke', 340, -1, lean=14)
    uke.leg('near', (uke.pelvis[0] - 44, 406), bend=1)
    tori.leg('near', (uke.pelvis[0] - 30, 404), bend=-1)
    grip(tori, uke); tori.arms_top = True
    s.add(uke); s.add(tori)
    mark(s, (uke.pelvis[0] - 20, 404), r=24)
    return s


def kake():
    s = Scene()
    tori = standing('tori', 268, 1, lean=-4)
    uke = standing('uke', 340, -1, lean=-10)
    grip(tori, uke)
    tori.arms_top = True
    ux, tx = uke.pelvis[0], tori.pelvis[0]

    uke.leg('near', (ux - 12, 392), bend=1)
    uke.leg('far', (ux + 6, 398), bend=1)
    tori.leg('near', (ux - 22, 400), bend=-1)
    s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 370))

    s.add(uke); s.add(tori)
    return s


if __name__ == '__main__':
    print(triptych('tri_okuri_ashi_harai', [kuzushi(), tsukuri(), kake()], 'Okuri-ashi-harai',
                   ['Lateral / peso transferido: uke apoia todo o peso no pé que acabou de mover.', 'Tori acompanha o deslocamento lateral de uke, com o pé junto aos pés dele.', 'Varre os dois pés juntos; uke cai de costas.']))
