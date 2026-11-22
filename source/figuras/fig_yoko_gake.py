"""Figura: Yoko-gake (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi flutuante; tori varre o pé de uke com a sola do pé e cai de lado, projetando-o.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = Fig('uke', 332, 304, ang=222, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 22, GROUND - 2), bend=-1)
uke.leg('near', (ux - 18, 394), bend=-1)
tori = Fig('tori', 256, 372, ang=124, facing=1)
tori.leg('far', (206, GROUND - 4), bend=1)
tori.leg('near', (ux - 24, 400), bend=-1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.55), bend=-1)
uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))

if __name__ == '__main__':
    print(s.render('yoko_gake'))
