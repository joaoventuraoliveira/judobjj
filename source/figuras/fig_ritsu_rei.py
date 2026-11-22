"""Figura: Ritsu-rei (saudação em pé)
Descrição oficial usada na validação (IJF/Kodokan): saudação de pé antes e depois da prática.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = standing('tori', 200, 1, lean=30)
uke = standing('uke', 420, -1, lean=30)
for f in (tori, uke):
    f.arm('near', (f.pelvis[0] + 18 * f.facing, f.pelvis[1] + 36), bend=f.facing)
    f.arm('far', (f.pelvis[0] + 10 * f.facing, f.pelvis[1] + 40), bend=f.facing)
s.add(tori); s.add(uke)

if __name__ == '__main__':
    print(s.render('ritsu_rei'))
