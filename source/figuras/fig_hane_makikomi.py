"""Figura: Hane-makikomi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): após hane-goshi, tori solta a mão, gira envolvendo o corpo de uke e cai para a frente junto com ele.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 292, 334, ang=238, facing=-1)
tori.leg('far', (310, GROUND - 2), bend=1)
tori.leg('near', (350, 312), bend=-1)
uke = Fig('uke', 334, 282, ang=252, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 244), bend=-1)
uke.leg('near', (ux + 56, 330), bend=-1)
uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 40), bend=1)
uke.arm('far', (tori.neck[0] - 40, tori.neck[1] + 60), bend=1)
tori.arm('near', (tori.neck[0] - 60, 404), bend=1)
tori.arm('far', (tori.neck[0] - 80, tori.neck[1] + 50), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 210), (ux - 90, 150), (ux - 180, 360))

if __name__ == '__main__':
    print(s.render('hane_makikomi'))
