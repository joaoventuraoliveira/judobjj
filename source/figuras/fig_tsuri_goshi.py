"""Figura: Tsuri-goshi (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori alcança o cinto de uke, puxa-o à frente, eleva-o sobre os quadris e o lança por cima.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 316, ang=192, facing=-1)
uke = Fig('uke', 332, 290, ang=240, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx + 20, GROUND - 2), bend=1)
tori.leg('near', (tx - 26, GROUND - 2), bend=1)
uke.leg('far', (ux + 50, 390), bend=-1)
uke.leg('near', (ux + 76, 368), bend=-1)
tori.arm('near', uke.at(0.12), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 190), (ux - 90, 190 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('tsuri_goshi'))
