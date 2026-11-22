"""Figura: Hiza-guruma (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi ao canto frontal direito; tori apoia a sola do pé no joelho de uke como fulcro e o gira.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=-12)
uke = standing('uke', 340, -1, lean=22)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 36, GROUND - 2), bend=1)
tori.leg('near', uke.limbs['leg_near'][1], bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('hiza_guruma'))
