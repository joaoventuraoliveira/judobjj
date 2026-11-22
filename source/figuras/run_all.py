"""run_all.py — renderiza todos os fig_*.py e monta uma folha de contato para conferência."""
import glob, os, runpy, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

only = sys.argv[1:]
done = []
for path in sorted(glob.glob(os.path.join(HERE, 'fig_*.py'))):
    name = os.path.basename(path)[4:-3]
    if only and name not in only:
        continue
    runpy.run_path(path, run_name='__main__')
    done.append(name)

# folha de contato
cells = [Image.open(os.path.join(HERE, '..', 'png', n + '.png')) for n in done]
cw, ch = 520, 420
cols = 3
rows = (len(cells) + cols - 1) // cols
sheet = Image.new('RGBA', (cw * cols, ch * rows), (255, 255, 255, 255))
d = ImageDraw.Draw(sheet)
for i, (n, im) in enumerate(zip(done, cells)):
    im = im.copy(); im.thumbnail((cw - 20, ch - 40))
    x, y = (i % cols) * cw, (i // cols) * ch
    sheet.alpha_composite(im, (x + 10, y + 30))
    d.text((x + 10, y + 8), n, fill=(0, 0, 0, 255))
sheet.save(os.path.join(HERE, '..', 'contact_sheet.png'))
print(len(done), 'figuras')
