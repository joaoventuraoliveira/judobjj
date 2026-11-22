"""Figura: Harai-goshi (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori puxa uke ao quadril, gira e varre a coxa dele com a parte de trás da própria coxa.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 304, ang=222, facing=-1)
uke = Fig('uke', 338, 270, ang=246, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx - 4, GROUND - 2), bend=1)
uke.leg('far', (ux + 48, 372), bend=-1)
uke.leg('near', (ux + 66, 270), bend=-1)
tori.leg('near', (tx + 110, 276), bend=1)
tori.arm('near', uke.at(0.82), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 180), (ux - 90, 180 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('harai_goshi'))
