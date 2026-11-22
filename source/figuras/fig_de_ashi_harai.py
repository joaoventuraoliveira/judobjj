"""Figura: De-ashi-harai (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): quando uke vai apoiar o peso no pé que acabou de avançar, tori varre esse pé.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=-6)
uke = standing('uke', 340, -1, lean=10)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 50, 404), bend=1)
uke.leg('far', (ux + 16, GROUND - 2), bend=1)
tori.leg('near', (ux - 58, 404), bend=-1)
s.arrow((uke.head[0] + 10, uke.head[1] - 14), (ux + 110, 200), (ux + 120, 360))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('de_ashi_harai'))
