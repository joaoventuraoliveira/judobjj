"""Figura: O-soto-gari (1º kyô)
Descrição oficial usada na validação (IJF/Kodokan): kuzushi para trás/canto traseiro direito; tori ceifa a perna de apoio de uke com a perna direita; uke cai para trás.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = s.add(standing('tori', 272, 1, lean=22))
uke = s.add(standing('uke', 338, -1, lean=-26))
grip(tori, uke)
uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))

if __name__ == '__main__':
    print(s.render('o_soto_gari'))
