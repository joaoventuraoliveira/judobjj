"""Figura: Ushiro-goshi (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): contragolpe a um golpe de quadril: tori envolve a cintura de uke por trás, levanta-o no ar e o arremessa de costas.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = Fig('uke', 296, 224, ang=168, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 30, 350), bend=-1)
uke.leg('near', (ux - 10, 344), bend=-1)
tori = Fig('tori', 330, 324, ang=172, facing=-1)
tori.leg('far', (356, GROUND - 2), bend=1)
tori.leg('near', (304, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.15), bend=1)
tori.arm('far', uke.at(0.3), bend=1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 20), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux - 40, 130), (ux + 40, 40), (ux + 160, 300))

if __name__ == '__main__':
    print(s.render('ushiro_goshi'))
