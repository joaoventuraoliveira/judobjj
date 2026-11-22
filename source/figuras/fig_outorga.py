"""Figura: Entrega da faixa
Descrição oficial usada na validação (IJF/Kodokan): o examinador entrega a nova faixa ao candidato.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = standing('tori', 240, 1, lean=18)
uke = standing('uke', 370, -1, lean=10)
belt_x, belt_y = 306, 284
uke.arm('near', (belt_x + 26, belt_y + 6), bend=-1)
uke.arm('far', (belt_x + 30, belt_y + 2), bend=-1)
tori.arm('near', (belt_x - 26, belt_y + 6), bend=1)
tori.arm('far', (belt_x - 30, belt_y + 2), bend=1)
s.add(tori); s.add(uke)
s.raw_front(f'<rect x="{belt_x-42}" y="{belt_y-8}" width="84" height="20" rx="6" fill="#111"/>'
            f'<rect x="{belt_x-42}" y="{belt_y+3}" width="84" height="2" fill="#444"/>')

if __name__ == '__main__':
    print(s.render('outorga'))
