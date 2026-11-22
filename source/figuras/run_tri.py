"""run_tri.py — renderiza os tri_*.py (todos ou os nomes passados) e gera folhas de conferência."""
import glob, os, runpy, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
only = sys.argv[1:]
done = []
for path in sorted(glob.glob(os.path.join(HERE, 'tri_*.py'))):
    name = os.path.basename(path)[:-3]
    if only and name[4:] not in only:
        continue
    runpy.run_path(path, run_name='__main__')
    done.append(name)

# folhas de conferência: 4 figuras por folha
for k in range(0, len(done), 4):
    ims = [Image.open(os.path.join(HERE, '..', 'png', n + '.png')) for n in done[k:k + 4]]
    w = 1500
    ims = [im.resize((w, int(im.height * w / im.width))) for im in ims]
    sheet = Image.new('RGBA', (w, sum(i.height for i in ims) + 10 * len(ims)), 'white')
    y = 0
    for im in ims:
        sheet.alpha_composite(im, (0, y)); y += im.height + 10
    sheet.save(os.path.join(HERE, '..', f'tri_sheet_{k // 4 + 1}.png'))
print(len(done), 'figuras em três fases')
