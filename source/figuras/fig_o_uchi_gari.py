"""Figura: O-uchi-gari (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi ao canto traseiro; tori entra fundo e ceifa a perna de uke por dentro; uke cai para trás.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=18)
uke = standing('uke', 340, -1, lean=-20)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 26, 366), bend=1)
uke.leg('far', (ux + 20, GROUND - 2), bend=1)
tori.leg('near', (ux + 20, 380), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))

s.add(tori); s.add(uke)

if __name__ == '__main__':
    print(s.render('o_uchi_gari'))
