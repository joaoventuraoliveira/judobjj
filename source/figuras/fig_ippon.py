"""Figura: Ippon (projeção completa)
Descrição oficial usada na validação (IJF/Kodokan): uke projetado de costas, com controle de tori pela manga.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = lying('uke', 260, -1, y=398)
tori = standing('tori', 412, -1, lean=30)
uke.arm('near', (346, 334), bend=1)
uke.arm('far', (uke.neck[0] - 30, 404), bend=1)
tori.arm('near', (346, 334), bend=-1)
tori.arm('far', (tori.neck[0] - 40, tori.neck[1] + 70), bend=-1)
s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('ippon'))
