"""Figura: Uki-goshi (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori entra com o quadril, envolve a cintura de uke com o braço e gira, lançando-o sobre o quadril sem elevá-lo.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 312, ang=190, facing=-1)
uke = Fig('uke', 330, 300, ang=228, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx + 20, GROUND - 2), bend=1)
tori.leg('near', (tx - 26, GROUND - 2), bend=1)
uke.leg('far', (ux + 40, GROUND - 2), bend=-1)
uke.leg('near', (ux + 66, 380), bend=-1)
tori.arm('near', uke.at(0.18), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 220), (ux - 90, 220 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('uki_goshi'))
