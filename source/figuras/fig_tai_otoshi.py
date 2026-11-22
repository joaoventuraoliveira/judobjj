"""Figura: Tai-otoshi (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori abre o corpo, põe o pé à frente do pé de uke e o puxa para baixo com as duas mãos, lançando-o sobre a perna.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 318, ang=196, facing=-1)
uke = Fig('uke', 352, 296, ang=222, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx - 22, GROUND - 2), bend=1)
uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
uke.leg('near', (ux - 6, GROUND - 2), bend=-1)
tori.leg('near', (tx + 92, 404), bend=1)
tori.arm('near', uke.at(0.82), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 200), (ux - 90, 200 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('tai_otoshi'))
