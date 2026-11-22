"""Figura: Yoko-guruma (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori desliza a perna entre as pernas de uke, cai de lado e o projeta por cima da cabeça.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 326, 398, ang=264, facing=-1)
tori.leg('far', (404, 404), bend=1)
uke = Fig('uke', 330, 246, ang=286, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 180), bend=-1)
uke.leg('near', (ux + 60, 340), bend=-1)
tori.leg('near', (ux + 30, 330), bend=1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 70), bend=1)
tori.arm('near', uke.at(0.3), bend=-1)
tori.arm('far', uke.at(0.7), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux + 70, 150), (ux - 60, 80), (ux - 160, 320))

if __name__ == '__main__':
    print(s.render('yoko_guruma'))
