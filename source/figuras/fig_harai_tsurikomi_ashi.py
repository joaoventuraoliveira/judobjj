"""Figura: Harai-tsurikomi-ashi (3º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori puxa e eleva uke para a frente e varre o tornozelo do pé avançado pela frente.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=-14)
uke = standing('uke', 340, -1, lean=18)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 46, 392), bend=1)
tori.leg('near', (ux - 50, 396), bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 20, 120), (tx - 60, 330))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('harai_tsurikomi_ashi'))
