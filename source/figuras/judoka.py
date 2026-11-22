"""
judoka.py — módulo base para desenhar judocas originais em SVG/PNG.

Cada figura do documento tem o seu próprio script (fig_*.py) que importa
este módulo, monta a cena (posição do tronco, alvos de mãos e pés) e chama
render(). As poses usam cinemática inversa de dois segmentos (braços e
pernas), então basta dizer onde a mão ou o pé deve chegar.

Convenções
- Tela de 600 x 460 unidades; chão em y = GROUND.
- Ângulos em graus: 0 = para baixo, 90 = para a direita, 180 = para cima,
  -90 (ou 270) = para a esquerda.
- TORI veste judogi branco; UKE veste judogi azul; ambos com faixa preta.
- Saída: SVG + PNG com fundo transparente (rsvg-convert).

Uso mínimo:
    from judoka import Fig, Scene
    s = Scene()
    t = s.add(Fig('tori', 240, 300, ang=180, facing=1))
    ...
    s.render('nome_do_arquivo')
"""
import math
import os
import subprocess

GROUND = 420
W, H = 600, 460
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Comprimentos dos segmentos (unidades da tela)
LEN = dict(ua=50, fa=46, th=62, sh=60, torso=90)

PALETTE = {
    'tori': dict(gi='#F7F7F4', shade='#D9D9D4', line='#3B3B3B'),
    'uke': dict(gi='#1F57B5', shade='#16438E', line='#0D2A5C'),
}
SKIN = '#E7B48C'
SKIN_LINE = '#8A5A3C'
HAIR = '#2A211C'
BELT = '#111111'
ARROW = '#D62828'


def vec(a, l):
    r = math.radians(a)
    return (math.sin(r) * l, math.cos(r) * l)


def add(p, v):
    return (p[0] + v[0], p[1] + v[1])


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def ik(root, target, l1, l2, bend):
    """Cinemática inversa de dois segmentos. bend = +1 ou -1 escolhe o lado da dobra."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy)
    d = max(min(d, l1 + l2 - 0.5), abs(l1 - l2) + 0.5)
    base = math.atan2(dy, dx)
    cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    a = math.acos(max(-1, min(1, cos_a)))
    ang = base + bend * a
    mid = (root[0] + math.cos(ang) * l1, root[1] + math.sin(ang) * l1)
    dir2 = math.atan2(target[1] - mid[1], target[0] - mid[0])
    end = (mid[0] + math.cos(dir2) * l2, mid[1] + math.sin(dir2) * l2)
    return mid, end


class Fig:
    """Um judoca. kind = 'tori' (branco) ou 'uke' (azul).
    (px, py) = pelve; ang = direção do tronco (180 = em pé); facing = +1 direita, -1 esquerda."""

    def __init__(self, kind, px, py, ang=180, facing=1, scale=1.0):
        self.kind, self.facing, self.s = kind, facing, scale
        self.pelvis = (px, py)
        self.ang = ang
        self.neck = add(self.pelvis, vec(ang, LEN['torso'] * scale))
        self.shoulder = add(self.pelvis, vec(ang, LEN['torso'] * 0.86 * scale))
        self.head = add(self.neck, vec(ang, 24 * scale))
        self.limbs = {}
        self.arms_top = False   # True = braços desenhados por cima de todos (pegada visível)

    # pontos úteis para mirar mãos e pés do parceiro
    def at(self, t):
        """Ponto no tronco: t=0 pelve, t=1 pescoço."""
        return lerp(self.pelvis, self.neck, t)

    def arm(self, which, target, bend=1):
        mid, end = ik(self.shoulder, target, LEN['ua'] * self.s, LEN['fa'] * self.s, bend)
        self.limbs['arm_' + which] = (self.shoulder, mid, end)
        return self

    def leg(self, which, target, bend=-1):
        mid, end = ik(self.pelvis, target, LEN['th'] * self.s, LEN['sh'] * self.s, bend)
        self.limbs['leg_' + which] = (self.pelvis, mid, end)
        return self

    # ---- desenho -------------------------------------------------------
    def _poly(self, pts, color, width):
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width:.1f}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')

    def _limb(self, key, far):
        if key not in self.limbs:
            return ''
        c = PALETTE[self.kind]
        root, mid, end = self.limbs[key]
        s = self.s
        out = []
        if key.startswith('arm'):
            cuff = lerp(mid, end, 0.78)
            out.append(self._poly([cuff, end], SKIN_LINE, 13 * s))
            out.append(self._poly([cuff, end], SKIN, 10 * s))
            out.append(f'<circle cx="{end[0]:.1f}" cy="{end[1]:.1f}" r="{8*s:.1f}" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="{1.6*s:.1f}"/>')
            out.append(self._poly([root, mid, cuff], c['line'], 25 * s))
            out.append(self._poly([root, mid, cuff], c['shade'] if far else c['gi'], 21 * s))
        else:
            ankle = lerp(mid, end, 0.9)
            fx = end[0] + 9 * s * self.facing_of_foot(mid, end)
            out.append(f'<ellipse cx="{fx:.1f}" cy="{end[1]:.1f}" rx="{13*s:.1f}" ry="{7*s:.1f}" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="{1.6*s:.1f}"/>')
            out.append(self._poly([root, mid, ankle], c['line'], 31 * s))
            out.append(self._poly([root, mid, ankle], c['shade'] if far else c['gi'], 27 * s))
        return '\n'.join(out)

    def facing_of_foot(self, mid, end):
        return self.facing

    def _torso(self):
        c = PALETTE[self.kind]
        s = self.s
        out = [self._poly([self.pelvis, self.neck], c['line'], 52 * s),
               self._poly([self.pelvis, self.neck], c['gi'], 48 * s)]
        # gola e lapela
        perp = vec(self.ang + 90 * self.facing, 1)
        front = add(self.at(0.97), (perp[0] * 12 * s, perp[1] * 12 * s))
        lap_end = add(self.at(0.18), (perp[0] * 2 * s, perp[1] * 2 * s))
        out.append(f'<circle cx="{self.neck[0]:.1f}" cy="{self.neck[1]:.1f}" r="{10*s:.1f}" fill="{SKIN}" stroke="{SKIN_LINE}" stroke-width="{1.4*s:.1f}"/>')
        out.append(self._poly([add(self.neck, (perp[0]*-8*s, perp[1]*-8*s)), front, lap_end], c['line'], 4 * s))
        return '\n'.join(out)

    def _belt(self):
        s = self.s
        perp = vec(self.ang + 90, 1)
        center = self.at(0.14)
        a = add(center, (perp[0] * 27 * s, perp[1] * 27 * s))
        b = add(center, (perp[0] * -27 * s, perp[1] * -27 * s))
        side = vec(self.ang + 90 * self.facing, 1)
        knot = add(center, (side[0] * 8 * s, side[1] * 8 * s))
        down = vec(self.ang + 180, 1)
        t1 = add(knot, (down[0] * 22 * s + side[0] * 5 * s, down[1] * 22 * s + side[1] * 5 * s))
        t2 = add(knot, (down[0] * 20 * s - side[0] * 6 * s, down[1] * 20 * s - side[1] * 6 * s))
        return '\n'.join([
            self._poly([a, b], BELT, 10 * s),
            self._poly([knot, t1], BELT, 6 * s),
            self._poly([knot, t2], BELT, 6 * s),
            f'<circle cx="{knot[0]:.1f}" cy="{knot[1]:.1f}" r="{5.5*s:.1f}" fill="{BELT}"/>'])

    def _head(self):
        s = self.s
        hx, hy = self.head
        back = vec(self.ang + 90 * -self.facing, 1)
        up = vec(self.ang, 1)
        cx, cy = hx + back[0] * 9 * s + up[0] * 8 * s, hy + back[1] * 9 * s + up[1] * 8 * s
        cid = f'h{id(self)}'
        return '\n'.join([
            f'<clipPath id="{cid}"><circle cx="{hx:.1f}" cy="{hy:.1f}" r="{17*s:.1f}"/></clipPath>',
            f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{17*s:.1f}" fill="{SKIN}"/>',
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{15*s:.1f}" fill="{HAIR}" clip-path="url(#{cid})"/>',
            f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{17*s:.1f}" fill="none" stroke="{SKIN_LINE}" stroke-width="{1.8*s:.1f}"/>'])

    def svg(self, arms=True):
        parts = [self._limb('arm_far', True) if arms else '', self._limb('leg_far', True),
                 self._torso(), self._belt(), self._limb('leg_near', False),
                 self._head(), self._limb('arm_near', False) if arms else '']
        return '\n'.join(p for p in parts if p)

    def arms_svg(self):
        return '\n'.join(p for p in (self._limb('arm_far', True), self._limb('arm_near', False)) if p)


class Scene:
    def __init__(self, width=W, height=H, shadow=True):
        self.w, self.h = width, height
        self.items = []
        self.extra_back = []
        self.extra_front = []
        self.shadow = shadow

    def add(self, fig):
        self.items.append(fig)
        return fig

    def arrow(self, p1, ctrl, p2, color=ARROW, width=5):
        """Seta curva indicando a direção do desequilíbrio ou da projeção."""
        d = f'M{p1[0]} {p1[1]} Q{ctrl[0]} {ctrl[1]} {p2[0]} {p2[1]}'
        self.extra_front.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-dasharray="2 10" marker-end="url(#arrow)"/>')

    def raw_back(self, s):
        self.extra_back.append(s)

    def raw_front(self, s):
        self.extra_front.append(s)

    def inner(self):
        """Conteúdo da cena sem o elemento <svg> (para montar painéis)."""
        full = self.to_svg()
        start = full.index('</defs>') + len('</defs>')
        return full[start:full.rindex('</svg>')]

    def to_svg(self):
        defs = ('<defs><marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" '
                'markerHeight="4" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="' + ARROW + '"/></marker></defs>')
        body = []
        if self.shadow:
            xs = [f.pelvis[0] for f in self.items] or [self.w / 2]
            cx = sum(xs) / len(xs)
            body.append(f'<ellipse cx="{cx:.1f}" cy="{GROUND+4}" rx="{150}" ry="10" fill="#000" fill-opacity="0.10"/>')
        body += self.extra_back
        body += [f.svg(arms=not f.arms_top) for f in self.items]
        body += [f.arms_svg() for f in self.items if f.arms_top]
        body += self.extra_front
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}">{defs}\n' + '\n'.join(body) + '\n</svg>')

    def render(self, name, px_width=2400, pad=60):
        """Gera SVG e PNG transparente, recortado no conteúdo com margem, 300 dpi."""
        svg_path = os.path.join(OUT, 'svg', name + '.svg')
        png_path = os.path.join(OUT, 'png', name + '.png')
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(self.to_svg())
        subprocess.run(['rsvg-convert', '-w', str(px_width), '-o', png_path, svg_path], check=True)
        from PIL import Image
        im = Image.open(png_path).convert('RGBA')
        box = im.getchannel('A').getbbox()
        if box:
            l, t, r, b = box
            im = im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))
        im.save(png_path, dpi=(300, 300))
        return png_path


# ---------- atalhos de pose ------------------------------------------------

def standing(kind, x, facing, lean=0, py=298, stance=24):
    """Judoca em pé (shizen-tai). lean > 0 inclina o tronco para a frente."""
    f = Fig(kind, x, py, ang=180 - lean * facing, facing=facing)
    f.leg('far', (x - stance * facing * 0.6, GROUND - 2), bend=-facing)
    f.leg('near', (x + stance * facing, GROUND - 2), bend=-facing)
    return f


def lying(kind, x, head_dir, y=398, facing=None):
    """Judoca deitado de costas. head_dir = +1 cabeça para a direita, -1 para a esquerda."""
    f = Fig(kind, x, y, ang=90 * head_dir, facing=facing or head_dir)
    f.leg('far', (x - 110 * head_dir, GROUND - 4), bend=head_dir)
    f.leg('near', (x - 100 * head_dir, GROUND - 30), bend=head_dir)
    return f


def kneeling(kind, x, facing, lean=0, seiza=True):
    """Judoca ajoelhado (seiza). lean inclina o tronco à frente (za-rei)."""
    f = Fig(kind, x, GROUND - 52, ang=180 - lean * facing, facing=facing)
    if seiza:
        f.limbs['leg_far'] = (f.pelvis, (x + 52 * facing, GROUND - 14), (x - 6 * facing, GROUND - 8))
        f.limbs['leg_near'] = (f.pelvis, (x + 58 * facing, GROUND - 12), (x - 2 * facing, GROUND - 6))
    return f


def grip(tori, uke):
    """Kumi-kata básico: mão direita na gola, esquerda na manga."""
    tori.arm('near', uke.at(0.82), bend=tori.facing)
    tori.arm('far', add(uke.at(0.55), (uke.facing * -10, 6)), bend=tori.facing)
    uke.arm('near', tori.at(0.82), bend=uke.facing)
    uke.arm('far', add(tori.at(0.55), (tori.facing * -10, 6)), bend=uke.facing)


# ---------- figuras em três fases (kuzushi · tsukuri · kake) ----------------

def kuzushi_arrow(scene, start, vec_xy, color=ARROW):
    """Seta reta e cheia: direção do desequilíbrio (kuzushi)."""
    x1, y1 = start
    x2, y2 = x1 + vec_xy[0], y1 + vec_xy[1]
    scene.raw_front(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="9" '
                    f'stroke-linecap="round" marker-end="url(#arrow)"/>')


def mark(scene, p, r=26, color=ARROW):
    """Círculo tracejado: ponto de contato preparado no tsukuri."""
    scene.raw_front(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="none" stroke="{color}" '
                    f'stroke-width="4" stroke-dasharray="8 6"/>')


PHASES = [('崩し', 'Kuzushi', 'desequilíbrio'), ('作り', 'Tsukuri', 'entrada / preparação'), ('掛け', 'Kake', 'execução / projeção')]
FONT = "Noto Sans CJK JP, DejaVu Sans, sans-serif"


def _esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def triptych(name, scenes, title, captions, px_width=3000, pad=40):
    """Monta 3 cenas lado a lado com títulos das fases e legendas. Gera SVG + PNG transparente 300 dpi."""
    cell, top = 620, 96
    total_w, total_h = cell * 3, top + 470 + 100
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" '
             f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ARROW}"/></marker></defs>',
             f'<text x="{total_w/2}" y="34" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="#1A1A1A">{_esc(title)}</text>']
    for i, (sc, (kanji, roma, pt), cap) in enumerate(zip(scenes, PHASES, captions)):
        x0 = i * cell
        parts.append(f'<text x="{x0 + cell/2}" y="84" text-anchor="middle" font-family="{FONT}" font-size="26" fill="#1A1A1A">'
                     f'<tspan font-weight="700">{i+1}. {kanji} {roma}</tspan><tspan fill="#555"> · {pt}</tspan></text>')
        parts.append(f'<g transform="translate({x0 - 20 + (cell - 620) / 2},{top - 100}) scale(1.1)">' + sc.inner() + '</g>')
        if badges and badges[i]:
            text, color = badges[i]
            w = 30 + len(text) * 15
            bx = x0 + cell / 2 - (w + 50) / 2
            parts.append(f'<g><circle cx="{bx+20}" cy="120" r="19" fill="none" stroke="{color}" stroke-width="6"/>'
                         f'<line x1="{bx+7}" y1="107" x2="{bx+33}" y2="133" stroke="{color}" stroke-width="6"/>'
                         f'<rect x="{bx+50}" y="102" width="{w}" height="36" rx="8" fill="{color}"/>'
                         f'<text x="{bx+50+w/2}" y="128" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
                         f'font-size="21" font-weight="700" fill="#FFFFFF">{text}</text></g>')
        y = top + 470 + 28
        for j, line in enumerate(_wrap(cap, 46 if n > 1 else 58)):
            parts.append(f'<text x="{x0 + cell/2}" y="{y + j*26}" text-anchor="middle" font-family="{FONT}" font-size="20" fill="#333">{_esc(line)}</text>')
        if i < 2:
            parts.append(f'<line x1="{x0+cell}" y1="70" x2="{x0+cell}" y2="{total_h-20}" stroke="#BBBBBB" stroke-width="2" stroke-dasharray="6 8"/>')
    parts.append('</svg>')
    svg_path = os.path.join(OUT, 'svg', name + '.svg')
    png_path = os.path.join(OUT, 'png', name + '.png')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    subprocess.run(['rsvg-convert', '-w', str(px_width), '-o', png_path, svg_path], check=True)
    from PIL import Image
    im = Image.open(png_path).convert('RGBA')
    box = im.getchannel('A').getbbox()
    if box:
        l, t, r, b = box
        im = im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))
    im.save(png_path, dpi=(300, 300))
    return png_path


def _wrap(text, n):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines


def badge(scene, text, color='#C8102E', x=470, y=40):
    """Selo de penalidade (ex.: HANSOKU-MAKE, SHIDO) com ícone de proibido."""
    w = 18 + len(text) * 13
    scene.raw_front(
        f'<g><circle cx="{x-34}" cy="{y}" r="22" fill="none" stroke="{color}" stroke-width="6"/>'
        f'<line x1="{x-49}" y1="{y-15}" x2="{x-19}" y2="{y+15}" stroke="{color}" stroke-width="6"/>'
        f'<rect x="{x-6}" y="{y-18}" width="{w}" height="36" rx="8" fill="{color}"/>'
        f'<text x="{x-6+w/2}" y="{y+8}" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
        f'font-size="20" font-weight="700" fill="#FFFFFF">{text}</text></g>')


def panels(name, scenes, heads, title, captions, px_width=None, pad=40, badges=None):
    """Monta N cenas lado a lado. heads = [(texto_negrito, texto_claro), ...].
    badges = [(texto, cor) ou None, ...] — selo de penalidade sob o título de cada quadro."""
    n = len(scenes)
    cell, top = (760 if n == 1 else 620), 96
    total_w, total_h = cell * n, top + 470 + 100
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">',
             '<defs><marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" '
             f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ARROW}"/></marker></defs>',
             f'<text x="{total_w/2}" y="34" text-anchor="middle" font-family="{FONT}" font-size="30" font-weight="700" fill="#1A1A1A">{_esc(title)}</text>']
    for i, (sc, (bold, light), cap) in enumerate(zip(scenes, heads, captions)):
        x0 = i * cell
        parts.append(f'<text x="{x0 + cell/2}" y="84" text-anchor="middle" font-family="{FONT}" font-size="26" fill="#1A1A1A">'
                     f'<tspan font-weight="700">{_esc(bold)}</tspan><tspan fill="#555"> {_esc(light)}</tspan></text>')
        parts.append(f'<g transform="translate({x0 - 20 + (cell - 620) / 2},{top - 100}) scale(1.1)">' + sc.inner() + '</g>')
        if badges and badges[i]:
            text, color = badges[i]
            w = 30 + len(text) * 15
            bx = x0 + cell / 2 - (w + 50) / 2
            parts.append(f'<g><circle cx="{bx+20}" cy="120" r="19" fill="none" stroke="{color}" stroke-width="6"/>'
                         f'<line x1="{bx+7}" y1="107" x2="{bx+33}" y2="133" stroke="{color}" stroke-width="6"/>'
                         f'<rect x="{bx+50}" y="102" width="{w}" height="36" rx="8" fill="{color}"/>'
                         f'<text x="{bx+50+w/2}" y="128" text-anchor="middle" font-family="DejaVu Sans, sans-serif" '
                         f'font-size="21" font-weight="700" fill="#FFFFFF">{text}</text></g>')
        y = top + 470 + 28
        for j, line in enumerate(_wrap(cap, 46 if n > 1 else 58)):
            parts.append(f'<text x="{x0 + cell/2}" y="{y + j*26}" text-anchor="middle" font-family="{FONT}" font-size="20" fill="#333">{_esc(line)}</text>')
        if i < n - 1:
            parts.append(f'<line x1="{x0+cell}" y1="70" x2="{x0+cell}" y2="{total_h-20}" stroke="#BBBBBB" stroke-width="2" stroke-dasharray="6 8"/>')
    parts.append('</svg>')
    svg_path = os.path.join(OUT, 'svg', name + '.svg')
    png_path = os.path.join(OUT, 'png', name + '.png')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    subprocess.run(['rsvg-convert', '-w', str(px_width or 1000 * n), '-o', png_path, svg_path], check=True)
    from PIL import Image
    im = Image.open(png_path).convert('RGBA')
    box = im.getchannel('A').getbbox()
    if box:
        l, t, r, b = box
        im = im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))
    im.save(png_path, dpi=(300, 300))
    return png_path
