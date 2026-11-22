"""Figura: Kumi-kata (pegada básica)
Descrição oficial usada na validação (IJF/Kodokan): mão direita na gola e esquerda na manga.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = standing('tori', 250, 1, lean=4)
uke = standing('uke', 350, -1, lean=4)
grip(tori, uke)
s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('kumikata'))
