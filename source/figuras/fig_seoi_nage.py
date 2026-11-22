"""Figura: Seoi-nage (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi à frente; tori gira com o cotovelo direito sob a axila de uke, carrega-o nas costas e lança por cima do ombro.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 318, ang=200, facing=-1)
tori.leg('far', (tori.pelvis[0] + 22, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] - 28, GROUND - 2), bend=1)
uke = Fig('uke', 312, 206, ang=262, facing=-1)
uke.leg('far', (uke.pelvis[0] + 90, 150), bend=-1)
uke.leg('near', (uke.pelvis[0] + 105, 188), bend=-1)
tori.arm('near', uke.at(0.8), bend=1)
tori.arm('far', (tori.pelvis[0] - 70, 300), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
uke.arm('far', (tori.pelvis[0] - 65, 296), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 60, 150), (uke.pelvis[0] - 120, 110), (uke.pelvis[0] - 160, 300))

if __name__ == '__main__':
    print(s.render('seoi_nage'))
