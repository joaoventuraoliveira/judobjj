"""Figura: Sasae-tsurikomi-ashi (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi ao canto frontal direito; tori bloqueia a perna de apoio logo acima do tornozelo e gira, puxando.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=-16)
uke = standing('uke', 340, -1, lean=22)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 38, GROUND - 2), bend=1)
k, f = uke.limbs['leg_near'][1], uke.limbs['leg_near'][2]
tori.leg('near', (k[0] + (f[0]-k[0])*0.78, k[1] + (f[1]-k[1])*0.78), bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('sasae_tsurikomi_ashi'))
