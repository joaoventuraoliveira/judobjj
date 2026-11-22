"""Figura: O-guruma (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori estende a perna sobre o abdômen ou as coxas de uke e o gira sobre ela.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 300, ang=212, facing=-1)
uke = Fig('uke', 352, 290, ang=230, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx - 6, GROUND - 2), bend=1)
uke.leg('far', (ux + 28, GROUND - 2), bend=-1)
uke.leg('near', (ux - 2, GROUND - 2), bend=-1)
tori.leg('near', (tx + 112, 300), bend=1)
tori.arm('near', uke.at(0.82), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 200), (ux - 90, 200 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('o_guruma'))
