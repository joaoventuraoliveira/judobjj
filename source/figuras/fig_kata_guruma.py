"""Figura: Kata-guruma (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori eleva uke sobre os ombros, passando-o pela nuca, e o lança para baixo, à frente.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 336, ang=196, facing=-1)
tori.leg('far', (318, GROUND - 2), bend=1)
tori.leg('near', (262, GROUND - 2), bend=1)
uke = Fig('uke', tori.neck[0] + 44, tori.neck[1] - 24, ang=272, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 52, 330), bend=-1)
uke.leg('near', (ux + 70, 318), bend=-1)
uke.arm('near', (uke.neck[0] - 12, uke.neck[1] + 80), bend=1)
uke.arm('far', (uke.neck[0] + 10, uke.neck[1] + 84), bend=1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', (uke.neck[0] - 4, uke.neck[1] + 60), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 60, 170), (ux - 100, 120), (ux - 190, 320))

if __name__ == '__main__':
    print(s.render('kata_guruma'))
