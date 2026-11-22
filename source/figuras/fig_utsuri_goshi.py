"""Figura: Utsuri-goshi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): contragolpe a um golpe de quadril: tori flexiona os joelhos, eleva uke, troca o quadril e o projeta girando.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = Fig('uke', 290, 246, ang=204, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 8, 380), bend=-1)
uke.leg('near', (ux + 40, 372), bend=-1)
tori = Fig('tori', 326, 330, ang=174, facing=-1)
tori.leg('far', (352, GROUND - 2), bend=1)
tori.leg('near', (300, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.25), bend=1)
tori.arm('far', uke.at(0.45), bend=1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 10, 140), (ux - 110, 120), (ux - 150, 340))

if __name__ == '__main__':
    print(s.render('utsuri_goshi'))
