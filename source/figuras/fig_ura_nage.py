"""Figura: Ura-nage (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori envolve a cintura de uke, levanta-o e cai para trás, projetando-o por cima do ombro.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 346, ang=222, facing=1)
tori.leg('far', (330, GROUND - 2), bend=-1)
tori.leg('near', (350, GROUND - 2), bend=-1)
uke = Fig('uke', tori.neck[0] - 70, tori.neck[1] - 70, ang=318, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 60, uke.pelvis[1] - 90), bend=-1)
uke.leg('near', (ux + 30, uke.pelvis[1] - 100), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 60), bend=1)
tori.arm('near', uke.at(0.1), bend=-1)
tori.arm('far', uke.at(0.3), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux + 60, uke.pelvis[1] - 110), (ux - 80, uke.pelvis[1] - 120), (ux - 140, 360))

if __name__ == '__main__':
    print(s.render('ura_nage'))
