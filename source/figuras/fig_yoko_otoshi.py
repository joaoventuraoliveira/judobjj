"""Figura: Yoko-otoshi (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi para o lado; tori desliza a perna por fora do pé de uke e cai de lado, lançando-o.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = Fig('uke', 334, 304, ang=226, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 26, GROUND - 2), bend=-1)
uke.leg('near', (ux - 4, 404), bend=-1)
tori = Fig('tori', 262, 392, ang=118, facing=1)
tori.leg('far', (196, GROUND - 4), bend=1)
tori.leg('near', (ux - 2, 412), bend=-1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.55), bend=-1)
uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))

if __name__ == '__main__':
    print(s.render('yoko_otoshi'))
