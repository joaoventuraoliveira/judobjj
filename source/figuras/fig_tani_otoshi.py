"""Figura: Tani-otoshi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori desliza a perna por trás dos pés de uke e cai de lado; uke cai para o canto traseiro.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = Fig('uke', 334, 304, ang=214, facing=1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
uke.leg('near', (ux + 6, 404), bend=-1)
tori = Fig('tori', 262, 392, ang=150, facing=1)
tori.leg('far', (206, GROUND - 4), bend=1)
tori.leg('near', (ux + 34, 410), bend=-1)
tori.arm('near', uke.at(0.8), bend=-1)
tori.arm('far', uke.at(0.5), bend=-1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 10, uke.head[1] - 20), (uke.head[0] - 90, uke.head[1] - 20), (uke.head[0] - 120, 330))

if __name__ == '__main__':
    print(s.render('tani_otoshi'))
