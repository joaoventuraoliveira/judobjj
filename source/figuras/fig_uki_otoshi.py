"""Figura: Uki-otoshi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi flutuante ao canto frontal; tori puxa para baixo com as duas mãos e projeta uke em círculo.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 356, ang=196, facing=-1)
tori.leg('far', (252, GROUND - 2), bend=1)
tori.limbs['leg_near'] = (tori.pelvis, (330, 410), (378, 412))
uke = Fig('uke', 322, 212, ang=292, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 84, 160), bend=-1)
uke.leg('near', (ux + 64, 136), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 70), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 54), bend=1)
tori.arm('near', uke.at(0.85), bend=1)
tori.arm('far', (tori.neck[0] - 64, tori.neck[1] + 56), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 70, 120), (ux - 80, 70), (ux - 170, 320))

if __name__ == '__main__':
    print(s.render('uki_otoshi'))
