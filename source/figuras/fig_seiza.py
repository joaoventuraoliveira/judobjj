"""Figura: Seiza (estudo e concentração)
Descrição oficial usada na validação (IJF/Kodokan): postura sentada sobre os calcanhares.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = kneeling('tori', 300, 1, lean=0)
tori.arm('near', (tori.pelvis[0] + 46, tori.pelvis[1] - 10), bend=1)
tori.arm('far', (tori.pelvis[0] + 40, tori.pelvis[1] - 6), bend=1)
s.add(tori)

if __name__ == '__main__':
    print(s.render('seiza'))
