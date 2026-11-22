"""Figura: Yoko-wakare (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori cai de lado estendendo as duas pernas à frente de uke e o lança por cima do corpo estendido.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 396, ang=272, facing=-1)
tori.leg('far', (412, 408), bend=1)
tori.leg('near', (420, 398), bend=1)
uke = Fig('uke', 382, 286, ang=238, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 20, GROUND - 2), bend=-1)
uke.leg('near', (ux + 44, 392), bend=-1)
uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 70), bend=1)
uke.arm('far', (uke.neck[0] - 20, uke.neck[1] + 80), bend=1)
tori.arm('near', uke.at(0.8), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 30, 220), (ux - 110, 170), (ux - 200, 340))

if __name__ == '__main__':
    print(s.render('yoko_wakare'))
