"""Figura: Hane-goshi (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori puxa uke junto ao lado direito e o lança com o impulso ascendente do quadril e da perna dobrada.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 306, ang=212, facing=-1)
uke = Fig('uke', 336, 276, ang=240, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx - 4, GROUND - 2), bend=1)
uke.leg('far', (ux + 46, 378), bend=-1)
uke.leg('near', (ux + 74, 300), bend=-1)
tori.leg('near', (tx + 42, 352), bend=-1)
tori.arm('near', uke.at(0.82), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 180), (ux - 90, 180 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('hane_goshi'))
