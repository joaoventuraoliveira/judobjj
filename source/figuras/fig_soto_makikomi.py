"""Figura: Soto-makikomi (4º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori solta a pegada, gira, prende o braço de uke na axila e enrola o corpo dele ao seu redor.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 296, 336, ang=246, facing=-1)
tori.leg('far', (318, GROUND - 2), bend=1)
tori.leg('near', (366, GROUND - 2), bend=1)
uke = Fig('uke', 334, 286, ang=254, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 248), bend=-1)
uke.leg('near', (ux + 50, 340), bend=-1)
uke.arm('near', (tori.at(0.7)[0] - 50, tori.at(0.7)[1] + 20), bend=1)
uke.arm('far', (tori.neck[0] - 40, tori.neck[1] + 60), bend=1)
tori.arm('near', (tori.neck[0] - 40, 404), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 54), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 210), (ux - 90, 150), (ux - 180, 360))

if __name__ == '__main__':
    print(s.render('soto_makikomi'))
