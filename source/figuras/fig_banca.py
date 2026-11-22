"""Figura: Banca examinadora
Descrição oficial usada na validação (IJF/Kodokan): candidato saúda a banca de três examinadores.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

for x in (380, 450, 520):
    e = Fig('uke', x, 330, ang=180, facing=-1)
    e.arm('near', (x - 40, 312), bend=-1)
    e.arm('far', (x - 30, 314), bend=-1)
    s.add(e)
s.raw_front('<rect x="336" y="312" width="230" height="20" rx="4" fill="#8B6B4A" stroke="#5A4430" stroke-width="2"/>'
            '<rect x="346" y="332" width="12" height="88" fill="#6E5338"/><rect x="544" y="332" width="12" height="88" fill="#6E5338"/>'
            '<rect x="356" y="332" width="190" height="56" fill="#8B6B4A" fill-opacity="0.35"/>')
tori = standing('tori', 190, 1, lean=30)
tori.arm('near', (tori.pelvis[0] + 18, tori.pelvis[1] + 36), bend=1)
tori.arm('far', (tori.pelvis[0] + 10, tori.pelvis[1] + 40), bend=1)
s.add(tori)

if __name__ == '__main__':
    print(s.render('banca'))
