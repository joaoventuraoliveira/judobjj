"""Figura: Ko-uchi-gari (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi para trás; tori varre o tornozelo de uke pelo lado interno com a sola do pé.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=10)
uke = standing('uke', 340, -1, lean=-16)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 46, 398), bend=1)
uke.leg('far', (ux + 22, GROUND - 2), bend=1)
tori.leg('near', (ux - 10, 404), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('ko_uchi_gari'))
