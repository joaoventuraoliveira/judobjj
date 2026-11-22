"""Figura: O-soto-guruma (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi para trás; tori estende a perna atrás dos joelhos de uke e o roda por cima dela.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=22)
uke = standing('uke', 340, -1, lean=-28)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 6, GROUND - 2), bend=1)
uke.leg('far', (ux + 22, GROUND - 2), bend=1)
tori.leg('far', (ux - 44, GROUND - 2), bend=-1)
tori.leg('near', (ux + 86, 336), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 360))

s.add(tori); s.add(uke)

if __name__ == '__main__':
    print(s.render('o_soto_guruma'))
