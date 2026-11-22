"""Figura: Tsurikomi-goshi (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori desce o quadril abaixo das coxas de uke e o eleva puxando com as duas mãos, lançando-o sobre os quadris.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = Fig('tori', 300, 338, ang=196, facing=-1)
uke = Fig('uke', 330, 300, ang=236, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]

tori.leg('far', (tx + 24, GROUND - 2), bend=1)
tori.leg('near', (tx - 30, GROUND - 2), bend=1)
uke.leg('far', (ux + 48, GROUND - 4), bend=-1)
uke.leg('near', (ux + 74, 378), bend=-1)
tori.arm('near', uke.at(0.97), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 210), (ux - 90, 210 - 90), (ux - 175, 330))

if __name__ == '__main__':
    print(s.render('tsurikomi_goshi'))
