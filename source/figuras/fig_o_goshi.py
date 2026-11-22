"""Figura: O-goshi (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi à frente; tori entra fundo com o quadril direito, eleva uke sobre o quadril e gira, lançando-o por cima.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 312, ang=192, facing=-1)
tori.leg('far', (tori.pelvis[0] + 20, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
uke = Fig('uke', 330, 292, ang=236, facing=-1)
uke.leg('far', (uke.pelvis[0] + 50, 392), bend=-1)
uke.leg('near', (uke.pelvis[0] + 78, 372), bend=-1)
tori.arm('near', uke.at(0.15), bend=1)
tori.arm('far', (tori.pelvis[0] - 72, 262), bend=-1)
uke.arm('near', (tori.neck[0] - 20, tori.neck[1] + 20), bend=1)
uke.arm('far', (tori.pelvis[0] - 68, 260), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 40, 210), (uke.pelvis[0] - 90, 120), (uke.pelvis[0] - 170, 300))

if __name__ == '__main__':
    print(s.render('o_goshi'))
