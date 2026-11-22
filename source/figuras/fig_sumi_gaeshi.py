"""Figura: Sumi-gaeshi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori cai para trás apoiando o peito do pé atrás da coxa de uke e o lança por cima da cabeça.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 248, 396, ang=100, facing=1)
tori.leg('far', (178, GROUND - 4), bend=1)
uke = Fig('uke', 302, 270, ang=62, facing=1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 96, 230), bend=1)
uke.leg('near', (ux - 66, 300), bend=1)
tori.leg('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
uke.arm('near', (uke.neck[0] + 34, uke.neck[1] + 60), bend=-1)
uke.arm('far', (uke.neck[0] + 46, uke.neck[1] + 50), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux - 40, 200), (ux + 110, 130), (ux + 180, 330))

if __name__ == '__main__':
    print(s.render('sumi_gaeshi'))
