"""Figura: Faixas do judô brasileiro
Descrição oficial usada na validação (IJF/Kodokan): sequência de cores da CBJ, do 11º kyu ao 10º dan.
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()

s.shadow = False
belts = [('Branca', '#F7F7F4', None), ('11º kyu', '#F7F7F4', '#9AA0A6'), ('10º kyu', '#9AA0A6', None),
         ('9º kyu', '#9AA0A6', '#1F57B5'), ('8º kyu', '#1F57B5', None), ('7º kyu', '#1F57B5', '#F2C318'),
         ('6º kyu', '#F2C318', None), ('5º kyu', '#F2C318', '#F07F1A'), ('4º kyu', '#F07F1A', None),
         ('3º kyu', '#2E9E4F', None), ('2º kyu', '#7A3FA0', None), ('1º kyu', '#7B4A26', None),
         ('1º a 5º dan', '#111111', None), ('6º a 8º dan', '#C8102E', '#F7F7F4'), ('9º e 10º dan', '#C8102E', None)]
for i, (label, c1, c2) in enumerate(belts):
    col, row = i % 3, i // 3
    x, y = 20 + col * 190, 20 + row * 84
    s.raw_back(f'<rect x="{x}" y="{y}" width="160" height="26" rx="6" fill="{c1}" stroke="#3B3B3B" stroke-width="2"/>')
    if c2:
        s.raw_back(f'<rect x="{x+80}" y="{y+1}" width="79" height="24" rx="5" fill="{c2}"/>'
                   f'<rect x="{x}" y="{y}" width="160" height="26" rx="6" fill="none" stroke="#3B3B3B" stroke-width="2"/>')
    s.raw_back(f'<text x="{x+80}" y="{y+52}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="17" fill="#222">{label}</text>')
s.w, s.h = 590, 440

if __name__ == '__main__':
    print(s.render('faixas'))
