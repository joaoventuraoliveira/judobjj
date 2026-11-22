"""Figura: Sukui-nage (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori, ao lado de uke, envolve as coxas dele, quebra o equilíbrio para trás, eleva-o e o projeta para trás.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 330, ang=166, facing=1)
tori.leg('far', (268, GROUND - 2), bend=-1)
tori.leg('near', (330, GROUND - 2), bend=-1)
uke = Fig('uke', 334, 246, ang=122, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 92, 290), bend=1)
uke.leg('near', (ux - 104, 262), bend=1)
uke.arm('near', (uke.neck[0] + 40, uke.neck[1] - 30), bend=-1)
uke.arm('far', (uke.neck[0] + 50, uke.neck[1] - 10), bend=-1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', uke.at(0.12), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] + 10, uke.head[1] - 20), (ux + 150, 140), (ux + 160, 360))

if __name__ == '__main__':
    print(s.render('sukui_nage'))
