"""Figura: Uki-waza (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori abre o corpo, estende a perna bloqueando o pé de uke e cai de lado, projetando-o por cima de si.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 250, 392, ang=104, facing=1)
tori.leg('far', (184, GROUND - 4), bend=1)
uke = Fig('uke', 318, 246, ang=292, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 80, 186), bend=-1)
uke.leg('near', (ux + 44, 360), bend=-1)
tori.leg('near', (ux + 40, 410), bend=1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 70), bend=1)
s.add(tori); s.add(uke)
s.arrow((ux + 70, 150), (ux - 70, 90), (ux - 150, 330))

if __name__ == '__main__':
    print(s.render('uki_waza'))
