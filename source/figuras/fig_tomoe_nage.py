"""Figura: Tomoe-nage (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori cai para trás, apoia o pé direito no abdômen de uke e o lança por cima da própria cabeça (sacrifício).
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 250, 396, ang=100, facing=1)
tori.leg('far', (tori.pelvis[0] - 70, GROUND - 4), bend=1)
uke = Fig('uke', 300, 262, ang=58, facing=1)
uke.leg('far', (uke.pelvis[0] - 100, 210), bend=1)
uke.leg('near', (uke.pelvis[0] - 92, 240), bend=1)
tori.leg('near', uke.at(0.1), bend=1)
tori.arm('near', uke.at(0.9), bend=-1)
tori.arm('far', add(uke.at(0.95), (10, 10)), bend=-1)
uke.arm('near', (uke.neck[0] + 30, uke.neck[1] + 60), bend=-1)
uke.arm('far', (uke.neck[0] + 45, uke.neck[1] + 50), bend=-1)
s.add(tori); s.add(uke)
s.arrow((uke.pelvis[0] - 30, 190), (uke.pelvis[0] + 120, 130), (uke.pelvis[0] + 190, 330))

if __name__ == '__main__':
    print(s.render('tomoe_nage'))
