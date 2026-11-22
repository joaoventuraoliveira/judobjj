"""
make_scripts.py — gera um script fig_<nome>.py por figura a partir das cenas abaixo.
Cada script gerado é autônomo: importa judoka.py e renderiza a sua figura.
Para regerar tudo:  python3 make_scripts.py && python3 run_all.py
"""
import os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))

HEADER = '''"""Figura: {title}
Descrição oficial usada na validação (IJF/Kodokan): {ref}
Gerado por make_scripts.py — pode ser editado à mão.
"""
from judoka import Scene, Fig, standing, kneeling, lying, grip, add, GROUND

s = Scene()
'''

FOOTER = '''
if __name__ == '__main__':
    print(s.render('{name}'))
'''

SCENES = {}


def scene(name, title, ref):
    def deco(code):
        SCENES[name] = (title, ref, textwrap.dedent(code))
        return code
    return deco


# --------------------------------------------------------------------- piloto
scene('o_soto_gari', 'O-soto-gari (1º kyô)',
      'kuzushi para trás/canto traseiro direito; tori ceifa a perna de apoio de uke com a perna direita; uke cai para trás.')('''
tori = s.add(standing('tori', 272, 1, lean=22))
uke = s.add(standing('uke', 338, -1, lean=-26))
grip(tori, uke)
uke.leg('far', (uke.pelvis[0] + 18, GROUND - 2), bend=1)
uke.leg('near', (uke.pelvis[0] - 30, 338), bend=1)
tori.leg('far', (uke.pelvis[0] - 40, GROUND - 2), bend=-1)
tori.leg('near', (uke.pelvis[0] + 62, 300), bend=-1)
s.arrow((uke.head[0] + 20, uke.head[1] - 10), (uke.head[0] + 110, uke.head[1] + 10), (uke.head[0] + 112, 300))
''')

scene('seoi_nage', 'Seoi-nage (1º kyô)',
      'kuzushi à frente; tori gira com o cotovelo direito sob a axila de uke, carrega-o nas costas e lança por cima do ombro.')('''
tori = Fig('tori', 300, 318, ang=200, facing=-1)
tori.leg('far', (tori.pelvis[0] + 22, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] - 28, GROUND - 2), bend=1)
uke = Fig('uke', 312, 206, ang=262, facing=-1)
uke.leg('far', (uke.pelvis[0] + 90, 150), bend=-1)
uke.leg('near', (uke.pelvis[0] + 105, 188), bend=-1)
tori.arm('near', uke.at(0.8), bend=1)
tori.arm('far', (tori.pelvis[0] - 70, 300), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
uke.arm('far', (tori.pelvis[0] - 65, 296), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 60, 150), (uke.pelvis[0] - 120, 110), (uke.pelvis[0] - 160, 300))
''')

scene('o_goshi', 'O-goshi (1º kyô)',
      'kuzushi à frente; tori entra fundo com o quadril direito, eleva uke sobre o quadril e gira, lançando-o por cima.')('''
tori = Fig('tori', 300, 312, ang=192, facing=-1)
tori.leg('far', (tori.pelvis[0] + 20, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] - 26, GROUND - 2), bend=1)
uke = Fig('uke', 330, 292, ang=236, facing=-1)
uke.leg('far', (uke.pelvis[0] + 50, 392), bend=-1)
uke.leg('near', (uke.pelvis[0] + 78, 372), bend=-1)
tori.arm('near', uke.at(0.15), bend=1)
tori.arm('far', (tori.pelvis[0] - 72, 262), bend=-1)
uke.arm('near', (tori.neck[0] - 20, tori.neck[1] + 20), bend=1)
uke.arm('far', (tori.pelvis[0] - 68, 260), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 40, 210), (uke.pelvis[0] - 90, 120), (uke.pelvis[0] - 170, 300))
''')

scene('uchi_mata', 'Uchi-mata (2º kyô)',
      'kuzushi à frente; tori varre fundo a coxa interna de uke com a parte de trás da coxa direita, girando à esquerda.')('''
tori = Fig('tori', 290, 300, ang=232, facing=-1)
tori.leg('far', (tori.pelvis[0] - 8, GROUND - 2), bend=1)
tori.leg('near', (tori.pelvis[0] + 112, 214), bend=1)
uke = Fig('uke', 340, 250, ang=250, facing=-1)
uke.leg('far', (uke.pelvis[0] + 40, 360), bend=-1)
uke.leg('near', (uke.pelvis[0] + 92, 196), bend=-1)
tori.arm('near', uke.at(0.85), bend=1)
tori.arm('far', (tori.neck[0] - 60, tori.neck[1] + 70), bend=-1)
uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 30), bend=1)
uke.arm('far', (tori.neck[0] - 55, tori.neck[1] + 66), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.pelvis[0] + 70, 170), (uke.pelvis[0] - 60, 90), (uke.pelvis[0] - 170, 260))
''')

scene('tomoe_nage', 'Tomoe-nage (3º kyô)',
      'tori cai para trás, apoia o pé direito no abdômen de uke e o lança por cima da própria cabeça (sacrifício).')('''
tori = Fig('tori', 250, 396, ang=100, facing=1)
tori.leg('far', (tori.pelvis[0] - 70, GROUND - 4), bend=1)
uke = Fig('uke', 300, 262, ang=58, facing=1)
uke.leg('far', (uke.pelvis[0] - 100, 210), bend=1)
uke.leg('near', (uke.pelvis[0] - 92, 240), bend=1)
tori.leg('near', uke.at(0.1), bend=1)
tori.arm('near', uke.at(0.9), bend=-1)
tori.arm('far', add(uke.at(0.95), (10, 10)), bend=-1)
uke.arm('near', (uke.neck[0] + 30, uke.neck[1] + 60), bend=-1)
uke.arm('far', (uke.neck[0] + 45, uke.neck[1] + 50), bend=-1)
s.add(tori); s.add(uke)
s.arrow((uke.pelvis[0] - 30, 190), (uke.pelvis[0] + 120, 130), (uke.pelvis[0] + 190, 330))
''')

scene('kesa_gatame', 'Kesa-gatame (osaekomi-waza)',
      'tori ao lado direito de uke, de frente para a cabeça; braço direito atrás do pescoço, mão esquerda segura o judogi sob a axila; uke de costas.')('''
uke = lying('uke', 330, 1, y=396)
uke.arm('near', (uke.neck[0] - 30, 330), bend=1)
uke.arm('far', (uke.neck[0] + 40, 405), bend=-1)
tori = Fig('tori', 292, 384, ang=150, facing=1)
tori.leg('far', (tori.pelvis[0] - 118, GROUND - 4), bend=1)
tori.leg('near', (tori.pelvis[0] + 40, GROUND - 4), bend=-1)
tori.arm('near', (uke.head[0] + 18, uke.head[1] + 6), bend=1)
tori.arm('far', (uke.neck[0] - 40, 345), bend=1)
s.add(uke); s.add(tori)
''')

# ============================== técnicas restantes do Gokyo ==============================
FACE = """tori = standing('tori', 268, 1, lean={lt})
uke = standing('uke', 340, -1, lean={lu})
grip(tori, uke)
tori.arms_top = True
ux, tx = uke.pelvis[0], tori.pelvis[0]
"""

def face(name, title, ref, lt, lu, body, order='tori,uke'):
    a, b = order.split(',')
    scene(name, title, ref)(FACE.format(lt=lt, lu=lu) + body + f"\ns.add({a}); s.add({b})\n")

face('de_ashi_harai', 'De-ashi-harai (1º kyô)', 'quando uke vai apoiar o peso no pé que acabou de avançar, tori varre esse pé.', -6, 10, """
uke.leg('near', (ux - 50, 404), bend=1)
uke.leg('far', (ux + 16, GROUND - 2), bend=1)
tori.leg('near', (ux - 58, 404), bend=-1)
s.arrow((uke.head[0] + 10, uke.head[1] - 14), (ux + 110, 200), (ux + 120, 360))
""", order='uke,tori')

face('hiza_guruma', 'Hiza-guruma (1º kyô)', 'kuzushi ao canto frontal direito; tori apoia a sola do pé no joelho de uke como fulcro e o gira.', -12, 22, """
uke.leg('near', (ux - 36, GROUND - 2), bend=1)
tori.leg('near', uke.limbs['leg_near'][1], bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))
""", order='uke,tori')

face('sasae_tsurikomi_ashi', 'Sasae-tsurikomi-ashi (1º kyô)', 'kuzushi ao canto frontal direito; tori bloqueia a perna de apoio logo acima do tornozelo e gira, puxando.', -16, 22, """
uke.leg('near', (ux - 38, GROUND - 2), bend=1)
k, f = uke.limbs['leg_near'][1], uke.limbs['leg_near'][2]
tori.leg('near', (k[0] + (f[0]-k[0])*0.78, k[1] + (f[1]-k[1])*0.78), bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 30, 120), (tx - 70, 330))
""", order='uke,tori')

face('harai_tsurikomi_ashi', 'Harai-tsurikomi-ashi (3º kyô)', 'tori puxa e eleva uke para a frente e varre o tornozelo do pé avançado pela frente.', -14, 18, """
uke.leg('near', (ux - 46, 392), bend=1)
tori.leg('near', (ux - 50, 396), bend=-1)
s.arrow((uke.head[0] + 6, uke.head[1] - 16), (tx - 20, 120), (tx - 60, 330))
""", order='uke,tori')

face('okuri_ashi_harai', 'Okuri-ashi-harai (2º kyô)', 'quando uke desloca os pés lateralmente, tori acompanha e varre as duas pernas; uke cai de costas.', -4, -10, """
uke.leg('near', (ux - 12, 392), bend=1)
uke.leg('far', (ux + 6, 398), bend=1)
tori.leg('near', (ux - 22, 400), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 370))
""", order='uke,tori')

face('ko_soto_gari', 'Ko-soto-gari (2º kyô)', 'kuzushi para trás; tori varre o tornozelo de uke por trás com a sola do pé.', 8, -18, """
uke.leg('near', (ux - 40, 392), bend=1)
tori.leg('near', (ux - 28, 400), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))
""", order='uke,tori')

face('ko_soto_gake', 'Ko-soto-gake (3º kyô)', 'kuzushi para trás; tori engancha o tornozelo de uke por trás e o lança para trás.', 10, -22, """
uke.leg('near', (ux - 12, GROUND - 2), bend=1)
tori.leg('near', (ux + 12, 398), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))
""")

face('ko_uchi_gari', 'Ko-uchi-gari (2º kyô)', 'kuzushi para trás; tori varre o tornozelo de uke pelo lado interno com a sola do pé.', 10, -16, """
uke.leg('near', (ux - 46, 398), bend=1)
uke.leg('far', (ux + 22, GROUND - 2), bend=1)
tori.leg('near', (ux - 10, 404), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))
""", order='uke,tori')

face('o_uchi_gari', 'O-uchi-gari (1º kyô)', 'kuzushi ao canto traseiro; tori entra fundo e ceifa a perna de uke por dentro; uke cai para trás.', 18, -20, """
uke.leg('near', (ux - 26, 366), bend=1)
uke.leg('far', (ux + 20, GROUND - 2), bend=1)
tori.leg('near', (ux + 20, 380), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 110, 210), (ux + 120, 370))
""")

face('o_soto_guruma', 'O-soto-guruma (5º kyô)', 'kuzushi para trás; tori estende a perna atrás dos joelhos de uke e o roda por cima dela.', 22, -28, """
uke.leg('near', (ux - 6, GROUND - 2), bend=1)
uke.leg('far', (ux + 22, GROUND - 2), bend=1)
tori.leg('far', (ux - 44, GROUND - 2), bend=-1)
tori.leg('near', (ux + 86, 336), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 360))
""")

face('sumi_otoshi', 'Sumi-otoshi (5º kyô)', 'tori pisa ao lado externo do pé de uke e, com o corpo e as mãos, projeta-o ao canto traseiro.', 12, -32, """
uke.leg('near', (ux - 30, GROUND - 2), bend=1)
uke.leg('far', (ux + 14, 400), bend=1)
tori.leg('near', (ux - 30, GROUND - 2), bend=-1)
s.arrow((uke.head[0] + 16, uke.head[1] - 10), (ux + 120, 200), (ux + 130, 360))
""")

# ---- entradas de costas (tori gira e fica de costas para uke; projeção para a esquerda)
TURN = """tori = Fig('tori', 300, {tpy}, ang={tang}, facing=-1)
uke = Fig('uke', {ux}, {upy}, ang={uang}, facing=-1)
tx, ux = tori.pelvis[0], uke.pelvis[0]
"""
ARMS = """tori.arm('near', {tn}, bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 60), bend=-1)
uke.arm('near', (tori.neck[0] - 14, tori.neck[1] + 26), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 62), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, {ay}), (ux - 90, {ay} - 90), (ux - 175, 330))
"""

def turn(name, title, ref, tpy, tang, ux, upy, uang, legs, tn='uke.at(0.82)', ay=190):
    scene(name, title, ref)(TURN.format(tpy=tpy, tang=tang, ux=ux, upy=upy, uang=uang) + legs + ARMS.format(tn=tn, ay=ay))

turn('uki_goshi', 'Uki-goshi (1º kyô)', 'tori entra com o quadril, envolve a cintura de uke com o braço e gira, lançando-o sobre o quadril sem elevá-lo.',
     312, 190, 330, 300, 228, """
tori.leg('far', (tx + 20, GROUND - 2), bend=1)
tori.leg('near', (tx - 26, GROUND - 2), bend=1)
uke.leg('far', (ux + 40, GROUND - 2), bend=-1)
uke.leg('near', (ux + 66, 380), bend=-1)
""", tn='uke.at(0.18)', ay=220)

turn('koshi_guruma', 'Koshi-guruma (2º kyô)', 'tori encaixa o quadril, envolve o pescoço de uke e o roda sobre os quadris com amplo movimento.',
     316, 194, 334, 284, 244, """
tori.leg('far', (tx + 20, GROUND - 2), bend=1)
tori.leg('near', (tx - 26, GROUND - 2), bend=1)
uke.leg('far', (ux + 52, 378), bend=-1)
uke.leg('near', (ux + 80, 350), bend=-1)
""", tn='uke.neck')

turn('tsurikomi_goshi', 'Tsurikomi-goshi (2º kyô)', 'tori desce o quadril abaixo das coxas de uke e o eleva puxando com as duas mãos, lançando-o sobre os quadris.',
     338, 196, 330, 300, 236, """
tori.leg('far', (tx + 24, GROUND - 2), bend=1)
tori.leg('near', (tx - 30, GROUND - 2), bend=1)
uke.leg('far', (ux + 48, GROUND - 4), bend=-1)
uke.leg('near', (ux + 74, 378), bend=-1)
""", tn='uke.at(0.97)', ay=210)

turn('tsuri_goshi', 'Tsuri-goshi (3º kyô)', 'tori alcança o cinto de uke, puxa-o à frente, eleva-o sobre os quadris e o lança por cima.',
     316, 192, 332, 290, 240, """
tori.leg('far', (tx + 20, GROUND - 2), bend=1)
tori.leg('near', (tx - 26, GROUND - 2), bend=1)
uke.leg('far', (ux + 50, 390), bend=-1)
uke.leg('near', (ux + 76, 368), bend=-1)
""", tn='uke.at(0.12)')

turn('harai_goshi', 'Harai-goshi (2º kyô)', 'tori puxa uke ao quadril, gira e varre a coxa dele com a parte de trás da própria coxa.',
     304, 222, 338, 270, 246, """
tori.leg('far', (tx - 4, GROUND - 2), bend=1)
uke.leg('far', (ux + 48, 372), bend=-1)
uke.leg('near', (ux + 66, 270), bend=-1)
tori.leg('near', (tx + 110, 276), bend=1)
""", ay=180)

turn('hane_goshi', 'Hane-goshi (3º kyô)', 'tori puxa uke junto ao lado direito e o lança com o impulso ascendente do quadril e da perna dobrada.',
     306, 212, 336, 276, 240, """
tori.leg('far', (tx - 4, GROUND - 2), bend=1)
uke.leg('far', (ux + 46, 378), bend=-1)
uke.leg('near', (ux + 74, 300), bend=-1)
tori.leg('near', (tx + 42, 352), bend=-1)
""", ay=180)

turn('ashi_guruma', 'Ashi-guruma (3º kyô)', 'tori gira e estende a perna sobre o joelho de uke, lançando-o num círculo por cima dela.',
     300, 210, 350, 292, 226, """
tori.leg('far', (tx - 6, GROUND - 2), bend=1)
uke.leg('far', (ux + 28, GROUND - 2), bend=-1)
uke.leg('near', (ux - 4, GROUND - 2), bend=-1)
tori.leg('near', (tx + 112, 352), bend=1)
""", ay=200)

turn('o_guruma', 'O-guruma (4º kyô)', 'tori estende a perna sobre o abdômen ou as coxas de uke e o gira sobre ela.',
     300, 212, 352, 290, 230, """
tori.leg('far', (tx - 6, GROUND - 2), bend=1)
uke.leg('far', (ux + 28, GROUND - 2), bend=-1)
uke.leg('near', (ux - 2, GROUND - 2), bend=-1)
tori.leg('near', (tx + 112, 300), bend=1)
""", ay=200)

turn('tai_otoshi', 'Tai-otoshi (2º kyô)', 'tori abre o corpo, põe o pé à frente do pé de uke e o puxa para baixo com as duas mãos, lançando-o sobre a perna.',
     318, 196, 352, 296, 222, """
tori.leg('far', (tx - 22, GROUND - 2), bend=1)
uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
uke.leg('near', (ux - 6, GROUND - 2), bend=-1)
tori.leg('near', (tx + 92, 404), bend=1)
""", ay=200)


scene('kata_guruma', 'Kata-guruma (3º kyô)', 'tori eleva uke sobre os ombros, passando-o pela nuca, e o lança para baixo, à frente.')("""
tori = Fig('tori', 300, 336, ang=196, facing=-1)
tori.leg('far', (318, GROUND - 2), bend=1)
tori.leg('near', (262, GROUND - 2), bend=1)
uke = Fig('uke', tori.neck[0] + 44, tori.neck[1] - 24, ang=272, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 52, 330), bend=-1)
uke.leg('near', (ux + 70, 318), bend=-1)
uke.arm('near', (uke.neck[0] - 12, uke.neck[1] + 80), bend=1)
uke.arm('far', (uke.neck[0] + 10, uke.neck[1] + 84), bend=1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', (uke.neck[0] - 4, uke.neck[1] + 60), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 60, 170), (ux - 100, 120), (ux - 190, 320))
""")

scene('uki_otoshi', 'Uki-otoshi (4º kyô)', 'kuzushi flutuante ao canto frontal; tori puxa para baixo com as duas mãos e projeta uke em círculo.')("""
tori = Fig('tori', 300, 356, ang=196, facing=-1)
tori.leg('far', (252, GROUND - 2), bend=1)
tori.limbs['leg_near'] = (tori.pelvis, (330, 410), (378, 412))
uke = Fig('uke', 322, 212, ang=292, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 84, 160), bend=-1)
uke.leg('near', (ux + 64, 136), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 70), bend=1)
uke.arm('far', (tori.neck[0] - 60, tori.neck[1] + 54), bend=1)
tori.arm('near', uke.at(0.85), bend=1)
tori.arm('far', (tori.neck[0] - 64, tori.neck[1] + 56), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 70, 120), (ux - 80, 70), (ux - 170, 320))
""")

scene('sukui_nage', 'Sukui-nage (4º kyô)', 'tori, ao lado de uke, envolve as coxas dele, quebra o equilíbrio para trás, eleva-o e o projeta para trás.')("""
tori = Fig('tori', 300, 330, ang=166, facing=1)
tori.leg('far', (268, GROUND - 2), bend=-1)
tori.leg('near', (330, GROUND - 2), bend=-1)
uke = Fig('uke', 334, 246, ang=122, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 92, 290), bend=1)
uke.leg('near', (ux - 104, 262), bend=1)
uke.arm('near', (uke.neck[0] + 40, uke.neck[1] - 30), bend=-1)
uke.arm('far', (uke.neck[0] + 50, uke.neck[1] - 10), bend=-1)
tori.arm('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('far', uke.at(0.12), bend=1)
s.add(uke); s.add(tori)
s.arrow((uke.head[0] + 10, uke.head[1] - 20), (ux + 150, 140), (ux + 160, 360))
""")

scene('utsuri_goshi', 'Utsuri-goshi (4º kyô)', 'contragolpe a um golpe de quadril: tori flexiona os joelhos, eleva uke, troca o quadril e o projeta girando.')("""
uke = Fig('uke', 290, 246, ang=204, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 8, 380), bend=-1)
uke.leg('near', (ux + 40, 372), bend=-1)
tori = Fig('tori', 326, 330, ang=174, facing=-1)
tori.leg('far', (352, GROUND - 2), bend=1)
tori.leg('near', (300, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.25), bend=1)
tori.arm('far', uke.at(0.45), bend=1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 60), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux + 10, 140), (ux - 110, 120), (ux - 150, 340))
""")

scene('ushiro_goshi', 'Ushiro-goshi (5º kyô)', 'contragolpe a um golpe de quadril: tori envolve a cintura de uke por trás, levanta-o no ar e o arremessa de costas.')("""
uke = Fig('uke', 296, 224, ang=168, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 30, 350), bend=-1)
uke.leg('near', (ux - 10, 344), bend=-1)
tori = Fig('tori', 330, 324, ang=172, facing=-1)
tori.leg('far', (356, GROUND - 2), bend=1)
tori.leg('near', (304, GROUND - 2), bend=1)
tori.arm('near', uke.at(0.15), bend=1)
tori.arm('far', uke.at(0.3), bend=1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 20), bend=1)
uke.arm('far', (uke.neck[0] - 40, uke.neck[1] + 50), bend=1)
s.add(uke); s.add(tori)
s.arrow((ux - 40, 130), (ux + 40, 40), (ux + 160, 300))
""")

scene('ura_nage', 'Ura-nage (5º kyô)', 'tori envolve a cintura de uke, levanta-o e cai para trás, projetando-o por cima do ombro.')("""
tori = Fig('tori', 300, 346, ang=222, facing=1)
tori.leg('far', (330, GROUND - 2), bend=-1)
tori.leg('near', (350, GROUND - 2), bend=-1)
uke = Fig('uke', tori.neck[0] - 70, tori.neck[1] - 70, ang=318, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 60, uke.pelvis[1] - 90), bend=-1)
uke.leg('near', (ux + 30, uke.pelvis[1] - 100), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 50), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 60), bend=1)
tori.arm('near', uke.at(0.1), bend=-1)
tori.arm('far', uke.at(0.3), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux + 60, uke.pelvis[1] - 110), (ux - 80, uke.pelvis[1] - 120), (ux - 140, 360))
""")

# ---- sutemi-waza
scene('sumi_gaeshi', 'Sumi-gaeshi (4º kyô)', 'tori cai para trás apoiando o peito do pé atrás da coxa de uke e o lança por cima da cabeça.')("""
tori = Fig('tori', 248, 396, ang=100, facing=1)
tori.leg('far', (178, GROUND - 4), bend=1)
uke = Fig('uke', 302, 270, ang=62, facing=1)
ux = uke.pelvis[0]
uke.leg('far', (ux - 96, 230), bend=1)
uke.leg('near', (ux - 66, 300), bend=1)
tori.leg('near', uke.limbs['leg_near'][1], bend=1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
uke.arm('near', (uke.neck[0] + 34, uke.neck[1] + 60), bend=-1)
uke.arm('far', (uke.neck[0] + 46, uke.neck[1] + 50), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux - 40, 200), (ux + 110, 130), (ux + 180, 330))
""")

scene('tani_otoshi', 'Tani-otoshi (4º kyô)', 'tori desliza a perna por trás dos pés de uke e cai de lado; uke cai para o canto traseiro.')("""
uke = Fig('uke', 334, 304, ang=214, facing=1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 30, GROUND - 2), bend=-1)
uke.leg('near', (ux + 6, 404), bend=-1)
tori = Fig('tori', 262, 392, ang=150, facing=1)
tori.leg('far', (206, GROUND - 4), bend=1)
tori.leg('near', (ux + 34, 410), bend=-1)
tori.arm('near', uke.at(0.8), bend=-1)
tori.arm('far', uke.at(0.5), bend=-1)
uke.arm('near', (uke.neck[0] - 50, uke.neck[1] + 30), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 10, uke.head[1] - 20), (uke.head[0] - 90, uke.head[1] - 20), (uke.head[0] - 120, 330))
""")

scene('yoko_otoshi', 'Yoko-otoshi (3º kyô)', 'kuzushi para o lado; tori desliza a perna por fora do pé de uke e cai de lado, lançando-o.')("""
uke = Fig('uke', 334, 304, ang=226, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 26, GROUND - 2), bend=-1)
uke.leg('near', (ux - 4, 404), bend=-1)
tori = Fig('tori', 262, 392, ang=118, facing=1)
tori.leg('far', (196, GROUND - 4), bend=1)
tori.leg('near', (ux - 2, 412), bend=-1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.55), bend=-1)
uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))
""")

scene('uki_waza', 'Uki-waza (5º kyô)', 'tori abre o corpo, estende a perna bloqueando o pé de uke e cai de lado, projetando-o por cima de si.')("""
tori = Fig('tori', 250, 392, ang=104, facing=1)
tori.leg('far', (184, GROUND - 4), bend=1)
uke = Fig('uke', 318, 246, ang=292, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 80, 186), bend=-1)
uke.leg('near', (ux + 44, 360), bend=-1)
tori.leg('near', (ux + 40, 410), bend=1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 70), bend=1)
s.add(tori); s.add(uke)
s.arrow((ux + 70, 150), (ux - 70, 90), (ux - 150, 330))
""")

scene('yoko_wakare', 'Yoko-wakare (5º kyô)', 'tori cai de lado estendendo as duas pernas à frente de uke e o lança por cima do corpo estendido.')("""
tori = Fig('tori', 300, 396, ang=272, facing=-1)
tori.leg('far', (412, 408), bend=1)
tori.leg('near', (420, 398), bend=1)
uke = Fig('uke', 382, 286, ang=238, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 20, GROUND - 2), bend=-1)
uke.leg('near', (ux + 44, 392), bend=-1)
uke.arm('near', (uke.neck[0] - 40, uke.neck[1] + 70), bend=1)
uke.arm('far', (uke.neck[0] - 20, uke.neck[1] + 80), bend=1)
tori.arm('near', uke.at(0.8), bend=-1)
tori.arm('far', uke.at(0.6), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 30, 220), (ux - 110, 170), (ux - 200, 340))
""")

scene('yoko_guruma', 'Yoko-guruma (5º kyô)', 'tori desliza a perna entre as pernas de uke, cai de lado e o projeta por cima da cabeça.')("""
tori = Fig('tori', 326, 398, ang=264, facing=-1)
tori.leg('far', (404, 404), bend=1)
uke = Fig('uke', 330, 246, ang=286, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 180), bend=-1)
uke.leg('near', (ux + 60, 340), bend=-1)
tori.leg('near', (ux + 30, 330), bend=1)
uke.arm('near', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
uke.arm('far', (uke.neck[0] - 10, uke.neck[1] + 70), bend=1)
tori.arm('near', uke.at(0.3), bend=-1)
tori.arm('far', uke.at(0.7), bend=-1)
s.add(tori); s.add(uke)
s.arrow((ux + 70, 150), (ux - 60, 80), (ux - 160, 320))
""")

scene('yoko_gake', 'Yoko-gake (5º kyô)', 'kuzushi flutuante; tori varre o pé de uke com a sola do pé e cai de lado, projetando-o.')("""
uke = Fig('uke', 332, 304, ang=222, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 22, GROUND - 2), bend=-1)
uke.leg('near', (ux - 18, 394), bend=-1)
tori = Fig('tori', 256, 372, ang=124, facing=1)
tori.leg('far', (206, GROUND - 4), bend=1)
tori.leg('near', (ux - 24, 400), bend=-1)
tori.arm('near', uke.at(0.85), bend=-1)
tori.arm('far', uke.at(0.55), bend=-1)
uke.arm('near', (uke.neck[0] - 46, uke.neck[1] + 40), bend=1)
uke.arm('far', (uke.neck[0] - 30, uke.neck[1] + 60), bend=1)
s.add(tori); s.add(uke)
s.arrow((uke.head[0] + 16, uke.head[1] - 14), (uke.head[0] - 80, uke.head[1] - 40), (uke.head[0] - 140, 320))
""")

scene('hane_makikomi', 'Hane-makikomi (4º kyô)', 'após hane-goshi, tori solta a mão, gira envolvendo o corpo de uke e cai para a frente junto com ele.')("""
tori = Fig('tori', 292, 334, ang=238, facing=-1)
tori.leg('far', (310, GROUND - 2), bend=1)
tori.leg('near', (350, 312), bend=-1)
uke = Fig('uke', 334, 282, ang=252, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 244), bend=-1)
uke.leg('near', (ux + 56, 330), bend=-1)
uke.arm('near', (tori.neck[0] - 10, tori.neck[1] + 40), bend=1)
uke.arm('far', (tori.neck[0] - 40, tori.neck[1] + 60), bend=1)
tori.arm('near', (tori.neck[0] - 60, 404), bend=1)
tori.arm('far', (tori.neck[0] - 80, tori.neck[1] + 50), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 210), (ux - 90, 150), (ux - 180, 360))
""")

scene('soto_makikomi', 'Soto-makikomi (4º kyô)', 'tori solta a pegada, gira, prende o braço de uke na axila e enrola o corpo dele ao seu redor.')("""
tori = Fig('tori', 296, 336, ang=246, facing=-1)
tori.leg('far', (318, GROUND - 2), bend=1)
tori.leg('near', (366, GROUND - 2), bend=1)
uke = Fig('uke', 334, 286, ang=254, facing=-1)
ux = uke.pelvis[0]
uke.leg('far', (ux + 70, 248), bend=-1)
uke.leg('near', (ux + 50, 340), bend=-1)
uke.arm('near', (tori.at(0.7)[0] - 50, tori.at(0.7)[1] + 20), bend=1)
uke.arm('far', (tori.neck[0] - 40, tori.neck[1] + 60), bend=1)
tori.arm('near', (tori.neck[0] - 40, 404), bend=1)
tori.arm('far', (tori.neck[0] - 70, tori.neck[1] + 54), bend=-1)
s.add(uke); s.add(tori)
s.arrow((ux + 50, 210), (ux - 90, 150), (ux - 180, 360))
""")

# ============================== ilustrações de seção ==============================
scene('ritsu_rei', 'Ritsu-rei (saudação em pé)', 'saudação de pé antes e depois da prática.')("""
tori = standing('tori', 200, 1, lean=30)
uke = standing('uke', 420, -1, lean=30)
for f in (tori, uke):
    f.arm('near', (f.pelvis[0] + 18 * f.facing, f.pelvis[1] + 36), bend=f.facing)
    f.arm('far', (f.pelvis[0] + 10 * f.facing, f.pelvis[1] + 40), bend=f.facing)
s.add(tori); s.add(uke)
""")

scene('za_rei', 'Za-rei (saudação ajoelhado)', 'saudação ajoelhada que abre os katas e as aulas.')("""
tori = kneeling('tori', 150, 1, lean=48)
uke = kneeling('uke', 470, -1, lean=48)
for f in (tori, uke):
    f.arm('near', (f.pelvis[0] + 92 * f.facing, GROUND - 6), bend=f.facing)
    f.arm('far', (f.pelvis[0] + 86 * f.facing, GROUND - 4), bend=f.facing)
s.add(tori); s.add(uke)
""")

scene('seiza', 'Seiza (estudo e concentração)', 'postura sentada sobre os calcanhares.')("""
tori = kneeling('tori', 300, 1, lean=0)
tori.arm('near', (tori.pelvis[0] + 46, tori.pelvis[1] - 10), bend=1)
tori.arm('far', (tori.pelvis[0] + 40, tori.pelvis[1] - 6), bend=1)
s.add(tori)
""")

scene('shizen_hontai', 'Shizen-hontai (postura natural)', 'postura natural fundamental, pés na largura dos ombros.')("""
tori = standing('tori', 300, 1, lean=0, stance=20)
tori.arm('near', (tori.pelvis[0] + 8, tori.pelvis[1] + 40), bend=1)
tori.arm('far', (tori.pelvis[0] - 2, tori.pelvis[1] + 42), bend=1)
s.add(tori)
""")

scene('kumikata', 'Kumi-kata (pegada básica)', 'mão direita na gola e esquerda na manga.')("""
tori = standing('tori', 250, 1, lean=4)
uke = standing('uke', 350, -1, lean=4)
grip(tori, uke)
s.add(uke); s.add(tori)
""")

scene('yoko_ukemi', 'Yoko-ukemi (queda lateral)', 'queda de lado com batida do braço no tatame.')("""
tori = Fig('tori', 300, 392, ang=104, facing=1)
tori.leg('far', (196, 404), bend=1)
tori.leg('near', (214, 350), bend=1)
tori.arm('far', (tori.neck[0] + 40, tori.neck[1] - 30), bend=-1)
tori.arm('near', (tori.pelvis[0] + 20, GROUND - 2), bend=1)
s.add(tori)
s.raw_front('<path d="M300 432 l-18 10 M320 434 l0 14 M340 432 l18 10" stroke="#D62828" stroke-width="5" stroke-linecap="round"/>')
""")

scene('ippon', 'Ippon (projeção completa)', 'uke projetado de costas, com controle de tori pela manga.')("""
uke = lying('uke', 260, -1, y=398)
tori = standing('tori', 412, -1, lean=30)
uke.arm('near', (346, 334), bend=1)
uke.arm('far', (uke.neck[0] - 30, 404), bend=1)
tori.arm('near', (346, 334), bend=-1)
tori.arm('far', (tori.neck[0] - 40, tori.neck[1] + 70), bend=-1)
s.add(uke); s.add(tori)
""")

scene('outorga', 'Entrega da faixa', 'o examinador entrega a nova faixa ao candidato.')("""
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
""")

scene('banca', 'Banca examinadora', 'candidato saúda a banca de três examinadores.')("""
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
""")

scene('faixas', 'Faixas do judô brasileiro', 'sequência de cores da CBJ, do 11º kyu ao 10º dan.')("""
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
""")

# ------------------------------------------------------------------------


def write_all(only=None):
    for name, (title, ref, code) in SCENES.items():
        if only and name not in only:
            continue
        path = os.path.join(HERE, f'fig_{name}.py')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(HEADER.format(title=title, ref=ref) + code + FOOTER.format(name=name))
    return len(SCENES)


if __name__ == '__main__':
    print(write_all(), 'scripts gerados')
