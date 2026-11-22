"""Figura: Uchi-mata (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi à frente; tori varre fundo a coxa interna de uke com a parte de trás da coxa direita, girando à esquerda.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 290, 300, ang=232, facing=-1)
tori.leg('far', (tori.pelvis[0] - 8, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] + 112, 214), bend=1)
uke = Fig('uke', 340, 250, ang=250, facing=-1)
uke.leg('far', (uke.pelvis[0] + 40, 360), bend=-1)
uke.leg('near', (uke.pelvis[0] + 92, 196), bend=-1)
tori.arm('near', uke.at(0.85), bend=1)
tori.arm('far', (tori.neck[0] - 60, tori.neck[1] + 70), bend=-1)
uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 30), bend=1)
uke.arm('far', (tori.neck[0] - 55, tori.neck[1] + 66), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 70, 170), (uke.pelvis[0] - 60, 90), (uke.pelvis[0] - 170, 260))

if __name__ == '__main__':
    print(s.render('uchi_mata'))
