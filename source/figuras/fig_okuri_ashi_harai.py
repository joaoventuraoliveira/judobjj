"""Figura: Okuri-ashi-harai (2º kyô)
Descrição oficial usada na validação (IJF/Kodokan): quando uke desloca os pés lateralmente, tori acompanha e varre as duas pernas; uke cai de costas.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
tori = standing('tori', 268, 1, lean=-4)
uke = standing('uke', 340, -1, lean=-10)
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]

uke.leg('near', (ux - 12, 392), bend=1)
uke.leg('far', (ux + 6, 398), bend=1)
tori.leg('near', (ux - 22, 400), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 370))

s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('okuri_ashi_harai'))
