"""Figura: Kesa-gatame (osaekomi-waza)
Descrição oficial usada na validação (IJF/Kodokan): tori ao lado direito de uke, de frente para a cabeça; braço direito atrás do pescoço, mão esquerda segura o judogi sob a axila; uke de costas.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

uke = lying('uke', 330, 1, y=396)
uke.arm('near', (uke.neck[0] - 30, 330), bend=1)
uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
tori = Fig('tori', 292, 384, ang=150, facing=1)
tori.leg('far', (tori.pelvis[0] - 118, GROUND - 4), bend=1)
tori.leg('near', (tori.pelvis[0] + 40, GROUND - 4), bend=-1)
tori.arm('near', (uke.head[0] + 18, uke.head[1] + 6), bend=1)
tori.arm('far', (uke.neck[0] - 40, 345), bend=1)
s.add(uke); s.add(tori)

if __name__ == '__main__':
    print(s.render('kesa_gatame'))
