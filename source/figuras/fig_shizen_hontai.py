"""Figura: Shizen-hontai (postura natural)
Descrição oficial usada na validação (IJF/Kodokan): postura natural fundamental, pés na largura dos ombros.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = standing('tori', 300, 1, lean=0, stance=20)
tori.arm('near', (tori.pelvis[0] + 8, tori.pelvis[1] + 40), bend=1)
tori.arm('far', (tori.pelvis[0] - 2, tori.pelvis[1] + 42), bend=1)
s.add(tori)

if __name__ == '__main__':
    print(s.render('shizen_hontai'))
