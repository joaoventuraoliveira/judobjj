"""Figura: Yoko-ukemi (queda lateral)
Descrição oficial usada na validação (IJF/Kodokan): queda de lado com batida do braço no tatame.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

tori = Fig('tori', 300, 392, ang=104, facing=1)
tori.leg('far', (196, 404), bend=1)
tori.leg('near', (214, 350), bend=1)
tori.arm('far', (tori.neck[0] + 40, tori.neck[1] - 30), bend=-1)
tori.arm('near', (tori.pelvis[0] + 20, GROUND - 2), bend=1)
s.add(tori)
s.raw_front('<path d="M300 432 l-18 10 M320 434 l0 14 M340 432 l18 10" stroke="#D62828" stroke-width="5" stroke-linecap="round"/>')

if __name__ == '__main__':
    print(s.render('yoko_ukemi'))
