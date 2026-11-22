"""Figura: Sumi-otoshi (5º kyô)
Descrição oficial usada na validação (IJF/Kodokan): tori pisa ao lado externo do pé de uke e, com o corpo e as mãos, projeta-o ao canto traseiro.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=12)
uke = standing('uke', 340, -1, lean=-32)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 30, GROUND - 2), bend=1)
uke.leg('far', (ux + 14, 400), bend=1)
tori.leg('near', (ux - 30, GROUND - 2), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 360))

s.add(tori); s.add(uke)

if __name__ == '__main__':
    print(s.render('sumi_otoshi'))
