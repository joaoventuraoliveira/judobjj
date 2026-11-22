"""Figura: Ko-soto-gari (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi para trás; tori varre o tornozelo de uke por trás com a sola do pé.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=8)
uke = standing('uke', 340, -1, lean=-18)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 40, 392), bend=1)
tori.leg('near', (ux - 28, 400), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('ko_soto_gari'))
