"""Figura: Za-rei (saudação ajoelhado)
Descrição oficial usada na validação (IJF/Kodokan): saudação ajoelhada que abre os katas e as aulas.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = kneeling('tori', 150, 1, lean=48)
uke = kneeling('uke', 470, -1, lean=48)
for f in (tori, uke):
    f.arm('near', (f.pelvis[0] + 92 * f.facing, GROUND - 6), bend=f.facing)
    f.arm('far', (f.pelvis[0] + 86 * f.facing, GROUND - 4), bend=f.facing)
s.add(tori); s.add(uke)

if __name__ == '__main__':
    print(s.render('za_rei'))
